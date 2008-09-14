import wx
print wx.version()

DIM = 100
POS = 20

class TestPanel(wx.Panel):
    def __init__(self, *args, **kw):
        wx.Panel.__init__(self, *args, **kw)

        self.Bind(wx.EVT_PAINT, self.OnPaint)

        self.bmps = []
        self.bmps.append( self.MakeBitmap(blue=128, alpha=128) )
        self.bmps.append( self.MakeBitmap() )
        self.bmps.append( self.MakeBitmap(blue=255, alpha=255) )


    def MakeBitmap(self, red=0, green=0, blue=0, alpha=0):
        bmp = wx.EmptyBitmapRGBA(DIM, DIM, red, green, blue, alpha)
        
        dc = wx.MemoryDC(bmp)
        gc = wx.GraphicsContext.Create(dc)

        path = gc.CreatePath()
        path.MoveToPoint(POS,POS)
        path.AddLineToPoint(DIM-POS, DIM-POS)
        gc.SetPen(wx.Pen("red", 8))
        gc.StrokePath(path)

        return bmp
    
        
    def OnPaint(self, evt):
        dc = wx.PaintDC(self)
        sz = self.GetSize()
        dc.SetPen(wx.Pen("navy", 1))
        x = y = 0
        while x < sz.width * 2 or y < sz.height * 2:
            x += 20
            y += 20
            dc.DrawLine(x, 0, 0, y)

        x, y = 25,25
        for bmp in self.bmps:
            dc.DrawBitmap(bmp, x, y, True)
            x += DIM + 25
        
        
        
app = wx.App(redirect=False)
frm = wx.Frame(None, title="EmptyBitmapRGBA")
pnl = TestPanel(frm)
frm.Show()
app.MainLoop()
