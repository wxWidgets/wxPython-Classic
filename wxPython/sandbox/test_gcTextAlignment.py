import wx
print wx.version()

SIZE=(800,600)

class Test(wx.Panel):

    def __init__(self, *args, **kwargs):

        wx.Panel.__init__(self, *args, **kwargs)
        self.Bind(wx.EVT_PAINT, self.OnPaint)


    def OnPaint(self, event):
        dc = wx.PaintDC(self)
        dc.SetBackground(wx.Brush('WHITE'))

        fontsize = 100

        dc.Clear()
        font = wx.Font(fontsize, wx.ROMAN, wx.NORMAL, wx.BOLD)
        dc.SetFont(font)
        dc.SetPen(wx.BLACK_PEN)

        dc.SetDeviceOrigin(100, 100)

        # start with a DeviceContext
        text = 'DDDDD'
        dc.DrawText(text, 0, 0)
        w, h = dc.GetTextExtent(text)

        # horizontal lines
        dc.DrawLine(0, 0, w, 0)
        dc.DrawLine(0, h/2., w, h/2.)
        dc.DrawLine(0, h, w, h)

        # vertical lines
        dc.DrawLine(0, 0, 0, h)
        dc.DrawLine(w/2., 0, w/2., h)
        dc.DrawLine(w, 0, w, h)


        # now use a GraphicsContext
        gc = wx.GraphicsContext.Create(dc)
        gc.SetFont(font)
        gc.SetPen(wx.BLACK_PEN)

        gc.Translate(0, 200)
        text = 'GGGGG'

        # first draw text with normal co-ordinates
        gc.DrawText(text, 0, 0)
        w, h = gc.GetTextExtent(text)

        # horizontal lines
        gc.StrokeLine(0, 0, w, 0)
        gc.StrokeLine(0, h/2., w, h/2.)
        gc.StrokeLine(0, h, w, h)

        # vertical lines
        gc.StrokeLine(0, 0, 0, h)
        gc.StrokeLine(w/2., 0, w/2., h)
        gc.StrokeLine(w, 0, w, h)



################################################################################
if __name__ == '__main__':
    app = wx.App(redirect=False)
    f = wx.Frame(parent=None, pos=(0, 0), size=SIZE)
    Test(f)
    f.Show()
    app.MainLoop()


# EOF

