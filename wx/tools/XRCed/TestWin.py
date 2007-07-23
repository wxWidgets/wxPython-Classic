# Name:         view.py
# Purpose:      TestWindow and related classes
# Author:       Roman Rolinsky <rolinsky@femagsoft.com>
# Created:      13.07.2007
# RCS-ID:       $Id: view.py 47356 2007-07-12 01:00:57Z ROL $

from globals import *
import wx
import view
from component import Manager

def getAllChildren(w, children):
    for ch in w.GetChildren():
        children.append(ch)
        children.extend(getAllChildren(ch, children))
    return children

class TestWindow:
    '''Test window manager showing currently edited subtree.'''
    def __init__(self):
        self.Init()

    def Init(self):
        self.hl = self.hlDT = None      # highlight objects (Rect)
        self.frame = self.object = None # currenly shown frame and related object
        self.item = None
        self.pos = wx.DefaultPosition
        self.size = wx.DefaultSize        
        self.isDirty = False            # if refresh neeeded

    def SetView(self, frame, object, item):
        TRACE('SetView %s %s', frame, object)
        restoreSize = False
        if self.object:
            # Old window must be destroyed in new uses different frame
            # or is itself a toplevel window
            if not frame or frame and not self.frame:
                # Remember old item
                if item == self.item:
                    restoreSize = True
                TRACE('Closing old frame, restoreSize=%d', restoreSize)
                self.GetFrame().Close()
        self.frame = frame
        self.object = object
        object.SetDropTarget(DropTarget(object))
        if wx.Platform == '__WXMAC__':
            for ch in getAllChildren(object, []):
                ch.SetDropTarget(DropTarget(ch))
        object.Bind(wx.EVT_PAINT, self.OnPaint)
        if self.pos != wx.DefaultPosition:
            self.GetFrame().SetPosition(self.pos)
        if restoreSize:   # keep same size in refreshing
            TRACE('restoring size %s', self.size)
            self.GetFrame().SetSize(self.size)
        self.item = item
        self.hl = self.hlDT = None
        g.Listener.InstallTestWinEvents()
                
    def OnPaint(self, evt):
        if self.hl: self.hl.Refresh()

    def GetFrame(self):
        if self.frame: return self.frame
        else: return self.object

    def Show(self, show=True):
        self.GetFrame().Show(show)

    def IsShown(self):
        return bool(self.object) and self.object.IsShown()

    def IsDirty(self):
        '''If test window must be refreshed.'''
        return self.IsShown() and self.isDirty

    def Destroy(self):
        TRACE('Destroy')
        # Remember dimensions
        self.pos = self.GetFrame().GetPosition()
        self.size = self.GetFrame().GetSize()
        self.GetFrame().Destroy()
        self.frame = self.object = self.item = None
        self.hl = self.hlDT = None

    # Find the object for an item
    def FindObject(self, item):
        tree = view.tree
        if not item or item == tree.root:
            return None
        if item == self.item: return self.object
        # Traverse tree until we reach the root  or the test object
        items = [item]
        while 1:
            item = tree.GetItemParent(item)
            if item == tree.root: return None # item outside if the test subtree
            elif item == self.item: break
            else: items.append(item)
        # Now traverse back, searching children
        obj = self.object
        comp = Manager.getNodeComp(tree.GetPyData(self.item))
        while items and obj:
            if not (isinstance(obj, wx.Window) or isinstance(obj, wx.Sizer)):
                return None
            parentItem = item
            item = items.pop()
            index = tree.ItemIndex(item)
            obj = comp.getChildObject(tree.GetPyData(parentItem), obj, index)
            node = tree.GetPyData(item)
            comp = Manager.getNodeComp(node)
        return obj

    # Find tree item corresponding to testWin object
    def FindObjectItem(self, item, obj):
        # We simply perform depth-first traversal, sinse it's too much
        # hassle to deal with all sizer/window combinations
        w = self.FindObject(item)
        if w == obj or isinstance(w, wx.SizerItem) and w.GetWindow() == obj:
            return item
        if view.tree.ItemHasChildren(item):
            child = view.tree.GetFirstChild(item)[0]
            while child:
                found = self.FindObjectItem(child, obj)
                if found: return found
                child = view.tree.GetNextSibling(child)
        return None

    # Find the rectangle or rectangles corresponding to a tree item
    # in the test window (or return None)
    def FindObjectRect(self, item):
        tree = view.tree
        if not item or item == tree.root: return None
        # Traverse tree until we reach the root  or the test object
        items = [item]
        while 1:
            item = tree.GetItemParent(item)
            if item == tree.root: return None # item outside if the test subtree
            elif item == self.item: break
            else: items.append(item)
        # Now traverse back from parents to children
        obj = self.object
        offset = wx.Point(0,0)
        comp = Manager.getNodeComp(tree.GetPyData(self.item))
        while items and obj:
            if not (isinstance(obj, wx.Window) or isinstance(obj, wx.Sizer)):
                return None
            parentItem = item
            item = items.pop()
            index = tree.ItemIndex(item)
            obj = comp.getChildObject(tree.GetPyData(parentItem), obj, index)
            node = tree.GetPyData(item)
            comp = Manager.getNodeComp(node)
            rect = comp.getRect(obj)
            if not rect: return None
            if isinstance(obj, wx.Window) and items:
                offset += rect[0].GetTopLeft()
        [r.Offset(offset) for r in rect]
        return rect

    def Highlight(self, rect):
        if not self.hl:
            self.hl = Highlight(self.object, rect)
        else:
            self.hl.Move(rect)
            
    def HighlightDT(self, rect, item):
        print 'hlDT'
        if not self.hlDT:
            self.hlDT = Highlight(self.object, rect, wx.BLUE)
            self.hlDT.origColour = view.tree.GetItemTextColour(item)
        else:
            self.hlDT.Move(rect)
            view.tree.SetItemTextColour(self.hlDT.item, self.hlDT.origColour)
        view.tree.SetItemTextColour(item, view.tree.COLOUR_DT)            
        self.hlDT.item = item
            
    def RemoveHighlight(self):
        if self.hl is None: return
        self.hl.Destroy()
        self.hl = None
        
    def RemoveHighlightDT(self):
        print 'removehlDT'
        if self.hlDT is None: return
        if self.hlDT.item:
            view.tree.SetItemTextColour(self.hlDT.item, self.hlDT.origColour)
        self.hlDT.Destroy()
        self.hlDT = None
        view.frame.SetStatusText('')

            
################################################################################

# DragAndDrop

class DropTarget(wx.DropTarget):
    def __init__(self, win):
        self.win = win
        self.do = MyDataObject()
        wx.DropTarget.__init__(self, self.do)
        self.onHL = self.left = False

    # Find best object for dropping
    def WhereToDrop(self, x, y, d):
        print 'whereto',x,y
        # Find object by position
        if wx.Platform == '__WXMAC__':
            scrPos = self.win.ClientToScreen((x,y))
        else:
            scrPos = view.testWin.object.ClientToScreen((x,y))
        print scrPos
        obj = wx.FindWindowAtPoint(scrPos)
        print 'obj=', obj
        if not obj:
            return wx.DragNone, ()
        if view.testWin.hlDT and obj in view.testWin.hlDT.lines:
            self.onHL = True
            print 'on hl'
            return d, ()
        item = view.testWin.FindObjectItem(view.testWin.item, obj)
        if not item:
            return wx.DragNone, ()
        # If window has a sizer use it as parent
        if obj.GetSizer():
            obj = obj.GetSizer()
            item = view.testWin.FindObjectItem(view.testWin.item, obj)
        return d, (obj,item)

    # Drop
    def OnData(self, x, y, d):
#        import pdb;pdb.set_trace()
        view.testWin.RemoveHighlightDT()
        self.onHL = self.left = False
        self.GetData()
        id = int(self.do.GetDataHere())
        d,other = self.WhereToDrop(x, y, d)
        if d != wx.DragNone and other:
            obj,item = other
            g.Presenter.setData(item)
            comp = Manager.findById(id)
            mouseState = wx.GetMouseState()
            forceSibling = mouseState.ControlDown()
            forceInsert = mouseState.ShiftDown()
            g.Presenter.updateCreateState(forceSibling, forceInsert)
            if not g.Presenter.checkCompatibility(comp):
                return wx.DragNone
            item = g.Presenter.create(comp)
            node = view.tree.GetPyData(item)
            parentItem = view.tree.GetItemParent(item)
            parentNode = view.tree.GetPyData(parentItem)
            parentComp = Manager.getNodeComp(parentNode)
            # If pos if not set by default and parent is not a sizer, set pos to
            # drop coordinates
            if 'pos' in comp.attributes and not comp.getAttribute(node, 'pos') \
                   and parentComp.isContainer() and \
                   not parentComp.isSizer():
                # Calc relative coords
                rect = view.testWin.FindObjectRect(parentItem)
                x -= rect[0].x
                y -= rect[0].y
                comp.addAttribute(node, 'pos', '%d,%d' % (x, y))
                g.Presenter.setData(item)
            view.frame.SetStatusText('Object created')
        return d

    def OnDragOver(self, x, y, d):
        d,other = self.WhereToDrop(x, y, d)
        if d == wx.DragNone:
            view.frame.SetStatusText('Inappropriate drop target')
            view.testWin.RemoveHighlightDT()
        elif other:
            if self.left: 
                view.testWin.RemoveHighlightDT()
                self.onHL = self.left = False
            obj,item = other
            hl = view.testWin.hlDT
            if not hl or hl.item != item:
                rect = view.testWin.FindObjectRect(item)
                if not rect: return wx.DragNone
                view.testWin.HighlightDT(rect, item)
                view.tree.EnsureVisible(item)
            view.frame.SetStatusText('Drop target: %s' % view.tree.GetItemText(item))
        return d

    def OnLeave(self):
        if self.onHL: 
            view.testWin.RemoveHighlightDT()
            self.onHL = False
        else: self.left = True

################################################################################

class Highlight:
    '''
    Create a highlight rectangle by using multiple windows. rect is a
    single Rect or a list of Rects (for sizeritems).
    '''
    def __init__(self, w, rect, colour=wx.RED):
        self.win = w
        self.colour = colour
        rects = rect[1:]
        rect = rect[0]
        if rect.width == -1: rect.width = 0
        if rect.height == -1: rect.height = 0
        self.lines = [wx.Window(w, -1, rect.GetTopLeft(), (rect.width, 2)),
                      wx.Window(w, -1, rect.GetTopLeft(), (2, rect.height)),
                      wx.Window(w, -1, (rect.x + rect.width - 2, rect.y), (2, rect.height)),
                      wx.Window(w, -1, (rect.x, rect.y + rect.height - 2), (rect.width, 2))]
        for l in self.lines:
            l.SetBackgroundColour(colour)
            l.SetDropTarget(DropTarget(l))
        if wx.Platform == '__WXMSW__':
            [l.Bind(wx.EVT_PAINT, self.OnPaint) for l in self.lines]
        for r in rects:
            self.AddSizerItem(r)
    # Repainting is not always done for these windows on Windows
    def OnPaint(self, evt):
        w = evt.GetEventObject()
        dc = wx.PaintDC(w)
        w.ClearBackground()
        dc.Destroy()
    def Destroy(self):
        for l in self.lines:
            l.Hide()
            wx.CallAfter(l.Destroy)
    def Refresh(self):
        [l.Refresh() for l in self.lines]
    def Move(self, rect):
        print 'move',rect
        rects = rect[1:]
        rect = rect[0]
        pos = rect.GetTopLeft()
        size = rect.GetSize()
        if size.width == -1: size.width = 0
        if size.height == -1: size.height = 0
        for l in self.lines[4:]:
            l.Hide()
            wx.CallAfter(l.Destroy)
        self.lines[4:] = []
        self.lines[0].SetDimensions(pos.x, pos.y, size.width, 2)
        self.lines[1].SetDimensions(pos.x, pos.y, 2, size.height)
        self.lines[2].SetDimensions(pos.x + size.width - 2, pos.y, 2, size.height)
        self.lines[3].SetDimensions(pos.x, pos.y + size.height - 2, size.width, 2)
        for r in rects:
            self.AddSizerItem(r)
#        self.Refresh()
    def AddSizerItem(self, rect):
        w = self.win
        colour = self.colour
        lines = [wx.Window(w, -1, rect.GetTopLeft(), (rect.width, 1)),
                 wx.Window(w, -1, rect.GetTopLeft(), (1, rect.height)),
                 wx.Window(w, -1, (rect.x + rect.width - 1, rect.y), (1, rect.height)),
                 wx.Window(w, -1, (rect.x, rect.y + rect.height - 1), (rect.width, 1))]
        for l in lines:
            l.SetBackgroundColour(colour)
            l.SetDropTarget(DropTarget(l))
        if wx.Platform == '__WXMSW__':
            [l.Bind(wx.EVT_PAINT, self.OnPaint) for l in lines]
        self.lines.extend(lines)
