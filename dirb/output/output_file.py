
class OutputFile:

    def __init__(self, file_path):
        # TODO Validate file path
        self.filepath = file_path

        # Clear out file
        with open(self.filepath, 'w+') as output_file:
            output_file.write('')

    def write_message(self, message):
        with open(self.filepath, 'a') as output_file:
            output_file.write(message + '\n')