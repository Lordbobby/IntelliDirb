from queue import Queue
from threading import Thread

from dirb.enum.http_client_worker import send_queued_requests
from dirb.output.output_worker import handle_output


class DirbManager:
    def __init__(self, target, mode, output_handler, num_threads=10):
        self.target = target
        self.mode = mode
        self.output_handler = output_handler
        self.num_threads = num_threads

    def enumerate(self):
        request_queue = Queue(maxsize=0)
        response_queue = Queue(maxsize=0)
        output_queue = Queue(maxsize=0)

        # Spin up worker threads
        request_workers = []

        for i in range(self.num_threads):
            request_worker = Thread(target=send_queued_requests, args=(self.target, request_queue, response_queue))
            request_worker.daemon = True
            request_worker.start()

            request_workers.append(request_worker)

        # Spin up output thread
        output_worker = Thread(target=handle_output, args=(self.output_handler, output_queue))
        output_worker.daemon = True
        output_worker.start()

        # Kick off enumeration
        self.mode.begin_processing(request_queue, response_queue)

        # Clean up threads once complete
        for worker in request_workers:
            worker.join()

        output_worker.join()