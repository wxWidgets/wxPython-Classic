# Name:         listener.py
# Purpose:      Listener for dispatching events from view to presenter
# Author:       Roman Rolinsky <rolinsky@femagsoft.com>
# Created:      07.06.2007
# RCS-ID:       $Id$

import wx
import os,sys,shutil,tempfile
from globals import *
from presenter import Presenter
from component import Manager
import view
import undo

class _Listener:
    '''
    Installs event handlers to view objects and delegates some events
    to Presenter.
    '''
    def Install(self, frame, tree, panel):
        '''Set event handlers.'''
        self.frame = frame
        self.tree = tree
        self.panel = panel

        # Some local members
        self.inUpdateUI = self.inIdle = False
        self.clipboardHasData = False
        
        # Component events
        wx.EVT_MENU_RANGE(frame, Manager.firstId, Manager.lastId,
                          self.OnComponentCreate)
        wx.EVT_MENU_RANGE(frame, Manager.firstId + ID.SHIFT, Manager.lastId + ID.SHIFT,
                          self.OnComponentReplace)

        # Other events
        frame.Bind(wx.EVT_IDLE, self.OnIdle)
        frame.Bind(wx.EVT_CLOSE, self.OnCloseWindow)
#        wx.EVT_KEY_DOWN(frame, tools.OnKeyDown)
#        wx.EVT_KEY_UP(frame, tools.OnKeyUp)
#        wx.EVT_ICONIZE(frame, self.OnIconize)

        # Menubar events
        # File
        frame.Bind(wx.EVT_MENU, self.OnRecentFile, id=wx.ID_FILE1, id2=wx.ID_FILE9)
        wx.EVT_MENU(frame, wx.ID_NEW, self.OnNew)
        wx.EVT_MENU(frame, wx.ID_OPEN, self.OnOpen)
        wx.EVT_MENU(frame, wx.ID_SAVE, self.OnSaveOrSaveAs)
        wx.EVT_MENU(frame, wx.ID_SAVEAS, self.OnSaveOrSaveAs)
#        wx.EVT_MENU(frame, self.ID_GENERATE_PYTHON, self.OnGeneratePython)
#        wx.EVT_MENU(frame, self.ID_PREFS, self.OnPrefs)
        wx.EVT_MENU(frame, wx.ID_EXIT, self.OnExit)

        # Edit
        wx.EVT_MENU(frame, wx.ID_UNDO, self.OnUndo)
        wx.EVT_MENU(frame, wx.ID_REDO, self.OnRedo)
        wx.EVT_MENU(frame, wx.ID_CUT, self.OnCut)
        wx.EVT_MENU(frame, wx.ID_COPY, self.OnCopy)
        wx.EVT_MENU(frame, wx.ID_PASTE, self.OnPaste)
        wx.EVT_MENU(frame, ID.PASTE_SIBLING, self.OnPasteSibling)
        wx.EVT_MENU(frame, wx.ID_DELETE, self.OnDelete)
        wx.EVT_MENU(frame, frame.ID_TOOL_PASTE, self.OnPaste)
        wx.EVT_MENU(frame, frame.ID_LOCATE, self.OnLocate)
        wx.EVT_MENU(frame, frame.ID_TOOL_LOCATE, self.OnLocate)
        # View
        wx.EVT_MENU(frame, frame.ID_EMBED_PANEL, self.OnEmbedPanel)
        wx.EVT_MENU(frame, frame.ID_SHOW_TOOLS, self.OnShowTools)
        wx.EVT_MENU(frame, frame.ID_TEST, self.OnTest)
        wx.EVT_MENU(frame, frame.ID_REFRESH, self.OnRefresh)
        wx.EVT_MENU(frame, frame.ID_AUTO_REFRESH, self.OnAutoRefresh)
        wx.EVT_MENU(frame, frame.ID_TEST_HIDE, self.OnTestHide)
        wx.EVT_MENU(frame, frame.ID_SHOW_XML, self.OnShowXML)
        # Move
        wx.EVT_MENU(frame, frame.ID_MOVEUP, self.OnMoveUp)
        wx.EVT_MENU(frame, frame.ID_MOVEDOWN, self.OnMoveDown)
        wx.EVT_MENU(frame, frame.ID_MOVELEFT, self.OnMoveLeft)
        wx.EVT_MENU(frame, frame.ID_MOVERIGHT, self.OnMoveRight)        
        # Help
        wx.EVT_MENU(frame, wx.ID_ABOUT, self.OnAbout)
        wx.EVT_MENU(frame, frame.ID_README, self.OnReadme)
        if debug:
            wx.EVT_MENU(frame, frame.ID_DEBUG_CMD, self.OnDebugCMD)

        # Update events
        wx.EVT_UPDATE_UI(frame, wx.ID_SAVE, self.OnUpdateUI)
        wx.EVT_UPDATE_UI(frame, wx.ID_CUT, self.OnUpdateUI)
        wx.EVT_UPDATE_UI(frame, wx.ID_COPY, self.OnUpdateUI)
        wx.EVT_UPDATE_UI(frame, wx.ID_PASTE, self.OnUpdateUI)
        wx.EVT_UPDATE_UI(frame, wx.ID_DELETE, self.OnUpdateUI)
        wx.EVT_UPDATE_UI(frame, frame.ID_LOCATE, self.OnUpdateUI)
        wx.EVT_UPDATE_UI(frame, frame.ID_TOOL_LOCATE, self.OnUpdateUI)
        wx.EVT_UPDATE_UI(frame, frame.ID_TOOL_PASTE, self.OnUpdateUI)
        wx.EVT_UPDATE_UI(frame, wx.ID_UNDO, self.OnUpdateUI)
        wx.EVT_UPDATE_UI(frame, wx.ID_REDO, self.OnUpdateUI)
        wx.EVT_UPDATE_UI(frame, frame.ID_TEST, self.OnUpdateUI)
        wx.EVT_UPDATE_UI(frame, frame.ID_MOVEUP, self.OnUpdateUI)
        wx.EVT_UPDATE_UI(frame, frame.ID_MOVEDOWN, self.OnUpdateUI)
        wx.EVT_UPDATE_UI(frame, frame.ID_MOVELEFT, self.OnUpdateUI)
        wx.EVT_UPDATE_UI(frame, frame.ID_MOVERIGHT, self.OnUpdateUI)
        wx.EVT_UPDATE_UI(frame, frame.ID_REFRESH, self.OnUpdateUI)
        wx.EVT_UPDATE_UI(frame, frame.ID_SHOW_XML, self.OnUpdateUI)

        wx.EVT_MENU(frame, ID.COLLAPSE, self.OnCollapse)
        wx.EVT_MENU(frame, ID.EXPAND, self.OnExpand)

        wx.EVT_UPDATE_UI(frame, ID.COLLAPSE, self.OnUpdateUI)
        wx.EVT_UPDATE_UI(frame, ID.EXPAND, self.OnUpdateUI)

        # XMLTree events
        # Register events
        tree.Bind(wx.EVT_LEFT_DOWN, self.OnTreeLeftDown)
        tree.Bind(wx.EVT_RIGHT_DOWN, self.OnTreeRightDown)
        tree.Bind(wx.EVT_TREE_SEL_CHANGING, self.OnTreeSelChanging)
        tree.Bind(wx.EVT_TREE_SEL_CHANGED, self.OnTreeSelChanged)
        tree.Bind(wx.EVT_TREE_ITEM_COLLAPSED, self.OnTreeItemCollapsed)

        # Panel events
        panel.nb.Bind(wx.EVT_NOTEBOOK_PAGE_CHANGING, self.OnPanelPageChanging)
        panel.nb.Bind(wx.EVT_NOTEBOOK_PAGE_CHANGED, self.OnPanelPageChanged)

        wx.EVT_MENU_HIGHLIGHT_ALL(self.frame, self.OnMenuHighlight)

    def OnComponentCreate(self, evt):
        '''Hadnler for creating new elements.'''
        comp = Manager.findById(evt.GetId())
        g.undoMan.RegisterUndo(undo.UndoGlobal()) # !!! TODO
        Presenter.create(comp)

    def OnComponentReplace(self, evt):
        '''Hadnler for creating new elements.'''
        comp = Manager.findById(evt.GetId() - ID.SHIFT)
        g.undoMan.RegisterUndo(undo.UndoGlobal()) # !!! TODO
        Presenter.replace(comp)

    def OnNew(self, evt):
        '''wx.ID_NEW hadndler.'''
        if not self.AskSave(): return
        Presenter.init()

    def OnOpen(self, evt):
        '''wx.ID_OPEN handler.'''
        if not self.AskSave(): return
        dlg = wx.FileDialog(self.frame, 'Open', os.path.dirname(Presenter.path),
                           '', '*.xrc', wx.OPEN | wx.CHANGE_DIR)
        if dlg.ShowModal() == wx.ID_OK:
            # Not we will really try to load
            # ...but first clear the undo data
            g.undoMan.Clear()
            path = dlg.GetPath()
            self.frame.SetStatusText('Loading...')
            wx.BeginBusyCursor()
            try:
                if Presenter.open(path):
                    self.frame.SetStatusText('Data loaded')
                    self.SaveRecent(path)
                else:
                    self.frame.SetStatusText('Failed')
            finally:
                wx.EndBusyCursor()
        dlg.Destroy()

    def OnRecentFile(self, evt):
        '''wx.ID_FILE<n> handler.'''
        if not self.AskSave(): return
        wx.BeginBusyCursor()

        # get the pathname based on the menu ID
        fileNum = evt.GetId() - wx.ID_FILE1
        path = g.fileHistory.GetHistoryFile(fileNum)
            
        if Presenter.open(path):
            self.frame.SetStatusText('Data loaded')
            # add it back to the history so it will be moved up the list
            self.SaveRecent(path)
        else:
            self.frame.SetStatusText('Failed')

        wx.EndBusyCursor()

    def OnSaveOrSaveAs(self, evt):
        '''wx.ID_SAVE and wx.ID_SAVEAS handler'''
        path = Presenter.path
        if evt.GetId() == wx.ID_SAVEAS or not path:
            dirname = os.path.abspath(os.path.dirname(path))
            dlg = wx.FileDialog(self.frame, 'Save As', dirname, '', '*.xrc',
                               wx.SAVE | wx.OVERWRITE_PROMPT | wx.CHANGE_DIR)
            if dlg.ShowModal() == wx.ID_OK:
                path = dlg.GetPath()
                if isinstance(path, unicode):
                    path = path.encode(sys.getfilesystemencoding())
                dlg.Destroy()
            else:
                dlg.Destroy()
                return

            if g.conf.localconf:
                # if we already have a localconf then it needs to be
                # copied to a new config with the new name
                lc = g.conf.localconf
                nc = Presenter.createLocalConf(path)
                flag, key, idx = lc.GetFirstEntry()
                while flag:
                    nc.Write(key, lc.Read(key))
                    flag, key, idx = lc.GetNextEntry(idx)
                g.conf.localconf = nc
            else:
                # otherwise create a new one
                g.conf.localconf = Presenter.createLocalConf(path)
        self.frame.SetStatusText('Saving...')
        wx.BeginBusyCursor()
        try:
            try:
                Presenter.save(path) # save temporary file first
                if g.conf.localconf.ReadBool("autogenerate", False):
                    pypath = g.conf.localconf.Read("filename")
                    embed = g.conf.localconf.ReadBool("embedResource", False)
                    genGettext = g.conf.localconf.ReadBool("genGettext", False)
                    self.GeneratePython(path, pypath, embed, genGettext)
                    
                self.frame.SetStatusText('Data saved')
                self.SaveRecent(path)
            except IOError:
                self.frame.SetStatusText('Failed')
        finally:
            wx.EndBusyCursor()        

    def OnExit(self, evt):
        '''wx.ID_EXIT handler'''
        self.frame.Close()
        
    def SaveRecent(self, path):
        '''Append path to recently used files.'''
        g.fileHistory.AddFileToHistory(path)

    def AskSave(self):
        '''Show confirmation dialog.'''
        if not Presenter.modified: return True
        flags = wx.ICON_EXCLAMATION | wx.YES_NO | wx.CANCEL | wx.CENTRE
        dlg = wx.MessageDialog(self.frame, 'File is modified. Save before exit?',
                               'Save before too late?', flags)
        say = dlg.ShowModal()
        dlg.Destroy()
        wx.Yield()
        if say == wx.ID_YES:
            self.OnSaveOrSaveAs(wx.CommandEvent(wx.ID_SAVE))
            # If save was successful, modified flag is unset
            if not Presenter.modified: return True
        elif say == wx.ID_NO:
            Presenter.setModified(False)
            return True
        return False

    def OnCloseWindow(self, evt):
        '''wx.EVT_CLOSE handler'''
        if not self.AskSave(): return
        if view.testWin.object: view.testWin.Destroy()
        if not self.frame.IsIconized():
            g.conf.x, g.conf.y = self.frame.GetPosition()
            if wx.Platform == '__WXMAC__':
                g.conf.width, g.conf.height = self.frame.GetClientSize()
            else:
                g.conf.width, g.conf.height = self.frame.GetSize()
#            if conf.embedPanel:
#                conf.sashPos = self.splitter.GetSashPosition()
#            else:
#                conf.panelX, conf.panelY = self.miniframe.GetPosition()
#                conf.panelWidth, conf.panelHeight = self.miniframe.GetSize()
        evt.Skip()

    def OnUndo(self, evt):
        if g.undoMan.CanUndo():
            g.undoMan.Undo()

    def OnRedo(self, evt):
        if g.undoMan.CanRedo():
            g.undoMan.Redo()

    def OnCut(self, evt):
        '''wx.ID_CUT handler.'''
        g.undoMan.RegisterUndo(undo.UndoGlobal()) # !!! TODO
        Presenter.cut()

    def OnDelete(self, evt):
        '''wx.ID_DELETE handler.'''
        if len(self.tree.GetSelections()) == 1:
            item = self.tree.GetSelection()
            index = self.tree.ItemFullIndex(item)
            node = Presenter.delete(self.tree.GetSelection())
            g.undoMan.RegisterUndo(undo.UndoCutDelete(index, node))
        else:
            g.undoMan.RegisterUndo(undo.UndoGlobal())
            Presenter.deleteMany(self.tree.GetSelections())

    def OnCopy(self, evt):
        '''wx.ID_COPY handler.'''
        Presenter.copy()

    def OnPaste(self, evt):
        '''wx.ID_PASTE handler.'''
        g.undoMan.RegisterUndo(undo.UndoGlobal()) # !!! TODO
        Presenter.paste()

    def OnPasteSibling(self, evt):
        '''ID.PASTE_SIBLING handler.'''
        g.undoMan.RegisterUndo(undo.UndoGlobal()) # !!! TODO
        Presenter.paste()

    def ItemsAreCompatible(self, parent, child):
        raise NotImplementedError

    def OnMoveUp(self, evt):
        raise NotImplementedError

    def OnMoveDown(self, evt):
        raise NotImplementedError
    
    def OnMoveLeft(self, evt):
        raise NotImplementedError

    def OnMoveRight(self, evt):
        raise NotImplementedError

    def OnLocate(self, evt):
        raise NotImplementedError

    def OnRefresh(self, evt):
        raise NotImplementedError

    def OnAutoRefresh(self, evt):
        conf.autoRefresh = evt.IsChecked()
        self.menuBar.Check(ID.AUTO_REFRESH, conf.autoRefresh)
        self.tb.ToggleTool(ID.AUTO_REFRESH, conf.autoRefresh)

    def OnAbout(self, evt):
        str = '''\
XRCed version %s

(c) Roman Rolinsky <rollrom@users.sourceforge.net>
Homepage: http://xrced.sourceforge.net\
''' % version
        dlg = wx.MessageDialog(self.frame, str, 'About XRCed', wx.OK | wx.CENTRE)
        dlg.ShowModal()
        dlg.Destroy()

    def OnReadme(self, evt):
        text = open(os.path.join(g.basePath, 'README.txt'), 'r').read()
        dlg = view.ScrolledMessageDialog(self.frame, text, "XRCed README")
        dlg.ShowModal()
        dlg.Destroy()

    # Simple emulation of python command line
    def OnDebugCMD(self, evt):
        while 1:
            try:
                exec raw_input('C:\> ')
            except EOFError:
                print '^D'
                break
            except:
                import traceback
                (etype, value, tb) =sys.exc_info()
                tblist =traceback.extract_tb(tb)[1:]
                msg =' '.join(traceback.format_exception_only(etype, value)
                        +traceback.format_list(tblist))
                print msg


    def OnEmbedPanel(self, evt):
        self.frame.EmbedUnembed(evt.IsChecked())

    def OnShowTools(self, evt):
        raise NotImplementedError # !!!

        conf.showTools = evt.IsChecked()
        g.tools.Show(conf.showTools)
        if conf.showTools:
            self.toolsSizer.Prepend(g.tools, 0, wx.EXPAND)
        else:
            self.toolsSizer.Remove(g.tools)
        self.toolsSizer.Layout()
        
    def OnTest(self, evt):
        if not self.tree.GetSelection(): return
        object = Presenter.createTestWin(self.tree.GetSelection())
        if object:
            frame = view.testWin.GetFrame()
            frame.Bind(wx.EVT_CLOSE, self.OnCloseTestWin)
            frame.Bind(wx.EVT_SIZE, self.OnSizeTestWin)

    def OnCloseTestWin(self, evt):
        Presenter.closeTestWin()

    def OnSizeTestWin(self, evt):
        print 'OnSizeTestWin'
        evt.Skip()

    def OnTestHide(self, evt):
        Presenter.closeTestWin()

    def OnShowXML(self, evt):
        Presenter.showXML()

    def OnMenuHighlight(self, evt):
        menuId = evt.GetMenuId()
        if menuId != -1:
            menu = evt.GetEventObject()
            try:
                help = menu.GetHelpString(menuId)
                if menuId == wx.ID_UNDO:
                    help += ' ' + g.undoMan.GetUndoLabel()
                elif menuId == wx.ID_REDO:
                    help += ' ' + g.undoMan.GetRedoLabel()
                self.frame.SetStatusText(help)
            except:
                self.frame.SetStatusText('')
        else:
            self.frame.SetStatusText('')

    def OnUpdateUI(self, evt):
        if self.inUpdateUI: return          # Recursive call protection
        self.inUpdateUI = True
        if evt.GetId() in [wx.ID_CUT, wx.ID_COPY, wx.ID_DELETE]:
            evt.Enable(bool(self.tree.GetSelection()))
        elif evt.GetId() == wx.ID_SAVE:
            evt.Enable(Presenter.modified)
        elif evt.GetId() in [self.frame.ID_SHOW_XML]:
            evt.Enable(len(self.tree.GetSelections()) == 1)
        elif evt.GetId() in [wx.ID_PASTE, self.frame.ID_TOOL_PASTE]:
            evt.Enable(self.clipboardHasData)
# !!! Does not work on wxGTK
#             enabled = False
#             if not wx.TheClipboard.IsOpened() and wx.TheClipboard.Open():
#                 data = wx.CustomDataObject('XRCED_elem')
#                 if wx.TheClipboard.IsSupported(data.GetFormat()):
#                     enabled = True
#                 else:
#                     data = wx.CustomDataObject('XRCED_node')
#                     if wx.TheClipboard.IsSupported(data.GetFormat()):
#                         enabled = True
#                 wx.TheClipboard.Close()
#             evt.Enable(enabled)
        elif evt.GetId() in [self.frame.ID_TEST,
                             self.frame.ID_MOVEUP, self.frame.ID_MOVEDOWN,
                             self.frame.ID_MOVELEFT, self.frame.ID_MOVERIGHT]:
            evt.Enable(bool(self.tree.GetSelection()))
        elif evt.GetId() in [self.frame.ID_LOCATE, self.frame.ID_TOOL_LOCATE,
                             self.frame.ID_REFRESH]:
            evt.Enable(view.testWin.IsShown())
        elif evt.GetId() == wx.ID_UNDO:  evt.Enable(g.undoMan.CanUndo())
        elif evt.GetId() == wx.ID_REDO:  evt.Enable(g.undoMan.CanRedo())
        elif evt.GetId() in [ID.COLLAPSE, ID.EXPAND]:
            evt.Enable(not self.tree.GetSelection() or
                       len(self.tree.GetSelections()) == 1 and \
                           self.tree.ItemHasChildren(self.tree.GetSelection()))
        self.inUpdateUI = False

    def OnIdle(self, evt):
#        print 'onidle',self.inIdle
        if self.inIdle: return          # Recursive call protection
        self.inIdle = True
        if not Presenter.applied:
            item = self.tree.GetSelection()
            if item: Presenter.update(item)

        # Check clipboard
        self.clipboardHasData = True
#        self.clipboardHasData = False
#         if not wx.TheClipboard.IsOpened() and wx.TheClipboard.Open():
#             data = wx.CustomDataObject('XRCED_elem')
#             if wx.TheClipboard.IsSupported(data.GetFormat()):
#                 self.clipboardHasData = True
#             else:
#                 data = wx.CustomDataObject('XRCED_node')
#                 if wx.TheClipboard.IsSupported(data.GetFormat()):
#                     self.clipboardHasData = True
#             wx.TheClipboard.Close()

        self.inIdle = False
        return

        try:
            if tree.needUpdate:
                if conf.autoRefresh:
                    if g.testWin:
                        #self.SetStatusText('Refreshing test window...')
                        # (re)create
                        tree.CreateTestWin(g.testWin.item)
                        #self.SetStatusText('')
                    tree.needUpdate = False
            elif tree.pendingHighLight:
                try:
                    tree.HighLight(tree.pendingHighLight)
                except:
                    # Remove highlight if any problem
                    if g.testWin and g.testWin.highLight:
                        g.testWin.highLight.Remove()
                    tree.pendingHighLight = None
                    raise
            else:
                evt.Skip()
        finally:
            self.inIdle = False

    def OnIconize(self, evt):
        raise NotImplementedError # !!!

        if evt.Iconized():
            conf.x, conf.y = self.GetPosition()
            conf.width, conf.height = self.GetSize()
            if conf.embedPanel:
                conf.sashPos = self.splitter.GetSashPosition()
            else:
                conf.panelX, conf.panelY = self.miniFrame.GetPosition()
                conf.panelWidth, conf.panelHeight = self.miniFrame.GetSize()
                self.miniFrame.Show(False)
        else:
            if not conf.embedPanel:
                self.miniFrame.Show(True)
        evt.Skip()

    # Expand/collapse subtree
    def OnExpand(self, evt):
        if self.tree.GetSelection(): 
            map(self.tree.ExpandAllChildren, self.tree.GetSelections())
        else: 
            self.tree.ExpandAll()

    def OnCollapse(self, evt):
        if self.tree.GetSelection(): 
            map(self.tree.CollapseAllChildren, self.tree.GetSelections())
        else: 
            self.tree.CollapseAll()

    #
    # XMLTree event handlers
    #
    
    def OnTreeLeftDown(self, evt):
        pt = evt.GetPosition();
        item, flags = self.tree.HitTest(pt)
        if flags & wx.TREE_HITTEST_NOWHERE or not item:
            # Unselecting seems to be broken on wxGTK!!!
            Presenter.unselect()
        evt.Skip()

    def OnTreeRightDown(self, evt):
        forceSibling = evt.ControlDown()
        forceInsert = evt.ShiftDown()
        Presenter.popupMenu(forceSibling, forceInsert, evt.GetPosition())

    def OnTreeSelChanging(self, evt):
        # Permit multiple selection for same level only
        state = wx.GetMouseState()
        oldItem = evt.GetOldItem()
        if oldItem and (state.ShiftDown() or state.ControlDown()) and \
           self.tree.GetItemParent(oldItem) != self.tree.GetItemParent(evt.GetItem()):
            evt.Veto()
            self.frame.SetStatusText('Veto selection (not same level)')
            return
        # If panel has a pending undo, register it
        if Presenter.panelIsDirty():
            g.undoMan.RegisterUndo(self.panel.undo)
            self.panel.undo = None
        evt.Skip()

    def OnTreeSelChanged(self, evt):
        if evt.GetOldItem():
            if not Presenter.applied:
                Presenter.update(evt.GetOldItem())
        # Tell presenter to update current data and view
        Presenter.setData(evt.GetItem())
        # Set initial sibling/insert modes
        Presenter.createSibling = not Presenter.comp.isContainer()
        Presenter.insertBefore = False
        evt.Skip()

    def OnTreeItemCollapsed(self, evt):
        # If no selection, reset panel
        if not self.tree.GetSelection():
            if not Presenter.applied: Presenter.update()
            Presenter.setData(None)
        evt.Skip()

    def OnPanelPageChanging(self, evt):
        TRACE('OnPanelPageChanging: %d %d', evt.GetOldSelection(), evt.GetSelection())
        # Register undo if something was changed
        i = evt.GetOldSelection()
#        import pdb;pdb.set_trace()
        if i >= 0 and Presenter.panelIsDirty():
            g.undoMan.RegisterUndo(self.panel.undo)
        evt.Skip()

    def OnPanelPageChanged(self, evt):
        TRACE('OnPanelPageChanged: %d %d', evt.GetOldSelection(), evt.GetSelection())
        # Register new undo 
        Presenter.createUndoEdit(page=evt.GetSelection())
        evt.Skip()

# Singleton class
Listener = _Listener()
