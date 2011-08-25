import wx
print wx.version()

class MyDialog(wx.Dialog):
    def __init__(self, *args, **kw):
        wx.Dialog.__init__(self, *args, **kw)

        tc1 = wx.TextCtrl(self, size=(200,-1))
        tc2 = wx.TextCtrl(self, size=(200,-1))

        ok = wx.Button(self, wx.ID_OK)
        cancel = wx.Button(self, wx.ID_CANCEL)
        ok.SetDefault()

        vsizer = wx.BoxSizer(wx.VERTICAL)
        hsizer = wx.BoxSizer(wx.HORIZONTAL)

        hsizer.Add(ok)
        hsizer.Add(cancel, 0, wx.LEFT, 10)

        vsizer.Add(tc1, 0, wx.TOP|wx.BOTTOM, 8)
        vsizer.Add(tc2, 0, wx.TOP|wx.BOTTOM, 8)
        vsizer.Add((1,8))
        vsizer.Add(hsizer, 0, wx.EXPAND)

        self.Sizer = wx.BoxSizer()
        self.Sizer.Add(vsizer, 1, wx.EXPAND|wx.ALL, 10)


class App(wx.App):
    def OnInit(self):
        dlg = MyDialog(None, title='MyDialog')
        print dlg.ShowModal()
        dlg.Destroy()
        return True

app = App(False)
app.MainLoop()
