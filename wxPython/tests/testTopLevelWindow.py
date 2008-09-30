"""Unit tests for wx.TopLevelWindow.

Methods yet to test for wx.TopLevelWindow:
__init__, CenterOnScreen, CentreOnScreen, EnableCloseButton, GetDefaultItem, GetIcon,
GetTmpDefaultItem, Iconize, IsActive, IsAlwaysMaximized, IsIconized,
MacGetMetalAppearance, MacSetMetalAppearance, RequestUserAttention, Restore, SetDefaultItem,
SetIcon, SetIcons, SetShape, SetTmpDefaultItem"""

import unittest
import wx

import testWindow
import testSize
import wxtest

class TopLevelWindowTest(unittest.TestCase):
    def testConstructorFails(self):
        """__init__"""
        self.assertRaises(AttributeError, wx.TopLevelWindow)

# -----------------------------------------------------------

class TopLevelWindowBase(testWindow.WindowTest):
    def __init__(self, arg):
        # superclass setup
        super(TopLevelWindowBase,self).__init__(arg)
        self.title = "Lorem Ipsum"
        
    def setUp(self):
        self.frame = wx.Frame(parent=None, id=wx.ID_ANY)
        self.testControl = None
    
    def tearDown(self):
        self.frame.Hide()
        self.frame.Destroy()
        self.testControl.Hide()
        self.testControl.Destroy()
    
    def testFullScreen(self):
        """ShowFullScreen, IsFullScreen"""
        self.testControl.ShowFullScreen(True)
        self.assert_(self.testControl.IsFullScreen())
        self.testControl.ShowFullScreen(False)
        self.assert_(not self.testControl.IsFullScreen())
    
    '''
    # TODO: determine expected behavior of ShowFullScreen's return value, and update test
    def testShowFullScreen(self):
        """ShowFullScreen"""
        self.assert_(self.testControl.ShowFullScreen(True))
        self.assert_(not self.testControl.ShowFullScreen(True))
        self.assert_(self.testControl.ShowFullScreen(False))
        self.assert_(not self.testControl.ShowFullScreen(False))
    '''
    
    def testMaximize(self):
        """Maximize, IsMaximized"""
        self.testControl.Maximize()
        self.assert_(self.testControl.IsMaximized())
        self.testControl.Maximize(False)
        self.assert_(not self.testControl.IsMaximized())
        self.testControl.Maximize(True)
        self.assert_(self.testControl.IsMaximized())
    
    # TODO: test title with newlines and special characters
    def testTitle(self):
        """SetTitle, GetTitle"""
        self.testControl.SetTitle(self.title)
        self.assertEquals(self.title, self.testControl.GetTitle())
    
    def testTitleConstructor(self):
        """__init__, GetTitle"""
        self.testControl = type(self.testControl)(self.frame, title=self.title)
        self.assertEquals(self.title, self.testControl.GetTitle())
        
    def testTopLevel(self):
        """IsTopLevel"""
        self.assert_(self.testControl.IsTopLevel())
        
    # Although SizeHints are a method of wx.Window, they are basically deprecated
    # for all but TopLevelWindows, so we should test them here. 
    
    def testSizeHints(self):
        """SetSizeHints, GetMinWidth, GetMinHeight, GetMaxWidth, GetMaxHeight"""
        data = testSize.getSizeData()
        for (minW,minH),(maxW,maxH) in zip(data,data):
            maxW += 1
            maxH += 1 # maxes greater than mins
            self.testControl.SetSizeHints(minW, minH, maxW, maxH)
            self.assertEquals(minW, self.testControl.GetMinWidth())
            self.assertEquals(minH, self.testControl.GetMinHeight())
            self.assertEquals(maxW, self.testControl.GetMaxWidth())
            self.assertEquals(maxH, self.testControl.GetMaxHeight())
            
    # TODO: make the whole thing more robust
    def testInvalidSizeHints(self):
        """SetSizeHints"""
        # max can't be less than min (except on Ubuntu?)
        if wxtest.PlatformIsNotGtk():
            self.assertRaises(wx.PyAssertionError, self.testControl.SetSizeHints, 100,100,10,10)
