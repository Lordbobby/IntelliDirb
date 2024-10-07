from dirb.modes.parser.regex_based import RegexBasedParser

class HrefParser(RegexBasedParser):
    def __init__(self):
        super().__init__('href=[\'"]([^\s:#\'"]+)[\'"]')