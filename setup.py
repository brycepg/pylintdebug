import os
from setuptools import setup
import fastentrypoints

setup(
    name = "pylintdebug",
    version = "0.0.1",
    py_modules = ['fastentrypoints'],
    author = "Bryce Guinta",
    author_email = "bryce.paul.guinta@gmail.com",
    description = "Debug pylint",
    license = "MIT",
    entry_points = {'console_scripts': ['pylintdebug=pylintdebug:cli.main']},
)
