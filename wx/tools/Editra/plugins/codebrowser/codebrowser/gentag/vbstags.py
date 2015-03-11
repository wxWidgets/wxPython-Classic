###############################################################################
# Name: vbstags.py                                                            #
# Purpose: Generate Tags for Fortran                                          #
# Author: Cody Precord <cprecord@editra.org>                                  #
# Copyright: (c) 2008 Cody Precord <staff@editra.org>                         #
# License: wxWindows License                                                  #
###############################################################################

"""
FILE: vbstags.py
AUTHOR: Cody Precord
LANGUAGE: Python
SUMMARY:
  Generate a DocStruct object that captures the structure of a VBScript
document.

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
    rtags.SetElementDescription('pubfunct', "Public Functions")
    rtags.SetElementPriority('pubfunct', 4)
    rtags.SetElementDescription('function', "Functions")
    rtags.SetElementPriority('function', 3)
    rtags.SetElementDescription('pubsub', "Public Subroutines")
    rtags.SetElementPriority('pubsub', 2)
    rtags.SetElementDescription('subroutine', "Subroutines")
    rtags.SetElementPriority('subroutine', 1)

    for lnum, line in enumerate(buff):
        line = line.strip()

        # Skip comment and empty lines
        if line.startswith(u"'") or not line:
            continue

        # Temporary variables
        llen = len(line)
        tline = line.lower()

        # Check Subroutine, and Function Defs
        if tline.startswith(u'sub') and llen > 3 and line[3].isspace():
            name = parselib.GetFirstIdentifier(line[3:].strip())
            rtags.AddElement('sub', taglib.Function(name, lnum, 'subroutine'))
        elif tline.startswith(u'public sub') and llen > 10 and line[10].isspace():
            name = parselib.GetFirstIdentifier(line[10:].strip())
            rtags.AddElement('pubsub', taglib.Function(name, lnum, 'pubsub'))
        elif tline.startswith(u'function') and llen > 8 and line[8].isspace():
            name = parselib.GetFirstIdentifier(line[8:].strip())
            rtags.AddFunction(taglib.Function(name, lnum))
        elif tline.startswith(u'public function') and llen > 15 and line[15].isspace():
            name = parselib.GetFirstIdentifier(line[15:].strip())
            rtags.AddElement('pubfunct', taglib.Function(name, lnum, 'pubfunct'))
        else:
            pass
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

