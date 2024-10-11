from dirb.modes.parser.filter.filter import ServiceFilter


class NginxFilter(ServiceFilter):
    def __init__(self):
        super().__init__('nginx')

    def is_service(self, content, response):
        if 'Server' in response.headers and 'nginx' in response.headers['Server']:
            return True
        return False