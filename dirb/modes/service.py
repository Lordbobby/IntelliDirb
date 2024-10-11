from dirb.modes.dictionary import ParsedDictionary
from dirb.modes.parser.service import ServiceParser
from dirb.target import Target

class Service(ParsedDictionary):

    def __init__(self, wordlist, target: Target, extensions):
        super().__init__(wordlist, target, extensions)

        self.parsers = [ ServiceParser() ]