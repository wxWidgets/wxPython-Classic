"""Unit tests for wx.ControlWithItems.

TODO: are there any other methods that need testing?"""

import unittest
import wx

import testControl
import testItemContainer

class ControlWithItemsTest(unittest.TestCase):
    def testConstructorFails(self):
        """__init__"""
        self.assertRaises(AttributeError, wx.ControlWithItems)

class ControlWithItemsBase(testControl.ControlTest, testItemContainer.ItemContainerBase):
    """Mixing wx.Control with wx.ItemContainer """
    pass
