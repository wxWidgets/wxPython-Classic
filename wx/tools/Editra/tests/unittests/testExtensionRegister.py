###############################################################################
# Name: testExtensionRegister.py                                              #
# Purpose: Unit tests for syntax.synextreg.ExtensionRegister                  #
# Author: Cody Precord <cprecord@editra.org>                                  #
# Copyright: (c) 2009 Cody Precord <staff@editra.org>                         #
# License: wxWindows License                                                  #
###############################################################################

"""Unittest cases for testing the file type extension register"""

__author__ = "Cody Precord <cprecord@editra.org>"
__svnid__ = "$Id$"
__revision__ = "$Revision$"

#-----------------------------------------------------------------------------#
# Imports
import unittest

# Local modules
import common

# Module to test
import syntax.synextreg as synreg

#-----------------------------------------------------------------------------#
# Test Class

class ExtensionRegisterTest(unittest.TestCase):
    def setUp(self):
        self.reg = synreg.ExtensionRegister()

    def tearDown(self):
        self.reg.LoadDefault()

    def testAssociate(self):
        """Test that Associate successfully adds new extensions to the
        current associations of a filetype.

        """
        curr = list(self.reg[synreg.LANG_XML]) # force list copy
        self.reg.Associate(synreg.LANG_XML, 'myXml')
        self.assertTrue('myXml' in self.reg[synreg.LANG_XML])
        curr.append('myXml')
        curr.sort()
        self.assertEquals(self.reg[synreg.LANG_XML], curr)

        # Test against adding duplicates
        self.assertTrue('xml' in self.reg[synreg.LANG_XML])
        self.reg.Associate(synreg.LANG_XML, 'xml')
        self.assertEquals(self.reg[synreg.LANG_XML].count('xml'), 1)

    def testDisassociate(self):
        """Test removing an association"""
        self.assertTrue('html' in self.reg[synreg.LANG_HTML])
        self.reg.Disassociate(synreg.LANG_HTML, 'html')
        self.assertTrue('html' not in self.reg[synreg.LANG_HTML])

    def testSingleton(self):
        """Test that the syntax register is a singleton"""
        self.assertTrue(self.reg is synreg.ExtensionRegister())

    def testFileTypeFromExt(self):
        """Test getting the filetype identifier from a given extension"""
        self.assertTrue('cpp' in self.reg[synreg.LANG_CPP])
        self.assertEquals(self.reg.FileTypeFromExt('cpp'), synreg.LANG_CPP)

        # Test that non-existant returns LANG_TEXT
        self.assertEquals(self.reg.FileTypeFromExt('fake_Exent'), synreg.LANG_TXT)

    def testGetAllExtensions(self):
        self.assertTrue(isinstance(self.reg.GetAllExtensions(), list))

    def testLoadDefault(self):
        """Test loading the default settings"""
        d = list(self.reg[synreg.LANG_C]) # force list copy
        self.reg.Associate(synreg.LANG_C, 'NEW_C')
        self.assertTrue('NEW_C' in self.reg[synreg.LANG_C])
        self.assertNotEquals(d, self.reg[synreg.LANG_C])
        self.reg.LoadDefault()
        self.assertEquals(d, self.reg[synreg.LANG_C])

    # TODO:
#    def testLoadFromConfig(self):
#        pass
    
    def testSetAssociation(self):
        d = self.reg[synreg.LANG_PHP]
        self.reg.SetAssociation(synreg.LANG_PHP, "xxx yyy zzz")
        n = self.reg[synreg.LANG_PHP]
        self.assertTrue('xxx' in n)
        self.assertTrue('yyy' in n)
        self.assertTrue('zzz' in n)

        for e in d:
            self.assertFalse(e in n)

    def testGetFileExtension(self):
        """Test the module function GetFileExtensions"""
        ext = self.reg.GetAllExtensions()
        self.assertTrue(isinstance(ext, list))
        for item in ext:
            self.assertTrue(isinstance(item, basestring))
