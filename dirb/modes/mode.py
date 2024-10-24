from queue import Queue
from time import time_ns

from dirb.enum.request_queue import Priority
from dirb.enum.response_validator import ResponseValidator
from dirb.output import logger
from dirb.output.color import Color
from dirb.output.messages import ResponseMessage, StartMessage, FinishMessage, SummaryMessage, ParserStatMessage
from dirb.target import Target
from dirb.wordlist.wordlist_file import WordlistFile

WORDS_TO_PULL = 500

def create_extension_list(extensions):
    result = ['']

    for extension in extensions.split(','):
        if not extension.startswith('.'):
            extension = f'.{extension}'

        result.append(extension)

    return result

class ModeStats:
    requests = 0
    valid_responses = 0
    start = 0
    finish = 0
    parser_stats = {}

    def get_total_time(self):
        return (self.finish - self.start) / 1e9

    def add_request(self, parser):
        if parser not in self.parser_stats:
            self.parser_stats[parser] = { 'total': 0, 'valid': 0 }

        self.parser_stats[parser]['total'] += 1
        self.requests += 1

    def add_valid(self, parser):
        if parser not in self.parser_stats:
            self.parser_stats[parser] = {'total': 0, 'valid': 0}

        self.parser_stats[parser]['valid'] += 1
        self.valid_responses += 1

class Mode:

    def __init__(self, wordlist: str, target: Target, extensions):
        self.wordlist = self.get_wordlist_file(wordlist)
        self.target = target.get_base_url()
        self.extensions = create_extension_list(extensions)
        
        self.validator = ResponseValidator()
        self.stats = ModeStats()

        # tracking for wordlist
        self.current_directory = '/'
        self.directory_queue = Queue(maxsize=0)

    def get_wordlist_file(self, wordlist_path):
        return WordlistFile(wordlist_path)

    def is_wordlist_not_exhausted(self):
        return self.wordlist.index < self.wordlist.lines or not self.directory_queue.empty()

    def enumerate(self, request_queue, response_queue, output_queue):
        logger.info('Beginning enumeration...')
        output_queue.put(StartMessage())
        self.stats.start = time_ns()

        while self.is_wordlist_not_exhausted() or not request_queue.empty() or not response_queue.empty():
            self.enumerate_wordlist(request_queue, response_queue, output_queue)

            # Ensure requests have finished
            request_queue.join()

        output_queue.put(FinishMessage(self.stats))
        self.stats.finish = time_ns()

        output_queue.put(SummaryMessage(self.stats))

        for parser, stats in self.stats.parser_stats.items():
            output_queue.put(ParserStatMessage(parser, stats))

    def enumerate_wordlist(self, request_queue, response_queue, output_queue):
        while self.is_wordlist_not_exhausted() or not request_queue.empty() or not response_queue.empty():
            self.handle_responses(request_queue, response_queue, output_queue)
            self.update_request_queue(request_queue)

    def recurse_directory(self, path: str):
        if not path.startswith('/'):
            path = f'/{path}'

        if not path.endswith('/'):
            path = f'{path}/'

        self.directory_queue.put(path)

    def reset_wordlist(self):
        if self.directory_queue.empty():
            return

        self.wordlist.reset_index()
        self.current_directory = self.directory_queue.get()
        logger.debug(f'Reset wordlist with new directory: {self.current_directory}')

    def add_request(self, request_queue, url, tag, priority=Priority.NORMAL):
        if url in request_queue.tested_urls:
            return

        self.stats.add_request(tag)
        request_queue.add_request(url, tag, priority)

    def update_request_queue(self, request_queue):
        if self.wordlist.index >= self.wordlist.lines:
            self.reset_wordlist()
            return

        if request_queue.qsize() > WORDS_TO_PULL * 10:
            logger.debug('Queue sufficiently full, skipping adding requests for now.')
            return

        words = self.wordlist.get_words(WORDS_TO_PULL)

        logger.debug(f'Adding requests to queue based on {len(words)} words and this extension list: {self.extensions}')

        for word, tag in words:
            for extension in self.extensions:
                if len(extension) and word.endswith(extension):
                    continue

                self.add_request(request_queue, f'{self.target}{self.current_directory}{word}{extension}', tag)

    def handle_responses(self, request_queue, response_queue, output_queue):
        # counter so it doesn't run forever
        processed = 0
        
        while not response_queue.empty() and processed < WORDS_TO_PULL:
            processed += 1
            response, tag = response_queue.get()

            logger.debug(f'Mode processing response: [{response.status_code}] {response.url}')

            if not self.validator.validate_response(response):
                continue
            
            self.process_valid_response(response, tag, request_queue, output_queue)

    def process_valid_response(self, response, tag, request_queue, output_queue):
        logger.debug(f'Processing valid response: [{response.status_code}] {response.url}')
        output_queue.put(ResponseMessage(response, tag))

        self.stats.add_valid(tag)