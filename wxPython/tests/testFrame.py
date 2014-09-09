"""Unit tests for wx.Frame.

Methods yet to test:
__init__, Command, Create, DoGiveHelp, DoMenuUpdates, GetStatusBarPane, 
ProcessCommand, SendSizeEvent, SetStatusBarPane, SetStatusWidths"""

import unittest
import wx

import wxtest
import testTopLevelWindow

class FrameTest(testTopLevelWindow.TopLevelWindowBase):
    def setUp(self):
        self.frame = wx.Frame(parent=None, id=wx.ID_ANY)
        self.testControl = wx.Frame(parent=self.frame)
        self.texts = ["one","two","three","four","five"]
        self.menubar = wx.MenuBar()
        self.menubar2 = wx.MenuBar()
        self.statusbar = wx.StatusBar(parent=self.testControl, id=wx.ID_ANY)
        self.statusbar2 = wx.StatusBar(parent=self.testControl, id=wx.ID_ANY)
        self.toolbar = wx.ToolBar(self.testControl)
        self.toolbar2 = wx.ToolBar(self.testControl)
    
    def testMenuBar(self):
        """SetMenuBar, GetMenuBar"""
        self.testControl.SetMenuBar(self.menubar)
        self.assertEquals(self.menubar, self.testControl.GetMenuBar())
        self.assertNotEquals(self.menubar, self.menubar2)
        self.testControl.SetMenuBar(self.menubar2)
        self.assertEquals(self.menubar2, self.testControl.GetMenuBar())
        self.assertNotEquals(self.menubar, self.testControl.GetMenuBar())
    
    # see testSize method, below; probably the same issue
    def testRect(self):
        """SetRect, GetRect"""
        if wxtest.PlatformIsWindows():
            self.testControl.SetRect(wx.Rect(0,0,0,0))
            self.assertEquals(wx.Rect(0,0,123,34),self.testControl.GetRect())
        else:
            super(FrameTest,self).testSize()
    
    # wx.Frame's size has a minimum on Windows
    def testSize(self):
        """SetSize, GetSize"""
        if wxtest.PlatformIsWindows():
            self.testControl.SetSize(wx.Size(1,1))
            self.assertEquals(wx.Size(123,34),self.testControl.GetSize())
        else:
            super(FrameTest,self).testSize()
    
    def testStatusBar(self):
        """SetStatusBar, GetStatusBar"""
        self.assertNotEquals(self.statusbar,self.statusbar2) # sanity check
        self.testControl.SetStatusBar(self.statusbar)
        self.assertEquals(self.statusbar, self.testControl.GetStatusBar())
        self.testControl.SetStatusBar(self.statusbar2)
        self.assertEquals(self.statusbar2, self.testControl.GetStatusBar())
        self.assertNotEquals(self.statusbar, self.testControl.GetStatusBar())
        
    def testStatusBarCreation(self):
        """CreateStatusBar, GetStatusBar"""
        if wxtest.ASSERTIONS_ON:
            self.assertRaises(wx.PyAssertionError, self.testControl.PushStatusText, "text")
        else:
            self.testControl.PushStatusText("text")
        sb = self.testControl.CreateStatusBar()
        self.testControl.PushStatusText("text") # test that it doesn't blow up
        self.assert_(isinstance(self.testControl.GetStatusBar(), wx.StatusBar))
        self.assertEquals(sb, self.testControl.GetStatusBar())
    
    def testStatusBarPushPop(self):
        """PushStatusText, PopStatusText"""
        self.testControl.SetStatusBar(self.statusbar)
        for txt in self.texts:
            self.testControl.PushStatusText(txt)
        for t in self.texts[::-1]:
            self.assertEquals(t, self.statusbar.GetStatusText())
            self.testControl.PopStatusText()
    
    def testStatusBarText(self):
        """SetStatusText, GetStatusText"""
        self.testControl.SetStatusBar(self.statusbar)
        for txt in self.texts:
            self.testControl.SetStatusText(txt)
            self.assertEquals(txt, self.statusbar.GetStatusText())
    
    def testToolBar(self):
        """CreateToolBar"""
        tb = self.testControl.CreateToolBar()
        self.assertEquals(tb, self.testControl.GetToolBar())
    
    def testToolBarCreation(self):
        """SetToolBar, GetToolBar"""
        self.assertNotEquals(self.toolbar,self.toolbar2) # sanity check
        self.testControl.SetToolBar(self.toolbar)
        self.assertEquals(self.toolbar, self.testControl.GetToolBar())
        self.testControl.SetToolBar(self.toolbar2)
        self.assertEquals(self.toolbar2, self.testControl.GetToolBar())
        self.assertNotEquals(self.toolbar, self.testControl.GetToolBar())
    

if __name__ == '__main__':
    unittest.main()
