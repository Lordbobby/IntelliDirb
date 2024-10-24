from dirb.modes.parser.regex_based import RegexBasedParser

class HrefParser(RegexBasedParser):
    def __init__(self):
        super().__init__('href=[\'"]([^\s:?#\'&*"]+)[^:]\S*[\'"]')

    def find_paths_in_response(self, content, regex):
        matches = super().find_paths_in_response(content, regex)

        matches = [match for match in matches if not match.startswith('http')]

        return matches