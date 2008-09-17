import sys, os
import wx
import wx.lib.wxcairo
import cairo
import math

print wx.version()
##import os; print "pid:", os.getpid(); raw_input("Press Enter...")

# Set this to control what kind of DC is used
TYPE = 1


class TestPanel(wx.Panel):
    def __init__(self, *args, **kw):
        wx.Panel.__init__(self, *args, **kw)

        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_LEFT_DCLICK, self.OnDClick)


    def OnDClick(self, evt):
        print 'wx.ClientDC'
        dc = wx.ClientDC(self)
        dc.SetBackground(wx.Brush('pink'))
        dc.Clear()
        self.Render(dc)
        
        
    def OnPaint(self, evt):
        if TYPE == 1:
            print 'wx.PaintDC'
            dc = wx.PaintDC(self)
            self.Render(dc)

        if TYPE == 2:
            print 'wx.BufferedPaintDC'
            dc = wx.BufferedPaintDC(self)
            dc.SetBackground(wx.Brush(self.GetBackgroundColour()))
            dc.Clear()
            self.Render(dc)

        def testWithBmp(depth):
            w, h = self.GetClientSize()
            bmp = wx.EmptyBitmap(w, h, depth)
            dc = wx.MemoryDC(bmp)
            dc.SetBackground(wx.Brush(self.GetBackgroundColour()))
            dc.Clear()
            self.Render(dc)
            del dc
            dc = wx.PaintDC(self)
            dc.DrawBitmap(bmp, 0,0, True)

        if TYPE == 3:
            print 'wx.MemoryDC with bitmap depth -1'
            testWithBmp(-1)
            
        if TYPE == 4:
            print 'wx.MemoryDC with bitmap depth 24'
            testWithBmp(24)

        if TYPE == 5:
            print 'wx.MemoryDC with bitmap depth 32'
            testWithBmp(32)

        if TYPE == 6:
            print 'wx.GCDC'
            dc = wx.GCDC(wx.PaintDC(self))
            self.Render(dc)

        
    def Render(self, dc):
        # Draw some stuff on the plain dc
        sz = self.GetSize()
        dc.SetPen(wx.Pen("navy", 1))
        x = y = 0
        while x < sz.width * 2 or y < sz.height * 2:
            x += 20
            y += 20
            dc.DrawLine(x, 0, 0, y)
        
        # now draw something with cairo
        ctx = wx.lib.wxcairo.ContextFromDC(dc)
        ctx.set_line_width(15)
        ctx.move_to(150, 50)
        ctx.line_to(250, 250)
        ctx.rel_line_to(-200, 0)
        ctx.close_path()
        ctx.stroke()

        # and something else...
        ctx.arc(200, 200, 80, 0, math.pi*2)
        ctx.set_source_rgba(0, 1, 1, 0.5)
        ctx.fill_preserve()
        ctx.set_source_rgb(1, 0.5, 0)
        ctx.stroke()

        # here's a gradient pattern
        ptn = cairo.RadialGradient(315, 70, 25,
                                   302, 70, 128)
        ptn.add_color_stop_rgba(0, 1,1,1,1)
        ptn.add_color_stop_rgba(1, 0,0,0,1)
        ctx.set_source(ptn)
        ctx.arc(328, 96, 75, 0, math.pi*2)
        ctx.fill()

        # Draw some text
        face = wx.lib.wxcairo.FontFaceFromFont(
            wx.FFont(10, wx.SWISS, wx.FONTFLAG_BOLD))
        ctx.set_font_face(face)
        ctx.set_font_size(60)
        ctx.move_to(360, 180)
        ctx.set_source_rgb(0, 0, 0)
        ctx.show_text("Hello")

        # Text as a path, with fill and stroke
        ctx.move_to(400, 220)
        ctx.text_path("World")
        ctx.set_source_rgb(0.39, 0.07, 0.78)
        ctx.fill_preserve()
        ctx.set_source_rgb(0,0,0)
        ctx.set_line_width(2)
        ctx.stroke()

        # Show iterating and modifying a (text) path
        ctx.new_path()
        ctx.move_to(0, 0)
        ctx.set_source_rgb(0.3, 0.3, 0.3)
        ctx.set_font_size(30)
        text = "This path was warped..."
        ctx.text_path(text)
        tw, th = ctx.text_extents(text)[2:4]
        self.warpPath(ctx, tw, th, 360,300)
        ctx.fill()

        # Test converting ImageSurface to wx.Bitmap  (32-bit RGBA)
        fname = os.path.join(os.path.dirname(sys.argv[0]), 'toucan.png')
        img = cairo.ImageSurface.create_from_png(fname)
        ctx.set_source_surface(img, 10, 230)
        ctx.paint()
        bmp = wx.lib.wxcairo.BitmapFromImageSurface(img)
        dc.DrawBitmap(bmp, 10, 340)

        # Now a 24-bit surface
        img = cairo.ImageSurface(cairo.FORMAT_RGB24, 80,80)
        ictx = cairo.Context(img)
        ictx.rectangle(0,0, 80,80)
        ictx.set_source_rgb(1,0,0)
        ictx.fill()
        ictx.arc(40,40, 35, 0, 2*math.pi)
        ictx.set_source_rgb(0,0,1)
        ictx.fill()
        ctx.set_source_surface(img, 200,230)
        ctx.paint()
        bmp = wx.lib.wxcairo.BitmapFromImageSurface(img)
        dc.DrawBitmap(bmp, 200, 340)

        # Test converting a bitmap to an ImageSurface
        bmp = wx.Bitmap(fname)
        img = wx.lib.wxcairo.ImageSurfaceFromBitmap(bmp)
        ctx.set_source_surface(img, 300, 230)
        ctx.paint()
        

        
    def warpPath(self, ctx, tw, th, dx, dy):
        def f(x, y):
            xn = x - tw/2
            yn = y+ xn ** 3 / ((tw/2)**3) * 70
            return xn+dx, yn+dy

        path = ctx.copy_path()
        ctx.new_path()
        for type, points in path:
            if type == cairo.PATH_MOVE_TO:
                x, y = f(*points)
                ctx.move_to(x, y)

            elif type == cairo.PATH_LINE_TO:
                x, y = f(*points)
                ctx.line_to(x, y)

            elif type == cairo.PATH_CURVE_TO:
                x1, y1, x2, y2, x3, y3 = points
                x1, y1 = f(x1, y1)
                x2, y2 = f(x2, y2)
                x3, y3 = f(x3, y3)
                ctx.curve_to(x1, y1, x2, y2, x3, y3)

            elif type == cairo.PATH_CLOSE_PATH:
                ctx.close_path()

                
try:
    TYPE = int(sys.argv[1])
except:
    pass
if TYPE < 1 or TYPE > 6:
    TYPE = 1


app = wx.App(redirect=False)
frm = wx.Frame(None, title="PyCairo on a wx.DC", size=(600,500))
pnl = TestPanel(frm)
frm.Show()
app.MainLoop()
