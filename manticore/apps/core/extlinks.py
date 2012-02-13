import re

class ExtlinksBlankMiddleware(object):
        '''
        Makes sure all external and only exernal links open in a new window.
        '''
        def __init__(self):
            self.targets = re.compile(r'''target=.\w*.''')
            self.extlinks = re.compile(r'''<a (?P<old>[^>]*http.?://)''')
        def process_response(self, request, response):
            if ("text" in response['Content-Type']):
                response.content = self.targets.sub('', response.content)
                response.content = self.extlinks.sub('<a target="_blank" \g<old>',response.content)
                return response
            else:
                return response
