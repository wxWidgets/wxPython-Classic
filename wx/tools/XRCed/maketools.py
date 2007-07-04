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
    bitmap = wx.EmptyBitmap(w, h, -1)
    memory.SelectObject(bitmap)
    memory.Blit(0, 0, w, h, context, x, y)
    bitmap.SaveFile(filename, wx.BITMAP_TYPE_BMP)
    bitmap.Destroy()
    memory.Destroy()
    context.Destroy()

def OnCloseFrame(evt):
    frame = evt.GetEventObject()
    for w in frame.GetChildren():
        klass = w.GetClassName()
        print 'Saving bitmap for', klass
        try:
            WTF(w, os.path.join('bitmaps', klass + '.bmp'))
        except:
            print 'Sorry, no luck.'
    evt.Skip()

if __name__ == '__main__':
    try: 
        resFile = sys.argv[1]
    except:
        print 'usage: python maketools.py xrc_file'
    app = wx.PySimpleApp()
    res = xrc.EmptyXmlResource()
    res.Load(resFile)
    frame = res.LoadFrame(None, 'FRAME')
    if not frame:
        print 'error loading FRAME'
        sys.exit(1)
    if not os.path.exists('bitmaps'): os.mkdir('bitmaps')
    frame.Bind(wx.EVT_CLOSE, OnCloseFrame)
    frame.Center(wx.BOTH)
    frame.Show()
    wx.MessageBox('Just close me now.')
    app.MainLoop()
