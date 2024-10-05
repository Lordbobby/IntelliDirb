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

        resp_size = len(response.content)

        if resp_size not in self.size_counter:
            self.size_counter[resp_size] = 1

            return True

        self.size_counter[resp_size] = self.size_counter[resp_size] + 1

        # Check if this is a constant response size, may indicate a not found page returning a valid response code
        if self.size_counter[resp_size] > 5:
            return False

        if response.status_code in self.valid_response_codes:
            return True

        return False