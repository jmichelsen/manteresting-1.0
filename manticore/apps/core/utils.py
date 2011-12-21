from django.core.urlresolvers import reverse as _reverse

def reverse(view_name, *args, **kwargs):
    """More convient url reverse"""
    return _reverse(view_name, args=args, kwargs=kwargs)
