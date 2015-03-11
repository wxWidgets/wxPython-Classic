###############################################################################
# Name: batchtags.py                                                          #
# Purpose: Generate Tags for Batch Scripts                                    #
# Author: Cody Precord <cprecord@editra.org>                                  #
# Copyright: (c) 2008 Cody Precord <staff@editra.org>                         #
# License: wxWindows License                                                  #
###############################################################################

"""
FILE: batchtags.py
AUTHOR: Cody Precord
LANGUAGE: Python
SUMMARY:
  Generate a DocStruct object that captures the structure of a Dos Batch Script.
Currently it supports parsing and generation of Labels.

"""

__author__ = "Cody Precord <cprecord@editra.org>"
__svnid__ = "$Id$"
__revision__ = "$Revision$"

#--------------------------------------------------------------------------#
# Dependancies
import taglib
import parselib

#--------------------------------------------------------------------------#

def GenerateTags(buff):
    """Create a DocStruct object that represents a batch Script
    @param buff: a file like buffer object (StringIO)
    @todo: generate tags for batch tables?

    """
    rtags = taglib.DocStruct()
    rtags.SetElementDescription('label', "Labels")
    rtags.SetElementDescription('section', "Labels")

    for lnum, line in enumerate(buff):
        line = line.strip()
        llen = len(line)

        # Skip comment and empty lines
        if (line.startswith(u"rem") and llen > 3 and line[3].isspace()) or not line:
            continue

        # Check for labels
        if line.startswith(u":"):
            name = parselib.GetFirstIdentifier(line[1:])
            if name is not None:
                rtags.AddElement('label', taglib.Section(name, lnum))

    return rtags

#-----------------------------------------------------------------------------#
# Test
if __name__ == '__main__':
    import sys
    import StringIO
    fhandle = open(sys.argv[1])
    txt = fhandle.read()
    fhandle.close()
    tags = GenerateTags(StringIO.StringIO(txt))
    print "\n\nElements:"
    for element in tags.GetElements():
        print "\n%s:" % element.keys()[0]
        for val in element.values()[0]:
            print "%s [%d]" % (val.GetName(), val.GetLine())
    print "END"
