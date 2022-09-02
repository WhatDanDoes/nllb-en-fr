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
    parser.add_argument('--json', help='Path to JSON file')
    parser.add_argument('-p', '--phrase', nargs='+', help='The input phrase to be translated')

    args = parser.parse_args()
    return args


def main():
    """CLI for English-to-French NLLB translator"""

    args = parse_arguments()

    if (args.phrase): 
      phrase = ' '.join(args.phrase)
  
      output_string = command.translate(phrase)
  
      print(output_string)

    if (args.json):
      data = command.translate_json(args.json)
      print(data)
