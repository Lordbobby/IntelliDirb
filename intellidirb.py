from argparse import ArgumentParser, FileType


def setup_argument_parser():
    arg_parser: ArgumentParser = ArgumentParser()

    arg_parser.add_argument('-m', dest='mode',
                        choices=['dict', 'content', 'service', 'script', 'all'], default='dict',
                        help='Choose the fuzzing mode.')
    arg_parser.add_argument('-o', dest='out_file', type=FileType('w'), required=False, help='Output file.')
    arg_parser.add_argument('-w', dest='wordlist', type=FileType('r'), required=True, help='Wordlist file.')

    return arg_parser

if __name__ == 'main':
    parser = setup_argument_parser()

    args = parser.parse_args()