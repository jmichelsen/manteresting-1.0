import os
import urllib2
import urlparse

from django.views.generic import CreateView, UpdateView, DeleteView, TemplateView
from django.http import HttpResponseForbidden
from django.forms.models import modelform_factory
from django import forms
from django.core.files.base import ContentFile

from endless_pagination.views import AjaxListView

from .models import Nail, FriendFeed


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
    def get_form_class(self):
        form_class = super(UpdateNailView, self).get_form_class()
        form_class.base_fields['workbench'].queryset = self.request.user.workbenches.all()
        return form_class


class RenailView(UpdateByView):
    def get_form_class(self):
        Form = modelform_factory(Nail, exclude=['original'])
        Form.base_fields['description'].initial = self.object.description
        Form.base_fields['workbench'].queryset = self.request.user.workbenches.all()
        return Form

    def get_form_kwargs(self):
        """Set instance to null, because we want to create new object and update the old one.
        """
        kwargs = super(RenailView, self).get_form_kwargs()
        kwargs.pop('instance', None)
        return kwargs

    def form_valid(self, form):
        cloned_from = self.object

        self.object = form.save(commit=False)
        self.object.original = cloned_from.original
        self.object.source_url = cloned_from.source_url
        self.object.source_title = cloned_from.source_title
        self.object.cloned_from = cloned_from
        self.object.save()
        form.save_m2m()
        return super(RenailView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        data = super(RenailView, self).get_context_data(**kwargs)
        data['cloned_from'] = self.object
        return data


class DeleteNailView(RestrictToOwner, DeleteByView):
    def get_object(self):
        obj = super(DeleteNailView, self).get_object()
        self.success_url = obj.workbench.get_absolute_url()
        return obj


class DeleteWorkbenchView(RestrictToOwner, DeleteByView):
    def get_object(self):
        obj = super(DeleteWorkbenchView, self).get_object()
        self.success_url = obj.user.get_absolute_url()
        return obj


class AllNailsView(TemplateView):
    template_name = 'homepage.html'

    def get_context_data(self, **kwargs):
        data = super(AllNailsView, self).get_context_data(**kwargs)
        data['nails'] = Nail.objects.all().order_by('-id')[:100]
        data['main_menu_item'] = 'all'
        return data

'''class AjaxNailsView(TemplateView):
    template_name = 'homepage.html'

    def get_context_data(self, **kwargs):
        data = super(AllNailsView, self).get_context_data(**kwargs)
        if request.is_ajax()
            data['nails'] = Nail.objects.all().order_by('-timestamp')[:200]
            data['main_menu_item'] = 'all'
        return data
'''

class HomepageView(AllNailsView):
    """Does the same as AllNailsView for anonymous users,
    but shows only followed items for authorized.
    """

    def get_context_data(self, **kwargs):
        data = super(HomepageView, self).get_context_data(**kwargs)

        user = self.request.user
        if user.is_authenticated():
            #if FriendFeed.objects.filter(user=user).count() == 0:
            #    # trying to make a full update only
            #    # if feed is empty
            #    FriendFeed.rebuild_for(user)

            nails = [ff.nail for ff in user.friendfeed.order_by('-timestamp')[:40]]
            if nails:
                data['nails'] = nails
            else:
                data['nails'] = user.nails.all().order_by('-id')[:40]

            data['main_menu_item'] = 'workers-you-follow'


        return data


class AjaxAllNailsView(AjaxListView):
    """Shows all nails using infinite scrolling.
    """

    template_name = 'homepage.html'
    page_template = '_nails.html'

    def get_queryset(self):
        self.nails = Nail.objects.all().order_by('-id')
        return self.nails


    def get_context_data(self, **kwargs):
        data = super(AjaxAllNailsView, self).get_context_data(**kwargs)
        data['nails'] = self.nails
        data['main_menu_item'] = 'all'
        return data


class AjaxHomepageView(AjaxListView):
    """Does the same as AjaxAllNailsView for anonymous users,
    but shows only followed items for authorized.
    """

    template_name = 'homepage.html'
    page_template = '_nails.html'

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated():
            self.nails = [ff.nail for ff in user.friendfeed.order_by('-timestamp')]
            if not self.nails:
                self.nails = user.nails.all().order_by('-id')
        else:
            self.nails = Nail.objects.all().order_by('-id')
        return self.nails


    def get_context_data(self, **kwargs):
        data = super(AjaxHomepageView, self).get_context_data(**kwargs)
        user = self.request.user
        data['nails'] = self.nails
        if user.is_authenticated():
            data['main_menu_item'] = 'workers-you-follow'
        return data

