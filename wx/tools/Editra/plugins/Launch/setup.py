# -*- coding: utf-8 -*-
# Setup script to build the Launch plugin. To build the plugin
# just run 'python setup.py bdist_egg' and an egg will be built and put into 
# the dist directory of this folder.
"""Runs the script thats in the current buffer and displays output in the Shelf. 
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
        name='Launch',
        version='1.14',
        description=__doc__,
        author=__author__,
        author_email="cprecord@editra.org",
        license="wxWindows",
        url="http://editra.org",
        platforms=["Linux", "OS X", "Windows"],
        packages=['launch'],
        entry_points='''
        [Editra.plugins]
        Launch = launch:Launch
        '''
        )

