from dirb.output import logger


def handle_output(output_handler, output_queue, status):
    logger.debug('Spinning up output worker...')

    while status.running:
        if output_queue.empty():
            continue

        message = output_queue.get()

        output_handler.send_message(message)

    logger.debug('Output worker finished.')