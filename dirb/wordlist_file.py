from mmap import mmap

from dirb.output import logger

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

    def reset_index(self):
        logger.debug('Resetting wordlist index.')

        self.index = 0
        self.byte_index = 0

    def get_words(self, num):
        logger.debug(f'Getting {num} words from the dictionary.')

        with open(self.file_path, 'r') as file:
            words = file.readlines(num)
            words = [word.rstrip() for word in words]

            self.index += num
            self.byte_index = file.tell()

            logger.debug(f'Grabbed {len(words)} words from the dictionary.')

            return words