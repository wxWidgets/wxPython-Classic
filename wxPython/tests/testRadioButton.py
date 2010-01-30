"""Unit tests for wx.RadioButton.
        
Methods yet to test:
__init__, Create"""

import unittest
import wx

import testControl

class RadioButtonTest(testControl.ControlTest):
    def setUp(self):
        self.frame = wx.Frame(parent=None, id=wx.ID_ANY)
        self.label = "Label of the RadioButton!"
        self.testControl = wx.RadioButton(parent=self.frame, label=self.label,
                                style=wx.RB_GROUP)
        
    def testDifferentGroupsToggle(self):
        """ """
        one = [ wx.RadioButton(self.frame, style=wx.RB_GROUP),
                wx.RadioButton(self.frame),
                wx.RadioButton(self.frame) ]
        two = [ wx.RadioButton(self.frame, style=wx.RB_GROUP),
                wx.RadioButton(self.frame),
                wx.RadioButton(self.frame) ]
        for i in range(len(one)):
            one[i].SetValue(True)
            for j in range(len(two)):
                two[j].SetValue(True)
                for rb in two:
                    if rb == two[j]:
                        self.assert_(rb.GetValue())
                    else:
                        self.assert_(not rb.GetValue())
                        
    def testLabel(self):
        """GetLabel"""
        # Overrides previous testLabel method
        self.assertEquals(self.label, self.testControl.GetLabel())
    
    def testToggle(self):
        """ """
        a = wx.RadioButton(self.frame, label="a")
        b = wx.RadioButton(self.frame, label="b")
        self.testControl.SetValue(True)
        self.assert_(self.testControl.GetValue())
        for rad in (a,b):
            self.assert_(not rad.GetValue())
        a.SetValue(True)
        self.assert_(a.GetValue())
        for rad in (b,self.testControl):
            self.assert_(not rad.GetValue())
        b.SetValue(True)
        self.assert_(b.GetValue())
        for rad in (a,self.testControl):
            self.assert_(not rad.GetValue())
        
    def testValue(self):
        """SetValue, GetValue"""
        self.testControl.SetValue(True)
        self.assert_(self.testControl.GetValue())
        self.testControl.SetValue(False)
        self.assert_(not self.testControl.GetValue())
        
        
if __name__ == '__main__':
    unittest.main()