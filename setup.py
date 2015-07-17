#!/usr/bin/env python
# -*- coding: utf-8 -*-


import os
import sys

if sys.version_info < (2, 6):
    raise ImportError("dmoz-parser requires python >= 2.6")


# TODO add ez_setup?
from setuptools import setup, find_packages

setup(
    name = 'dmoz-parser',
    version = '0.0.1',
    description = 'Tool to parse the DMOZ data',
    long_description = read('README.rst'),

    packages=find_packages(),

    install_requires=[
        'smart-open==1.2.1'
    ],
)
