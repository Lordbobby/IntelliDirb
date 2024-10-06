from dirb.enum.request_queue import RequestQueue
from dirb.modes.mode import Mode
from dirb.output import logger
from dirb.output.messages import RecurseMessage

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
