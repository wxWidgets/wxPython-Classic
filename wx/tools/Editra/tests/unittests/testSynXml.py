###############################################################################
# Name: testSynXml.py                                                         #
# Purpose: Unit tests for the Syntax Xml Library                              #
# Author: Cody Precord <cprecord@editra.org>                                  #
# Copyright: (c) 2009 Cody Precord <staff@editra.org>                         #
# License: wxWindows License                                                  #
###############################################################################

"""Unittest cases for the Syntax Xml Library"""

__author__ = "Cody Precord <cprecord@editra.org>"
__svnid__ = "$Id$"
__revision__ = "$Revision$"

#-----------------------------------------------------------------------------#
# Imports
import wx.stc
import unittest

# Local modules
import common

# Module to test
import syntax

#-----------------------------------------------------------------------------#
# Test Class

class SynXmlTest(unittest.TestCase):
    def setUp(self):
        self.path = common.GetDataFilePath(u'syntax.xml')
        self.bad = common.GetDataFilePath(u'bad.xml')
        self.xml = common.GetFileContents(self.path)
        self.badxml = common.GetFileContents(self.bad)

        self.fhandle = syntax.SyntaxModeHandler(self.path)
        self.fhandle.LoadFromDisk()

    def tearDown(self):
        pass

    #---- Base Tests ----#

    def testGetXml(self):
        """Test getting the xml representation"""
        tmp_h = syntax.SyntaxModeHandler()
        tmp_h.LoadFromString(self.xml)

        x1 = self.fhandle.GetXml()
        x2 = tmp_h.GetXml()
        self.assertEquals(x1, x2)

    #---- SyntaxModeHandler tests ----#

    def testGetCommentPattern(self):
        """Get retrieving the comment pattern from the xml"""
        self.assertEquals(self.fhandle.CommentPattern,
                          self.fhandle.GetCommentPattern())
        self.assertEquals(self.fhandle.CommentPattern, [u"#",],
                          "pattern is: %s" % self.fhandle.CommentPattern)

    def testGetFeatureFromXml(self):
        """Test retrieving a feature"""
        feat = self.fhandle.GetFeatureFromXml(u'AutoIndenter')
        self.assertEquals(feat, u'myextension.py')

    def testGetFileExtensions(self):
        """Test getting the file extension list"""
        exts = self.fhandle.GetFileExtensions()
        self.assertTrue(isinstance(exts, list))
        for ext in exts:
            self.assertTrue(isinstance(ext, basestring))

    def testGetKeywords(self):
        """Test getting the keywords from the xml"""
        kwords = self.fhandle.GetKeywords()
        self.assertTrue(isinstance(kwords, list), "Not a List")
        self.assertTrue(isinstance(kwords[0], tuple), "Not a tuple")
        self.assertTrue(len(kwords) == 2)
        self.assertEquals(kwords[0][0], 0, "not sorted")
        self.assertTrue(u'else' in kwords[0][1])
        self.assertTrue(u'str' in kwords[1][1])

    def testGetLangId(self):
        """Test getting the language identifier string"""
        lid = self.fhandle.GetLangId()
        self.assertEquals(lid, 'ID_LANG_PYTHON')

    def testGetProperties(self):
        """Test getting the property list from the xml"""
        props = self.fhandle.GetProperties()
        self.assertTrue(isinstance(props, list))
        self.assertTrue(isinstance(props[0], tuple))
        self.assertTrue(len(props) == 2)
        self.assertEquals(props[0][0], "fold")
        self.assertEquals(props[0][1], "1")

    def testGetSyntaxSpec(self):
        """Test getting the syntax specifications from the xml"""
        spec = self.fhandle.GetSyntaxSpec()
        self.assertTrue(isinstance(spec, list))
        self.assertTrue(isinstance(spec[0], tuple))
        self.assertTrue(len(spec) == 2)
        self.assertEquals(spec[0][0], wx.stc.STC_P_DEFAULT,
                          "val was: %s" % spec[0][0])
        self.assertEquals(spec[0][1], "default_style",
                          "val was: %s" % spec[0][1])
        self.assertEquals(spec[1][0], wx.stc.STC_P_WORD,
                          "val was: %s" % spec[0][0])
        self.assertEquals(spec[1][1], "keyword_style",
                          "val was: %s" % spec[0][1])

    def testIsOk(self):
        """Test IsOk method"""
        tmp_h = syntax.SyntaxModeHandler(self.path)
        tmp_h.LoadFromDisk()
        self.assertTrue(tmp_h.IsOk())
        self.assertTrue(tmp_h.Ok)
        tmp_h = syntax.SyntaxModeHandler(self.bad)
        tmp_h.LoadFromDisk()
        self.assertFalse(tmp_h.IsOk())
        self.assertFalse(tmp_h.Ok)

    def testVersion(self):
        """Test the xml version attribute"""
        self.assertEquals(self.fhandle.Version, 1,
                        "val was: " + str(self.fhandle.Version))
        
