###############################################################################
# Name: testHistoryCache.py                                                   #
# Purpose: Unit tests for the base KeyHandler class                           #
# Author: Cody Precord <cprecord@editra.org>                                  #
# Copyright: (c) 2009 Cody Precord <staff@editra.org>                         #
# License: wxWindows License                                                  #
###############################################################################

"""Unittest cases for testing the HistoryCache class"""

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

class HistoryCacheTest(unittest.TestCase):
    def setUp(self):
        self.cache = ebmlib.HistoryCache()

    def tearDown(self):
        pass

    #---- Tests ----#

    def testClear(self):
        """Test clearning the cache"""
        self.cache.PutItem("hello")
        self.assertTrue(self.cache.GetSize() > 0)
        self.cache.Clear()
        self.assertTrue(self.cache.GetSize() == 0)

    def testGetSize(self):
        """Test GetSize method"""
        self.cache.Clear()
        self.assertTrue(self.cache.GetSize() == 0)
        self.cache.PutItem("hello")
        self.assertTrue(self.cache.GetSize() == 1)

    def testGetMaxSize(self):
        """Test retrieving the max size"""
        self.assertTrue(self.cache.GetMaxSize() == ebmlib.HIST_CACHE_UNLIMITED)
        self.cache.SetMaxSize(25)
        self.assertTrue(self.cache.GetMaxSize() == 25)

    def testGetNextItem(self):
        """Test getting the next item in the cache"""
        self.cache.Clear()
        self.cache.PutItem("Hello1")
        self.cache.PutItem("Hello2")
        self.cache.PutItem("Hello3")
        self.cache.PutItem("Hello4")

        # Should be at end of the cache right now
        self.assertTrue(self.cache.GetNextItem() == None, "Found item when none was expected")

        # modify internal pointer for testing purposes
        self.cache.cpos = -1
        item = self.cache.GetNextItem()
        self.assertTrue(item == "Hello1", "Item is %s, pos==%d" % (item, self.cache.cpos))
        item = self.cache.GetNextItem()
        self.assertTrue(item == "Hello2", "Item is %s, pos==%d" % (item, self.cache.cpos))
        item = self.cache.GetNextItem()
        self.assertTrue(item == "Hello3", "Item is %s, pos==%d" % (item, self.cache.cpos))
        item = self.cache.GetNextItem()
        self.assertTrue(item == "Hello4", "Item is %s, pos==%d" % (item, self.cache.cpos))

    def testGetPreviousItem(self):
        """Test getting the previous item in the cache"""
        self.cache.Clear()
        self.cache.PutItem("Hello1")
        self.cache.PutItem("Hello2")
        self.cache.PutItem("Hello3")
        self.cache.PutItem("Hello4")

        self.assertTrue(self.cache.GetPreviousItem() == "Hello4")
        self.assertTrue(self.cache.GetPreviousItem() == "Hello3")
        self.assertTrue(self.cache.GetPreviousItem() == "Hello2")
        self.assertTrue(self.cache.GetPreviousItem() == "Hello1")
        # Should be at beginning of the cache right now
        self.assertTrue(self.cache.GetPreviousItem() == None, "Found item when none was expected")

    def testHasNext(self):
        """Test checking if there are more items in the cache to the right"""
        self.cache.Clear()
        self.assertFalse(self.cache.HasNext(), "HasNext is True in empty cache")
        self.cache.PutItem("Hello1")
        self.cache.GetPreviousItem()
        self.assertTrue(self.cache.HasNext(), "Pos:%d, Size:%d" % (self.cache.cpos, self.cache.GetSize()))

    def testHasPrevious(self):
        """Test checking if there are more items in the cache to the left"""
        self.cache.Clear()
        self.cache.PutItem("Hello1")
        self.assertTrue(self.cache.HasPrevious())
        self.cache.GetPreviousItem()
        self.assertFalse(self.cache.HasPrevious())

    def testPeek(self):
        """Test peeking at the next/prev item in the cache."""
        self.cache.Clear()
        self.assertEquals(self.cache.PeekNext(), None)
        self.assertEquals(self.cache.PeekNext(), None)
        self.assertEquals(self.cache.PeekPrevious(), None)
        self.assertEquals(self.cache.PeekPrevious(), None)
        self.cache.PutItem("hello")
        self.cache.PutItem("hello1")
        self.assertEquals(self.cache.PeekPrevious(), "hello1")
        self.assertEquals(self.cache.PeekNext(), None)
        self.cache.PutItem("hello2")
        self.cache.PutItem("hello3")
        self.assertEquals(self.cache.PeekPrevious(), "hello3")
        self.assertEquals(self.cache.PeekPrevious(), "hello3")
        self.cache.GetPreviousItem() # move back one position
        self.assertEquals(self.cache.PeekPrevious(), "hello2")
        self.assertEquals(self.cache.PeekPrevious(), "hello2")
        self.assertEquals(self.cache.PeekNext(), "hello3")
        self.assertEquals(self.cache.PeekNext(), "hello3")

    def testPutItem(self):
        """Test putting an item in the cache"""
        self.cache.Clear()
        self.cache.PutItem("hello")
        self.assertTrue(self.cache.GetSize() == 1)
        self.cache.PutItem("hello2")
        self.cache.PutItem("hello3")
        self.assertTrue(self.cache.GetSize() == 3)

    def testSetMaxSize(self):
        """Test setting the max size of the cache"""
        self.cache.Clear()

        # Test invalid cache size
        self.assertRaises(AssertionError, self.cache.SetMaxSize, 0)

        # Test setting a valid cache size
        self.cache.SetMaxSize(3)
        self.assertEquals(self.cache.GetMaxSize(), 3)

        # Ensure max size is enforced
        self.cache.PutItem("Hello1")
        self.cache.PutItem("Hello2")
        self.cache.PutItem("Hello3")
        self.assertEquals(self.cache.GetSize(), 3)
        self.cache.PutItem("Hello4")
        self.assertEquals(self.cache.GetSize(), 3)

        # Test that correct items are still on the cache
        self.assertTrue(self.cache.GetPreviousItem(), "Hello4")
        self.assertTrue(self.cache.GetPreviousItem(), "Hello3")
        self.assertTrue(self.cache.GetPreviousItem(), "Hello2")
        item = self.cache.GetPreviousItem()
        self.assertTrue(item == None, "Item should be None: %s" % item)
