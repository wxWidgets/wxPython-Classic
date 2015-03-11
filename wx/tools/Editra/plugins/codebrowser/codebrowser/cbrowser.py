###############################################################################
# Name: cbrowser.py                                                           #
# Purpose: CodeBrowser UI                                                     #
# Author: Cody Precord <cprecord@editra.org>                                  #
# Copyright: (c) 2008 Cody Precord <staff@editra.org>                         #
# License: wxWindows License                                                  #
###############################################################################

"""
FILE: cbrowser.py
AUTHOR: Cody Precord
LANGUAGE: Python
SUMMARY:
    CodeBrowser UI, displays the DocStruct object returned by the L{gentag} lib
as a tree. Clicking on the elements in the tree will navigate to where the
element is defined in the file.

"""

__author__ = "Cody Precord <cprecord@editra.org>"
__svnid__ = "$Id$"
__revision__ = "$Revision$"

#--------------------------------------------------------------------------#
# Imports
import StringIO
import wx

# Editra Libraries
import ed_glob
import ebmlib
from profiler import Profile_Get, Profile_Set
import ed_msg
import ed_thread

# Local Imports
import cbconfig
import gentag.taglib as taglib
from tagload import TagLoader
import IconFile

#--------------------------------------------------------------------------#
# Globals
ID_CODEBROWSER = wx.NewId()
ID_BROWSER = wx.NewId()
ID_GOTO_ELEMENT = wx.NewId()
PANE_NAME = u"CodeBrowser"
MSG_CODEBROWSER_MENU = ("CodeBrowser", "ContextMenu")
_ = wx.GetTranslation

# HACK for i18n scripts to pick up translation strings
STRINGS = ( _("Class Definitions"), _("Defines"), _("Function Definitions"),
            _("Global Variables"), _("Identities"), _("Labels"), _("Macros"),
            _("Macro Definitions"), _("Namespaces"), _("Packages"),
            _("Procedure Definitions"), _("Programs"), _("Protocols"),
            _("Sections"), _("Style Tags"), _("Subroutines"),
            _("Subroutine Declarations"), _("Task Definitions"), 
            _("Modules"), _("Functions"), _("Public Functions"),
            _("Public Subroutines"), _("Imports"), _("Elements") )
del STRINGS

#--------------------------------------------------------------------------#

class CodeBrowserTree(wx.TreeCtrl):
    def __init__(self, parent, id=ID_BROWSER,
                 pos=wx.DefaultPosition, size=wx.DefaultSize,
                 style=wx.TR_DEFAULT_STYLE|wx.TR_HIDE_ROOT):
        super(CodeBrowserTree, self).__init__(parent, id, pos, size, style)

        # Attributes
        self._log = wx.GetApp().GetLog()
        self._mw = parent
        self._menu = ebmlib.ContextMenuManager()
        self._selected = None
        self._cjob = 0
        self._lastjob = u'' # Name of file in last sent out job
        self._cdoc = None   # Current DocStruct
        self.icons = dict()
        self.il = None

        # struct used in buffer-tree sync
        self._ds_flat = list() # list of tuples - [(line, item_id),(line, item_id)...]

        self._timer = wx.Timer(self)
        self._sync_timer = wx.Timer(self)
        self._cpage = None
        self._force = False

        # Setup
        self._SetupImageList()
        viewm = self._mw.GetMenuBar().GetMenuByName("view")
        self._mi = viewm.InsertAlpha(ID_CODEBROWSER, _("Code Browser"), 
                                     _("Open Code Browser Sidepanel"),
                                     wx.ITEM_CHECK,
                                     after=ed_glob.ID_PRE_MARK)

        self.root = self.AddRoot('CodeBrowser')
        self.SetPyData(self.root, None)
        self.SetItemImage(self.root, self.icons['class'])
        self.nodes = dict(globals=None, classes=None, funct=None)

        # Event Handlers
        self.Bind(wx.EVT_TREE_ITEM_ACTIVATED, self.OnActivated)
        self.Bind(wx.EVT_TREE_ITEM_RIGHT_CLICK, self.OnContext)
        self.Bind(wx.EVT_TREE_ITEM_EXPANDED, self.OnExpanding)
        self.Bind(wx.EVT_MENU, self.OnMenu)
        self.Bind(wx.EVT_TIMER, self.OnStartJob, self._timer)
        self.Bind(wx.EVT_TIMER, lambda evt: self._SyncTree(), self._sync_timer)
        self.Bind(wx.EVT_WINDOW_DESTROY, self.OnDestroy)
        self.Bind(EVT_JOB_FINISHED, self.OnTagsReady)

        # Editra Message Handlers
        ed_msg.Subscribe(self.OnThemeChange, ed_msg.EDMSG_THEME_CHANGED)
        ed_msg.Subscribe(self.OnUpdateTree, ed_msg.EDMSG_UI_NB_CHANGED)
        ed_msg.Subscribe(self.OnUpdateTree, ed_msg.EDMSG_FILE_OPENED)
        ed_msg.Subscribe(self.OnUpdateTree, ed_msg.EDMSG_FILE_SAVED)
        ed_msg.Subscribe(self.OnSyncTree, ed_msg.EDMSG_UI_STC_POS_CHANGED)
        ed_msg.Subscribe(self.OnEditorRestore, ed_msg.EDMSG_UI_STC_RESTORE)
        ed_msg.Subscribe(self.OnBrowserCfg,
                         ed_msg.EDMSG_PROFILE_CHANGE + (cbconfig.CB_PROFILE_KEY,))

        # Backwards compatibility
        if hasattr(ed_msg, 'EDMSG_UI_STC_LEXER') and \
           hasattr(ed_msg, 'EDMSG_DSP_FONT'):
            ed_msg.Subscribe(self.OnUpdateFont, ed_msg.EDMSG_DSP_FONT)
            ed_msg.Subscribe(self.OnUpdateTree, ed_msg.EDMSG_UI_STC_LEXER)

    def OnDestroy(self, event):
        """Unsubscribe from messages on destroy"""
        if self:
            self._menu.Clear()
            ed_msg.Unsubscribe(self.OnUpdateTree)
            ed_msg.Unsubscribe(self.OnThemeChange)
            ed_msg.Unsubscribe(self.OnUpdateFont)
            ed_msg.Unsubscribe(self.OnSyncTree)
            ed_msg.Unsubscribe(self.OnEditorRestore)

    def _GetCurrentCtrl(self):
        """Get the current buffer"""
        return self._mw.GetNotebook().GetCurrentCtrl()

    def _GetFQN(self, node):
        """Returns fully qualified name of the tree node in the form
        ...grandparent.parent.child
        @param node: node id

        """
        rval=""
        if node and node.IsOk():
            path = [self.GetItemText(node)]
            parent = self.GetItemParent(node)
            root = self.GetRootItem()
            while parent and parent.IsOk() and parent != root:
                path.append(self.GetItemText(parent))
                parent = self.GetItemParent(parent)
            
            # Join path elements and strip line information as this could be changed
            path.reverse()
            rval = '.'.join([p.split(u'[')[0].strip() for p in path])
            
        return rval
    
    def _ClearTree(self):
        """Clear the tree and caches"""
        self._cdoc = None
        self._ds_flat = list()
        self.Unselect() # XXX: workaround focus issue in 2.9
        self.DeleteChildren(self.root)

    def _FindNodeForLine(self, line):
        """Returns node id of the docstruct element given line belongs to
        @param line: line number
        @returns: tree node id

        """
        # HACK This should probably be done with bisect search
        rval = None
        line += 1
        if self._ds_flat:
            for citem in self._ds_flat:
                if citem[0] < line:
                    cline = citem[0]
                    rval = citem[1]
                else:
                    break

#        self._log("[codebrowser][info] For line %d found item %s" % \
#                  (line, self._GetFQN(rval)))
        return rval

    def _SetupImageList(self):
        """Setup the image list for the tree"""
        imglst = wx.ImageList(16, 16)

        globe = wx.ArtProvider.GetBitmap(str(ed_glob.ID_WEB), wx.ART_MENU)
        self.icons['globals'] = imglst.Add(globe)

        bmp = wx.ArtProvider.GetBitmap(str(ed_glob.ID_CLASS_TYPE), wx.ART_MENU)
        self.icons['class'] = imglst.Add(bmp)
        self.icons['section'] = imglst.Add(IconFile.Brick_Add.GetBitmap())
        bmp = wx.ArtProvider.GetBitmap(str(ed_glob.ID_FUNCT_TYPE), wx.ART_MENU)
        self.icons['function'] = imglst.Add(bmp)
        bmp = wx.ArtProvider.GetBitmap(str(ed_glob.ID_METHOD_TYPE), wx.ART_MENU)
        self.icons['method'] = imglst.Add(bmp)
        self.icons['subroutine'] = self.icons['function']
        self.icons['procedure'] = self.icons['function']
        self.icons['task'] = imglst.Add(bmp)
        self.icons['function2'] = self.icons['task']
        bmp = wx.ArtProvider.GetBitmap(str(ed_glob.ID_VARIABLE_TYPE), wx.ART_MENU)
        self.icons['variable'] = imglst.Add(bmp)
        self.icons['namespace'] = imglst.Add(IconFile.Brick_Bricks.GetBitmap())
        self.icons['tag_red'] = imglst.Add(IconFile.Tag_Red.GetBitmap())
        self.icons['tag_blue'] = imglst.Add(IconFile.Tag_Blue.GetBitmap())
        self.icons['tag_green'] = imglst.Add(IconFile.Tag_Green.GetBitmap())
        self.SetImageList(imglst)
        # NOTE: Must save reference to the image list or tree will crash!!!
        self.il = imglst

    def _GetIconIndex(self, cobj):
        """Get the index of an appropriate icon for the given code object
        @param cobj: L{taglib.Code} object
        @return: int

        """
        img = self.icons.get(cobj.type, None)

        # Try and find an appropriate fallback icon
        if img is None:
            if isinstance(cobj, taglib.Function):
                img = self.icons['function']
            elif isinstance(cobj, taglib.Class):
                img = self.icons['class']
            elif isinstance(cobj, taglib.Scope):
                img = self.icons['section']
            else:
                img = self.icons['variable']
        return img

    def _SyncTree(self):
        """Synchronize tree node selection with current position in the text
        """
        if not self._ShouldUpdate():
            return
        line = self._GetCurrentCtrl().GetCurrentLineNum()
        self._log("[codebrowser][info] Syncing tree for position %d" % line)
        scope_item = self._FindNodeForLine(line)
        if scope_item:
            selected = self.GetSelection()
            if selected:
                if selected != scope_item:
                    self.Unselect()
                    self.SelectItem(scope_item)
            else:
                self.SelectItem(scope_item)
                
            self.EnsureVisible(scope_item)

    def _ShouldUpdate(self):
        """Check whether the tree should do an update or not
        @return: bool

        """
        pane = self._mw.GetFrameManager().GetPane(PANE_NAME)
        if self._mw.IsExiting() or not pane.IsShown():
            return False
        else:
            return True

    def AppendClass(self, cobj):
        """Append a class node to the tree
        @param cobj: Class item object

        """
        if self.nodes.get('classes', None) is None:
            desc = self._cdoc.GetElementDescription('class')
            if desc == 'class':
                desc = "Class Definitions"
            croot = self.AppendItem(self.GetRootItem(), _(desc))
            self.SetItemHasChildren(croot)
            self.SetPyData(croot, None)
            self.SetItemImage(croot, self.icons['class'])
            self.nodes['classes'] = croot

        croot = self.AppendCodeObj(self.nodes['classes'], cobj, self.icons['class'])

    def AppendCodeObj(self, node, cobj, img):
        """Append a code object to the given node and set its data
        @param node: node to attach object to
        @param cobj: code object
        @return: tree item id

        """
        item_id = self.AppendItem(node, u"%s [%d]" % (cobj.GetName(), 1 + cobj.GetLine()), img)
        self._ds_flat.append((cobj.GetLine(), item_id))
        self.SetPyData(item_id, cobj.GetLine())
        # If the item is a scope it may have sub items
        if isinstance(cobj, taglib.Scope):
            elements = cobj.GetElements()
            if len(elements):
                self.SetItemHasChildren(item_id)
                for elem in elements: # Ordered list of dict objects
                    for otype in elem[elem.keys()[0]]:
                        if otype is cobj:
                            # attempt to prevent infinite recursion with bad doc trees
                            continue
                        img = self._GetIconIndex(otype)
                        # Make recursive call as Scope's may contain other
                        # Scopes.
                        self.AppendCodeObj(item_id, otype, img)
        return item_id

    def AppendGlobal(self, gobj):
        """Append a global variable/object to the Globals node
        @param gobj: Object derived from Scope

        """
        if self.nodes.get('globals', None) is None:
            desc = self._cdoc.GetElementDescription('variable')
            if desc == 'variable':
                desc = "Global Variables"
            self.nodes['globals']  = self.AppendItem(self.GetRootItem(), _(desc))
            self.SetItemHasChildren(self.nodes['globals'])
            self.SetPyData(self.nodes['globals'], None)
            self.SetItemImage(self.nodes['globals'], self.icons['globals'])

        self.AppendCodeObj(self.nodes['globals'], gobj, self.icons['variable'])

    def AppendElement(self, obj):
        """Append a general code object to the document
        @param obj: Code object

        """
        # Check if there is a node for this Code object
        if self.nodes.get(obj.type, None) is None:
            # Look for a description to use as category title
            if self._cdoc is not None:
                desc = self._cdoc.GetElementDescription(obj.type).title()
            else:
                desc = obj.type.title()

            self.nodes[obj.type] = self.AppendItem(self.GetRootItem(), _(desc),
                                                   self._GetIconIndex(obj))
            self.SetItemHasChildren(self.nodes[obj.type])
            self.SetPyData(self.nodes[obj.type], None)

        self.AppendCodeObj(self.nodes[obj.type], obj, self._GetIconIndex(obj))

    def DeleteChildren(self, item):
        """Delete the children of a given node"""
        super(CodeBrowserTree, self).DeleteChildren(item)
        for key in self.nodes.keys():
            self.nodes[key] = None

    def GetMainWindow(self):
        """Get this panels main window"""
        return self._mw

    def GotoElement(self, tree_id):
        """Navigate the cursor to the element identified in the
        code browser tree.
        @param tree_id: Tree Id

        """
        try:
            line = self.GetPyData(tree_id)
        except wx.PyAssertionError:
            # Ignore unexplainable errors from wx...
            line = None

        if line is not None:
            ctrl = self._mw.GetNotebook().GetCurrentCtrl()
            ctrl.GotoLine(line)

            # Need CallAfter to make the focus work on Windows
            # Otherwise the tree control will reclaim the focus
            wx.CallAfter(ctrl.SetFocus)

    def OnActivated(self, evt):
        """Handle when an item is clicked on
        @param evt: wx.TreeEvent

        """
        tree_id = evt.GetItem()
        if tree_id is not None:
            self.GotoElement(tree_id)

    def OnContext(self, evt):
        """Show the context menu when an item is clicked on"""
        self._menu.Clear()
        self._menu.Menu = wx.Menu()
        tree_id = evt.GetItem()
        data = self.GetPyData(tree_id)
        # Add the Goto menu option
        if data is not None:
            self._menu.SetUserData("object", data)
            self._selected = tree_id # Store the selected
            txt = self.GetItemText(self._selected).split('[')[0].strip()
            self._menu.Menu.Append(ID_GOTO_ELEMENT, _("Goto \"%s\"") % txt)
        # Let clients hook into the context menu
        # Call AddHandler to add a callback handler callback(menu_id, itemdata)
        ed_msg.PostMessage(MSG_CODEBROWSER_MENU, self._menu)
        self.PopupMenu(self._menu.Menu)

    def OnCompareItems(self, item1, item2):
        """Compare two tree items for sorting.
        @param item1: wx.TreeItem
        @param item2: wx.TreeItem
        @return: -1, 0, 1

        """
        sortopt = cbconfig.GetSortOption()
        if sortopt == cbconfig.CB_ALPHA_SORT:
            # Sort items by name
            val1 = self.GetItemText(item1).lower()
            val2 = self.GetItemText(item2).lower()
        else:
            # Sort items by line number
            val1 = self.GetPyData(item1)
            val2 = self.GetPyData(item2)

        if val1 < val2:
            return -1
        elif val1 == val2:
            return 0
        else:
            return 1

    def OnBrowserCfg(self, msg):
        """Profile update message for when CodeBrowser
        configuration is updated.

        """
        # Resort all items
        def SortAllItems(parent):
            item, cookie = self.GetFirstChild(parent)
            while item:
                if self.ItemHasChildren(item):
                    if self.IsExpanded(item):
                        self.SortChildren(item)
                    SortAllItems(item)
                item, cookie = self.GetNextChild(parent, cookie)
        SortAllItems(self.root)

    def OnMenu(self, evt):
        """Handle the context menu events"""
        e_id  = evt.GetId()
        handler = self._menu.GetHandler(e_id)
        if handler:
            data = None
            if self._selected is not None:
                data = self.GetPyData(self._selected)
            handler(e_id, data)
        elif e_id == ID_GOTO_ELEMENT:
            if self._selected is not None:
                self.GotoElement(self._selected)
        else:
            evt.Skip()

    @ed_msg.mwcontext
    def OnEditorRestore(self, msg):
        """Called when editor size is unmaximized"""
        self.OnUpdateTree()

    def OnExpanding(self, evt):
        """Update sorting"""
        item = evt.GetItem()
        self.SortChildren(item)

    def OnThemeChange(self, msg):
        """Update the images when Editra's theme changes
        @param msg: Message Object

        """
        self._SetupImageList()
        self.Refresh()

    def OnTagsReady(self, evt):
        """Processing of tag generation has completed, check results
        and update view.
        @param evt: EVT_JOB_FINISHED

        """
        # Make sure that the values that are being returned are the ones for
        # the currently active buffer.
        if evt.GetId() == self._cjob:
            self._lastjob = u''
            self.Freeze()
            self.UpdateAll(evt.GetValue())
            self.Thaw()
            # Stop busy indicator
            ed_msg.PostMessage(ed_msg.EDMSG_PROGRESS_STATE,
                               (self._mw.GetId(), 0, 0))

            if not self._timer.IsRunning():
                self._cpage = None

    def OnUpdateFont(self, msg):
        """Update the ui font when a message comes saying to do so."""
        font = msg.GetData()
        if isinstance(font, wx.Font) and not font.IsNull():
            self.SetFont(font)

    def OnUpdateMenu(self, evt):
        """UpdateUI handler for the panels menu item, to update the check
        mark.
        @param evt: wx.UpdateUIEvent

        """
        pane = self._mw.GetFrameManager().GetPane(PANE_NAME)
        evt.Check(pane.IsShown())

    @ed_msg.mwcontext
    def OnSyncTree(self, msg):
        """Handler for tree synchronization.
        Uses a one shot timer to optimize multiple fast caret movement events.

        """
        if not self._ShouldUpdate():
            return # If panel is not visible don't update
        
        if self._sync_timer.IsRunning():
            self._sync_timer.Stop()
        
        #One shot timer for tree sync
        self._sync_timer.Start(300, True)

    def OnStartJob(self, evt):
        """Start the tree update job
        
        @param evt: wxTimerEvent

        """
        if self._cpage is None or not isinstance(self._cpage, wx.Window):
            self._cpage = None
            return
        else:
            # Check if its still the current page
            parent = self._cpage.GetParent()
            if self._cpage != parent.GetCurrentPage():
                return

        # Get the generator method
        genfun = TagLoader.GetGenerator(self._cpage.GetLangId())
        self._cjob += 1 # increment job Id

        # Check if we need to do updates
        if genfun is not None and (self._force or self._ShouldUpdate()):
            self._force = False

            # Start progress indicator in pulse mode
            ed_msg.PostMessage(ed_msg.EDMSG_PROGRESS_SHOW,
                               (self._mw.GetId(), True))
            ed_msg.PostMessage(ed_msg.EDMSG_PROGRESS_STATE,
                               (self._mw.GetId(), -1, -1))

            # Create and start the worker thread
            task = TagGenJob(self, self._cjob, genfun,
                             StringIO.StringIO(self._cpage.GetText()))
            ed_thread.EdThreadPool().QueueJob(task.DoTask)
        else:
            self._ClearTree()
            ed_msg.PostMessage(ed_msg.EDMSG_PROGRESS_SHOW,
                               (self._mw.GetId(), False))
            return

    def OnUpdateTree(self, msg=None, force=False):
        """Update the tree when an action message is sent
        @keyword msg: Message Object
        @keyword force: Force update

        """
        # Check for if update should be skipped
        if not force:
            context = None
            if msg is not None:
                context = msg.GetContext()

            if context is not None and context != self._mw.GetId():
                return
        
        # Don't update if panel is not visible
        if not self._ShouldUpdate():
            return

        page = self._GetCurrentCtrl()
        cfname = page.GetFileName()

        # If its a blank document just clear out
        if not len(cfname):
            self._ClearTree()
            return

        # If document job is same as current don't start a new one
        if force or self._lastjob != cfname:
            self._lastjob = cfname
            if self._timer.IsRunning():
                self._timer.Stop()

            # Cache the current job information
            self._cpage = page
            self._force = force

            # Start the oneshot timer for beginning the tag generator job
            self._timer.Start(300, True)
    
    def OnShowAUIPane(self):
        """Interface method that the main Editra window will call
        When its auimanager does a Show when this window is contained
        within an aui pane. Forces the tree to update.

        """
        self.OnUpdateTree(force=True)

    def OnShowBrowser(self, evt):
        """Show the browser pane
        @param evt: wx.MenuEvent

        """
        if evt.GetId() == ID_CODEBROWSER:
            mgr = self._mw.GetFrameManager()
            pane = mgr.GetPane(PANE_NAME)
            pane.Show(not pane.IsShown())
            mgr.Update()
            self.OnShowAUIPane()
        else:
            evt.Skip()

    def UpdateAll(self, tags):
        """Update the entire tree
        @param tags: DocStruct object

        """
        self._ClearTree()
        self._cdoc = tags
        # Check and add any common types in the document first

        # Global Variables
        for var in tags.GetVariables():
            self.AppendGlobal(var)

        # Class Definitions
        for cls in tags.GetClasses():
            self.AppendClass(cls)

        # Check for any remaining custom types of code objects to add
        for element in tags.GetElements():
            for elem in element.values():
                if element.keys()[0] not in ['class', 'variable']:
                    for item in elem:
                        self.AppendElement(item)

        # Expand all main nodes except the one for global variables
        for node in [ node for node in self.nodes.values()
                      if node is not None and node != self.nodes['globals']]:
            self.Expand(node)
        
        self._ds_flat.sort(cmp=lambda x,y: cmp(x[0],y[0]))
        self._SyncTree()

#--------------------------------------------------------------------------#
# Tag Generator
class TagGenJob(object):
    """Thread for running tag parser on and returning the results for
    display in the tree.

    """
    def __init__(self, reciever, job_id, genfun, buff):
        """Create the thread object
        @param reciever: Window to recieve result
        @param job_id: id of this job
        @param genfun: tag generator function
        @param buff: string buffer to pass to genfun

        """
        super(TagGenJob, self).__init__()

        # Attributes
        self.reciever = reciever
        self.job = job_id
        self.buff = buff
        self.task = genfun

    def DoTask(self):
        """Run the generator function and return the docstruct to
        the main thread.

        """
        tags = self.task(self.buff)
        evt = TagGenEvent(edEVT_JOB_FINISHED, self.job, tags)
        wx.CallAfter(wx.PostEvent, self.reciever, evt)
        
#--------------------------------------------------------------------------#
# Tag Generator Thread Event(s)

edEVT_JOB_FINISHED = wx.NewEventType()
EVT_JOB_FINISHED = wx.PyEventBinder(edEVT_JOB_FINISHED, 1)

class TagGenEvent(wx.PyCommandEvent):
    """Event to signal when a tag generation job is complete.
    The event id is the job number and the value is the DocStruct
    created by the tag generator

    """
    def __init__(self, etype, eid, value=taglib.DocStruct()):
        """Creates the event object"""
        super(TagGenEvent, self).__init__(etype, eid)
        self._value = value

    def GetValue(self):
        """Returns the value from the event.
        @return: the value of this event

        """
        return self._value
