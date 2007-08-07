import unittest
import wx

import wxtest
import testButton

"""
This file contains classes and methods for unit testing the API of 
wx.BitmapButton

Methods yet to test:
__init__, Create, GetBitmapDisabled, GetBitmapFocus, GetBitmapHover,
GetBitmapLabel, GetBitmapSelected, GetMarginX, GetMarginY,
SetBitmapDisabled, SetBitmapFocus, SetBitmapHover, SetBitmapLabel,
SetBitmapSelected, SetMargins
"""


class BitmapButtonTest(testButton.ButtonTest):
    def setUp(self):
        self.app = wx.PySimpleApp()
        self.frame = wx.Frame(parent=None, id=wx.ID_ANY)
        self.testControl = wx.BitmapButton(parent=self.frame, bitmap=wx.NullBitmap)
    
    # crashes interpreter on Windows for some reason
    def testAllControlsNeedParents(self):
        """__init__"""
        if wxtest.PlatformIsNotWindows():
            super(BitmapButtonTest,self).testAllControlsNeedParents()
        

if __name__ == '__main__':
    unittest.main()