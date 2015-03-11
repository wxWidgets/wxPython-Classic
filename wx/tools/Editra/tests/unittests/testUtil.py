###############################################################################
# Name: testUtil.py                                                           #
# Purpose: Unit tests for util.py module in Editra/src                        #
# Author: Cody Precord <cprecord@editra.org>                                  #
# Copyright: (c) 2008 Cody Precord <staff@editra.org>                         #
# License: wxWindows License                                                  #
###############################################################################

"""Unittest cases for testing the various Utility functions in
the util module.

"""

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
import util

#-----------------------------------------------------------------------------#
# Test Class

class UtilTest(unittest.TestCase):
    def setUp(self):
        self.fpath = common.GetDataFilePath(u'test_read_utf8.txt')
        self.bpath = common.GetDataFilePath(u'image_test.png')

    def tearDown(self):
        pass

    #---- Tests ----#

    def testFilterFiles(self):
        """Test the file filter function"""
        rlist = util.FilterFiles([self.fpath, self.bpath])
        self.assertEquals(len(rlist), 1)

    def testGetAllEncodings(self):
        """Test getting the list of available system encodings"""
        encs = util.GetAllEncodings()
        self.assertTrue(len(encs) > 0)

        for enc in encs:
            self.assertTrue(isinstance(enc, basestring))

    def testGetFileManagerCmd(self):
        """Test retrieving the systems filemanager command"""
        cmd = util.GetFileManagerCmd()
        self.assertTrue(isinstance(cmd, basestring))

        self.assertTrue(len(cmd) > 0)
