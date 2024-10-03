
# Ensure slash at end. Will allow just about anything as target string.
def _parse_input(target_str: str):
    if target_str.endswith('/'):
        target_str = target_str[:-1]

    return target_str

class Target:
    def __init__(self, target_str):
        self.url = _parse_input(target_str)

    def get_base_url(self):
        return self.url

