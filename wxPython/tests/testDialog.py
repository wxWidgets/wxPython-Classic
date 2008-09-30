"""Unit tests for wx.Dialog.

Methods yet to test:
__init__, Create, CreateButtonSizer, CreateSeparatedButtonSizer, CreateStdDialogButtonSizer,
CreateTextSizer, EndModal, GetAffirmativeId, GetEscapeId,
GetReturnCode, IsModal, SetAffirmativeId, SetEscapeId, SetReturnCode, ShowModal"""

import unittest
import wx

import testTopLevelWindow

class DialogTest(testTopLevelWindow.TopLevelWindowBase):
    def setUp(self):
        self.frame = wx.Frame(parent=None, id=wx.ID_ANY)
        self.testControl = wx.Dialog(parent=self.frame)
    
    
if __name__ == '__main__':
    unittest.main()