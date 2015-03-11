###############################################################################
# Name: __ini__.py                                                            #
# Purpose: Tag Generator Library                                              #
# Author: Cody Precord <cprecord@editra.org>                                  #
# Copyright: (c) 2008 Cody Precord <staff@editra.org>                         #
# License: wxWindows License                                                  #
###############################################################################

"""
This library provides modules for generating a document structure object that
generalizes the code structure of various different document types. The library
can be easily extended by adding a new module for a new language type that
populates a L{taglib.DocStruct} object using the various classes and api's
available in L{taglib}.

The taglib module contains the basic api for capturing the structure of the
code in a document in an object oriented manner. Many common code element type
classes are provided in taglib to populate the DocStruct with for more
information on how to use this api and extend it see L{taglib}.

"""

__author__ = "Cody Precord <cprecord@editra.org>"
__svnid__ = "$Id$"
__revision__ = "$Revision$"
