"""Unit tests for wx.SpinCtrl

TODO:
    should it be legal for min value to be greater than max value?

Methods yet to test:
__init__, Create, SetSelection"""

import unittest
import wx

import wxtest
import testControl

class SpinCtrlTest(testControl.ControlTest):
    def setUp(self):
        self.frame = wx.Frame(parent=None, id=wx.ID_ANY)
        self.testControl = wx.SpinCtrl(parent=self.frame)
        self.min = -1000
        self.max = 1000
        self.initial = 42
    
    # TODO: crashes interpreter on Windows for some reason
    def testAllControlsNeedParents(self):
        """__init__"""
        if wxtest.PlatformIsNotWindows():
            super(SpinCtrlTest,self).testAllControlsNeedParents()
    
    # TODO: expand tests for constructor; multiple tests, at least one for each option
    def testConstructor(self):
        """__init__"""
        # 'Nearly all of the complexity of the spin ontrol is in the constructor'
        #    - pg.209, 1st paragraph, 'wxPython in Action'
        self.testControl = wx.SpinCtrl(parent=self.frame,
                            min=self.min, max=self.max,
                            initial=self.initial)
        self.assertEquals(self.min, self.testControl.GetMin())
        self.assertEquals(self.max, self.testControl.GetMax())
        self.assertEquals(self.initial, self.testControl.GetValue())
    
    def testMinMaxRange(self):
        """SetRange, GetMin, GetMax"""
        for min,max in ((1,10),(-100,-10),(100,1000)):
            self.testControl.SetRange(min,max)
            self.assertEquals(min, self.testControl.GetMin())
            self.assertEquals(max, self.testControl.GetMax())
    
    def testValue(self):
        """SetValue, GetValue"""
        min = self.testControl.GetMin()
        max = self.testControl.GetMax()
        for i in range(min,max+1):
            self.testControl.SetValue(i)
            self.assertEquals(i, self.testControl.GetValue())
        for j in range(min-100,min):
            self.testControl.SetValue(j)
            self.assertEquals(min, self.testControl.GetValue())
        for k in range(max,max+100):
            self.testControl.SetValue(k)
            self.assertEquals(max, self.testControl.GetValue())
    
    def testValueString(self):
        """SetValueString"""
        min = self.testControl.GetMin()
        max = self.testControl.GetMax()
        for i in range(min,max+1):
            si = str(i)
            self.testControl.SetValueString(si)
            self.assertEquals(i, self.testControl.GetValue())
        for j in range(min-100,min):
            sj = str(j)
            self.testControl.SetValueString(sj)
            self.assertEquals(min, self.testControl.GetValue())
        for k in range(max,max+100):
            sk = str(k)
            self.testControl.SetValueString(sk)
            self.assertEquals(max, self.testControl.GetValue())
            
            
if __name__ == '__main__':
    unittest.main()