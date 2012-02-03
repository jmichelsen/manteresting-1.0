from django import template

register = template.Library()

@register.filter
def pdb(value):
    import pdb;
    pdb.set_trace()
    return value


@register.tag
def bookmarklet(parser, token):
    try:
        tag_name, name = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError("%r tag requires exactly one argument" % token.split_contents()[0])

    if not (name[0] == name[-1] and name[0] in ('"', "'")):
        raise template.TemplateSyntaxError("%r tag's argument should be in quotes" % tag_name)

    nodelist = parser.parse(('endbookmarklet',))
    parser.delete_first_token()
    return BookmarkletNode(nodelist, name[1:-1])


class BookmarkletNode(template.Node):
    def __init__(self, nodelist, name):
        self.nodelist = nodelist
        self.name = name

    def render(self, context):
        output = self.nodelist.render(context)
        code = ''.join(
            line.strip()
            for line in output.split('\n')
        )
        return '<a href="{0}">{1}</a>'.format(code, self.name)

