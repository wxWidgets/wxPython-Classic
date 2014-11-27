"""Unit tests for wx.Size.

Methods yet to test:
__init__, __del__, __getitem__, __len__, __nonzero__,
__reduce__, __repr__, __setitem__, __str__, __sub__, DecBy, DecTo,
IncBy, IncTo, Scale, SetDefaults"""

import unittest
import wx

import wxtest
import math

def getSizes(ctrl, kind):
    # determine get/set methods
    set,get = None,None
    if kind == wxtest.SIZE:
        set,get = ctrl.SetSize, ctrl.GetSize
    elif kind == wxtest.VIRTUAL_SIZE:
        set,get = ctrl.SetVirtualSize, ctrl.GetVirtualSize
    elif kind == wxtest.CLIENT_SIZE:
        set,get = ctrl.SetClientSize, ctrl.GetClientSize
    else:
        raise TypeError("Incorrect type constant used")
    # get mins and maxes
    set((1,1))
    xmin,ymin = get()
    set((2**15-1,2**15-1))  # 16-bit signed int
                            # for more information, see issue #1756896.
                            # if the limit is exceeded, wx will sometimes return junk
                            # values rather than asserting the max possible value
    xmax,ymax = get()
    # print?
    #print "%s [x]: %s (min), %s (max)" % (str(type(ctrl)), str(xmin), str(xmax))
    #print "%s [y]: %s (min), %s (max)" % (str(type(ctrl)), str(ymin), str(ymax))
    # generate data sets
    xset = [xmin,xmax]
    yset = [ymin,ymax]
    xrange = xmax-xmin
    yrange = ymax-ymin
    xinc = int(math.floor(xrange/11))
    yinc = int(math.floor(yrange/11))
    for i in range(1,11):
        xset.append(xmin+xinc*i)
        yset.append(ymin+yinc*i)
    return zip(xset,yset)

def getSizeData():
    data = []
    for x in range(0,100,10):
        for y in range(0,100,10):
            data.append(wx.Size(x,y))
    return data

# -----------------------------------------------------------

NEG_TWO = wx.Size(-2,-2)
NEG_ONE = wx.Size(-1,-1)
ZERO    = wx.Size(0,0)
ONE     = wx.Size(1,1)
TWO     = wx.Size(2,2)

# -----------------------------------------------------------

class SizeTest(unittest.TestCase):
    def setUp(self):
        self.testControl = wx.Size()
    
    # NOTE:
    #   testEquals, testNotEquals, testAddition, testSubtraction
    #   were copied from testPoint class.  In the future, possibly
    #   refactor out code duplication.
    def testEquals(self):
        """__eq__"""
        self.assert_( ZERO == ZERO )
        self.assert_( ZERO == wx.Size(0,0) )
        self.assert_( ZERO == wx.Size() )
        self.assert_( NEG_ONE == NEG_ONE )
        self.assert_( NEG_ONE == wx.Size(-1,-1) )
        self.assert_( ONE == ONE )
        self.assert_( ONE == wx.Size(1,1) )
        
    def testNotEquals(self):
        """__ne__"""
        self.assert_( ZERO != ONE )
        self.assert_( ONE != NEG_ONE )
        self.assert_( TWO != NEG_TWO )
        self.assert_( NEG_TWO != ZERO )
    
    def testAddition(self):
        """__add__"""
        self.assertEquals( ONE+NEG_ONE, ZERO )
        self.assertEquals( TWO+NEG_TWO, ZERO )
        self.assertEquals( ONE+ONE, TWO )
        self.assertEquals( ZERO+ZERO, ZERO )
        self.assertEquals( NEG_ONE+NEG_ONE, NEG_TWO )
        self.assertEquals( ONE+ZERO, ONE )
        self.assertEquals( TWO+NEG_ONE, ONE )
    
    def testSubtraction(self):
        """__sub__"""
        self.assertEquals( ONE-ONE, ZERO )
        self.assertEquals( NEG_ONE-NEG_ONE, ZERO )
        self.assertEquals( ONE-NEG_ONE, TWO )
        self.assertEquals( NEG_ONE-ONE, NEG_TWO )
        self.assertEquals( ZERO-ONE, NEG_ONE )
        self.assertEquals( ZERO-NEG_ONE, ONE )
        self.assertEquals( NEG_ONE-ZERO, NEG_ONE )
        self.assertEquals( ONE-ZERO, ONE )
    
    def testFullySpecified(self):
        """IsFullySpecified"""
        self.assert_(self.testControl.IsFullySpecified())
        self.assert_(wx.Size(10,10).IsFullySpecified())
        self.assert_(wx.Size(-10,-10).IsFullySpecified())
        self.assert_(not wx.Size(-1,-1).IsFullySpecified())
    
    def testGetSet(self):
        """Set, Get"""
        for w,h in getSizeData():
            self.testControl.Set(w,h)
            self.assertEquals((w,h), self.testControl.Get())
    
    def testHeight(self):
        """SetHeight, GetHeight"""
        for w,h in getSizeData():
            self.testControl.SetHeight(h)
            self.assertEquals(h, self.testControl.GetHeight())
    
    def testWidth(self):
        """SetWidth, GetWidth"""
        for w,h in getSizeData():
            self.testControl.SetWidth(w)
            self.assertEquals(w, self.testControl.GetWidth())
            
            
