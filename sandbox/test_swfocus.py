import wx
print wx.version()

import os; print "PID:", os.getpid()



class TestPanel(wx.Panel):
    """
    For testing tabbing into a scrolled window
    """
    def __init__(self, *args, **kw):
        wx.Panel.__init__(self, *args, **kw)

        tc1 = wx.TextCtrl(self, -1, "one", size=(150,-1))
        
        sw = wx.ScrolledWindow(self, -1,   size=(150,150),
                               #style = wx.WANTS_CHARS|wx.BORDER
                               )
        sw.SetBackgroundColour("light blue")
        sw.SetVirtualSize((150,150))
        sw.SetScrollRate(5,5)
        
        tc2 = wx.TextCtrl(self, -1, "two", size=(150,-1))
        
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(tc1, 0, wx.ALL, 15)
        sizer.Add(sw, 0, wx.ALL, 15)
        sizer.Add(tc2, 0, wx.ALL, 15)

        self.SetSizer(sizer)

        sw.Bind(wx.EVT_SET_FOCUS, self.OnSetFocus)
        sw.Bind(wx.EVT_KILL_FOCUS, self.OnKillFocus)

    def OnSetFocus(self, evt):
        evt.Skip()
        print "OnSetFocus"
        
    def OnKillFocus(self, evt):
        evt.Skip()
        print "OnKillFocus"



app = wx.App(redirect=False)
frm = wx.Frame(None, title="Tab to ScrolledWindow")

pnl = TestPanel(frm)

pnl.Sizer.SetSizeHints(frm)
frm.Show()
app.MainLoop()
