###############################################################################
# Name: testEdFile.py                                                         #
# Purpose: Unit tests for ed_txt.py                                           #
# Author: Cody Precord <cprecord@editra.org>                                  #
# Copyright: (c) 2008 Cody Precord <staff@editra.org>                         #
# License: wxWindows License                                                  #
###############################################################################

"""Unittests for EdFile"""

__author__ = "Cody Precord <cprecord@editra.org>"
__svnid__ = "$Id$"
__revision__ = "$Revision$"

#-----------------------------------------------------------------------------#
# Imports
import os
import codecs
import types
import unittest

# Local imports
import common

# Module(s) to test
import ed_txt
import ebmlib

#-----------------------------------------------------------------------------#

class EdFileTest(unittest.TestCase):
    def setUp(self):
        # NEED this otherwise GetApp calls fail for some yet to be
        # determined reason even though an App has been created earlier
        # in runUnitTests...
        self.app = common.EdApp(False)

        self.path = common.GetDataFilePath(u'test_read_utf8.txt')
        self.file = ed_txt.EdFile(self.path)
        self.mtime = ebmlib.GetFileModTime(self.path)

        self.path_utf16 = common.GetDataFilePath(u'test_read_utf16.txt')
        self.mtime_utf16 = ebmlib.GetFileModTime(self.path_utf16)

        self.path_utf16_big = common.GetDataFilePath(u'test_read_utf16_big.txt')

        self.ipath = common.GetDataFilePath(u'image_test.png')
        self.img = ed_txt.EdFile(self.ipath)

        self.bpath = common.GetDataFilePath(u'test_read_utf8_bom.txt')
        self.utf8_bom_file = ed_txt.EdFile(self.bpath)

    def tearDown(self):
        self.file.Close()
        common.CleanTempDir()

    #---- Tests ----#
    def testClone(self):
        """Test making a copy of a file object"""
        clone = self.file.Clone()
        self.assertEquals(clone.GetPath(), self.file.GetPath())
        self.assertEquals(clone.Encoding, self.file.Encoding)
        self.assertEquals(clone.GetMagic(), self.file.GetMagic())
        self.assertEquals(clone.HasBom(), self.file.HasBom())
        self.assertEquals(clone.IsRawBytes(), self.file.IsRawBytes())
        self.assertEquals(clone.IsReadOnly(), self.file.IsReadOnly())

    def testRead(self):
        """Test reading from the file and getting the text"""
        txt = self.file.Read()
        self.assertFalse(self.file.HasBom())
        self.assertTrue(len(txt))

    def testReadNonPrintChars(self):
        """Test reading a plain text file that has a non printable
        character in it.
        """
        path = common.GetDataFilePath(u'non_print_char.txt')
        fileobj = ed_txt.EdFile(path)
        txt = fileobj.Read()
        self.assertTrue(type(txt) == types.UnicodeType)
        self.assertFalse(fileobj.IsRawBytes())
        self.assertFalse(fileobj.IsReadOnly())

    #---- Encoding Tests ----#

    def testReadUTF8Bom(self):
        """Test reading a utf8 bom file"""
        txt = self.utf8_bom_file.Read()
        self.assertTrue(self.utf8_bom_file.HasBom())
        self.assertTrue(len(txt))

    def testWriteUTF8Bom(self):
        """Test writing a file that has utf8 bom character"""
        txt = self.utf8_bom_file.Read()
        self.assertTrue(self.utf8_bom_file.HasBom())

        new_path = os.path.join(common.GetTempDir(), ebmlib.GetFileName(self.bpath))
        self.utf8_bom_file.SetPath(new_path) # write to test temp dir
        self.utf8_bom_file.Write(txt)

        # Open and verify that BOM was correctly written back
        f = open(new_path, 'rb')
        ntxt = f.read()
        f.close()
        self.assertTrue(ntxt.startswith(codecs.BOM_UTF8))

        # Ensure that BOM was only written once
        tmp = ntxt.lstrip(codecs.BOM_UTF8)
        self.assertFalse(tmp.startswith(codecs.BOM_UTF8))
        tmp = tmp.decode('utf-8')
        self.assertEquals(txt, tmp)

    def testWriteUTF16File(self):
        """Test that input and output bytes match"""
        fobj = ed_txt.EdFile(self.path_utf16)
        txt = fobj.Read()
        self.assertTrue(type(txt) == types.UnicodeType)
        self.assertTrue(fobj.Encoding in ('utf-16-le', 'utf_16_le', 'utf-16', 'utf_16'))
        self.assertFalse(fobj.HasBom()) # test file has no BOM

        # Get original raw bytes
        raw_bytes = common.GetFileContents(fobj.GetPath())
        
        # Write the unicode back out to disk
        out = common.GetTempFilePath('utf_16_output.txt')
        fobj.SetPath(out)
        self.assertFalse(fobj.HasBom()) # test file has no BOM
        fobj.Write(txt)

        # Get raw bytes that were just written
        new_bytes = common.GetFileContents(out)
        self.assertEquals(raw_bytes, new_bytes)

    def testReadUTF32Bom(self):
        """Test reading a file that has a UTF32 BOM"""
        fname = common.GetDataFilePath('test_read_utf32_bom.txt')
        fileutf32 = ed_txt.EdFile(fname)
        data = fileutf32.Read()
        self.assertTrue(fileutf32.HasBom(), "UTF-32 BOM not detected!")
        self.assertTrue(fileutf32.Encoding in ("utf-32", "utf_32"),
                        "Incorrect Encoding detected: %s" % fileutf32.Encoding)

    def testGetEncoding(self):
        """Test the encoding detection"""
        txt = self.file.Read()
        self.assertTrue(self.file.GetEncoding() == 'utf-8')
        fobj16 = ed_txt.EdFile(self.path_utf16)
        txt = fobj16.Read()
        enc = fobj16.GetEncoding() 
        self.assertTrue(enc in ('utf-16', 'utf_16', 'utf_16_le', 'utf-16-le'),
                        "Encoding Found: %s" % enc)

    def testGetExtension(self):
        """Test getting the file extension"""
        self.assertTrue(self.file.GetExtension() == 'txt')

    def testGetPath(self):
        """Test getting the files path"""
        self.assertTrue(self.file.GetPath() == self.path)

    def testGetMagic(self):
        """Test getting the magic comment"""
        self.file.Read()
        self.assertTrue(self.file.GetMagic())

        self.img.Read()
        self.assertFalse(self.img.GetMagic())

    def testGetModTime(self):
        """Test getting the files last modification time"""
        self.file.ModTime = self.mtime
        mtime = self.file.ModTime
        self.assertTrue(mtime == self.mtime, "Modtime was: " + str(mtime))

    def testHasBom(self):
        """Test checking if file has a bom marker or not"""
        self.assertFalse(self.file.HasBom(), "File has a BOM")

    def testIsRawBytes(self):
        """Test reading a file that can't be properly encoded and was
        read as raw bytes.

        """
        txt = self.file.Read()
        self.assertTrue(ebmlib.IsUnicode(txt))
        self.assertFalse(self.file.IsRawBytes())

        rpath = common.GetDataFilePath(u'embedded_nulls.txt')
        rfile = ed_txt.EdFile(rpath)
        txt = rfile.Read()
        self.assertTrue(ebmlib.IsUnicode(txt))
        self.assertFalse(rfile.IsRawBytes())

        bytes_value = self.img.Read()
        self.assertTrue(self.img.IsRawBytes())

    def testIsReadOnly(self):
        """Test if the file is read only or not"""
        self.assertFalse(self.file.IsReadOnly(), "File is readonly")
        self.assertEqual(self.file.IsReadOnly(), self.file.ReadOnly)

    def testSetEncoding(self):
        """Test setting the file objects encoding"""
        self.file.SetEncoding('latin1')
        self.assertTrue(self.file.GetEncoding() == 'latin1')

    #---- Module utility function tests ----#

    def testDecodeString(self):
        """Test decoding a string to unicode."""
        test = "test string"
        self.assertTrue(isinstance(test, str), "Not a string")
        uni = ed_txt.DecodeString(test, 'utf-8')
        self.assertTrue(isinstance(uni, types.UnicodeType), "Failed decode")

