import wx
print wx.version()


class TestPanel(wx.Panel):
    def __init__(self, *args, **kw):
        wx.Panel.__init__(self, *args, **kw)
        self.Bind(wx.EVT_PAINT, self.OnPaint)

    def OnPaint(self, evt):
        txt = 'This is a test...  MMMMM'
        dc = wx.PaintDC(self)
        dc.SetPen(wx.Pen('red', 1))
        dc.SetBrush(wx.TRANSPARENT_BRUSH)

        dc.SetFont(wx.FFont(12, wx.TELETYPE))
        w, h = dc.GetTextExtent(txt)
        print 'TELETYPE:', (w,h)
        dc.DrawText(txt, 25, 25)
        dc.DrawRectangle(25, 25, w, h)

        dc.SetFont(wx.FFont(12, wx.SWISS))
        w, h = dc.GetTextExtent(txt)
        print 'SWISS:   ', (w,h)
        dc.DrawText(txt, 25, 60)
        dc.DrawRectangle(25, 60, w, h)


app = wx.App(False)
frm = wx.Frame(None, title='GTE Test')
pnl = TestPanel(frm)
frm.Show()
app.MainLoop()

        
