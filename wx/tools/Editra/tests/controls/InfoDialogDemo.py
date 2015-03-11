###############################################################################
# Name: InfoDialogDemo.py                                                     #
# Purpose: Test and demo file for eclib.InfoDialog                            #
# Author: Cody Precord <cprecord@editra.org>                                  #
# Copyright: (c) 2009 Cody Precord <staff@editra.org>                         #
# Licence: wxWindows Licence                                                  #
###############################################################################

"""
Test file for testing the File InfoDialog.

"""

__author__ = "Cody Precord <cprecord@editra.org>"
__svnid__ = "$Id: ColorSetterDemo.py 59368 2009-03-06 15:03:58Z CJP $"
__revision__ = "$Revision: 59368 $"

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
        wx.Panel.__init__(self, parent, wx.ID_ANY, size=(500,500))

        # Attributes
        self.fpicker = wx.FilePickerCtrl(self)
        self.log = log

        # Layout
        self.__DoLayout()

        # Event Handers
        self.Bind(wx.EVT_FILEPICKER_CHANGED, self.OnFilePicked)

    def __DoLayout(self):
        """Layout the panel"""
        vsizer = wx.BoxSizer(wx.VERTICAL)

        stext = wx.StaticText(self, label="Choose a file: ")
        hsizer = wx.BoxSizer(wx.HORIZONTAL)
        hsizer.Add(stext, 0, wx.ALIGN_CENTER_VERTICAL)
        hsizer.Add(self.fpicker, 1, wx.EXPAND)

        vsizer.AddStretchSpacer()
        vsizer.Add(hsizer, 0, wx.ALIGN_CENTER)
        vsizer.AddStretchSpacer()

        self.SetSizer(vsizer)
        self.SetAutoLayout(True)

    def OnFilePicked(self, evt):
        fname = self.fpicker.GetPath()
        dlg = eclib.FileInfoDlg(self, fname, bmp=IconFile.Monkey.GetBitmap())
        dlg.CenterOnParent()
        dlg.Show()

#----------------------------------------------------------------------

def runTest(frame, nb, log):
    win = TestPanel(nb, log)
    return win

class TestLog:
    def __init__(self):
        pass

    def write(self, msg):
        print msg

#----------------------------------------------------------------------

overview = eclib.infodlg.__doc__
title = "FileInfoDlg"

#-----------------------------------------------------------------------------#
if __name__ == '__main__':
    try:
        import run
    except ImportError:
        app = wx.PySimpleApp(False)
        frame = wx.Frame(None, title="File Info Dialog Demo")
        sizer = wx.BoxSizer(wx.HORIZONTAL)
        sizer.Add(TestPanel(frame, TestLog()), 1, wx.EXPAND)
        frame.CreateStatusBar()
        frame.SetSizer(sizer)
        frame.SetInitialSize((300, 300))
        frame.Show()
        app.MainLoop()
    else:
        run.main(['', os.path.basename(sys.argv[0])] + sys.argv[1:])
