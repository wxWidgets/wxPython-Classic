###############################################################################
# Name: testSyntaxFunctions.py                                                #
# Purpose: Unit tests for syntax.syntax functions                             #
# Author: Cody Precord <cprecord@editra.org>                                  #
# Copyright: (c) 2009 Cody Precord <staff@editra.org>                         #
# License: wxWindows License                                                  #
###############################################################################

"""Unittest cases for testing syntax.syntax functions"""

__author__ = "Cody Precord <cprecord@editra.org>"
__svnid__ = "$Id$"
__revision__ = "$Revision$"

#-----------------------------------------------------------------------------#
# Imports
import unittest
import wx

# Module to test
import syntax.syntax as syntax
import syntax.synglob as synglob

#-----------------------------------------------------------------------------#
# Test Class

class SyntaxFunctionsTest(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    #---- Test Cases ----#

    def testGenFileFilters(self):
        """Test getting the file filter list"""
        filters = syntax.GenFileFilters()
        self.assertTrue(isinstance(filters, list))
        for f in filters:
            self.assertTrue(isinstance(f, basestring))
        self.assertTrue(filters[-1][-1] != u"|")

    def testGetLexerMenu(self):
        """Test creating the lexer menu"""
        menu = syntax.GenLexerMenu()
        self.assertTrue(isinstance(menu, wx.Menu))

    def testGetExtensionFromId(self):
        """Test getting a file extension from a language id"""
        ext = syntax.GetExtFromId(synglob.ID_LANG_PYTHON)
        self.assertTrue(isinstance(ext, basestring))

    def testGetIdFromExt(self):
        """Test getting a file display name"""
        tid = syntax.GetIdFromExt('py')
        self.assertEquals(tid, synglob.ID_LANG_PYTHON)

        tid = syntax.GetIdFromExt('cpp')
        self.assertEquals(tid, synglob.ID_LANG_CPP)

        tid = syntax.GetIdFromExt('zzz')
        self.assertEquals(tid, synglob.ID_LANG_TXT)

    def testGetLexerList(self):
        """Test getting the list of available languages"""
        langs = syntax.GetLexerList()
        self.assertTrue(isinstance(langs, list))
        self.assertTrue(synglob.LANG_PYTHON in langs)
        for lang in langs:
            self.assertTrue(isinstance(lang, basestring))

    def testSyntaxIds(self):
        """Test getting the Syntax Id List"""
        sids = syntax.SyntaxIds()
        self.assertTrue(sids is syntax.SYNTAX_IDS)
        for sid in sids:
            self.assertTrue(isinstance(sid, int))
