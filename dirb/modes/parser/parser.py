class Parser:
    def __init__(self):
        self.name = type(self).__name__
        self.tag = self.name.replace('Parser', '')

    def parse(self, content, response, target):
        return []

    def _build_results(self, urls=None, words=None):
        results = {'urls': [], 'words': []}

        if urls is not None:
            results['urls'] = list(set(urls))

        if words is not None:
            results['words'] = list(set(words))

        return results