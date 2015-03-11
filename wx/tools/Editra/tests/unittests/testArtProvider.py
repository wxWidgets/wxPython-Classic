###############################################################################
# Name: testArtProvider.py                                                    #
# Purpose: Unit tests for the ArtProvider                                     #
# Author: Cody Precord <cprecord@editra.org>                                  #
# Copyright: (c) 2009 Cody Precord <staff@editra.org>                         #
# License: wxWindows License                                                  #
###############################################################################

"""Unittest cases for testing the artprovider"""

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
import ed_glob
import ed_art

#-----------------------------------------------------------------------------#
# Test Class

class ArtProviderTest(unittest.TestCase):
    """Tests the ArtProvider class"""
    def setUp(self):
        ap = ed_art.EditraArt()
        wx.ArtProvider.Push(ap)

    def tearDown(self):
        pass

    #---- Test Cases ----#

    def testGetBitmap(self):
        """Test getting a bitmap from the provider"""
        ap = wx.ArtProvider()
        bmp = ap.GetBitmap(str(ed_glob.ID_COPY), wx.ART_MENU)
        self.assertTrue(bmp.IsOk())
        self.assertEquals(bmp.GetSize(), (16, 16))

        bmp = ap.GetBitmap(str(ed_glob.ID_COPY), wx.ART_TOOLBAR)
        self.assertTrue(bmp.IsOk())

        bmp = ap.GetBitmap(str(-1), wx.ART_MENU)
        self.assertTrue(bmp.IsNull())
