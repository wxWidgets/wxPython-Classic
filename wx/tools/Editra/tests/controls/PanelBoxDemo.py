###############################################################################
# Name: PanelBoxDemo.py                                                       #
# Purpose: Test and demo of PanelBox control.                                 #
# Author: Cody Precord <cprecord@editra.org>                                  #
# Copyright: (c) 2009 Cody Precord <staff@editra.org>                         #
# Licence: wxWindows Licence                                                  #
###############################################################################

"""
Test file for testing the PanelBox control

"""

__author__ = "Cody Precord <cprecord@editra.org>"
__svnid__ = "$Id$"
__revision__ = "$Revision$"

#-----------------------------------------------------------------------------#
# Imports
import os
import sys
import wx

# Put local Editra.eclib package on the path
#sys.path.insert(0, os.path.abspath('../../src'))
import eclib as eclib

# Local imports
import IconFile

#-----------------------------------------------------------------------------#

class TestPanel(eclib.PanelBox):
    def __init__(self, parent, log):
        eclib.PanelBox.__init__(self, parent, wx.ID_ANY, size=(500,500))

        # Attributes
        self.log = log

        # Setup
        self._PopulateList()

    def _PopulateList(self):
        """Fill the PanelBox with some random PanelBoxItems"""
        monkey = IconFile.Monkey.GetBitmap()
        devil = IconFile.Devil.GetBitmap()
        home = IconFile.Home.GetBitmap()

        items = [(monkey, "Bananas, Bananas, Bananas!!"),
                 (devil,  "Label Text"),
                 (home,   "Home"),
                 (devil,  "A longer label to put into the panelbox item"),
                 (monkey, "More Bananas, Bananas, Bananas!!") ]

        for bmp, label in (items * 3):
            pbi = TestPanelBoxItem(self, bmp, label, self.log)
            self.AppendItem(pbi)

#----------------------------------------------------------------------

class TestPanelBoxItem(eclib.PanelBoxItemBase):
    """Create some simple PanelBoxItem to test with"""
    def __init__(self, parent, bmp, label, log):
        eclib.PanelBoxItemBase.__init__(self, parent)

        # Attributes
        self.log = log
        self.bmp = wx.StaticBitmap(self, bitmap=bmp)
        self.label = wx.StaticText(self, label=label)
        self.button = wx.Button(self, label="Press Me")

        # Layout
        self.__DoLayout()

        # Event handlers
        self.button.Bind(wx.EVT_BUTTON, self.OnButton)

    def __DoLayout(self):
        vsizer = wx.BoxSizer(wx.VERTICAL)
        sizer = wx.BoxSizer(wx.HORIZONTAL)
        sizer.AddMany([((5, 5), 0), (self.bmp, 0, wx.ALIGN_CENTER_VERTICAL),
                       ((5, 5), 0), (self.label, 0, wx.ALIGN_CENTER_VERTICAL),
                       ((-1, 5), 1, wx.EXPAND),
                       (self.button, 0, wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL),
                       ((5, 5), 0)])
        vsizer.AddMany([((5, 5), 0), (sizer, 1, wx.EXPAND), ((5, 5), 0)])
        self.SetSizer(vsizer)

    def OnButton(self, evt):
        self.log.write("Button Pressed: %d" % evt.GetId())

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

overview = eclib.panelbox.__doc__
title = "PanelBox"

#-----------------------------------------------------------------------------#
if __name__ == '__main__':
    try:
        import run
    except ImportError:
        app = wx.PySimpleApp(False)
        frame = wx.Frame(None, title="PanelBox Demo")
        sizer = wx.BoxSizer(wx.HORIZONTAL)
        sizer.Add(TestPanel(frame, TestLog()), 1, wx.EXPAND)
        frame.CreateStatusBar()
        frame.SetSizer(sizer)
        frame.SetInitialSize()
        frame.Show()
        app.MainLoop()
    else:
        run.main(['', os.path.basename(sys.argv[0])] + sys.argv[1:])
