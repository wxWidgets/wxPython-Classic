"""Unit tests for wx.ComboBox.
        
Methods yet to test:
__init__, CanCopy, CanCut, CanPaste, CanRedo, CanUndo, Copy, Create,
Cut, GetCurrentSelection, GetInsertionPoint, GetLastPosition, GetMark,
Paste, Redo, Remove, Replace, SelectAll, SetInsertionPoint, 
SetInsertionPointEnd, SetMark, SetStringSelection, Undo"""

import unittest
import wx

import testChoice

class ComboBoxTest(testChoice.ChoiceTest):
    def setUp(self):
        self.frame = wx.Frame(parent=None, id=wx.ID_ANY)
        self.testControl = wx.ComboBox(parent=self.frame)
    
    def testEditable(self):
        """__init__, IsEditable"""
        self.assert_(self.testControl.IsEditable())
        self.testControl = wx.ComboBox(self.frame, style=wx.CB_READONLY)
        self.assert_(not self.testControl.IsEditable())
    
    def testSetEditable(self):
        """SetEditable, IsEditable"""
        self.testControl.SetEditable(True)
        self.assert_(self.testControl.IsEditable())
        self.testControl.SetEditable(False)
        self.assert_(not self.testControl.IsEditable())
    
    def testValue(self):
        """SetValue, GetValue"""
        txt1 = "Hello"
        txt2 = "World"
        self.testControl.SetValue(txt1)
        self.assertEquals(txt1, self.testControl.GetValue())
        self.testControl.SetValue(txt2)
        self.assertEquals(txt2, self.testControl.GetValue())
        self.assertNotEquals(txt1, self.testControl.GetValue())
        

if __name__ == '__main__':
    unittest.main()