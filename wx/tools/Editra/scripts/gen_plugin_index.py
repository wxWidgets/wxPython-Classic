#!/usr/bin/env python
###############################################################################
# Name: gen_plugin_index.py                                                   #
# Purpose: Generate the index file for the plugin manager                     #
# Author: Cody Precord <cprecord@editra.org>                                  #
# Copyright: (c) 2008 Cody Precord <staff@editra.org>                         #
# License: wxWindows License                                                  #
###############################################################################

"""

"""

__author__ = "Cody Precord <cprecord@editra.org>"
__svnid__ = "$Id$"
__revision__ = "$Revision$"

#-----------------------------------------------------------------------------#
# Imports
import os
import sys

#-----------------------------------------------------------------------------#

INDEX = "plugin.idx"

#-----------------------------------------------------------------------------#

def findDirectories(path):
    """Find all directories under the given path
    @return: list of strings

    """
    if not os.path.isdir(path):
        raise ValueError("path must be a directory")

    dirs = list()
    for dname in os.listdir(path):
        if dname not in "build dist":
            dirs.append(os.path.join(path, dname))

    return dirs

def getInfoTxt(path):
    """Get the information text about the plugin"""
    rtxt = ''
    try:
        fhandle = open(path, 'r')
        rtxt = fhandle.read()
        rtxt = rtxt.strip()
    except IOError:
        print("Bad file path: " + path)
    finally:
        fhandle.close()

    return rtxt

def generateIndex(paths):
    """Generate the index for the plugins found under the given
    directory.
    @param paths: list of paths to look for plugin directories under

    """
    # Make sure we are working with absolute paths
    apaths = [ os.path.abspath(path) for path in paths ]

    # Collect all the plugin project directories
    spaths = list()
    for path in paths:
        if os.path.exists(path):
            dirs = findDirectories(path)
            spaths.extend(dirs)

    # Find all the info.txt files
    ifiles = list()
    for path in spaths:
        info = os.path.join(path, 'info.txt')
        if os.path.exists(info):
            ifiles.append(info)

    # Construct the index
    info = [getInfoTxt(fname) for fname in ifiles]
    index = open(INDEX, 'w')
    out = "\n###\n".join(info)
    index.write(out)
    index.close()
    
#-----------------------------------------------------------------------------#

if __name__ == '__main__':
    paths = sys.argv[1:]
    generateIndex(paths)

