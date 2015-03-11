# -*- coding: utf-8 -*-
# Setup script to build the CodeBrowser plugin. To build the plugin
# just run 'python setup.py bdist_egg' and an egg will be built and put into 
# a directory called dist in the same directory as this script.
""" Editra CodeBrowser Plugin """

__author__ = "Cody Precord"

import sys
try:
    from setuptools import setup
except ImportError:
    print "You must have setup tools installed in order to build this plugin"
    setup = None

if setup != None:
    setup(
        name='CodeBrowser',
        version='1.5',
        description=__doc__,
        author=__author__,
        author_email="cprecord@editra.org",
        license="wxWindows",
        url="http://editra.org",
        platforms=["Linux", "OS X", "Windows"],
        packages=['codebrowser',],
        package_data={'codebrowser' : ['gentag/*.py']},
        entry_points='''
        [Editra.plugins]
        CodeBrowser = codebrowser:CodeBrowser
        '''
        )
