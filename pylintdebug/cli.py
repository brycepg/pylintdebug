import sys
import argparse

import pylint
from pylint.lint import Run

from .func import print_callsite_location


def monkeypatch_add_message():
    """Monkeypatch the pylint base add_message method to print
    callsite location

    Every message that is added to pylint passes through
    this method
    """
    print("Monkeypatching add_message")
    method_path = pylint.checkers.BaseChecker.add_message
    pylint.checkers.BaseChecker._debug_add_message = method_path
    pylint.checkers.BaseChecker.add_message = debug_add_message

def debug_add_message(*args, **kwargs):
    print_callsite_location()
    return pylint.checkers.BaseChecker._debug_add_message(*args, **kwargs)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('path')
    parser.add_argument('--messages-location', action='store_true', default=False, help="Get location of add_message in pylint source tree")
    parser.add_argument('--pylint-messages', action='store_true', help='enable all pylint messages')
    args = parser.parse_args()
    if args.messages_location:
        monkeypatch_add_message()
    if not args.messages_location:
        print("No debug options given for {}".format(sys.arv[0]))
    pylint_args = []
    if args.pylint_messages:
        pylint_args.append('--enable=all')
    else:
        pylint_args.append('--disable=all')
    Run([args.path, '-rn', '-sn'] + pylint_args)
