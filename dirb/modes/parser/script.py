import re

from dirb.modes.parser.regex_based import RegexBasedParser

def grab_script_data(content):
    script_data = re.findall('<script>(.*)</script>', content)

    return ' '.join(script_data)

class ScriptParser(RegexBasedParser):
    def __init__(self):
        super().__init__('[\'"]([^\'"]*)[\'"?]+')

    def find_paths_in_response(self, content, regex):
        js_strings = super().find_paths_in_response(content, regex)
        print(js_strings)
        paths = []

        for string in js_strings:
            if '/' not in string or '</' in string:
                continue

            if '//' not in string:
                paths.append(string)
                continue

            matches = re.findall('/(?<=(?<!/)/)(?!/)[^?:*&#\']+', string)
            [paths.append(match) for match in matches]

        return paths

    def parse(self, content, response, target):
        if not response.url.endswith('.js'):
            content = grab_script_data(content)

        return super().parse(content, response, target)