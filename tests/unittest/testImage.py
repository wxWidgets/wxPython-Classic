import unittest
import wx

"""
This file contains classes and methods for unit testing the API of 
wx.Image

Methods yet to test:


__del__
__nonzero__
AddHandler
Blur
BlurHorizontal
BlurVertical
CanRead
CanReadStream
ComputeHistogram
ConvertAlphaToMask
ConvertColourToAlpha
ConvertToBitmap
ConvertToGreyscale
ConvertToMono
ConvertToMonoBitmap
Copy
CountColours
Create
Destroy
FindFirstUnusedColour
GetAlphaBuffer
GetAlphaData
GetBlue
GetData
GetDataBuffer
GetGreen
GetHandlers
GetHeight
GetImageCount
GetImageExtWildcard
GetMaskBlue
GetMaskGreen
GetMaskRed
GetOption
GetOptionInt
GetOrFindMaskColour
GetRed
GetSize
GetSubImage
GetWidth
HasOption
HSVtoRGB
InsertHandler
IsTransparent
LoadFile
LoadMimeFile
LoadMimeStream
LoadStream
Mirror
Paste
RemoveHandler
Replace
ResampleBicubic
ResampleBox
Rescale
Resize
RGBtoHSV
Rotate
Rotate90
RotateHue
SaveFile
SaveMimeFile
Scale
SetAlpha
SetAlphaBuffer
SetAlphaData
SetData
SetDataBuffer
SetMaskColour
SetMaskFromImage
SetOption
SetOptionInt
SetRGB
SetRGBRect
ShrinkBy
Size
"""


class ImageTest(unittest.TestCase):
    def setUp(self):
        self.app = wx.PySimpleApp()
        self.testControl = wx.EmptyImage(1,1)
    
    def tearDown(self):
        self.testControl.Destroy()
        self.app.Destroy()
        
    def testAlpha(self):
        """InitAlpha, HasAlpha"""
        self.assert_(not self.testControl.HasAlpha())
        self.testControl.InitAlpha()
        self.assert_(self.testControl.HasAlpha())
        
    def testInit(self):
        """__init__"""
        self.testControl = wx.Image('')
        self.assert_(isinstance(self.testControl, wx.Image))
    
    def testIsOk(self):
        """IsOk, Ok"""
        self.assert_(self.testControl.IsOk())
        self.assert_(self.testControl.Ok())
        self.testControl = wx.Image('')
        self.assert_(not self.testControl.IsOk())
        self.assert_(not self.testControl.Ok())
    
    def testMask(self):
        """SetMask, HasMask"""
        self.testControl.SetMask()
        self.assert_(self.testControl.HasMask())
        self.testControl.SetMask(False)
        self.assert_(not self.testControl.HasMask())
        self.testControl.SetMask(True)
        self.assert_(self.testControl.HasMask())
        

if __name__ == '__main__':
    unittest.main()