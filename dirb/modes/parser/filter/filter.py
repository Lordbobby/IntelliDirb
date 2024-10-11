
class ServiceFilter:
    def __init__(self, service_name):
        self.service_name = service_name

    def is_service(self, content, response):
        return False