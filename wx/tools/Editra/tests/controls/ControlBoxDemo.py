###############################################################################
# Name: ControlBoxDemo.py                                                     #
# Purpose: ControlBox and ControlBar Test and Demo File                       #
# Author: Cody Precord <cprecord@editra.org>                                  #
# Copyright: (c) 2008 Cody Precord <staff@editra.org>                         #
# Licence: wxWindows Licence                                                  #
###############################################################################

"""
Test file for testing the ControlBox, ControlBar, and SegmentBar classes

"""

__author__ = "Cody Precord <cprecord@editra.org>"
__svnid__ = "$Id$"
__revision__ = "$Revision$"

#-----------------------------------------------------------------------------#
# Imports
import time
import random
import sys
import os
import wx

#sys.path.insert(0, os.path.abspath('../../src'))
import eclib

# Local imports
import IconFile

#-----------------------------------------------------------------------------#
# Globals
ID_SHOW_CONTROL = wx.NewId()
ID_SHOW_SEGMENT = wx.NewId()

#-----------------------------------------------------------------------------#

class TestPanel(eclib.ControlBox):
    def __init__(self, parent, log):
        super(TestPanel, self).__init__(parent)

        # Attributes
        self.log = log

        # Setup
        self.CreateControlBar()
        cbar = self.GetControlBar()
        cbar.SetMargins(2, 2)
        cbar.AddControl(wx.Button(cbar, ID_SHOW_CONTROL, label="Show ControlBar Sample"))
        cbar.AddControl(wx.Button(cbar, ID_SHOW_SEGMENT, label="Show SegmentBar Sample"))
        text = wx.TextCtrl(self, style=wx.TE_MULTILINE|wx.TE_RICH2)
        text.SetValue("Welcome to the ControlBox Sample.\n\nThis window is a "
                      "ControlBox containing a TextCtrl and a ControlBar in it.\n\n"
                      "Click a button to see the extended samples.")
        self.SetWindow(text)

        # Event Handlers
        self.Bind(wx.EVT_BUTTON, self.OnButton)

    def OnButton(self, evt):
        """Handle Button Events"""
        e_id = evt.GetId()
        if e_id == ID_SHOW_CONTROL:
            # Show a Frame with a ControlBox using ControlBars in it
            frame = MakeTestFrame(self, "ControlBar Sample", self.log, False)
            frame.Show()
        elif e_id == ID_SHOW_SEGMENT:
            # Show a frame with a ControlBox using SegmentBars in it
            frame = MakeTestFrame(self, "SegmentBar Sample", self.log, True)
            frame.Show()
        else:
            evt.Skip()

#-----------------------------------------------------------------------------#

class ControlBarPanel(eclib.ControlBox):
    def __init__(self, parent, log):
        super(ControlBarPanel, self).__init__(parent)

        # Attributes
        self.log = log
        self.gauge = None
        self._timer = wx.Timer(self)

        # Setup
        if random.choice((True, False)):
            orient1 = wx.TOP
            orient2 = wx.BOTTOM
            edgealign = wx.ALIGN_RIGHT
        else:
            orient1 = wx.LEFT
            orient2 = wx.RIGHT
            edgealign = wx.ALIGN_BOTTOM

        cbar = self.CreateControlBar(pos=orient1)
        cbar.SetMargins(1, 1)
        err_bmp = wx.ArtProvider.GetBitmap(wx.ART_ERROR, wx.ART_MENU, (16, 16))
        w_bmp = wx.ArtProvider.GetBitmap(wx.ART_WARNING, wx.ART_MENU, (16, 16))
        cbar.AddTool(wx.ID_ANY, err_bmp, "hello world")
        cbar.AddTool(wx.ID_ANY, w_bmp, "warning")
        # only add other controls in horizontal mode (for aesthetics reasons)
        if not cbar.IsVerticalMode():
            cbar.AddStretchSpacer()
            choice = wx.Choice(cbar, wx.ID_ANY, choices=[str(x) for x in range(10)])
            cbar.AddControl(choice, edgealign)
            cbar.AddControl(wx.Button(cbar, label="New Frame"), edgealign)

        bbar = self.CreateControlBar(orient2)
        bbar.SetMargins(1, 1)
        bbar.AddTool(wx.ID_ANY, err_bmp, "HELLO")
        # Only add other controls in horizontal mode
        self.gauge = None
        if not bbar.IsVerticalMode():
            bbar.AddStretchSpacer()
            self.gauge = wx.Gauge(bbar, size=(100, 16))
            bbar.AddControl(self.gauge, edgealign)

        self.SetWindow(wx.TextCtrl(self, style=wx.TE_MULTILINE))
        self.Bind(eclib.EVT_CTRLBAR, self.OnControlBar)
        self.Bind(wx.EVT_BUTTON, self.OnButton)
        self.Bind(wx.EVT_TIMER, self.OnTimer)

        self._timer.Start(150)

    def OnControlBar(self, evt):
        self.log.write("ControlBarEvent: %d" % evt.GetId())

    def OnButton(self, evt):
        self.log.write("Button tool clicked: Id=%d" % evt.GetId())
        frame = MakeTestFrame(self, "Random Test Frame", self.log,
                              bool(long(time.time()) % 2))
        frame.Show()

    def OnTimer(self, evt):
        if self.gauge:
            self.gauge.Pulse()

#-----------------------------------------------------------------------------#

class SegmentPanel(eclib.ControlBox):
    def __init__(self, parent, log):
        super(SegmentPanel, self).__init__(parent)

        # Attributes
        self.log = log

        # Make up the top segment bar
        segbar = eclib.SegmentBar(self, style=eclib.CTRLBAR_STYLE_GRADIENT|\
                                              eclib.CTRLBAR_STYLE_LABELS|\
                                              eclib.CTRLBAR_STYLE_NO_DIVIDERS)
        for num in range(5):
            if num % 2:
                segbar.AddSegment(wx.NewId(), IconFile.Home.GetBitmap(), label=u'Home')
            else:
                segbar.AddSegment(wx.NewId(), IconFile.Monkey.GetBitmap(), label=u'Monkey')

        segbar.SetSegmentOption(4, eclib.SEGBTN_OPT_CLOSEBTNR)
        segbar.SetSegmentOption(3, eclib.SEGBTN_OPT_CLOSEBTNL)
        segbar.SetSegmentOption(2, eclib.SEGBTN_OPT_CLOSEBTNL)

        # Make a bottom segment bar
        segbar2 = eclib.SegmentBar(self, style=eclib.CTRLBAR_STYLE_GRADIENT)
        for num in range(5):
            if num % 2:
                segbar2.AddSegment(wx.NewId(), IconFile.Book.GetBitmap())
            else:
                segbar2.AddSegment(wx.NewId(), IconFile.Address.GetBitmap())

        # Put the components together
        self.SetControlBar(segbar, wx.TOP)
        self.SetControlBar(segbar2, wx.BOTTOM)
        self.SetWindow(wx.TextCtrl(self, style=wx.TE_MULTILINE, value="Hello World"))

        # Event Handlers
        self.Bind(eclib.EVT_SEGMENT_SELECTED, self.OnSegmentClicked)

    def OnSegmentClicked(self, evt):
        cur = evt.GetCurrentSelection()
        pre = evt.GetPreviousSelection()
        self.log.write("Segment Clicked: Cur=%d, Pre=%d, Id=%d" % (cur, pre, evt.GetId()))

#-----------------------------------------------------------------------------#

def MakeTestFrame(caller, title, log, segment=False):
    frame = wx.Frame(None, title=title)
    fsizer = wx.BoxSizer(wx.VERTICAL)
    if not segment:
        panel = ControlBarPanel(frame, log)
    else:
        panel = SegmentPanel(frame, log)
    fsizer.Add(panel, 1, wx.EXPAND)
    frame.SetSizer(fsizer)

    # Adjust Window Position
    if caller is not None:
        pos = caller.GetScreenPosition()
        frame.SetPosition((pos[0]+22, pos[1]+22))

    return frame

#-----------------------------------------------------------------------------#

class TestLog:
    def __init__(self):
        pass

    def write(self, msg):
        print msg

#-----------------------------------------------------------------------------#

overview = eclib.ctrlbox.__doc__
title = "ControlBox"

#-----------------------------------------------------------------------------#

if __name__ == '__main__':
    try:
        import run
    except ImportError:
        app = wx.PySimpleApp(False)
        frame = wx.Frame(None, title="ControlBox Test")
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(TestPanel(frame, TestLog()), 1, wx.EXPAND)
        frame.SetSizer(sizer)
        frame.Show()
        app.MainLoop()
    else:
        run.main(['', os.path.basename(sys.argv[0])] + sys.argv[1:])
