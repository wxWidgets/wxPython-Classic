"""Unit tests for wx.GraphicsContext.

These tests can pretty much be copied from testGraphicsRenderer:
CreateBrush
CreateFont
CreateMatrix
CreatePath
CreatePen

Methods yet to test:
__del__, Clip, ClipRegion, ConcatTransform, CreateFromNative, CreateFromNativeWindow,
CreateLinearGradientBrush, CreateMeasuringContext, CreateRadialGradientBrush,
DrawBitmap, DrawEllipse, DrawIcon, DrawLines, DrawPath, DrawRectangle,
DrawRotatedText, DrawRoundedRectangle, DrawText, FillPath, GetFullTextExtent,
GetLogicalFunction, GetNativeContext, GetPartialTextExtents, GetTextExtent,
GetTransform, PopState, PushState, ResetClip, Rotate, Scale, SetBrush,
SetFont, SetLogicalFunction, SetPen, SetTransform, ShouldOffset,
StrokeLine, StrokeLines, StrokePath, Translate

And finally, is this a typo or what?:
StrokeLineSegements
TODO: file a bug report"""

import unittest
import wx

import wxtest
import testGraphicsObject

class GraphicsContextTest(testGraphicsObject.GraphicsObjectTest):
    def setUp(self):
        self.frame = wx.Frame(None)
        if wxtest.PlatformIsGtk():
            self.frame.Show() # otherwise segfault
        self.renderer = wx.GraphicsRenderer.GetDefaultRenderer()
        self.testControl = self.renderer.CreateContext(self.frame)
    
    def tearDown(self):
        self.testControl.Destroy()
        self.frame.Destroy()
        
    def testConstructorFails_wxGraphicsContextOnly(self):
        """__init__"""
        self.assertRaises(AttributeError, wx.GraphicsContext)
    
    def testCreate(self):
        """Create"""
        context = wx.GraphicsContext.Create(self.frame)
        self.assert_(isinstance(context, wx.GraphicsContext))
    
    def testGetRenderer(self):
        """GetRenderer"""
        # Overrides test in testGraphicsObject.GraphicsObjectTest
        self.assertEquals(repr(self.renderer), repr(self.testControl.GetRenderer()))
            
            
