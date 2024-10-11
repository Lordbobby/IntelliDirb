from dirb.modes.parser.regex_based import RegexBasedParser

class LinkParser(RegexBasedParser):
    def __init__(self, target):
        target = target.replace('/', '\\\\?/')
        super().__init__(f'{target}([^\s:?#\'"\r\n<]+)')