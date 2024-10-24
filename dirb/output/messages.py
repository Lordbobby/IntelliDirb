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

        return f'{color}{str(status_code):6}{reset} {self.tag:8} {lines:6} {size:8} {self.response.url}'

class LogMessage(Message):
    def __init__(self, message):
        super().__init__('LogMessage')

        self.message = message

    def to_csv_string(self):
        return ''

    def to_console_string(self):
        return self.message

class RecurseMessage(Message):
    def __init__(self, directory, excluded=False):
        super().__init__('Recurse')

        self.directory = directory
        self.excluded = excluded

    def to_csv_string(self):
        return super().to_csv_string(self.directory, self.excluded)

    def to_console_string(self):
        exclusion_msg = ''
        if self.excluded:
            exclusion_msg = f'{Color.RED}[NOT RECURSING]'

        return f'{Color.YELLOW} ->{Color.RESET} Identified likely directory: {Color.GREEN}{self.directory} {exclusion_msg}{Color.RESET}'

class SummaryMessage(Message):
    def __init__(self, stats):
        super().__init__('Summary')

        self.stats = stats

    def to_csv_string(self):
        return ''

    def to_console_string(self):
        header = f'\n{Color.BLUE}===={Color.RESET} Summary {Color.BLUE}===={Color.RESET}'
        summary = f'Finished enumerating in {Color.BLUE}{self.stats.get_total_time():.2f}{Color.RESET} seconds.'
        totals = f'Totals: {Color.GREEN}{self.stats.valid_responses}{Color.RESET} / {Color.RED}{self.stats.requests}{Color.RESET}'
        parser_header = '\nBreakdown by request origin:'
        lines = [header, summary, totals, parser_header]

        name_length = len(max(self.stats.parser_stats.keys(), key=len))
        valid_length = len(max([str(stat['valid']) for stat in self.stats.parser_stats.values()], key=len))

        for parser, stats in self.stats.parser_stats.items():
            parser_name = f'{parser}:'
            valid_num = f'{Color.GREEN}{str(stats["valid"]):{valid_length}}{Color.RESET}'
            total_num = f'{Color.BLUE}{str(stats["total"])}{Color.RESET}'

            lines.append(f'- {parser_name:{name_length + 1}} {valid_num} / {total_num}')

        return '\n'.join(lines)

class ParserStatMessage(Message):
    def __init__(self, parser, stats):
        super().__init__('ParserStat')

        self.parser = parser
        self.stats = stats

    def to_csv_string(self):
        return super().to_csv_string(self.parser, self.stats['valid'], self.stats['total'])
