from dirb.modes.dictionary import ParsedDictionary
from dirb.modes.parser.href import HrefParser
from dirb.modes.parser.src import SrcParser
from dirb.target import Target
from dirb.wordlist_file import WordlistFile

class Content(ParsedDictionary):

    def __init__(self, wordlist: WordlistFile, target: Target, extensions):
        super().__init__(wordlist, target, extensions)

        self.parsers = [ HrefParser(), SrcParser() ]