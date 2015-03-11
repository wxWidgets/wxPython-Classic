###############################################################################
# Name: nsistags.py                                                           #
# Purpose: Generate Tags for Nullsoft Installer Scripts                       #
# Author: Cody Precord <cprecord@editra.org>                                  #
# Copyright: (c) 2008 Cody Precord <staff@editra.org>                         #
# License: wxWindows License                                                  #
###############################################################################

"""
FILE: nsistags.py
AUTHOR: Cody Precord
LANGUAGE: Python
SUMMARY:
  Generate a DocStruct object that captures the structure of a NSIS Script. It
currently supports generating tags for Sections, Functions, and Macro defs.

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
    """Create a DocStruct object that represents a NSIS Script
    @param buff: a file like buffer object (StringIO)
    @todo: generate tags for lua tables?

    """
    rtags = taglib.DocStruct()

    # Set Descriptions of Document Element Types
    rtags.SetElementDescription('variable', "Defines")
    rtags.SetElementDescription('section', "Section Definitions")
    rtags.SetElementDescription('macro', "Macro Definitions")
    rtags.SetElementDescription('function', "Function Definitions")
    rtags.SetElementPriority('variable', 4)
    rtags.SetElementPriority('section', 3)
    rtags.SetElementPriority('function', 2)
    rtags.SetElementPriority('macro', 1)

    # Parse the lines for code objects
    for lnum, line in enumerate(buff):
        line = line.strip()
        llen = len(line)

        # Skip comment and empty lines
        if line.startswith(u"#") or line.startswith(u";") or not line:
            continue

        # Look for functions and sections
        if parselib.IsToken(line, 0, u'Function'):
            parts = line.split()
            if len(parts) > 1:
                rtags.AddFunction(taglib.Function(parts[1], lnum))
        elif parselib.IsToken(line, 0, u'Section'):
            parts = line.split()
            if len(parts) > 1 and parts[1][0] not in ['"', "'", "`"]:
                rtags.AddElement('section', taglib.Section(parts[1], lnum))
            else:
                for idx, part in enumerate(parts[1:]):
                    if parts[idx][-1] in ['"', "'", "`"]:
                        rtags.AddElement('section', taglib.Section(part, lnum))
                        break
        elif parselib.IsToken(line, 0, u'!macro'):
            parts = line.split()
            if len(parts) > 1:
                rtags.AddElement('macro', taglib.Macro(parts[1], lnum))
        elif parselib.IsToken(line, 0, u'!define'):
            parts = line.split()
            if len(parts) > 1 and parts[1][0].isalpha():
                rtags.AddVariable(taglib.Variable(parts[1], lnum))
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

