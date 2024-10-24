import re

from dirb.modes.parser.parser import Parser

def calculate_base_url(response):
    base_url = re.findall('(.*/)', response.url)[0]

    return base_url

def collapse_url(url):
    orig_url = url
    iterations = 0

    while url.find('../') != -1 and iterations < 10:
        end = url.find('../')
        start = url.rfind('/', 0, end)
        start = url.rfind('/', 0, start) + 1
        end = end + 3
        url = url[:start] + url[end:]

        iterations += 1

    if iterations == 10:
        return orig_url

    return url

class RegexBasedParser(Parser):
    def __init__(self, regex):
        super().__init__()
        self.regex = regex

    def find_paths_in_response(self, content, regex):
        matches = re.findall(regex, content)

        return matches

    def parse(self, content, response, target):
        if response.url.split('.')[:-1] in ['jpg', 'png', 'svg', 'gif', 'woff2']:
            return self._build_results()

        found_paths = self.find_paths_in_response(content, self.regex)
        request_urls = []

        base_url = calculate_base_url(response)

        for path in found_paths:
            path = path.replace('\/', '/')

            url = f'{target}{path}'

            if not path.startswith('/'):
                url = f'{base_url}{path}'

            # collapse to clean it up
            url = url.replace('/./', '/')
            url = collapse_url(url)

            request_urls.append(url)

        return self._build_results(urls=request_urls)
