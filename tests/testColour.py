"""Unit tests for wx.Colour.
        
Methods yet to test:
__del__, __eq__, __getitem__, __len__, __ne__, __nonzero__, __reduce__, 
__repr__, __str__, GetAsString, GetPixel"""

import unittest
import wx

import wxtest
            
def getColourEquivalents():
    # doesn't include wx.Colour instances, only equivalents
    return tuple(   getColourEquivalentNames() +
                    getColourEquivalentHexValues() +
                    getColourEquivalentTuples() )
    
def getColourEquivalentNames():
    return tuple((name, wx.TheColourDatabase.FindColour(name)) for name in getColourNames())

def getColourEquivalentHexValues():
    return tuple((hexify(col), col) for name,col in getColourEquivalentNames())
    
def getColourEquivalentTuples():
    return tuple((col.Get(), col) for name,col in getColourEquivalentNames())

def hexify(col):
    (r,g,b) = col.Get()
    rhex, ghex, bhex = hex(r)[2:], hex(g)[2:], hex(b)[2:]
    if len(rhex) == 1:
        rhex = '0' + rhex
    if len(ghex) == 1:
        ghex = '0' + ghex
    if len(bhex) == 1:
        bhex = '0' + bhex
    return '#' + rhex + ghex + bhex

def getColourNames():
    """Colour names from inspection of wx.TheColourDatabase.
    These appear to be identical on all platforms"""
    return ('BLACK','BLUE','SLATE BLUE','GREEN','SPRING GREEN','CYAN','NAVY',
            'STEEL BLUE','FOREST GREEN','SEA GREEN','DARK GREY','MIDNIGHT BLUE',
            'DARK GREEN','DARK SLATE GREY','MEDIUM BLUE','SKY BLUE','LIME GREEN',
            'MEDIUM AQUAMARINE','CORNFLOWER BLUE','MEDIUM SEA GREEN','INDIAN RED',
            'VIOLET','DARK OLIVE GREEN','DIM GREY','CADET BLUE','MEDIUM GREY',
            'DARK SLATE BLUE','MEDIUM FOREST GREEN','SALMON','DARK TURQUOISE',
            'AQUAMARINE','MEDIUM TURQUOISE','MEDIUM SLATE BLUE','MEDIUM SPRING GREEN',
            'GREY','FIREBRICK','MAROON','SIENNA','LIGHT STEEL BLUE','PALE GREEN',
            'MEDIUM ORCHID','GREEN YELLOW','DARK ORCHID','YELLOW GREEN','BLUE VIOLET',
            'KHAKI','BROWN','TURQUOISE','PURPLE','LIGHT BLUE','LIGHT GREY','ORANGE',
            'VIOLET RED','GOLD','THISTLE','WHEAT','MEDIUM VIOLET RED','ORCHID',
            'TAN','GOLDENROD','PLUM','MEDIUM GOLDENROD','RED','ORANGE RED',
            'LIGHT MAGENTA','CORAL','PINK','YELLOW','WHITE')

# -----------------------------------------------------------

class ColourTest(unittest.TestCase):
    
    def testSetFromName(self):
        """SetFromName"""
        for name,colour in getColourEquivalentNames():
            newcol = wx.Colour()
            newcol.SetFromName(name)
            self.assertEquals(colour, newcol)
    
    def testConstructor(self):
        """__init__"""
        self.assertRaises(ValueError, wx.Colour, -1)
        self.assertRaises(OverflowError, wx.Colour, 256)
        
    def testGetSetRGB(self):
        """SetRGB, GetRGB"""
        for tup,color in getColourEquivalentTuples():
            sludge = color.GetRGB()
            del color
            color = wx.Colour()
            color.SetRGB(sludge)
            self.assertEquals(sludge, color.GetRGB())
            
    def testMultipleAccessors(self):
        """Get, Set"""
        for i in range(256):
            color = wx.Colour()
            color.Set(i,i,i,i)
            self.assertEquals((i,i,i), color.Get())
            self.assertEquals(i, color.Alpha())
    
    def testOk(self):
        """IsOk, Ok"""
        c1 = wx.Colour(255,255,255,255)
        c2 = wx.Colour(0,0,0,0)
        c3 = wx.Colour()
        for color in (c1, c2, c3):
            self.assert_(color.IsOk())
            self.assert_(color.Ok())
    
    def testOkFalse(self):
        """IsOk, Ok"""
        # HACK: to generate an invalid wx.Colour instance
        # NOTE: cannot access colBg directly without crashing the interpreter
        attr = wx.VisualAttributes()
        self.assert_(not attr.colBg.Ok())
        self.assert_(not attr.colBg.IsOk())
    
    def testSingleAccessors(self):
        """Red, Green, Blue, Alpha"""
        for i in range(256):
            colour = wx.Colour(i,i,i,i)
            self.assertEquals(i, colour.Red())
            self.assertEquals(i, colour.Green())
            self.assertEquals(i, colour.Blue())
            self.assertEquals(i, colour.Alpha())

