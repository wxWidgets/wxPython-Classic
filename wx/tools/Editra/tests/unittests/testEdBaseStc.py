###############################################################################
# Name: testSynGlob.py                                                        #
# Purpose: Unit tests for ed_basestc                                          #
# Author: Cody Precord <cprecord@editra.org>                                  #
# Copyright: (c) 2012 Cody Precord <staff@editra.org>                         #
# License: wxWindows License                                                  #
###############################################################################

"""Unittest cases for testing the STC base class"""

__author__ = "Cody Precord <cprecord@editra.org>"
__svnid__ = "$Id:  $"
__revision__ = "$Revision:  $"

#-----------------------------------------------------------------------------#
# Imports
import os
import unittest
import common

# Module to test
import ed_glob
import ed_basestc

#-----------------------------------------------------------------------------#
# Test Class

class EdBaseStcTest(unittest.TestCase):
    def setUp(self):
        # Setup config
        ed_glob.CONFIG['STYLES_DIR'] = common.GetStylesDir()

        # Create control(s)
        self.frame = common.TestFrame(None)
        self.stc = ed_basestc.EditraBaseStc(self.frame)

    def tearDown(self):
        self.frame.Destroy()

    #---- Test Cases ----#

    def testAddLine(self):
        """Test the AddLine method"""
        ccount = self.stc.LineCount
        cpos = self.stc.CurrentLine
        self.stc.AddLine() # add after
        self.assertTrue(ccount == (self.stc.LineCount - 1)) # should be 1 new line
        self.assertTrue(cpos == (self.stc.CurrentLine - 1),
                        repr((cpos, self.stc.CurrentLine))) # cursor position should move to new line
        ccount = self.stc.LineCount
        cpos = self.stc.CurrentLine
        # Test add line above current one
        self.stc.AddLine(before=True)
        self.assertTrue(ccount == (self.stc.LineCount - 1)) # should be 1 new line
        self.assertTrue(cpos == self.stc.CurrentLine, 
                        repr((cpos, self.stc.CurrentLine))) # cursor position should be same line
        # TODO: add tests for indent

    def testGetEOLChar(self):
        """Test that correct eol character is returned"""
        fresh_stc = ed_basestc.EditraBaseStc(self.frame)
        eolchr = fresh_stc.GetEOLChar()
        fresh_stc.Destroy()
        self.assertEquals(eolchr, os.linesep)

    def testLoadFile(self):
        """Test loading a file into the control"""
        path = common.GetDataFilePath("syntax.xml")
        self.assertTrue(self.stc.LoadFile(path))
        self.assertFalse(self.stc.GetReadOnly()) # should be good text
