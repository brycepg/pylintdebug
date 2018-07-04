The utility is intended to help debug pylint and astroid.

This program will forward the given path to pylint and conditionally monkey patch pylint to give debug information

# Installation

    git clone git@github.com:brycepg/pylintdebug.git
    cd pylintdebug
    pip install pylintdebug

# Usage

    pylintdebug [args] <path_of_file_to_debug>

To find out where messages are being called use:

    pylintdebug --messages file.py

Use `--extend-args` to pass arguments to pylint

Use the `--inference` flag to print information about inference occuring


### reveal\_inference call

``pylintdebug`` patches astroid with an psuedo-function called `reveal_inference`. Calling `reveal_inference(node)` will reveal astroid information about this node. This is useful for understanding the flow of a python program in the wild. Additional informatino can be gleaned from `reveal_inference(node, pdb=True)` which will start pdb in the function and allow you to step into `astroid` inference.

# API

importing pylintdebug will automatically add the reveal\_inference call to astroid's brain.

## print info about inference functions

```python
from pylintdebug import patch
patch.patch_inference_functions()
```
