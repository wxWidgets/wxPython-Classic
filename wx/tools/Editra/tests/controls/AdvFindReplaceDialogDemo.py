###############################################################################
# Name: AdvFindReplaceDialogDemo.py                                           #
# Purpose: Advanced Find Replace Dialog Test and Demo File                    #
# Author: Cody Precord <cprecord@editra.org>                                  #
# Copyright: (c) 2008 Cody Precord <staff@editra.org>                         #
# Licence: wxWindows Licence                                                  #
###############################################################################

"""
Test file for testing the Advanced Find Replace Dialog

"""

__author__ = "Cody Precord <cprecord@editra.org>"
__svnid__ = "$Id$"
__revision__ = "$Revision$"

#-----------------------------------------------------------------------------#
# Imports
import sys
import os
import wx

#sys.path.insert(0, os.path.abspath('../../src'))
import eclib

#-----------------------------------------------------------------------------#
ID_DEFAULT = wx.NewId()
ID_DIALOG  = wx.NewId()
ID_REPLACE = wx.NewId()
ID_NOUPDOWN = wx.NewId()
ID_NOOPTS  = wx.NewId()
ID_REGEX   = wx.NewId()
ID_NOLOOK  = wx.NewId()
ID_NOWHOLEW = wx.NewId()
ID_NO_COUNT = wx.NewId()
ID_NO_ALL_ACT = wx.NewId()
ID_NO_MODE_SELECT = wx.NewId()
ID_MINIMAL = wx.NewId()

#-----------------------------------------------------------------------------#
# There are a large number of possible flag/style combinations here are just a
# few examples for creating different versions of the dialog.
DIALOG_MAP = {ID_DEFAULT : (wx.FindReplaceData(),
                            eclib.AFR_STYLE_FINDDIALOG,
                            "Default Find Dialog"),
              ID_DIALOG  : (wx.FindReplaceData(),
                            eclib.AFR_STYLE_NON_FLOATING,
                            "Non Floating Find Dialog"),
              ID_REPLACE : (wx.FindReplaceData(),
                            eclib.AFR_STYLE_REPLACEDIALOG,
                            "Default Replace Dialog"),
              ID_NOUPDOWN : (wx.FindReplaceData(eclib.AFR_NOUPDOWN),
                            eclib.AFR_STYLE_REPLACEDIALOG,
                            "No Up/Down Option"),
              ID_NOOPTS  : (wx.FindReplaceData(eclib.AFR_NOOPTIONS),
                           eclib.AFR_STYLE_FINDDIALOG,
                           "Options Hidden"),
              ID_REGEX   : (wx.FindReplaceData(eclib.AFR_REGEX),
                            eclib.AFR_STYLE_FINDDIALOG,
                            "Regex Selected"),
              ID_NOLOOK  : (wx.FindReplaceData(eclib.AFR_NOLOOKIN),
                            eclib.AFR_STYLE_FINDDIALOG,
                            "Lookin Hidden"),
              ID_NOWHOLEW : (wx.FindReplaceData(eclib.AFR_NOWHOLEWORD),
                             eclib.AFR_STYLE_FINDDIALOG,
                             "Whole Word Disabled"),
              ID_NO_COUNT : (wx.FindReplaceData(eclib.AFR_NO_COUNT),
                             eclib.AFR_STYLE_FINDDIALOG,
                             "No Count Button"),
              ID_NO_ALL_ACT : (wx.FindReplaceData(eclib.AFR_NO_ALL_BTN),
                             eclib.AFR_STYLE_FINDDIALOG,
                             "No Find/Replace All"),
              ID_NO_MODE_SELECT : (wx.FindReplaceData(),
                             eclib.AFR_STYLE_FINDDIALOG|eclib.AFR_STYLE_NO_MODE_SELECT,
                             "No Mode Select"),
              ID_MINIMAL : (wx.FindReplaceData(eclib.AFR_SIMPLE),
                            eclib.AFR_STYLE_FINDDIALOG,
                            "All Options Hidden")}

BUTTONS = [(ID_DEFAULT, "Default"), (ID_DIALOG, "Non-Floating"),
           (ID_REPLACE, "Replace Dialog"), (ID_NOUPDOWN, "No Up/Down Option"),
           (ID_NOOPTS, "Options Hidden"),
           (ID_REGEX, "Regular Expression"), (ID_NOLOOK, "Lookin Hidden"),
           (ID_NOWHOLEW, "Whole Word Disabled"), (ID_NO_COUNT, "No Count Button"),
           (ID_NO_ALL_ACT, "No Find/Replace All"),
           (ID_NO_MODE_SELECT, "No Mode Select"), (ID_MINIMAL, "Minimal")]

#-----------------------------------------------------------------------------#

class TestPanel(wx.Panel):
    def __init__(self, parent, log):
        wx.Panel.__init__(self, parent)

        # Attributes
        self.data = None
        self.dlg = None
        self.log = log

        # Layout
        self.__DoLayout()

        # Event Handlers
        self.Bind(wx.EVT_BUTTON, self.OnButton)
        self.Bind(eclib.EVT_FIND, self.OnFind)
        self.Bind(eclib.EVT_FIND_ALL, self.OnFind)
        self.Bind(eclib.EVT_FIND_NEXT, self.OnFind)
        self.Bind(eclib.EVT_REPLACE, self.OnFind)
        self.Bind(eclib.EVT_REPLACE_ALL, self.OnFind)
        self.Bind(eclib.EVT_FIND_CLOSE, self.OnFindClose)

    def __DoLayout(self):
        """Layout the panel"""
        fsizer = wx.BoxSizer(wx.VERTICAL)
        fsizer.Add((10, 10), 0)
        for bid, lbl in BUTTONS:
            btn = wx.Button(self, bid, lbl)
            fsizer.Add(btn, 0)
            fsizer.Add((5, 5), 0)
        msizer = wx.BoxSizer(wx.HORIZONTAL)
        msizer.AddMany([((10, 10), 0), (fsizer, 0, wx.EXPAND), ((10, 10), 0)])
        self.SetSizer(msizer)
        self.SetAutoLayout(True)

    def OnButton(self, evt):
        """Show a dialog"""
        e_id = evt.GetId()
        if e_id in DIALOG_MAP:
            self.data, style, title = DIALOG_MAP[e_id]
            self.dlg = eclib.AdvFindReplaceDlg(self, self.data, title, style)
            self.dlg.CenterOnParent()
            self.dlg.Show()
        else:
            evt.Skip()

    def OnFind(self, evt):
        self.log.write("Search String: %s" % evt.GetFindString())
        self.log.write("Replace String: %s" % evt.GetReplaceString())
        self.log.write("Location: %s" % evt.GetDirectory())
        self.log.write("Search Type: %d" % evt.GetSearchType())
        self.log.write("Whole Word: %d" % evt.IsWholeWord())
        self.log.write("Match Case: %d" % evt.IsMatchCase())
        self.log.write("Regular Expression: %d" % evt.IsRegEx())
        self.log.write("Search Up: %d" % evt.IsUp())
        self.log.write("EvtType: %d" % evt.GetEventType())

    def OnFindClose(self, evt):
        """Called when dialog closes"""
        if self.dlg is not None:
            self.log.write("Dialog Closed")
            self.dlg.Destroy()
            self.dlg = None
        
#-----------------------------------------------------------------------------#

class TestLog:
    def __init__(self):
        pass

    def write(self, msg):
        print msg

#-----------------------------------------------------------------------------#

overview = eclib.finddlg.__doc__
title = "AdvFindReplaceDlg"

#-----------------------------------------------------------------------------#
if __name__ == '__main__':
    try:
        import run
    except ImportError:
        app = wx.PySimpleApp(False)
        frame = wx.Frame(None, title="Advanced Find Dialog Test")
        sizer = wx.BoxSizer(wx.HORIZONTAL)
        sizer.Add(TestPanel(frame, TestLog()), 1, wx.EXPAND)
        frame.CreateStatusBar()
        frame.SetSizer(sizer)
        frame.SetInitialSize(wx.Size(350, 350))
        frame.CenterOnParent()
        frame.Show()
        app.MainLoop()
    else:
        run.main(['', os.path.basename(sys.argv[0])] + sys.argv[1:])
