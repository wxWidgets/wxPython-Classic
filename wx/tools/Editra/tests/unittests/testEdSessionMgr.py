###############################################################################
# Name: testEdSessionMgr.py                                                   #
# Purpose: Unit tests for the session manager class.                          #
# Author: Cody Precord <cprecord@editra.org>                                  #
# Copyright: (c) 2011 Cody Precord <staff@editra.org>                         #
# License: wxWindows License                                                  #
###############################################################################

"""Unittest cases for testing EdSessionMgr class"""

__author__ = "Cody Precord <cprecord@editra.org>"
__svnid__ = "$Id: $"
__revision__ = "$Revision: $"

#-----------------------------------------------------------------------------#
# Imports
import os
import unittest

import common

# Module to test
import ed_session

#-----------------------------------------------------------------------------#
# Test Class

class EdSessionMgrTest(unittest.TestCase):
    def setUp(self):
        self._mgr = ed_session.SessionManager(common.GetTempDir())
        common.CopyToTempDir(common.GetDataFilePath('__default.session'))

    def tearDown(self):
        common.CleanTempDir()

    #---- Tests ----#

    def testDeleteSession(self):
        """Test deleting a session file"""
        # 1. Create a session to delete
        files = ['foo.py', 'bar.py']
        rval = self._mgr.SaveSession('testdelete', files)
        path = self._mgr.PathFromSessionName('testdelete')
        self.assertTrue(os.path.exists(path))
        # 2. Delete it
        bDeleted = self._mgr.DeleteSession('testdelete')
        # 3. Make sure its been deleted
        self.assertTrue(bDeleted)
        self.assertTrue(not os.path.exists(path))

    def testGetSavedSessions(self):
        """Test retrieving the list of saved sessions"""
        slist = self._mgr.GetSavedSessions()
        self.assertTrue(isinstance(slist, list))
        self.assertEquals(len(slist), 1)

    def testLoadSession(self):
        """Test loading a serialized session file"""
        dsession = self._mgr.DefaultSession
        rval = self._mgr.LoadSession(dsession)
        self.assertTrue(isinstance(rval, list))
        self.assertEquals(len(rval), 8)

    def testSaveSession(self):
        """Test saving a session file to disk"""
        files = ['foo.py', 'bar.py']
        rval = self._mgr.SaveSession('foobar', files)
        self.assertTrue(rval) # Saved successfully
        loaded = self._mgr.LoadSession('foobar')
        self.assertEquals(len(loaded), 2)
        self.assertTrue('foo.py' in loaded)
        self.assertTrue('bar.py' in loaded)
        sessions = self._mgr.GetSavedSessions()
        self.assertTrue('foobar' in sessions)
        self.assertTrue('__default' in sessions)

    def testPathFromSessionName(self):
        path = self._mgr.PathFromSessionName('foobar')
        self.assertTrue(path.endswith(self._mgr.SessionExtension))
        self.assertTrue(path.startswith(self._mgr.SessionDir))

    def testSessionNameFromPath(self):
        path = common.GetTempFilePath('__default.session')
        name = self._mgr.SessionNameFromPath(path)
        self.assertEquals(name, '__default')
        # Test missing extension
        self.assertRaises(AssertionError,
                          self._mgr.SessionNameFromPath, path.rsplit('.', 1)[0])
