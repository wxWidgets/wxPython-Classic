###############################################################################
# Name: testSyntaxDataBase.py                                                 #
# Purpose: Unit tests for synextreg.ExtensionRegister                         #
# Author: Cody Precord <cprecord@editra.org>                                  #
# Copyright: (c) 2010 Cody Precord <staff@editra.org>                         #
# License: wxWindows License                                                  #
###############################################################################

"""Unittest cases for testing synextreg.ExtensionRegister class"""

__author__ = "Cody Precord <cprecord@editra.org>"
__svnid__ = "$Id$"
__revision__ = "$Revision$"

#-----------------------------------------------------------------------------#
# Imports
import unittest
import os
import wx
import wx.stc

# Module to test
import syntax.synextreg as synextreg

#-----------------------------------------------------------------------------#
# Test Class

class SyntaxExtRegTest(unittest.TestCase):

    def setUp(self):
        self.reg = synextreg.ExtensionRegister()

    def tearDown(self):
        self.reg.LoadDefault()

    #---- Test Cases ----#

    def testSingleton(self):
        self.assertTrue(self.reg is synextreg.ExtensionRegister())

    def testUnknownValue(self):
        val = self.reg['SomeFakeUnknownValue']
        self.assertTrue(val == u'txt')

    def testSetItem(self):
        self.assertRaises(TypeError, self.reg.__setitem__, 'test', 1)

    def testSerialize(self):
        ser = str(self.reg)
        self.assertTrue(isinstance(ser, basestring))
        for line in ser.split(os.linesep):
            self.assertTrue("=" in line)

    def testAssociate(self):
        self.reg.Associate(synextreg.LANG_TXT, "foo")
        ftype = self.reg.FileTypeFromExt("foo")
        self.assertEquals(ftype, synextreg.LANG_TXT)
        # An unknown extension should fall back to type Text
        ftype = self.reg.FileTypeFromExt("UNKNOWN_EXTENSION")
        self.assertEquals(ftype, synextreg.LANG_TXT)

    def testDisassociate(self):
        ftype = self.reg.FileTypeFromExt("pyw")
        self.assertEquals(ftype, synextreg.LANG_PYTHON)
        self.reg.Disassociate(synextreg.LANG_PYTHON, "pyw")
        ftype = self.reg.FileTypeFromExt("pyw")
        self.assertEquals(ftype, synextreg.LANG_TXT)

    def testFileTypeFromExt(self):
        ftype = self.reg.FileTypeFromExt("cpp")
        self.assertEquals(ftype, synextreg.LANG_CPP)
        ftype = self.reg.FileTypeFromExt("py")
        self.assertEquals(ftype, synextreg.LANG_PYTHON)
        ftype = self.reg.FileTypeFromExt("html")
        self.assertEquals(ftype, synextreg.LANG_HTML)

    def testGetAllExtensions(self):
        exts = self.reg.GetAllExtensions()
        self.assertTrue(isinstance(exts, list))
        for ext in exts:
            self.assertTrue(isinstance(ext, basestring), "Type Fail: %s" % ext)

    def testLoadDefault(self):
        self.reg.Associate(synextreg.LANG_CPP, "foo")
        ftype = self.reg.FileTypeFromExt("foo")
        self.assertTrue(ftype == synextreg.LANG_CPP, "FTYPE: %s" % ftype)
        self.reg.LoadDefault()
        ftype = self.reg.FileTypeFromExt("foo")
        self.assertTrue(ftype == synextreg.LANG_TXT)

    def testRemove(self):
        self.assertFalse(self.reg.Remove("UNKNOWN+TYPE"))
        self.assertTrue(self.reg.Remove(synextreg.LANG_4GL))

    def testSetAssociation(self):
        self.reg.Associate(synextreg.LANG_CPP, "foo")
        ftype = self.reg.FileTypeFromExt("foo")
        self.assertTrue(ftype == synextreg.LANG_CPP, "FTYPE: %s" % ftype)
        ftype = self.reg.FileTypeFromExt("cpp")
        self.assertTrue(ftype == synextreg.LANG_CPP, "FTYPE: %s" % ftype)

        # SetAssociation should replace existing associations with the
        # ones set by this call
        self.reg.SetAssociation(synextreg.LANG_CPP, "foo")
        ftype = self.reg.FileTypeFromExt("foo")
        self.assertTrue(ftype == synextreg.LANG_CPP)
        ftype = self.reg.FileTypeFromExt("cpp")
        self.assertTrue(ftype == synextreg.LANG_TXT, "FTYPE: %s" % ftype)

    #--- Module Level Function Tests ----#

    def testGetFileExtensionsFunct(self):
        exts1 = self.reg.GetAllExtensions()
        exts2 = synextreg.GetFileExtensions()
        self.assertTrue(exts1 == exts2)

    def testRegisterNewLangId(self):
        self.assertFalse("ID_LANG_FAKELANG" in dir(synextreg))
        nid = synextreg.RegisterNewLangId("ID_LANG_FAKELANG", "FakeLang")
        self.assertTrue(isinstance(nid, int))
        self.assertTrue("ID_LANG_FAKELANG" in dir(synextreg))

