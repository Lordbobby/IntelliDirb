import requests
from queue import Queue

from dirb.dirb_manager import DirbStatus
from dirb.target import Target


def send_queued_requests(target: Target, request_queue: Queue, response_queue: Queue, status: DirbStatus):
    while status.running:
        request_path = request_queue.get()
        request_url = target.build_url(request_path)

        response = requests.get(request_url)

        response_queue.put(response)

        request_queue.task_done()