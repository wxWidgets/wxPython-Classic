###############################################################################
# Name: testEBMLibMisc.py                                                     #
# Purpose: Unit tests for ebmlib misc utils                                   #
# Author: Cody Precord <cprecord@editra.org>                                  #
# Copyright: (c) 2010 Cody Precord <staff@editra.org>                         #
# License: wxWindows License                                                  #
###############################################################################

"""Unittest cases for testing the Misc Utilities module in ebmlib"""

__author__ = "Cody Precord <cprecord@editra.org>"
__svnid__ = "$Id$"
__revision__ = "$Revision$"

#-----------------------------------------------------------------------------#
# Imports
import unittest

# Module to test
import ebmlib

#-----------------------------------------------------------------------------#
# Test Class

class EBMLibMiscTest(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testMinMax(self):
        data = [(1, 2), (2, 1), (100, 200), (43, 41)]
        for val in data:
            res = ebmlib.MinMax(*val)
            self.assertTrue(res[0] < res[1])

