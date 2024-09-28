
# Ensure slash at end. Will allow just about anything as target string.
def _parse_input(target_str):
    if not target_str.endswith('/'):
        target_str = f'{target_str}/'

    return target_str

class Target:
    def __init__(self, target_str):
        self.url = _parse_input(target_str)

    def get_base_url(self):
        return self.url

    def build_url(self, path):
        return f'{self.url}{path}'

