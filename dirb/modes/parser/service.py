import os
import sys

from dirb.modes.parser.filter.apache import ApacheFilter
from dirb.modes.parser.filter.joomla import JoomlaFilter
from dirb.modes.parser.filter.litespeed import LiteSpeedFilter
from dirb.modes.parser.filter.nginx import NginxFilter
from dirb.modes.parser.filter.php import PHPFilter
from dirb.modes.parser.filter.phpbb import PhpBBFilter
from dirb.modes.parser.filter.wordpress import WordPressFilter
from dirb.modes.parser.parser import Parser
from dirb.output import logger
from dirb.output.color import Color

WORDLIST_DIR = f'{os.path.dirname(sys.modules[__name__].__file__)}/wordlists/'

def build_results_from_wordlists(wordlists, target):
    urls = []
    words = []

    for wordlist in wordlists:
        with open(wordlist, 'r') as file:
            line = file.readline()
            while line:
                line = line.rstrip()

                if line.startswith('/'):
                    urls.append(f'{target}{line}')
                elif '/' in line:
                    urls.append(f'{target}/{line}')
                else:
                    words.append(line)

                line = file.readline()

    return {'urls': urls, 'words': words}

class ServiceParser(Parser):

    def __init__(self):
        super().__init__()

        self.filter_map = {
            ApacheFilter(): f'{WORDLIST_DIR}apache.txt',
            NginxFilter(): f'{WORDLIST_DIR}nginx.txt',
            PHPFilter(): f'{WORDLIST_DIR}PHP.fuzz.txt',
            WordPressFilter(): f'{WORDLIST_DIR}wordpress.fuzz.txt',
            JoomlaFilter(): f'{WORDLIST_DIR}urls-joomla-3.0.3.txt',
            LiteSpeedFilter(): f'{WORDLIST_DIR}litespeed.txt',
            PhpBBFilter(): f'{WORDLIST_DIR}phpBB.txt',
        }

        self.identified = []

    def parse(self, content, response, target):
        wordlists = []

        for service_filter, wordlist in self.filter_map.items():
            if service_filter.service_name in self.identified:
                continue

            if service_filter.is_service(content, response):
                logger.info(f'Identified service {Color.GREEN}{service_filter.service_name}{Color.RESET} from response.')

                wordlists.append(wordlist)
                self.identified.append(service_filter.service_name)

        return build_results_from_wordlists(wordlists, target)

