###############################################################################
# Name: cbconfig.py                                                           #
# Purpose: CodeBrowser UI                                                     #
# Author: Cody Precord <cprecord@editra.org>                                  #
# Copyright: (c) 2010 Cody Precord <staff@editra.org>                         #
# License: wxWindows License                                                  #
###############################################################################

"""
Provides configuration interface for CodeBrowser options

"""

__author__ = "Cody Precord <cprecord@editra.org>"
__svnid__ = "$Id$"
__revision__ = "$Revision$"

# Imports
import wx

# Editra Imports
from profiler import Profile_Set, Profile_Get

# Globals
_ = wx.GetTranslation
CB_PROFILE_KEY = "CodeBrowser.Config"
# Code Browser config identifiers
CB_SORT_OPTION = "CodeBrowser.SortOpt"
CB_ALPHA_SORT = "CodeBrowser.AlphaSort"
CB_LINENUM_SORT = "CodeBrowser.LineNumSort"

#-----------------------------------------------------------------------------#

class CBConfigPanel(wx.Panel):
    """Configuration panel for plugin manager dialog"""
    def __init__(self, parent):
        super(CBConfigPanel, self).__init__(parent)

        # Attributes
        self._sb = wx.StaticBox(self, label=_("Sorting"))
        self._sbs = wx.StaticBoxSizer(self._sb, wx.VERTICAL)
        self._alpha = wx.RadioButton(self, label=_("Alphabetically"),
                                     name=CB_ALPHA_SORT)
        self._linenum = wx.RadioButton(self, label=_("Line Number"),
                                       name=CB_LINENUM_SORT)

        # Layout
        self.__DoLayout()

        # Setup
        sortopt = GetSortOption()
        ctrl = self.FindWindowByName(sortopt)
        if ctrl:
            ctrl.SetValue(True)

        # Event Handlers
        self.Bind(wx.EVT_RADIOBUTTON, self.OnSortOpt)

    def __DoLayout(self):
        """Layout the window"""
        vsizer = wx.BoxSizer(wx.VERTICAL)
        self._sbs.Add(self._alpha, 0, wx.ALL, 3)
        self._sbs.Add(self._linenum, 0, wx.ALL, 3)
        vsizer.Add(self._sbs, 0, wx.EXPAND|wx.ALL, 8)
        self.SetSizer(vsizer)

    def OnSortOpt(self, event):
        """Handle changes to sorting options"""
        e_obj = event.GetEventObject()
        cfgobj = Profile_Get(CB_PROFILE_KEY, default=dict())
        if e_obj == self._alpha:
            cfgobj[CB_SORT_OPTION] = CB_ALPHA_SORT # Set Alpha mode
            Profile_Set(CB_PROFILE_KEY, cfgobj) # generate update msg
        elif e_obj == self._linenum:
            cfgobj[CB_SORT_OPTION] = CB_LINENUM_SORT # Set Line number mode
            Profile_Set(CB_PROFILE_KEY, cfgobj) # generate update msg
        else:
            event.Skip()

#-----------------------------------------------------------------------------#

def GetSortOption():
    """Get current sorting option"""
    cfgobj = Profile_Get(CB_PROFILE_KEY, default=dict())
    sortopt = cfgobj.get(CB_SORT_OPTION, CB_ALPHA_SORT)
    return sortopt
