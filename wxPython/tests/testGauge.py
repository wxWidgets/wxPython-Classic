"""Unit tests for wx.Gauge.

Methods yet to test:
__init__, Create, Pulse"""

import unittest
import wx

import wxtest
import testControl

class GaugeTest(testControl.ControlTest):
    def setUp(self):
        self.frame = wx.Frame(parent=None)
        self.testControl = wx.Gauge(parent=self.frame)
    
    # C++ docs state:
    #   This method is not implemented (returns 0) for most platforms.
    def testBezelFace(self):
        """SetBezelFace, GetBezelFace"""
        if wxtest.PlatformIsMac() or wxtest.PlatformIsGtk() or \
                wxtest.PlatformIsWindows():
            for i in range(self.testControl.GetRange()):
                self.testControl.SetBezelFace(i)
                self.assertEquals(0, self.testControl.GetBezelFace())
        else:
            # this can't happen.
            # TODO: what platforms does it work on?
            raise EnvironmentError("Current platform not represented in wxtest")
    
    def testIsVertical(self):
        """IsVertical"""
        vert  = wx.Gauge(self.frame, style=wx.GA_VERTICAL)
        horiz = wx.Gauge(self.frame, style=wx.GA_HORIZONTAL)
        self.assert_(not self.testControl.IsVertical()) # default
        self.assert_(vert.IsVertical())
        self.assert_(not horiz.IsVertical())
    
    def testRange(self):
        """SetRange, GetRange"""
        for i in range(0,1000,10):
            self.testControl.SetRange(i)
            self.assertEquals(i, self.testControl.GetRange())
    
    # C++ docs state:
    #   This method is not implemented (returns 0) for most platforms.
    def testShadowWidth(self):
        """SetShadowWidth, GetShadowWidth"""
        if wxtest.PlatformIsMac() or wxtest.PlatformIsGtk() or \
                wxtest.PlatformIsWindows():
            for i in range(self.testControl.GetRange()):
                self.testControl.SetShadowWidth(i)
                self.assertEquals(0, self.testControl.GetShadowWidth())
        else:
            # this can't happen.
            # TODO: what platforms does it work on?
            raise EnvironmentError("Current platform not represented in wxtest")
    
    def testValue(self):
        """SetValue, GetValue"""
        for i in range(self.testControl.GetRange()):
            self.testControl.SetValue(i)
            self.assertEquals(i, self.testControl.GetValue())

if __name__ == '__main__':
    unittest.main()