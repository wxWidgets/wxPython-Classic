"""Unit tests for wx.GraphicsRenderer.

Methods yet to test:
__del__, CreateContextFromNativeContext, CreateContextFromNativeWindow,
CreateLinearGradientBrush, CreateMeasuringContext, CreateRadialGradientBrush"""

import unittest
import wx

import wxtest

class GraphicsRendererTest(unittest.TestCase):
    def setUp(self):
        self.frame = wx.Frame(None)
        if wxtest.PlatformIsGtk():
            self.frame.Show()
        self.testControl = wx.GraphicsRenderer.GetDefaultRenderer()
    
    def tearDown(self):
        # crashes if you try to destroy the wx.GraphicsRenderer
        self.frame.Destroy()

    def testConstructorFails_wxGraphicsRendererOnly(self):
        """__init__"""
        self.assertRaises(AttributeError, wx.GraphicsRenderer)
    
    def testCreateBrush(self):
        """CreateBrush"""
        brush = self.testControl.CreateBrush(wx.Brush(wx.Colour(0,0,0)))
        self.assert_(isinstance(brush, wx.GraphicsBrush))
        self.assertEquals(repr(brush.GetRenderer()), repr(self.testControl))
    
    def testCreateContext(self):
        """CreateContext"""
        context = self.testControl.CreateContext(self.frame)
        self.assert_(isinstance(context, wx.GraphicsContext))
        self.assertEquals(repr(context.GetRenderer()), repr(self.testControl))
    
    def testCreateContextFails(self):
        """CreateContext"""
        # CreateContext needs to take an argument
        self.assertRaises(NotImplementedError, self.testControl.CreateContext)
    
    def testCreateFont(self):
        """CreateFont"""
        font = self.testControl.CreateFont(
                wx.Font(8, wx.FONTFAMILY_ROMAN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))
        self.assert_(isinstance(font, wx.GraphicsFont))
        self.assertEquals(repr(font.GetRenderer()), repr(self.testControl))
    
    def testCreateMatrix(self):
        """CreateMatrix"""
        matrix = self.testControl.CreateMatrix()
        self.assert_(isinstance(matrix, wx.GraphicsMatrix))
        self.assertEquals(repr(matrix.GetRenderer()), repr(self.testControl))
    
    def testCreatePath(self):
        """CreatePath"""
        path = self.testControl.CreatePath()
        self.assert_(isinstance(path, wx.GraphicsPath))
        self.assertEquals(repr(path.GetRenderer()), repr(self.testControl))
    
    def testCreatePen(self):
        """CreatePen"""
        pen = self.testControl.CreatePen(wx.Pen(wx.Colour(0,0,0)))
        self.assert_(isinstance(pen, wx.GraphicsPen))
        self.assertEquals(repr(pen.GetRenderer()), repr(self.testControl))
    
    def testGetDefaultRenderer(self):
        """GetDefaultRenderer"""
        # TODO: are there other tests that can be run for this function?
        self.assert_(isinstance(self.testControl.GetDefaultRenderer(), wx.GraphicsRenderer))
