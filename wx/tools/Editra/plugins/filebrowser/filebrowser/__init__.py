# -*- coding: utf-8 -*-
###############################################################################
# Name: __init__.py                                                           #
# Purpose: FileBrowser Plugin                                                 #
# Author: Cody Precord <cprecord@editra.org>                                  #
# Copyright: (c) 2007-2008 Cody Precord <staff@editra.org>                    #
# Licence: wxWindows Licence                                                  #
###############################################################################
# Plugin Meta
"""Adds a File Browser Sidepanel"""
__author__ = "Cody Precord"

#-----------------------------------------------------------------------------#
# Imports
import wx

# Libs from Editra
import iface
import plugin
import ed_fmgr
from profiler import Profile_Get, Profile_Set

# Local imports
import fbcfg
import browser

#-----------------------------------------------------------------------------#
# Globals
_ = wx.GetTranslation

#-----------------------------------------------------------------------------#
# Interface implementation
class FileBrowserPanel(plugin.Plugin):
    """Adds a filebrowser to the view menu"""
    plugin.Implements(iface.MainWindowI)

    def PlugIt(self, parent):
        """Adds the view menu entry and registers the event handler"""
        self._mw = parent
        self._log = wx.GetApp().GetLog()
        if self._mw != None:
            self._log("[filebrowser][info] Installing filebrowser plugin")
            
            #---- Create File Browser ----#
            # TODO hook in saved filter from profile
            self._filebrowser = browser.BrowserPane(self._mw)
            mgr = self._mw.GetFrameManager()
            mgr.AddPane(self._filebrowser, 
                        ed_fmgr.EdPaneInfo().Name(browser.PANE_NAME).\
                            Caption("File Browser").Left().Layer(1).\
                            CloseButton(True).MaximizeButton(True).\
                            BestSize(wx.Size(215, 350)))
            mgr.Update()

    def GetMinVersion(self):
        return "0.7.08" # all new file view controls and other interfaces needed

    def GetMenuHandlers(self):
        """Pass even handler for menu item to main window for management"""
        return [(browser.ID_FILEBROWSE, self._filebrowser.OnShowBrowser)]

    def GetUIHandlers(self):
        """Pass Ui handlers to main window for management"""
        return [(browser.ID_FILEBROWSE, self._filebrowser.OnUpdateMenu)]

#-----------------------------------------------------------------------------#

class FBConfigObject(plugin.PluginConfigObject):
    """Plugin configuration object for FileBrowser
    Provides configuration panel for plugin dialog.

    """
    def GetConfigPanel(self, parent):
        """Get the configuration panel for this plugin
        @param parent: parent window for the panel
        @return: wxPanel

        """
        return fbcfg.FBConfigPanel(parent)

    def GetLabel(self):
        """Get the label for this config panel
        @return string

        """
        return _("FileBrowser")

def GetConfigObject():
    return FBConfigObject()
