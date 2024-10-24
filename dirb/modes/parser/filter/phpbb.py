from dirb.modes.parser.filter.filter import ServiceFilter

class PhpBBFilter(ServiceFilter):
    def __init__(self):
        super().__init__('phpbb')

    def is_service(self, content, response):
        return 'phpBB Limited' in content