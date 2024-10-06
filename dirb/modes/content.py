from dirb.enum.request_queue import RequestQueue
from dirb.modes.dictionary import Dictionary

class Content(Dictionary):

    def process_valid_response(self, response, request_queue: RequestQueue, output_queue):
        super().process_valid_response(response, request_queue, output_queue)
