import wx
import wx.lib.flatnotebook as fnb

# Test types:
#    1. No notebook, the two webkit ctrls are side-by-side in a sizer,
#       the button destroys the 2nd webkit ctrl
#    2. Use native notebook, button deletes 2nd page
#    3. Use FlatNotebook, button deletes 2nd page
TEST = 2

from wx.webkit import WebKitCtrl
#from webview import WebView as WebKitCtrl


#import os; print 'PID:', os.getpid(); raw_input("Press enter...")

class TestFrame(wx.Frame):
    def __init__(self, *args, **kw):
        wx.Frame.__init__(self, *args, **kw)

        if TEST == 1:
            wkparent = self
            lbl = "Destroy 2nd WKC"
        elif TEST == 2:
            self.nb = wx.Notebook(self)
            wkparent = self.nb
            lbl = "Delete 2nd Page"
        elif TEST == 3:
            self.nb = fnb.FlatNotebook(self)
            wkparent = self.nb
            lbl = "Delete 2nd Page"
       
        self.wk1 = WebKitCtrl(wkparent)
        self.wk2 = WebKitCtrl(wkparent)
        self.wk1.LoadURL("http://wxPython.org")
        self.wk2.LoadURL("http://wxWidgets.org")
        #self.wk1 = wx.Panel(self.nb); self.wk1.SetBackgroundColour('red')
        #self.wk2 = wx.Panel(self.nb); self.wk2.SetBackgroundColour('blue')

        if TEST > 1:
            self.nb.AddPage(self.wk1, "zero")
            self.nb.AddPage(self.wk2, "one")
        btn = wx.Button(self, -1, lbl)
        self.Bind(wx.EVT_BUTTON, self.OnButton, btn)

        self.Sizer = wx.BoxSizer(wx.VERTICAL)
        if TEST == 1:
            self.Sizer.Add(self.wk1, 1, wx.EXPAND)
            self.Sizer.Add(self.wk2, 1, wx.EXPAND)        
        else:
            self.Sizer.Add(self.nb, 1, wx.EXPAND)
        self.Sizer.Add(btn, 0, wx.ALL, 10)
        

    def OnButton(self, evt):
        if TEST == 1:
            if self.wk2:
                self.wk2.Destroy()
                print "Destroy called"
        else:
            self.nb.DeletePage(1)


app = wx.App(redirect=False)
frm = TestFrame(None, size=(600,500))
frm.Show()
#import wx.lib.inspection
#wx.lib.inspection.InspectionTool().Show()
app.MainLoop()
