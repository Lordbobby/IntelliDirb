from dirb.modes.dictionary import ParsedDictionary
from dirb.modes.parser.href import HrefParser
from dirb.modes.parser.index import IndexParser
from dirb.modes.parser.link import LinkParser
from dirb.modes.parser.redirect import RedirectParser
from dirb.modes.parser.script import ScriptParser
from dirb.modes.parser.service import ServiceParser
from dirb.modes.parser.src import SrcParser
from dirb.target import Target


class Combined(ParsedDictionary):

    def __init__(self, wordlist, target: Target, extensions, excluded_dirs):
        super().__init__(wordlist, target, extensions, excluded_dirs)

        self.parsers = [ IndexParser(), HrefParser(), SrcParser(), LinkParser(self.target), ScriptParser(), ServiceParser(), RedirectParser() ]