# Module:       TestScrolledPanel.py
#
# Function:     Show scrolling problem with last visible line
#
# Created:      07 Jun 2010     Forestfield Software Ltd
#
#-----------------------------------------------------------------------
import os, sys, time

import wx
from wx.lib import scrolledpanel

#====================
USE_ORIGINAL = True  # Set True to demonstrate the default behaviour 
#====================   of modified scrolledpanel remains unchanged

class MyApp(wx.App):
    def OnInit(self):
        frame = TestFrame((350, 254), "Test ScrolledPanel")
        frame.Show(True)
        self.SetTopWindow(frame)
        return True

#-----------------------------------------------------------------------

class TestFrame(wx.Frame):
    def __init__(self, size=wx.DefaultSize, title='', style=wx.DEFAULT_FRAME_STYLE):
        wx.Frame.__init__(self, parent=None, size=size, title=title, style=style)
        self.Centre()
        sizer = wx.BoxSizer(wx.VERTICAL)
        self.panel = TestPanel(self, -1, self.GetClientSizeTuple())
        sizer.Add(self.panel, 1, wx.EXPAND)
        self.SetSizer(sizer)
        self.SetAutoLayout(True)
        self.panel.Render()
        self.Bind(wx.EVT_CLOSE, self.OnCloseWindow)

    def OnCloseWindow(self, event):
        self.Destroy()


#----------------------------------------------------------------------

BOX_HEIGHT = 20
GAP_WIDTH = 12

class TestPanel(scrolledpanel.ScrolledPanel):
    """ Panel displays a list of words and allows user to click individual words
        (to add or subtract them from a search string)
    """
    def __init__(self, parent, id, size):
        scrolledpanel.ScrolledPanel.__init__(self, parent, id, size)
        self.parent = parent
        self.Bind(wx.EVT_IDLE, self.OnIdle)
        self.Bind(wx.EVT_SIZE, self.OnResize)
        self.resizing = False
        self.words = []
        for k in range(100):
            self.words.append('word%d' % k)

    def OnIdle(self, event):
        " Redraw panel on resize"
        if self.resizing:
            self.Render()
            self.resizing = False
        event.Skip()

    def OnResize(self, event):
        " Panel size change"
        self.resizing = True
        event.Skip()

    def Render(self):
        """ Dynamically create word-list display based on available space in panel
        """
        sz = self.GetSizer()
        if sz:                      # remove any previous words
            sz.Clear(True)
        self.SetBackgroundColour("white")
        pwidth, pheight = self.GetSizeTuple()

        vsizer = wx.BoxSizer(wx.VERTICAL)
        newrow = True
        width = 0
        for word in self.words:
            wwidth, wheight = self.GetTextExtent(word)
            winwidth = wwidth + GAP_WIDTH
            if width + winwidth > (pwidth - 18):        #allow for possible vscrollbar
                newrow = True
            if newrow:
                hsizer = wx.BoxSizer(wx.HORIZONTAL)
                vsizer.Add(hsizer, 0, 0)
                width = 0
                newrow = False
            ww = WordWindow(self, word=word, size=(winwidth, BOX_HEIGHT))
            hsizer.Add(ww, 0, 0)
            width += winwidth
        self.SetSizer(vsizer)
        self.SetAutoLayout(True)

        if not hasattr(self, 'scrollIntoView'):
            print "Using original wx.lib.scrolledpanel"
            self.SetupScrolling(scroll_x=False, scrollToTop=False)
        elif USE_ORIGINAL:
            print "Using modified wx.lib.scrolledpanel with original behaviour"
            self.SetupScrolling(scroll_x=False, scrollToTop=False)
        else:
            print "Using modified wx.lib.scrolledpanel"   
            self.SetupScrolling(scroll_x=False, scrollToTop=False, scrollIntoView=False)

        self.Refresh()

    def AddWord(self, word):
        """ When a word is clicked, this method is called by the corresponding
            WordWindow instance. It relays the word upward to its own parent
        """
        # self.parent.AddText(word)
        print "Clicked %s" % word

#----------------------------------------------------------------------------

class WordWindow(wx.Panel):
    def __init__(self, parent, ID=-1, word="", pos=wx.DefaultPosition, size=(100, 25)):
        wx.Panel.__init__(self, parent, ID, pos, size, 0, word)
        self.parent = parent
        self.word = word
        self.SetMinSize(size)
        self.whiteBrush = wx.Brush(wx.Colour(255, 255, 255))
        self.greenBrush = wx.Brush(wx.Colour(152, 251, 152))
        self.redBrush = wx.Brush(wx.Colour(238, 44, 44))
        self.greenPen = wx.Pen(wx.Colour(34, 139, 34), width=1)
        self.whitePen = wx.Pen(wx.Colour(255, 255, 255), width=1.5)
        self.clearPen = wx.Pen(wx.Colour(0, 0, 0), style=wx.TRANSPARENT)
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_ENTER_WINDOW, self.OnMouseEnter)
        self.Bind(wx.EVT_LEAVE_WINDOW, self.OnMouseLeave)
        self.Bind(wx.EVT_LEFT_UP, self.OnLeftUp)
        self.highlight = False

    def OnPaint(self, evt):
        winwid, winht = self.GetClientSize()
        dc = wx.PaintDC(self)
        dc.Clear()
        if self.highlight:
            dc.SetPen(self.greenPen)
            dc.SetBrush(self.greenBrush)
            dc.DrawRectangle(0, 0, winwid, winht)
            dc.SetBrush(self.redBrush)
            dc.SetPen(self.clearPen)
            dc.DrawRectangle(winwid-GAP_WIDTH+2, 2, GAP_WIDTH-4, winht-4)
            dc.SetPen(self.whitePen)
            dc.DrawLine(winwid-GAP_WIDTH+4, winht/2, winwid-4, winht/2)
        else:
            dc.SetPen(self.clearPen)
            dc.SetBrush(self.whiteBrush)
            dc.DrawRectangle(0, 0, winwid, winht)

        w,h = dc.GetTextExtent(self.word)
        dc.SetTextForeground("blue")
        dc.SetFont(self.GetFont())
        dc.DrawText(self.word, 2, (winht-h)/2)
                
    def OnMouseEnter(self, event):
        "Change to Green and Red background colours"
        self.highlight = True
        self.Refresh()

    def OnMouseLeave(self, event):
        "Restore original background colour"
        self.highlight = False
        self.Refresh()

    def OnLeftUp(self, event):
        "Return the word clicked"
        winwid, winht = self.GetClientSize()
        prefix = ''
        xpos = event.GetX()
        if xpos > winwid - GAP_WIDTH:       # clicked in red, exclude from next search
            prefix = ' -'
        self.parent.AddWord(prefix + self.word)

#-----------------------------------------------------------------------

if __name__ == '__main__':
    app = MyApp(redirect=False)
    app.MainLoop()



