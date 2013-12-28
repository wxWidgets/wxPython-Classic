import wx
print wx.version()

##import os; print "pid:", os.getpid(); raw_input("press enter...")

class Frame(wx.Frame):
    def __init__(self, *args, **kw):
        wx.Frame.__init__(self, *args, **kw)

        p = wx.Panel(self)
        p.SetWindowVariant(wx.WINDOW_VARIANT_MINI)

        wx.Button(p, label="H", pos=(25,25), style=wx.BU_EXACTFIT)
        wx.Button(p, label="this is longer than the default width",
                  pos=(25,50), style=wx.BU_EXACTFIT)
        

app = wx.App(redirect=False)
frm = Frame(None, title='ExactFit & wxWINDOW_VARIANT_MINI')
frm.Show()
app.MainLoop()

