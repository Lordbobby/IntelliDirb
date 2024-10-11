import time
from queue import PriorityQueue

from dirb.output import logger
from dirb.util.prioritized_item import PrioritizedItem

class Priority:
    IMMEDIATE = 1
    NORMAL = 5

class RequestQueue(PriorityQueue):
    tested_urls = []
    grabbed_urls = 0

    def add_request(self, url, priority=Priority.NORMAL):
        if url in self.tested_urls:
            return

        self.tested_urls.append(url)
        self.put(PrioritizedItem(priority, time.time_ns(), url))

    def get(self, block = True, timeout = None):
        self.grabbed_urls += 1
        if self.grabbed_urls % 1000:
            logger.info(f'Sent {self.grabbed_urls} requests.')

        return super().get(block, timeout).item