from queue import PriorityQueue

from dirb.util.prioritized_item import PrioritizedItem

class Priority:
    IMMEDIATE = 1
    NORMAL = 5

class RequestQueue(PriorityQueue):

    def add_request(self, url, priority=Priority.NORMAL):
        self.put(PrioritizedItem(priority, url))