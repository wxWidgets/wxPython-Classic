"""Unit tests for wx.ListBox.
        
Methods yet to test:
__init__, AppendAndEnsureVisible, Create, DeselectAll, EnsureVisible,
GetSelections, HitTest,
Set, SetFirstItem, SetFirstItemStr, SetStringSelection

These methods don't have corresponding getters:
SetItemBackgroundColour, SetItemFont, SetItemForegroundColour"""

import unittest
import wx

import testControlWithItems

class ListBoxTest(testControlWithItems.ControlWithItemsBase):
    def __init__(self, arg):
        # superclass setup
        super(ListBoxTest,self).__init__(arg)
        self.name = "Name of Control"
        self.choices = ["a","b","c","d","e"]
        self.more_choices = ["w","x","y","z"]
        
    def setUp(self):
        self.frame = wx.Frame(parent=None, id=wx.ID_ANY)
        self.testControl = wx.ListBox(parent=self.frame)
    
    def testDeselect(self):
        """Deselect"""
        self.testControl.InsertItems(self.choices,0)
        for i in range(len(self.choices)):
            self.testControl.Select(i)
            self.assert_(self.testControl.IsSelected(i))
            self.testControl.Deselect(i)
            self.assert_(not self.testControl.IsSelected(i))
    
    def testInsertItems(self):
        """InsertItems"""
        self.testControl.InsertItems(self.choices,0)
        self.assertEquals(self.choices, self.testControl.GetItems())
        self.testControl.InsertItems(self.more_choices,self.testControl.GetCount())
        even_more = self.choices + self.more_choices
        self.assertEquals(even_more, self.testControl.GetItems())
        self.testControl.InsertItems(self.more_choices,0)
        most = self.more_choices + even_more
        self.assertEquals(most, self.testControl.GetItems())
    
    def testSelect(self):
        """Select, IsSelected"""
        self.testControl.InsertItems(self.choices,0)
        for i in range(len(self.choices)):
            self.testControl.Select(i)
            for j in range(len(self.choices)):
                if i == j:
                    self.assert_(self.testControl.IsSelected(j))
                else:
                    self.assert_(not self.testControl.IsSelected(j))
        
    def testSetSelection(self):
        """SetSelection, IsSelected"""
        self.testControl.InsertItems(self.choices,0)
        for i in range(len(self.choices)):
            self.testControl.SetSelection(i)
            for j in range(len(self.choices)):
                if i == j:
                    self.assert_(self.testControl.IsSelected(j))
                else:
                    self.assert_(not self.testControl.IsSelected(j))
                    
    def testSorted(self):
        """IsSorted"""
        self.choices.reverse() # prove the wx.LB_SORT flag sorts them
        self.testControl = wx.ListBox(self.frame, choices=self.choices)
        self.assert_(not self.testControl.IsSorted())
        self.testControl = wx.ListBox(self.frame, choices=self.choices,
                                            style=wx.LB_SORT)
        self.assert_(self.testControl.IsSorted())
        

if __name__ == '__main__':
    unittest.main()