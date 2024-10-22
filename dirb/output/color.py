
class _Color:
    RED = '\033[91m'
    GREEN = '\033[92m'
    BLUE = '\033[94m'
    YELLOW = '\033[93m'
    RESET = '\033[0m'

    def disable_colors(self):
        self.RED = ''
        self.GREEN = ''
        self.BLUE = ''
        self.YELLOW = ''
        self.RESET = ''

Color = _Color()