###############################################################################
# Name: testSynGlob.py                                                        #
# Purpose: Unit tests for syntax.synglob utilities                            #
# Author: Cody Precord <cprecord@editra.org>                                  #
# Copyright: (c) 2009 Cody Precord <staff@editra.org>                         #
# License: wxWindows License                                                  #
###############################################################################

"""Unittest cases for testing syntax.synglob utilities and functions"""

__author__ = "Cody Precord <cprecord@editra.org>"
__svnid__ = "$Id$"
__revision__ = "$Revision$"

#-----------------------------------------------------------------------------#
# Imports
import unittest

# Module to test
import syntax.synglob as synglob

#-----------------------------------------------------------------------------#
# Test Class

class SynGlobTest(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    #---- Test Cases ----#

    def testGetDescriptionFromId(self):
        """Test GetDescriptionFromId"""
        desc = synglob.GetDescriptionFromId(synglob.ID_LANG_PYTHON)
        self.assertEquals(desc, synglob.LANG_PYTHON)

        desc = synglob.GetDescriptionFromId(synglob.ID_LANG_JAVA)
        self.assertEquals(desc, synglob.LANG_JAVA)

        # Test that some unknown id's always return Plain Text
        desc = synglob.GetDescriptionFromId(0)
        self.assertEquals(desc, synglob.LANG_TXT)

        desc = synglob.GetDescriptionFromId(100)
        self.assertEquals(desc, synglob.LANG_TXT)

    def testGetIdFromDescription(self):
        """Get getting a language id from its description string"""
        id_ = synglob.GetIdFromDescription(u"Python")
        self.assertEquals(id_, synglob.ID_LANG_PYTHON)

        id_ = synglob.GetIdFromDescription(u"python")
        self.assertEquals(id_, synglob.ID_LANG_PYTHON)

        id_ = synglob.GetIdFromDescription(u"C")
        self.assertEquals(id_, synglob.ID_LANG_C)

        id_ = synglob.GetIdFromDescription(u"SomeFakeLang")
        self.assertEquals(id_, synglob.ID_LANG_TXT)

