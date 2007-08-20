"""Unit tests for wx.GraphicsFont.

Methods yet to test:
__del__"""

import unittest
import wx

import testGraphicsObject

class GraphicsFontTest(testGraphicsObject.GraphicsObjectTest):
    def setUp(self):
        self.app = wx.PySimpleApp()
        self.renderer = wx.GraphicsRenderer.GetDefaultRenderer()
        self.testControl = self.renderer.CreateFont(
                wx.Font(8, wx.FONTFAMILY_ROMAN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))
    
    def testConstructor(self):
        """__init__"""
        font = wx.GraphicsFont()
        self.assert_(isinstance(font, wx.GraphicsFont))
    
    def testGetRenderer(self):
        """GetRenderer"""
        # Overrides test in testGraphicsObject.GraphicsObjectTest
        self.assertEquals(repr(self.renderer), repr(self.testControl.GetRenderer()))
    
    def testIsNullTrue(self):
        """IsNull"""
        # Overrides test in testGraphicsObject.GraphicsObjectTest
        self.testControl = wx.GraphicsFont()
        self.assert_(self.testControl.IsNull())
            
            
if __name__ == '__main__':
    unittest.main()