from django.views.generic import CreateView, UpdateView, DeleteView, TemplateView
from django.http import HttpResponseForbidden

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
    def form_valid(self, form):
        if form.cleaned_data['workbench'].user != self.request.user:
            raise ImmediateHttpResponse(HttpResponseForbidden())
        return super(CreateNailView, self).form_valid(form)

    def get_form_class(self):
        form_class = super(CreateNailView, self).get_form_class()
        form_class.base_fields['workbench'].queryset = self.request.user.workbenches.all()
        return form_class


class UpdateNailView(RestrictToOwner, UpdateByView):
    def is_owner(self, user, obj):
        return obj.workbench.user == user


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
        data['nails'] = Nail.objects.all()[:20]
        return data

