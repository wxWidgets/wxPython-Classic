"""Unit tests for wx.TopLevelWindow.

Methods yet to test for wx.TopLevelWindow:
__init__, CenterOnScreen, CentreOnScreen, EnableCloseButton, GetDefaultItem, GetIcon,
GetTmpDefaultItem, Iconize, IsActive, IsAlwaysMaximized, IsIconized,
MacGetMetalAppearance, MacSetMetalAppearance, RequestUserAttention, Restore, SetDefaultItem,
SetIcon, SetIcons, SetShape, SetTmpDefaultItem"""

import unittest
import wx

import testWindow

class TopLevelWindowTest(unittest.TestCase):
    def setUp(self):
        self.app = wx.PySimpleApp()
    
    def tearDown(self):
        self.app.Destroy()
    
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
        self.app = wx.PySimpleApp()
        self.frame = wx.Frame(parent=None, id=wx.ID_ANY)
        self.testControl = None
    
    def tearDown(self):
        self.frame.Hide()
        self.frame.Destroy()
        self.testControl.Hide()
        self.testControl.Destroy()
        self.app.Destroy()
    
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
        
    
if __name__ == '__main__':
    unittest.main(defaultTest='TopLevelWindowTest')