# -*- coding: utf-8 -*-
###############################################################################
# Name: cfgdlg.py                                                             #
# Purpose: Configuration Dialog                                               #
# Author: Cody Precord <cprecord@editra.org>                                  #
# Copyright: (c) 2008 Cody Precord <staff@editra.org>                         #
# License: wxWindows License                                                  #
###############################################################################

"""Launch Configuration Dialog"""

__author__ = "Cody Precord <cprecord@editra.org>"
__svnid__ = "$Id$"
__revision__ = "$Revision$"

#-----------------------------------------------------------------------------#
# Imports
import sys
import wx
import wx.lib.mixins.listctrl as listmix
import wx.lib.intctrl as intctrl
import cStringIO
import zlib

# Local Imports
import handlers

# Editra Libraries
import ed_glob
import eclib
import ed_msg
import ed_basewin
from profiler import Profile_Get, Profile_Set
import syntax.syntax as syntax
import util

#-----------------------------------------------------------------------------#
# Globals

# General Panel
ID_LANGUAGE = wx.NewId()
ID_EXECUTABLES = wx.NewId()

# Misc Panel
ID_AUTOCLEAR = wx.NewId()
ID_ERROR_BEEP = wx.NewId()
ID_WRAP_OUTPUT = wx.NewId()

# Color Buttons
ID_DEF_BACK = wx.NewId()
ID_DEF_FORE = wx.NewId()
ID_INFO_BACK = wx.NewId()
ID_INFO_FORE = wx.NewId()
ID_ERR_BACK = wx.NewId()
ID_ERR_FORE = wx.NewId()
ID_WARN_BACK = wx.NewId()
ID_WARN_FORE = wx.NewId()

COLOR_MAP = { ID_DEF_BACK : 'defaultb', ID_DEF_FORE : 'defaultf',
              ID_ERR_BACK : 'errorb',   ID_ERR_FORE : 'errorf',
              ID_INFO_BACK : 'infob',   ID_INFO_FORE : 'infof',
              ID_WARN_BACK : 'warnb',   ID_WARN_FORE : 'warnf'}

_ = wx.GetTranslation

#----------------------------------------------------------------------
DEFAULT_LINEBUFFER = 1000

def InitConfig():
    """Initialize the Launch configuration"""
    cfg = Profile_Get(handlers.CONFIG_KEY, default=dict())
    bChanged = False
    for key, val in (('autoclear', False), ('errorbeep', False),
                     ('wrapout', False), ('defaultf', wx.BLACK),
                     ('defaultb', wx.WHITE), ('errorf', wx.RED),
                     ('errorb', wx.WHITE), ('infof', wx.BLUE),
                     ('infob', wx.WHITE), ('warnf', wx.RED),
                     ('warnb', wx.WHITE), ('linebuffer', DEFAULT_LINEBUFFER)):
        # Set default value for any uninitialized preference
        if key not in cfg:
            cfg[key] = val
            bChanged = True
    if bChanged:
        Profile_Set(handlers.CONFIG_KEY, cfg)

#----------------------------------------------------------------------

class ConfigDialog(ed_basewin.EdBaseFrame):
    """Configuration dialog for configuring what executables are available
    for a filetype and what the preferred one is.

    """
    def __init__(self, parent, ftype=0):
        """Create the ConfigDialog
        @param parent: The parent window
        @keyword ftype: The filetype to set

        """
        super(ConfigDialog, self).__init__(parent, title=_("Launch Configuration"))

        # Layout
        self.__DoLayout()

    def __DoLayout(self):
        """Layout the dialog"""
        sizer = wx.BoxSizer(wx.VERTICAL)
        hsizer = wx.BoxSizer(wx.HORIZONTAL)
        vsizer = wx.BoxSizer(wx.VERTICAL)
        panel = wx.Panel(self)
        noteb = ConfigNotebook(panel)
        hsizer.AddMany([((5, 5), 0), (noteb, 1, wx.EXPAND), ((5, 5), 0)])
        vsizer.AddMany([((5, 5), 0), (hsizer, 1, wx.EXPAND), ((10, 10), 0)])
        panel.SetSizer(vsizer)
        sizer.Add(panel, 1, wx.EXPAND)
        self.SetSizer(sizer)
        self.SetAutoLayout(True)
        self.SetInitialSize()
        self.SetMinSize((420, 345))

#-----------------------------------------------------------------------------#

class ConfigNotebook(wx.Notebook):
    """Notebook for holding config pages"""
    def __init__(self, parent):
        super(ConfigNotebook, self).__init__(parent)

        # Make sure config has been initialized
        InitConfig()

        # Setup
        self.AddPage(ConfigPanel(self), _("General"))
        self.AddPage(OutputPanel(self), _("Output"))
        self.AddPage(MiscPanel(self), _("Misc"))

#-----------------------------------------------------------------------------#

class ConfigPanel(wx.Panel):
    """Configuration panel that holds the controls for configuration"""
    def __init__(self, parent):
        super(ConfigPanel, self).__init__(parent)

        # Attributes
        self.addbtn = None
        self.delbtn = None
        self.infotxt = None

        # Layout
        self.__DoLayout()

        # Event Handlers
        self.Bind(wx.EVT_BUTTON, self.OnButton)
        self.Bind(wx.EVT_CHOICE, self.OnChoice)
        self.Bind(wx.EVT_LIST_END_LABEL_EDIT, self.OnEndEdit)

    def __DoLayout(self):
        """Layout the controls"""
        msizer = wx.BoxSizer(wx.VERTICAL)

        lsizer = wx.BoxSizer(wx.HORIZONTAL)
        ftype = wx.GetApp().GetCurrentBuffer().GetLangId()
        ftype = handlers.GetHandlerById(ftype)
        hname = ftype.GetName()
        util.Log("[Launch][info] ConfigPanel: %s" % hname)
        htypes = sorted(syntax.SyntaxNames())
        lang_ch = wx.Choice(self, ID_LANGUAGE, choices=htypes)
        if ftype != handlers.DEFAULT_HANDLER:
            lang_ch.SetStringSelection(hname)
        else:
            lang_ch.SetStringSelection(htypes[0])

        lsizer.AddMany([(wx.StaticText(self, label=_("File Type") + u":"), 0,
                         wx.ALIGN_CENTER_VERTICAL), ((5, 5), 0),
                        (lang_ch, 1, wx.EXPAND|wx.ALIGN_CENTER_VERTICAL)])

        # Main area
        sbox = wx.StaticBox(self, label=_("Executables"))
        boxsz = wx.StaticBoxSizer(sbox, wx.VERTICAL)

        # Default exe
        dsizer = wx.BoxSizer(wx.HORIZONTAL)
        chandler = handlers.GetHandlerByName(lang_ch.GetStringSelection())
        cmds = chandler.GetAliases()
        def_ch = wx.Choice(self, wx.ID_DEFAULT, choices=cmds)
        if chandler.GetName() != handlers.DEFAULT_HANDLER:
            def_ch.SetStringSelection(chandler.GetDefault())
        elif len(cmds):
            def_ch.SetStringSelection(cmds[0])
        else:
            pass

        dsizer.AddMany([(wx.StaticText(self, label=_("Default") + u":"), 0,
                         wx.ALIGN_CENTER_VERTICAL), ((5, 5), 0),
                        (def_ch, 1, wx.EXPAND|wx.ALIGN_CENTER_VERTICAL)])

        # Executables List
        exelist = CommandListCtrl(self, ID_EXECUTABLES,
                                  style=wx.LC_EDIT_LABELS|\
                                        wx.BORDER|wx.LC_REPORT|\
                                        wx.LC_SINGLE_SEL)
        self.SetListItems(chandler.GetCommands())
        bmp = wx.ArtProvider.GetBitmap(str(ed_glob.ID_ADD), wx.ART_MENU)
        self.addbtn = wx.BitmapButton(self, wx.ID_ADD, bmp)
        self.addbtn.SetToolTipString(_("Add a new executable"))
        bmp = wx.ArtProvider.GetBitmap(str(ed_glob.ID_REMOVE), wx.ART_MENU)
        self.delbtn = wx.BitmapButton(self, wx.ID_REMOVE, bmp)
        self.delbtn.SetToolTipString(_("Remove selection from list"))
        btnsz = wx.BoxSizer(wx.HORIZONTAL)
        self.infotxt = wx.StaticText(self, label=_("Transient XML Handler"))
        self.infotxt.Hide()
        btnsz.AddMany([(self.addbtn, 0), ((2, 2), 0), (self.delbtn, 0),
                       ((5,2),0), (self.infotxt, 0, wx.ALIGN_CENTER_VERTICAL)])

        # Box Sizer Layout
        boxsz.AddMany([((5, 5), 0), (dsizer, 0, wx.ALIGN_CENTER|wx.EXPAND),
                       ((5, 5), 0), (wx.StaticLine(self), 0, wx.EXPAND),
                       ((8, 8), 0), (exelist, 1, wx.EXPAND), ((5, 5), 0),
                       (btnsz, 0, wx.ALIGN_LEFT)])

        # Setup the main sizer
        msizer.AddMany([((10, 10), 0), (lsizer, 0, wx.EXPAND),
                        ((10, 10), 0), (wx.StaticLine(self), 0, wx.EXPAND),
                        ((10, 10), 0),
                        (boxsz, 1, wx.EXPAND|wx.ALIGN_CENTER_VERTICAL),
                        ((10, 10), 0)])

        hsizer = wx.BoxSizer(wx.HORIZONTAL)
        hsizer.AddMany([((8, 8), 0), (msizer, 1, wx.EXPAND), ((8, 8), 0)])
        self.SetSizer(hsizer)

        self.UpdateForHandler()

    def __DoUpdateHandler(self, handler):
        exes = self.GetListItems()
        handler.SetCommands(exes)
        def_ch = self.FindWindowById(wx.ID_DEFAULT)
        def_ch.SetItems(handler.GetAliases())
        def_ch.SetStringSelection(handler.GetDefault())
        handler.StoreState()

    def GetCurrentHandler(self):
        """Get the currently selected file type handler
        @return: handlers.FileTypeHandler

        """
        ftype = self.FindWindowById(ID_LANGUAGE).GetStringSelection()
        return handlers.GetHandlerByName(ftype)

    def GetListItems(self):
        """Get all the values from the list control
        return: tuple (alias, cmd)

        """
        item_id = -1
        exes = list()
        elist = self.FindWindowById(ID_EXECUTABLES)
        for item in range(elist.GetItemCount()):
            item_id = elist.GetNextItem(item_id)
            if item_id == -1:
                break
            val = (elist.GetItem(item_id, 0).GetText(),
                   elist.GetItem(item_id, 1).GetText())
            exes.append(val)
        return exes

    def OnButton(self, evt):
        """Handle the add and remove button events
        @param evt: wxButtonEvent

        """
        e_id = evt.GetId()
        elist = self.FindWindowById(ID_EXECUTABLES)
        if e_id == wx.ID_ADD:
            elist.Append([_("**Alias**"), _("**New Commandline**")])
        elif e_id == wx.ID_REMOVE:
            item = -1
            items = []
            while True:
                item = elist.GetNextItem(item, wx.LIST_NEXT_ALL,
                                         wx.LIST_STATE_SELECTED)
                if item == -1:
                    break
                items.append(item)

            for item in reversed(sorted(items)):
                elist.DeleteItem(item)

            wx.CallAfter(self.__DoUpdateHandler, self.GetCurrentHandler())
        else:
            evt.Skip()

    def OnChoice(self, evt):
        """Handle the choice selection events"""
        e_id = evt.GetId()
        e_obj = evt.GetEventObject()
        e_val = e_obj.GetStringSelection()
        if e_id == ID_LANGUAGE:
            self.UpdateForHandler()
        elif e_id == wx.ID_DEFAULT:
            handler = self.GetCurrentHandler()
            handler.SetDefault((e_val, handler.GetCommand(e_val)))
            handler.StoreState()
        else:
            evt.Skip()

    def OnEndEdit(self, evt):
        """Store the new list values after the editing of a
        label has finished.
        @param evt: wxEVT_LIST_END_LABEL_EDIT
        @note: values in list are set until after this handler has finished

        """
        handler = self.GetCurrentHandler()
        if handler.GetName() != handlers.DEFAULT_HANDLER:
            exes = self.GetListItems()
            idx = evt.GetIndex()
            col = evt.GetColumn()
            nval = evt.GetLabel()
            if len(exes) >= idx:
                # Update an existing item
                if col == 0:
                    exes[idx] = (nval, exes[idx][1])
                else:
                    exes[idx] = (exes[idx][0], nval)
            else:
                # Add a new item
                # This should not happen
                exes.append((nval, nval))

            # Store the new values
            handler.SetCommands(exes)
            if len(exes) == 1:
                # Make sure default is set
                handler.SetDefault(exes[0])
            handler.StoreState()
            def_ch = self.FindWindowById(wx.ID_DEFAULT)
            def_ch.SetItems(handler.GetAliases())
            def_ch.SetStringSelection(handler.GetDefault())

    def SetListItems(self, items):
        """Set the items that are in the list control
        @param items: list of tuples (alias, cmd)

        """
        elist = self.FindWindowById(ID_EXECUTABLES)
        for exe in items:
            elist.Append(exe)

    def UpdateForHandler(self):
        """Update the panel for the current filetype handler"""
        handler = self.GetCurrentHandler()
        elist = self.FindWindowById(ID_EXECUTABLES)
        elist.DeleteAllItems()
        def_ch = self.FindWindowById(wx.ID_DEFAULT)
        def_ch.SetItems(handler.GetAliases())
        def_ch.SetStringSelection(handler.GetDefault())
        self.SetListItems(handler.GetCommands())
        # Enable control states
        transient = handler.meta.transient
        def_ch.Enable(not transient)
        elist.Enable(not transient)
        self.addbtn.Enable(not transient)
        self.delbtn.Enable(not transient)
        if self.infotxt.Show(transient):
            self.Layout()

#-----------------------------------------------------------------------------#

class OutputPanel(wx.Panel):
    """Output buffer settings panel"""
    def __init__(self, parent):
        super(OutputPanel, self).__init__(parent)

        # Layout
        self._bufftxt = None
        self.__DoLayout()

        # Event Handlers
        self.Bind(wx.EVT_CHECKBOX, self.OnCheck)
        self.Bind(eclib.EVT_COLORSETTER, self.OnColor)
        self._bufftxt.Bind(wx.EVT_KILL_FOCUS, self.OnLineBuffKillFocus)

    def __DoLayout(self):
        """Layout the controls"""
        msizer = wx.BoxSizer(wx.VERTICAL)
        sbox = wx.StaticBox(self, label=_("Text Colors"))
        boxsz = wx.StaticBoxSizer(sbox, wx.VERTICAL)

        # Launch Config
        cfg = Profile_Get(handlers.CONFIG_KEY, default=dict())

        # Actions Configuration
        clear_cb = wx.CheckBox(self, ID_AUTOCLEAR,
                               _("Automatically clear output buffer between runs"))
        clear_cb.SetValue(cfg.get('autoclear', False))
        error_cb = wx.CheckBox(self, ID_ERROR_BEEP,
                               _("Audible feedback when errors are detected"))
        error_cb.SetValue(cfg.get('errorbeep', False))
        wrap_cb = wx.CheckBox(self, ID_WRAP_OUTPUT,
                              _("Wrap lines in output buffer"))
        wrap_cb.SetValue(cfg.get('wrapoutput', False))
        buff_sz = wx.BoxSizer(wx.HORIZONTAL)
        buff_sz.Add(wx.StaticText(self, label=_("Line Buffering:")), 0,
                    wx.ALIGN_CENTER_VERTICAL)
        self._bufftxt = intctrl.IntCtrl(self, min=0, max=50000, allow_none=True)
        self._bufftxt.ToolTip = wx.ToolTip(_("0-50000 (0 unlimited)"))
        lbufcfg = max(0, cfg.get('linebuffer', DEFAULT_LINEBUFFER))
        self._bufftxt.Value = unicode(lbufcfg)
        buff_sz.Add(self._bufftxt, 0, wx.ALL, 5)

        # Colors
        colors = dict()
        for btn in COLOR_MAP.iteritems():
            cbtn = eclib.ColorSetter(self, btn[0], color=cfg.get(btn[1], wx.WHITE))
            colors[btn[0]] = cbtn

        flexg = wx.FlexGridSizer(5, 5, 5, 5)
        flexg.AddGrowableCol(1, 1)
        flexg.AddGrowableCol(3, 1)
        flexg.AddMany([# First Row
                       ((5, 5), 0), ((5, 5), 1),
                       (wx.StaticText(self, label=_("Foreground")), 0,
                        wx.ALIGN_CENTER),
                       ((5, 5), 1),
                       (wx.StaticText(self, label=_("Background")), 0,
                        wx.ALIGN_CENTER),
                       # Second Row
                       (wx.StaticText(self, label=_("Plain Text") + u":"), 0,
                        wx.ALIGN_CENTER_VERTICAL),
                       ((5, 5), 1),
                       (colors[ID_DEF_FORE], 0, wx.EXPAND),
                       ((5, 5), 1),
                       (colors[ID_DEF_BACK], 0, wx.EXPAND),
                       # Third Row
                       (wx.StaticText(self, label=_("Error Text") + u":"), 0,
                        wx.ALIGN_CENTER_VERTICAL),
                       ((5, 5), 1),
                       (colors[ID_ERR_FORE], 0, wx.EXPAND),
                       ((5, 5), 1),
                       (colors[ID_ERR_BACK], 0, wx.EXPAND),
                       # Fourth Row
                       (wx.StaticText(self, label=_("Info Text") + u":"), 0,
                        wx.ALIGN_CENTER_VERTICAL),
                       ((5, 5), 1),
                       (colors[ID_INFO_FORE], 0, wx.EXPAND),
                       ((5, 5), 1),
                       (colors[ID_INFO_BACK], 0, wx.EXPAND),
                       # Fifth Row
                       (wx.StaticText(self, label=_("Warning Text") + u":"), 0,
                        wx.ALIGN_CENTER_VERTICAL),
                       ((5, 5), 1),
                       (colors[ID_WARN_FORE], 0, wx.EXPAND),
                       ((5, 5), 1),
                       (colors[ID_WARN_BACK], 0, wx.EXPAND)])
        boxsz.Add(flexg, 0, wx.EXPAND)

        # Layout
        msizer.AddMany([((5, 5), 0),
                        (wx.StaticText(self, label=("Actions") + u":"), 0),
                        ((5, 5), 0), (clear_cb, 0),
                        ((5, 5), 0), (error_cb, 0),
                        ((5, 5), 0), (wrap_cb, 0),
                        ((5, 5), 0), (buff_sz, 0),
                        ((10, 10), 0), (wx.StaticLine(self), 0, wx.EXPAND),
                        ((10, 10), 0),
                        (boxsz, 1, wx.EXPAND)])
        hsizer = wx.BoxSizer(wx.HORIZONTAL)
        hsizer.AddMany([((5, 5), 0), (msizer, 1, wx.EXPAND), ((5, 5), 0)])
        self.SetSizer(hsizer)

    def OnCheck(self, evt):
        """Handle checkbox events"""
        e_id = evt.GetId()
        e_val = evt.GetEventObject().GetValue()
        cfg = Profile_Get(handlers.CONFIG_KEY, default=dict())
        if e_id == ID_AUTOCLEAR:
            cfg['autoclear'] = e_val
            Profile_Set(handlers.CONFIG_KEY, cfg)
        elif e_id == ID_ERROR_BEEP:
            cfg['errorbeep'] = e_val
            Profile_Set(handlers.CONFIG_KEY, cfg)
        elif e_id == ID_WRAP_OUTPUT:
            cfg['wrapoutput'] = e_val
            Profile_Set(handlers.CONFIG_KEY, cfg)
        else:
            evt.Skip()

    def OnColor(self, evt):
        """Handle color change events"""
        e_id = evt.GetId()
        color = COLOR_MAP.get(e_id, None)
        cfg = Profile_Get(handlers.CONFIG_KEY, default=dict())
        if color is not None:
            cfg[color] = evt.GetValue().Get()
            Profile_Set(handlers.CONFIG_KEY, cfg)
        else:
            evt.Skip()

    def OnLineBuffKillFocus(self, evt):
        self.UpdateLineBuffCfg()
        evt.Skip()

    def UpdateLineBuffCfg(self):
        """Update the line buffer configuration"""
        util.Log("[Launch][info] LineBuffer config updated")
        val = self._bufftxt.GetValue()
        if self._bufftxt.IsInBounds(val):
            cfg = Profile_Get(handlers.CONFIG_KEY, default=dict())
            cval = cfg.get('linebuffer', DEFAULT_LINEBUFFER)
            ival = int(val)
            if ival == 0:
                ival = -1
            if ival != cval:
                cfg['linebuffer'] = ival
                Profile_Set(handlers.CONFIG_KEY, cfg)

#-----------------------------------------------------------------------------#

class MiscPanel(wx.Panel):
    """Misc settings panel"""
    def __init__(self, parent):
        super(MiscPanel, self).__init__(parent)

        # Attributes
        self.savecb = None
        self.saveallcb = None

        # Layout
        self.__DoLayout()

        # Event Handlers
        self.Bind(wx.EVT_CHECKBOX, self.OnCheck)

    def __DoLayout(self):
        """Layout the panel"""
        sizer = wx.BoxSizer(wx.VERTICAL)
        cfg = Profile_Get(handlers.CONFIG_KEY, default=dict())

        # Editor options
        ebox = wx.StaticBox(self, label=_("Editor Options"))
        eboxsz = wx.StaticBoxSizer(ebox, wx.VERTICAL)
        lbl = _("Automatically save current file before running")
        self.savecb = wx.CheckBox(self, label=lbl)
        self.savecb.SetValue(cfg.get('autosave', False))
        lbl = _("Automatically save all open files before running")
        self.saveallcb = wx.CheckBox(self, label=lbl)
        self.saveallcb.SetValue(cfg.get('autosaveall', False))
        eboxsz.Add(self.savecb, 0, wx.ALL, 3)
        eboxsz.Add(self.saveallcb, 0, wx.ALL, 3)
        sizer.Add(eboxsz, 0, wx.EXPAND|wx.ALL, 5)

        self.SetSizer(sizer)

    def OnCheck(self, event):
        """Update the configuration"""
        e_obj = event.GetEventObject()
        value = e_obj.GetValue()
        cfg = Profile_Get(handlers.CONFIG_KEY, default=dict())
        if e_obj is self.savecb:
            cfg['autosave'] = value
            Profile_Set(handlers.CONFIG_KEY, cfg)
        elif e_obj is self.saveallcb:
            cfg['autosaveall'] = value
            Profile_Set(handlers.CONFIG_KEY, cfg)
        else:
            event.Skip()

#-----------------------------------------------------------------------------#
ID_BROWSE = wx.NewId()

class CommandListCtrl(eclib.EEditListCtrl):
    """Auto-width adjusting list for showing editing the commands"""
    def __init__(self, *args, **kwargs):
        super(CommandListCtrl, self).__init__(*args, **kwargs)

        # Attributes
        self._menu = None
        self._cindex = -1

        # Setup
        self.SetToolTipString(_("Click on an item to edit"))
#        pcol = _("Dir")
#        self.InsertColumn(0, pcol)
        self.InsertColumn(0, _("Alias"))
        self.InsertColumn(1, _("Executable Commands"))
#        self.SetColumnWidth(0, self.GetTextExtent(pcol)[0] + 5)

        # Event Handlers
        self.Bind(wx.EVT_LIST_ITEM_RIGHT_CLICK, self.OnContextClick)
        self.Bind(wx.EVT_MENU, self.OnMenu, id=ID_BROWSE)

    def OnContextClick(self, evt):
        """Handle right clicks"""
        if not self.GetSelectedItemCount():
            evt.Skip()
            return

        if self._menu is None:
            # Lazy init of menu
            self._menu = wx.Menu()
            self._menu.Append(ID_BROWSE, _("Browse..."))

        self._cindex = evt.GetIndex()
        self.PopupMenu(self._menu)

    def OnMenu(self, evt):
        """Handle Menu events"""
        e_id = evt.GetId()
        if e_id == ID_BROWSE:
            dlg = wx.FileDialog(self, _("Choose and executable"))
            if dlg.ShowModal() == wx.ID_OK:
                path = dlg.GetPath()
                if self._cindex >= 0:
                    self.SetStringItem(self._cindex, 1, path)
                    levt = wx.ListEvent(wx.wxEVT_COMMAND_LIST_END_LABEL_EDIT,
                                        self.GetId())
# TODO: ERR ><! there are no setters for index, column, and label...
#                    levt.Index = self._cindex
#                    levt.SetInt(self._cindex)
#                    levt.Column = 1
#                    levt.Label = path
                    # HACK set the member variables directly...
                    levt.m_itemIndex = self._cindex
                    levt.m_col = 1
                    levt.SetString(path)
                    wx.PostEvent(self.GetParent(), levt)
        else:
            evt.Skip()

#    def Append(self, entry):
#        """Append a row to the list. Overrides ListCtrl.Append to allow
#        for setting a bool on the first object to check or uncheck the
#        checkbox on the first column.
#        @param entry: tuple (bool, string, string)

#        """
#        check, alias, cmd = entry
#        wx.ListCtrl.Append(self, ('', alias, cmd))
#        self.CheckItem(self.GetItemCount() - 1, check)

#    def OpenEditor(self, col, row):
#        """Disable the editor for the first column
#        @param col: Column to edit
#        @param row: Row to edit

#        """
#        if col != 0:
#            listmix.TextEditMixin.OpenEditor(self, col, row)
#        else:
#            # Handle the checkbox click
#            self.CheckItem(row, not self.IsChecked(row))

#    def OnCheckItem(self, index, flag):
#        """Override CheckListMixin to update handlers
#        @param index: list index
#        @param flag: check or uncheck

#        """
#        parent = self.GetParent()
#        parent.UpdateCurrentHandler(index)
