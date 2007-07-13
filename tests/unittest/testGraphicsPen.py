import unittest
import wx

import testGraphicsObject

"""
This file contains classes and methods for unit testing the API of
wx.GraphicsPen.

Methods yet to test:
__del__
"""

class GraphicsPenTest(testGraphicsObject.GraphicsObjectTest):
    def setUp(self):
        self.app = wx.PySimpleApp()
        self.renderer = wx.GraphicsRenderer.GetDefaultRenderer()
        self.pen = wx.Pen(wx.Colour(0,0,0))
        self.testControl = self.renderer.CreatePen(self.pen)
        
    def testConstructorPasses(self):
        """__init__"""
        self.assert_(isinstance(wx.GraphicsPen(),wx.GraphicsPen))
    
    def testGetRenderer(self):
        """GetRenderer
        Overrides test in testGraphicsObject.GraphicsObjectTest"""
        self.assertEquals(repr(self.renderer), repr(self.testControl.GetRenderer()))
        
        
def suite():
    suite = unittest.makeSuite(GraphicsPenTest)
    return suite
    
if __name__ == '__main__':
    unittest.main(defaultTest='suite')
