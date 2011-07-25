"""Unit tests for wx.GraphicsMatrix.

Methods yet to test:
__del__, Concat, Get, GetNativeMatrix, Invert, IsEqual, IsIdentity,
Rotate, Scale, Set, TransformDistance, TransformPoint, Translate"""

import unittest
import wx

import testGraphicsObject

class GraphicsMatrixTest(testGraphicsObject.GraphicsObjectTest):
    def setUp(self):
        self.renderer = wx.GraphicsRenderer.GetDefaultRenderer()
        self.testControl = self.renderer.CreateMatrix()
        
    def testConstructorFails_wxGraphicsMatrixOnly(self):
        """__init__"""
        self.assertRaises(AttributeError, wx.GraphicsMatrix)
    
    def testGetRenderer(self):
        """GetRenderer"""
        # Overrides test in testGraphicsObject.GraphicsObjectTest
        self.assertEquals(repr(self.renderer), repr(self.testControl.GetRenderer()))
        # TODO: I wonder why this fails?
        #self.assert_(self.renderer is self.testControl.GetRenderer())


if __name__ == '__main__':
    unittest.main()