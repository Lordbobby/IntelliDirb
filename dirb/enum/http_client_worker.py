import requests
from queue import Queue

from dirb.enum.request_queue import RequestQueue
from dirb.output import logger

def send_queued_requests(request_queue: RequestQueue, response_queue: Queue, status):
    logger.debug('Spinning up HTTP client worker...')

    while status.running:
        if request_queue.empty():
            continue

        request_url = request_queue.get()
        logger.debug(f'Sending request to: {request_url}')

        response = requests.get(request_url, allow_redirects=False)

        response_queue.put(response)
        request_queue.task_done()

    logger.debug('HTTP client worker finished.')