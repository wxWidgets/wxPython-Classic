# -*- coding: utf-8 -*-
# Setup script to build the File Browser plugin. To build the plugin
# just run 'python setup.py bdist_egg' and an egg will be built and put into 
# a directory called dist in the same directory as this script.
""" Setup file for creating the filebrowser plugin """

__author__ = "Cody Precord"

import sys
try:
    from setuptools import setup
except ImportError:
    print "You must have setup tools installed in order to build this plugin"
    setup = None

if setup != None:
    setup(
        name='FileBrowser',
        version='2.2',
        description=__doc__,
        author=__author__,
        author_email="cprecord@editra.org",
        license="wxWindows",
        url="http://editra.org",
        platforms=["Linux", "OS X", "Windows"],
        packages=['filebrowser'],
        package_data={'filebrowser' : ['CHANGELOG']},
        entry_points='''
        [Editra.plugins]
        FileBrowser = filebrowser:FileBrowserPanel
        '''
        )
