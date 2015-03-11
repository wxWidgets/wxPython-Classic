###############################################################################
# Name: ProgressStatusBarDemo.py                                              #
# Purpose: Test and demo of ProgressStatusBar class.                          #
# Author: Cody Precord <cprecord@editra.org>                                  #
# Copyright: (c) 2009 Cody Precord <staff@editra.org>                         #
# Licence: wxWindows Licence                                                  #
###############################################################################

"""
Test file for testing the ProgressStatusBar control

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
        self.button = wx.Button(self, label="Show ProgressStatusBar Demo")

        # Layout
        self.__DoLayout()

        # Event Handlers
        self.button.Bind(wx.EVT_BUTTON, self.OnButton)

    def __DoLayout(self):
        """Layout the panel"""
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.AddStretchSpacer()
        sizer.Add(self.button, 0, wx.ALIGN_CENTER)
        sizer.AddStretchSpacer()

        hsizer = wx.BoxSizer(wx.HORIZONTAL)
        hsizer.AddStretchSpacer()
        hsizer.Add(sizer, 0, wx.ALIGN_CENTER)
        hsizer.AddStretchSpacer()

        self.SetSizer(hsizer)

    def OnButton(self, evt):
        frame = PBSDemoFrame()
        frame.Show()

#----------------------------------------------------------------------

ID_START = wx.NewId()
ID_START_BUSY = wx.NewId()

class PBSDemoFrame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, title="ProgressStatusBar Demo")

        # Attributes
        self.panel = PBSDemoPanel(self)
        self.timer = wx.Timer(self)

        # Layout
        self.__DoLayout()

        # Event Handlers
        self.Bind(wx.EVT_BUTTON, self.OnButton)
        self.Bind(wx.EVT_TIMER, self.OnTimer)

    def __del__(self):
        if self.timer.IsRunning():
            self.timer.Stop()

    def __DoLayout(self):
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.panel, 1, wx.EXPAND)
        self.SetSizer(sizer)
        # NOTE: must use SB_FLAT style
        # TODO: fix this in control to enforce this req.
        statb = eclib.ProgressStatusBar(self, style=wx.SB_FLAT)
        statb.SetRange(1024)
        self.SetStatusBar(statb)

    def OnButton(self, evt):
        e_id = evt.GetId()
        statb = self.GetStatusBar()
        self.panel.SetButtonState(e_id)

        if e_id == wx.ID_STOP:
            statb.SetStatusText(u"", 0)
            if self.timer.IsRunning():
                self.timer.Stop()
            statb.Stop()
            
        elif e_id == ID_START:
            # Start timer to simulate updates with
            statb.ShowProgress()
            self.timer.Start(125)
        elif e_id == ID_START_BUSY:
            statb.StartBusy()
            self.SetStatusText("Busy...", 0)
        else:
            evt.Skip()

    def OnTimer(self, evt):
        statb = self.GetStatusBar()
        cprog = statb.GetProgress()
        cprog += 8
        if cprog > 1024:
            cprog = 0
        statb.SetProgress(cprog)
        self.SetStatusText("Processing %d of 1024" % cprog, 0)

#----------------------------------------------------------------------

class PBSDemoPanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)

        # Attributes
        self.startb = wx.Button(self, ID_START, label="Start")
        self.startb.SetToolTipString("Click to start progress bar")
        self.busyb = wx.Button(self, ID_START_BUSY, label="Start Busy")
        self.busyb.SetToolTipString("Click to start progress bar in 'Busy' mode")
        self.stopb = wx.Button(self, wx.ID_STOP, label="Stop")
        self.stopb.SetToolTipString("Stop and hide the progress gauge")
        self.stopb.Disable()

        # Layout
        self.__DoLayout()

    def __DoLayout(self):
        sizer = wx.BoxSizer(wx.HORIZONTAL)
        sizer.AddMany([((-1, 5), 0, wx.EXPAND),
                       (self.startb, 0, wx.ALIGN_CENTER_VERTICAL),
                       (self.busyb, 0, wx.ALIGN_CENTER_VERTICAL),
                       (self.stopb, 0, wx.ALIGN_CENTER_VERTICAL),
                       ((-1, 5), 0, wx.EXPAND)])
        vsizer = wx.BoxSizer(wx.VERTICAL)
        vsizer.Add(sizer, 1, wx.ALIGN_CENTER)
        self.SetSizer(vsizer)

    def SetButtonState(self, state):
        if state in (ID_START, ID_START_BUSY):
            self.busyb.Disable()
            self.startb.Disable()
            self.stopb.Enable()
        elif state == wx.ID_STOP:
            self.busyb.Enable()
            self.startb.Enable()
            self.stopb.Disable()
        else:
            pass

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

overview = eclib.pstatbar.__doc__
title = "ProgressStatusBar"

#-----------------------------------------------------------------------------#
if __name__ == '__main__':
    try:
        import run
    except ImportError:
        app = wx.PySimpleApp(False)
        frame = wx.Frame(None, title="ProgressStatusBar Demo")
        sizer = wx.BoxSizer(wx.HORIZONTAL)
        sizer.Add(TestPanel(frame, TestLog()), 1, wx.EXPAND)
        frame.CreateStatusBar()
        frame.SetSizer(sizer)
        frame.Show()
        app.MainLoop()
    else:
        run.main(['', os.path.basename(sys.argv[0])] + sys.argv[1:])
