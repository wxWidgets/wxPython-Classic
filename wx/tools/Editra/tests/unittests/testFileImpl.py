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
import os
import types
import unittest

# Local unittest imports
import common

# Module(s) to test
import ebmlib

#-----------------------------------------------------------------------------#

class FileImplTest(unittest.TestCase):
    def setUp(self):
        self.path = common.GetDataFilePath(u'test_read_utf8.txt')
        self.file = ebmlib.FileObjectImpl(self.path)
        self.mtime = ebmlib.GetFileModTime(self.path)

    def tearDown(self):
        self.file.Close()

    #---- Tests ----#

    def testClone(self):
        """Test cloning the file object"""
        fobj = self.file.Clone()
        self.assertTrue(fobj.Path == self.file.Path)
        self.assertTrue(fobj.ModTime == self.file.ModTime)
        self.assertTrue(fobj.ReadOnly == self.file.ReadOnly)

    def testRead(self):
        """Test reading from the file and getting the text"""
        txt = self.file.Read()
        self.assertTrue(len(txt))

    def testExists(self):
        """Test if the file exists"""
        self.assertTrue(self.file.Exists())
        nfile = ebmlib.FileObjectImpl('some_fake_file')
        self.assertFalse(nfile.Exists())

    def testGetExtension(self):
        """Test getting the file extension"""
        self.assertTrue(self.file.GetExtension() == 'txt')

    def testGetLastError(self):
        """Test fetching last file op error"""
        self.assertEquals(self.file.GetLastError(), u"None")

        # Test that errors come back as Unicode
        self.file.SetLastError("OS CALL FAILED")
        errmsg = self.file.GetLastError()
        self.assertTrue(ebmlib.IsUnicode(errmsg), "Error not decoded properly!")

        # Tests path for error message that is already Unicode
        self.file.SetLastError(u"FAIL!")
        errmsg = self.file.GetLastError()
        self.assertEquals(errmsg, u"FAIL!")

    def testGetPath(self):
        """Test getting the files path"""
        self.assertTrue(self.file.GetPath() == self.path)

    def testGetModTime(self):
        """Test getting the files last modification time"""
        self.file.ModTime = self.mtime
        mtime = self.file.ModTime
        self.assertTrue(mtime == self.mtime, "Modtime was: " + str(mtime))
        self.assertTrue(mtime == self.file.ModTime)

    def testIsOpen(self):
        """Test checking the state of the file"""
        self.assertFalse(self.file.IsOpen())

    def testIsReadOnly(self):
        """Test if the file is read only or not"""
        self.assertFalse(self.file.IsReadOnly(), "File is readonly")
        self.assertEqual(self.file.IsReadOnly(), self.file.ReadOnly)

    def testGetSize(self):
        """Test fetching the file size"""
        self.assertTrue(self.file.GetSize() > 0)
