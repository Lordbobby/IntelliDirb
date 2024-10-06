from queue import PriorityQueue

from dirb.util.prioritized_item import PrioritizedItem

class Priority:
    IMMEDIATE = 1
    NORMAL = 5

class RequestQueue(PriorityQueue):
    valid_urls = []

    def add_request(self, url, priority=Priority.NORMAL):
        self.put(PrioritizedItem(priority, url))

    def add_valid_url(self, url):
        self.valid_urls.append(url)

    def get(self, block = True, timeout = None):
        url = super().get(block, timeout).item

        while url in self.valid_urls:
            self.task_done()
            url = super().get(block, timeout).item

        return url