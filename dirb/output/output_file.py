
class OutputFile:

    def __init__(self, file_path):
        # TODO Validate file path
        self.filepath = file_path

    def write_message(self, message):
        with open(self.filepath, 'w+') as output_file:
            output_file.write(message)