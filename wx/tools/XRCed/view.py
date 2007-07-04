# Name:         view.py
# Purpose:      View classes
# Author:       Roman Rolinsky <rolinsky@femagsoft.com>
# Created:      07.06.2007
# RCS-ID:       $Id$

import os
from globals import *
from XMLTree import XMLTree
from XMLTreeMenu import XMLTreeMenu
from AttributePanel import Panel
from tools import ToolPanel
import images

def CreateView():
    '''
    Create all necessary view objects. Some of them are set as module
    global variables for convenience.
    '''

    # Load resources
    res = xrc.EmptyXmlResource()
    res.Load(os.path.join(g.basePath, 'xrced.xrc'))
    g.res = res

    global frame
    frame = Frame()                     # frame creates other

    # Tool panel on a MiniFrame
    global toolFrame
    toolFrame = wx.MiniFrame(frame, -1, 'Tool Panel')
    toolPanel = ToolPanel(toolFrame)

class Frame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, -1, '', size=(640,480))
        bar = self.CreateStatusBar(2)
        bar.SetStatusWidths([-1, 40])
        self.SetIcon(images.getIconIcon())

        self.InitMenuBar()

        self.ID_TOOL_PASTE = wx.NewId()
        self.ID_TOOL_LOCATE = wx.NewId()

        # Create toolbar
        self.tb = tb = self.CreateToolBar(wx.TB_HORIZONTAL | wx.NO_BORDER | wx.TB_FLAT)
        # Use tango icons and slightly wider bitmap size on Mac
        if wx.Platform in ['__WXMAC__', '__WXMSW__']:
            tb.SetToolBitmapSize((26,26))
        else:
            tb.SetToolBitmapSize((24,24))
        self.InitToolBar(g.conf.embedPanel) # add tools

        # Build interface
        sizer = wx.BoxSizer(wx.VERTICAL)
        #sizer.Add(wx.StaticLine(self, -1), 0, wx.EXPAND)
        # Horizontal sizer for toolbar and splitter
        self.toolsSizer = sizer1 = wx.BoxSizer()
        splitter = wx.SplitterWindow(self, -1, style=wx.SP_3DSASH)
        self.splitter = splitter
        splitter.SetMinimumPaneSize(100)

        global tree
        tree = XMLTree(splitter)

        # Miniframe for split mode
        self.miniFrame = mf = wx.MiniFrame(self, -1, 'Attributes',
                                           (g.conf.panelX, g.conf.panelY),
                                           (g.conf.panelWidth, g.conf.panelHeight))
        mf.tb = mf.CreateToolBar(wx.TB_HORIZONTAL | wx.NO_BORDER | wx.TB_FLAT)
        # Use tango icons and slightly wider bitmap size on Mac
        if wx.Platform in ['__WXMAC__', '__WXMSW__']:
            mf.tb.SetToolBitmapSize((26,26))
        else:
            mf.tb.SetToolBitmapSize((24,24))
        self.InitMiniToolBar(mf.tb)
        
        sizer2 = wx.BoxSizer()
        mf.SetSizer(sizer2)

        # Create attribute panel
        global panel
        if g.conf.embedPanel:
            panel = Panel(splitter)
            # Set plitter windows
            splitter.SplitVertically(tree, panel, g.conf.sashPos)
        else:
            panel = Panel(miniFrame)
            sizer2.Add(panel, 1, wx.EXPAND)
            miniFrame.Show(True)
            splitter.Initialize(tree)
        if wx.Platform == '__WXMAC__':
            sizer1.Add(splitter, 1, wx.EXPAND|wx.RIGHT, 5)
        else:
            sizer1.Add(splitter, 1, wx.EXPAND)
        sizer.Add(sizer1, 1, wx.EXPAND)

        self.SetSizer(sizer)

    def Clear(self):
        pass

    def InitMenuBar(self):
        # Make menus
        menuBar = wx.MenuBar()

        menu = wx.Menu()                # File menu
        menu.Append(wx.ID_NEW, '&New\tCtrl-N', 'New file')
        menu.AppendSeparator()
        menu.Append(wx.ID_OPEN, '&Open...\tCtrl-O', 'Open XRC file')
        
        self.recentMenu = wx.Menu()
        g.fileHistory.UseMenu(self.recentMenu)
        g.fileHistory.AddFilesToMenu()

        menu.AppendMenu(-1, 'Open &Recent', self.recentMenu, 'Open a recent file')
        
        menu.AppendSeparator()
        menu.Append(wx.ID_SAVE, '&Save\tCtrl-S', 'Save XRC file')
        menu.Append(wx.ID_SAVEAS, 'Save &As...', 'Save XRC file under different name')
        self.ID_GENERATE_PYTHON = wx.NewId()
        menu.Append(self.ID_GENERATE_PYTHON, '&Generate Python...', 
                    'Generate a Python module that uses this XRC')
        menu.AppendSeparator()
        self.ID_PREFS = wx.NewId()
        menu.Append(self.ID_PREFS, 'Preferences...', 'Change XRCed settings')
        menu.AppendSeparator()
        menu.Append(wx.ID_EXIT, '&Quit\tCtrl-Q', 'Exit application')

        menuBar.Append(menu, '&File')

        menu = wx.Menu()                # Edit menu
        menu.Append(wx.ID_UNDO, '&Undo\tCtrl-Z', 'Undo')
        menu.Append(wx.ID_REDO, '&Redo\tCtrl-Y', 'Redo')
        menu.AppendSeparator()
        menu.Append(wx.ID_CUT, 'Cut\tCtrl-X', 'Cut to the clipboard')
        menu.Append(wx.ID_COPY, '&Copy\tCtrl-C', 'Copy to the clipboard')
        menu.Append(wx.ID_PASTE, '&Paste\tCtrl-V', 'Paste from the clipboard')
        menu.Append(wx.ID_DELETE, '&Delete\tCtrl-D', 'Delete object')
        menu.AppendSeparator()
        self.ID_LOCATE = wx.NewId()
        self.ART_LOCATE = 'ART_LOCATE'
        menu.Append(self.ID_LOCATE, '&Locate\tCtrl-L', 'Locate control in test window and select it')
        
        menuBar.Append(menu, '&Edit')
        
        menu = wx.Menu()                # View menu
        self.ID_EMBED_PANEL = wx.NewId()
        menu.Append(self.ID_EMBED_PANEL, '&Embed Panel',
                    'Toggle embedding properties panel in the main window', True)
        menu.Check(self.ID_EMBED_PANEL, g.conf.embedPanel)
        self.ID_SHOW_TOOLS = wx.NewId()
        menu.Append(self.ID_SHOW_TOOLS, 'Show &Tools', 'Toggle tools', True)
        menu.Check(self.ID_SHOW_TOOLS, g.conf.showTools)
        menu.AppendSeparator()
        self.ID_TEST = wx.NewId()
        self.ART_TEST = 'ART_TEST'
        menu.Append(self.ID_TEST, '&Test\tF5', 'Show test window')
        self.ID_REFRESH = wx.NewId()
        self.ART_REFRESH = 'ART_REFRESH'
        menu.Append(self.ID_REFRESH, '&Refresh\tCtrl-R', 'Refresh test window')
        self.ID_AUTO_REFRESH = wx.NewId()
        self.ART_AUTO_REFRESH = 'ART_AUTO_REFRESH'
        menu.Append(self.ID_AUTO_REFRESH, '&Auto-refresh\tAlt-A',
                    'Toggle auto-refresh mode', True)
        menu.Check(self.ID_AUTO_REFRESH, g.conf.autoRefresh)
        self.ID_TEST_HIDE = wx.NewId()
        menu.Append(self.ID_TEST_HIDE, '&Hide\tF6', 'Close test window')
        menu.AppendSeparator()
        self.ID_SHOW_XML = wx.NewId()
        menu.Append(self.ID_SHOW_XML, 'Show &XML...', 'Show XML source for the selected subtree')
        
        menuBar.Append(menu, '&View')

        menu = wx.Menu()                # Move menu
        self.ID_MOVEUP = wx.NewId()
        self.ART_MOVEUP = 'ART_MOVEUP'
        menu.Append(self.ID_MOVEUP, '&Up', 'Move before previous sibling')
        self.ID_MOVEDOWN = wx.NewId()
        self.ART_MOVEDOWN = 'ART_MOVEDOWN'
        menu.Append(self.ID_MOVEDOWN, '&Down', 'Move after next sibling')
        self.ID_MOVELEFT = wx.NewId()
        self.ART_MOVELEFT = 'ART_MOVELEFT'
        menu.Append(self.ID_MOVELEFT, '&Make sibling', 'Make sibling of parent')
        self.ID_MOVERIGHT = wx.NewId()
        self.ART_MOVERIGHT = 'ART_MOVERIGHT'
        menu.Append(self.ID_MOVERIGHT, '&Make child', 'Make child of previous sibling')
        
        menuBar.Append(menu, '&Move')

        menu = wx.Menu()                # Help menu
        menu.Append(wx.ID_ABOUT, '&About...', 'About XCRed')
        self.ID_README = wx.NewId()
        menu.Append(self.ID_README, '&Readme...\tF1', 'View the README file')
        if debug:
            self.ID_DEBUG_CMD = wx.NewId()
            menu.Append(self.ID_DEBUG_CMD, 'CMD', 'Python command line')
            
        menuBar.Append(menu, '&Help')

        self.menuBar = menuBar
        self.SetMenuBar(menuBar)

    def InitToolBar(self, long):
        '''Initialize toolbar, long is boolean.'''
        tb = self.tb
        tb.ClearTools()
        new_bmp  = wx.ArtProvider.GetBitmap(wx.ART_NORMAL_FILE, wx.ART_TOOLBAR)
        open_bmp = wx.ArtProvider.GetBitmap(wx.ART_FILE_OPEN, wx.ART_TOOLBAR)
        save_bmp = wx.ArtProvider.GetBitmap(wx.ART_FILE_SAVE, wx.ART_TOOLBAR)
        undo_bmp = wx.ArtProvider.GetBitmap(wx.ART_UNDO, wx.ART_TOOLBAR)
        redo_bmp = wx.ArtProvider.GetBitmap(wx.ART_REDO, wx.ART_TOOLBAR)
        cut_bmp  = wx.ArtProvider.GetBitmap(wx.ART_CUT, wx.ART_TOOLBAR)
        copy_bmp = wx.ArtProvider.GetBitmap(wx.ART_COPY, wx.ART_TOOLBAR)
        paste_bmp= wx.ArtProvider.GetBitmap(wx.ART_PASTE, wx.ART_TOOLBAR)
        tb.AddSimpleTool(wx.ID_NEW, new_bmp, 'New', 'New file')
        tb.AddSimpleTool(wx.ID_OPEN, open_bmp, 'Open', 'Open file')
        tb.AddSimpleTool(wx.ID_SAVE, save_bmp, 'Save', 'Save file')
        tb.AddSeparator()
        tb.AddSimpleTool(wx.ID_UNDO, undo_bmp, 'Undo', 'Undo')
        tb.AddSimpleTool(wx.ID_REDO, redo_bmp, 'Redo', 'Redo')
        tb.AddSeparator()
        tb.AddSimpleTool(wx.ID_CUT, cut_bmp, 'Cut', 'Cut')
        tb.AddSimpleTool(wx.ID_COPY, copy_bmp, 'Copy', 'Copy')
        tb.AddSimpleTool(self.ID_TOOL_PASTE, paste_bmp, 'Paste', 'Paste')
        tb.AddSeparator()
        bmp = wx.ArtProvider.GetBitmap(self.ART_MOVEUP, wx.ART_TOOLBAR)
        tb.AddSimpleTool(self.ID_MOVEUP, bmp,
                         'Up', 'Move before previous sibling')
        bmp = wx.ArtProvider.GetBitmap(self.ART_MOVEDOWN, wx.ART_TOOLBAR)
        tb.AddSimpleTool(self.ID_MOVEDOWN, bmp,
                         'Down', 'Move after next sibling')
        bmp = wx.ArtProvider.GetBitmap(self.ART_MOVELEFT, wx.ART_TOOLBAR)
        tb.AddSimpleTool(self.ID_MOVELEFT, bmp,
                         'Make Sibling', 'Make sibling of parent')
        bmp = wx.ArtProvider.GetBitmap(self.ART_MOVERIGHT, wx.ART_TOOLBAR)
        tb.AddSimpleTool(self.ID_MOVERIGHT, bmp,
                         'Make Child', 'Make child of previous sibling')
        if long:
            tb.AddSeparator()
            bmp = wx.ArtProvider.GetBitmap(self.ART_LOCATE, wx.ART_TOOLBAR)
            tb.AddSimpleTool(self.ID_TOOL_LOCATE, bmp,
                             'Locate', 'Locate control in test window and select it', True)
            bmp = wx.ArtProvider.GetBitmap(self.ART_TEST, wx.ART_TOOLBAR)
            tb.AddSimpleTool(self.ID_TEST, bmp, 'Test', 'Test window')
            bmp = wx.ArtProvider.GetBitmap(self.ART_REFRESH, wx.ART_TOOLBAR)
            tb.AddSimpleTool(self.ID_REFRESH, bmp, 'Refresh', 'Refresh view')
            bmp = wx.ArtProvider.GetBitmap(self.ART_AUTO_REFRESH, wx.ART_TOOLBAR)
            tb.AddSimpleTool(self.ID_AUTO_REFRESH, bmp,
                             'Auto-refresh', 'Toggle auto-refresh mode', True)
            tb.ToggleTool(self.ID_AUTO_REFRESH, g.conf.autoRefresh)
        tb.Realize()
        self.minWidth = tb.GetSize()[0] # minimal width is the size of toolbar 

    def InitMiniToolBar(self, tb):
        bmp = wx.ArtProvider.GetBitmap(self.ART_LOCATE, wx.ART_TOOLBAR)
        tb.AddSimpleTool(self.ID_TOOL_LOCATE, bmp,
                         'Locate', 'Locate control in test window and select it', True)
        bmp = wx.ArtProvider.GetBitmap(self.ART_TEST, wx.ART_TOOLBAR)
        tb.AddSimpleTool(self.ID_TEST, bmp, 'Test', 'Test window')
        bmp = wx.ArtProvider.GetBitmap(self.ART_REFRESH, wx.ART_TOOLBAR)
        tb.AddSimpleTool(self.ID_REFRESH, bmp, 'Refresh', 'Refresh view')
        bmp = wx.ArtProvider.GetBitmap(self.ART_AUTO_REFRESH, wx.ART_TOOLBAR)
        tb.AddSimpleTool(self.ID_AUTO_REFRESH, bmp,
                         'Auto-refresh', 'Toggle auto-refresh mode', True)
        tb.ToggleTool(self.ID_AUTO_REFRESH, g.conf.autoRefresh)
        tb.Realize() 

    def EmbedUnembed(self, embedPanel):
        conf = g.conf
        conf.embedPanel = embedPanel
        if conf.embedPanel:
            # Remember last dimentions
            conf.panelX, conf.panelY = self.miniFrame.GetPosition()
            conf.panelWidth, conf.panelHeight = self.miniFrame.GetSize()
            size = self.GetSize()
            pos = self.GetPosition()
            sizePanel = panel.GetSize()
            panel.Reparent(self.splitter)
            self.miniFrame.GetSizer().Remove(panel)
            # Widen
            self.SetDimensions(pos.x, pos.y, size.width + sizePanel.width, size.height)
            self.splitter.SplitVertically(tree, panel, conf.sashPos)
            self.miniFrame.Show(False)
        else:
            conf.sashPos = self.splitter.GetSashPosition()
            pos = self.GetPosition()
            size = self.GetSize()
            sizePanel = panel.GetSize()
            self.splitter.Unsplit(panel)
            sizer = self.miniFrame.GetSizer()
            panel.Reparent(self.miniFrame)
            panel.Show(True)
            sizer.Add(panel, 1, wx.EXPAND)
            self.miniFrame.Show(True)
            self.miniFrame.SetDimensions(conf.panelX, conf.panelY,
                                         conf.panelWidth, conf.panelHeight)
            self.miniFrame.Layout()
            # Reduce width
            self.SetDimensions(pos.x, pos.y,
                               max(size.width - sizePanel.width, self.minWidth), size.height)
        
        # Set long or short toolbar
        self.InitToolBar(embedPanel)

# ScrolledMessageDialog - modified from wxPython lib to set fixed-width font
class ScrolledMessageDialog(wx.Dialog):
    def __init__(self, parent, msg, caption, textSize=(80,40), centered=True):
        from wx.lib.layoutf import Layoutf
        wx.Dialog.__init__(self, parent, -1, caption)
        text = wx.TextCtrl(self, -1, msg, wx.DefaultPosition,
                             wx.DefaultSize, wx.TE_MULTILINE | wx.TE_READONLY)
        text.SetFont(g.modernFont())
        dc = wx.WindowDC(text)
        w, h = dc.GetFullTextExtent(' ', g.modernFont())[:2]
        ok = wx.Button(self, wx.ID_OK, "OK")
        ok.SetDefault()
        text.SetConstraints(Layoutf('t=t5#1;b=t5#2;l=l5#1;r=r5#1', (self,ok)))
        text.SetSize((w * textSize[0] + 30, h * textSize[1]))
        text.ShowPosition(1)            # scroll to the first line
        ok.SetConstraints(Layoutf('b=b5#1;x%w50#1;w!80;h!35', (self,)))
        self.SetAutoLayout(True)
        self.Fit()
        if centered:
            self.CenterOnScreen(wx.BOTH)

# ArtProvider for toolbar icons
class ToolArtProvider(wx.ArtProvider):
    def __init__(self):
        wx.ArtProvider.__init__(self)
        self.images = {
            'ART_LOCATE': images.getLocateImage(),
            'ART_TEST': images.getTestImage(),
            'ART_REFRESH': images.getRefreshImage(),
            'ART_AUTO_REFRESH': images.getAutoRefreshImage(),
            'ART_MOVEUP': images.getMoveUpImage(),
            'ART_MOVEDOWN': images.getMoveDownImage(),
            'ART_MOVELEFT': images.getMoveLeftImage(),
            'ART_MOVERIGHT': images.getMoveRightImage()
            }
        if wx.Platform in ['__WXMAC__', '__WXMSW__']:
            self.images.update({
                    wx.ART_NORMAL_FILE: images.getNewImage(),
                    wx.ART_FILE_OPEN: images.getOpenImage(),
                    wx.ART_FILE_SAVE: images.getSaveImage(),
                    wx.ART_UNDO: images.getUndoImage(),
                    wx.ART_REDO: images.getRedoImage(),
                    wx.ART_CUT: images.getCutImage(),
                    wx.ART_COPY: images.getCopyImage(),
                    wx.ART_PASTE: images.getPasteImage()
                    })

    def CreateBitmap(self, id, client, size):
        bmp = wx.NullBitmap
        if id in self.images:
            img = self.images[id]
            # Alpha not implemented completely there
            if wx.Platform in ['__WXMAC__', '__WXMSW__']:
                img.ConvertAlphaToMask()
            bmp = wx.BitmapFromImage(img)
        return bmp

################################################################################

class _TestWindow:
    '''Test window manager showing currently edited subtree.'''
    def __init__(self):
        self.Init()

    def Init(self):
        self.hl = self.hlDT = None      # highlight objects
        self.frame = self.object = None # currenly shown frame and related object
        self.item = None
        self.pos = wx.DefaultPosition
        self.size = wx.DefaultSize        

    def SetView(self, frame, object, item):
        if self.object:                 # test window present
            if not frame or frame and not self.frame:
                self.GetFrame().Close()
                wx.Yield()
        self.frame = frame
        self.object = object
        object.SetDropTarget(DropTarget())
        self.hl = self.hlDT = None
        if self.pos != wx.DefaultPosition:
            self.GetFrame().SetPosition(self.pos)
        if item == self.item:   # try to keep same size
            self.GetFrame().SetSize(self.size)
        self.item = item

    def GetFrame(self):
        if self.frame: return self.frame
        else: return self.object

    def Show(self, show=True):
        self.GetFrame().Show(show)

    def IsShown(self):
        return self.object is not None and self.object.IsShown()

    def Destroy(self):
        if self.frame: self.frame.Destroy()
        elif self.object: self.object.Destroy()
        self.frame = self.object = self.item = None

testWin = _TestWindow()

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

    def RemoveHL(self):
        raise NotImplementedError
        
        hl = g.testWin.highLightDT
        if hl:
            if hl.item:
                g.tree.SetItemTextColour(hl.item, g.tree.itemColour)
            hl.Remove()
        
