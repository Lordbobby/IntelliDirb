import re

from dirb.modes.parser.parser import Parser

def calculate_base_url(response):
    base_url = re.findall('(.*/)', response.url)[0]

    return base_url

class RegexBasedParser(Parser):
    def __init__(self, regex):
        super().__init__()
        self.regex = regex

    def find_paths_in_response(self, content, regex):
        matches = re.findall(regex, content)

        return matches

    def parse(self, content, response, target):
        found_paths = self.find_paths_in_response(content, self.regex)
        request_urls = []

        base_url = calculate_base_url(response)

        for path in found_paths:
            url = f'{target}{path}'

            if not path.startswith('/'):
                url = f'{base_url}{path}'

            # collapse to clean it up
            url = url.replace('/./', '/')

            request_urls.append(url)

        return self._build_results(urls=request_urls)
