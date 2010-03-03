import wx

ID = 10001

class TestFrame(wx.Frame):
    def __init__(self, *args, **kw):
        wx.Frame.__init__(self, *args, **kw)

        p = wx.Panel(self)
        b = wx.Button(p, -1, "Test it...", (15,15))
        self.Bind(wx.EVT_BUTTON, self.onTestIt, b)
        self.Bind(wx.EVT_WINDOW_DESTROY, self.onDestroy, id=ID)

        
    def onTestIt(self, evt):
        print "Testing destroy event..."
        p = wx.Panel(self, ID)
        wx.CallLater(100, p.Destroy)


    def onDestroy(self, evt):
        print 'Got destroy event:'
        print '    Id:', evt.GetId()
        print '   Obj:', evt.GetEventObject()
        print '   Wnd:', evt.GetWindow()



app = wx.App(False)
frm = TestFrame(None, title="window destroy")
frm.Show()
app.MainLoop()
