import unittest
import wx

import testControlWithItems

"""
This file contains classes and methods for unit testing the API of wx.Choice.
        
Methods yet to test:
__init__, Create, GetCurrentSelection
"""

class ChoiceTest(testControlWithItems.ControlWithItemsBase):
    def setUp(self):
        self.app = wx.PySimpleApp()
        self.frame = wx.Frame(parent=None, id=wx.ID_ANY)
        self.testControl = wx.Choice(parent=self.frame)
        
        
if __name__ == '__main__':
    unittest.main()