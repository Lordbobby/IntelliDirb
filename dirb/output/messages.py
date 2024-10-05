from time import time_ns

from requests import Response

class Message:
    def __init__(self, message_type):
        self.type = message_type

    def to_csv_string(self, *args):
        fields = [
            str(time_ns()),
            self.type,
        ]

        [fields.append(str(arg)) for arg in args]
        [fields.append('') for _ in range(10 - len(fields))] # ensure 10 fields

        return ','.join(fields)

    def to_console_string(self, *args):
        args = [str(arg) for arg in args]

        return '\t'.join(args)

class ResponseMessage(Message):
    def __init__(self, response: Response):
        super().__init__('Response')

        self.response = response

    def to_csv_string(self):
        return super().to_csv_string(self.response.status_code, len(self.response.content), self.response.url)

    def to_console_string(self):
        return super().to_console_string(self.response.status_code, len(self.response.content), self.response.url)