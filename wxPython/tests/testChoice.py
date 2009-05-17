"""Unit tests for wx.Choice.
        
Methods yet to test:
__init__, Create, GetCurrentSelection"""

import unittest
import wx

import testControlWithItems

class ChoiceTest(testControlWithItems.ControlWithItemsBase):
    def setUp(self):
        self.frame = wx.Frame(parent=None, id=wx.ID_ANY)
        self.testControl = wx.Choice(parent=self.frame)
        
        
if __name__ == '__main__':
    unittest.main()