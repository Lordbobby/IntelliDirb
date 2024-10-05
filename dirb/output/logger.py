from dirb.output.color import Color
from dirb.output.messages import LogMessage

DEBUG_LEVEL = 1
INFO_LEVEL = 2
ERROR_LEVEL = 3
CRITICAL_LEVEL = 4

log_settings = {
    'current_level': 1,
    'output_queue': None,
    'level_map': {
        'DEBUG': DEBUG_LEVEL,
        'INFO': INFO_LEVEL,
        'ERROR': ERROR_LEVEL,
        'CRITICAL': CRITICAL_LEVEL
    }
}

def set_current_log_level(level):
    log_settings['current_level'] = log_settings['level_map'][level]

def set_output_queue(output_queue):
    log_settings['output_queue'] = output_queue

# noinspection PyUnresolvedReferences
def log(level, level_name, message):
    current_level = log_settings['current_level']

    if level < current_level:
        return

    message = f'[{level_name}] {message}'

    # Prefer to use the output queue, but if it isn't available, print
    if log_settings['output_queue'] is None:
        print(message)
        return

    log_settings['output_queue'].put(LogMessage(message))

def critical(message):
    log(CRITICAL_LEVEL, f'{Color.RED}CRITICAL{Color.RESET}', message)

def error(message):
    log(ERROR_LEVEL, f'{Color.RED}ERROR{Color.RESET}', message)

def info(message):
    log(INFO_LEVEL, f'{Color.BLUE}INFO{Color.RESET}', message)

def debug(message):
    log(DEBUG_LEVEL, f'{Color.BLUE}DEBUG{Color.RESET}', message)
