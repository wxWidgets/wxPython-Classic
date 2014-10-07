import wx
print wx.version()

class MyApp(wx.App):
    def OnInit(self):
        f = wx.Frame(None, title="Hello World")
        self.tc = wx.TextCtrl(f, style=wx.TE_MULTILINE|wx.HSCROLL)
        f.Show()
        return True
    
    def MacOpenFiles(self, filenames):
        self.tc.AppendText("You requested to open files:\n")
        for name in filenames:
            self.tc.AppendText("    %r\n" % name)

    def MacReopenApp(self):
        self.tc.AppendText("You requested to reopen the application\n")

app = MyApp()
app.MainLoop()

