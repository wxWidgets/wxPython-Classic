###############################################################################
# Name: testFactory.py                                                        #
# Purpose: Unit tests for the FactoryMixin.                                   #
# Author: Cody Precord <cprecord@editra.org>                                  #
# Copyright: (c) 2011 Cody Precord <staff@editra.org>                         #
# License: wxWindows License                                                  #
###############################################################################

"""Unittest cases for testing ebmlib.FactoryMixin"""

__author__ = "Cody Precord <cprecord@editra.org>"
__svnid__ = "$Id$"
__revision__ = "$Revision$"

#-----------------------------------------------------------------------------#
# Imports
import unittest

# Module to test
import ebmlib

#-----------------------------------------------------------------------------#
# Test Class

class FactoryTest(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testFactoryCreate(self):
        obj = BaseWidget.FactoryCreate('foo')
        self.assertTrue(isinstance(obj, FooWidget))
        self.assertTrue(obj.meta.data == 'FOOBAR')
        obj = BaseWidget.FactoryCreate('bar')
        self.assertTrue(isinstance(obj, BarWidget))
        self.assertTrue(obj.meta.data == 'NULL')
        obj = BaseWidget.FactoryCreate('junk')
        self.assertTrue(type(obj) is BaseWidget)

#-----------------------------------------------------------------------------#

# Test classes to test factory

class BaseWidget(ebmlib.FactoryMixin):
    def __init__(self):
        super(BaseWidget, self).__init__()

    @classmethod
    def GetMetaDefaults(cls):
        return dict(id=None, data="NULL")

class FooWidget(BaseWidget):
    class meta:
        id = "foo"
        data = "FOOBAR"

class BarWidget(BaseWidget):
    class meta:
        id = "bar"
