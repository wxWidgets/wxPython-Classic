import unittest
import wx

import testControl
import testItemContainer

"""
This file contains classes and methods for unit testing the API of wx.ControlWithItems.
"""

class ControlWithItemsTest(unittest.TestCase):
    def setUp(self):
        self.app = wx.PySimpleApp()
    
    def tearDown(self):
        self.app.Destroy()
    
    def testConstructorFails(self):
        """__init__"""
        self.assertRaises(AttributeError, wx.ControlWithItems)

class ControlWithItemsBase(testControl.ControlTest, testItemContainer.ItemContainerBase):
    """Mixing wx.Control with wx.ItemContainer """
    pass


if __name__ == '__main__':
    unittest.main(defaultTest="ControlWithItemsTest")