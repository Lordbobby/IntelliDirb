import re
from time import time_ns

from dirb.enum.request_queue import RequestQueue, Priority
from dirb.modes.mode import Mode
from dirb.output import logger
from dirb.output.messages import RecurseMessage
from dirb.target import Target
from dirb.util.settings import Settings
from dirb.wordlist.extended_wordlist import ExtendedWordlist

def can_recurse(response):
    request_url = response.request.url
    if 'Location' in response.headers and f'{request_url}/'.endswith(response.headers['Location']):
        return True
    return False

class Dictionary(Mode):
    def process_valid_response(self, response, tag, request_queue: RequestQueue, output_queue):
        super().process_valid_response(response, tag, request_queue, output_queue)

        if can_recurse(response) and Settings.can_recurse:
            directory = response.headers['Location']
            directory = re.findall('(?<=(?<!/)/)(?!/)[^?&#]+', directory)[0]

            self.recurse_directory(directory)
            output_queue.put(RecurseMessage(directory))
            logger.debug(f'Recursing {directory} from response url {response.url} and request url {response.request.url}')

class ParsedDictionary(Dictionary):
    def __init__(self, wordlist, target: Target, extensions):
        super().__init__(wordlist, target, extensions)

        self.parsers = []

    def get_wordlist_file(self, wordlist_path):
        return ExtendedWordlist(wordlist_path)

    def process_valid_response(self, response, tag, request_queue: RequestQueue, output_queue):
        super().process_valid_response(response, tag, request_queue, output_queue)

        # If no page content, ignore
        if not len(response.content):
            return

        content = response.text

        total_urls = 0
        total_words = 0

        for parser in self.parsers:
            start = time_ns()
            parsed_results = parser.parse(content, response, self.target)
            total_time = time_ns() - start
            request_urls = parsed_results['urls']
            words = parsed_results['words']

            len_urls = len(request_urls)
            len_words = len(words)

            logger.debug(f'Ran {parser.name} against response content in {total_time/1e9:.2f} seconds and got {len_urls} URLs and {len_words} words.')

            if len_urls:
                self.add_requests(request_urls, request_queue, parser.tag)
                total_urls += len_urls

            if len_words:
                self.add_words(words, parser.tag)
                total_words += len_words

        if total_urls or total_words:
            logger.debug(f'Parsers identified {total_urls} URLS and {total_words} words from {response.url} response.')

    def add_requests(self, request_urls, request_queue, tag):
        for url in request_urls:
            self.add_request(request_queue, url, tag, priority=Priority.IMMEDIATE)

            logger.debug(f'Adding request from page content: {url}')

    def add_words(self, words, tag):
        self.wordlist.add_words(words, tag)