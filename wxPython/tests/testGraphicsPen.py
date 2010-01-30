"""Unit tests for wx.GraphicsPen.

Methods yet to test:
__del__"""

import unittest
import wx

import testGraphicsObject

class GraphicsPenTest(testGraphicsObject.GraphicsObjectTest):
    def setUp(self):
        self.renderer = wx.GraphicsRenderer.GetDefaultRenderer()
        self.pen = wx.Pen(wx.Colour(0,0,0))
        self.testControl = self.renderer.CreatePen(self.pen)
        
    def testConstructorPasses_wxGraphicsPenOnly(self):
        """__init__"""
        self.assert_(isinstance(wx.GraphicsPen(),wx.GraphicsPen))
    
    def testGetRenderer(self):
        """GetRenderer"""
        # Overrides test in testGraphicsObject.GraphicsObjectTest
        self.assertEquals(repr(self.renderer), repr(self.testControl.GetRenderer()))
        
        
if __name__ == '__main__':
    unittest.main()