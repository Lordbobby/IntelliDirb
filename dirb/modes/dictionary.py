from dirb.enum.request_queue import RequestQueue, Priority
from dirb.modes.mode import Mode
from dirb.output import logger
from dirb.output.color import Color
from dirb.output.messages import RecurseMessage
from dirb.target import Target
from dirb.wordlist_file import WordlistFile


def can_recurse(response):
    request_url = response.request.url
    if 'Location' in response.headers and f'{request_url}/'.endswith(response.headers['Location']):
        return True
    return False

class Dictionary(Mode):

    def process_valid_response(self, response, request_queue: RequestQueue, output_queue):
        super().process_valid_response(response, request_queue, output_queue)

        if can_recurse(response):
            directory = response.headers['Location']

            self.recurse_directory(directory)
            output_queue.put(RecurseMessage(directory))
            logger.debug(f'Recursing {directory} from response url {response.url} and request url {response.request.url}')

class ParsedDictionary(Dictionary):
    def __init__(self, wordlist: WordlistFile, target: Target, extensions):
        super().__init__(wordlist, target, extensions)

        self.parsers = []

    def process_valid_response(self, response, request_queue: RequestQueue, output_queue):
        super().process_valid_response(response, request_queue, output_queue)

        # If no page content, ignore
        if not len(response.content):
            return

        content = str(response.content)

        for parser in self.parsers:
            request_urls = parser.parse_for_requests(content, response, self.target)
            words = parser.parse_for_words(content, response)

            logger.debug(f'Ran {parser} against response content and got {len(request_urls)} URLs and {len(words)} words.')

            if len(request_urls):
                self.add_requests(request_urls, request_queue)

            if len(words):
                self.add_words(words)

    def add_requests(self, request_urls, request_queue):
        for url in request_urls:
            self.add_request(request_queue, url, priority=Priority.IMMEDIATE)

            logger.debug(f'Adding request from page content: {url}')

        logger.info(f'Found {Color.GREEN}{len(request_urls)}{Color.RESET} URL from page content.')

    def add_words(self, words):
        # TODO add words to supplemental wordlist
        logger.info(f'Adding {len(words)} words to supplemental wordlist.')