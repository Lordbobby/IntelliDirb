from dirb.output.messages import Message
from dirb.output.no_output_file import NoOutputFile
from dirb.output.output_file import OutputFile

class OutputHandler:

    def __init__(self):
        self.output_file = NoOutputFile()

    def set_output_file(self, file_path):
        self.output_file = OutputFile(file_path)

    def send_message(self, message: Message):
        console_string = message.to_console_string()

        if len(console_string):
            print(console_string)

        csv_string = message.to_csv_string()

        if len(csv_string):
            self.output_file.write_message(csv_string)