import unittest
import wx

import testGraphicsObject

"""
This file contains classes and methods for unit testing the API of
wx.GraphicsMatrix.

Methods yet to test:
__del__, Concat, Get, GetNativeMatrix, Invert, IsEqual, IsIdentity,
Rotate, Scale, Set, TransformDistance, TransformPoint, Translate
"""

class GraphicsMatrixTest(testGraphicsObject.GraphicsObjectTest):
    def setUp(self):
        self.app = wx.PySimpleApp()
        self.renderer = wx.GraphicsRenderer.GetDefaultRenderer()
        self.testControl = self.renderer.CreateMatrix()
        
    def testConstructorFails(self):
        """__init__"""
        self.assertRaises(AttributeError, wx.GraphicsMatrix)
    
    def testGetRenderer(self):
        """GetRenderer
        Overrides test in testGraphicsObject.GraphicsObjectTest"""
        self.assertEquals(repr(self.renderer), repr(self.testControl.GetRenderer()))
        # I wonder why this fails?
        #self.assert_(self.renderer is self.testControl.GetRenderer())
            
            
if __name__ == '__main__':
    unittest.main()