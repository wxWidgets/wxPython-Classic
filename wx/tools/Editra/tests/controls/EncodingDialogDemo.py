###############################################################################
# Name: EncodingDialogDemo.py                                                 #
# Purpose: Test and demo file for eclib.EncodingDialog                        #
# Author: Cody Precord <cprecord@editra.org>                                  #
# Copyright: (c) 2010 Cody Precord <staff@editra.org>                         #
# Licence: wxWindows Licence                                                  #
###############################################################################

"""
Test file for testing the EncodingDialog.

"""

__author__ = "Cody Precord <cprecord@editra.org>"
__svnid__ = "$Id$"
__revision__ = "$Revision$"

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
        self.btnDlg = wx.Button(self, label="Show Encoding Dialog")
        self.log = log

        # Layout
        self.__DoLayout()

        # Event Handlers
        self.Bind(wx.EVT_BUTTON, self.OnShowDialogBtn)

    def __DoLayout(self):
        """Layout the panel"""
        vsizer = wx.BoxSizer(wx.VERTICAL)
        vsizer.Add(self.btnDlg, 0, wx.ALIGN_CENTER|wx.TOP, 20)
        self.SetSizer(vsizer)

    def OnShowDialogBtn(self, evt):
        """Show one of the test dialogs"""
        e_obj = evt.GetEventObject()
        if e_obj == self.btnDlg:
            dlg = eclib.EncodingDialog(self, msg="Select an encoding",
                                       title="Encoding Dialog",
                                       elist=eclib.GetAllEncodings(),
                                       default="utf-8")
            dlg.SetBitmap(IconFile.Home.GetBitmap())
            dlg.CenterOnParent()
            if dlg.ShowModal() == wx.ID_OK:
                enc = dlg.GetEncoding()
                self.log.write("Got Encoding: %s" % enc)
            dlg.Destroy()

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

overview = eclib.encdlg.__doc__
title = "EncodingDialog"

#-----------------------------------------------------------------------------#
if __name__ == '__main__':
    try:
        import run
    except ImportError:
        app = wx.PySimpleApp(False)
        frame = wx.Frame(None, title="EncodingDialog Demo")
        sizer = wx.BoxSizer(wx.HORIZONTAL)
        sizer.Add(TestPanel(frame, TestLog()), 1, wx.EXPAND)
        frame.CreateStatusBar()
        frame.SetSizer(sizer)
        frame.SetInitialSize((300, 300))
        frame.Show()
        app.MainLoop()
    else:
        run.main(['', os.path.basename(sys.argv[0])] + sys.argv[1:])
