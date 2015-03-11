###############################################################################
# Name: innotags.py                                                           #
# Purpose: Generate Tags for Inno Setup Scripts                               #
# Author: Cody Precord <cprecord@editra.org>                                  #
# Copyright: (c) 2008 Cody Precord <staff@editra.org>                         #
# License: wxWindows License                                                  #
###############################################################################

"""
FILE: innotags.py
AUTHOR: Cody Precord
LANGUAGE: Python
SUMMARY:
  Generate a DocStruct object that captures the structure of a Inno Setup Script
Currently supports parsing of Sections, Function Definitions, Procedure
Definitions, and Global Define statements.

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
    """Create a DocStruct object that represents an Inno Setup Script
    @param buff: a file like buffer object (StringIO)
    @todo: perhaps group functions, procedures within the Scope of a Section
           object.

    """
    rtags = taglib.DocStruct()
    rtags.SetElementDescription('section', "Sections")
    rtags.SetElementDescription('variable', "Defines")
    rtags.SetElementDescription('function', "Function Definitions")
    rtags.SetElementDescription('procedure', "Procedure Definitions")
    rtags.SetElementPriority('section', 3)
    rtags.SetElementPriority('function', 2)
    rtags.SetElementPriority('procedure', 1)

    for lnum, line in enumerate(buff):
        line = line.strip()

        # Skip comment and empty lines
        if line.startswith(u";") or not line:
            continue

        # Check for a section
        if line.startswith(u"["):
            secend = line.find(u"]")
            if secend != -1:
                section = taglib.Section(line[1:secend], lnum)
                rtags.AddElement('section', section)
        elif parselib.IsToken(line, 0, u'function'):
            name = parselib.GetFirstIdentifier(line[8:].strip())
            if name is not None:
                rtags.AddFunction(taglib.Function(name, lnum))
        elif parselib.IsToken(line, 0, u'procedure'):
            name = parselib.GetFirstIdentifier(line[9:].strip())
            if name is not None:
                rtags.AddElement('procedure',
                                 taglib.Function(name, lnum, 'procedure'))
        elif parselib.IsToken(line, 0, u'#define'):
            name = parselib.GetFirstIdentifier(line[7:].strip())
            if name is not None:
                rtags.AddVariable(taglib.Variable(name, lnum))
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
