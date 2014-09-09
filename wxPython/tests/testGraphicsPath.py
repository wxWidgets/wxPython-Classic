"""Unit tests for wx.GraphicsPath.

Methods yet to test:
__del__, AddArc, AddArcToPoint, AddCircle, AddCurveToPoint, AddEllipse,
AddLineToPoint, AddPath, AddQuadCurveToPoint, AddRectangle, AddRoundedRectangle,
CloseSubpath, Contains, GetBox, GetCurrentPoint, GetNativePath, MoveToPoint,
Transform, UnGetNativePath"""

import unittest
import wx

import testGraphicsObject

class GraphicsPathTest(testGraphicsObject.GraphicsObjectTest):
    def setUp(self):
        self.renderer = wx.GraphicsRenderer.GetDefaultRenderer()
        self.testControl = self.renderer.CreatePath()
        
    def testConstructorFails_wxGraphicsPath(self):
        """__init__"""
        self.assertRaises(AttributeError, wx.GraphicsPath)
    
    def testGetRenderer(self):
        """GetRenderer"""
        # Overrides test in testGraphicsObject.GraphicsObjectTest
        self.assertEquals(repr(self.renderer), repr(self.testControl.GetRenderer()))
            
            
if __name__ == '__main__':
    unittest.main()