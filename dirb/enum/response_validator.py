from requests import Response

class ResponseValidator:
    def __init__(self):
        self.size_counter = {}

        # anything that indicates a webpage is there
        self.valid_response_codes = [200, 201, 202, 301, 302, 400, 401, 403, 405, 500]

        self.invalid_response_codes = [404]

    def validate_response(self, response: Response):
        if response.status_code in self.invalid_response_codes:
            return False

        # Prevent valid . files from hitting
        if response.status_code == 403 and response.url.split('/')[-1].startswith('.'):
            return False

        if response.status_code in self.valid_response_codes:
            return True

        return False