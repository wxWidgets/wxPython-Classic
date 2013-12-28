import wx

class MyApp(wx.App):
    def OnInit(self):
        f = wx.Frame(None, title="Hello World")
        self.tc = wx.TextCtrl(f, style=wx.TE_MULTILINE|wx.HSCROLL)
        f.Show()
        return True
    
    def MacOpenFile(self, filename):
        # Code to load filename goes here.  We'll just print the names.
        self.tc.AppendText("You requested to open: \"%s\"\n" % filename)

app = MyApp()
app.MainLoop()

