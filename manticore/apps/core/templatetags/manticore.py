from django import template

register = template.Library()

@register.filter
def pdb(value):
    import pdb;
    pdb.set_trace()
    return value

