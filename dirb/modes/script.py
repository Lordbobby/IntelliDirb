from dirb.modes.dictionary import ParsedDictionary
from dirb.modes.parser.script import ScriptParser
from dirb.target import Target

class Script(ParsedDictionary):

    def __init__(self, wordlist, target: Target, extensions):
        super().__init__(wordlist, target, extensions)

        self.parsers = [ ScriptParser() ]