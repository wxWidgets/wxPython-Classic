import unittest
import wx

"""
This file contains classes and methods for unit testing the API of 
wx.Bitmap

Methods yet to test:


__del__
__ne__
__nonzero__
ConvertToImage
CopyFromBuffer
CopyFromBufferRGBA
CopyFromIcon
GetDepth
GetHeight
GetPalette
GetSize
GetSubBitmap
GetWidth
LoadFile
SaveFile
SetDepth
SetHeight
SetMaskColour
SetSize
SetWidth
"""


class BitmapTest(unittest.TestCase):
    def setUp(self):
        self.app = wx.PySimpleApp()
        self.testControl = wx.EmptyBitmap(1,1)
    
    def tearDown(self):
        self.testControl.Destroy()
        self.app.Destroy()
    
    def testEquals(self):
        """__eq__"""
        a = wx.Bitmap('')
        b = wx.Bitmap('')
        c = wx.Bitmap('')
        c.SetSize((1,1))
        self.assertEquals(a,b)
        self.assertNotEquals(a,c)
        self.assertNotEquals(b,c)
    
    def testInit(self):
        """__init__"""
        self.testControl = wx.Bitmap('')
        self.assert_(isinstance(self.testControl, wx.Bitmap))
    
    def testIsOk(self):
        """IsOk, Ok"""
        self.assert_(self.testControl.IsOk())
        self.assert_(self.testControl.Ok())
        self.testControl = wx.Bitmap('')
        self.assert_(not self.testControl.IsOk())
        self.assert_(not self.testControl.Ok())
    
    def testMask(self):
        """SetMask, GetMask"""
        m = wx.Mask(self.testControl)
        self.testControl.SetMask(m)
        self.assert_(m.IsSameAs(self.testControl.GetMask()))
        

if __name__ == '__main__':
    unittest.main()