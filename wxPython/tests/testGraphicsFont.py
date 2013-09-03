"""Unit tests for wx.GraphicsFont.

Methods yet to test:
__del__"""

import unittest
import wx

import testGraphicsObject

class GraphicsFontTest(testGraphicsObject.GraphicsObjectTest):
    def setUp(self):
        self.renderer = wx.GraphicsRenderer.GetDefaultRenderer()
        self.font = wx.Font(8, wx.FONTFAMILY_ROMAN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL)
        self.testControl = self.renderer.CreateFont(self.font)
    
    def testConstructor_wxGraphicsFontOnly(self):
        """__init__"""
        self.testControl = wx.GraphicsFont()
        self.assert_(isinstance(self.testControl, wx.GraphicsFont))
    
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