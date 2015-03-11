###############################################################################
# Name: testECLUtil.py                                                        #
# Purpose: Unit tests for the eclib.eclutil module                            #
# Author: Cody Precord <cprecord@editra.org>                                  #
# Copyright: (c) 2009 Cody Precord <staff@editra.org>                         #
# License: wxWindows License                                                  #
###############################################################################

"""Unittest cases for testing the eclib.eclutil functions"""

__author__ = "Cody Precord <cprecord@editra.org>"
__svnid__ = "$Id$"
__revision__ = "$Revision$"

#-----------------------------------------------------------------------------#
# Imports
import wx
import unittest

# Local modules
import common

# Module to test
import eclib

#-----------------------------------------------------------------------------#
# Test Class

class ECLUtilTest(unittest.TestCase):
    """Tests for the eclib.eclutil functions"""
    def setUp(self):
        self.app = wx.App(False)

    def tearDown(self):
        self.app.Destroy()

    #---- Tests ----#

    def testAdjustAlpha(self):
        """Test adjusting the alpha channel of a colour"""
        c = wx.Colour(255, 255, 255, 255)

        c = eclib.AdjustAlpha(c, 128)
        self.assertEquals(c.Alpha(), 128, "Alpha == %d" % c.Alpha())

        c = eclib.AdjustAlpha(c, 0)
        self.assertEquals(c.Alpha(), 0)

        self.assertRaises(ValueError, eclib.AdjustAlpha, c, -3)

    def testAdjustColour(self):
        """Test that a valid colour results are returned"""
        c = wx.Colour(125, 125, 125)

        # Check that the color was brightened
        c2 = eclib.AdjustColour(c, 50)
        self.assertTrue(sum(c.Get()) < sum(c2.Get()),
                        "Failed to lighten colour")

        # Check that the color was darkened
        c2 = eclib.AdjustColour(c, -50)
        self.assertTrue(sum(c.Get()) > sum(c2.Get()),
                        "Failed to darken colour")

    def testBestLabelColour(self):
        """Test getting the best label colour"""
        c = eclib.BestLabelColour(wx.BLACK)
        self.assertEquals((255, 255, 255), c.Get())

        c = eclib.BestLabelColour(wx.WHITE)
        self.assertEquals((0, 0, 0), c.Get())

    def testHexToRGB(self):
        """Test conversion of a hex value to a rgb tuple"""
        c = eclib.HexToRGB("000000")
        self.assertEquals(c, [0, 0, 0])

        c = eclib.HexToRGB("#000000")
        self.assertEquals(c, [0, 0, 0])

        c = eclib.HexToRGB("#0000FF")
        self.assertEquals(c, [0, 0, 255])

        c = eclib.HexToRGB("#FF00FF")
        self.assertEquals(c, [255, 0, 255])

        self.assertRaises(IndexError, eclib.HexToRGB, u"")
        self.assertRaises(ValueError, eclib.HexToRGB, "FF23GG")
