import wx
from wx.lib.mixins.inspection import InspectableApp
print wx.version()

class Panel(wx.Panel):
    def __init__(self, *args, **kw):
        wx.Panel.__init__(self, *args, **kw)        
        self.Bind(wx.EVT_PAINT, self.onPaint)
        
        self.Sizer = wx.BoxSizer()
        self.Sizer.Add(wx.StaticBitmap(self, -1, self.makeBitmap(0)), 0, wx.ALL, 5)
        self.Sizer.Add(wx.StaticBitmap(self, -1, self.makeBitmap(wx.CONTROL_CHECKED)), 0, wx.ALL, 5)
        
        
    def makeBitmap(self, flag):
        size = (16,16)
        bmp = wx.EmptyBitmap(*size)
        dc = wx.MemoryDC(bmp)
        dc.Clear()
        
        rect = wx.RectPS((0,0), size)
        wx.RendererNative.Get().DrawCheckBox(self, dc, rect, flag)

        return bmp

    
    def onPaint(self, evt):
        dc = wx.PaintDC(self)
        #dc = wx.BufferedPaintDC(self)
        
        bmp = self.makeBitmap(0)
        dc.DrawBitmap(bmp, 5,50)
        bmp = self.makeBitmap(wx.CONTROL_CHECKED)
        dc.DrawBitmap(bmp, 33,50)
        
    
app = InspectableApp(False)
frm = wx.Frame(None)
pnl = Panel(frm)
frm.Show()
app.MainLoop()
