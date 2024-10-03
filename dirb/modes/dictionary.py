
from dirb.modes.mode import Mode

class Dictionary(Mode):

    def process_valid_response(self, response, output_queue):
        super().process_valid_response(response, output_queue)
