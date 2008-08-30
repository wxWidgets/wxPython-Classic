"""Unit tests for wx.Bitmap.

Methods yet to test:
__del__, __nonzero__, ConvertToImage, CopyFromBuffer, CopyFromBufferRGBA,
CopyFromIcon, GetPalette, LoadFile, SaveFile, SetMaskColour"""

import unittest
import wx

import wxtest
import testSize

class BitmapTest(unittest.TestCase):
    def setUp(self):
        self.testControl = wx.EmptyBitmap(10,10)
    
    def tearDown(self):
        self.testControl.Destroy()
    
    def testDepth(self):
        """SetDepth, GetDepth"""
        for i in range(1,1000,20):
            self.testControl.SetDepth(i)
            self.assertEquals(i, self.testControl.GetDepth())
    
    def testEquals(self):
        """__eq__, __ne__"""
        ty = type(self.testControl)
        a = ty("")
        b = ty("")
        c = ty("")
        c.SetSize((1,1))
        self.assertEquals(a,b)
        self.assertNotEquals(a,c)
        self.assertNotEquals(b,c)
    
    def testHeight(self):
        """SetHeight, GetHeight"""
        for h in range(2**0, 2**15, 2**7):
            self.testControl.SetHeight(h)
            self.assertEquals(h, self.testControl.GetHeight())
    
    def testInit(self):
        """__init__"""
        self.testControl = wx.Bitmap("")
        self.assert_(isinstance(self.testControl, wx.Bitmap))
    
    def testIsOk(self):
        """IsOk, Ok"""
        ty = type(self.testControl)
        self.assert_(self.testControl.IsOk())
        self.assert_(self.testControl.Ok())
        self.testControl = ty("")
        self.assert_(not self.testControl.IsOk())
        self.assert_(not self.testControl.Ok())
    
    def testMask(self):
        """SetMask, GetMask"""
        m = wx.Mask(self.testControl)
        self.testControl.SetMask(m)
        self.assert_(m.IsSameAs(self.testControl.GetMask()))
    
    def testSize(self):
        """SetSize, GetSize"""
        for size in testSize.getSizes(self.testControl, wxtest.SIZE):
            self.testControl.SetSize(size)
            self.assertEquals(size, self.testControl.GetSize())
    
    def testSubBitmap(self):
        """GetSubBitmap"""
        # additional setup
        origmask = wx.Mask(self.testControl, wx.Colour(120,30,90))
        self.testControl.SetMask(origmask)
        origdepth = self.testControl.GetDepth()
        # make SubBitmap
        sub = self.testControl.GetSubBitmap(wx.Rect(1,1,1,1))
        self.assert_(isinstance(sub, wx.Bitmap))
        self.assertEquals(wx.Size(1,1), sub.GetSize())
        # TODO: ensure it has the right colors or something?
        # "This function preserves bit depth and mask information."
        self.assert_(origmask.IsSameAs(sub.GetMask()))
        self.assertEquals(origdepth, sub.GetDepth())
    
    
    # FIXME: This is the wrong test for this condition. In fact, this test
    # shows that SetDepth is doing the wrong thing by creating an invalid 
    # bitmap, instead of asserting or simply not setting the depth to an
    # invalid value. 
    '''
    def testSubBitmapInvalidDepth(self):
        """GetSubBitmap"""
        self.testControl.SetDepth(25) # invalid depth
        if wxtest.ASSERTIONS_ON:
            self.assertRaises(wx.PyAssertionError, self.testControl.GetSubBitmap,
                                wx.Rect(1,1,1,1))
    '''
    
    def testSubBitmapOutOfBounds(self):
        """GetSubBitmap"""
        if wxtest.ASSERTIONS_ON:
            self.assertRaises(wx.PyAssertionError, self.testControl.GetSubBitmap,
                                wx.Rect(10,10,1,1)) # wx.Rect is out of bounds
        else:
            b = self.testControl.GetSubBitmap(wx.Rect(10,10,1,1))
            self.assert_(isinstance(b, wx.Bitmap))
    
    def testWidth(self):
        """SetWidth, GetWidth"""
        for w in range(2**0, 2**15, 2**7):
            self.testControl.SetWidth(w)
            self.assertEquals(w, self.testControl.GetWidth())
        

