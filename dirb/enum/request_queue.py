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

    def add_request(self, url, tag, priority=Priority.NORMAL):
        if url in self.tested_urls:
            return

        self.tested_urls.append(url)
        self.put(PrioritizedItem(priority, time.time_ns(), url, tag))

    def get(self, block = True, timeout = None):
        self.grabbed_urls += 1
        if self.grabbed_urls % 1000 == 0:
            logger.info(f'Sent {self.grabbed_urls} requests.')

        item = super().get(block, timeout)
        return item.item, item.tag