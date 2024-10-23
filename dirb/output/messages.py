from time import time_ns
from requests import Response

from dirb.output.color import Color

class Message:
    def __init__(self, message_type):
        self.creation_time = str(time_ns())
        self.type = message_type

    def to_csv_string(self, *args):
        fields = [
            self.creation_time,
            self.type,
        ]

        [fields.append(str(arg)) for arg in args]
        [fields.append('') for _ in range(6 - len(fields))] # ensure 5 fields

        return ','.join(fields)

    def to_console_string(self):
        return ''

class StartMessage(Message):
    def __init__(self):
        super().__init__('Start')

class FinishMessage(Message):
    def __init__(self, stats):
        super().__init__('Finish')
        self.stats = stats

    def to_csv_string(self):
        return super().to_csv_string(self.stats.requests, self.stats.valid_responses)

class ResponseMessage(Message):
    def __init__(self, response: Response, tag):
        super().__init__('Response')

        self.response = response
        self.tag = tag

    def to_csv_string(self):
        return super().to_csv_string(self.tag, self.response.status_code, len(self.response.content), self.response.url)

    def to_console_string(self):
        status_code = self.response.status_code
        size = f'{len(self.response.content)}c'
        lines = f'{self.response.content.count(0x0A)}l'
        color = Color.BLUE
        reset = Color.RESET

        if 200 <= status_code < 300:
            color = Color.GREEN

        if 300 <= status_code < 400:
            color = Color.YELLOW

        if 400 <= status_code:
            color = Color.RED

        return f'{color}{str(status_code):6}{reset} {self.tag:12} {lines:6} {size:8} {self.response.url}'

class LogMessage(Message):
    def __init__(self, message):
        super().__init__('LogMessage')

        self.message = message

    def to_csv_string(self):
        return ''

    def to_console_string(self):
        return self.message

class RecurseMessage(Message):
    def __init__(self, directory):
        super().__init__('Recurse')

        self.directory = directory

    def to_csv_string(self):
        return super().to_csv_string(self.directory)

    def to_console_string(self):
        return f'{Color.YELLOW} ->{Color.RESET} Identified likely directory: {Color.GREEN}{self.directory}{Color.RESET}'