class Parser:
    def parse(self, content, response, target):
        return []

    def _build_results(self, urls=None, words=None):
        results = {'urls': [], 'words': []}

        if urls is not None:
            results['urls'] = urls

        if words is not None:
            results['words']= words

        return results