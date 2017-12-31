"""Debugging functions

func_info:

Decorator to print args and return values
This helps understanding chain of events in code. The downside
is you need to know


print_callsite_location:

Prints the parent file, line location of the current function
This helps finding where method calls to widely used interfaces occur in code
"""
import sys
import inspect
from collections import abc


try:
    from astroid.node_classes import NodeNG
    HAS_ASTROID = True
except ImportError:
    HAS_ASTROID = False

def func_info(func=None, **options):
    """Decorator to retrieve function info

    Allows for additional keyword arguments in decorator.

    Keyword Args:
        listify: If true listify generators to make them printable
    """
    if func is None:
        def partial_infer(func):
            return func_info(func, **options)
        return partial_infer
    def inner(*args, **kwargs):
        convert_generators = options.get("listify", False)
        print("Calling", func.__qualname__)
        for arg in args:
            if HAS_ASTROID and isinstance(arg, NodeNG):
                if "\n" not in arg.as_string() and len(arg.as_string()) < 80:
                    print("Node: ", arg.as_string())
                else:
                    print("Node: ", arg)
        if args:
            print("Args:", args)
        if kwargs:
            print("kwargs:", kwargs)
        result = func(*args, **kwargs)
        if isinstance(result, abc.Generator) and convert_generators:
            result = list(result)
        print("result", result)
        print("-------")
        print()
        if convert_generators:
            result = iter(result)
        return result
    return inner


def print_callsite_location():
    """Print location of function call of the parent of the call location."""
    fi = inspect.getouterframes( inspect.currentframe() )[2]
    print("{path}:{line} {fname}".format(
        line=fi.lineno, path=fi.filename, fname=fi.function))
