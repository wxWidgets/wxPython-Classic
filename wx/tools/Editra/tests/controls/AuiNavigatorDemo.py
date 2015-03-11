###############################################################################
# Name: AuiPaneNavigator.py                                                   #
# Purpose: Test and demo file for eclib.AuiPaneNavigator                      #
# Author: Cody Precord <cprecord@editra.org>                                  #
# Copyright: (c) 2009 Cody Precord <staff@editra.org>                         #
# Licence: wxWindows Licence                                                  #
###############################################################################

"""
Test file for testing the AuiPaneNavigator

"""

__author__ = "Cody Precord <cprecord@editra.org>"
__svnid__ = "$Id$"
__revision__ = "$Revision$"

#-----------------------------------------------------------------------------#
# Imports
import os
import sys
import wx
import wx.aui as aui

import IconFile

# Put local package on the path
#sys.path.insert(0, os.path.abspath('../../src'))
import eclib

#-----------------------------------------------------------------------------#
ID_NAVI = wx.NewId()

#-----------------------------------------------------------------------------#

class TestPanel(wx.Panel):
    def __init__(self, parent, log):
        wx.Panel.__init__(self, parent, wx.ID_ANY, size=(500,500))

        # Attributes
        self._paneNavi = None
        self.mgr = aui.AuiManager(self, aui.AUI_MGR_ALLOW_ACTIVE_PANE|aui.AUI_MGR_TRANSPARENT_HINT)
        self.log = log

        # Setup
        panes = list()
        for pane in range(4):
            tmp = wx.Panel(self, size=(100,100))
            panes.append(tmp)

        if wx.Platform != '__WXMAC__':
            txt = wx.StaticText(panes[0], label="Ctrl+1 to activate navigator")
        else:
            txt = wx.StaticText(panes[0], label="Alt+Tab to activate navigator")
        sizer = wx.BoxSizer()
        sizer.Add(txt, 0, wx.ALIGN_CENTER|wx.ALL, 20)
        panes[0].SetSizer(sizer)

        # Populate aui manager
        name = "Panel%s"
        pos = ['Center', 'Left', 'Top', 'Right']
        for idx, pane in enumerate(panes):
            tmp = name % idx
            if idx > 0:
                txt = wx.TextCtrl(pane)
                s = wx.BoxSizer()
                s.Add(txt, 1, wx.EXPAND)
                pane.SetSizer(s)

            ai = aui.AuiPaneInfo().Caption(tmp).MinSize((100,100)).Name(tmp)
            ai = getattr(ai, pos[idx])()
            self.mgr.AddPane(pane, ai)
        self.mgr.Update()

        tlw = self.GetTopLevelParent()
        if wx.Platform != '__WXMAC__':
            tbl = wx.AcceleratorTable([(wx.ACCEL_CTRL, ord('1'), ID_NAVI)])
        else:
            tbl = wx.AcceleratorTable([(wx.ACCEL_ALT, wx.WXK_TAB, ID_NAVI)])
        tlw.SetAcceleratorTable(tbl)
        tlw.Bind(wx.EVT_MENU, self.OnNavigate, id=ID_NAVI)

        self.Bind(wx.EVT_WINDOW_DESTROY, self.OnDestroy)

    def OnDestroy(self, evt):
        # DEMO hack unbind event handler on delete
        tlw = self.GetTopLevelParent()
        if tlw is not None:
            tlw.Unbind(wx.EVT_MENU, tlw, id=ID_NAVI)
            tlw.SetAcceleratorTable(wx.AcceleratorTable([]))

    def OnNavigate(self, evt):
        """Make use of the AuiPaneNavigator"""
        if self._paneNavi is not None:
            evt.Skip()
            return

        self._paneNavi = eclib.AuiPaneNavigator(self,
                                                self.mgr,
                                                IconFile.Address.GetBitmap(),
                                                "Navigator Test")
        self._paneNavi.SetReturnCode(wx.ID_OK)
        self._paneNavi.ShowModal()

        sel = self._paneNavi.GetSelection()
        self._paneNavi.Destroy()
        self._paneNavi = None

        if isinstance(sel, basestring):
            paneInfo = self.mgr.GetPane(sel)
            if paneInfo.IsOk():
                if not paneInfo.IsShown():
                    paneInfo.Show()
                    self.mgr.Update()
                paneInfo.window.SetFocus()

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

overview = eclib.auinavi.__doc__
title = "AuiPaneNavigator"

#-----------------------------------------------------------------------------#
if __name__ == '__main__':
    try:
        import run
    except ImportError:
        app = wx.PySimpleApp(False)
        frame = wx.Frame(None, title="AuiPaneNavigator Demo")
        sizer = wx.BoxSizer(wx.HORIZONTAL)
        sizer.Add(TestPanel(frame, TestLog()), 1, wx.EXPAND)
        frame.CreateStatusBar()
        frame.SetSizer(sizer)
        frame.SetInitialSize((300, 300))
        frame.Show()
        app.MainLoop()
    else:
        run.main(['', os.path.basename(sys.argv[0])] + sys.argv[1:])
