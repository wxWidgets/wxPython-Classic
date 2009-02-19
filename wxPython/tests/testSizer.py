"""Unit tests for wx.Sizer.

Since wx.Sizer is an abstract base class, tests implemented for wx.Sizer will
instead be run on instances of derived classes.
        
Methods yet to test:
__init__, __del__, Add, AddF, AddItem, AddMany, AddSizer, AddSpacer, AddStretchSpacer,
AddWindow, CalcMin, Clear, DeleteWindows, Detach, Fit, FitInside, GetChildren,
GetContainingWindow, GetItem, GetMinSize, GetMinSizeTuple, GetPosition, GetPositionTuple,
GetSize, GetSizeTuple, Hide, Insert,InsertF, InsertItem, InsertSizer, InsertSpacer,
InsertStretchSpacer, InsertWindow, IsShown, Layout, Prepend, PrependF, PrependItem,
PrependSizer, PrependSpacer, PrependStretchSpacer, PrependWindow, RecalcSizes, Remove,
RemovePos, RemoveSizer, RemoveWindow, Replace, SetContainingWindow, SetDimension,
SetItemMinSize, SetMinSize, SetSizeHints, SetVirtualSizeHints, Show, ShowItems"""

import unittest
import wx

class SizerTest(unittest.TestCase):
    def testConstructorFails(self):
        """__init__"""
        self.assertRaises(AttributeError, wx.Sizer)
    
# -----------------------------------------------------------

class SizerBase(unittest.TestCase):
    # to be overridden in derived classes
    def setUp(self):
        self.frame = wx.Frame(parent=None, id=wx.ID_ANY)
        self.testControl = None
    
    def tearDown(self):
        self.frame.Destroy()


if __name__ == '__main__':
    unittest.main(defaultTest="SizerTest")