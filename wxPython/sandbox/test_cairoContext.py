import sys, os
import wx
import wx.lib.graphics as g

import math
import cairo


print wx.version()
##import os; print "pid:", os.getpid(); raw_input("Press Enter...")


class TestPanel(wx.Panel):
    def __init__(self, *args, **kw):
        wx.Panel.__init__(self, *args, **kw)

        self.Bind(wx.EVT_PAINT, self.OnPaint)

        
    def OnPaint(self, evt):
        dc = wx.PaintDC(self)
        self.Render(dc)


    def Render(self, dc):
        ctx = g.GraphicsContext.Create(dc)
        ctx.Clear("wheat")
        
        path = ctx.CreatePath()
        path.AddRectangle(0, 0, 100, 100)
        ctx.SetPen(g.GraphicsPen('black'))
        ctx.Translate(10,10)
        ctx.StrokePath(path)

        path.AddCircle(50, 50, 50)
        ctx.Translate(110, 0)
        ctx.SetPen(ctx.CreatePen(wx.Pen('blue', 3)))
        ctx.StrokePath(path)
        sqpath = path

        ctx.Translate(110, 0)
        pen = g.GraphicsPen('red', 3, wx.USER_DASH)
        pen.Dashes = [4, 6, 8, 6, 4]
        ctx.SetPen(pen)
        ctx.StrokeLine(0,0, 75,0)

        pen = g.GraphicsPen('purple', 3)
        ctx.SetPen(pen)
        ctx.StrokeLines( [ (0,10), (75,10), (75,30), (0,30) ] )
        
        pen = g.GraphicsPen('green', 3)
        ctx.SetPen(pen)
        ctx.StrokeLineSegments(
            [ ( 0, 50), ( 0, 60),   (0, 70),  (0, 80) ],
            [ (75, 50), (75, 60),  (75, 70), (75, 80) ]  )

        ctx.Translate(90, 0)
        path = ctx.CreatePath()
        path.AddEllipse(0,0, 100,48)
        path.AddRoundedRectangle(0,52,100,48, 5)
        ctx.SetPen(g.GraphicsPen('magenta', 3))
        ctx.StrokePath(path)

        ctx.Translate(110, 0)
        path = ctx.CreatePath()
        path.AddLineToPoint(100,100)
        path.AddLineToPoint(100,  0)
        path.AddLineToPoint(  0,100)
        path.AddLineToPoint(  0,  0)
        path.AddLineToPoint(100,100)
        ctx.SetPen(g.GraphicsPen('orchid', 3))
        ctx.StrokePath(path)


        ctx.SetTransform(ctx.CreateMatrix())
        ctx.Translate(10, 120)
        pattern = cairo.LinearGradient(0,0, 0,100)
        pattern.add_color_stop_rgb(0, 0,0,1)
        pattern.add_color_stop_rgba(1, 1,0,0, 0.1)
        pen = g.GraphicsPen.CreateFromPattern(pattern, 30)
        pen.Cap = wx.CAP_BUTT
        ctx.SetPen(pen)
        ctx.StrokeLine(0,0, 100, 100)

        ctx.Translate(110, 0)
        fname = os.path.join(os.path.dirname(sys.argv[0]), 'toucan.png')
        bmp = wx.Bitmap(fname)
        pen = g.GraphicsPen(width=40, style=wx.STIPPLE)
        pen.Stipple = bmp
        pen.Cap = wx.CAP_BUTT
        ctx.SetPen(pen)
        ctx.StrokeLine(0,0, 100, 100)

        ctx.Translate(120, 0)
        ctx.SetPen(g.GraphicsPen('black', 4))
        ctx.SetBrush(g.GraphicsBrush('orange'))
        ctx.FillPath(sqpath)
        
        ctx.Translate(120, 0)
        ctx.DrawPath(sqpath)

        ctx.SetTransform(ctx.CreateMatrix())
        ctx.Translate(10, 250)
        ctx.SetFont(wx.FFont(28, wx.SWISS, wx.FONTFLAG_BOLD), 'blue')
        ctx.DrawText("Hello", 0,0)
        ctx.DrawText("World", 0,35, g.GraphicsBrush('orchid'))

        ctx.Translate(125, 0)
        ctx.DrawRotatedText("wxPython", 0, 0, math.radians(-30))
        ctx.SetFont(wx.FFont(28, wx.ROMAN, wx.FONTFLAG_BOLD))
        ctx.DrawRotatedText("& Cairo", 0, 45, math.radians(-30), g.GraphicsBrush('orchid'))

        ctx.SetBrush(g.GraphicsBrush((0,128,0,128)))
        ctx.FillPath(g.GraphicsPath().AddCircle(0,0,4))
        ctx.FillPath(g.GraphicsPath().AddCircle(0,45,4))

        ctx.Translate(125, 0)
        font = ctx.CreateFont(wx.FFont(40, wx.SWISS, wx.FONTFLAG_BOLD))
        gbrush = ctx.CreateLinearGradientBrush(0,0, 100,0, "orchid", "navy")
        font.Brush = gbrush
        ctx.SetFont(font)
        ctx.DrawText("brush", 0,0)
        
        
                
app = wx.App(redirect=False)
frm = wx.Frame(None, title="Cairo GrpahicsContext", size=(600,500))
pnl = TestPanel(frm)
frm.Show()
app.MainLoop()
