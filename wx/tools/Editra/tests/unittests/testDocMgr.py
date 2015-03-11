###############################################################################
# Name: testDocMgr.py                                                         #
# Purpose: Unit tests for the doctools module.                                #
# Author: Cody Precord <cprecord@editra.org>                                  #
# Copyright: (c) 2009 Cody Precord <staff@editra.org>                         #
# License: wxWindows License                                                  #
###############################################################################

"""Unittest cases for testing doctools.DocPositionMgr"""

__author__ = "Cody Precord <cprecord@editra.org>"
__svnid__ = "$Id$"
__revision__ = "$Revision$"

#-----------------------------------------------------------------------------#
# Imports
import wx
import os
import unittest

# Module to test
import doctools

#-----------------------------------------------------------------------------#
# Test Class

class DocMgrTest(unittest.TestCase):
    def setUp(self):
        self.mgr = doctools.DocPositionMgr()

        # Populate some data
        self.mgr.AddRecord(('test.py', 20))
        self.mgr.AddRecord(('test2.py', 100))
        self.mgr.AddRecord(('test3.py', 1200))

    def tearDown(self):
        pass

    #---- Tests ----#
    def testGetBook(self):
        """Test that the path of the book is set"""
        book = self.mgr.GetBook()
        self.assertTrue(book is None, "book == %s" % book)

    def testGetPos(self):
        """Test fetching file positions from the manager."""
        self.assertEqual(self.mgr.GetPos('test2.py'), 100)
        self.assertEqual(self.mgr.GetPos('test3.py'), 1200)
        self.assertNotEqual(self.mgr.GetPos('test.py'), 1200)
        
        # Test trying to get an unknown file
        self.assertEqual(self.mgr.GetPos('fakefile.txt'), 0)

    #-- Test Position Navigator cache --#
    def testCanNavigate(self):
        """Test CanNavigateNext/Prev functions"""
        self.mgr.FlushNaviCache()
        self.assertFalse(self.mgr.CanNavigatePrev())
        self.assertFalse(self.mgr.CanNavigateNext())
        self.mgr.AddNaviPosition('test4.py', 200)
        self.assertTrue(self.mgr.CanNavigatePrev())
        self.mgr.AddNaviPosition('test5.py', 83)
        self.mgr.AddNaviPosition('test5.py', 45)
        self.mgr.AddNaviPosition('test6.py', 998)
        self.assertFalse(self.mgr.CanNavigateNext())
        self.mgr.GetPreviousNaviPos()
        self.mgr.GetPreviousNaviPos()
        self.assertTrue(self.mgr.CanNavigateNext())

    def testGetNextNaviPos(self):
        """Test Getting the next position in the history and retrieving
        items from the navigator cache

        """
        self.mgr.FlushNaviCache()
        self.mgr.AddNaviPosition('test4.py', 200)
        self.mgr.AddNaviPosition('test5.py', 83)
        self.mgr.AddNaviPosition('test5.py', 45)
        self.mgr.AddNaviPosition('test6.py', 998)

        # Move back to begining of cache
        self.mgr.GetPreviousNaviPos()
        self.mgr.GetPreviousNaviPos()
        self.mgr.GetPreviousNaviPos()
        self.mgr.GetPreviousNaviPos()

        pos = self.mgr.GetNextNaviPos() # next in cache
        self.assertEqual(pos[1], 200)

        pos = self.mgr.GetNextNaviPos()
        self.assertEqual(pos[1], 83)

        pos = self.mgr.GetNextNaviPos()
        self.assertEqual(pos[1], 45)

#        pos = self.mgr.GetNextNaviPos('test5.py')
#        self.assertEqual(pos[1], 83)

    def testGetPreviousNaviPos(self):
        """Test Getting the previous position in the history and retrieving
        items from the navigator cache

        """
        self.mgr.FlushNaviCache()
        self.mgr.AddNaviPosition('test4.py', 200)
        self.mgr.AddNaviPosition('test5.py', 83)
        self.mgr.AddNaviPosition('test5.py', 45)
        self.mgr.AddNaviPosition('test6.py', 998)

        pos = self.mgr.GetPreviousNaviPos()
        self.assertEqual(pos[1], 998)

        pos = self.mgr.GetPreviousNaviPos()
        self.assertEqual(pos[1], 45)

        pos = self.mgr.GetPreviousNaviPos()
        self.assertEqual(pos[1], 83)
