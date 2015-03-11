###############################################################################
# Name: testFileUtil.py                                                       #
# Purpose: Unit tests for the fileutil functions of ebmlib                    #
# Author: Cody Precord <cprecord@editra.org>                                  #
# Copyright: (c) 2009 Cody Precord <staff@editra.org>                         #
# License: wxWindows License                                                  #
###############################################################################

"""Unittest cases for testing the fileutil functions"""

__author__ = "Cody Precord <cprecord@editra.org>"
__svnid__ = "$Id$"
__revision__ = "$Revision$"

#-----------------------------------------------------------------------------#
# Imports
import os
import platform
import unittest

# Local modules
import common

# Module to test
import ebmlib

#-----------------------------------------------------------------------------#

ISWINDOWS = platform.system().lower() in ('windows', 'microsoft')

#-----------------------------------------------------------------------------#
# Test Class

class FileUtilTest(unittest.TestCase):
    """Tests for the fileutil functions of ebmlib"""
    def setUp(self):
        self.ddir = common.GetDataDir()
        self.tdir = common.GetTempDir()
        self.fpath = common.GetDataFilePath(u'test_read_utf8.txt')

    def tearDown(self):
        common.CleanTempDir()

    #---- Tests ----#

    def testAddFileExtension(self):
        """Test adding file extension to a filename"""
        name = ebmlib.AddFileExtension('foo', 'py')
        self.assertEquals('foo.py', name)
        name = ebmlib.AddFileExtension('bar', '.py')
        self.assertEquals('bar.py', name)
        name = ebmlib.AddFileExtension('foobar.py', 'py')
        self.assertEquals('foobar.py', name)

    def testComparePaths(self):
        """Test functionality of ComparePaths function"""
        # Test case sensitivity
        if ISWINDOWS:
            self.assertTrue(ebmlib.ComparePaths("C:\\Windows", "C:\\WINDOWS"))
            self.assertTrue(ebmlib.ComparePaths("C:\\Windows", "C:\\Windows"))
        else:
            self.assertFalse(ebmlib.ComparePaths("/usr/bin", "/usr/BIN"))
            self.assertTrue(ebmlib.ComparePaths("/usr/bin", "/usr/bin"))

        # Test wacky path strings
        if ISWINDOWS:
            self.assertTrue(ebmlib.ComparePaths("C:\\Windows\\..\\", "C:\\"))
        else:
            self.assertTrue(ebmlib.ComparePaths("/usr/../", "/"))

    def testGetAbsPath(self):
        """Test getting a files absolute path"""
        path = os.path.join(u'.', u'data')
        self.assertEquals(self.ddir, ebmlib.GetAbsPath(path))

        # Test short path to long name transform on windows
        if ISWINDOWS:
            path = "c:\\documents and settings"
            spath = "C:\\DOCUME~1"
            self.assertEquals(path, ebmlib.GetAbsPath(spath).lower(), 
                              "Missing win32api extension modules?")

    def testGetFileExtension(self):
        """Test getting a files extension"""
        ext = ebmlib.GetFileExtension(u'hello.txt')
        self.assertTrue(ext == u'txt')

        ext = ebmlib.GetFileExtension(u'hello.py')
        self.assertTrue(ext == u'py')

        ext = ebmlib.GetFileExtension(u'hello.txt.tmp')
        self.assertTrue(ext == u'tmp')

    def testGetFileModTime(self):
        """Test getting a files modtime"""
        mtime = ebmlib.GetFileModTime(self.fpath)
        self.assertNotEqual(mtime, 0, "Mtime was: " + str(mtime))

    def testGetFileName(self):
        """Test that getting the file name from a string returns the correct
        string.

        """
        roots = (("Home", "foo", "projects"), ("usr", "bin"),
                 ("Users", "bar", "Desktop"))
        fname = "test.py"
        paths = [os.path.join(os.sep.join(root), fname) for root in roots]
        for path in paths:
            self.assertEqual(fname, ebmlib.GetFileName(path),
                             "ebmlib.GetFileName(%s) != %s" % (path, fname))

    def testGetFileSize(self):
        """Test getting a files size"""
        self.assertTrue(ebmlib.GetFileSize(self.fpath) != 0)
        self.assertTrue(ebmlib.GetFileSize(u'SomeFakeFile.txt') == 0)

    def testPathExists(self):
        """Test if a path exists"""
        path = common.GetDataFilePath(u'test_read_utf8.txt')
        fail = common.GetDataFilePath(u'fake_file.txt')

        # Test regular file paths
        self.assertTrue(ebmlib.PathExists(path))
        self.assertFalse(ebmlib.PathExists(fail))

        # Test URI
        path = u"file://" + path
        fail = u"file://" + fail
        self.assertTrue(ebmlib.PathExists(path))
        self.assertFalse(ebmlib.PathExists(fail))

    def testGetPathFromURI(self):
        """Test getting a real file path from a file:// uri"""
        if ISWINDOWS:
            path = ebmlib.GetPathFromURI(u"file://C:/Users/test/test.txt")
            self.assertEquals(path, u"C:\\Users\\test\\test.txt")
        else:
            path = ebmlib.GetPathFromURI(u"file://Users/test/test.txt")
            self.assertEquals(path, u"/Users/test/test.txt")

            path = ebmlib.GetPathFromURI(u"/Users/test")
            self.assertEquals(path, u"/Users/test")

    def testGetPathName(self):
        """Test that getting the path name from a string returns the correct
        string.

        """
        roots = (("Home", "foo", "projects"), ("usr", "bin"),
                 ("Users", "bar", "Desktop"))
        fname = "test.py"
        paths = [os.sep.join(root) for root in roots]
        for path in paths:
            tmp = os.path.join(path, fname)
            result = ebmlib.GetPathName(tmp)
            self.assertEqual(path, result,
                             "%s != %s" % (result, path))

    def testGetUniqueName(self):
        """Test getting a unique file name at a given path"""
        path = ebmlib.GetUniqueName(self.ddir, u'test_read_utf8.txt')
        self.assertTrue(path != self.fpath)

        # File that does not yet exist
        path = common.GetDataFilePath(u'newfile.txt')
        uname = ebmlib.GetUniqueName(self.ddir, u'newfile.txt')
        self.assertTrue(path == uname)

    def testMakeNewFile(self):
        """Test the MakeNewFile utility"""
        result = ebmlib.MakeNewFile(self.tdir, u'test_new_file.txt')
        self.assertTrue(result[0])
        self.assertTrue(os.path.exists(result[1]))
        
        result2 = ebmlib.MakeNewFile(self.tdir, u'test_new_file.txt')
        self.assertTrue(result2[1])
        self.assertTrue(result[1] != result2[1])

    def testMakeNewFolder(self):
        """Test the MakeNewFoloder utility"""
        result = ebmlib.MakeNewFolder(self.tdir, u'test_new_folder')
        self.assertTrue(result[0])
        self.assertTrue(os.path.exists(result[1]))
        
        result2 = ebmlib.MakeNewFolder(self.tdir, u'test_new_folder')
        self.assertTrue(result2[1])
        self.assertTrue(result[1] != result2[1])

    def testWhich(self):
        """Test the Which function"""
        # NOTE: this may produce false positives on some systems
        if ISWINDOWS:
            prog = 'ping.exe'
        else:
            prog = 'ping'
        exe = ebmlib.Which(prog)
        self.assertNotEqual(exe, None)
