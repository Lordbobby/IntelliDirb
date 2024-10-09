from dirb.modes.dictionary import ParsedDictionary
from dirb.modes.parser.href import HrefParser
from dirb.modes.parser.script import ScriptParser
from dirb.modes.parser.src import SrcParser
from dirb.target import Target
from dirb.wordlist.wordlist_file import WordlistFile

class Combined(ParsedDictionary):

    def __init__(self, wordlist, target: Target, extensions):
        super().__init__(wordlist, target, extensions)

        self.parsers = [ HrefParser(), SrcParser(), ScriptParser() ]