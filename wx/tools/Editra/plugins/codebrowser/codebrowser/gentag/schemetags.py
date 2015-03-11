###############################################################################
# Name: schemetags.py                                                         #
# Purpose: Generate Tags for Scheme                                           #
# Author: Cody Precord <cprecord@editra.org>                                  #
# Copyright: (c) 2008 Cody Precord <staff@editra.org>                         #
# License: wxWindows License                                                  #
###############################################################################

"""
FILE: schemetags.py
AUTHOR: Cody Precord
LANGUAGE: Python
SUMMARY:
  Generate a DocStruct object that captures the structure of Scheme code

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
    """Create a DocStruct object that represents a Scheme document
    @param buff: a file like buffer object (StringIO)

    """
    rtags = taglib.DocStruct()
    rtags.SetElementDescription('function', "Function Definitions")

    for lnum, line in enumerate(buff):
        line = line.strip()

        # Skip comment and empty lines
        if line.startswith(u";") or not line:
            continue

        # Check Function Definitions
        if line.startswith('(') and u'define' in line:
            llen = len(line)
            idx = 1
            idx += (len(line[idx:]) - len(line[idx:].lstrip()))
            if llen > idx and line[idx:].startswith(u'define') and \
               (llen > (idx + 6)) and line[idx+6].isspace():
                idx = parselib.SkipWhitespace(line, idx + 6)
                if llen > idx and line[idx] == u'(':
                    # function with parameters
                    idx = parselib.SkipWhitespace(line, idx + 1)
                name = GetIdentifierName(line[idx:])
                if name is not None:
                    rtags.AddFunction(taglib.Function(name, lnum))

    return rtags

#-----------------------------------------------------------------------------#
# Utilities
def GetIdentifierName(line):
    """Get the identifier name starting at the begining of the given line
    if no valid identifier is found None is returned instead.
    @param line: string to extract identifier from
    @return: string or None

    """
    rstr = None
    if len(line) and line[0].isalpha():
        rstr = u''
        for char in line:
            if char.isalnum() or char in ('_', '-'):
                rstr += char
            else:
                break

        if not len(rstr):
            rstr = None
    return rstr

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
