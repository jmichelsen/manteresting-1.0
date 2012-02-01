import os
import urllib2
import urlparse

from django.views.generic import CreateView, UpdateView, DeleteView, TemplateView
from django.http import HttpResponseForbidden
from django.forms.models import modelform_factory
from django import forms
from django.core.files.base import ContentFile

from .models import Nail


class ImmediateHttpResponse(BaseException):
    def __init__(self, response):
        self.response = response


class ThrowResultMixin(object):
    """Allows to throw result on any stage of the request processing chain.
    """
    def dispatch(self, request, *args, **kwargs):
        try:
            return super(ThrowResultMixin, self).dispatch(request, *args, **kwargs)
        except ImmediateHttpResponse, e:
            return e.response


class RequireLogin(object):
    """This mixin restricts access for anonymous users.
    """
    def get(self, request, *args, **kwargs):
        self._check(request)
        return super(RequireLogin, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self._check(request)
        return super(RequireLogin, self).post(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        self._check(request)
        return super(RequireLogin, self).delete(request, *args, **kwargs)

    def _check(self, request):
        if request.user.is_anonymous():
            raise ImmediateHttpResponse(HttpResponseForbidden())


class ByMixin(ThrowResultMixin, RequireLogin):
    """This mixin sets given field to current logged user.

    Useful, when you want create object to be owned by those
    user, who submitted the form.
    """
    by_user_field = 'user'

    def get_form_kwargs(self):
        """
        Returns the keyword arguments for instanciating the form.
        """
        kwargs = super(ByMixin, self).get_form_kwargs()
        if self.request.method in ('POST', 'PUT'):
            if not self.request.user.is_anonymous():
                data = kwargs.setdefault('data', self.request.POST).copy()
                data.setdefault(self.by_user_field, self.request.user.pk)
                kwargs['data'] = data
        return kwargs


class RestrictToOwner(ThrowResultMixin):
    """This mixin restricts access to GET/POST and other operations to
    the objects owner.
    """
    owner_field = 'user'

    def get_object(self, *args, **kwargs):
        obj = super(RestrictToOwner, self).get_object(*args, **kwargs)
        if not self.is_owner(self.request.user, obj):
            raise ImmediateHttpResponse(HttpResponseForbidden())
        return obj

    def is_owner(self, user, obj):
        return getattr(obj, self.owner_field) == user


class CreateByView(ByMixin, CreateView):
    pass


class UpdateByView(ByMixin, UpdateView):
    pass


class DeleteByView(ByMixin, DeleteView):
    pass


class UpdateWorkbenchView(RestrictToOwner, UpdateByView):
    pass


class CreateNailView(CreateByView):
    def get_form_class(self):
        BaseForm = super(CreateNailView, self).get_form_class()
        request = self.request

        class Form(BaseForm):
            if 'media' in request.GET:
                media = forms.URLField(widget=forms.HiddenInput)

            def __init__(self, *args, **kwargs):
                kwargs.setdefault('initial', {})
                kwargs['initial'].update(
                    dict(
                        media=request.GET.get('media'),
                        source_url=request.GET.get('source_url'),
                        source_title=request.GET.get('source_title'),
                    )
                )

                super(Form, self).__init__(*args, **kwargs)

                if 'media' in request.GET:
                    del self.fields['original']

                self.fields['workbench'].queryset = request.user.workbenches.all()
                self.fields['source_url'].widget = forms.HiddenInput()
                self.fields['source_title'].widget = forms.HiddenInput()

            def save(self, *args, **kwargs):
                kwargs['commit'] = False
                instance = super(Form, self).save(*args, **kwargs)

                if 'media' in self.cleaned_data:
                    url = self.cleaned_data['media']
                    path = urlparse.urlparse(url).path.rstrip('/')
                    filename = os.path.basename(path)
                    response = urllib2.urlopen(
                        url,
                        timeout=15,
                    )
                    code = response.getcode()

                    if code < 200 or code >= 300:
                        raise RuntimeError(u'Can\'t download file from "%s"' % url)

                    instance.original.save(
                        filename,
                        ContentFile(response.read()),
                    )

                    if not instance.source_url:
                        instance.source_url = url

                    if instance.source_url and not instance.source_title:
                        instance.source_title = urlparse.urlparse(instance.source_url).netloc
                else:
                    instance.source_title = u'Uploaded by user'

                instance.save()
                self.save_m2m()
                return instance

        return Form


class UpdateNailView(RestrictToOwner, UpdateByView):
    def is_owner(self, user, obj):
        return obj.workbench.user == user

    def get_form_class(self):
        form_class = super(UpdateNailView, self).get_form_class()
        form_class.base_fields['workbench'].queryset = self.request.user.workbenches.all()
        return form_class


class RepinNailView(UpdateByView):
    def get_form_class(self):
        RepinForm = modelform_factory(Nail, exclude=['original'])
        RepinForm.base_fields['description'].initial = self.object.description
        RepinForm.base_fields['workbench'].queryset = self.request.user.workbenches.all()
        return RepinForm

    def get_form_kwargs(self):
        """Set instance to null, because we want to create new object and update the old one.
        """
        kwargs = super(RepinNailView, self).get_form_kwargs()
        kwargs.pop('instance', None)
        return kwargs

    def form_valid(self, form):
        cloned_from = self.object

        self.object = form.save(commit=False)
        self.object.original = cloned_from.original
        self.object.cloned_from = cloned_from
        self.object.save()
        form.save_m2m()
        return super(RepinNailView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        data = super(RepinNailView, self).get_context_data(**kwargs)
        data['cloned_from'] = self.object
        return data


class DeleteNailView(RestrictToOwner, DeleteByView):
    def is_owner(self, user, obj):
        return obj.workbench.user == user

    def get_object(self):
        obj = super(DeleteNailView, self).get_object()
        self.success_url = obj.workbench.get_absolute_url()
        return obj


class DeleteWorkbenchView(RestrictToOwner, DeleteByView):
    def get_object(self):
        obj = super(DeleteWorkbenchView, self).get_object()
        self.success_url = obj.user.get_absolute_url()
        return obj


class HomepageView(TemplateView):
    template_name = 'homepage.html'

    def get_context_data(self, **kwargs):
        data = super(HomepageView, self).get_context_data(**kwargs)
        data['nails'] = Nail.objects.all().order_by('-id')[:20]
        return data

