"""Unit tests for wx.Panel.

Methods yet to test:
__init__, Create, SetFocusIgnoringChildren"""

import unittest
import wx

import testWindow

class PanelTest(testWindow.WindowTest):
    def setUp(self):
        self.frame = wx.Frame(parent=None, id=wx.ID_ANY)
        self.testControl = wx.Panel(parent=self.frame)
    

if __name__ == '__main__':
    unittest.main()