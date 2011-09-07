"""Unit tests for wx.BitmapButton.

Methods yet to test:
__init__, Create, GetBitmapDisabled, GetBitmapFocus, GetBitmapHover,
GetBitmapLabel, GetBitmapSelected, GetMarginX, GetMarginY,
SetBitmapDisabled, SetBitmapFocus, SetBitmapHover, SetBitmapLabel,
SetBitmapSelected, SetMargins"""

import unittest
import wx

import wxtest
import testButton

class BitmapButtonTest(testButton.ButtonTest):
    def setUp(self):
        self.frame = wx.Frame(parent=None, id=wx.ID_ANY)
        self.testControl = wx.BitmapButton(parent=self.frame, bitmap=wx.NullBitmap)
    
    # TODO: crashes interpreter on Windows for some reason
    def testAllControlsNeedParents(self):
        """__init__"""
        if wxtest.PlatformIsNotWindows():
            super(BitmapButtonTest,self).testAllControlsNeedParents()
        

if __name__ == '__main__':
    unittest.main()