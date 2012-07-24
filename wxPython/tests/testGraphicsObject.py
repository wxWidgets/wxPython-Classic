"""Unit tests for wx.GraphicsObject.

Methods yet to test:
__del__"""

import unittest
import wx

class GraphicsObjectTest(unittest.TestCase):
    def setUp(self):
        self.testControl = wx.GraphicsObject()
    
    def tearDown(self):
        self.testControl.Destroy()
    
    def testConstructor_wxGraphicsObjectTest(self):
        """__init__"""
        self.testControl = wx.GraphicsObject()
        self.assert_(isinstance(self.testControl, wx.GraphicsObject))
    
    def testGetRenderer(self):
        """GetRenderer"""
        # TODO: is there any way to set the renderer?
        #       or to check anything else?
        self.assertEquals(None, self.testControl.GetRenderer())
    
    def testIsNullFalse_wxGraphicsObjectOnly(self):
        """IsNull"""
        for obj in (wx.NullGraphicsBrush,
                    wx.NullGraphicsFont,
                    wx.NullGraphicsMatrix,
                    wx.NullGraphicsPath,
                    wx.NullGraphicsPen):
            self.assert_(obj.IsNull())
            
    def testIsNullTrue(self):
        """IsNull"""
        self.assert_(not self.testControl.IsNull())
