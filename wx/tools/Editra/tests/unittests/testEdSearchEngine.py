# -*- encoding: utf-8 -*-
###############################################################################
# Name: testEdSearchEngine                                                    #
# Purpose: Unittest for ed_search.EdSearchEngine                              #
# Author: Cody Precord <cprecord@editra.org>                                  #
# Copyright: (c) 2011 Cody Precord <staff@editra.org>                         #
# License: wxWindows License                                                  #
###############################################################################

"""Unittests for Editra's text SearchEngine specialization EdSearchEngine"""

__author__ = "Cody Precord <cprecord@editra.org>"
__svnid__ = "$Id: $"
__revision__ = "$Revision:  $"

#-----------------------------------------------------------------------------#
# Imports
import unittest
import unicodedata

# Module to test
import ed_search

#-----------------------------------------------------------------------------#
# Search Pool

# NOTE: changing this string requires changing the related tests that use it
POOL = ("Test string to use for the find tests. The find tests work on strings"
        " while the search methods work on files. Here is some more random"
        " strings to search in. def foo(param1, param2): print param1, param2"
        " 123 + 754 / 5 = $x. $var1 = TEST_STRING; $var2=test_string; test ")

POOL2 = """Multiline test pool of text to search in.
This text can be used to check for doing multiline searches. As well
as doing multiline replaces.
"""

#-----------------------------------------------------------------------------#
# Test Class

class EdSearchEngineTest(unittest.TestCase):
    def setUp(self):
        """Setup the test items"""
        self._def_eng = ed_search.EdSearchEngine(u"", regex=False, down=True,
                                               matchcase=False, wholeword=False)
        self._ww_eng = ed_search.EdSearchEngine(u"", regex=False, down=True,
                                              matchcase=False, wholeword=True)
        self._mc_eng = ed_search.EdSearchEngine(u"", regex=False, down=True,
                                              matchcase=True, wholeword=False)
        self._regex_eng = ed_search.EdSearchEngine(u"", regex=True, down=True,
                                                 matchcase=False, wholeword=False)
        self._regexmc_eng = ed_search.EdSearchEngine(u"", regex=True, down=True,
                                                  matchcase=True, wholeword=False)
        self._regww_eng = ed_search.EdSearchEngine(u"", regex=True, down=True,
                                                 matchcase=False, wholeword=True)
        self._all_eng = ed_search.EdSearchEngine(u"", regex=True, down=True,
                                               matchcase=True, wholeword=True)

    def tearDown(self):
        pass

    #---- Method Tests ----#
    def testIsRegEx(self):
        """Test if the regex flag is properly set"""
        self.assertTrue(self._regex_eng.IsRegEx(), "Regex Engine is not Regex")
        self.assertFalse(self._def_eng.IsRegEx(), "Default Engine is Regex")

    def testIsMatchCase(self):
        """Test if the match case flag is properly set"""
        self.assertTrue(self._mc_eng.IsMatchCase())
        self.assertFalse(self._def_eng.IsMatchCase())
        self.assertTrue(self._all_eng.IsMatchCase())
        
    def testIsWholeWord(self):
        """Test if the whole word flag is properly set"""
        self.assertTrue(self._ww_eng.IsWholeWord())
        self.assertFalse(self._def_eng.IsWholeWord())
        self.assertTrue(self._all_eng.IsWholeWord())

    def testNormalFind(self):
        """Test find procedure to see if it acuratly returns the correct
        positions in the search pool

        """
        # Test default search
        self._def_eng.SetSearchPool(POOL)
        self._def_eng.SetQuery('test')
        t1 = self._def_eng.Find(0)
        self.assertTrue(t1 is not None, "Find failed")
        self.assertEquals(t1[0], 0, "Find got wrong postion")
        self.assertEquals(t1[1] - t1[0], 4, "Find returned wrong span")

        # Find Next
        t2 = self._def_eng.Find(t1[1])
        self.assertTrue(t2 is not None, "Find next failed")
        self.assertEquals(t2[0] + t1[1], 32, "Find next: %d != 32" % t2[0])

        # Test not found
        self._def_eng.SetQuery('gyoza')
        t3 = self._def_eng.Find(0)
        self.assertTrue(t3 is None)

    def testFindAll(self):
        """Test doing a find all in the search pool"""
        self._def_eng.SetSearchPool(POOL)
        
        # Find All Case insensitive
        self._def_eng.SetQuery(u"test")
        t1 = self._def_eng.FindAll()
        self.assertTrue(len(t1) == 6, "Found: %d Expected: 5" % len(t1))

        # Find All Match Case
        self._def_eng.SetFlags(matchcase=True)
        t2 = self._def_eng.FindAll()
        self.assertTrue(len(t2) == 4, "Found: %d Expected: 3" % len(t2))

        # Find All Match Case / Whole Word
        self._def_eng.SetFlags(wholeword=True)
        t3 = self._def_eng.FindAll()
        self.assertTrue(len(t3) == 1, "Found: %d Expected: 1" % len(t3))

        # Find searching in a pool that is a string not Unicode
        self._def_eng.SetFlags(wholeword=False)
        self._def_eng.SetFlags(matchcase=False)
        pool = u"Hello ä".encode('utf-8')
        self._def_eng.SetSearchPool(pool)
        self._def_eng.SetQuery(u'ä')
        t4 = self._def_eng.FindAll()
        self.assertTrue(len(t4) == 1, "Find Results %s" % repr(t4))

    def testWholeWordFind(self):
        """Test find procedure to see if it accurately returns the correct
        positions in the search pool

        """
        # Test default search
        self._ww_eng.SetSearchPool(POOL)
        self._ww_eng.SetQuery('test')
        t1 = self._ww_eng.Find(0)
        self.assertTrue(t1 is not None, "Find failed")
        self.assertEquals(t1[0], 0, "Find got wrong postion")
        self.assertEquals(t1[1] - t1[0], 4, "Find returned wrong span")

        # Find Next (Should be None)
        t2 = self._ww_eng.Find(t1[1])
        self.assertTrue(t2 is not None, "Find next failed")

    def testMatchCaseFind(self):
        """Test find procedure to see if it accurately returns the correct
        positions in the search pool

        """
        # Test default search
        self._mc_eng.SetSearchPool(POOL)
        self._mc_eng.SetQuery('test')
        t1 = self._mc_eng.Find(0)
        self.assertTrue(t1 is not None, "Find failed")
        self.assertEquals(t1[0], 32, "Find got wrong position")
        self.assertEquals(t1[1] - t1[0], 4, "Find returned wrong span")

        # Find Next
        t2 = self._mc_eng.Find(t1[1])
        self.assertTrue(t2 is not None, "Find next failed")
        self.assertEquals(t2[0] + t1[1], 48, "Find next: %d != 48" % t2[0])

        # Test not found
        self._mc_eng.SetQuery('TeSt')
        t3 = self._mc_eng.Find(0)
        self.assertTrue(t3 is None)

    def testQuery(self):
        """Test setting and retrieving the search query"""
        q1 = self._def_eng.GetQuery()
        self.assertTrue(q1 == u"")
        self._def_eng.SetQuery(u"test")
        self.assertTrue(self._def_eng.GetQuery() == u"test")

    def testRegexFind(self):
        """Test find procedure to see if it accurately returns the correct
        positions in the search pool

        """
        # Test Regex search
        self._regex_eng.SetSearchPool(POOL)
        self._regex_eng.SetQuery('t[a-u]+')
        t1 = self._regex_eng.Find(0)
        self.assertFalse(t1 is None, "Regex find failed")

        # Find Next
        t2 = self._regex_eng.Find(t1[1])
        self.assertTrue(t2 is not None, "Find next failed")
        self.assertEquals(t2[0] + t1[1], 6, "Find next: %d != 6" % t2[0])

        # Test not found
        self._regex_eng.SetQuery('test{10,10}')
        t3 = self._regex_eng.Find(0)
        self.assertTrue(t3 is None)

        # Multiline 
        # TODO

    def testNormalizedFind(self):
        """Test searching for normalized Unicode data"""
        pool = unicodedata.normalize('NFC', u"école")
        query = unicodedata.normalize('NFD', u"école")
        self.assertTrue(pool != query)
        search = ed_search.EdSearchEngine(query)
        search.SetSearchPool(pool)
        val = search.Find()
        self.assertTrue(val is not None)

        pool = unichr(0x00E9)
        query = u'e' + u'\u0301'
        self.assertTrue(pool != query)
        search = ed_search.EdSearchEngine(query)
        search.SetSearchPool(u"foobar " + pool)
        val = search.Find()
        self.assertTrue(val is not None)

#-----------------------------------------------------------------------------#

if __name__ == '__main__':
    unittest.main()
