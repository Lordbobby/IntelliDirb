from dirb.modes.parser.filter.filter import ServiceFilter

class LiteSpeedFilter(ServiceFilter):
    def __init__(self):
        super().__init__('litespeed')

    def is_service(self, content, response):
        if 'Server' in response.headers and 'LiteSpeed' in response.headers['Server']:
            return True
        return False