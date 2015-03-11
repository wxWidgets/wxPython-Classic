###############################################################################
# Name: testCycleCache.py                                                     #
# Purpose: Unit tests for the CycleCache                                      #
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
import unittest

# Module to test
import ebmlib

#-----------------------------------------------------------------------------#
# Test Class

class CycleCacheTest(unittest.TestCase):
    def setUp(self):
        self.cache = ebmlib.CycleCache(5)

    def tearDown(self):
        pass

    def testClear(self):
        """Test clearing the cache"""
        self.cache.PutItem("hello")
        self.cache.PutItem("hello1")
        self.assertTrue(self.cache.GetCurrentSize())
        self.cache.Clear()
        self.assertTrue(self.cache.GetCurrentSize() == 0)

    def testGetNext(self):
        """Test getting items from the cache"""
        self.cache.Clear()
        self.cache.PutItem("hello")
        self.cache.PutItem("hello1")
        self.cache.PutItem("hello2")
        self.cache.PutItem("hello3")
        self.cache.PutItem("hello4")
        self.assertEquals(self.cache.GetNext(), "hello4")
        self.assertEquals(self.cache.GetNext(), "hello3")
        self.assertEquals(self.cache.GetNext(), "hello2")
        self.assertEquals(self.cache.GetNext(), "hello1")
        self.assertEquals(self.cache.GetNext(), "hello")
        self.assertEquals(self.cache.GetNext(), "hello4")
        self.assertEquals(self.cache.GetNext(), "hello3")
        self.assertEquals(self.cache.GetNext(), "hello2")

    def testPeek(self):
        """Test peeking in the cache"""
        self.cache.Clear()
        self.cache.PutItem("hello")
        self.cache.PutItem("hello1")
        self.cache.PutItem("hello2")
        self.assertEquals(self.cache.PeekNext(), "hello2")
        self.assertEquals(self.cache.PeekPrev(), "hello")

    def testPutItem(self):
        """Test putting items in the cache"""
        self.cache.Clear()
        self.cache.PutItem("hello")
        self.assertTrue(self.cache.GetCurrentSize() == 1)
        self.cache.PutItem("hello1")
        self.cache.PutItem("hello2")
        self.cache.PutItem("hello3")
        self.cache.PutItem("hello4")
        self.assertTrue(self.cache.GetCurrentSize() == 5)
        self.cache.PutItem("hello5")
        self.assertTrue(self.cache.GetCurrentSize() == 5)

    def testReset(self):
        """Test resetting the position"""
        self.cache.Clear()
        self.cache.PutItem("hello1")
        self.cache.PutItem("hello2")
        self.cache.PutItem("hello3")
        self.assertEquals(self.cache.GetNext(), "hello3")
        self.assertEquals(self.cache.GetNext(), "hello2")
        self.cache.Reset()
        self.assertEquals(self.cache.GetNext(), "hello3")
