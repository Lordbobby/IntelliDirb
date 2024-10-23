from mmap import mmap

from dirb.output import logger
from dirb.output.color import Color
from dirb.output.stats.tag import Tag


# https://stackoverflow.com/a/850962
def count_lines(file_path):
    with open(file_path, 'r+') as file:
        buffer = mmap(file.fileno(), 0)
        lines = 0
        readline = buffer.readline
        while readline():
            lines += 1
        return lines

class WordlistFile:
    def __init__(self, file_path):
        self.file_path = file_path
        # TODO validate file
        self.lines = count_lines(file_path)

        self.index = 0
        self.byte_index = 0

        logger.info(f'Loaded wordlist file with {Color.GREEN}{self.lines}{Color.RESET} words.')

    def reset_index(self):
        logger.debug('Resetting wordlist index.')

        self.index = 0
        self.byte_index = 0

    def get_words(self, num):
        if self.index >= self.lines:
            return []

        logger.debug(f'Getting {num} words from the dictionary.')

        with open(self.file_path, 'r') as file:
            file.seek(self.byte_index)

            words = []
            line = file.readline()
            while line:
                words.append((line.rstrip(), Tag.DICTIONARY))

                if len(words) >= num:
                    break

                line = file.readline()

            self.index += num
            self.byte_index = file.tell()

            logger.debug(f'Grabbed {len(words)} words from the dictionary.')

            return words