# -*- coding: utf-8 -*-
# Setup script to build the hello plugin. To build the plugin
# just run 'python setup.py bdist_egg'

""" The hello plugin is a very simple plugin implimenting the well
known hello world program for Editra. It does so by adding the
words "Hello World" to the View Menu. Which in turn opens a dialog
that says hello world again.

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
            name='Hello',
            version='0.3',
            description=__doc__,
            author=__author__,
            author_email="cprecord@editra.org",
            license="wxWindows",
            url="http://editra.org",
            platforms=["Linux", "OS X", "Windows"],
            packages=['hello'],
            entry_points='''
            [Editra.plugins]
            Hello = hello:Hello
            '''
        )
