###############################################################################
# Name: testContextMenuManager.py                                             #
# Purpose: Unit tests for ebmlib.ContextMenuManager                           #
# Author: Cody Precord <cprecord@editra.org>                                  #
# Copyright: (c) 2010 Cody Precord <staff@editra.org>                         #
# License: wxWindows License                                                  #
###############################################################################

"""Unittest cases for testing the ebmlib.ContextMenuManager"""

__author__ = "Cody Precord <cprecord@editra.org>"
__svnid__ = "$Id$"
__revision__ = "$Revision$"

#-----------------------------------------------------------------------------#
# Imports
import unittest
import wx

# Module to test
import ebmlib

#-----------------------------------------------------------------------------#
# Test Class

class ContextMenuManagerTest(unittest.TestCase):

    def setUp(self):
        self.cmgr = ebmlib.ContextMenuManager()

    def tearDown(self):
        self.cmgr.Clear()

    def testMenu(self):
        self.assertTrue(self.cmgr.Menu is None)
        self.cmgr.SetMenu(wx.Menu())
        self.assertTrue(self.cmgr.Menu is not None)
        self.assertTrue(isinstance(self.cmgr.Menu, wx.Menu))

    def testPosition(self):
        self.assertTrue(isinstance(self.cmgr.Position, tuple))
        self.assertTrue(len(self.cmgr.Position) == 2)
        self.assertTrue(isinstance(self.cmgr.Position[0], int))
        self.assertTrue(isinstance(self.cmgr.Position[1], int))
        self.cmgr.SetPosition((20, 20))
        self.assertTrue(self.cmgr.Position == (20, 20))

    def testAddHandler(self):
        def foo():
            pass
        self.cmgr.AddHandler(100, foo)
        hndlr = self.cmgr.GetHandler(100)
        self.assertTrue(callable(hndlr))

    def testUserData(self):
        self.cmgr.SetUserData('foo', 100)
        self.assertTrue(self.cmgr.GetUserData('foo') == 100)
        self.assertTrue(self.cmgr.GetUserData('asdf') is None)

