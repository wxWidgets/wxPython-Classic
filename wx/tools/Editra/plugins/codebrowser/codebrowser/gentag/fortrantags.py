###############################################################################
# Name: fortrantags.py                                                        #
# Purpose: Generate Tags for Fortran                                          #
# Author: Cody Precord <cprecord@editra.org>                                  #
# Copyright: (c) 2008 Cody Precord <staff@editra.org>                         #
# License: wxWindows License                                                  #
###############################################################################

"""
FILE: fortrantags.py
AUTHOR: Cody Precord
LANGUAGE: Python
SUMMARY:
  Generate a DocStruct object that captures the structure of a Fortran.
Currently supports parsing for Programs, Subroutines, and Functions.

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
    """Create a DocStruct object that represents a Fortran
    @param buff: a file like buffer object (StringIO)

    """
    rtags = taglib.DocStruct()
    rtags.SetElementDescription('program', "Programs")
    rtags.SetElementPriority('program', 3)
    rtags.SetElementDescription('subroutine', "Subroutines")
    rtags.SetElementPriority('subroutine', 2)
    rtags.SetElementDescription('function', "Function Definitions")
    rtags.SetElementPriority('function', 1)

    for lnum, line in enumerate(buff):
        line = line.strip()

        # Skip comment and empty lines
        if line.startswith(u"!") or line.startswith(u"*") or not line:
            continue

        # Temporary variables
        llen = len(line)
        tline = line.lower()

        # Check Program, Subroutine, and Function Defs
        if tline.startswith(u'program') and llen > 7 and line[7].isspace():
            name = parselib.GetFirstIdentifier(line[7:].strip())
            rtags.AddElement('program', Program(name, lnum))
        elif tline.startswith(u'subroutine') and llen > 10 and line[10].isspace():
            name = parselib.GetFirstIdentifier(line[10:].strip())
            rtags.AddElement('subroutine', taglib.Function(name, lnum, 'subroutine'))
        elif tline.startswith(u'function') and llen > 8 and line[8].isspace():
            name = parselib.GetFirstIdentifier(line[8:].strip())
            rtags.AddFunction(taglib.Function(name, lnum))
        else:
            pass
    return rtags

#-----------------------------------------------------------------------------#
# Utilities
class Program(taglib.Scope):
    """Program Code Object"""
    def __init__(self, name, line, scope=None):
        taglib.Scope.__init__(self, name, line, "program", scope)

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

