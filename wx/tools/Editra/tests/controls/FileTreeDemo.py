###############################################################################
# Name: FileTreeDemo.py                                                       #
# Purpose: Test and demo file for eclib.FileTree                              #
# Author: Cody Precord <cprecord@editra.org>                                  #
# Copyright: (c) 2011 Cody Precord <staff@editra.org>                         #
# Licence: wxWindows Licence                                                  #
###############################################################################

"""
Test file for testing the FileTree control

"""

__author__ = "Cody Precord <cprecord@editra.org>"
__svnid__ = "$Id:  $"
__revision__ = "$Revision:  $"

#-----------------------------------------------------------------------------#
# Imports
import os
import sys
import wx

import IconFile

# Put local package on the path
#sys.path.insert(0, os.path.abspath('../../src'))
import eclib

#-----------------------------------------------------------------------------#

class TestPanel(wx.Panel):
    def __init__(self, parent, log):
        super(TestPanel, self).__init__(parent)

        # Attributes
        self.ftree = eclib.FileTree(self)
        self.ftree.AddWatchDirectory(wx.GetUserHome())
        self.selbtn = wx.Button(self, label="Selected Files")
        self.addbtn = wx.DirPickerCtrl(self, message="Add Watch",
                                       style=wx.DIRP_CHANGE_DIR)
        self.addbtn.PickerCtrl.SetLabel("Add Watch")
        self.rmbtn = wx.Button(self, label="Remove Watch")
        self.setselbtn = wx.Button(self, label="Select a File")
        self.log = log

        # Layout
        self.__DoLayout()

        # Event Handlers
        self.Bind(wx.EVT_BUTTON, self.OnGetSelected, self.selbtn)
        self.Bind(wx.EVT_DIRPICKER_CHANGED, self.OnAddWatch, self.addbtn)
        self.Bind(wx.EVT_BUTTON, self.OnRemoveWatch, self.rmbtn)
        self.Bind(wx.EVT_BUTTON, self.OnSelectFile, self.setselbtn)

    def __DoLayout(self):
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.ftree, 1, wx.EXPAND)
        btnsz = wx.BoxSizer(wx.HORIZONTAL)
        btnsz.Add(self.addbtn)
        btnsz.Add(self.rmbtn)
        btnsz.Add(self.selbtn)
        btnsz.Add(self.setselbtn)
        sizer.Add(btnsz)
        self.SetSizer(sizer)

    def OnAddWatch(self, evt):
        val = self.addbtn.GetPath()
        self.log.write("Add new watch: %s" % val)
        self.ftree.AddWatchDirectory(val)

    def OnRemoveWatch(self, evt):
        ch = wx.GetSingleChoice("Select watch dir to remove", "Remove Watch",
                                self.ftree.WatchDirs, self)
        if ch:
            self.ftree.RemoveWatchDirectory(ch)

    def OnGetSelected(self, evt):
        sel = self.ftree.GetSelectedFiles()
        self.log.write(repr(sel))

    def OnSelectFile(self, evt):
        ddir = ""
        if len(self.ftree.WatchDirs):
            ddir = self.ftree.WatchDirs[0]
        dlg = wx.FileDialog(self, "Select a file", ddir,
                            style=wx.FD_OPEN)
        if dlg.ShowModal() == wx.ID_OK:
            fname = dlg.GetPath()
            self.log.write("SelectFile(%s)" % fname)
            self.ftree.SelectFile(fname)
        dlg.Destroy()

#-----------------------------------------------------------------------------#

def runTest(frame, nb, log):
    win = TestPanel(nb, log)
    return win

class TestLog:
    def __init__(self):
        pass

    def write(self, msg):
        print msg

#----------------------------------------------------------------------

overview = eclib.FileTree.__doc__
title = "FileTree"

#-----------------------------------------------------------------------------#
if __name__ == '__main__':
    try:
        import run
    except ImportError:
        app = wx.App(False)
        frame = wx.Frame(None, title="FileTree Demo")
        sizer = wx.BoxSizer(wx.HORIZONTAL)
        sizer.Add(TestPanel(frame, TestLog()), 1, wx.EXPAND)
        frame.CreateStatusBar()
        frame.SetSizer(sizer)
        frame.SetInitialSize((300, 300))
        frame.Show()
        app.MainLoop()
    else:
        run.main(['', os.path.basename(sys.argv[0])] + sys.argv[1:])
