import wx
print wx.version()

class CPanel(wx.Panel):
    def __init__(self, parent, color, *args, **kw):
        wx.Panel.__init__(self, parent, *args, **kw)
        self.SetBackgroundColour(color)
        if 'wxMac' in wx.PlatformInfo:
            self.SetWindowVariant(wx.WINDOW_VARIANT_SMALL)
        self.SetMinSize(self.GetSize())
        txt = wx.StaticText(self, -1,
                            "%s: %s" % (self.Name, self.Size),
                            pos=(10,10))

        

class TestPanel(wx.Panel):
    def __init__(self, *args, **kw):
        wx.Panel.__init__(self, *args, **kw)

        self.MakeContent()

        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_ERASE_BACKGROUND, lambda e: None)


    def MakeContent(self):
        p1 = CPanel(self, 'pink',       size=(120,250), name="one")
        p2 = CPanel(self, 'light blue', size=(120,150), name="two")
        p3 = CPanel(self, 'sea green',  size=(120,75),  name="three")
        p4 = CPanel(self, 'blue',       size=(120,50),  name="four")
        p5 = CPanel(self, 'blue',       size=(120,50),  name="five")

        gbs = self.gbs = wx.GridBagSizer(10,10)
        gbs.Add(p1, pos=(0,0), span=(2,1))
        gbs.Add(p2, pos=(0,1))
        gbs.Add(p3, pos=(1,1))
        gbs.Add(p4, pos=(3,0))
        gbs.Add(p5, pos=(3,1))

        p6 = CPanel(self, 'yellow',     size=(280,50),  name="six")
        gbs.Add(p6, pos=(2,1), span=(1,2))

        box = wx.BoxSizer()
        box.Add(gbs, 1, wx.EXPAND|wx.ALL, 10)
        self.SetSizer(box)
        

    def OnPaint(self, evt):
        dc = wx.BufferedPaintDC(self)
        dc.SetBackground(wx.Brush(self.BackgroundColour))
        dc.Clear()
        dc.SetPen(wx.Pen('red'))

        x,y = self.gbs.Position
        w,h = self.Size
        
        dc.DrawLine(0, y, w, y)
        for rh in self.gbs.RowHeights:
            y += rh + self.gbs.VGap/2
            dc.DrawLine(0, y, w, y)
            y += self.gbs.VGap/2
        dc.DrawLine(x, 0, x, h)            
        for cw in self.gbs.ColWidths:
            x += cw + self.gbs.HGap/2
            dc.DrawLine(x, 0, x, h)
            x += self.gbs.HGap/2


if __name__ == '__main__':
    app = wx.App(False)
    frm = wx.Frame(None, title="GBS spanning test", size=(400, 500))
    pbl = TestPanel(frm, name="main")
    frm.Show()
    # import wx.lib.inspection
    # wx.lib.inspection.InspectionTool().Show()
    app.MainLoop()

