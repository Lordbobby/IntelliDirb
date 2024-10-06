from queue import Queue, PriorityQueue
from time import time_ns

from urllib3 import request

from dirb.enum.request_queue import RequestQueue
from dirb.enum.response_validator import ResponseValidator
from dirb.output import logger
from dirb.output.color import Color
from dirb.output.messages import ResponseMessage, StartMessage, FinishMessage
from dirb.target import Target
from dirb.util.prioritized_item import PrioritizedItem
from dirb.wordlist_file import WordlistFile

WORDS_TO_PULL = 100

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

class Mode:

    def __init__(self, wordlist: WordlistFile, target: Target, extensions):
        self.wordlist = wordlist
        self.target = target.get_base_url()
        self.extensions = create_extension_list(extensions)
        
        self.validator = ResponseValidator()
        self.stats = ModeStats()

        # tracking for wordlist
        self.current_directory = '/'
        self.directory_queue = Queue(maxsize=0)

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

        # Log summary
        run_time = (time_ns() - self.stats.start) / 1e9
        run_message = f'Finished enumerating in {Color.BLUE}{run_time:.2f}{Color.RESET} seconds.'
        requests_message = f'Sent {Color.BLUE}{self.stats.requests}{Color.RESET} requests.'
        responses_message = f'Identified {Color.GREEN}{self.stats.valid_responses}{Color.RESET} valid responses.'

        logger.info(f'{run_message} {requests_message} {responses_message}')

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

    def update_request_queue(self, request_queue):
        if self.wordlist.index >= self.wordlist.lines:
            self.reset_wordlist()
            return

        words = self.wordlist.get_words(WORDS_TO_PULL)

        logger.debug(f'Adding requests to queue based on {len(words)} words and this extension list: {self.extensions}')

        for extension in self.extensions:
            for word in words:
                self.stats.requests += 1
                request_queue.add_request(f'{self.target}{self.current_directory}{word}{extension}')

    def handle_responses(self, request_queue, response_queue, output_queue):
        # counter so it doesn't run forever
        processed = 0
        
        while not response_queue.empty() and processed < WORDS_TO_PULL:
            processed += 1
            response = response_queue.get()

            logger.debug(f'Mode processing response: [{response.status_code}] {response.url}')

            if not self.validator.validate_response(response):
                continue
            
            self.process_valid_response(response, request_queue, output_queue)

    def process_valid_response(self, response, request_queue, output_queue):
        logger.debug(f'Processing valid response: [{response.status_code}] {response.url}')
        output_queue.put(ResponseMessage(response))
        self.stats.valid_responses += 1
