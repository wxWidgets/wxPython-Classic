"""Unit tests for wx.TextCtrl.

Methods yet to test:
__init__, CanCopy, CanCut, CanPaste, CanRedo, CanUndo, ChangeValue, Create, 
DiscardEdits, EmulateKeyPress, GetDefaultStyle,
GetLastPosition, GetLineLength, GetLineText, GetNumberOfLines, GetString,
GetStyle, HitTest, HitTestPos, IsEditable, IsModified, LoadFile, MacCheckSpelling,
MarkDirty, PositionToXY, Redo, SaveFile, SelectAll, SendTextUpdatedEvent,
SetDefaultStyle, SetEditable, SetMaxLength, SetModified, SetStyle, ShowPosition,
Undo, write, XYToPosition"""

import unittest
import wx

import testControl

class TextCtrlTest(testControl.ControlTest):
    def setUp(self):
        self.frame = wx.Frame(parent=None, id=wx.ID_ANY)
        self.empty_value = ""
        self.default_value = self.empty_value
        # value of GetValue() is only defined to maintain \n for multi-line controls
        # so don't test with \n for single-line controls.
        self.value = "Hello, World! Lorem Ipsum!"
        self.text = "The quick brown fox jumps over the lazy dog."
        self.testControl = wx.TextCtrl(parent=self.frame, value=self.default_value)
    
    # TODO: break up this method into smaller tests
    def testCopyCutPaste(self):
        """Copy, Cut, Paste"""
        txt1 = "Yet Another TextControl"
        txt2 = "Here is some more text!"
        txt3 = "And here is the third."
        otherControl = wx.TextCtrl(self.frame, id=wx.ID_ANY, value=txt1)
        # sanity checks
        self.assert_(self.testControl.IsEmpty())
        self.assertEquals(txt1, otherControl.GetValue())
        # copy/paste
        otherControl.SelectAll() # need to select in order to copy!
        otherControl.Copy()
        self.testControl.Paste()
        self.assertEquals(txt1, otherControl.GetValue())
        self.assertEquals(txt1, self.testControl.GetValue())
        # cut/paste
        otherControl.SetValue(txt2)
        otherControl.SelectAll()
        otherControl.Cut()
        self.testControl.Paste()
        self.assert_(otherControl.IsEmpty())
        self.assertEquals(txt1+txt2, self.testControl.GetValue())
        self.testControl.SelectAll()
        self.testControl.Paste()
        self.assertEquals(txt2, self.testControl.GetValue())
        # you can't copy what isn't selected...
        otherControl.SetValue(txt3)
        self.testControl.Clear()
        otherControl.Copy()
        self.testControl.Paste()
        self.assertNotEquals(txt3, self.testControl.GetValue())
        self.assertEquals(txt2, self.testControl.GetValue())
    
    def testIsEmpty(self):
        """IsEmpty"""
        self.assert_(self.testControl.IsEmpty())
        self.testControl.SetValue(self.value)
        self.assert_(not self.testControl.IsEmpty())
        self.testControl.SetValue(self.empty_value)
        self.assert_(self.testControl.IsEmpty())
        
    def testMultiLine(self):
        """IsMultiLine"""
        self.testControl = wx.TextCtrl(parent=self.frame, style=wx.TE_MULTILINE)
        self.assert_(self.testControl.IsMultiLine())
        self.assert_(not self.testControl.IsSingleLine())
        
    def testSingleLine(self):
        """IsSingleLine"""
        self.assert_(self.testControl.IsSingleLine())
        self.assert_(not self.testControl.IsMultiLine())
    
    # Text manipulation methods of wx.TextCtrl (Table 7.4 in "wxPython in Action")
    # AppendText, Clear, EmulateKeyPress, GetInsertionPoint, SetInsertionPoint,
    # SetInsertionPointEnd, GetRange, GetSelection, GetStringSelection, SetSelection,
    # GetValue, SetValue, Remove, Replace, WriteText
    
    def testAppendText(self):
        """AppendText"""
        txt1, txt2 = self.text[:20], self.text[20:]
        self.testControl.SetValue(txt1)
        self.testControl.AppendText(txt2)
        self.assertEquals(self.text, self.testControl.GetValue())
        self.assertEquals(len(self.text), self.testControl.GetInsertionPoint())
    
    def testClear(self):
        """Clear"""
        # TODO: ensure wx.wxEVT_COMMAND_TEXT_UPDATED event generated
        self.testControl.SetValue(self.text)
        self.assert_(not self.testControl.IsEmpty())
        self.testControl.Clear()
        self.assert_(self.testControl.IsEmpty())
    
    def testGetRange(self):
        """GetRange"""
        self.testControl.SetValue(self.text)
        for i,j in ((0,2),(1,9),(7,len(self.text))):
            self.assertEquals(self.text[i:j], self.testControl.GetRange(i,j))
        
    def testInsertionPoint(self):
        """SetInsertionPoint, GetInsertionPoint"""
        self.testControl.SetValue(self.text)
        # TODO: Is 1 the lowest possible value for GetInsertionPoint()?
        self.testControl.SetInsertionPoint(0)
        self.assertEquals(0, self.testControl.GetInsertionPoint())
        self.testControl.SetInsertionPoint(10)
        self.assertEquals(10, self.testControl.GetInsertionPoint())
        self.testControl.SetInsertionPoint(999)
        self.assertEquals(len(self.text), self.testControl.GetInsertionPoint())
    
    def testInsertionPointEnd(self):
        """SetInsertionPointEnd"""
        self.testControl.SetValue(self.text)
        self.testControl.SetInsertionPointEnd()
        self.assertEquals(len(self.text), self.testControl.GetInsertionPoint())
    
    def testRemove(self):
        """Remove"""
        for i,j in ((0,2),(2,10),(7,len(self.text))):
            self.testControl.SetValue(self.text)
            removed = self.text[:i] + self.text[j:]
            self.testControl.Remove(i,j)
            self.assertEquals(removed, self.testControl.GetValue())
    
    def testRemoveEmpty(self):
        """Remove, IsEmpty"""
        self.testControl.SetValue(self.text)
        self.testControl.Remove(0,len(self.text))
        self.assert_(self.testControl.IsEmpty())
    
    def testReplace(self):
        """Replace"""
        rep = "asdf jkl;"
        for i,j in ((0,2),(2,10),(7,len(self.text))):
            self.testControl.SetValue(self.text)
            replaced = self.text[:i] + rep + self.text[j:]
            self.testControl.Replace(i,j,rep)
            self.assertEquals(replaced, self.testControl.GetValue())
        
    def testSelection(self):
        """SetSelection, GetSelection, GetStringSelection"""
        self.testControl.SetValue(self.text)
        for i,j in ((0,2),(1,9),(7,len(self.text))):
            self.testControl.SetSelection(i,j)
            self.assertEquals((i,j), self.testControl.GetSelection())
            self.assertEquals(self.text[i:j], self.testControl.GetStringSelection())
    
    # TODO: test "normal" values, as well as newlines and special characters in value
    def testValue(self):
        """SetValue, GetValue"""
        self.assertEquals(self.default_value, self.testControl.GetValue())
        self.testControl.SetValue(self.value)
        self.assertEquals(self.value, self.testControl.GetValue())
        self.testControl.SetValue(self.default_value)
        self.assertEquals(self.default_value, self.testControl.GetValue())
        

if __name__ == '__main__':
    unittest.main()