import unittest
import wx

import testWindow

"""
This file contains classes and methods for unit testing the API of wx.Panel.

Methods yet to test:
__init__, Create, SetFocusIgnoringChildren
"""

class PanelTest(testWindow.WindowTest):
    def setUp(self):
        self.app = wx.PySimpleApp()
        self.frame = wx.Frame(parent=None, id=wx.ID_ANY)
        self.testControl = wx.Panel(parent=self.frame)
    

def suite():
    suite = unittest.makeSuite(PanelTest)
    return suite
    
if __name__ == '__main__':
    unittest.main(defaultTest='suite')
