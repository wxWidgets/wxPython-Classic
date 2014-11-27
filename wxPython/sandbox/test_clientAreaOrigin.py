
import wx

class BorderPanel(wx.PyPanel):
   def __init__(self, *args, **kwargs):
       wx.PyPanel.__init__(self, *args, **kwargs)
       self.border = 20

   def DoGetClientSize(self):
       print "DoGetClientSize"
       border2 = self.border * 2
       width, height = self.GetSize()
       width = width - border2 if width > border2 else 0
       height = height - border2 if height > border2 else 0
       return width, height

   def GetClientAreaOrigin(self):
       print "GetClientAreaOrigin"
       return self.border, self.border



class MyPanel(BorderPanel):
   def __init__(self, *args, **kwargs):
       BorderPanel.__init__(self, *args, **kwargs)
       childpanel = wx.Panel(self)
       childpanel.SetBackgroundColour(wx.Colour(0,0,255))
       sizer = wx.BoxSizer()
       sizer.Add(childpanel, 1, wx.EXPAND)
       self.SetSizer(sizer)


class BorderTestFrame(wx.Frame):
   def __init__(self):
       wx.Frame.__init__(self, parent=None, title="BorderTest")
       mypanel = MyPanel(self)
       sizer = wx.BoxSizer()
       sizer.Add(mypanel, 1, wx.EXPAND)
       self.SetSizer(sizer)



class BorderTestApp(wx.App):
   def __init__(self):
       wx.App.__init__(self, redirect=False)
       frame = BorderTestFrame()
       frame.Show(True)


if __name__ == '__main__':
   app = BorderTestApp()
   app.MainLoop()
