# -*- coding: utf-8 -*-
# Setup script to build the PyShell plugin. To build the plugin
# just run 'python setup.py bdist_egg' and an egg will be built and put into 
# the dist directory of this folder.
"""Adds an interactive PyShell that can be opened in the Shelf. Multiple
instances can be opened in the Shelf at once.

"""
__author__ = "Cody Precord"

import sys
try:
    from setuptools import setup
except ImportError:
    print "You must have setup tools installed in order to build this plugin"
    setup = None

if setup != None:
    setup(
        name='PyShell',
        version='0.9',
        description=__doc__,
        author=__author__,
        author_email="cprecord@editra.org",
        license="wxWindows",
        url="http://editra.org",
        platforms=["Linux", "OS X", "Windows"],
        packages=['PyShell'],
        entry_points='''
        [Editra.plugins]
        PyShell = PyShell:PyShell
        '''
        )
