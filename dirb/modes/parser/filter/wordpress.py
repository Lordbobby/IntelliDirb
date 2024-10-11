from dirb.modes.parser.filter.filter import ServiceFilter


class WordPressFilter(ServiceFilter):
    def __init__(self):
        super().__init__('wordpress')

    def is_service(self, content, response):
        return 'wp-includes' in content and 'wp-content' in content