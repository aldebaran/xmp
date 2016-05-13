#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from setuptools import setup
import os

CONTAINING_DIRECTORY = os.path.dirname(os.path.realpath(__file__))

setup(
    name='xmp',
    version=open(os.path.join(CONTAINING_DIRECTORY,"xmp/VERSION")).read().split()[0],
    author='Louis-Kenzo Cahier',
    author_email='lkcahier@aldebaran.com',
    packages=['xmp', 'xmp.commands', 'xmp.qiq'],
    package_data={"xmp":["VERSION"]},
    scripts=['bin/xmp'],
    url='.',
    license='LICENSE.txt',
    description='XMP is a tool to read/write metadata in files.',
    long_description=open(os.path.join(CONTAINING_DIRECTORY,'README.md')).read(),
    test_suite="tests",
    install_requires=[
        "python-xmp-toolkit >= 2.0.1",
    ]
)

