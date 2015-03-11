###############################################################################
# Name: shtags.py                                                             #
# Purpose: Generate Tags for Shell Scripts                                    #
# Author: Cody Precord <cprecord@editra.org>                                  #
# Copyright: (c) 2008 Cody Precord <staff@editra.org>                         #
# License: wxWindows License                                                  #
###############################################################################

"""
FILE: shtags.py
AUTHOR: Cody Precord
LANGUAGE: Python
SUMMARY:
  Generate a DocStruct object that captures the structure of a shell script,
the returned structure contains all the function definitions in the document.
It currently should work well with Bourne, Bash, Korn, and C-Shell scripts.

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
    """Create a DocStruct object that represents a Shell Script
    @param buff: a file like buffer object (StringIO)

    """
    rtags = taglib.DocStruct()
    rtags.SetElementDescription('function', "Function Definitions")

    for lnum, line in enumerate(buff):
        line = line.strip()

        # Skip comment and empty lines
        if line.startswith(u"#") or not line:
            continue

        # Check Regular Function Defs
        if parselib.IsToken(line, 0, u'function'):
            parts = line.split()
            plen = len(parts)
            if plen >= 2 and parselib.IsGoodName(parts[1]):
                if plen == 2 or parts[2] == u"{":
                    rtags.AddFunction(taglib.Function(parts[1], lnum))
            continue

        # Check fname () function defs
        if u"(" in line:
            parts = line.split()
            plen = len(parts)
            if plen >= 2 and parselib.IsGoodName(parts[0]):
                if u''.join(parts[1:]).startswith("()"):
                    rtags.AddFunction(taglib.Function(parts[0], lnum))
            else:
                continue

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
