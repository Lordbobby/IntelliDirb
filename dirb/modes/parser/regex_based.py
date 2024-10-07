import re

from dirb.modes.parser.parser import Parser

def find_paths_in_response(content, regex):
    matches = re.findall(regex, content)

    return matches

def calculate_base_url(response):
    base_url = re.findall('(.*/)', response.url)[0]

    return base_url

class RegexBasedParser(Parser):
    def __init__(self, regex):
        self.regex = regex

    def parse_for_requests(self, content, response, target):
        found_paths = find_paths_in_response(content, self.regex)
        request_urls = []

        base_url = calculate_base_url(response)

        for path in found_paths:
            url = f'{target}/{path}'

            if not path.startswith('/'):
                url = f'{base_url}{path}'

            request_urls.append(url)

        return request_urls
