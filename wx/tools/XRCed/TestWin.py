# Name:         view.py
# Purpose:      TestWindow and related classes
# Author:       Roman Rolinsky <rolinsky@femagsoft.com>
# Created:      13.07.2007
# RCS-ID:       $Id: view.py 47356 2007-07-12 01:00:57Z ROL $

from globals import *
import wx
import view
from component import Manager

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
        if self.object:                 # test window present
            if not frame or frame and not self.frame:
                self.GetFrame().Close()
        self.frame = frame
        self.object = object
        object.SetDropTarget(DropTarget())
        object.Bind(wx.EVT_PAINT, self.OnPaint)
        self.hl = self.hlDT = None
        if self.pos != wx.DefaultPosition:
            self.GetFrame().SetPosition(self.pos)
        if item == self.item:   # try to keep same size
            self.GetFrame().SetSize(self.size)
        self.item = item
        self.hl = None

    def OnPaint(self, evt):
        if self.hl: self.hl.Refresh()
        evt.Skip()

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
        if self.hl: self.hl.Destroy()
        if self.frame: self.frame.Destroy()
        elif self.object: self.object.Destroy()
        self.frame = self.object = self.item = None

    # Find wx object corresponding to a tree item (or return None)
    def FindObject(self, item):
        tree = view.tree
        if not item or item == tree.root: return None
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
            item = items.pop()
            index = tree.ItemIndex(item)
            obj = comp.getChildObject(obj, index)
            node = tree.GetPyData(item)
            comp = Manager.getNodeComp(node)
        return obj

    def Highlight(self, rect):
        if not self.hl:
#            if self.frame:
#                self.hl = Highlight(self.frame.panel, rect)
#            else:
                self.hl = Highlight(self.object, rect)
        else:
            self.hl.Move(rect)
            
    def HighlightSizerItem(self, rect):
        self.hl.AddSizerItem(rect)
  
    def RemoveHighlight(self):
        if self.hl is None: return
        self.hl.Destroy()
        self.hl = None
        
################################################################################

# DragAndDrop

class DropTarget(wx.PyDropTarget):
    def __init__(self):
        self.do = MyDataObject()
        wx.DropTarget.__init__(self, self.do)

    # Find best object for dropping
    def WhereToDrop(self, x, y, d):
        raise NotImplementedError
        
        # Find object by position
        obj = wx.FindWindowAtPoint(g.testWin.ClientToScreen((x,y)))
        if not obj:
            return wx.DragNone, ()

    def Destroy(self):
        if self.frame: self.frame.Destroy()
        elif self.object: self.object.Destroy()
        self.frame = self.object = self.item = None

        item = g.frame.FindObject(g.testWin.item, obj)
        if not item:
            return wx.DragNone, ()
        xxx = g.tree.GetPyData(item).treeObject()
        parentItem = None
        # Check if window has a XRC sizer, then use it as parent
        if obj.GetSizer():
            sizer = obj.GetSizer()
            sizerItem = g.frame.FindObject(g.testWin.item, sizer)
            if sizerItem:
                parentItem = sizerItem
                obj = sizer
                item = wx.TreeItemId()
        # if not sizer but can have children, it is parent with free placement
        elif xxx.hasChildren:
            parentItem = item
            item = wx.TreeItemId()
        # Otherwise, try to add to item's parent
        if not parentItem:
            parentItem = g.tree.GetItemParent(item)
            obj = g.tree.FindNodeObject(parentItem)
        parent = g.tree.GetPyData(parentItem).treeObject()
        return d,(obj,parent,parentItem,item)
        
    # Drop
    def OnData(self, x, y, d):
        raise NotImplementedError
        
        self.GetData()
        id = int(self.do.GetDataHere())
        d,other = self.WhereToDrop(x, y, d)
        if d != wx.DragNone:
            obj,parent,parentItem,item = other
            view.tree.SetSelection(parentItem)
            xxx = g.frame.CreateXXX(parent, parentItem, item,  id)
            # Set coordinates if parent is not sizer
            if not parent.isSizer:
                xxx.set('pos', '%d,%d' % (x, y))
                view.panel.SetData(xxx)
            view.frame.SetStatusText('Object created')
        self.RemoveHL()
        return d

    def OnDragOver(self, x, y, d):
        raise NotImplementedError
        
        d,other = self.WhereToDrop(x, y, d)
        if d != wx.DragNone:
            obj,parent,parentItem,item = other
            pos, size = g.tree.FindNodePos(parentItem, obj), obj.GetSize()
            hl = g.testWin.highLightDT
            # Set color of highlighted item back to normal
            if hl and hl.item:
                if hl.item != parentItem:
                    g.tree.SetItemTextColour(hl.item, g.tree.itemColour)
                    # Highlight future parent
                    g.tree.itemColour = g.tree.GetItemTextColour(parentItem) # save current
            if not hl or hl.item != parentItem:
                g.testWin.highLightDT = updateHL(hl, HighLightDTBox, pos, size)
                g.testWin.highLightDT.item = parentItem
            g.tree.SetItemTextColour(parentItem, g.tree.COLOUR_DT)
            g.tree.EnsureVisible(parentItem)
            g.frame.SetStatusText('Drop target: %s' % parent.treeName())
        else:
            g.frame.SetStatusText('Inappropriate drop target')
            self.RemoveHL()
        return d

    def OnLeave(self):
        raise NotImplementedError
        
        self.RemoveHL()

################################################################################

class Highlight:
    def __init__(self, w, rect, colour=wx.RED):
        self.win = w
        self.colour = colour
        if rect.width == -1: rect.width = 0
        if rect.height == -1: rect.height = 0
        self.lines = [wx.Window(w, -1, rect.GetTopLeft(), (rect.width, 2)),
                      wx.Window(w, -1, rect.GetTopLeft(), (2, rect.height)),
                      wx.Window(w, -1, (rect.x + rect.width - 2, rect.y), (2, rect.height)),
                      wx.Window(w, -1, (rect.x, rect.y + rect.height - 2), (rect.width, 2))]
        [l.SetBackgroundColour(colour) for l in self.lines]
        if wx.Platform == '__WXMSW__':
            [l.Bind(wx.EVT_PAINT, self.OnPaint) for l in self.lines]
        self.rect = rect
    # Repainting is not always done for these windows on Windows
    def OnPaint(self, evt):
        w = evt.GetEventObject()
        dc = wx.PaintDC(w)
        w.ClearBackground()
        dc.Destroy()
    def Destroy(self):
        [l.Destroy() for l in self.lines]
    def Refresh(self):
        [l.Refresh() for l in self.lines]
    def Move(self, rect):
        pos = rect.GetTopLeft()
        size = rect.GetSize()
        if size.width == -1: size.width = 0
        if size.height == -1: size.height = 0
        [l.Destroy() for l in self.lines[4:]]
        self.lines[4:] = []
        self.lines[0].SetDimensions(pos.x, pos.y, size.width, 2)
        self.lines[1].SetDimensions(pos.x, pos.y, 2, size.height)
        self.lines[2].SetDimensions(pos.x + size.width - 2, pos.y, 2, size.height)
        self.lines[3].SetDimensions(pos.x, pos.y + size.height - 2, size.width, 2)
        self.Refresh()
    def AddSizerItem(self, rect):
        w = self.win
        colour = self.colour
        lines = [wx.Window(w, -1, rect.GetTopLeft(), (rect.width, 1)),
                 wx.Window(w, -1, rect.GetTopLeft(), (1, rect.height)),
                 wx.Window(w, -1, (rect.x + rect.width - 1, rect.y), (1, rect.height)),
                 wx.Window(w, -1, (rect.x, rect.y + rect.height - 1), (rect.width, 1))]
        [l.SetBackgroundColour(colour) for l in lines]
        if wx.Platform == '__WXMSW__':
            [l.Bind(wx.EVT_PAINT, self.OnPaint) for l in lines]
        self.lines.extend(lines)
