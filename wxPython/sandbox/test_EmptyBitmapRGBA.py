import wx
print wx.version()

USE_CAIRO = False
if USE_CAIRO:
    import wx.lib.wxcairo
    import cairo

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
        if not USE_CAIRO:
            # This one works fine on Mac and Windows, but not wxGTK...
            bmp = wx.EmptyBitmapRGBA(DIM, DIM, red, green, blue, alpha)
            dc = wx.MemoryDC(bmp)
            gc = wx.GraphicsContext.Create(dc)            
            path = gc.CreatePath()
            path.MoveToPoint(POS,POS)
            path.AddLineToPoint(DIM-POS, DIM-POS)
            gc.SetPen(wx.Pen("red", 8))
            gc.StrokePath(path)
            
        else:
            # try out a couple possible workarounds
            sfc = cairo.ImageSurface(cairo.FORMAT_ARGB32, DIM, DIM)
            ctx = cairo.Context(sfc)
            if False:
                # use straight cairo
                ctx.set_source_rgba(red/255.0, green/255.0, blue/255.0, alpha/255.0)
                ctx.paint()
                ctx.set_line_width(8)
                ctx.set_line_cap(cairo.LINE_CAP_ROUND)
                ctx.set_source_rgb(1, 0, 0)
                ctx.move_to(POS, POS)
                ctx.line_to(DIM-POS, DIM-POS)
                ctx.stroke()
            else:
                # use our GC-like wrapper
                import wx.lib.graphics as g
                gc = g.GraphicsContext.CreateFromNative(ctx)
                gc.Clear(wx.Colour(red, green, blue, alpha))
                path = gc.CreatePath()
                path.MoveToPoint(POS,POS)
                path.AddLineToPoint(DIM-POS, DIM-POS)
                gc.SetPen(wx.Pen("red", 8))
                gc.StrokePath(path)
            bmp = wx.lib.wxcairo.BitmapFromImageSurface(sfc)

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
