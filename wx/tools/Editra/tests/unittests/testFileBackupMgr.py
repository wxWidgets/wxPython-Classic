###############################################################################
# Name: testFileImpl.py                                                       #
# Purpose: Unit tests for FileObjectImpl                                      #
# Author: Cody Precord <cprecord@editra.org>                                  #
# Copyright: (c) 2009 Cody Precord <staff@editra.org>                         #
# License: wxWindows License                                                  #
###############################################################################

"""Unittests for ebmlib.FileObjectImpl class"""

__author__ = "Cody Precord <cprecord@editra.org>"
__svnid__ = "$Id$"
__revision__ = "$Revision$"

#-----------------------------------------------------------------------------#
# Imports
import wx
import os
import time
import unittest

# Local imports
import common

# Module(s) to test
import ebmlib

#-----------------------------------------------------------------------------#

class FileBackupMgrTest(unittest.TestCase):
    def setUp(self):
        self.bkup = ebmlib.FileBackupMgr(None, u"%s~")
        self.path = common.MakeTempFile("test.txt")
        self.file = ebmlib.FileObjectImpl(self.path)

    def tearDown(self):
        common.CleanTempDir()

    #---- Tests ----#

    def testGetBackupFilename(self):
        """Test getting the backup file name"""
        fname = self.bkup.GetBackupFilename(self.path)
        self.assertTrue(fname.endswith(u"~"))

    def testGetBackupWriter(self):
        """Test getting the backup writer function"""
        writer = self.bkup.GetBackupWriter(self.file)
        self.assertTrue(callable(writer))

    def testHasBackup(self):
        """Test checking if a backup exists"""
        self.assertFalse(self.bkup.HasBackup(self.path))
        self.bkup.MakeBackupCopy(self.path)
        self.assertTrue(self.bkup.HasBackup(self.path))

    def testIsBackupNewer(self):
        """Test checking that the backup is newer"""
        fname = common.MakeTempFile("test2.txt")
        fobj = ebmlib.FileObjectImpl(fname)
        self.assertFalse(self.bkup.IsBackupNewer(fname))
        time.sleep(1) # make sure modtime is different
        writer = self.bkup.GetBackupWriter(fobj)
        writer("TEST BACKUP")
        bname = self.bkup.GetBackupFilename(fname)
        self.assertTrue(self.bkup.IsBackupNewer(fname))

    def testMakeBackupCopy(self):
        """Test making a backup copy of a file"""
        fname = common.MakeTempFile("test3.txt")
        self.assertTrue(os.path.exists(fname))
        self.bkup.MakeBackupCopy(fname)
        bkup = self.bkup.GetBackupFilename(fname)
        self.assertTrue(os.path.exists(bkup))

    def testSetBackupFileTemplate(self):
        """Test setting the template for making backup files"""
        self.bkup.SetBackupFileTemplate(u"%s#")
        self.assertEquals(u"%s#", self.bkup.template)
        self.assertRaises(AssertionError, self.bkup.SetBackupFileTemplate, "!")
        self.assertRaises(AssertionError, self.bkup.SetBackupFileTemplate, "%s%s")

    def testSetHeader(self):
        """Test setting the file header"""
        self.bkup.SetHeader("Hello World")
        self.assertEquals("Hello World", self.bkup.header)
        self.assertRaises(AssertionError, self.bkup.SetHeader, "\n\nHELLO")

    def testBackupWithHeader(self):
        """Tests using the backup file header identifier option"""
        bkup = ebmlib.FileBackupMgr("SuperHeader", u"%s~")
        path = common.MakeTempFile("test_header.txt")
        self.assertTrue(bkup.MakeBackupCopy(path))
        bkupf = bkup.GetBackupFilename(path)
        self.assertTrue(os.path.exists(bkupf), "Invalid path: %s" % bkupf)
        txt = common.GetFileContents(bkupf)
        self.assertTrue(txt.startswith("SuperHeader"))

    def testBackupCustomDirectory(self):
        """"Test doing a backup to a custom directory"""
        bkup = ebmlib.FileBackupMgr()
        bkup.SetBackupDirectory(common.GetTempDir())
        self.assertTrue(bkup.MakeBackupCopy(__file__))
        path = bkup.GetBackupFilename(__file__)
        self.assertTrue(os.path.exists(path), "Path Fail: %s" % path)