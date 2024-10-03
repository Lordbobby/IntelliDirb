import requests
from queue import Queue

from dirb.dirb_manager import DirbStatus

def send_queued_requests(request_queue: Queue, response_queue: Queue, status: DirbStatus):
    while status.running:
        request_url = request_queue.get()
        response = requests.get(request_url)

        response_queue.put(response)

        request_queue.task_done()