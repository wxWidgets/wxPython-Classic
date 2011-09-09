import wx

class MyFrame(wx.Frame):
    def __init__(self, *args, **kw):
        wx.Frame.__init__(self, *args, **kw)
        p = wx.Panel(self)
        self.st = wx.StaticText(p, label="The HotKey is Ctrl-Shift-F12", pos=(15,30))
        font = self.st.GetFont()
        font.MakeBold().MakeLarger()
        self.st.SetFont(font)

        self.hkid = hkid = wx.NewId()
        self.Bind(wx.EVT_HOTKEY, self.OnHotKey, id=hkid)
        result = self.RegisterHotKey(hkid,
                                     wx.MOD_CONTROL|wx.MOD_SHIFT,
                                     wx.WXK_F12)
        if not result:
            self.st.SetLabel("RegisterHotKey failed!")

        p.Bind(wx.EVT_LEFT_UP, self.OnLeftUp)
        

    def OnHotKey(self, evt):
        self.st.SetLabel("You pressed the hotkey.")
        wx.FutureCall(1000, self.st.SetLabel, "")

    def OnLeftUp(self, evt):
        self.UnregisterHotKey(self.hkid)
        self.st.SetLabel("HotKey unregistered.")

        

app = wx.App()
frm = MyFrame(None, title="Test RegisterHotKey")
frm.Show()
app.MainLoop()
