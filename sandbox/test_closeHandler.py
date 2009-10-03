import wx
print wx.version()

class ParentFrame(wx.Frame):
    def __init__(self, *args, **kw):
        wx.Frame.__init__(self, *args, **kw)
        child = ChildFrame(self, title="ChildFrame")
        child.Show()
        

class ChildFrame(wx.Frame):
    def __init__(self, *args, **kw):
        wx.Frame.__init__(self, *args, **kw)
        self.Bind(wx.EVT_CLOSE, self.OnClose)

    def OnClose(self, evt):
        wx.MessageBox("EVT_CLOSE handler called")
        self.Destroy()
        

if __name__ == "__main__":
    app = wx.App()
    frm = ParentFrame(None, title="ParentFrame")
    frm.Show()
    app.MainLoop()

    
