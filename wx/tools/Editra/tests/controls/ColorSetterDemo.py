###############################################################################
# Name: ColorSetterDemo.py                                                    #
# Purpose: Test and demo file for eclib.ColorSetter control                   #
# Author: Cody Precord <cprecord@editra.org>                                  #
# Copyright: (c) 2009 Cody Precord <staff@editra.org>                         #
# Licence: wxWindows Licence                                                  #
###############################################################################

"""
Test file for testing the ColorSetter control

"""

__author__ = "Cody Precord <cprecord@editra.org>"
__svnid__ = "$Id$"
__revision__ = "$Revision$"

#-----------------------------------------------------------------------------#
# Imports
import os
import sys
import wx

# Put local package on the path
#sys.path.insert(0, os.path.abspath('../../src'))
import eclib

#-----------------------------------------------------------------------------#

class TestPanel(wx.Panel):
    def __init__(self, parent, log):
        wx.Panel.__init__(self, parent, wx.ID_ANY, size=(500,500))

        # Attributes
        self.log = log

        # Layout
        self.__DoLayout()

        # Event Handers
        self.Bind(eclib.EVT_COLORSETTER, self.OnColorChange)

    def __DoLayout(self):
        """Layout the panel"""
        gs = wx.GridSizer(3, 2, 5, 15)
        colors = ('red', 'yellow', 'green', 'blue', 'orange', 'purple')
        for color in colors:
            cobj = wx.TheColourDatabase.FindColour(color)
            csetter = eclib.ColorSetter(self, wx.ID_ANY, cobj)
            gs.Add(csetter)

        sizer = wx.BoxSizer(wx.HORIZONTAL)
        sizer.Add(gs, 0, wx.ALIGN_CENTER|wx.ALL, 5)
        vsizer = wx.BoxSizer(wx.VERTICAL)
        vsizer.AddStretchSpacer()
        vsizer.Add(sizer, 0, wx.ALIGN_CENTER)
        vsizer.AddStretchSpacer()

        self.SetSizer(vsizer)
        self.SetAutoLayout(True)

    def OnColorChange(self, evt):
        """Called when the color selection has changed in
        the colorsetter control.

        """
        eid= evt.GetId()
        val = evt.GetValue()
        self.log.write("ColorSetter Change: Id=%d, Val=%s" % (eid, val))

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

overview = eclib.colorsetter.__doc__
title = "ColorSetter"

#-----------------------------------------------------------------------------#
if __name__ == '__main__':
    try:
        import sys
        import run
    except ImportError:
        app = wx.PySimpleApp(False)
        frame = wx.Frame(None, title="ColorSetter Demo")
        sizer = wx.BoxSizer(wx.HORIZONTAL)
        sizer.Add(TestPanel(frame, TestLog()), 1, wx.EXPAND)
        frame.CreateStatusBar()
        frame.SetSizer(sizer)
        frame.SetInitialSize()
        frame.Show()
        app.MainLoop()
    else:
        run.main(['', os.path.basename(sys.argv[0])] + sys.argv[1:])
