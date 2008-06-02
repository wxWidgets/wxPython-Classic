import wx
print wx.version()

class Frame(wx.Frame):
    def __init__(self, *args, **kw):
        wx.Frame.__init__(self, *args, **kw)
        mbar = wx.MenuBar()
        menu = wx.Menu()
        menu.Append(wx.ID_EXIT, "E&xit\tCtrl-Q")
        mbar.Append(menu, "&File")
        self.SetMenuBar(mbar)

        tbar = wx.ToolBar(self)
        tbar.SetToolBitmapSize((24,24))
        item = tbar.AddSimpleTool(-1,
                wx.ArtProvider.GetBitmap(wx.ART_NEW, wx.ART_TOOLBAR, (24,24)))
        tbar.Realize()
        self.SetToolBar(tbar)
        
        self.Bind(wx.EVT_MENU, self.OnExit, id=wx.ID_EXIT)
        self.Bind(wx.EVT_UPDATE_UI, self.OnUpdate, item)

        wx.UpdateUIEvent.SetUpdateInterval(1000)

    def OnExit(self, evt):
        self.Close()

    def OnUpdate(self, evt):
        print 'OnUpdate:', wx.DateTime.Now()
        evt.Enable(True)

app = wx.App(redirect=False)
frm = Frame(None, title='EVT_UPDATE_UI test')
frm.Show()
app.MainLoop()

