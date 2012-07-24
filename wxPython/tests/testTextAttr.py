"""Unit tests for wx.TextAttr.
        
Methods yet to test:
Combine, GetAlignment, GetFlags, GetLeftIndent, GetLeftSubIndent, GetRightIndent,
GetTabs, HasAlignment, HasFlag, HasLeftIndent, HasRightIndent, HasTabs, Init,
Merge, SetAlignment, SetFlags, SetLeftIndent, SetRightIndent, SetTabs"""

import unittest
import wx

import testColour

class TextAttrTest(unittest.TestCase):
    def setUp(self):
        self.testControl = wx.TextAttr()
        self.colour = wx.Colour(128,128,128)
        self.font = wx.Font(8, wx.FONTFAMILY_ROMAN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD)
    
    def testBackgroundColour(self):
        """SetBackgroundColour, GetBackgroundColour, HasBackgroundColour"""
        self.assert_(not self.testControl.HasBackgroundColour())
        self.assertEquals(wx.NullColour, self.testControl.GetBackgroundColour())
        for test,colour in testColour.getColourEquivalents():
            self.testControl.SetBackgroundColour(test)
            self.assert_(self.testControl.HasBackgroundColour())
            self.assertEquals(colour, self.testControl.GetBackgroundColour())
    
    def testIsDefaultBackgroundColour(self):
        """IsDefault"""
        self.assert_(self.testControl.IsDefault())
        self.testControl.SetBackgroundColour(self.colour)
        self.assert_(not self.testControl.IsDefault())

    def testIsDefaultTextColour(self):
        """IsDefault"""
        self.assert_(self.testControl.IsDefault())
        self.testControl.SetTextColour(self.colour)
        self.assert_(not self.testControl.IsDefault())

    def testIsDefaultFont(self):
        """IsDefault"""
        self.assert_(self.testControl.IsDefault())
        self.testControl.SetFont(self.font)
        self.assert_(not self.testControl.IsDefault())
    
    def testConstructor(self):
        """__init__"""
        # a trivial test as yet
        # TODO: exercise constructor more fully
        a = wx.TextAttr()
    
    def testFont(self):
        """SetFont, GetFont, HasFont"""
        self.assert_(not self.testControl.HasFont())
        self.assertEquals(wx.NullFont, self.testControl.GetFont())
        self.testControl.SetFont(self.font)
        self.assert_(self.testControl.HasFont())
        self.assertEquals(self.font, self.testControl.GetFont())
    
    def testTextColour(self):
        """SetTextColour, GetTextColour, HasTextColour"""
        self.assert_(not self.testControl.HasTextColour())
        self.assertEquals(wx.NullColour, self.testControl.GetTextColour())
        for test,colour in testColour.getColourEquivalents():
            self.testControl.SetTextColour(test)
            self.assert_(self.testControl.HasTextColour())
            self.assertEquals(colour, self.testControl.GetTextColour())
