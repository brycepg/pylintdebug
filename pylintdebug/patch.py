import re
from types import FunctionType, MethodType

import astroid
from astroid import inference
from astroid.brain.brain_builtin_inference import register_builtin_transform
import pylint

from .func import func_info
from .func import print_callsite_location

def functions_from_module(module, pattern):
    def gen_functions():
        for value in module.__dict__:
            if re.match(pattern, value):
                pyobj = getattr(inference, value)
                if isinstance(pyobj, FunctionType):
                    yield pyobj
    return list(gen_functions())


def patch_decorator_into_function(namespace, fnames, decorator):
    for fname in fnames:
        func = getattr(namespace, fname)
        setattr(namespace, fname, decorator(func))

def log_func_info_astroid(namespace, fnames):
    for fname in fnames:
        func = getattr(namespace, fname)
        res = func_info(func, listify=True)
        if res.__qualname__  == func.__qualname__:
            return
        setattr(namespace, fname, res)


def patch_inference_functions():
    log_func_info_astroid(
        astroid.node_classes.NodeNG,
        ["infer"])


def patch_add_message():
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
    #print("args:", args)
    #print("kwargs:", kwargs)
    return pylint.checkers.BaseChecker._debug_add_message(*args, **kwargs)


def reveal_inference(node, context=None):
    """
    bool keywords:
        pdb: If True start debugger
        string: if True print as_string() for nodes
        context: If True will display context

    Example:
        node = reveal_inference(node)

        will print inference information about node
        if node is in any inference chain
    """
    string = False
    display_context = False
    if context and context.callcontext:
        for arg in context.callcontex.args:
            print("callcontext arg: ", arg)
    if node.keywords is not None:
        for keyword in node.keywords:
            if not _is_keyword_true(keyword):
                continue
            arg = keyword.arg
            if arg == "pdb":
                import pdb; pdb.set_trace()
            elif arg == "string":
                string = True
            elif arg == "context":
                display_context = True
            else:
                raise ValueError("Unknown keyword {arg}".format(arg=arg))
    if context is None:
        print("Context is None")
    if display_context and context is not None:
        print("context path:", context.path)
        print("context lookupname:", context.lookupname)
        print("context boundnode:", context.boundnode)
        print("context callcontext:", context.callcontext)
        if context.callcontext:
            print("callcontext args:", context.callcontext.args)
            print("callcontext keywords:", context.callcontext.keywords)
        print("context inferred:", context.inferred)
    for arg in node.args:
        arg_value = arg
        if string:
            arg_value = "{arg} ({string})".format(arg=arg, string=arg.as_string())
        infer_value = list(arg.infer(context=context))
        if string:
            string_values = ','.join([val.as_string() for val in infer_value])
            infer_value = "{infer} ({string})".format(infer=infer_value, string=string_values)
        scope_msg = ""
        scope_name = node.scope().name
        if scope_name:
            scope_msg = " in {}".format(scope_name)
        msg_fmt = "{arg} infers to {inference} on line {lineno}{scope_msg}"
        msg = msg_fmt.format(arg=arg_value, inference=infer_value,
                             lineno=node.lineno, scope_msg=scope_msg)
        print(msg)
    return node


def _is_keyword_true(keyword):
    return next(keyword.value.infer()).as_string() == "True"


register_builtin_transform(reveal_inference, 'reveal_inference')
