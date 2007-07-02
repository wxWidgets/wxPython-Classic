import unittest
import wx

import testChoice

"""
This file contains classes and methods for unit testing the API of 
wx.ComboBox.
        
Methods yet to test:

__init__, CanCopy, CanCut, CanPaste, CanRedo, CanUndo, Copy, Create,
Cut, GetCurrentSelection, GetInsertionPoint, GetLastPosition, GetMark,
GetValue, IsEditable, Paste, Redo, Remove, Replace, SelectAll, SetEditable,
SetInsertionPoint, SetInsertionPointEnd, SetMark, SetStringSelection,
SetValue, Undo
"""

class ComboBoxTest(testChoice.ChoiceTest):
    def setUp(self):
        self.app = wx.PySimpleApp()
        self.frame = wx.Frame(parent=None, id=wx.ID_ANY)
        self.testControl = wx.ComboBox(parent=self.frame)
        

def suite():
    suite = unittest.makeSuite(ComboBoxTest)
    return suite
    
if __name__ == '__main__':
    unittest.main(defaultTest='suite')
