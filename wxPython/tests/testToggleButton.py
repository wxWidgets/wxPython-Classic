"""Unit tests for wx.ToggleButton.

This class is virtually fully-tested."""

import unittest
import wx

import testControl

class ToggleButtonTest(testControl.ControlTest):
    def setUp(self):
        self.frame = wx.Frame(parent=None, id=wx.ID_ANY)
        self.testControl = wx.ToggleButton(parent=self.frame)
        
    def testSetValueFails(self):
        """SetValue"""
        # That SetValue must be called with one and only one argument
        self.assertRaises(TypeError, self.testControl.SetValue)
        self.assertRaises(TypeError, self.testControl.SetValue, True, True)
    
    def testValue(self):
        """SetValue, GetValue"""
        self.assert_(not self.testControl.GetValue())
        self.testControl.SetValue(True)
        self.assert_(self.testControl.GetValue())
        self.testControl.SetValue(False)
        self.assert_(not self.testControl.GetValue())
        

if __name__ == '__main__':
    unittest.main()