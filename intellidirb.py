from argparse import ArgumentParser
from art import tprint

from dirb.Target import Target
from dirb.dirb_manager import DirbManager
from dirb.modes.dictionary import Dictionary
from dirb.output.output_handler import OutputHandler
from dirb.wordlist_file import WordlistFile


def print_header():
    tprint('IntelliDirb', 'tarty1')

def setup_argument_parser():
    arg_parser: ArgumentParser = ArgumentParser()

    arg_parser.add_argument('-m', dest='mode',
                        choices=['dict', 'content', 'service', 'script', 'all'], default='dict',
                        help='Choose the fuzzing mode.')
    arg_parser.add_argument('-o', dest='out_file', required=False, help='Output file.')
    arg_parser.add_argument('-w', dest='wordlist', required=True, help='Wordlist file.')
    arg_parser.add_argument(dest='target', required=True, help='Target IP and port to enumeration.')

    return arg_parser

if __name__ == 'main':
    print_header()

    parser = setup_argument_parser()
    args = parser.parse_args()

    # Setup output handling
    output_handler = OutputHandler()

    if args.out_file:
        output_handler.set_output_file(args.out_file)

    # Setup wordlist
    wordlist = WordlistFile(args.wordlist)

    # Setup mode
    mode = Dictionary(wordlist)

    # Setup target
    target = Target(args.target)

    dirb = DirbManager(target, mode, output_handler)

    dirb.enumerate()