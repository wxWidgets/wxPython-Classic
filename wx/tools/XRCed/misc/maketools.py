# Name:         maketools.py
# Purpose:      Script to create tool bitmaps by screen capture
# Author:       Roman Rolinsky <rolinsky@femagsoft.com>
# Created:      04.07.2007
# RCS-ID:       $Id$

import os,sys,time
import wx
import wx.xrc as xrc
import wx.grid as grid

def WTF(win, filename):
    """WindowToFile: save part of the screen as 'filename'."""
    if wx.Platform == '__WXMAC__':
        # Blit does not write color
        os.system('screencapture scr.png')
        screen = wx.Bitmap('scr.png')
        rect = win.GetRect()
        bitmap = screen.GetSubBitmap(rect)
    else:
        context = wx.ScreenDC()
        memory = wx.MemoryDC()
        x,y = win.GetPosition()
        w,h = win.GetSize()
        x0,y0 = win.ClientToScreen((0,0))
        h += y0 - y + 5
        w += 10
        bitmap = wx.EmptyBitmap(w, h, -1)
        memory.SelectObject(bitmap)
        memory.Blit(0, 0, w, h, context, x, y)
        memory.Destroy()
        context.Destroy()
    print 'Saving bitmap ', filename
    bitmap.SaveFile(filename, wx.BITMAP_TYPE_PNG)
    bitmap.Destroy()


def WTFC(win, filename, obj):
    """WindowToFileClient"""
    if wx.Platform == '__WXMAC__':
        # Blit does not write color
        os.system('screencapture scr.png')
        screen = wx.Bitmap('scr.png')
        rect = win.GetClientRect()
        rect.Offset(win.ClientToScreen((0, 0)))
        bitmap = screen.GetSubBitmap(rect)
    else:
        context = wx.ScreenDC()
        memory = wx.MemoryDC()
        x,y = win.GetPosition()
        w,h = win.GetSize()
        x0,y0 = win.ClientToScreen((0,0))
        h = obj.GetSize()[1]
#        h += y0 - y + 5
#        w += 10
        bitmap = wx.EmptyBitmap(128, h, -1)
        memory.SelectObject(bitmap)
        memory.Blit(0, 0, 128, h, context, x0, y + 24)
        memory.Destroy()
        context.Destroy()
    print 'Saving bitmap ', filename
    bitmap.SaveFile(filename, wx.BITMAP_TYPE_PNG)
    bitmap.Destroy()


def WCTF(win, dirname):
    """WindowChildrenToFile: save all child windows."""
    if wx.Platform == '__WXMAC__':
        # Blit does not write color
        os.system('screencapture scr.png')
        screen = wx.Bitmap('scr.png')
        rect = win.GetClientRect()
        rect.Offset(win.ClientToScreen((0, 0)))
        bitmap = screen.GetSubBitmap(rect)
    else:
        context = wx.ClientDC(win)
        memory = wx.MemoryDC()
        x,y = win.GetPosition()
        w,h = win.GetSize()
        bitmap = wx.EmptyBitmap(w, h, -1)
        memory.SelectObject(bitmap)
        memory.Blit(0, 0, w, h, context, 0, 0)
        memory.Destroy()
        context.Destroy()
    for w in win.GetChildren():
        klass = w.GetClassName()
        if w.GetName() != '-1': # replace by the true name
            klass = w.GetName()
        print 'Saving bitmap for', klass
        filename = os.path.join(dirname, klass + '.png')
        sub = bitmap.GetSubBitmap(w.GetRect())
        sub.SaveFile(filename, wx.BITMAP_TYPE_PNG)
        sub.Destroy()
    bitmap.Destroy()

def create_panels(main_frame):
    frame = res.LoadFrame(main_frame, 'FRAME_Panels')
    if not frame:
        print 'error loading FRAME_Panels'
        return None
    # Put some data
    for w in frame.GetChildren():
        klass = w.GetClassName()
        if klass == 'wxTreeCtrl':
            r = w.AddRoot('Items')
            w.AppendItem(r, 'Item 1')
            w.AppendItem(r, 'Item 2')
            w.Expand(r)
        elif klass == 'wxListCtrl':
            w.InsertStringItem(0, "Item 1")
            w.InsertStringItem(1, "Item 2")
            w.InsertStringItem(2, "Item 3")
            w.InsertStringItem(3, "Item 4")
            w.InsertStringItem(4, "Item 5")
            w.InsertStringItem(5, "Item 6")
            w.InsertStringItem(6, "Item 7")
            w.InsertStringItem(7, "Item 8")
        elif klass == 'wxGrid':
            w.CreateGrid(2,1)
            w.AutoSizeRows()
            w.AutoSizeColumns()
        elif klass == 'wxScrolledWindow':
#            w.SetVirtualSize((20,20))
            sizer = wx.BoxSizer()
            p = wx.Panel(w, size=(100,100), style=wx.SUNKEN_BORDER)
#            w.SetScrollbars(1,1,10,10,1,1)
            p.SetBackgroundColour(wx.WHITE)
            sizer.Add(p)
            w.SetSizer(sizer)
    frame.Fit()
    frame.Show()
    return frame

def create_controls(main_frame):
    frame = res.LoadFrame(main_frame, 'FRAME_Controls')
    if not frame:
        print 'error loading FRAME_Controls'
        return None
    frame.Fit()
    frame.Show()
    return frame

def snap(evt):
    if evt.GetId() == xrc.XRCID('snap_panels'):
        WCTF(app.frame_panels, 'bitmaps')
    elif evt.GetId() == xrc.XRCID('snap_controls'):
        WCTF(app.frame_controls, 'bitmaps')
    elif evt.GetId() == xrc.XRCID('snap_frame'):
        WTF(app.frame_frame, 'bitmaps/wxFrame.png')
    elif evt.GetId() == xrc.XRCID('snap_dialog'):
        WTF(app.frame_dialog, 'bitmaps/wxDialog.png')
    elif evt.GetId() == xrc.XRCID('snap_propsheetdialog'):
        print 'sleeping 1 sec'
        time.sleep(1)
        WTF(app.frame_propsheetdialog, 'bitmaps/wxPropertySheetDialog.png')
    elif evt.GetId() == xrc.XRCID('snap_menubar'):
        WTFC(app.frame_menubar, 'bitmaps/wxMenuBar.png', app.frame_menubar.GetMenuBar())
    elif evt.GetId() == xrc.XRCID('snap_menu'):
        WTFC(app.frame_menubar, 'bitmaps/wxMenuBar.png')
    elif evt.GetId() == xrc.XRCID('snap_toolbar'):
        WTFC(app.frame_menubar, 'bitmaps/wxToolBar.png', app.frame_menubar.GetToolBar())

if __name__ == '__main__':
    try: 
        resFile = sys.argv[1]
    except:
        print 'usage: python maketools.py xrc_file'
        sys.exit(1)
    global app
    app = wx.PySimpleApp(useBestVisual=False)
    res = xrc.EmptyXmlResource()
    res.Load(resFile)

    # Main frame
    main_frame = res.LoadFrame(None, 'main_frame')
    assert main_frame
    app.main_frame = main_frame

    app.frame_panels = create_panels(main_frame)
    app.frame_panels.SetPosition((0,100))
    app.frame_controls = create_controls(main_frame)
    app.frame_panels.SetPosition((350,100))
    app.frame_frame = wx.Frame(main_frame, -1, '', (0,300), (128, 100))
    app.frame_frame.Show()
    app.frame_dialog = wx.Dialog(main_frame, -1, '', (140,300), (128, 100))
    app.frame_dialog.SetSize((128,100))    
    app.frame_dialog.Show()
    app.frame_propsheetdialog = res.LoadObject(main_frame, 'PROPSHEETDIALOG', 'wxPropertySheetDialog')
    app.frame_propsheetdialog.Show()
    app.frame_menubar = res.LoadFrame(main_frame, 'FRAME_MenuBar')
    app.frame_menubar.Show()
    app.frame_menubar = res.LoadFrame(main_frame, 'FRAME_ToolBar')
    app.frame_menubar.Show()

    if not os.path.exists('bitmaps'): os.mkdir('bitmaps')

    main_frame.Bind(wx.EVT_MENU, snap, id=xrc.XRCID('snap_panels'))
    main_frame.Bind(wx.EVT_MENU, snap, id=xrc.XRCID('snap_controls'))
    main_frame.Bind(wx.EVT_MENU, snap, id=xrc.XRCID('snap_frame'))
    main_frame.Bind(wx.EVT_MENU, snap, id=xrc.XRCID('snap_dialog'))
    main_frame.Bind(wx.EVT_MENU, snap, id=xrc.XRCID('snap_propsheetdialog'))
    main_frame.Bind(wx.EVT_MENU, snap, id=xrc.XRCID('snap_menubar'))
    main_frame.Bind(wx.EVT_MENU, snap, id=xrc.XRCID('snap_toolbar'))
    main_frame.Bind(wx.EVT_MENU, lambda evt: main_frame.Close(), id=wx.ID_EXIT)
    main_frame.SetStatusText('status')

    main_frame.Show()
    app.MainLoop()
