import re

from dirb.modes.parser.filter.filter import ServiceFilter

class JoomlaFilter(ServiceFilter):
    def __init__(self):
        super().__init__('joomla')

    def is_service(self, content, response):
        return re.search('<meta .*name\s*=\s*["\']generator["\'][^>]*content\s*=\s*["\']Joomla!', content) is not None