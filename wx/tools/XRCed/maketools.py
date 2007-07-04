# Name:         maketools.py
# Purpose:      Script to create tool bitmaps by screen capture
# Author:       Roman Rolinsky <rolinsky@femagsoft.com>
# Created:      04.07.2007
# RCS-ID:       $Id$

import os,sys
import wx
import wx.xrc as xrc



def WTF(win, filename):
    """WindowToFile: save part of the screen as 'filename'."""
    context = wx.ClientDC(win)
    memory = wx.MemoryDC( )
    x,y = win.GetPosition()
    w,h = win.GetSize()
#    import pdb;pdb.set_trace()
    print x,y,w,h
    bitmap = wx.EmptyBitmap(w, h, -1)
    memory.SelectObject(bitmap)
    memory.Blit(0, 0, w, h, context, x, y)
#    memory.SelectObject(wx.NullBitmap)
    bitmap.SaveFile(filename, wx.BITMAP_TYPE_BMP)
    memory.Destroy()
    context.Destroy()

def OnCreate(evt):
    print evt.GetEventObject()
    w = evt.GetEventObject()
    WTF(w, os.path.join('bitmaps', w.GetClassName() + '.bmp'))
    evt.Skip()

def OnCloseFrame(evt):
    frame = evt.GetEventObject()
    for w in frame.GetChildren():
        klass = w.GetClassName()
        print klass
        try:
            WTF(w, os.path.join('bitmaps', klass + '.bmp'))
            print 'OK'
        except:
            print 'KO'
    evt.Skip()

if __name__ == '__main__':
    global app
    app = wx.PySimpleApp()
    global res
    res = xrc.EmptyXmlResource()
    res.Load('tools.xrc')
    frame = res.LoadFrame(None, 'FRAME')
#    frame.Bind(wx.EVT_WINDOW_CREATE, OnCreate)
    frame.Bind(wx.EVT_CLOSE, OnCloseFrame)
    frame.Show()
    app.MainLoop()
