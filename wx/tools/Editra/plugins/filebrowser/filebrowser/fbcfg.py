# -*- coding: utf-8 -*-
###############################################################################
# Name: fbcfg.py                                                              #
# Purpose: FileBrowser configuration                                          #
# Author: Cody Precord <cprecord@editra.org>                                  #
# Copyright: (c) 2012 Cody Precord <staff@editra.org>                         #
# License: wxWindows License                                                  #
###############################################################################

"""
FileBrowser configuration

"""

__author__ = "Cody Precord <cprecord@editra.org>"
__svnid__ = "$Id:  $"
__revision__ = "$Revision:  $"

#-----------------------------------------------------------------------------#
# Imports
import wx

# Editra libraries
import ed_glob
import ed_basewin
from profiler import Profile_Get, Profile_Set
import eclib

#-----------------------------------------------------------------------------#

_ = wx.GetTranslation

FB_PROF_KEY = "FileBrowser.Config"
FB_SYNC_OPT = "SyncNotebook"
FB_SHF_OPT = "ShowHiddenFiles"
FB_FILTER_OPT = "ExcludeFilePatterns"

FB_DEFAULT_FILTERS = ["*.pyc", "*.pyo", "*~", "*.bak", "*.a", "*.o", 
                      ".DS_Store", "*.svn", "*.git", "*.bzr"]

#-----------------------------------------------------------------------------#

class FBConfigDlg(ed_basewin.EdBaseDialog):
    def __init__(self, parent):
        super(FBConfigDlg, self).__init__(parent, title=_("FileBrowser Config"),
                                          style=wx.DEFAULT_DIALOG_STYLE|wx.RESIZE_BORDER)

        # Attributes
        self.Panel = FBConfigPanel(self)

        # Setup
        self.SetInitialSize()

#-----------------------------------------------------------------------------#

class FBConfigPanel(wx.Panel):
    def __init__(self, parent):
        super(FBConfigPanel, self).__init__(parent)

        # Attributes
        self._sb = wx.StaticBox(self, label=_("Actions"))
        self._sbs = wx.StaticBoxSizer(self._sb, wx.VERTICAL)
        self._sync_cb = wx.CheckBox(self,
                                    label=_("Synch tree with tab selection"),
                                    name=FB_SYNC_OPT)
        self._vsb = wx.StaticBox(self, label=_("View"))
        self._vsbs = wx.StaticBoxSizer(self._vsb, wx.VERTICAL)
        self._vhf_cb = wx.CheckBox(self,
                                   label=_("Show Hidden Files"),
                                   name=FB_SHF_OPT)
        self._fsb = wx.StaticBox(self, label=_("Filters"), name=FB_FILTER_OPT)
        self._fsbs = wx.StaticBoxSizer(self._fsb, wx.VERTICAL)
        self._filters = wx.ListBox(self, size=(-1, 100), style=wx.LB_SORT)
        bmp = wx.ArtProvider.GetBitmap(str(ed_glob.ID_ADD), wx.ART_MENU)
        self._addb = eclib.PlateButton(self, bmp=bmp)
        bmp = wx.ArtProvider.GetBitmap(str(ed_glob.ID_REMOVE), wx.ART_MENU)
        self._rmb = eclib.PlateButton(self, bmp=bmp)

        # Setup
        self.__DoLayout()
        self._sync_cb.Value = GetFBOption(FB_SYNC_OPT, True)
        self._vhf_cb.Value = GetFBOption(FB_SHF_OPT, False)
        self._filters.Items = GetFBOption(FB_FILTER_OPT, FB_DEFAULT_FILTERS)
        self._filters.ToolTip = wx.ToolTip(_("List of files patterns to exclude "
                                             "from view\nThe use of wildcards "
                                             "(*) are permitted."))
        self._addb.ToolTip = wx.ToolTip(_("Add filter"))
        self._rmb.ToolTip = wx.ToolTip(_("Remove selected filter"))

        # Event Handlers
        self.Bind(wx.EVT_BUTTON, self.OnButton)
        self.Bind(wx.EVT_CHECKBOX, self.OnCheck, self._sync_cb)
        self.Bind(wx.EVT_CHECKBOX, self.OnCheck, self._vhf_cb)

    def __DoLayout(self):
        sizer = wx.BoxSizer(wx.VERTICAL)
        self._sbs.Add(self._sync_cb, 0, wx.ALL, 5)
        sizer.Add(self._sbs, 0, wx.ALL, 5)
        self._vsbs.Add(self._vhf_cb, 0, wx.ALL, 5)
        sizer.Add(self._vsbs, 0, wx.ALL, 5)
        self._fsbs.Add(self._filters, 0, wx.EXPAND|wx.ALL, 5)
        bsizer = wx.BoxSizer(wx.HORIZONTAL)
        bsizer.Add(self._addb, 0, wx.ALL|wx.ALIGN_RIGHT, 5)
        bsizer.Add(self._rmb, 0, wx.ALL|wx.ALIGN_RIGHT, 5)
        self._fsbs.Add(bsizer, 0, wx.ALIGN_RIGHT)
        sizer.Add(self._fsbs, 0, wx.EXPAND|wx.ALL, 5)
        sizer.Add((10, 10), 0)
        self.SetSizer(sizer)

    def OnButton(self, evt):
        """Filter add/remove buttons"""
        bChanged = False
        if evt.EventObject is self._addb:
            txt = wx.GetTextFromUser(_("Enter new filter"), _("Add File Filters"),
                                     parent=self.TopLevelParent)
            txt = txt.strip()
            items = self._filters.GetItems()
            if txt and txt not in items:
                self._filters.Append(txt)
                bChanged = True
        else:
            # Remove filters
            sels = self._filters.GetSelections()
            for idx in reversed(sels):
                self._filters.Delete(idx)
                bChanged = True

        if bChanged:
            cfgobj = Profile_Get(FB_PROF_KEY, default=dict())
            cfgobj[evt.EventObject.Name] = self._filters.GetItems()
            Profile_Set(FB_PROF_KEY, cfgobj)

    def OnCheck(self, evt):
        """Update Profile"""
        e_obj = evt.GetEventObject()
        cfgobj = Profile_Get(FB_PROF_KEY, default=dict())
        if e_obj in (self._vhf_cb, self._sync_cb):
            cfgobj[e_obj.Name] = e_obj.Value
            Profile_Set(FB_PROF_KEY, cfgobj)
        else:
            evt.Skip()

#-----------------------------------------------------------------------------#

def GetFBOption(opt, default=None):
    """Get FileBrowser option from the configuration"""
    cfgobj = Profile_Get(FB_PROF_KEY, default=dict())
    return cfgobj.get(opt, default)
