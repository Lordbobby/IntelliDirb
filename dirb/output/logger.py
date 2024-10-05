
DEBUG_LEVEL = 1
INFO_LEVEL = 2
ERROR_LEVEL = 3
CRITICAL_LEVEL = 4

log_settings = {
    'current_level': 1,
    'level_map': {
        'DEBUG': DEBUG_LEVEL,
        'INFO': INFO_LEVEL,
        'ERROR': ERROR_LEVEL,
        'CRITICAL': CRITICAL_LEVEL
    }
}

def set_current_log_level(level):
    log_settings['current_level'] = log_settings['level_map'][level]

def log(level, level_name, message):
    current_level = log_settings['current_level']

    if level < current_level:
        return

    print(f'[{level_name}] {message}')

def critical(message):
    log(CRITICAL_LEVEL, 'CRITICAL', message)

def error(message):
    log(ERROR_LEVEL, 'ERROR', message)

def info(message):
    log(INFO_LEVEL, 'INFO', message)

def debug(message):
    log(DEBUG_LEVEL, 'DEBUG', message)
