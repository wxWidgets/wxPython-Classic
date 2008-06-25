"""Unit tests for wx.CheckListBox.
        
Methods yet to test:
__init__, Check, Create, GetItemHeight, IsChecked"""

import unittest
import wx

import testListBox

class CheckListBoxTest(testListBox.ListBoxTest):
    def setUp(self):
        self.app = wx.PySimpleApp()
        self.frame = wx.Frame(parent=None, id=wx.ID_ANY)
        self.testControl = wx.CheckListBox(parent=self.frame)
        

if __name__ == '__main__':
    unittest.main()