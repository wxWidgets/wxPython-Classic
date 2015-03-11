###############################################################################
# Name: testSyntaxDataBase.py                                                 #
# Purpose: Unit tests for syntax.syndata Base Class                           #
# Author: Cody Precord <cprecord@editra.org>                                  #
# Copyright: (c) 2010 Cody Precord <staff@editra.org>                         #
# License: wxWindows License                                                  #
###############################################################################

"""Unittest cases for testing syndata.SyntaxDataBase class"""

__author__ = "Cody Precord <cprecord@editra.org>"
__svnid__ = "$Id$"
__revision__ = "$Revision$"

#-----------------------------------------------------------------------------#
# Imports
import unittest
import wx
import wx.stc

# Module to test
import syntax.syndata as syndata

#-----------------------------------------------------------------------------#
# Test Class

class SyntaxDataBaseTest(unittest.TestCase):

    def setUp(self):
        self.data = syndata.SyntaxDataBase()

    def tearDown(self):
        pass

    #---- Test Cases ----#

    def testCommentPattern(self):
        self.assertTrue(isinstance(self.data.CommentPattern, list))
        self.assertTrue(self.data.CommentPattern == self.data.GetCommentPattern())

    def testKeywords(self):
        self.assertTrue(isinstance(self.data.Keywords, list))
        self.assertTrue(self.data.Keywords == self.data.GetKeywords())

    def testLangId(self):
        self.assertTrue(isinstance(self.data.LangId, int))
        self.assertTrue(self.data.LangId == self.data.GetLangId())

    def testLexer(self):
        self.assertTrue(isinstance(self.data.Lexer, int)) 
        lexers = [ getattr(wx.stc, item) for item in dir(wx.stc)
                   if item.startswith('STC_LEX') ]
        self.assertTrue(self.data.Lexer in lexers)

    def testProperties(self):
        self.assertTrue(isinstance(self.data.Properties, list))
        self.assertTrue(self.data.Properties == self.data.GetProperties())

    def testSyntaxSpec(self):
        self.assertRaises(NotImplementedError, self.data.GetSyntaxSpec)

    def testRegisterFeature(self):
        def foo():
            pass
        self.data.RegisterFeature('foo', foo)
        self.assertTrue(self.data.GetFeature('foo') is foo)

    def testSetLangId(self):
        self.data.SetLangId(10)
        self.assertEquals(10, self.data.LangId)

    def testSetLexer(self):
        self.data.SetLexer(wx.stc.STC_LEX_CPP)
        self.assertEquals(wx.stc.STC_LEX_CPP, self.data.GetLexer())
