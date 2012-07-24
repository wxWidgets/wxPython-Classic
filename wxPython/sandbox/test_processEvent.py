import wx
print wx.version()


# An example of intercepting ProcessEvent by pushing a new class
# derived from wx.PyEvtHandler onto a window.


evtNameMap = {}

def MakeEventNamesMap():
    for name in dir(wx):
        if name.startswith('EVT'):
            evt = getattr(wx, name)
            if isinstance(evt, wx.PyEventBinder):
                evtNameMap[evt.typeId] = name 


class MyEvtHandler(wx.PyEvtHandler):
    def ProcessEvent(self, evt):
        name = evt.__class__.__name__
        if name not in ['IdleEvent', 'UpdateUIEvent']:
            print "%s\t%s" % (name, evtNameMap.get(evt.GetEventType(), 'unknown'))
            
        return False # Returning false means the event was not fully
                     # handled and to keep looking for event handlers


class TestFrame(wx.Frame):
    def __init__(self, *args, **kw):
        wx.Frame.__init__(self, *args, **kw)

        MakeEventNamesMap()

        p = wx.Panel(self)
        t = wx.TextCtrl(p, value="TextCtrl", pos=(25,25))
        b = wx.Button(p, label="Button", pos=(25, 75))

        b.PushEventHandler(MyEvtHandler())
        t.PushEventHandler(MyEvtHandler())


app = wx.App(False)
frm = TestFrame(None, title="Override ProcessEvent")
frm.Show()
app.MainLoop()
