from dirb.modes.parser.filter.filter import ServiceFilter


class PHPFilter(ServiceFilter):
    def __init__(self):
        super().__init__('php')

    def is_service(self, content, response):
        return response.url.endswith('.php') and response.status_code == 200