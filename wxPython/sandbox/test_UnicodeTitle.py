import wx
print wx.version()

import os; print "pid:", os.getpid(); ##raw_input("press enter...")


class TestFrame(wx.Frame):
    def __init__(self, *args, **kw):
        wx.Frame.__init__(self, *args, **kw)
        p = wx.Panel(self)
        b = wx.Button(p, -1, "Set Title", (20,20))
        b.Bind(wx.EVT_BUTTON, self.OnButton)

    def OnButton(self, evt):
        s = '\xd0\x9f\xd0\xb8\xd1\x82\xd0\xbe\xd0\xbd - ' \
            '\xd0\xbb\xd1\x83\xd1\x87\xd1\x88\xd0\xb8\xd0\xb9 ' \
            '\xd1\x8f\xd0\xb7\xd1\x8b\xd0\xba \xd0\xbf\xd1\x80\xd0\xbe\xd0\xb3\xd1\x80\xd0\xb0\xd0\xbc\xd0\xbc\xd0\xb8\xd1\x80\xd0\xbe\xd0\xb2\xd0\xb0\xd0\xbd\xd0\xb8\xd1\x8f!'
        u = s.decode('utf-8')
        self.SetTitle(u)

app = wx.App(False)
frm = TestFrame(None)
frm.Show()
app.MainLoop()
