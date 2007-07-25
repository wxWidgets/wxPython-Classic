import unittest
import wx

import testSize
import wxtest

"""
This file contains classes and methods for unit testing the API of wx.Rect
        
Methods yet to test:
__add__, __del__, __eq__, __getitem__, __iadd__, __len__, __ne__, __nonzero__,
__reduce__, __repr__, __setitem__, __str__, CenterIn, CentreIn, Contains, ContainsRect,
ContainsXY, Deflate, GetBottom, GetBottomLeft, GetBottomRight, GetHeight, GetLeft,
GetPosition, GetRight, GetSize, GetTop, GetTopLeft, GetTopRight, GetWidth, GetX, GetY,
Inflate, Inside, InsideRect, InsideXY, Intersect, Intersects, IsEmpty, Offset, OffsetXY,
Set, SetBottom, SetBottomLeft, SetBottomRight, SetHeight, SetLeft, SetPosition,
SetRight, SetSize, SetTop, SetTopLeft, SetTopRight, SetWidth, SetX, SetY, Union
"""

def getRectData(ctrl):
    sizes = testSize.getSizes(ctrl, wxtest.SIZE)
    # TODO: more variation in wx.Rects returned?
    return [ wx.Rect(10,10,w,h) for w,h in sizes ]

# TODO: find out if 32767 is some Windows limit, or a hard one.
#       Can we get rid of this magic number?
# NOTE: a wx.Rect can be created with values of greater than 32767,
#       but when returned from wx.Window, that's the max.

class RectTest(unittest.TestCase):
    def setUp(self):
        self.app = wx.PySimpleApp()
        
    def tearDown(self):
        self.app.Destroy()
    
    def testGet(self):
        """__init__, Get"""
        tup = range(0,100,10)
        for x,y,w,h in zip(tup,tup,tup,tup):
            rect = wx.Rect(x,y,w,h)
            self.assertEquals((x,y,w,h), rect.Get())
        rect = wx.Rect()
        self.assertEquals((0,0,0,0), rect.Get())
    

if __name__ == '__main__':
    unittest.main()