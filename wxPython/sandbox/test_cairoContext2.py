import sys, os
import wx
import wx.lib.graphics

import colorsys
import math
import cairo

print wx.version()
##import os; print "pid:", os.getpid(); raw_input("Press Enter...")

BASE  = 80.0    # sizes used in shapes drawn below
BASE2 = BASE/2
BASE4 = BASE/4


class TestPanel(wx.Panel):
    def __init__(self, *args, **kw):
        wx.Panel.__init__(self, *args, **kw)

        self.Bind(wx.EVT_PAINT, self.OnPaint)

        
    def OnPaint(self, evt):
        dc = wx.PaintDC(self)
        self.Render(dc)


    def Render(self, dc):
        gc = wx.lib.graphics.GraphicsContext.Create(dc)

        font = wx.SystemSettings.GetFont(wx.SYS_DEFAULT_GUI_FONT)
        font.SetWeight(wx.BOLD)
        gc.SetFont(font)

        # make a path that contains a circle and some lines, centered at 0,0
        path = gc.CreatePath()
        path.AddCircle(0, 0, BASE2)
        path.MoveToPoint(0, -BASE2)
        path.AddLineToPoint(0, BASE2)
        path.MoveToPoint(-BASE2, 0)
        path.AddLineToPoint(BASE2, 0)
        path.CloseSubpath()
        path.AddRectangle(-BASE4, -BASE4/2, BASE2, BASE4)


        # Now use that path to demonstrate various capbilites of the grpahics context
        gc.PushState()             # save current translation/scale/other state 
        gc.Translate(60, 75)       # reposition the context origin

        gc.SetPen(wx.Pen("navy", 1))
        gc.SetBrush(wx.Brush("pink"))

        # show the difference between stroking, filling and drawing
        for label, PathFunc in [("StrokePath", gc.StrokePath),
                                ("FillPath",   gc.FillPath),
                                ("DrawPath",   gc.DrawPath)]:
            w, h = gc.GetTextExtent(label)
            
            gc.DrawText(label, -w/2, -BASE2-h-4)
            PathFunc(path)
            gc.Translate(2*BASE, 0)

        gc.PopState()              # restore saved state
        gc.PushState()             # save it again
        gc.Translate(60, 200)      # offset to the lower part of the window
        
        gc.DrawText("Scale", 0, -BASE2)
        gc.Translate(0, 20)

        # for testing clipping
        #gc.Clip(0, 0, 100, 100)
        #rgn = wx.RegionFromPoints([ (0,0), (75,0), (75,25,), (100, 25),
        #                            (100,100), (0,100), (0,0)  ])
        #gc.ClipRegion(rgn)
        #gc.ResetClip()
        
        gc.SetBrush(wx.Brush(wx.Colour(178,  34,  34, 128)))   # 128 == half transparent
        for cnt in range(8):
            gc.Scale(1.08, 1.08)    # increase scale by 8%
            gc.Translate(5,5)     
            gc.DrawPath(path)

        gc.PopState()              # restore saved state
        gc.PushState()             # save it again
        gc.Translate(400, 200)
        gc.DrawText("Rotate", 0, -BASE2)

        # Move the origin over to the next location
        gc.Translate(0, 75)

        # draw our path again, rotating it about the central point,
        # and changing colors as we go
        for angle in range(0, 360, 30):
            gc.PushState()         # save this new current state so we can 
                                   # pop back to it at the end of the loop
            r, g, b = [int(c * 255) for c in colorsys.hsv_to_rgb(float(angle)/360, 1, 1)]
            gc.SetBrush(wx.Brush(wx.Colour(r, g, b, 64)))
            gc.SetPen(wx.Pen(wx.Colour(r, g, b, 128)))
            
            # use translate to artfully reposition each drawn path
            gc.Translate(1.5 * BASE2 * math.cos(math.radians(angle)),
                         1.5 * BASE2 * math.sin(math.radians(angle)))

            # use Rotate to rotate the path
            gc.Rotate(math.radians(angle))

            # now draw it
            gc.DrawPath(path)
            gc.PopState()

        # Draw a bitmap with an alpha channel on top of the last group
        fname = os.path.join(os.path.dirname(sys.argv[0]), 'toucan.png')
        bmp = wx.Bitmap(fname)
        bsz = bmp.GetSize()
        gc.DrawBitmap(bmp,
                      -bsz.width/2.5, 
                      -bsz.height/2.5,
                      bsz.width, bsz.height)

        gc.PopState()
        
        
                
app = wx.App(redirect=False)
frm = wx.Frame(None, title="Cairo GrpahicsContext2", size=(600,500))
pnl = TestPanel(frm)
frm.Show()
app.MainLoop()
