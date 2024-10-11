from dirb.modes.parser.filter.filter import ServiceFilter


class ApacheFilter(ServiceFilter):
    def __init__(self):
        super().__init__('apache')

    def is_service(self, content, response):
        if 'Server' in response.headers and 'Apache' in response.headers['Server']:
            return True
        return False