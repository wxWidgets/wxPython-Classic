

import wx
print wx.version()

USE_CAIRO = True
if USE_CAIRO:
    # use wx.lib.graphics.GraphicsContext
    import wx.lib.graphics as g  
else:
    # use the wx.GraphicsContext
    g = wx  
    

#----------------------------------------------------------------------


class TestPanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent, -1, style=wx.FULL_REPAINT_ON_RESIZE)
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        

    def OnPaint(self, evt):
        dc = wx.PaintDC(self)
        width, height = dc.GetSize()
        gc = g.GraphicsContext.Create(dc)

        if not USE_CAIRO:
            pen = wx.Pen('red', 0)
        else:
            pen = g.GraphicsPen('red', 0.01)
            
        pen.Cap = wx.CAP_BUTT
        gc.SetPen(pen)
        
        # Change the scale such that the range of the visible space is
        # 0-2 in each direction
        gc.Scale(width/2, height/2)

        # Move the origin by (1,1) making (0,0) be in the middle of
        # the window
        gc.Translate(1.0, 1.0)

        # Draw some lines and a path
        gc.StrokeLine(-0.95, -0.95, 0.95, 0.95)
        gc.StrokeLine(-0.95, 0.95, 0.95, -0.95)
        path = gc.CreatePath()
        path.AddCircle(0, 0, 0.33)
        gc.StrokePath(path)

        

app = wx.App(False)
frm = wx.Frame(None, title="Testing GC Translate & Scale")
pnl = TestPanel(frm)
frm.Show()
app.MainLoop()
