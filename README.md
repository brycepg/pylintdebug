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
