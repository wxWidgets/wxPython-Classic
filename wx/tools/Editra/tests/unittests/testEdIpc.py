###############################################################################
# Name: testEdIpc.py                                                          #
# Purpose: Unit tests for the IPC features from ed_ipc                        #
# Author: Cody Precord <cprecord@editra.org>                                  #
# Copyright: (c) 2010 Cody Precord <staff@editra.org>                         #
# License: wxWindows License                                                  #
###############################################################################

"""Unittest cases for testing the IPC functionality"""

__author__ = "Cody Precord <cprecord@editra.org>"
__svnid__ = "$Id:  $"
__revision__ = "$Revision:  $"

#-----------------------------------------------------------------------------#
# Imports
import wx
import os
import time
import unittest

# Local modules
import common

# Module to test
import ed_ipc

#-----------------------------------------------------------------------------#
# Test Class

class EdIpcTest(unittest.TestCase):
    """Tests for the ipc functions of ed_ipc"""
    def setUp(self):
        self.handler = wx.EvtHandler()
        self.port = ed_ipc.EDPORT + 1
        self.key = "foo"
        self.recieved = False
        self.server = ed_ipc.EdIpcServer(self.handler, self.key, self.port)

        self.handler.Bind(ed_ipc.EVT_COMMAND_RECV, self.OnIpcMsg)

    def tearDown(self):
        self.server.Shutdown()
        time.sleep(.5) # Give server time to shutdown
        self.handler.Unbind(ed_ipc.EVT_COMMAND_RECV)
        self.recieved = False

    def OnIpcMsg(self, event):
        self.recieved = True

    #---- Functional Tests ----#

    def testIpcCommand(self):
        xmlobj = ed_ipc.IPCCommand()
        arg = ed_ipc.IPCArg()
        arg.name = '-g'
        arg.value = 22
        xmlobj.arglist = [arg,] # GOTO line is only supported now
        f1 = ed_ipc.IPCFile()
        f1.value = "fileone.txt"
        f2 = ed_ipc.IPCFile()
        f2.value = "filetwo.txt"
        xmlobj.filelist = [f1, f2]
        serialized = xmlobj.GetXml()
        self.assertTrue(isinstance(serialized, basestring))

        newobj = ed_ipc.IPCCommand.parse(serialized)
        flist = newobj.filelist
        self.assertTrue(isinstance(flist, list))
        for f in xmlobj.filelist:
            self.assertTrue(f.value in [f2.value for f2 in flist])
        args = newobj.arglist
        for a in xmlobj.arglist:
            self.assertTrue(a.name in [a2.name for a2 in args])
            self.assertTrue(unicode(a.value) in [a3.value for a3 in args])

    def testSendCommands(self):
        command = ed_ipc.IPCCommand()
        rval = ed_ipc.SendCommands(command, self.key)
        self.assertTrue(rval)

#-----------------------------------------------------------------------------#
