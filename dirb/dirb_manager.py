import time
from queue import Queue
from threading import Thread

from dirb.enum.http_client_worker import send_queued_requests
from dirb.output.output_worker import handle_output

class DirbStatus:
    def __init__(self):
        self.running = True
        self.start_time = time.time_ns()

class DirbManager:
    def __init__(self, mode, output_handler, num_threads=10):
        self.mode = mode
        self.output_handler = output_handler
        self.num_threads = num_threads

    def enumerate(self):
        status = DirbStatus()

        # The max number of requests in the queue at any given time
        max_requests_in_queue = self.num_threads*1000

        # Queues are used to pass information between threads
        request_queue = Queue(maxsize=max_requests_in_queue)
        response_queue = Queue(maxsize=0)
        output_queue = Queue(maxsize=0)

        # Spin up request worker threads
        request_workers = []

        for i in range(self.num_threads):
            request_worker = Thread(target=send_queued_requests, args=(request_queue, response_queue, status))
            request_worker.daemon = True
            request_worker.start()

            request_workers.append(request_worker)

        # Spin up output thread
        output_worker = Thread(target=handle_output, args=(self.output_handler, output_queue, status))
        output_worker.daemon = True
        output_worker.start()

        # Kick off enumeration
        self.mode.enumerate(request_queue, response_queue, output_queue)

        status.running = False

        # Clean up threads once complete
        for worker in request_workers:
            worker.join()

        output_worker.join()