###############################################################################
# Name: __init__.py                                                           #
# Purpose: Hello World Sample Plugin                                          #
# Author: Cody Precord <cprecord@editra.org>                                  #
# Copyright: (c) 2007 Cody Precord <staff@editra.org>                         #
# Licence: wxWindows Licence                                                  #
###############################################################################
"""Adds Hello World to the View Menu"""
__author__ = "Cody Precord"
__version__ = "0.3"

import wx
import iface
import plugin

_ = wx.GetTranslation
#-----------------------------------------------------------------------------#

ID_HELLO = wx.NewId()
class Hello(plugin.Plugin):
    """Adds Hello World to the View Menu"""
    plugin.Implements(iface.MainWindowI)
    def PlugIt(self, parent):
        """Adds the view menu entry registers the event handler"""
        if parent:
            # This will let you use Editra's loggin system
            self._log = wx.GetApp().GetLog()
            self._log("[hello][info] Installing Hello World")
            vm = parent.GetMenuBar().GetMenuByName("view")
            vm.Append(ID_HELLO, _("Hello World"), 
                      _("Open a Hello World Dialog"))
        else:
            self._log("[hello][err] Failed to install hello plugin")

    def GetMenuHandlers(self):
        """This is used to register the menu handler with the app and
        associate the event with the parent window. It needs to return
        a list of ID/Handler pairs for each menu handler that the plugin
        is providing.

        """
        return [(ID_HELLO, SayHello)]

    def GetUIHandlers(self):
        """This is used to register the update ui handler with the app and
        associate the event with the parent window. This plugin doesn't use
        the UpdateUI event so it can just return an empty list.

        """
        return list()

#-----------------------------------------------------------------------------#
# This is the handler for opening the hello world dialog it is defined
# outside of the plugins class instance because that class is created
# as a singleton so if the event handler is part of that class there are
# problems with using when multiple windows are open.

def SayHello(evt):
    """Opens the hello dialog"""
    if evt.GetId() == ID_HELLO:
        dlg = wx.MessageBox(_("Editra's Hello Plugin Says Hello"), 
                            _("Hello World"))
    else:
        evt.Skip()

