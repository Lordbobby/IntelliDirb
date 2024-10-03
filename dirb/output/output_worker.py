
def handle_output(output_handler, output_queue, status):
    while status.running:
        message = output_queue.get()

        output_handler.send_message(message)