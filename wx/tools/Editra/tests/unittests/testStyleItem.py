###############################################################################
# Name: testStyleItem                                                         #
# Purpose: Unittest for ed_style.StyleItem                                    #
# Author: Cody Precord <cprecord@editra.org>                                  #
# Copyright: (c) 2008 Cody Precord <staff@editra.org>                         #
# License: wxWindows License                                                  #
###############################################################################

"""Unittest cases for StyleItems"""

__author__ = "Cody Precord <cprecord@editra.org>"
__svnid__ = "$Id$"
__revision__ = "$Revision$"

#-----------------------------------------------------------------------------#
# Imports
import unittest

# Module to test
import ed_style

#-----------------------------------------------------------------------------#
# Test Class

class StyleItemTest(unittest.TestCase):
    def setUp(self):
        self.item = ed_style.StyleItem("#FF0000", "#000000", "Times", "10", ex=["bold",])
        self.itemstr = "fore:#FF0000,back:#000000,face:Times,size:10,modifiers:bold"
        self.item2 = ed_style.StyleItem("#FF0000")
        self.itemstr2 = "fore:#FF0000"
        self.null = ed_style.NullStyleItem()

    def tearDown(self):
        pass

    #---- Method Tests ----#
    def testEquals(self):
        """Test that the equality operator is functioning correctly"""
        item1 = ed_style.StyleItem("#FF0000", "#000000", "Times", "10", ex=["bold",])
        item2 = ed_style.StyleItem("#FF0000", "#000000", "Times", "10", ex=["bold",])

        # Base Test
        self.assertEquals(item1, item2)

        # Test 2
        item3 = ed_style.StyleItem("#FF0000", "#0000FF", "Arial", "10")
        self.assertNotEquals(item1, item3,
                             "%s == %s" % (str(self.item), str(item2)))

        # Test 3
        # Coverage for bug of setting empty string in extra modifier styles
        # that was being allowed and would ultimatly fail the equality test.
        item1.SetExAttr(u'', True)
        self.assertEquals(item1, item2)

    def testString(self):
        """Test that string conversion works properly"""
        items1 = sorted(str(self.item).split(','))
        items2 = sorted(self.itemstr.split(','))
        self.assertEquals(items1, items2)

    def testGetAsList(self):
        """Test getting the style item attributes as a list"""
        itemlst = self.item.GetAsList()
        ilen = len(itemlst)
        self.assertTrue(ilen == 5, "Length Was: %d" % ilen)
        itemlst = self.item2.GetAsList()
        self.assertTrue(len(itemlst) == 1, "List Was: %s" % repr(itemlst))
        self.assertTrue(len(self.null.GetAsList()) == 0, "Null Item had values")

    def testGetBack(self):
        """Test retrieving the background color"""
        self.assertEquals(self.item.GetBack(), "#000000")
        self.assertEquals(self.null.GetBack(), u'')

    def testGetFore(self):
        """Test retrieving the background color"""
        self.assertEquals(self.item.GetFore(), "#FF0000")
        self.assertEquals(self.null.GetFore(), u'')

    def testGetFace(self):
        """Test retrieving the background color"""
        self.assertEquals(self.item.GetFace(), "Times")
        self.assertEquals(self.null.GetFace(), u'')

    def testGetSize(self):
        """Test retrieving the background color"""
        self.assertEquals(self.item.GetSize(), "10")
        self.assertEquals(self.null.GetSize(), u'')

    def testGetModifiers(self):
        """Test retrieving the extra modifier attributes"""
        self.assertEquals(self.item.GetModifiers(), "bold")
        self.assertEquals(self.null.GetModifiers(), u'')

    def testGetModifierList(self):
        """Test retrieving the extra modifier attributes list"""
        self.assertEquals(self.item.GetModifierList()[0], "bold")
        self.assertEquals(self.null.GetModifierList(), list())

    def testGetNamedAttr(self):
        """Test GetNamedAttr"""
        self.assertEquals(self.item.GetNamedAttr("fore"), self.item.GetFore())
        self.assertEquals(self.item.GetNamedAttr("back"), self.item.GetBack())
        self.assertEquals(self.item.GetNamedAttr("face"), self.item.GetFace())
        self.assertEquals(self.item.GetNamedAttr("size"), self.item.GetSize())

    def testIsNull(self):
        """Test Null check"""
        self.assertFalse(self.item.IsNull())
        self.assertTrue(ed_style.NullStyleItem().IsNull())
        self.assertTrue(self.null.IsNull())
        self.null.SetFore("#000000")
        self.assertFalse(self.null.IsNull())

    def testIsOk(self):
        """Test checker for if an item is Ok"""
        self.assertTrue(self.item.IsOk())
        self.assertFalse(ed_style.StyleItem().IsOk())
        self.assertFalse(self.null.IsOk())

    def testNullify(self):
        """Test nullifying a style item"""
        item = ed_style.StyleItem("#000000", "#FFFFFF")
        self.assertFalse(item.IsNull(), "Item is already null")
        item.Nullify()
        self.assertTrue(item.IsNull(), "Item was not nullified")
        self.assertEquals(str(item), u'')

    def testSetAttrFromString(self):
        """Test Setting attributes from a formatted string"""
        item = ed_style.StyleItem()
        item.SetAttrFromStr(self.itemstr)
        self.assertEquals(self.item, item,
                          "%s != %s" % (str(self.item), str(item)))

    def testSetBack(self):
        """Test setting the background colour attribute"""
        self.item.SetBack("#797979")
        self.assertEquals(self.item.GetBack(), "#797979")
        self.item.SetBack(None)
        self.assertEquals(self.item.GetBack(), "")

    def testSetFore(self):
        """Test setting the foreground colour attribute"""
        self.item.SetFore("#898989")
        self.assertEquals(self.item.GetFore(), "#898989")
        self.item.SetFore(None)
        self.assertEquals(self.item.GetFore(), "")

    def testSetFace(self):
        """Test setting the font attribute"""
        self.item.SetFace("TestFont")
        self.assertEquals(self.item.GetFace(), "TestFont")
        self.item.SetFace(None)
        self.assertEquals(self.item.GetFace(), "")

    def testSetSize(self):
        """Test setting the font size attribute"""
        self.item.SetSize(20)
        self.assertEquals(self.item.GetSize(), "20")
        self.item.SetSize(None)
        self.assertEquals(self.item.GetSize(), "")

    def testSetNamedAttr(self):
        """Test setting an attribute by name"""
        self.item.SetNamedAttr('face', 'FakeFont')
        self.assertEquals(self.item.GetFace(), "FakeFont")
        self.item.SetNamedAttr('fore', None)
        self.assertEquals(self.item.GetFore(), "")
