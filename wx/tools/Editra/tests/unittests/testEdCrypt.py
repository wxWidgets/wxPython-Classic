###############################################################################
# Name: testEdCrypt.py                                                        #
# Purpose: Unit tests for the ed_crypt module utilities                       #
# Author: Cody Precord <cprecord@editra.org>                                  #
# Copyright: (c) 2009 Cody Precord <staff@editra.org>                         #
# License: wxWindows License                                                  #
###############################################################################

"""Unittest cases for testing the ed_crypt utilities"""

__author__ = "Cody Precord <cprecord@editra.org>"
__svnid__ = "$Id$"
__revision__ = "$Revision$"

#-----------------------------------------------------------------------------#
# Imports
import os
import unittest

# Module to test
import ed_crypt

#-----------------------------------------------------------------------------#
# Test Class

class EdCryptTest(unittest.TestCase):
    """Tests for the ed_crypt utilties"""
    def setUp(self):
        self.salt = os.urandom(8)
        self.secret = "hello world"

    def tearDown(self):
        pass

    #---- Test Cases ----#

    def testEncrypt(self):
        """Test Encrypting a string"""
        e_str = ed_crypt.Encrypt(self.secret, self.salt)
        self.assertTrue(e_str != self.secret)
        self.assertTrue(len(e_str) > 0)

    def testDecrypt(self):
        """Test decrypting a string"""
        e_str = ed_crypt.Encrypt(self.secret, self.salt)
        self.assertTrue(e_str != self.secret)
        self.assertTrue(len(e_str) > 0)

        d_str = ed_crypt.Decrypt(e_str, self.salt)
        self.assertTrue(d_str == self.secret)
