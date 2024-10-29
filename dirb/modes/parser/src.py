from dirb.modes.parser.regex_based import RegexBasedParser

class SrcParser(RegexBasedParser):
    def __init__(self):
        super().__init__('src=[\'"]([^\s:?#\'"\(!]+)[\'"]')