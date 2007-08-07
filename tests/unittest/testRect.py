import unittest
import wx

import testSize
import wxtest

"""
This file contains classes and methods for unit testing the API of wx.Rect.

32767 (or 2**15-1) is the max number that should be used in wx.Rects.
Most platforms use a short int to store window sizes and positions.
        
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

# -----------------------------------------------------------

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