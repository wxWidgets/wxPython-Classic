###############################################################################
# Name: testProfile.py                                                        #
# Purpose: Unittest for settings persistance.                                 #
# Author: Cody Precord <cprecord@editra.org>                                  #
# Copyright: (c) 2009 Cody Precord <staff@editra.org>                         #
# License: wxWindows License                                                  #
###############################################################################

"""
Unittest for User Profile and settings persistance.

"""

__author__ = "Cody Precord <cprecord@editra.org>"
__svnid__ = "$Id$"
__revision__ = "$Revision$"

#-----------------------------------------------------------------------------#
# Imports
import unittest

# Module to test
import ed_msg
import profiler

#-----------------------------------------------------------------------------#

class ProfileTest(unittest.TestCase):
    def setUp(self):
        # Create the singleton profile object
        self._profile = profiler.TheProfile
        self._save = self._profile.copy()
        ed_msg.Subscribe(self.OnConfigMsg,
                         ed_msg.EDMSG_PROFILE_CHANGE + ('test',))

    def tearDown(self):
        ed_msg.Unsubscribe(self.OnConfigMsg)
        self._profile.update(self._save)

    def OnConfigMsg(self, msg):
        mtype = msg.GetType()
        mdata = msg.GetData()
        self.assertEquals(mtype[-1], 'test') 
        self.assertEquals(mdata, "TEST VALUE")

    #---- Begin Test Cases ----#

    def testConfigMessage(self):
        """Test configuration message notifications
        @see: OnConfigMsg

        """
        self._profile.Set('test', "TEST VALUE")

    def testIdentity(self):
        """Test that only one profile object can be created."""
        self.assertTrue(self._profile is profiler.Profile())

    def testLoadDefaultValues(self):
        """Test that default values are returned when no saved profile has been
        loaded.

        """
        # Load the default settings
        self._profile.LoadDefaults()

        # Try retrieving some values from it
        self.assertEquals(self._profile.Get('EDGE'), profiler._DEFAULTS['EDGE'])

        # Test a value that doesn't exist
        self.assertTrue(self._profile.Get('FAKEKEYTOFETCH') is None)

        # Test fallback value
        self.assertEquals(self._profile.Get('FAKEKEYTOFETCH', default="hello"), "hello")

    def testChangeValue(self):
        """Test changing an existing profile value."""
        self.assertTrue(self._profile.Get('TEST1') is None)

        # Now change the value
        self._profile.Set('TEST1', 123)
        self.assertTrue(self._profile.Get('TEST1') == 123)

    def testDeleteValue(self):
        """Test removing a value from the object."""
        # Add a value
        self._profile.Set('TEST2', "myString")
        self.assertTrue(self._profile.Get('TEST2') == "myString")

        # Now try to delete it
        self._profile.DeleteItem('TEST2')
        self.assertTrue(self._profile.Get('TEST2') is None)

    def testLoadProfile(self):
        """Test loading a stored profile."""
        # Add some values to the profile
        #TODO: should re-org profile support functions to make testing this
        #      not require modifing the installed profile loader.
#        self._profile.Set('VALUE1', 25)
#        self._profile.Set('VALUE2', "string")
#        self._profile.Write(

    def testSingleton(self):
        """Test that only the single instance of the Profile can be used"""
        self._profile.Set('UNIQUEVALUE', 'MYVALUE!!')
        new_profile = profiler.Profile()
        val = new_profile.Get('UNIQUEVALUE')
        self.assertEquals(val, 'MYVALUE!!')
        self.assertTrue(self._profile is new_profile)

    def testWrite(self):
        """Test writing the settings out to disk."""
        pass

    def testUpdate(self):
        """Test updating the profile from a dictionary."""
        pass

    #---- Tests for module level functions ----#

    def testCalcVersionValue(self):
        """Test the version value calculation function."""
        v1 = profiler.CalcVersionValue("1.0.0")
        v2 = profiler.CalcVersionValue("1.0.1")
        self.assertTrue(v1 < v2)
