"""Unit tests for wx.Window.

WindowTest is meant to be the base class of all test cases for classes derived
from wx.Window.  For the tests to run properly, derived classes must make sure
to call the constructor's superclass if they override it.  Additionally, they must create a 
few class properties from within the setUp method, and may create a few more.

Required properties:
    frame - just a generic frame, to use as a parent for Windows that need one
        TODO: in the future, consider renaming 'frame' to 'parent'
    testControl - an instance of the particular class under test

Optional properties:
        TODO: decide what to do with these; clean them up or move them out
    children - a sequence of frames whose parent is the testControl
    children_ids - IDs corresponding to each child
    children_names - names corresponding to each child

To find out where a particular method is tested, search for the name of that
method.  Each test contains, as a docstring, the names of the methods tested
within them.  Additionally, below is a list of methods needing tests.

Methods yet to test:
__init__, AcceptsFocus, AcceptsFocusFromKeyboard, AddChild, AdjustForLayoutDirection,
AssociateHandle, CacheBestSize, CanSetTransparent, CaptureMouse, CenterOnParent, CentreOnParent, 
ClearBackground, ClientToScreen, ClientToScreenXY, Close, ConvertDialogPointToPixels, 
ConvertDialogSizeToPixels, ConvertPixelPointToDialog, ConvertPixelSizeToDialog, 
Create, DestroyChildren, DissociateHandle, DLG_PNT, DLG_SZE, DragAcceptFiles, 
FindFocus, Fit, FitInside, GetAutoLayout, GetBestSize, 
GetBestSizeTuple, GetBestVirtualSize, GetBorder, GetCapture, GetCaret, GetCharHeight, 
GetCharWidth, GetClientAreaOrigin,
GetConstraints, GetContainingSizer, GetCursor, 
GetDefaultAttributes, GetDropTarget, GetEffectiveMinSize, GetEventHandler, GetExtraStyle, 
GetFullTextExtent, GetHandle, GetHelpTextAtPoint, GetLayoutDirection,
GetScreenPosition, GetScreenPositionTuple, GetScreenRect, GetScrollPos, GetScrollRange, 
GetScrollThumb, GetTextExtent, GetThemeEnabled,
GetUpdateClientRect, GetUpdateRegion, GetValidator, GetWindowBorderSize, 
GetWindowStyle, GetWindowStyleFlag, GetWindowVariant,
HasCapture, HasFlag, HasMultiplePages, HasScrollbar, HasTransparentBackground, HitTest, 
HitTestXY, InheritAttributes, InheritsBackgroundColour, InitDialog, InvalidateBestSize, 
IsDoubleBuffered, IsExposed, IsExposedPoint, IsExposedRect, IsRetained, 
Layout, LineDown, LineUp, Lower, MakeModal, 
MoveAfterInTabOrder, MoveBeforeInTabOrder, Navigate, NewControlId, NextControlId, 
PageDown, PageUp, PopEventHandler, PopupMenu, PopupMenuXY, PostCreate, PrepareDC, PrevControlId, 
PushEventHandler, Raise, Refresh, RefreshRect, RegisterHotKey, ReleaseMouse, RemoveChild, 
RemoveEventHandler, ScreenToClient, ScreenToClientXY, ScrollLines, ScrollPages, 
ScrollWindow, SendSizeEvent, SetAutoLayout, SetCaret, 
SetConstraints, SetContainingSizer, SetCursor, SetDimensions, SetDoubleBuffered,
SetDropTarget, SetEventHandler, SetExtraStyle, SetFocus, SetFocusFromKbd, 
SetHelpTextForId, SetInitialSize, SetLayoutDirection, 
SetScrollbar, SetScrollPos, SetSizeHintsSz, SetSizerAndFit, SetThemeEnabled, 
SetTransparent, SetValidator, SetVirtualSizeHints, SetVirtualSizeHintsSz,
SetWindowStyle, SetWindowStyleFlag, SetWindowVariant,
ShouldInheritColours, ToggleWindowStyle, TransferDataFromWindow, TransferDataToWindow, 
UnregisterHotKey, Update, UpdateWindowUI, UseBgCol, Validate, WarpPointer"""

import unittest
import wx

import wxtest
import testColour
import testRect
import testFont
import testPoint
import testSize

class WindowTest(unittest.TestCase):
    def __init__(self, arg):
        # superclass setup
        super(WindowTest,self).__init__(arg)
        # WindowTest setup
        # make derived classes less annoying
        self.children = []
        self.children_ids = []
        self.children_names = []

    def setUp(self):
        self.frame = wx.Frame(parent=None, id=wx.ID_ANY)
        self.testControl = wx.Window(parent=self.frame, id=wx.ID_ANY)
        self.children_ids = (42, 43, 44)
        self.children_names = ('Child One', 'Child Two', 'Child Three')
        self.children = ( wx.Frame(self.testControl, id=id, name=name)
                            for id, name in zip(self.children_ids, self.children_names) )

    def tearDown(self):
        self.frame.Destroy()

    def testAcceleratorTable(self):
        """SetAcceleratorTable, GetAcceleratorTable"""
        aTable = wx.AcceleratorTable([(wx.ACCEL_ALT,  ord('X'), wx.ID_ANY),
                              (wx.ACCEL_CTRL, ord('H'), wx.ID_ANY),
                              (wx.ACCEL_CTRL, ord('F'), wx.ID_ANY),
                              (wx.ACCEL_NORMAL, wx.WXK_F3, wx.ID_ANY)
                              ])
        self.testControl.SetAcceleratorTable(aTable)
        self.assert_(aTable.IsSameAs(self.testControl.GetAcceleratorTable()))
    
    def testBackgroundColor(self):
        """SetBackgroundColour, GetBackgroundColour"""
        for test, actual in testColour.getColourEquivalentHexValues() + \
                            testColour.getColourEquivalentTuples():
            self.assert_(self.testControl.SetBackgroundColour(test))
                        # return True when background colour changed
            self.assertEquals(actual, self.testControl.GetBackgroundColour())
            self.assert_(not self.testControl.SetBackgroundColour(test))
    
    # because of the name failures on Ubuntu
    def testBackgroundColourNames_wxWindowOnly(self):
        """SetBackgroundColour, GetBackgroundColour"""
        for test, actual in testColour.getColourEquivalentNames():
            self.assert_(self.testControl.SetBackgroundColour(test))
                        # return True when background colour changed
            self.assertEquals(actual, self.testControl.GetBackgroundColour())
            self.assert_(not self.testControl.SetBackgroundColour(test))
            
    def testBackgroundStyle(self):
        """SetBackgroundStyle, GetBackgroundStyle"""
        possible_styles = ( wx.BG_STYLE_COLOUR, wx.BG_STYLE_CUSTOM, wx.BG_STYLE_SYSTEM,
                            wx.BG_STYLE_COLOUR | wx.BG_STYLE_CUSTOM,
                            wx.BG_STYLE_COLOUR | wx.BG_STYLE_SYSTEM,
                            wx.BG_STYLE_CUSTOM | wx.BG_STYLE_SYSTEM,
                            wx.BG_STYLE_COLOUR | wx.BG_STYLE_CUSTOM | wx.BG_STYLE_SYSTEM
                          )
        for style in possible_styles:
            self.testControl.SetBackgroundStyle(style)
            self.assertEquals(self.testControl.GetBackgroundStyle(), style)
    
    # TODO: refactor this method
    # not strictly a test, there's no way to verify!
    def testCenter(self):
        """Center, Centre"""
        self.assertEquals(self.testControl.Center, self.testControl.Centre)
        self.testControl.Center() # default: BOTH
        self.testControl.Center(wx.HORIZONTAL)
        self.testControl.Center(wx.BOTH)
        self.testControl.Center(wx.VERTICAL)
        # This test is finicky.
        # TODO: consult the list about what makes this fail
        '''
        if wxtest.PlatformIsWindows():
            self.assertRaises(wx.PyAssertionError, self.testControl.Center, wx.CENTER_ON_SCREEN)
        # This, however, functions properly (it has a parent)
        for child in self.children:
            child.Center(wx.CENTER_ON_SCREEN)
        '''

    def testClientRect(self):
        """SetClientRect, GetClientRect"""
        # Robin says:
        # "Both GetClientAreaOrigin and GetClientSize will call platform specific
        # methods located in the derived classes, so they can (and do) vary across
        # platforms and window types.  IMO because of this potential variability
        # the only valid test for GetClientRect is that it returns a rectangle
        # positioned at GetClientAreaOrigin and with a size of GetClientSize."
        for rect in testRect.getRectData(self.testControl):
            self.testControl.SetClientRect(rect)
            r = self.testControl.GetClientRect()
            self.assertEquals(r.GetTopLeft(), self.testControl.GetClientAreaOrigin())
            self.assertEquals(r.GetSize(), self.testControl.GetClientSize())
 
    
    # See note above for why these tests are disabled.
    '''
    def testClientSize(self):
        """SetClientSize, GetClientSize"""
        for x,y in testSize.getSizes(self.testControl, wxtest.CLIENT_SIZE):
            self.testControl.SetClientSize(wx.Size(x,y))
            self.assertEquals(wx.Size(x,y), self.testControl.GetClientSize())
    
    def testClientSizeWH(self):
        """SetClientSizeWH, GetClientSizeTuple"""
        for w,h in testSize.getSizes(self.testControl, wxtest.CLIENT_SIZE):
            self.testControl.SetClientSizeWH(w,h)
            self.assertEquals((w,h), self.testControl.GetClientSizeTuple())
    '''
    
    def testDefaultAttributes(self):
        """GetClassDefaultAttributes"""
        attrs = type(self.testControl).GetClassDefaultAttributes()
        self.assert_(isinstance(attrs, wx.VisualAttributes))
        self.assert_(attrs.colBg.IsOk())
        self.assert_(attrs.colFg.IsOk())
        self.assert_(attrs.font.IsOk())
    
    '''
    Fails half the time.
    TODO: fix!
    def testDestroy(self):
        """Destroy"""
        self.assert_(self.testControl.Destroy())
        flag = False
        try:
            # for some reason, an assertRaises statement here will also 
            # raise an wx.PyDeadObjectError
            self.testControl.Destroy()
        except wx.PyDeadObjectError:
            flag = True
        self.assert_(flag)
        # put back a dummy object so cleanup can happen
        self.testControl = wx.Window(self.frame)
    '''
    
    def testEnable(self):
        """Enable, IsEnabled"""
        self.testControl.Enable(True)
        self.assert_(self.testControl.IsEnabled())
        for child in self.children:
            self.assert_(child.IsEnabled())
        self.assert_(not self.testControl.Enable(True))
        self.assert_(self.testControl.Enable(False))
        self.assert_(not self.testControl.IsEnabled())
        for child in self.children:
            self.assert_(not child.IsEnabled())
        self.assert_(self.testControl.Enable())
        self.assert_(self.testControl.IsEnabled())
        for child in self.children:
            self.assert_(child.IsEnabled())
    
    def testDisable(self):
        """Disable, IsEnabled"""
        self.testControl.Enable()
        self.assert_(self.testControl.Disable())
        self.assert_(not self.testControl.IsEnabled())
        self.assert_(not self.testControl.Disable())
        
    def testFindWindow(self):
        """FindWindowById, FindWindowByName"""
        for child, id, name in zip(self.children, self.children_ids, self.children_names):
            self.assertEquals(child, self.testControl.FindWindowById(id))
            self.assertEquals(child, self.testControl.FindWindowByName(name))
            
    def testFont(self):
        """SetFont, GetFont"""
        for font in testFont.getFontData():
            self.testControl.SetFont(font)
            self.assertEquals(font, self.testControl.GetFont())
            
    def testForegroundColour(self):
        """SetForegroundColour, GetForegroundColour"""
        for test, actual in testColour.getColourEquivalentHexValues() + \
                            testColour.getColourEquivalentTuples():
            self.assert_(self.testControl.SetForegroundColour(test))
                            # return True when background colour changed
            self.assertEquals(actual, self.testControl.GetForegroundColour())
            self.assert_(not self.testControl.SetForegroundColour(test))
    
    # because of the name failures on Ubuntu
    def testForegroundColourNames_wxWindowOnly(self):
        """SetForegroundColour, GetForegroundColour"""
        for test, actual in testColour.getColourEquivalentNames():
            self.assert_(self.testControl.SetForegroundColour(test))
                            # return True when background colour changed
            self.assertEquals(actual, self.testControl.GetForegroundColour())
            self.assert_(not self.testControl.SetForegroundColour(test))
            
    def testFreezeThaw(self):
        """Freeze, Thaw, IsFrozen"""
        if wxtest.PlatformIsNotGtk():
            self.testControl.Freeze()
            self.assert_(self.testControl.IsFrozen())
            self.testControl.Thaw()
            self.assert_(not self.testControl.IsFrozen())
        else:
            # wx.Window.Freeze is not implemented on wxGTK
            self.testControl.Freeze()
            self.assert_(not self.testControl.IsFrozen())
    
    def testGetChildren(self):
        """GetChildren"""
        # segfaults on Ubuntu for unknown reason
        if wxtest.PlatformIsNotGtk():
            a = wx.Window(self.testControl)
            b = wx.Window(self.testControl)
            c = wx.Window(self.testControl)
            for child in (a,b,c):
                self.assert_(child in self.testControl.GetChildren())
    
    def testGrandParent(self):
        """GetGrandParent, Reparent"""
        self.assertEquals(None, self.testControl.GetGrandParent())
        grandparent = wx.Frame(self.frame)
        parent = wx.Frame(grandparent)
        self.testControl.Reparent(parent)
        self.assertEquals(grandparent, self.testControl.GetGrandParent())
    
    # NOTE: this is peculiar
    '''
    def testHelpText(self):
        """SetHelpText, GetHelpText"""
        txt = "Here is some help text!"
        self.testControl.SetHelpText(txt)
        self.assertEquals(txt, self.testControl.GetHelpText())
    '''
    
    def testId(self):
        """SetId, GetId"""
        for id in (42, 314, 2718):
            self.testControl.SetId(id)
            self.assertEquals(id, self.testControl.GetId())
    
    def testIsBeingDeleted(self):
        """IsBeingDeleted"""
        # TODO: find a way to test this when it will return True
        self.assert_(not self.testControl.IsBeingDeleted())
    
    def testLabel(self):
        """SetLabel, GetLabel"""
        one = "here is &one label"
        two = "and here there is another"
        self.testControl.SetLabel(one)
        self.assertEquals(one, self.testControl.GetLabel())
        self.testControl.SetLabel(two)
        self.assertEquals(two, self.testControl.GetLabel())
        self.assertNotEquals(one, self.testControl.GetLabel())
    
    def testMaxSize(self):
        """SetMaxSize, GetMaxSize"""
        for max_size in testSize.getSizes(self.testControl, wxtest.SIZE):
            self.testControl.SetMaxSize(max_size)
            self.assertEquals(max_size, self.testControl.GetMaxSize())
            
    def testMinSize(self):
        """SetMinSize, GetMinSize"""
        for min_size in testSize.getSizes(self.testControl, wxtest.SIZE):
            self.testControl.SetMinSize(min_size)
            self.assertEquals(min_size, self.testControl.GetMinSize())
    
    # TODO: revisit this test method
    def testMove(self):
        """Move, MoveXY, GetPositionTuple"""
        for point in testPoint.getValidPointData():
            self.testControl.Move(point)
            self.assertEquals(point.Get(), self.testControl.GetPositionTuple())
        # TODO: what is expected behavior? see 'testPosition' above.
        unchanged = self.testControl.GetPositionTuple()
        self.testControl.Move(wx.Point(-1,-1))
        self.assertEquals(unchanged,self.testControl.GetPositionTuple())
        for point in testPoint.getValidPointData():
            x,y = point.Get()
            self.testControl.MoveXY(x,y)
            self.assertEquals((x,y), self.testControl.GetPositionTuple())
    
    def testName(self):
        """SetName, GetName"""
        # TODO: try it with newlines and special characters
        name = "The Name of the Panel"
        self.testControl.SetName(name)
        self.assertEquals(name, self.testControl.GetName())
        
    # what is the difference between SetOwnBackgroundColour and SetBackgroundColour?
    # the docs don't say anything about SetOwnBackgroundColour
    def testOwnBackgroundColor(self):
        """SetOwnBackgroundColour, GetBackgroundColour"""
        for test, actual in testColour.getColourEquivalentHexValues() + \
                            testColour.getColourEquivalentTuples():
            self.testControl.SetOwnBackgroundColour(test)
            self.assertEquals(actual, self.testControl.GetBackgroundColour())
    
    # because of the name failures on Ubuntu
    def testOwnBackgroundColorNames_wxWindowOnly(self):
        """SetOwnBackgroundColour, GetBackgroundColour"""
        for test, actual in testColour.getColourEquivalentNames():
            self.testControl.SetOwnBackgroundColour(test)
            self.assertEquals(actual, self.testControl.GetBackgroundColour())
    
    def testOwnFont(self):
        """SetOwnFont"""
        for font in testFont.getFontData():
            self.testControl.SetOwnFont(font)
            self.assertEquals(font, self.testControl.GetFont())
            
    def testOwnForegroundColor(self):
        """SetOwnForegroundColour, GetForegroundColour"""
        for test, actual in testColour.getColourEquivalentHexValues() + \
                            testColour.getColourEquivalentTuples():
            self.testControl.SetOwnForegroundColour(test)
            self.assertEquals(actual, self.testControl.GetForegroundColour())
    
    # because of the name failures on Ubuntu
    def testOwnForegroundColorNames_wxWindowOnly(self):
        """SetOwnForegroundColour, GetForegroundColour"""
        for test, actual in testColour.getColourEquivalentNames():
            self.testControl.SetOwnForegroundColour(test)
            self.assertEquals(actual, self.testControl.GetForegroundColour())
    
    def testParent(self):
        """GetParent, Reparent"""
        parent = self.testControl.GetParent()
        self.assertEquals(parent, self.frame)
        self.assert_(not self.testControl.Reparent(parent))
        anotherFrame = wx.Frame(self.frame)
        if self.testControl.Reparent(anotherFrame):
            newParent = self.testControl.GetParent()
            self.assertEquals(newParent, anotherFrame)
        else:
            self.assert_(False)
    
    def testPosition(self):
        """SetPosition, GetPosition"""
        for point in testPoint.getValidPointData():
            self.testControl.SetPosition(point)
            self.assertEquals(point, self.testControl.GetPosition())
        # TODO:
        # setting point of (-1,-1) does not affect position
        # is this expected behavior??
        unchanged = self.testControl.GetPosition()
        self.testControl.SetPosition(wx.Point(-1,-1))
        self.assertEquals(unchanged, self.testControl.GetPosition())
    
    def testRect(self):
        """SetRect, GetRect"""
        for rect in testRect.getRectData(self.testControl):
            self.testControl.SetRect(rect)
            # if a control has a min/max size, do not assert if attempts to
            # size the control outside those bounds do not work.
            size = rect.GetSize()
            if size >= self.testControl.GetMinSize() and size <= self.testControl.GetMaxSize():
                self.assertEquals(rect, self.testControl.GetRect())
        
    def testShow(self):
        """Show, IsShown"""
        self.testControl.Show(True)
        self.assert_(self.testControl.IsShown())
        self.testControl.Show(False)
        self.assert_(not self.testControl.IsShown())
        self.testControl.Show()
        self.assert_(self.testControl.IsShown())
    
    def testHide(self):
        """Hide"""
        self.testControl.Hide()
        self.assert_(not self.testControl.IsShown())
        
    def testShownOnScreen(self):
        """IsShownOnScreen"""
        self.testControl.Show()
        self.assert_(not self.frame.IsShown())
        if not self.testControl.IsTopLevel():
            self.assert_(not self.testControl.IsShownOnScreen())
        
        self.frame.Show()
        self.assert_(self.testControl.IsShownOnScreen())
        self.frame.Hide()
        if not self.testControl.IsTopLevel():
            self.assert_(not self.testControl.IsShownOnScreen())

    def testSize(self):
        """SetSize, GetSize"""
        for w,h in testSize.getSizes(self.testControl, wxtest.SIZE):
            size = wx.Size(w,h)
            self.testControl.SetSize(size)
            # if a control has a min/max size, do not assert if attempts to
            # size the control outside those bounds do not work.
            if size >= self.testControl.GetMinSize() and size <= self.testControl.GetMaxSize():
                self.assertEquals(size, self.testControl.GetSize())
    
    def testSizeWH(self):
        """SetSizeWH, GetSizeTuple"""
        for w,h in testSize.getSizes(self.testControl, wxtest.SIZE):
            self.testControl.SetSizeWH(w,h)
            # if a control has a min/max size, do not assert if attempts to
            # size the control outside those bounds do not work.
            if (w,h) >= self.testControl.GetMinSize() and (w,h) <= self.testControl.GetMaxSize():
                self.assertEquals((w,h), self.testControl.GetSizeTuple())
            
    def testSizer(self):
        """SetSizer, GetSizer"""
        # TODO: test for other functionality provided in SetSizer
        sz = wx.BoxSizer()
        self.testControl.SetSizer(sz)
        self.assertEquals(sz, self.testControl.GetSizer())
    
    def testToolTip(self):
        """SetToolTip, GetToolTip"""
        # wx.ToolTips don't have an equality test, so do it manually
        tip = wx.ToolTip('Here is a tip!')
        self.testControl.SetToolTip(tip)
        tip2 = self.testControl.GetToolTip()
        self.assertEquals(self.testControl, tip2.GetWindow())
        self.assertEquals(tip.GetTip(), tip2.GetTip())
    
    def testToolTipString(self):
        """SetToolTipString"""
        for txt in ('one','two','three'):
            self.testControl.SetToolTipString(txt)
            self.assertEquals(txt, self.testControl.GetToolTip().GetTip())
    
    def testTopLevel(self):
        """IsTopLevel"""
        self.assert_(not self.testControl.IsTopLevel())
    
    def testTopLevelParent(self):
        """GetTopLevelParent"""
        parent = wx.Frame(None)
        one = wx.Window(parent)
        two = wx.Window(one)
        three = wx.Window(two)
        four = wx.Window(three)
        self.assertEquals(parent, four.GetTopLevelParent())

    def testVirtualSize(self):
        """SetVirtualSize, GetVirtualSize"""
        for x,y in testSize.getSizes(self.testControl, wxtest.VIRTUAL_SIZE):
            self.testControl.SetVirtualSize(wx.Size(x,y))
            self.assertEquals(wx.Size(x,y), self.testControl.GetVirtualSize())
    
    def testVirtualSizeWH(self):
        """SetVirtualSizeWH, GetVirtualSizeTuple"""
        for w,h in testSize.getSizes(self.testControl, wxtest.VIRTUAL_SIZE):
            self.testControl.SetVirtualSizeWH(w,h)
            self.assertEquals((w,h),self.testControl.GetVirtualSizeTuple())
    
    def testWindowChildren_wxWindowOnly(self):
        """GetParent"""
        # Tests to make sure the window's children register as such
        for child in self.children:
            self.assertEquals(self.testControl, child.GetParent())
            
    
