from dirb.modes.parser.href import HrefParser

class IndexParser(HrefParser):

    def parse(self, content, response, target):
        if '<h1>Index of ' not in content and '<address>' not in content:
            return self._build_results()

        results = super().parse(content, response, target)

        return results