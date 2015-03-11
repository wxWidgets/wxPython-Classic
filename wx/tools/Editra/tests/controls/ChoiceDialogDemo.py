###############################################################################
# Name: ChoiceDialogDemo.py                                                   #
# Purpose: Test and demo file for eclib.ChoiceDialog                          #
# Author: Cody Precord <cprecord@editra.org>                                  #
# Copyright: (c) 2010 Cody Precord <staff@editra.org>                         #
# Licence: wxWindows Licence                                                  #
###############################################################################

"""
Test file for testing the ChoiceDialog.

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
        self.chLetter = wx.Button(self, label="Choose a Letter")
        self.chNumber = wx.Button(self, label="Choose a Number")
        self.log = log

        # Layout
        self.__DoLayout()

        # Event Handlers
        self.Bind(wx.EVT_BUTTON, self.OnShowDialogBtn)

    def __DoLayout(self):
        """Layout the panel"""
        vsizer = wx.BoxSizer(wx.VERTICAL)
        vsizer.Add(self.chLetter, 0, wx.ALIGN_CENTER|wx.TOP, 20)
        vsizer.Add(self.chNumber, 0, wx.ALIGN_CENTER|wx.TOP, 20)
        self.SetSizer(vsizer)

    def OnShowDialogBtn(self, evt):
        """Show one of the test dialogs"""
        e_obj = evt.GetEventObject()
        dlg = None
        
        if e_obj == self.chLetter:
            l = "abcdefghijklmnopqrstuvwxyz"
            dlg = eclib.ChoiceDialog(None, msg="Choose an letter",
                       title="Letter Dialog", choices=list(l),
                       default="m", style=wx.OK|wx.CANCEL|wx.ICON_WARNING)
        elif e_obj == self.chNumber:
            dlg = eclib.ChoiceDialog(None, msg="Choose an number",
                       title="Number Dialog", choices=map(unicode, range(20)),
                       default="3", style=wx.OK|wx.CANCEL|wx.ICON_WARNING)

        if dlg is not None:
            dlg.SetBitmap(IconFile.Monkey.GetBitmap())
            dlg.CenterOnParent()
            if dlg.ShowModal() == wx.ID_OK:
                self.log.write("Got Value: %s" % dlg.GetStringSelection())
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

overview = eclib.choicedlg.__doc__
title = "ChoiceDialog"

#-----------------------------------------------------------------------------#
if __name__ == '__main__':
    try:
        import run
    except ImportError:
        app = wx.PySimpleApp(False)
        frame = wx.Frame(None, title="ChoiceDialog Demo")
        sizer = wx.BoxSizer(wx.HORIZONTAL)
        sizer.Add(TestPanel(frame, TestLog()), 1, wx.EXPAND)
        frame.CreateStatusBar()
        frame.SetSizer(sizer)
        frame.SetInitialSize((300, 300))
        frame.Show()
        app.MainLoop()
    else:
        run.main(['', os.path.basename(sys.argv[0])] + sys.argv[1:])
