###############################################################################
# Name: testLogMsg.py                                                         #
# Purpose: Unittest for dev_tool.LogMsg                                       #
# Author: Cody Precord <cprecord@editra.org>                                  #
# Copyright: (c) 2008 Cody Precord <staff@editra.org>                         #
# License: wxWindows License                                                  #
###############################################################################

"""
Unittest for LogMsg class

"""

__author__ = "Cody Precord <cprecord@editra.org>"
__svnid__ = "$Id$"
__revision__ = "$Revision$"

#-----------------------------------------------------------------------------#
# Imports
import unittest

# Module to test
import dev_tool
import ebmlib

#-----------------------------------------------------------------------------#

class LogMsgTest(unittest.TestCase):
    def setUp(self):
        self.err = dev_tool.LogMsg("Error Message", "ed_main", "err")
        self.err2 = dev_tool.LogMsg("Error Message", "ed_stc", "err")
        self.warn = dev_tool.LogMsg("Warning Message", "ed_main", "warn")
        self.warn2 = dev_tool.LogMsg("Warning Message", "ed_stc", "warn")
        self.info = dev_tool.LogMsg("Info Message", "ed_main", "info")
        self.info2 = dev_tool.LogMsg("Info Message", "ed_stc", "info")

    def tearDown(self):
        pass

    #---- Method Tests ----#

    def testErrors(self):
        """Test error conditions"""
        self.assertRaises(AssertionError, dev_tool.LogMsg, 3, "foo", "bar")
        self.assertRaises(AssertionError, dev_tool.LogMsg, "foo", 2, "bar")
        self.assertRaises(AssertionError, dev_tool.LogMsg, "foo", "bar", 1)

    def testExpired(self):
        """Test Expired property"""
        self.assertFalse(self.err.Expired, "Message should not be expired")

        # Once a message has been displayed (converted to string) it is expired
        val = str(self.err)
        self.assertTrue(self.err.Expired, "Message should be expired")

    def testOrigin(self):
        """Test Origin property"""
        for msg in (self.err,  self.warn, self.info):
            self.assertEquals(msg.Origin, "ed_main", "%s != ed_main" % msg.Origin)
            self.assertTrue(isinstance(msg.Origin, basestring))

        for msg in (self.err2, self.warn2, self.info2):
            self.assertEquals(msg.Origin, "ed_stc", "%s != ed_stc" % msg.Origin)
            self.assertTrue(isinstance(msg.Origin, basestring))

    def testString(self):
        """Test conversion to bytestring"""
        msg1 = dev_tool.LogMsg("Error Message", "ed_main", "err")
        self.assertTrue(not ebmlib.IsUnicode(str(msg1)))

    def testType(self):
        """Test Type property"""
        self.assertEquals(self.err.Type, "err", "%s != err" % self.err.Type)
        self.assertTrue(isinstance(self.err.Type, basestring))

        self.assertEquals(self.warn.Type, "warn", "%s != err" % self.warn.Type)
        self.assertTrue(isinstance(self.warn.Type, basestring))

        self.assertEquals(self.info.Type, "info", "%s != err" % self.info.Type)
        self.assertTrue(isinstance(self.info.Type, basestring))

    def testUnicode(self):
        """Test that attributes are properly converted to Unicode"""
        msg1 = dev_tool.LogMsg("Error Message", "ed_main", "err")
        self.assertTrue(ebmlib.IsUnicode(msg1.Value))
        self.assertTrue(ebmlib.IsUnicode(msg1.Origin))
        self.assertTrue(ebmlib.IsUnicode(msg1.Type))
        self.assertTrue(ebmlib.IsUnicode(msg1.ClockTime))
        self.assertTrue(ebmlib.IsUnicode(unicode(msg1)))

        # Test with some non ascii values for conversion
        msg2 = dev_tool.LogMsg('\\u0259','\\u0259','\\u0259')
        self.assertTrue(ebmlib.IsUnicode(msg2.Value))
        self.assertTrue(ebmlib.IsUnicode(msg2.Origin))
        self.assertTrue(ebmlib.IsUnicode(msg2.Type))
        self.assertTrue(ebmlib.IsUnicode(unicode(msg2)))

    def testValue(self):
        """Test the message value property"""
        self.assertTrue(isinstance(self.err.Value, basestring))
        self.assertTrue(isinstance(self.warn.Value, basestring))
        self.assertTrue(isinstance(self.info.Value, basestring))
