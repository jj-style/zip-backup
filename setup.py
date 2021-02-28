#!/usr/bin/python3

from distutils.core import setup

setup(
    name="zipy-backup",
    version="1.0",
    description="Zip backup utility",
    author="JJ Style",
    author_email="style.jj@pm.me",
    url="https://github.com/jj-style/zip-backup",
    entry_points={
        "console_scripts": ["zipy-backup = backupper:main"],
    }
)
