import wx
print wx.version()

import os; print "PID:", os.getpid()


class TestPanel(wx.Panel):
    """
    A panel with a bunch of text fields in static boxes
    """
    def __init__(self, *args, **kw):
        wx.Panel.__init__(self, *args, **kw)

        sbs1 = self.MakeGroup("One",   ['aaaaa', 'bbbbb', 'ccccc'])
        sbs2 = self.MakeGroup("Two",   ['ddddd', 'eeeee', 'fffff'])
        sbs3 = self.MakeGroup("Three", ['ggggg', 'hhhhh', 'iiiii'])

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(sbs1, 0, wx.ALL, 15)
        sizer.Add(sbs2, 0, wx.ALL, 15)
        sizer.Add(sbs3, 0, wx.ALL, 15)

        self.SetSizer(sizer)
        

    def MakeGroup(self, label, items):
        sb = wx.StaticBox(self, label=label)
        sbs = wx.StaticBoxSizer(sb, wx.VERTICAL)
        
        fgs = wx.FlexGridSizer(cols=2, hgap=8, vgap=8)
        sbs.Add(fgs, 0, wx.ALL, 8)
        for item in items:
            fgs.Add(wx.StaticText(self, -1, item))
            fgs.Add(wx.TextCtrl(self, -1, "", size=(150,-1)))

        return sbs


class TestPanel2(TestPanel):
    """
    This one tests tabbing between fields on sub-panels
    """
    def MakeGroup(self, label, items):
        p = wx.Panel(self)
        p.SetBackgroundColour('pink')
        bs = wx.BoxSizer(wx.VERTICAL)
        
        fgs = wx.FlexGridSizer(cols=2, hgap=8, vgap=8)
        bs.Add(fgs, 0, wx.ALL, 8)
        for item in items:
            fgs.Add(wx.StaticText(p, -1, item))
            fgs.Add(wx.TextCtrl(p, -1, "", size=(150,-1)))

        p.SetSizer(bs)
        return p
    

app = wx.App(redirect=False)
frm = wx.Frame(None, title="Navigation Tests")

pnl = TestPanel(frm)
#pnl = TestPanel2(frm)

pnl.Sizer.SetSizeHints(frm)
frm.Show()
app.MainLoop()
