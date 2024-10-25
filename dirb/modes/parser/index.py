from dirb.modes.parser.href import HrefParser

def is_index(content):
    return '<h1>Index of ' in content and '<address>' in content

class IndexParser(HrefParser):

    def parse(self, content, response, target):
        if not is_index(content):
            return self._build_results()

        results = super().parse(content, response, target)

        return results