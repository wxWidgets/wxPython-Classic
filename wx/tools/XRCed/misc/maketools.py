# Name:         maketools.py
# Purpose:      Script to create tool bitmaps by screen capture
# Author:       Roman Rolinsky <rolinsky@femagsoft.com>
# Created:      04.07.2007
# RCS-ID:       $Id$

import os,sys
import wx
import wx.xrc as xrc
import wx.grid as grid


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

def OnOK(evt):
    me = evt.GetEventObject()
    frame = me.GetParent()
    for w in frame.GetChildren():
        if w is me: return
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
        sys.exit(1)
    app = wx.PySimpleApp()
    res = xrc.EmptyXmlResource()
    res.Load(resFile)
    # Frame for controls and other stuff
    for fname in ['FRAME_Panels', 'FRAME_Controls']:
        frame = res.LoadFrame(None, fname)
        if not frame:
            print 'error loading FRAME'
        # Put some data
        for w in frame.GetChildren():
            klass = w.GetClassName()
            if klass == 'wxTreeCtrl':
                r = w.AddRoot('Items')
                w.AppendItem(r, 'Item 1')
                w.AppendItem(r, 'Item 2')
                w.AppendItem(r, 'Item 3')
                w.AppendItem(r, 'Item 4')
                w.Expand(r)
            elif klass == 'wxListCtrl':
                w.InsertStringItem(0, "Item 1")
                w.InsertStringItem(1, "Item 2")
                w.InsertStringItem(2, "Item 3")
                w.InsertStringItem(3, "Item 4")
                w.InsertStringItem(4, "Item 5")
                w.InsertStringItem(5, "Item 6")
            elif klass == 'wxGrid':
                w.CreateGrid(2,1)
                #w.AutoSizeColumns()
        frame.Fit()
        frame.Bind(wx.EVT_BUTTON, OnOK, id=wx.ID_OK)
        frame.Show()
    if not os.path.exists('bitmaps'): os.mkdir('bitmaps')
    app.MainLoop()
