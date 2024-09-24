from dirb.output.no_output_file import NoOutputFile
from dirb.output.output_file import OutputFile


class OutputHandler:

    def __init__(self):
        self.output_file = NoOutputFile()

    def set_output_file(self, file_path):
        self.output_file = OutputFile(file_path)