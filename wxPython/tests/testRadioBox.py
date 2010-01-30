"""Unit tests for wx.RadioBox.

NOTE:
    wx.RadioBox has a GetCount method which isn't in the online docs,
    but is in "wxPython in Action".  The same goes for the 'Enable' method.
        
Methods yet to test:
__init__, Create, GetNextItem"""

import unittest
import wx

import testControl

class RadioBoxTest(testControl.ControlTest):
    def __init__(self, arg):
        # superclass setup
        super(RadioBoxTest,self).__init__(arg)
        self.choices = ["one","two","three","four","five"]
        
    def setUp(self):
        self.frame = wx.Frame(parent=None, id=wx.ID_ANY)
        self.testControl = wx.RadioBox(parent=self.frame,
                                choices=self.choices,
                                majorDimension=1,
                                style=wx.RA_SPECIFY_COLS # default
                                )
    
    def testColumnCount(self):
        """GetColumnCount"""
        self.assertEquals(1, self.testControl.GetColumnCount())
        self.testControl = wx.RadioBox(self.frame, choices=self.choices,
                                        majorDimension=1, style=wx.RA_SPECIFY_ROWS)
        self.assertEquals(len(self.choices), self.testControl.GetColumnCount())
    
    def testCount(self):
        """GetCount"""
        # TODO: This function needs to be documented.
        self.assertEquals(len(self.choices), self.testControl.GetCount())
    
    def testEnable(self):
        """Enable"""
        self.testControl.Enable()
        for i in range(self.testControl.GetCount()):
            self.assert_(self.testControl.IsItemEnabled(i))
    
    def testEnableItem(self):
        """EnableItem, IsItemEnabled"""
        for i in range(self.testControl.GetCount()):
            self.testControl.EnableItem(i)
            self.assert_(self.testControl.IsItemEnabled(i))
            self.testControl.EnableItem(i,False)
            self.assert_(not self.testControl.IsItemEnabled(i))
            self.testControl.EnableItem(i,True)
            self.assert_(self.testControl.IsItemEnabled(i))
    
    def testFindString(self):
        """FindString"""
        for i in range(len(self.choices)):
            index = self.testControl.FindString(self.choices[i])
            self.assertEquals(i, index)
        self.assertEquals(-1,self.testControl.FindString("asdfjkl;"))
    
    def testGetName(self):
        """GetName"""
        # Overrides testGetName in testControl
        self.testControl = wx.RadioBox(parent=self.frame,
                                    name=self.name, choices=self.choices)
            # needs a non-empty choices list or throws exception (on Windows)
            # TODO: test this or report it
        self.assertEquals(self.name, self.testControl.GetName())
        
    def testGetString(self):
        """GetString"""
        for i in range(len(self.choices)):
            self.assertEquals(self.choices[i], self.testControl.GetString(i))
    
    def testItemHelpText(self):
        """SetItemHelpText, GetItemHelpText"""
        for i in range(len(self.choices)):
            txt = "HelpText" + str(i)
            self.testControl.SetItemHelpText(i,txt)
            self.assertEquals(txt, self.testControl.GetItemHelpText(i))
    
    def testItemLabel(self):
        """SetItemLabel, GetItemLabel"""
        for i in range(len(self.choices)):
            txt = "LabelText" + str(i)
            self.testControl.SetItemLabel(i,txt)
            self.assertEquals(txt, self.testControl.GetItemLabel(i))
        
    def testItemToolTip(self):
        """SetItemToolTip, GetItemToolTip"""
        for i in range(len(self.choices)):
            txt = "ItemToolTipText" + str(i)
            self.testControl.SetItemToolTip(i,txt)
            self.assertEquals(txt, self.testControl.GetItemToolTip(i).GetTip())
                        # returns a wx.ToolTip
        
    def testRowCount(self):
        """GetRowCount"""
        self.assertEquals(len(self.choices), self.testControl.GetRowCount())
        self.testControl = wx.RadioBox(self.frame, choices=self.choices,
                                        majorDimension=1, style=wx.RA_SPECIFY_ROWS)
        self.assertEquals(1, self.testControl.GetRowCount())
    
    def testSelection(self):
        """SetSelection, GetSelection"""
        for i in range(self.testControl.GetCount()):
            self.testControl.SetSelection(i)
            self.assertEquals(i, self.testControl.GetSelection())
    
    def testSetString(self):
        """SetString"""
        for i in range(len(self.choices)):
            self.testControl.SetString(i, str(i))
            self.assertEquals(str(i), self.testControl.GetString(i))
    
    def testShowItem(self):
        """ShowItem, IsItemShown"""
        for i in range(self.testControl.GetCount()):
            self.testControl.ShowItem(i)
            self.assert_(self.testControl.IsItemShown(i))
            self.testControl.ShowItem(i,False)
            self.assert_(not self.testControl.IsItemShown(i))
            self.testControl.ShowItem(i,True)
            self.assert_(self.testControl.IsItemShown(i))
    
    def testStringSelection(self):
        """GetStringSelection, SetStringSelection"""
        for i in range(len(self.choices)):
            sel = self.choices[i]
            self.assert_(self.testControl.SetStringSelection(sel))
            self.assertEquals(sel, self.testControl.GetStringSelection())
            
            
if __name__ == '__main__':
    unittest.main()