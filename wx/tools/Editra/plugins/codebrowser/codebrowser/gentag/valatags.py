###############################################################################
# Name: valatags.py                                                           #
# Purpose: Generate Tags for Vala documents                                   #
# Author: Cody Precord <cprecord@editra.org>                                  #
# Copyright: (c) 2009 Cody Precord <staff@editra.org>                         #
# License: wxWindows License                                                  #
###############################################################################

"""
FILE: valatags.py
AUTHOR: Cody Precord
LANGUAGE: Python
SUMMARY:
  Generate a DocStruct object that captures the structure of a Vala document.
Currently it supports parsing for Classes, Class Methods, and Function
Definitions.

"""

__author__ = "Cody Precord <cprecord@editra.org>"
__svnid__ = "$Id$"
__revision__ = "$Revision$"

#--------------------------------------------------------------------------#
# Imports
import re

# Local Imports
import taglib
import parselib

#--------------------------------------------------------------------------#
# Globals

RE_METH = re.compile(r"([A-Za-z0-9_]+\s+)+([A-Za-z0-9_:]+)\s*\([^)]*\){0,1}\s*")
KEYWORDS = "if else for while catch do"

#--------------------------------------------------------------------------#

def GenerateTags(buff):
    """Create a DocStruct object that represents a vala dacument
    @param buff: a file like buffer object (StringIO)

    """
    rtags = taglib.DocStruct()

    # Setup document structure
    rtags.SetElementDescription('function', "Function Definitions")

    inclass = False      # Inside a class defintion
    incomment = False    # Inside a comment
    infundef = False     # Inside a function definition
    lastclass = None
    lastfun = None
    openb = 0            # Keep track of open brackets

    for lnum, line in enumerate(buff):
        line = line.strip()
        llen = len(line)
        idx = 0
        while idx < len(line):
            # Skip Whitespace
            idx = parselib.SkipWhitespace(line, idx)

            # Check for coments
            if line[idx:].startswith(u'/*'):
                idx += 2
                incomment = True
            elif line[idx:].startswith(u'//') or line[idx:].startswith(u'#'):
                break # go to next line
            elif line[idx:].startswith(u'*/'):
                idx += 2
                incomment = False

            # At end of line
            if idx >= llen:
                break

            # Look for tags
            if incomment:
                idx += 1
                continue
            elif line[idx] == u'{':
                idx += 1
                openb += 1
                # Class name must be followed by a {
                if not inclass and lastclass is not None:
                    inclass = True
                    rtags.AddClass(lastclass)
                elif lastfun is not None:
                    infundef = True
                    lastfun = None
                else:
                    pass
                continue
            elif line[idx] == u'}':
                idx += 1
                openb -= 1
                if inclass and openb == 0:
                    inclass = False
                    lastclass = None
                elif infundef and inclass and openb == 1:
                    infundef = False
                elif infundef and openb == 0:
                    infundef = False
                    lastfun = None
                else:
                    pass
                continue
            elif not infundef and parselib.IsToken(line, idx, u'class'):
                # Skip whitespace
                idx = parselib.SkipWhitespace(line, idx + 5)
                name = parselib.GetFirstIdentifier(line[idx:])
                if name is not None:
                    idx += len(name) # Move past the class name
                    lastclass = taglib.Class(name, lnum)
                continue

            match = RE_METH.match(line[idx:])
            if match is not None:
                # Check that not a method call
                sline = line.strip()
                if sline.endswith(u';'):
                    idx += match.end(2)
                    continue

                # Most likely a definition so store it in the DocStruct
                name = match.group(2)

                # Secondary check for other end cases regex will find
                if name in KEYWORDS:
                    idx += match.end(2)
                    continue

                lastfun = name
                if inclass and lastclass is not None:
                    lastclass.AddMethod(taglib.Method(name, lnum, lastclass.GetName()))
                else:
                    rtags.AddFunction(taglib.Function(name, lnum))
                idx += match.end(2)
            else:
                idx += 1

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
