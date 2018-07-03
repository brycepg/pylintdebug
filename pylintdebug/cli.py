import sys
import argparse
import shlex

from .patch import patch_add_message, patch_inference_functions

import pylint
from pylint.lint import Run

def get_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('path')
    parser.add_argument('--messages-location', action='store_true', default=False, help="Get location of add_message in pylint source tree")
    parser.add_argument('--no-pylint-messages', action='store_false', help='disable all pylint messages', default=True, dest="pylint_messages")
    parser.add_argument('--inference', action='store_true', help='Print info about inference engine', default=False)
    parser.add_argument('--extend-args', help="Extend pylint args", default="", dest="extended_args")
    return parser

def main():
    parser = get_parser()
    args = parser.parse_args()

    if args.messages_location:
        patch_add_message()
    if args.inference:
        patch_inference_functions()
    if not (args.messages_location or args.inference):
        print("No debug options given for {}".format(sys.argv[0]))

    pylint_args = get_pylint_args(args.path, args.pylint_messages, args.extended_args)
    Run(pylint_args)

def get_pylint_args(path, messages_enabled, extended_args):
    pylint_args = [path, '-rn', '-sn']
    if messages_enabled:
        pylint_args.append('--enable=all')
    else:
        pylint_args.append('--disable=all')
    pylint_args.extend(shlex.split(extended_args))
    return pylint_args
