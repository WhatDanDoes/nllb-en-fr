"""
CLI for English-to-French NLLB translator
"""
import argparse
from . import __version__, command


def parse_arguments():
    """
    Parse and handle CLI arguments
    """
    parser = argparse.ArgumentParser(description=__doc__)

    parser.add_argument('--version', action='version', version=__version__)
    parser.add_argument('input', nargs='+', help='The input sentence to be translated')

    args = parser.parse_args()
    return args


def main():
    """CLI for English-to-French NLLB translator"""

    args = parse_arguments()
    input_string = ' '.join(args.input)

    output_string = command.translate(input_string)

    print(output_string)
