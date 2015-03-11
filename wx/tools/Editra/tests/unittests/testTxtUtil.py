###############################################################################
# Name: testTxtUtil.py                                                        #
# Purpose: Unit tests for the txtutil functions of ebmlib                     #
# Author: Cody Precord <cprecord@editra.org>                                  #
# Copyright: (c) 2009 Cody Precord <staff@editra.org>                         #
# License: wxWindows License                                                  #
###############################################################################

"""Unittest cases for testing the txtutil functions"""

__author__ = "Cody Precord <cprecord@editra.org>"
__svnid__ = "$Id$"
__revision__ = "$Revision$"

#-----------------------------------------------------------------------------#
# Imports
import unittest

# Local modules
import common

# Module to test
import ebmlib

#-----------------------------------------------------------------------------#
# Test Class

class TxtUtilTest(unittest.TestCase):
    """Tests for the fileutil functions of ebmlib"""
    def setUp(self):
        pass

    def tearDown(self):
        pass

    #---- Unittests Test Cases----#

    def testIsUnicode(self):
        """Test checking if a string is unicode or not"""
        self.assertTrue(ebmlib.IsUnicode(u"HELLO"))
        self.assertFalse(ebmlib.IsUnicode("Hello"))

