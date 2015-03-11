###############################################################################
# Name: PlateButtonDemo.py                                                    #
# Purpose: PlateButton Test and Demo File                                     #
# Author: Cody Precord <cprecord@editra.org>                                  #
# Copyright: (c) 2007 Cody Precord <staff@editra.org>                         #
# Licence: wxWindows Licence                                                  #
###############################################################################

"""
Test file for testing the PlateButton control

"""

__author__ = "Cody Precord <cprecord@editra.org>"
__svnid__ = "$Id$"
__revision__ = "$Revision$"

#-----------------------------------------------------------------------------#
# Imports
import os
import sys
import webbrowser
import wx
import wx.lib.scrolledpanel as scrolled

#sys.path.insert(0, os.path.abspath('../../src'))
import eclib

from IconFile import *

#-----------------------------------------------------------------------------#

class TestPanel(scrolled.ScrolledPanel):
    def __init__(self, parent, log):
        self.log = log
        scrolled.ScrolledPanel.__init__(self, parent, wx.ID_ANY, size=(500,500))

        # Layout
        self.__DoLayout()
        self.SetupScrolling()

        # Event Handlers
        self.Bind(wx.EVT_BUTTON, self.OnButton)
        self.Bind(wx.EVT_TOGGLEBUTTON, self.OnToggleButton)
        self.Bind(wx.EVT_MENU, self.OnMenu)

    def __DoLayout(self):
        """Layout the panel"""
        # Make three different panels of buttons with different backgrounds
        # to test transparency and appearance of buttons under different use
        # cases
        p1 = wx.Panel(self)
        p2 = GradientPanel(self)
        p3 = wx.Panel(self)
        p3.SetBackgroundColour(wx.BLUE)

        self.__LayoutPanel(p1, "Default Background:")
        self.__LayoutPanel(p2, "Gradient Background:", exstyle=True)
        self.__LayoutPanel(p3, "Solid Background:")

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.AddMany([(p1, 0, wx.EXPAND), (p2, 0, wx.EXPAND), 
                       (p3, 0, wx.EXPAND)])
        self.SetSizer(sizer)
        self.SetAutoLayout(True)

    def __LayoutPanel(self, panel, label, exstyle=False):
        """Puts a set of controls in the panel
        @param panel: panel to layout
        @param label: panels title
        @keyword exstyle: Set the PB_STYLE_NOBG or not

        """
        # Bitmaps (32x32) and (16x16)
        devil = Devil.GetBitmap() # 32x32
        monkey = Monkey.GetBitmap() # 32x32
        address = Address.GetBitmap() # 16x16
        folder = Home.GetBitmap()
        bookmark = Book.GetBitmap() # 16x16

        vsizer = wx.BoxSizer(wx.VERTICAL)
        hsizer1 = wx.BoxSizer(wx.HORIZONTAL)
        hsizer1.Add((15, 15))
        hsizer2 = wx.BoxSizer(wx.HORIZONTAL)
        hsizer2.Add((15, 15))
        hsizer3 = wx.BoxSizer(wx.HORIZONTAL)
        hsizer3.Add((15, 15))
        hsizer4 = wx.BoxSizer(wx.HORIZONTAL)
        hsizer4.Add((15, 15))

        # Button Styles
        default = eclib.PB_STYLE_DEFAULT
        toggle = default | eclib.PB_STYLE_TOGGLE
        square  = eclib.PB_STYLE_SQUARE
        sqgrad  = eclib.PB_STYLE_SQUARE | eclib.PB_STYLE_GRADIENT
        gradient = eclib.PB_STYLE_GRADIENT

        # Create a number of different PlateButtons
        # Each button is created in the below loop by using the data set in this
        # lists tuple
        #        (bmp,   label,                Style,   Variant, Menu, Color, Enable)
        btype = [(None,  "Normal PlateButton", default, None,    None, None,  True),
                 (devil, "Normal w/Bitmap",    default, None,    None, None,  True),
                 (devil, "Disabled",           default, None,    None, None,  False),
                 (None,  "Normal w/Menu",      default, None,    True, None,  True),
                 (folder, "Home Folder",       default, None,    True, None,  True),
                 # Row 2
                 (None,  "Square PlateButton", square,  None,    None, None,  True),
                 (address, "Square/Bitmap",     square,  None,    None, None,  True),
                 (monkey, "Square/Gradient",   sqgrad,  None,    None, None,   True),
                 (address, "Square/Small",       square,  wx.WINDOW_VARIANT_SMALL, True, None, True),
                 (address, "Small Bitmap",      default, wx.WINDOW_VARIANT_SMALL, None, wx.Colour(33, 33, 33), True),
                 # Row 3
                 (devil, "Custom Color",       default, None,    None, wx.RED, True),
                 (monkey, "Gradient Highlight", gradient, None,  None, None,   True),
                 (monkey, "Custom Gradient",   gradient, None,   None, wx.Colour(245, 55, 245), True),
                 (devil,  "",                  default, None,    None, None,   True),
                 (bookmark,  "",               default, None,    True, None,   True),
                 (monkey,  "",                 square,  None,    None, None,   True),
                 # Row 4 Toggle buttons
                 (None,  "Toggle PlateButton", toggle, None,    None, None,  True),
                 (devil, "Toggle w/Bitmap",    toggle, None,    None, None,  True),
                 (devil, "Toggle Disabled",    toggle, None,    None, None,  False),
                 (None,  "Toggle w/Menu",      toggle, None,    True, None,  True),
                 (folder, "Toggle Home Folder",       toggle, None,    True, None,  True),
                 ]

        # Make and layout three rows of buttons in the panel
        for btn in btype:
            if exstyle:
                # With this style flag set the button can appear transparent on
                # on top of a background that is not solid in color, such as the
                # gradient panel in this demo.
                #
                # Note: This flag only has affect on wxMSW and should only be
                #       set when the background is not a solid color. On wxMac
                #       it is a no-op as this type of transparency is achieved
                #       without any help needed. On wxGtk it doesn't hurt to
                #       set but also unfortunatly doesn't help at all.
                bstyle = btn[2] | eclib.PB_STYLE_NOBG
            else:
                bstyle = btn[2]

            if btype.index(btn) < 5:
                tsizer = hsizer1
            elif btype.index(btn) < 10:
                tsizer = hsizer2
            elif btype.index(btn) < 16:
                tsizer = hsizer3
            else:
                tsizer = hsizer4

            tbtn = eclib.PlateButton(panel, wx.ID_ANY, btn[1], btn[0], style=bstyle)

            # Set a custom window size variant?
            if btn[3] is not None:
                tbtn.SetWindowVariant(btn[3])

            # Make a menu for the button?
            if btn[4] is not None:
                menu = wx.Menu()
                if btn[0] is not None and btn[0] == folder:
                    for fname in os.listdir(wx.GetHomeDir()):
                        if not fname.startswith('.'):
                            menu.Append(wx.NewId(), fname)
                elif btn[0] is not None and btn[0] == bookmark:
                    for url in ['http://wxpython.org', 'http://slashdot.org',
                                'http://editra.org', 'http://xkcd.com']:
                        menu.Append(wx.NewId(), url, "Open %s in your browser" % url)
                else:
                    menu.Append(wx.NewId(), "Menu Item 1")
                    menu.Append(wx.NewId(), "Menu Item 2")
                    menu.Append(wx.NewId(), "Menu Item 3")
                tbtn.SetMenu(menu)

            # Set a custom colour?
            if btn[5] is not None:
                tbtn.SetPressColor(btn[5])

            # Enable/Disable button state
            tbtn.Enable(btn[6])

            tsizer.AddMany([(tbtn, 0, wx.ALIGN_CENTER), ((10, 10))])

        txt_sz = wx.BoxSizer(wx.HORIZONTAL)
        txt_sz.AddMany([((5, 5)), (wx.StaticText(panel, label=label), 0, wx.ALIGN_LEFT)])
        vsizer.AddMany([((10, 10)),
                        (txt_sz, 0, wx.ALIGN_LEFT),
                        ((10, 10)), (hsizer1, 0, wx.EXPAND), ((10, 10)), 
                        (hsizer2, 0, wx.EXPAND), ((10, 10)), 
                        (hsizer3, 0, wx.EXPAND), ((10, 10)),
                        (hsizer4, 0, wx.EXPAND), ((10, 10))])
        panel.SetSizer(vsizer)

    def OnButton(self, evt):
        self.log.write("BUTTON CLICKED: Id: %d, Label: %s" % \
                       (evt.GetId(), evt.GetEventObject().LabelText))

    def OnToggleButton(self, evt):
        self.log.write("Toggle TOGGLEBUTTON CLICKED: Id: %d, Label: %s Pressed: %s" % \
                       (evt.GetId(), evt.GetEventObject().LabelText,
                        str(evt.GetEventObject().IsPressed())))

    def OnChildFocus(self, evt):
        """Override ScrolledPanel.OnChildFocus to prevent erratic
        scrolling on wxMac.

        """
        if wx.Platform != '__WXMAC__':
            evt.Skip()

        child = evt.GetWindow()
        self.ScrollChildIntoView(child)

    def OnMenu(self, evt):
        """Events from button menus"""
        self.log.write("MENU SELECTED: %d" % evt.GetId())
        e_obj = evt.GetEventObject()
        mitem = e_obj.FindItemById(evt.GetId())
        if mitem != wx.NOT_FOUND:
            label = mitem.GetLabel()
            if label.startswith('http://'):
                webbrowser.open(label, True)

#-----------------------------------------------------------------------------#

class GradientPanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        self.Bind(wx.EVT_PAINT, self.OnPaint)

    def OnPaint(self, evt):
        dc = wx.PaintDC(self)
        gc = wx.GraphicsContext.Create(dc)
        col1 = wx.SystemSettings_GetColour(wx.SYS_COLOUR_3DSHADOW)
        col2 = eclib.AdjustColour(col1, -90)
        col1 = eclib.AdjustColour(col1, 90)
        rect = self.GetClientRect()
        grad = gc.CreateLinearGradientBrush(0, 1, 0, rect.height - 1, col2, col1)

        pen_col = tuple([min(190, x) for x in eclib.AdjustColour(col1, -60)])
        gc.SetPen(gc.CreatePen(wx.Pen(pen_col, 1)))
        gc.SetBrush(grad)
        gc.DrawRectangle(0, 1, rect.width - 0.5, rect.height - 0.5)

        evt.Skip()
#----------------------------------------------------------------------

def runTest(frame, nb, log):
    win = TestPanel(nb, log)
    return win

class TestLog:
    def __init__(self):
        pass

    def write(self, msg):
        print msg

#----------------------------------------------------------------------

overview = eclib.platebtn.__doc__
title = "PlateButton"

#-----------------------------------------------------------------------------#
if __name__ == '__main__':
    try:
        import run
    except ImportError:
        app = wx.PySimpleApp(False)
        frame = wx.Frame(None, title="PlateButton Test")
        sizer = wx.BoxSizer(wx.HORIZONTAL)
        sizer.Add(TestPanel(frame, TestLog()), 1, wx.EXPAND)
        frame.CreateStatusBar()
        frame.SetSizer(sizer)
        frame.SetInitialSize()
        frame.Show()
        app.MainLoop()
    else:
        run.main(['', os.path.basename(sys.argv[0])] + sys.argv[1:])
