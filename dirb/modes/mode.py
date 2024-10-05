from queue import Queue

from dirb.enum.response_validator import ResponseValidator
from dirb.output import logger
from dirb.output.messages import ResponseMessage
from dirb.target import Target
from dirb.wordlist_file import WordlistFile

WORDS_TO_PULL = 100

def create_extension_list(extensions):
    result = ['']

    for extension in extensions.split(','):
        if not extension.startswith('.'):
            extension = f'.{extension}'

        result.append(extension)

    return result

class Mode:

    def __init__(self, wordlist: WordlistFile, target: Target, extensions):
        self.wordlist = wordlist
        self.target = target.get_base_url()
        self.extensions = create_extension_list(extensions)
        
        self.validator = ResponseValidator()

        # tracking for wordlist
        self.current_directory = '/'
        self.directory_queue = Queue(maxsize=0)

    def is_wordlist_not_exhausted(self):
        return self.wordlist.index < self.wordlist.lines or not self.directory_queue.empty()

    def enumerate(self, request_queue, response_queue, output_queue):
        logger.debug('Mode is beginning enumeration...')

        while self.is_wordlist_not_exhausted() or not request_queue.empty() or not response_queue.empty():
            self.handle_responses(response_queue, output_queue)

            self.update_request_queue(request_queue)

        logger.debug('Mode is finished enumerating.')

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

    def update_request_queue(self, request_queue):
        words = self.wordlist.get_words(WORDS_TO_PULL)

        logger.debug(f'Adding requests to queue based on {len(words)} words and this extension list: {self.extensions}')

        for extension in self.extensions:
            for word in words:
                url = f'{self.target}{self.current_directory}{word}{extension}'
                logger.debug(f'Adding request: {url}')
                request_queue.put(f'{self.target}{self.current_directory}{word}{extension}')

        if len(words) < WORDS_TO_PULL:
            self.reset_wordlist()

    def handle_responses(self, response_queue: Queue, output_queue):
        # counter so it doesn't run forever
        processed = 0
        
        while not response_queue.empty() and processed < WORDS_TO_PULL:
            logger.debug('Mode processing response.')

            processed += 1
            response = response_queue.get()
            
            if not self.validator.validate_response(response):
                pass
            
            self.process_valid_response(response, output_queue)

    def process_valid_response(self, response, output_queue):
        logger.debug(f'Processing valid response: [{response.status_code}] {response.url}')
        output_queue.put(ResponseMessage(response))
