# -*- coding: utf-8 -*-
###############################################################################
# Name: browser.py                                                            #
# Purpose: UI portion of the FileBrowser Plugin                               #
# Author: Cody Precord <cprecord@editra.org>                                  #
# Copyright: (c) 2008-2013 Cody Precord <staff@editra.org>                    #
# License: wxWindows License                                                  #
###############################################################################

"""
Provides a file browser panel and other UI components for Editra's
FileBrowser Plugin.

"""

__author__ = "Cody Precord <cprecord@editra.org>"
__svnid__ = "$Id$"
__revision__ = "$Revision$"

#-----------------------------------------------------------------------------#
# Imports
import os
import sys
import fnmatch
import time
import stat
import zipfile
import shutil
import subprocess
import wx

# Editra Library Modules
import ed_glob
import ed_msg
import ed_menu
import ed_mdlg
import syntax.synglob as synglob
import syntax.syntax as syntax
import util as util
import ed_thread
import eclib
import ebmlib
import ed_basewin

# Local Modules
import filebrowser.fbcfg as fbcfg

#-----------------------------------------------------------------------------#
# Globals
PANE_NAME = u'FileBrowser'
ID_FILEBROWSE = wx.NewId()

# Configure Platform specific commands
FILEMAN_CMD = util.GetFileManagerCmd()
if wx.Platform == '__WXMAC__':
    FILEMAN = 'Finder'
elif wx.Platform == '__WXMSW__':
    FILEMAN = 'Explorer'
else: # Other/Linux
    FILEMAN = FILEMAN_CMD.title()

def TrashString():
    """Get the trash description string"""
    if wx.Platform == '__WXMSW__':
        return _("Move to Recycle Bin")
    else:
        return _("Move to Trash")

def refreshAfter(func):
    """Do a file refresh after call. Helper decorator for
    FileBrowser2 class

    """
    def callRefresh(*args, **kwds):
      rval = func(*args, **kwds)
      args[0].RefreshView()
      return rval

    callRefresh.__name__ = func.__name__
    callRefresh.__doc__ = func.__doc__
    return callRefresh

_ = wx.GetTranslation
#-----------------------------------------------------------------------------#

ID_MARK_PATH = wx.NewId()
ID_OPEN_MARK = wx.NewId()
ID_REMOVE_MARK = wx.NewId()

class BrowserMenuBar(eclib.ControlBar):
    """Creates a menubar with """
    def __init__(self, parent):
        super(BrowserMenuBar, self).__init__(parent,
                                             style=eclib.CTRLBAR_STYLE_GRADIENT)

        if wx.Platform == '__WXGTK__':
            self.SetWindowStyle(eclib.CTRLBAR_STYLE_DEFAULT)

        # Attributes
        self._saved = ed_menu.EdMenu()
        self._rmpath = ed_menu.EdMenu()
        self._ids = list()  # List of ids of menu items
        self._rids = list() # List of remove menu item ids

        # Build Menus
        menu = ed_menu.EdMenu()
        menu.Append(ID_MARK_PATH, _("Save Selected Paths"))
        menu.AppendMenu(ID_OPEN_MARK, _("Jump to Saved Path"), self._saved)
        menu.AppendSeparator()
        menu.AppendMenu(ID_REMOVE_MARK, _("Remove Saved Path"), self._rmpath)

        # Button
        bmp = wx.ArtProvider.GetBitmap(str(ed_glob.ID_PREF), wx.ART_MENU)
        self.prefb = eclib.PlateButton(self, bmp=bmp,
                                       style=eclib.PB_STYLE_NOBG)
        bmp = wx.ArtProvider.GetBitmap(str(ed_glob.ID_ADD_BM), wx.ART_MENU)
        self.menub = eclib.PlateButton(self, bmp=bmp,
                                       style=eclib.PB_STYLE_NOBG)
        self.menub.SetToolTipString(_("Pathmarks"))
        self.menub.SetMenu(menu)

        # Layout bar
        self.AddControl(self.prefb, wx.ALIGN_LEFT)
        self.AddControl(self.menub, wx.ALIGN_LEFT)

        # Event Handlers
        ed_msg.Subscribe(self.OnThemeChanged, ed_msg.EDMSG_THEME_CHANGED)
        self.Bind(wx.EVT_BUTTON, self.OnPref, self.prefb)
        self.Bind(wx.EVT_BUTTON, lambda evt: self.menub.ShowMenu(), self.menub)
        self.Bind(wx.EVT_WINDOW_DESTROY, self.OnDestroy, self)

    SavedMenu = property(lambda self: self._saved)
    RemoveMenu = property(lambda self: self._rmpath)

    def OnDestroy(self, evt):
        """Unsubscribe from messages"""
        if self:
            ed_msg.Unsubscribe(self.OnThemeChanged)

    def OnPref(self, evt):
        """Show the preferences dialog"""
        dlg = fbcfg.FBConfigDlg(self.TopLevelParent)
        dlg.ShowModal()
        dlg.Destroy()

    # XXX maybe change to list the more recently added items near the top
    def AddItem(self, label):
        """Add an item to the saved list, this also adds an identical 
        entry to the remove list so it can be removed if need be.

        """
        save_id = wx.NewId()
        self._ids.append(save_id)
        rem_id = wx.NewId()
        self._rids.append(rem_id)
        self._saved.Append(save_id, label)
        self._rmpath.Append(rem_id, label)

    def GetOpenIds(self):
        """Returns the ordered list of menu item ids"""
        return self._ids

    def GetRemoveIds(self):
        """Returns the ordered list of remove menu item ids"""
        return self._rids

    def GetItemText(self, item_id):
        """Retrieves the text label of the given item"""
        item = self.SavedMenu.FindItemById(item_id)
        if not item:
            item = self.RemoveMenu.FindItemById(item_id)

        if item:
            return item.GetLabel()
        else:
            return u''

    def OnThemeChanged(self, msg):
        """Update the buttons icon when the icon theme changes
        @param msg: Message Object

        """
        bmp = wx.ArtProvider.GetBitmap(str(ed_glob.ID_ADD_BM), wx.ART_MENU)
        self.menub.SetBitmap(bmp)
        self.menub.Refresh()

    def RemoveItemById(self, path_id):
        """Removes a given menu item from both the saved
        and removed lists using the id as a lookup.

        """
        o_ids = self.GetOpenIds()
        r_ids = self.GetRemoveIds()

        if path_id in r_ids:
            index = r_ids.index(path_id)
            self.RemoveMenu.Remove(path_id)
            self.SavedMenu.Remove(o_ids[index])
            self._rids.remove(path_id)
            del self._ids[index]

#-----------------------------------------------------------------------------#

class BrowserPane(eclib.ControlBox):
    """Creates a filebrowser Pane"""
    def __init__(self, parent):
        super(BrowserPane, self).__init__(parent)
        
        # Attributes
        self._mw = parent
        self._menbar = BrowserMenuBar(self)
        self._browser = FileBrowser2(self)
        self._browser.SetMainWindow(self._mw)
        self._config = PathMarkConfig(ed_glob.CONFIG['CACHE_DIR'])
        for item in self._config.GetItemLabels():
            self._menbar.AddItem(item)

        # Layout
        self.SetWindow(self._browser)
        self.SetControlBar(self._menbar, wx.TOP)
        self.Layout()

        #---- Add Menu Items ----#
        viewm = self._mw.MenuBar.GetMenuByName("view")
        self._mi = viewm.InsertAlpha(ID_FILEBROWSE, _("File Browser"), 
                                     _("Open File Browser Sidepanel"),
                                     wx.ITEM_CHECK,
                                     after=ed_glob.ID_PRE_MARK)

        # Event Handlers
        self.Bind(wx.EVT_MENU, self.OnMenu)
        self.Bind(wx.EVT_SHOW, self.OnShow)
        self.Bind(wx.EVT_WINDOW_DESTROY, self.OnDestroy)

        # Messages
        ed_msg.Subscribe(self.OnUpdateFont, ed_msg.EDMSG_DSP_FONT)

    def OnDestroy(self, evt):
        """Save the config before we get destroyed"""
        if self:
            self._config.Save()
            ed_msg.Unsubscribe(self.OnUpdateFont)

    def OnShow(self, evt):
        if self and self._browser:
            self._browser.SuspendChecks(not evt.IsShown())
        evt.Skip()

    def GetMainWindow(self):
        """Get the MainWindow that owns this panel"""
        return self._mw

    def OnMenu(self, evt):
        """Handles the events associated with adding, opening,
        and removing paths in the menubars menus.

        """
        e_id = evt.Id
        o_ids = self._menbar.GetOpenIds()
        d_ids = self._menbar.GetRemoveIds()
        if e_id == ID_MARK_PATH:
            items = self._browser.SelectedFiles
            for item in items:
                self._menbar.AddItem(item)
                self._config.AddPathMark(item, item)
                self._config.Save()
        elif e_id in o_ids:
            pmark = self._menbar.GetItemText(e_id)
            path = self._config.GetPath(pmark)
            self._browser.SelectFile(path)
            self._browser.SetFocus()
        elif e_id in d_ids:
            plabel = self._menbar.GetItemText(e_id)
            self._menbar.RemoveItemById(e_id)
            self._config.RemovePathMark(plabel)
            self._config.Save()
        else:
            evt.Skip()

    def OnShowBrowser(self, evt):
        """Shows the filebrowser"""
        if evt.Id == ID_FILEBROWSE:
            mgr = self._mw.GetFrameManager()
            pane = mgr.GetPane(PANE_NAME)
            if pane.IsShown():
                pane.Hide()
            else:
                pane.Show()
                cbuff = self._mw.GetNotebook().GetCurrentCtrl()
                path = cbuff.GetFileName()
                if path:
                    self._browser.SelectFile(path)
            mgr.Update()
        else:
            evt.Skip()

    def OnUpdateFont(self, msg):
        """Update the ui font when a message comes saying to do so."""
        font = msg.GetData()
        if isinstance(font, wx.Font) and not font.IsNull():
            for child in (self, self._browser):
                if hasattr(child, 'SetFont'):
                    child.SetFont(font)

    def OnUpdateMenu(self, evt):
        """UpdateUI handler for the panels menu item, to update the check
        mark.
        @param evt: wx.UpdateUIEvent

        """
        pane = self._mw.GetFrameManager().GetPane(PANE_NAME)
        evt.Check(pane.IsShown())

#-----------------------------------------------------------------------------#

class FBMimeMgr(object):
    """Manager class for managing known file types and icons"""
    IMAGES = range(18)
    IMG_COMPUTER, \
    IMG_FLOPPY, \
    IMG_HARDDISK, \
    IMG_CD, \
    IMG_USB, \
    IMG_FOLDER, \
    IMG_FOLDER_OPEN, \
    IMG_NO_ACCESS, \
    IMG_BIN, \
    IMG_FILE, \
    IMG_PYTHON, \
    IMG_BOO, \
    IMG_CSS, \
    IMG_HTML, \
    IMG_JAVA, \
    IMG_PHP, \
    IMG_RUBY, \
    IMG_SHELL = IMAGES
    IMGMAP = { IMG_COMPUTER : ed_glob.ID_COMPUTER,
               IMG_FLOPPY  : ed_glob.ID_FLOPPY,
               IMG_HARDDISK : ed_glob.ID_HARDDISK,
               IMG_CD      : ed_glob.ID_CDROM,
               IMG_USB     : ed_glob.ID_USB,
               IMG_FOLDER  : ed_glob.ID_FOLDER,
               IMG_FOLDER_OPEN : ed_glob.ID_OPEN,
               IMG_NO_ACCESS : ed_glob.ID_STOP,
               IMG_BIN     : ed_glob.ID_BIN_FILE,
               IMG_FILE    : ed_glob.ID_FILE,
               IMG_PYTHON  : synglob.ID_LANG_PYTHON,
               IMG_BOO     : synglob.ID_LANG_BOO,
               IMG_CSS     : synglob.ID_LANG_CSS,
               IMG_HTML    : synglob.ID_LANG_HTML,
               IMG_JAVA    : synglob.ID_LANG_JAVA,
               IMG_PHP     : synglob.ID_LANG_PHP,
               IMG_RUBY    : synglob.ID_LANG_RUBY,
               IMG_SHELL   : synglob.ID_LANG_BASH }
    def __init__(self):
        super(FBMimeMgr, self).__init__()

        # Attributes
        self._ftype = FBMimeMgr.IMG_FILE
        
    @classmethod
    def PopulateImageList(cls, imglist):
        """Populate an ImageList with the icons for the file tree
        @param imglist: wx.ImageList instance (16x16)

        """
        imglist.RemoveAll()
        for img in FBMimeMgr.IMAGES:
            imgid = FBMimeMgr.IMGMAP[img]
            bmp = wx.ArtProvider_GetBitmap(str(imgid), wx.ART_MENU)
            if bmp.IsOk():
                imglist.Add(bmp)

    @classmethod
    def RefreshImageList(cls, imglist):
        """Refresh all icons from the icon manager"""
        for idx, img in enumerate(FBMimeMgr.IMAGES):
            imgid = FBMimeMgr.IMGMAP[img]
            bmp = wx.ArtProvider_GetBitmap(str(imgid), wx.ART_MENU)
            if bmp.IsOk():
                imglist.Replace(idx, bmp)

    def GetImageIndex(self, path, expanded=False):
        """Get the appropriate file index for the given path
        @param path: file name or path

        """
        self._ftype = FBMimeMgr.IMG_FILE
        if not os.access(path, os.R_OK):
            self._ftype = FBMimeMgr.IMG_NO_ACCESS
        elif self.IsDevice(path):
            pass
        elif os.path.isdir(path):
            if expanded:
                self._ftype = FBMimeMgr.IMG_FOLDER_OPEN
            else:
                self._ftype = FBMimeMgr.IMG_FOLDER
        elif self.IsKnownTextFile(path):
            pass
        elif self.IsKnownBinType(path):
            pass
        return self._ftype

    def IsKnownTextFile(self, path):
        """Is a known text file type
        @param path: file path / name

        """
        tpath = os.path.basename(path)
        ext = ebmlib.GetFileExtension(tpath)
        etype = syntax.GetIdFromExt(ext)
        tmap = { synglob.ID_LANG_PYTHON : FBMimeMgr.IMG_PYTHON,
                 synglob.ID_LANG_BOO : FBMimeMgr.IMG_BOO,
                 synglob.ID_LANG_CSS : FBMimeMgr.IMG_CSS,
                 synglob.ID_LANG_HTML : FBMimeMgr.IMG_HTML,
                 synglob.ID_LANG_JAVA : FBMimeMgr.IMG_JAVA,
                 synglob.ID_LANG_PHP : FBMimeMgr.IMG_PHP,
                 synglob.ID_LANG_RUBY : FBMimeMgr.IMG_RUBY,
                 synglob.ID_LANG_BASH : FBMimeMgr.IMG_SHELL }
        self._ftype = tmap.get(etype, FBMimeMgr.IMG_FILE)
        return self._ftype != FBMimeMgr.IMG_FILE

    def IsKnownBinType(self, path):
        """Is a known binary file type
        @param path: file path / name

        """
        ext = ebmlib.GetFileExtension(path)
        if ext in ('exe', 'dll', 'so'): # TODO better mapping
            self._ftype = FBMimeMgr.IMG_BIN
        else:
            return False
        return True

    def IsDevice(self, path):
        """Is the path some sort of device"""
        if os.path.ismount(path):
            self._ftype = FBMimeMgr.IMG_HARDDISK
            if wx.Platform == '__WXMSW__':
                dtype = ebmlib.GetWindowsDriveType(path)
                if isinstance(dtype, ebmlib.RemovableDrive):
                    self._ftype = FBMimeMgr.IMG_USB
                elif isinstance(dtype, ebmlib.CDROMDrive):
                    self._ftype = FBMimeMgr.IMG_CD
        rval = self._ftype != FBMimeMgr.IMG_FILE
        return rval

#-----------------------------------------------------------------------------#
# Menu Id's
ID_EDIT = wx.NewId()
ID_OPEN = wx.NewId()
ID_SEARCH_DIR = wx.NewId()
ID_REVEAL = wx.NewId()
ID_GETINFO = wx.NewId()
ID_RENAME = wx.NewId()
ID_NEW_FOLDER = wx.NewId()
ID_NEW_FILE = wx.NewId()
ID_DELETE = wx.NewId()
ID_DUPLICATE = wx.NewId()
ID_ARCHIVE = wx.NewId()

class FileBrowser2(ed_basewin.EDBaseFileTree):
    """File browser Tree"""
    def __init__(self, parent):
        self._mime = FBMimeMgr()

        super(FileBrowser2, self).__init__(parent)

        # Attributes
        self._mw = None
        self._menu = ebmlib.ContextMenuManager()
        self._monitor = ebmlib.DirectoryMonitor(checkFreq=-1) # manual refresh...
        self._monitor.SubscribeCallback(self.OnFilesChanged)
        self._monitor.StartMonitoring()
        self.isClosing = False
        self.syncTimer = wx.Timer(self)
        self._cpath = None

        # Setup
        self.SetupImageList()
        if wx.Platform == '__WXMSW__':
            for dname in ebmlib.GetWindowsDrives():
                if os.path.exists(dname.Name):
                    self.AddWatchDirectory(dname.Name)
        else:
            self.AddWatchDirectory("/")

        # Event Handlers
        self.Bind(wx.EVT_MENU, self.OnMenu)
        self.Bind(wx.EVT_TIMER, self.OnTimer)
        ed_msg.Subscribe(self.OnThemeChanged, ed_msg.EDMSG_THEME_CHANGED)
        ed_msg.Subscribe(self.OnPageChange, ed_msg.EDMSG_UI_NB_CHANGED)
        ed_msg.Subscribe(self.OnPageClosing, ed_msg.EDMSG_UI_NB_CLOSING)
        ed_msg.Subscribe(self.OnConfig, ed_msg.EDMSG_PROFILE_CHANGE + (fbcfg.FB_PROF_KEY,))

    def DoOnActivate(self, active):
        """Handle activation of main window that this
        tree belongs too.
        @param active: bool

        """
        # Suspend background checks when window is not active
        if active and self.IsShown():
            self.SuspendChecks(False) # Resume
        elif not active:
            self.SuspendChecks(True) # Suspend

    def DoOnDestroy(self):
        """Clean up resources and message handlers"""
        self._menu.Clear()
        ed_msg.Unsubscribe(self.OnPageChange)
        ed_msg.Unsubscribe(self.OnPageClosing)
        ed_msg.Unsubscribe(self.OnThemeChanged)
        ed_msg.Unsubscribe(self.OnConfig)
        if self.syncTimer.IsRunning():
            self.syncTimer.Stop()

    def SuspendChecks(self, suspend=True):
        """Suspend/Continue background monitoring"""
        self._monitor.Suspend(suspend)

    #--- FileTree interface methods ----#

    def DoSetupImageList(self):
        """Setup the image list for this control"""
        self._mime.PopulateImageList(self.ImageList)

    def DoGetFileImage(self, path):
        """Get the image for the given item"""
        return self._mime.GetImageIndex(path)

    def DoGetToolTip(self, item):
        """Get the tooltip to show for an item
        @return: string or None

        """
        tip = None
        if self.GetItemImage(item) == self._mime.IMG_NO_ACCESS:
            tip = _("Access Denied")
#        elif item: # Slightly annoying on GTK disable for now
#            tip = self.GetPyData(item)
        return tip

    def DoItemActivated(self, item):
        """Override to handle item activation
        @param item: TreeItem

        """
        self.OpenFiles(self.GetSelectedFiles())

    def DoItemCollapsed(self, item):
        """Handle when an item is collapsed"""
        d = self.GetPyData(item)
        if d:
            self._monitor.RemoveDirectory(d)
        super(FileBrowser2, self).DoItemCollapsed(item)
        self.SetItemImage(item, self._mime.GetImageIndex(d, False))

    def ShouldDisplayFile(self, path):
        """Check if the given file should be displayed based on configuration
        @param path: file path
        @return: bool

        """
        showHidden = fbcfg.GetFBOption(fbcfg.FB_SHF_OPT, False)
        if not showHidden and ebmlib.IsHidden(path):
            return False
        name = os.path.basename(path)
        filters = fbcfg.GetFBOption(fbcfg.FB_FILTER_OPT,
                                    fbcfg.FB_DEFAULT_FILTERS)
        if filter(lambda x: fnmatch.fnmatchcase(name, x), filters):
                return False
        return True

    def FilterFileList(self, paths):
        """Filter a list of files returning only the ones that are valid to
        display in the tree. Optimized for large lists of paths.
        @param paths: list of paths
        @return: filtered list

        """
        showHidden = fbcfg.GetFBOption(fbcfg.FB_SHF_OPT, False)
        filters = fbcfg.GetFBOption(fbcfg.FB_FILTER_OPT,
                                    fbcfg.FB_DEFAULT_FILTERS)
        isHidden = ebmlib.IsHidden
        rval = list()
        rAdd = rval.append
        getBase = os.path.basename
        for path in paths:
            if not showHidden and isHidden(path):
                continue
            name = getBase(path)
            if filter(lambda x: fnmatch.fnmatchcase(name, x), filters):
                continue
            rAdd(path)
        return rval

    def DoItemExpanding(self, item):
        """Handle when an item is expanding to display the folder contents
        @param item: TreeItem

        """
        busy = wx.BusyCursor() # can take a few seconds on big directories

        d = None
        try:
            d = self.GetPyData(item)
        except wx.PyAssertionError:
            util.Log("[FileBrowser][err] FileBrowser2.DoItemExpanding")
            return

        if d and os.path.exists(d) and os.access(d, os.R_OK):
            contents = FileBrowser2.GetDirContents(d)
            t1 = time.time()
            with eclib.Freezer(self) as _tmp:
                self.AppendFileNodes(item, self.FilterFileList(contents))
                self.SortChildren(item)
            util.Log("[FileBrowser][info] Tree expand time: %f" % (time.time() - t1))

            if not self._monitor.AddDirectory(d):
                self.SetItemImage(item, self._mime.IMG_NO_ACCESS)
                return

        # Update tree image
        self.SetItemImage(item, self._mime.GetImageIndex(d, True))

    def DoBeginEdit(self, item):
        """Handle when an item is requested to be edited"""
        d = None
        try:
            d = self.GetPyData(item)
        except wx.PyAssertionError:
            util.Log("[FileBrowser][err] FileBrowser2.DoItemExpanding")
            return False
        if d and not os.access(d, os.W_OK) or os.path.ismount(d):
            return False
        return True

    def DoEndEdit(self, item, newlabel):
        """Handle after a user has made changes to a label"""
        editOk = False
        path = self.GetPyData(item)
        # TODO: check access rights and validate input
        if path:
            newpath = os.path.join(os.path.dirname(path), newlabel)
            try:
                dobjs = TakeSnapshots([path,])
                os.rename(path, newpath)
                editOk = True
                if dobjs:
                    self.RefreshView(dobjs)
            except OSError:
                editOk = False # TODO: notify user of error
        return editOk

    def DoShowMenu(self, item):
        """Show context menu"""
        # Check if click was in blank window area
        activeNode = None
        try:
            activeNode = self.GetPyData(item)
        except wx.PyAssertionError:
            pass

        if not self._menu.Menu:
            self._menu.Menu = wx.Menu()
            # TODO: bother with theme changes ...?
            items = [(ID_EDIT, _("Edit"), None),
                     (ID_OPEN, _("Open with " + FILEMAN), ed_glob.ID_OPEN),
                     (ID_REVEAL, _("Reveal in " + FILEMAN), None),
                     (wx.ID_SEPARATOR, '', None),
                     (wx.ID_REFRESH, _("Refresh"), ed_glob.ID_REFRESH),
                     (wx.ID_SEPARATOR, '', None),
                     (ID_MARK_PATH, _("Bookmark Selected Path(s)"),
                      ed_glob.ID_ADD_BM),
                     (wx.ID_SEPARATOR, '', None),
                     (ID_SEARCH_DIR, _("Search in directory"), ed_glob.ID_FIND),
                     (wx.ID_SEPARATOR, '', None),
                     (ID_GETINFO, _("Get Info"), None),
                     (ID_RENAME, _("Rename"), None),
                     (wx.ID_SEPARATOR, '', None),
                     (ID_NEW_FOLDER, _("New Folder"), ed_glob.ID_FOLDER),
                     (ID_NEW_FILE, _("New File"), ed_glob.ID_NEW),
                     (wx.ID_SEPARATOR, '', None),
                     (ID_DUPLICATE, _("Duplicate"), None),
                     (ID_ARCHIVE, _("Create Archive of \"%s\"") % '', None),
                     (wx.ID_SEPARATOR, '', None),
                     (ID_DELETE, TrashString(), ed_glob.ID_DELETE),
                    ]

            for mi_tup in items:
                mitem = wx.MenuItem(self._menu.Menu, mi_tup[0], mi_tup[1])
                if mi_tup[2] is not None:
                    bmp = wx.ArtProvider.GetBitmap(str(mi_tup[2]), wx.ART_MENU)
                    mitem.SetBitmap(bmp)

                self._menu.Menu.AppendItem(mitem)

        # Set contextual data
        self._menu.SetUserData('item_id', item)
        self._menu.SetUserData('active_node', activeNode)
        self._menu.SetUserData('selected_nodes', self.GetSelectedFiles())

        # Update Menu
        mitem = self._menu.Menu.FindItemById(ID_ARCHIVE)
        if mitem != wx.NOT_FOUND:
            path = self._menu.GetUserData('active_node')
            mitem.SetText(_("Create Archive of \"%s\"") % \
                          path.split(os.path.sep)[-1])
        for mitem in (ID_DUPLICATE,):
            self._menu.Menu.Enable(mitem, len(self.GetSelections()) == 1)

        self.PopupMenu(self._menu.Menu)

    #---- End FileTree Interface Methods ----#

    @staticmethod
    def OpenFiles(files):
        """Open the list of files in Editra for editing
        @param files: list of file names

        """
        to_open = list()
        for fname in files:
            try:
                res = os.stat(fname)[0]
                if stat.S_ISREG(res) or stat.S_ISDIR(res):
                    to_open.append(fname)
            except (IOError, OSError), msg:
                util.Log("[filebrowser][err] %s" % str(msg))

        win = wx.GetApp().GetActiveWindow()
        if win:
            win.GetNotebook().OnDrop(to_open)

    def OnCompareItems(self, item1, item2):
        """Handle SortItems"""
        data = self.GetPyData(item1)
        if data is not None:
            path1 = int(not os.path.isdir(data))
        else:
            path1 = 0
        tup1 = (path1, data.lower())

        data2 = self.GetPyData(item2)
        if data2 is not None:
            path2 = int(not os.path.isdir(data2))
        else:
            path2 = 0
        tup2 = (path2, data2.lower())

        if tup1 < tup2:
            return -1
        elif tup1 == tup2:
            return 0
        else:
            return 1

    def OnFilesChanged(self, added, deleted, modified):
        """DirectoryMonitor callback - synchronize the view
        with the filesystem.
        @param added: list of paths added
        @param deleted: list of paths removed
        @param modified: list of paths modified

        """
        nodes = self.GetExpandedNodes()
        visible = list()
        for node in nodes:
            visible.extend(self.GetChildNodes(node))

        # Remove any deleted file objects
        for fobj in deleted:
            for item in visible:
                path = self.GetPyData(item)
                if fobj.Path == path:
                    self.Delete(item)
                    visible.remove(item)
                    break

        # Add any new file objects to the view
        pathCache = dict()
        needsort = list()
        for fobj in added:
            # apply filters to any new files
            if not self.ShouldDisplayFile(fobj.Path):
                continue
            dpath = os.path.dirname(fobj.Path)
            for item in nodes:
                path = self.GetPyData(item)
                if path == dpath:
                    # prevent duplicates from being added
                    if path not in pathCache:
                        pathCache[path] = self.GetNodePaths(item)
                        if fobj.Path in pathCache[path]:
                            continue

                    self.AppendFileNode(item, fobj.Path)
                    if item not in needsort:
                        needsort.append(item)
                    break

        # Re-sort display
        for item in needsort:
            self.SortChildren(item)

    def OnMenu(self, evt):
        """Handle the context menu events for performing
        filesystem operations

        """
        e_id = evt.Id
        path = self._menu.GetUserData('active_node')
        paths = self._menu.GetUserData('selected_nodes')

        def Opener(paths):
            """File opener job
            @param paths: list of paths

            """
            for fname in paths:
                subprocess.call([FILEMAN_CMD, fname])
                time.sleep(.25)

        if e_id == ID_EDIT:
            self.OpenFiles(paths)
        elif e_id == ID_OPEN:
            ed_thread.EdThreadPool().QueueJob(Opener, paths)
        elif e_id == ID_REVEAL:
            dpaths = [os.path.dirname(fname) for fname in paths]
            dpaths = list(set(dpaths))
            ed_thread.EdThreadPool().QueueJob(Opener, dpaths)
        elif e_id == wx.ID_REFRESH:
            # Refresh the view
            self.RefreshView()
        elif e_id == ID_SEARCH_DIR:
            if len(paths):
                path = paths[0] # Go off of the first selected item
                if not os.path.isdir(path):
                    path = os.path.dirname(path)
                mdata = dict(mainw=self._mw, lookin=path)
                ed_msg.PostMessage(ed_msg.EDMSG_FIND_SHOW_DLG, mdata) 
        elif e_id == ID_GETINFO:
            last = None
            for fname in paths:
                info = ed_mdlg.EdFileInfoDlg(self.TopLevelParent, fname)
                if last is None:
                    info.CenterOnParent()
                else:
                    lpos = last.GetPosition()
                    info.SetPosition((lpos[0] + 14, lpos[1] + 14))
                info.Show()
                last = info
        elif e_id == ID_RENAME:
            item = self._menu.GetUserData('item_id')
            self.EditLabel(item)
        elif e_id == ID_NEW_FOLDER:
            name = wx.GetTextFromUser(_("Enter folder name:"), _("New Folder"),
                                      parent=self.TopLevelParent)
            if name:
                dobjs = TakeSnapshots([path,])
                err, msg = ebmlib.MakeNewFolder(path, name)
                if not err:
                    wx.MessageBox(msg, _("Failed to create folder"),
                                  style=wx.OK|wx.CENTER|wx.ICON_ERROR)
                else:
                    self.RefreshView(dobjs)
        elif e_id == ID_NEW_FILE:
            name = wx.GetTextFromUser(_("Enter file name:"), _("New File"),
                                      parent=self.TopLevelParent)
            if name:
                dobjs = TakeSnapshots([path,])
                err, msg = ebmlib.MakeNewFile(path, name)
                if not err:
                    wx.MessageBox(msg, _("Failed to create file"),
                                  style=wx.OK|wx.CENTER|wx.ICON_ERROR)
                else:
                    self.RefreshView(dobjs)
        elif e_id == ID_DUPLICATE:
            dobjs = TakeSnapshots(paths)
            for fname in paths:
                DuplicatePath(fname)
            self.RefreshView(dobjs)
        elif e_id == ID_ARCHIVE:
            dobjs = TakeSnapshots([path,])
            MakeArchive(path)
            self.RefreshView(dobjs)
        elif e_id == ID_DELETE:
            dobjs = TakeSnapshots(paths)
            ebmlib.MoveToTrash(paths)
            self.RefreshView(dobjs)
        else:
            evt.Skip()
            return

    def OnThemeChanged(self, msg):
        """Update the icons when the icon theme has changed
        @param msg: Message Object

        """
        self._mime.RefreshImageList(self.ImageList)

    def OnConfig(self, msg):
        """Handle updates for filebrowser preference updates"""
        # TODO: refresh tree for hidden files on/off
        pass

    @ed_msg.mwcontext
    def OnPageClosing(self, msg):
        self.isClosing = True

    @ed_msg.mwcontext
    def OnPageChange(self, msg):
        """Synchronize selection with the notebook page changes
        @param msg: MessageObject
        @todo: check if message is from a page closing and avoid updates

        """
        if self.isClosing:
            self.isClosing = False
            return

        if not fbcfg.GetFBOption(fbcfg.FB_SYNC_OPT, True):
            return

        nbdata = msg.GetData()
        if not nbdata[0]:
            return

        pg_count = nbdata[0].GetPageCount()
        if nbdata[1] > pg_count  or nbdata[1] < 0:
            # Page is out of range, something has changed since the 
            # message was sent.
            return

        page = nbdata[0].GetPage(nbdata[1])
        if page:
            path = getattr(page, 'GetFileName', lambda: u"")()
            if len(path) and os.path.exists(path):
                # Delay selection for smoother operation when many
                # page change events are received in a short time.
                if self.syncTimer.IsRunning():
                    self.syncTimer.Stop()
                self._cpath = path
                self.syncTimer.Start(500, True)

    @refreshAfter
    def OnTimer(self, evt):
        """Handle tab synchronization"""
        if self._cpath:
            self.SelectFile(self._cpath)

    def RefreshView(self, paths=None):
        """Refresh file view of monitored directories"""
        self._monitor.Refresh(paths)

    def GetMainWindow(self):
        """Get the main window, needed by L{ed_msg.mwcontext}"""
        return self._mw

    def SetMainWindow(self, mainw):
        """Set the main window this browser belongs to.
        @param mainw: MainWindow or None

        """
        self._mw = mainw

#-----------------------------------------------------------------------------#

# TODO maybe switch to storing this info in the user profile instead of
#      managing it here.
class PathMarkConfig(object):
    """Manages the saving of pathmarks to make them usable from
    one session to the next.

    """
    CONFIG_FILE = u'pathmarks'

    def __init__(self, pname):
        """Creates the config object, the pname parameter
        is the base path to store the config file at on write.

        """
        super(PathMarkConfig, self).__init__()

        # Attributes
        self._base = os.path.join(pname, PathMarkConfig.CONFIG_FILE)
        self._pmarks = dict()

        self.Load()

    def AddPathMark(self, label, path):
        """Adds a label and a path to the config"""
        self._pmarks[label.strip()] = path.strip()

    def GetItemLabels(self):
        """Returns a list of all the item labels in the config"""
        return self._pmarks.keys()

    def GetPath(self, label):
        """Returns the path associated with a given label"""
        return self._pmarks.get(label, u'')

    def Load(self):
        """Loads the configuration data into the dictionary"""
        file_h = util.GetFileReader(self._base)
        if file_h != -1:
            lines = file_h.readlines()
            file_h.close()
        else:
            return False

        for line in lines:
            vals = line.strip().split(u"=")
            if len(vals) != 2:
                continue
            if os.path.exists(vals[1]):
                self.AddPathMark(vals[0], vals[1])
        return True

    def RemovePathMark(self, pmark):
        """Removes a path mark from the config"""
        if pmark in self._pmarks:
            del self._pmarks[pmark]

    def Save(self):
        """Writes the config out to disk"""
        file_h = util.GetFileWriter(self._base)
        if file_h == -1:
            return False

        for label in self._pmarks:
            file_h.write(u"%s=%s\n" % (label, self._pmarks[label]))
        file_h.close()
        return True

#-----------------------------------------------------------------------------#
# Utilities
def DuplicatePath(path):
    """Create a copy of the item at the end of the given path. The item
    will be created with a name in the form of Dirname_Copy for directories
    and FileName_Copy.extension for files.
    @param path: path to duplicate
    @return: Tuple of (success?, filename OR Error Message)

    """
    head, tail = os.path.split(path)
    if os.path.isdir(path):
        name = ebmlib.GetUniqueName(head, tail + "_Copy")
        copy = shutil.copytree
    else:
        tmp = [ part for part in tail.split('.') if len(part) ]
        if tail.startswith('.'):
            tmp[0] = "." + tmp[0]
            if '.' not in tail[1:]:
                tmp[0] = tmp[0] + "_Copy"
            else:
                tmp.insert(-1, "_Copy.")

            tmp = ''.join(tmp)
        elif '.' not in tail:
            # file with no extension
            tmp = tail + "_Copy"
        else:
            tmp = '.'.join(tmp[:-1]) + "_Copy." + tmp[-1]

        if len(tmp) > 1:
            name = ebmlib.GetUniqueName(head, tmp)
        copy = shutil.copy2

    try:
        copy(path, name)
    except (OSError, IOError, shutil.Error), msg:
        return (False, str(msg))

    return (True, name)

def MakeArchive(path):
    """Create a Zip archive of the item at the end of the given path
    @param path: full path to item to archive
    @return: Tuple of (success?, file name OR Error Message)
    @rtype: (bool, str)
    @todo: support for zipping multiple paths

    """
    dname, fname = os.path.split(path)
    ok = True
    name = ''
    if dname and fname:
        name = ebmlib.GetUniqueName(dname, fname + ".zip")
        files = list()
        cwd = os.getcwd()
        head = dname
        try:
            try:
                os.chdir(dname)
                if os.path.isdir(path):
                    for dpath, dname, fnames in os.walk(path):
                        files.extend([ os.path.join(dpath, fname).\
                                       replace(head, '', 1).\
                                       lstrip(os.path.sep) 
                                       for fname in fnames])

                zfile = zipfile.ZipFile(name, 'w', compression=zipfile.ZIP_DEFLATED)
                for fname in files:
                    zfile.write(fname.encode(sys.getfilesystemencoding()))
            except Exception, msg:
                ok = False
                name = str(msg)
        finally:
            zfile.close()
            os.chdir(cwd)

    return (ok, name)

def TakeSnapshots(paths):
    """Take snapshots of the given paths
    @param paths: list of paths to snapshot
    @return: list of DirectoryObjects or None

    """
    assert isinstance(paths, list)
    rlist = list()
    tpaths = list()
    for path in paths:
        path = os.path.dirname(path)
        if os.path.exists(path) and path not in tpaths:
            tpaths.append(path)
    for dpath in tpaths:
        dobj = ebmlib.GetDirectoryObject(dpath, False, True)
        rlist.append(dobj)
    if not len(rlist):
        rlist = None

    return rlist

#-----------------------------------------------------------------------------#
