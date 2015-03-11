###############################################################################
# Name: common.py                                                             #
# Purpose: Common utilities for unittests.                                    #
# Author: Cody Precord <cprecord@editra.org>                                  #
# Copyright: (c) 2008 Cody Precord <staff@editra.org>                         #
# License: wxWindows License                                                  #
###############################################################################

__author__ = "Cody Precord <cprecord@editra.org>"
__svnid__ = "$Id$"
__revision__ = "$Revision$"

#-----------------------------------------------------------------------------#
# Imports
import os
import locale
import shutil
import wx

# Imports for bootstrapping Editra
import plugin
import profiler

#-----------------------------------------------------------------------------#

class EdApp(wx.App):
    def OnInit(self):
        self.pmgr = plugin.PluginManager()

        # Bare minimum profile bootstrap
        profiler.Profile_Set('ENCODING', locale.getpreferredencoding())
        profiler.Profile_Set('ICONS', 'Tango')

        return True

    def GetLog(self):
        return lambda msg: None

    def GetPluginManager(self):
        return self.pmgr

#-----------------------------------------------------------------------------#

class TestFrame(wx.Frame):
    pass

#-----------------------------------------------------------------------------#

def CleanTempDir():
    """Clean all files from the temporary directory"""
    tdir = GetTempDir()
    for path in os.listdir(tdir):
        if path.startswith(u'.'):
            continue

        fpath = os.path.join(tdir, path)
        if os.path.isdir(fpath):
            shutil.rmtree(fpath)
        else:
            os.remove(fpath)

def CopyToTempDir(path):
    """Copy a file to the temp directory"""
    shutil.copy2(path, GetTempDir())

def GetDataDir():
    """Get the path to the test data directory
    @return: string

    """
    path = os.path.join(u'.', u'data')
    return os.path.abspath(path)

def GetDataFilePath(fname):
    """Get the absolute path of the given data file
    @param fname: filename
    @return: string

    """
    path = os.path.join(u'.', u'data', fname)
    return os.path.abspath(path)

def GetFileContents(path):
    """Get the contents of the given file
    @param path: string
    @return: string

    """
    handle = open(path, 'rb')
    txt = handle.read()
    handle.close()
    return txt

def GetTempDir():
    """Get the path to the test temp directory
    @return: string

    """
    path = os.path.join(u'.', u'temp')
    return os.path.abspath(path)

def GetTempFilePath(fname):
    """Get a path for a file in the temp directory
    @param fname: File name to get path for
    @return: string

    """
    tdir = GetTempDir()
    return os.path.join(tdir, fname)

def GetThemeDir():
    """Get the packages theme directory path
    @return: string

    """
    tpath = os.path.join(u"..", u"..", u"pixmaps", u"theme")
    tpath = os.path.abspath(tpath)
    return tpath

def GetStylesDir():
    tpath = os.path.join(u"..", u"..", u"styles")
    tpath = os.path.abspath(tpath)
    return tpath

def MakeTempFile(fname):
    """Make a new file in the temp directory with a give name
    @param fname: file name
    @return: new file path

    """
    path = os.path.join(GetTempDir(), fname)
    if not os.path.exists(path):
        handle = open(path, "wb")
        handle.write(" ")
        handle.close()
    return path
