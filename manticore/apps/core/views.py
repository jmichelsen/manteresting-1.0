from django.views.generic import CreateView, UpdateView
from django.http import HttpResponse, HttpResponseForbidden

class ImmediateHttpResponse(BaseException):
    def __init__(self, response):
        self.response = response


class ByMixin(object):
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

class ThrowResultMixin(object):
    """Allows to throw result on any stage of the request processing chain.
    """
    def dispatch(self, request, *args, **kwargs):
        try:
            return super(ThrowResultMixin, self).dispatch(request, *args, **kwargs)
        except ImmediateHttpResponse, e:
            return e.response


class RestrictToOwner(ThrowResultMixin):
    """This mixin restricts access to GET/POST and other operations to
    the objects owner.
    """
    owner_field = 'user'

    def get_object(self, *args, **kwargs):
        object = super(RestrictToOwner, self).get_object(*args, **kwargs)
        if not self.is_owner(self.request.user, object):
            raise ImmediateHttpResponse(HttpResponseForbidden())
        return object

    def is_owner(self, user, object):
        return getattr(object, self.owner_field) == user


class CreateByView(ByMixin, CreateView):
    pass

class UpdateByView(ByMixin, UpdateView):
    pass

class UpdateWorkbenchView(RestrictToOwner, UpdateByView):
    pass

class CreateNailView(ThrowResultMixin, CreateByView):
    def form_valid(self, form):
        if form.cleaned_data['workbench'].user != self.request.user:
            raise ImmediateHttpResponse(HttpResponseForbidden())
        return super(CreateNailView, self).form_valid(form)

    def get_form_class(self):
        form_class = super(CreateNailView, self).get_form_class()
        form_class.base_fields['workbench'].queryset = self.request.user.workbenches.all()
        return form_class

