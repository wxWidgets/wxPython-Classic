###############################################################################
# Name: testStyleMgr.py                                                       #
# Purpose: Unit test for Style Manager                                        #
# Author: Cody Precord <cprecord@editra.org>                                  #
# Copyright: (c) 2008 Cody Precord <staff@editra.org>                         #
# License: wxWindows License                                                  #
###############################################################################

"""Unittest cases for testing the StyleManager"""

__author__ = "Cody Precord <cprecord@editra.org>"
__svnid__ = "$Id$"
__revision__ = "$Revision$"

#-----------------------------------------------------------------------------#
# Imports
import os
import types
import wx
import unittest

# Local Imports
import common

# Module to Test
import ed_style

#-----------------------------------------------------------------------------#
# Test Class

class StyleMgrTest(unittest.TestCase):
    def setUp(self):
        self.mgr = ed_style.StyleMgr()
        self.dd = dict(ed_style.DEF_STYLE_DICT)
        self.bstr = ["fore:#000000", "back:#FFFFFF",
                     "face:%(primary)s", "size:%(size)d"]
        self.stylesheet = common.GetDataFilePath('no_comment_style.ess')

    def tearDown(self):
        pass

    #---- Tests ----#
    def testBlankStyleDictionary(self):
        """Test that a dictionary of blank and null items are returned"""
        blank = self.mgr.BlankStyleDictionary()
        self.assertTrue(isinstance(blank, dict), "No dictionary returned")
        self.assertEquals(sorted(blank.keys()), sorted(self.dd.keys()),
                          "Blank dictionary is missing some keys")

        # Check that all the items are blank and the same
        for key, item in blank.iteritems():
            if not item.IsNull():
                self.assertEquals(sorted(item.GetAsList()), sorted(self.bstr),
                                  "%s != %s" % (str(item.GetAsList()), self.bstr)) 

    # TODO add more tests for checking after changing style sheets
    def testGetCurrentStyleSetName(self):
        """Test getting the name of the current style set"""
        name = self.mgr.GetCurrentStyleSetName()
        self.assertEquals(name, "default")

    def testGetItemByName(self):
        """Test retrieving a StyleItem by name from the manager"""
        ditem = self.mgr.GetItemByName("default_style")
        self.assertTrue(ditem.IsOk(), "The default_style item is not OK")

        # Check getting a non existent style tag
        fake = self.mgr.GetItemByName("fakestyletag")
        self.assertFalse(fake.IsOk(), "The fake tag is not empty: %s" % str(fake))

        # Check that retrieving the same item twice returns the same value
        self.assertEquals(ditem, self.mgr.GetItemByName("default_style"),
                          "Retrieving same item twice yields different results")

    def testGetDefaultBackColour(self):
        """Test getting the current default_style's background color"""
        color = self.mgr.GetDefaultBackColour()
        self.assertTrue(isinstance(color, wx.Colour), "Not a wxColour Object")
        self.assertTrue(color.IsOk(), "Colour is not Ok")

        # Check hex string retrieval
        cstr = self.mgr.GetDefaultBackColour(as_hex=True)
        self.assertTrue(isinstance(cstr, basestring), "as_hex Failed")
        cstr2 = color.GetAsString(wx.C2S_HTML_SYNTAX).lower()
        self.assertEquals(cstr.lower(), cstr2,
                          "as_hex:%s != color:%s" % (cstr.lower(), cstr2))

    def testGetDefaultFont(self):
        """Test retrieval of the currently set default font"""
        font = self.mgr.GetDefaultFont()
        self.assertTrue(font.IsOk(), "Font is not OK")

        ditem = self.mgr.GetItemByName("default_style")
        self.assertEquals(font.GetFaceName().lower(), ditem.GetFace().lower(),
                          "%s != %s" % (font.GetFaceName(), ditem.GetFace()))

    def testGetDefaultForeColour(self):
        """Test getting the current default_style's foreground color"""
        color = self.mgr.GetDefaultForeColour()
        self.assertTrue(isinstance(color, wx.Colour), "Not a wxColour Object")
        self.assertTrue(color.IsOk(), "Colour is not Ok")

        # Check hex string retrieval
        cstr = self.mgr.GetDefaultForeColour(as_hex=True)
        self.assertTrue(isinstance(cstr, basestring), "as_hex Failed")
        cstr2 = color.GetAsString(wx.C2S_HTML_SYNTAX).lower()
        self.assertEquals(cstr.lower(), cstr2,
                          "as_hex:%s != color:%s" % (cstr.lower(), cstr2))

    def testGetFontDictionary(self):
        """Test getting the current font dictionary"""
        fdict = self.mgr.GetFontDictionary()
        self.assertTrue(isinstance(fdict, dict), "GetFontDictionary Failed")

        for key in ("primary", "secondary", "size", "size2", "size3"):
            self.assertTrue(fdict.get(key), "Failed to get %s" % key)

    def testGetStyleByName(self):
        """Test retrieval of a given style spec string"""
        for style in ('default_style', 'comment_style', 'string_style'):
            spec = self.mgr.GetStyleByName(style)
            self.assertTrue(isinstance(spec, basestring),
                            "GetStyleByName returned a %s" % str(type(spec)))
            self.assertTrue(len(spec), "Style %s is empty" % style)
            self.assertTrue('modifiers:' not in spec,
                            "Modifers attr in final spec")

        fake = self.mgr.GetStyleByName("fakestyletag")
        self.assertEquals(fake, wx.EmptyString)

    def testGetStyleFont(self):
        """Test getting the font objects for the current styles primary and
        secondary font settings.

        """
        pfont = self.mgr.GetStyleFont()
        self.assertTrue(pfont.IsOk(), "Primary font is not OK")
        sfont = self.mgr.GetStyleFont(primary=False)
        self.assertTrue(sfont.IsOk(), "Secondary font is not OK")

    def testGetStyleSet(self):
        """Test getting the current style set"""
        sty_set = self.mgr.GetStyleSet()
        self.assertTrue(isinstance(sty_set, dict), "Failed to retrieve set")
        self.assertTrue(len(sty_set) > 0, "Style set is empty!!")

    def testHasNamedStyle(self):
        """Test checking if the style set has the named style tag or not"""
        self.assertTrue(self.mgr.HasNamedStyle('default_style'),
                        "Default style not defined")
        self.assertFalse(self.mgr.HasNamedStyle('fakestyletag'),
                         "Set shouldn't have 'fakestyletag'")

    def testSetGlobalFont(self):
        """Test setting of a font in the global font dictionary"""
        self.assertTrue(self.mgr.SetGlobalFont("primary", "Arial", 10),
                        "Failed to set primary font")
        self.assertTrue(self.mgr.SetGlobalFont("secondary", "Arial", 10),
                        "Failed to set secondary font")

    def testStyleSetFont(self):
        """Test setting the font of the current style"""
        native = wx.SMALL_FONT.GetNativeFontInfo()
        native_s = native.ToString()

        self.mgr.SetStyleFont(wx.SMALL_FONT, primary=True)
        font = self.mgr.GetStyleFont(primary=True)
        nset = font.GetNativeFontInfo()
        self.assertEquals(native_s, nset.ToString())

        self.mgr.SetStyleFont(wx.SMALL_FONT, primary=False)
        font = self.mgr.GetStyleFont(primary=False)
        nset = font.GetNativeFontInfo()
        self.assertEquals(native_s, nset.ToString())

    def testSetStyleTag(self):
        """Test setting of individual style tags"""
        item = ed_style.StyleItem()
        fdict = dict(primary='Courier New', size=10)
        item.SetAttrFromStr(",".join(self.bstr) % fdict)
        self.assertTrue(self.mgr.SetStyleTag('default_style', item),
                        "Failed to set default style")
        citem = self.mgr.GetItemByName('default_style')
        self.assertEquals(citem, item,
                          "SetStyleTag incorrectly set the data\n"
                          "%s != %s" % (citem, item))
        self.assertFalse(self.mgr.SetStyleTag('default_style', self.bstr),
                         "SetStyleTag allowed setting of a list!")

    def testParseStyleData(self):
        """Test parsing Editra Style Sheets"""
        # Test valid style sheet
        data = common.GetFileContents(self.stylesheet)
        styledict = self.mgr.ParseStyleData(data)
        for tag, item in styledict.iteritems():
            self.assertTrue(isinstance(tag, types.UnicodeType), "%s Is not Unicode!" % tag)
            self.assertTrue(isinstance(item, ed_style.StyleItem))
        # Test loading sheet with malformed data
        sheet_path = common.GetDataFilePath('incorrect_syntax.ess')
        data = common.GetFileContents(sheet_path)
        styledict2 = self.mgr.ParseStyleData(data)
        self.assertTrue(len(styledict) > len(styledict2))
        for tag, item in styledict2.iteritems():
            self.assertTrue(isinstance(tag, types.UnicodeType), "%s Is not Unicode!" % tag)
            self.assertTrue(isinstance(item, ed_style.StyleItem))
        # Test stylesheet that is all on one line
        sheet_path = common.GetDataFilePath('one_liner.ess')
        data = common.GetFileContents(sheet_path)
        styledict3 = self.mgr.ParseStyleData(data)
        for tag, item in styledict3.iteritems():
            self.assertTrue(isinstance(tag, types.UnicodeType), "%s Is not Unicode!" % tag)
            self.assertTrue(isinstance(item, ed_style.StyleItem))

    def testPackStyleSet(self):
        """Test packing an incomplete style set"""
        ## TEST 1 - loading and packing sheet that does not define comment_style
        data = common.GetFileContents(self.stylesheet)
        styledict = self.mgr.ParseStyleData(data)
        self.assertTrue('comment_style' not in styledict)
        default = styledict.get('default_style')
        self.assertTrue(isinstance(default, ed_style.StyleItem))
        # Pack the Style Set
        styledict = self.mgr.PackStyleSet(styledict)
        self.assertTrue('comment_style' in styledict)
        whitestyle = styledict.get('comment_style')
        self.assertTrue(whitestyle == default)
        ## END TEST 1

    def testValidateColourData(self):
        """Validate that colour data is getting parsed correctly"""
        sheet_path = common.GetDataFilePath('old_format.ess')
        data = common.GetFileContents(sheet_path)
        styledict = self.mgr.ParseStyleData(data)
        styledict = self.mgr.PackStyleSet(styledict)
        for tag, item in styledict.iteritems():
            self.doValidateColourAttrs(tag, item)

    def doValidateColourAttrs(self, tag, item):
        """validate the colour attributes on an item"""
        if not item.IsNull():
            try:
                int(item.GetFore()[1:], 16)
                int(item.GetBack()[1:], 16)
            except Exception, msg:
                self.assertFalse(True, "Bad data in style item: %s:%s" % (tag,item))

    def testValidateBuiltinStyleSheets(self):
        """Validate formatting and parsing of all builtin style sheets"""
        sdir = common.GetStylesDir()
        for sheet in [os.path.join(sdir, f) for f in os.listdir(sdir)
                      if f.endswith('.ess')]:
            data = common.GetFileContents(sheet)
            styledict = self.mgr.ParseStyleData(data)
            styledict = self.mgr.PackStyleSet(styledict)
            for tag, item in styledict.iteritems():
                self.doValidateColourAttrs(tag, item)
                mods = item.GetModifierList()
                if len(mods):
                    for mod in mods:
                        self.assertTrue(mod in ('eol', 'bold', 'italic', 'underline'))
                isize = item.GetSize()
                if len(isize): # Null items such as select_style dont set this attr
                    self.assertTrue(isize.isdigit() or 
                                    (isize.startswith("%(") and isize.endswith(")d")),
                                    "Bad font size specification %s:%s:%s" % (sheet, tag, repr(isize)))
                # TODO: Fonts
