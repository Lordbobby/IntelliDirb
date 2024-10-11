from queue import PriorityQueue

from dirb.util.prioritized_item import PrioritizedItem

class Priority:
    IMMEDIATE = 1
    NORMAL = 5

class RequestQueue(PriorityQueue):
    tested_urls = []

    def add_request(self, url, priority=Priority.NORMAL):
        if url in self.tested_urls:
            return

        self.tested_urls.append(url)
        self.put(PrioritizedItem(priority, url))

    def get(self, block = True, timeout = None):
        return super().get(block, timeout).item