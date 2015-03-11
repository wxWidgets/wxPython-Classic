###############################################################################
# Name: testFileTypeChecker.py                                                #
# Purpose: Unit tests for ebmlib.FileTypeChecker                              #
# Author: Cody Precord <cprecord@editra.org>                                  #
# Copyright: (c) 2009 Cody Precord <staff@editra.org>                         #
# License: wxWindows License                                                  #
###############################################################################

"""Unittest cases for testing the FileTypeChecker class """

__author__ = "Cody Precord <cprecord@editra.org>"
__svnid__ = "$Id$"
__revision__ = "$Revision$"

#-----------------------------------------------------------------------------#
# Imports
import wx
import os
import unittest

# Local modules
import common

# Module to test
import ebmlib

#-----------------------------------------------------------------------------#
# Test Class

class FileTypeCheckerTest(unittest.TestCase):
    def setUp(self):
        self.fpath = common.GetDataFilePath(u'test_read_utf8.txt')
        self.bpath = common.GetDataFilePath(u'image_test.png')
        self.checker = ebmlib.FileTypeChecker()

    def tearDown(self):
        pass

    #---- Tests ----#
    def testIsBinary(self):
        """Test the IsBinary checker method"""
        self.assertTrue(self.checker.IsBinary(self.bpath))
        self.assertFalse(self.checker.IsBinary(self.fpath))

    def testIsBinaryBytes(self):
        """Test checking for binary bytes in a string"""
        f = open(self.bpath, 'rb')
        bytes = f.read()
        f.close()
        self.assertTrue(self.checker.IsBinaryBytes(bytes))
        f = open(self.fpath, 'rb')
        bytes = f.read()
        f.close()
        self.assertFalse(self.checker.IsBinaryBytes(bytes))

    def testIsReadableText(self):
        """Test if the file is a readable as text."""
        self.assertTrue(self.checker.IsReadableText(self.fpath))

