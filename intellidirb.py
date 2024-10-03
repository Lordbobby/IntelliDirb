import sys
from argparse import ArgumentParser
from art import tprint

from dirb.target import Target
from dirb.dirb_manager import DirbManager
from dirb.modes.dictionary import Dictionary
from dirb.output.output_handler import OutputHandler
from dirb.wordlist_file import WordlistFile

class CustomParser(ArgumentParser):
    def error(self, message):
        sys.stdout.write(f'Error: {message}\n\n')
        self.print_help()
        sys.exit(2)

def print_header():
    tprint('IntelliDirb', 'tarty1')
    print()

def setup_argument_parser():
    arg_parser: ArgumentParser = CustomParser()

    arg_parser.add_argument('target', help='Target IP and port to enumeration.')
    arg_parser.add_argument('-w', dest='wordlist', required=True, help='Wordlist file.')
    arg_parser.add_argument('-m', dest='mode',
                        choices=['dict', 'content', 'service', 'script', 'all'], default='dict',
                        help='Choose the fuzzing mode.')
    arg_parser.add_argument('-x', dest='extensions', help='Extensions to test for each word.')
    arg_parser.add_argument('-o', dest='out_file', help='Output file.')
    arg_parser.add_argument('-t', dest='threads', type=int, default=10, help='The number of threads to use (default=10).')

    return arg_parser

if __name__ == '__main__':
    print_header()

    parser = setup_argument_parser()
    args = parser.parse_args()

    # Setup output handling
    output_handler = OutputHandler()

    if args.out_file:
        output_handler.set_output_file(args.out_file)

    # Setup wordlist
    wordlist = WordlistFile(args.wordlist)

    # Setup target
    target = Target(args.target)

    # Setup mode
    mode = Dictionary(wordlist, target, args.extensions)

    dirb = DirbManager(mode, output_handler, args.threads)
    dirb.enumerate()