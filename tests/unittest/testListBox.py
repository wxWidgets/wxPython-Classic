import unittest
import wx

import testControlWithItems

"""
This file contains classes and methods for unit testing the API of wx.ListBox.

TODO: fill out docs
        
Methods yet to test:
__init__, AppendAndEnsureVisible, Create, DeselectAll, EnsureVisible,
GetSelections, HitTest,
Set, SetFirstItem, SetFirstItemStr, SetStringSelection

These methods don't have corresponding getters:
SetItemBackgroundColour, SetItemFont, SetItemForegroundColour
    
"""

class ListBoxTest(testControlWithItems.ControlWithItemsBase):
    def setUp(self):
        self.app = wx.PySimpleApp()
        self.frame = wx.Frame(parent=None, id=wx.ID_ANY)
        self.testControl = wx.ListBox(parent=self.frame)
    
    def testDeselect(self):
        """Deselect"""
        choices = ['a','b','c','d','e']
        self.testControl.InsertItems(choices,0)
        for i in range(len(choices)):
            self.testControl.Select(i)
            self.assert_(self.testControl.IsSelected(i))
            self.testControl.Deselect(i)
            self.assert_(not self.testControl.IsSelected(i))
    
    def testInsertItems(self):
        """InsertItems"""
        one = ['a','b','c']
        two = ['x','y','z']
        self.testControl.InsertItems(one,0)
        self.assertEquals(one, self.testControl.GetItems())
        self.testControl.InsertItems(two,self.testControl.GetCount())
        self.assertEquals(one+two, self.testControl.GetItems())
        self.testControl.InsertItems(two,0)
        self.assertEquals(two+one+two, self.testControl.GetItems())
    
    def testSelect(self):
        """Select, IsSelected"""
        choices = ['a','b','c','d','e']
        self.testControl.InsertItems(choices,0)
        for i in range(len(choices)):
            self.testControl.Select(i)
            for j in range(len(choices)):
                if i == j:
                    self.assert_(self.testControl.IsSelected(j))
                else:
                    self.assert_(not self.testControl.IsSelected(j))
        
    def testSetSelection(self):
        """SetSelection, IsSelected"""
        choices = ['a','b','c','d','e']
        self.testControl.InsertItems(choices,0)
        for i in range(len(choices)):
            self.testControl.SetSelection(i)
            for j in range(len(choices)):
                if i == j:
                    self.assert_(self.testControl.IsSelected(j))
                else:
                    self.assert_(not self.testControl.IsSelected(j))
    
    def testSorted(self):
        """IsSorted"""
        self.testControl.InsertItems(['a','b','c'],0)
        self.assert_(self.testControl.IsSorted())
        self.testControl = wx.ListBox(self.frame, choices=['z','y','x'])
        self.assert_(not self.testControl.IsSorted())
        

if __name__ == '__main__':
    unittest.main()