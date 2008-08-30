"""Unit tests for wx.ScrolledWindow.

Methods yet to test:
__init__, AdjustScrollbars, CalcScrolledPosition, CalcScrollInc,
CalcUnscrolledPosition, Create, DoPrepareDC, EnableScrolling,
GetViewStart, Scroll, SetScrollbars"""

import unittest
import wx

import testPanel

class ScrolledWindowTest(testPanel.PanelTest):
    def setUp(self):
        self.frame = wx.Frame(parent=None, id=wx.ID_ANY)
        self.testControl = wx.ScrolledWindow(parent=self.frame)
        self.windows = [ wx.Window(self.frame) for i in range(3) ]
    
    def testScale(self):
        """SetScale, GetScaleX, GetScaleY"""
        for i in range(1000):
            self.testControl.SetScale(i,i)
            self.assertEquals(i, self.testControl.GetScaleX())
            self.assertEquals(i, self.testControl.GetScaleY())
    
    def testScrollPageSize(self):
        """SetScrollPageSize, GetScrollPageSize"""
        for i in range(1000):
            for orient in (wx.HSCROLL, wx.VSCROLL):
                self.testControl.SetScrollPageSize(orient,i)
                self.assertEquals(i, self.testControl.GetScrollPageSize(orient))
    
    def testScrollRate(self):
        """SetScrollRate, GetScrollPixelsPerUnit"""
        # Note asymmetry between accessor methods
        for i in range(1000):
            self.testControl.SetScrollRate(i,i)
            self.assertEquals((i,i), self.testControl.GetScrollPixelsPerUnit())
        for tup in ((99,101),(31,27),(3,5),(1000,1)):
            self.testControl.SetScrollRate(*tup)
            self.assertEquals(tup, self.testControl.GetScrollPixelsPerUnit())
    
    def testTargetWindow(self):
        """SetTargetWindow, GetTargetWindow"""
        for i in range(len(self.windows)):
            window = self.windows[i]
            self.testControl.SetTargetWindow(window)
            self.assertEquals(window, self.testControl.GetTargetWindow())
            for j in range(len(self.windows)):
                if i == j: continue
                self.assertNotEquals(self.windows[j], self.testControl.GetTargetWindow())
            
            
if __name__ == '__main__':
    unittest.main()