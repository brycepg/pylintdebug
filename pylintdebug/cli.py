import argparse
import pylint
from pylint.lint import Run


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('path')
    parser.add_argument('--messages', action='store_true', default=False)
    args = parser.parse_args()
    if args.messages:
        print("MESSAGES")
        print(pylint.checkers.BaseChecker.add_message)
    Run([args.path])
