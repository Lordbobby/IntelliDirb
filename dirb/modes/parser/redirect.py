from dirb.modes.parser.parser import Parser

class RedirectParser(Parser):

    def __init__(self):
        super().__init__()

    def parse(self, content, response, target):
        urls = []

        if response.status_code == 301 and 'Location' in response.headers:
            urls.append(response.headers['Location'])

        return self._build_results(urls=urls)

