import wx
print wx.version()

DIM = 100
POS = 20

class TestPanel(wx.Panel):
    def __init__(self, *args, **kw):
        wx.Panel.__init__(self, *args, **kw)

        self.Bind(wx.EVT_PAINT, self.OnPaint)

        self.MakeSourceBitmap()
        self.MakeCopyImage()
        

    def MakeSourceBitmap(self):
        bmp = wx.EmptyBitmap(DIM, DIM, 32)
        bmp.UseAlpha()
        
        dc = wx.MemoryDC(bmp)
        gc = wx.GraphicsContext.Create(dc)

        gc.Clear( wx.Brush( (0,0,255, 128)))
        
        path = gc.CreatePath()
        path.AddRectangle(10,10,DIM-20,DIM-20)
        gc.SetBrush(wx.Brush(wx.Colour(128,128,128,180)))
        gc.FillPath(path)

        path = gc.CreatePath()
        path.MoveToPoint(POS,POS)
        path.AddLineToPoint(DIM-POS, DIM-POS)
        gc.SetPen(wx.Pen("red", 8))
        gc.StrokePath(path)

        gc.Clear()
        
        self.srcBmp = bmp
        
        
    def MakeCopyImage(self):
        self.cpyImg = self.srcBmp.ConvertToImage()
        print 'HasAlpha:', self.cpyImg.HasAlpha()
        #self.cpyImg.SaveFile("c:/tmp/testimage.png", wx.BITMAP_TYPE_PNG)
        
        
    def OnPaint(self, evt):
        dc = wx.PaintDC(self)
        sz = self.GetSize()
        dc.SetPen(wx.Pen("navy", 1))
        x = y = 0
        while x < sz.width * 2 or y < sz.height * 2:
            x += 20
            y += 20
            dc.DrawLine(x, 0, 0, y)
            
        dc.DrawBitmap(self.srcBmp,  25, 25, True)
        
        cpy = wx.BitmapFromImage(self.cpyImg)
        dc.DrawBitmap(cpy, 175, 25, True)
        
        
app = wx.App(redirect=False)
frm = wx.Frame(None, title="ConvertToImage")
pnl = TestPanel(frm)
frm.Show()
app.MainLoop()
