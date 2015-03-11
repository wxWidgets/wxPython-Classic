###############################################################################
# Name: sqltags.py                                                            #
# Purpose: Generate Tags for Sql, PL/SQL  documents                           #
# Author: Cody Precord <cprecord@editra.org>                                  #
# Copyright: (c) 2008 Cody Precord <staff@editra.org>                         #
# License: wxWindows License                                                  #
###############################################################################

"""
FILE: sqltags.py
AUTHOR: Cody Precord
LANGUAGE: Python
SUMMARY:
  Generate a DocStruct object that captures the structure of a SQL document.
Currently it supports parsing for Functions and Procedures

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
    """Create a DocStruct object that represents a SQL document
    @param buff: a file like buffer object (StringIO)

    """
    rtags = taglib.DocStruct()

    # Setup document structure
    rtags.SetElementDescription('function', "Function Definitions")
    rtags.SetElementDescription('procedure', "Procedure Definitions")
    rtags.SetElementDescription('package', "Packages")
    rtags.SetElementPriority('package', 3)
    rtags.SetElementPriority('function', 2)
    rtags.SetElementPriority('procedure', 1)

    # State Variables
    inpackage = False    # Inside a package
    incomment = False    # Inside a comment
    infunpro = False     # Inside a function or proceedure definition
    lastname = None      # Name of last found element
    lastpkg = None       # Last found package object
    lastpkgname = None   # Name of last package

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
            elif line[idx:].startswith(u'--') or line[idx:].startswith(u'#'):
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
            elif (inpackage or infunpro) and \
                 parselib.IsToken(line, idx, u'end', True):
                idx = parselib.SkipWhitespace(line, idx + 3)
                name = parselib.GetFirstIdentifier(line[idx:])
                if inpackage and name == lastpkgname:
                    inpackage = False
                    lastpkgname = None
                elif infunpro and name == lastname:
                    infunpro = False
                    lastname = None
            elif not infunpro and parselib.IsToken(line, idx, u'package', True):
                # Skip whitespace
                idx = parselib.SkipWhitespace(line, idx + 7)
                name = parselib.GetFirstIdentifier(line[idx:])
                if name is not None and name.lower() == u'body':
                    idx = parselib.SkipWhitespace(line, idx + 3)
                    name = parselib.GetFirstIdentifier(line[idx:])

                if name is not None:
                    inpackage = True
                    lastpkgname = name
                    lastpkg = taglib.Package(name, lnum)
                    rtags.AddElement('package', lastpkg)
            elif parselib.IsToken(line, idx, u'function', True):
                # Skip whitespace
                idx = parselib.SkipWhitespace(line, idx + 8)
                name = parselib.GetFirstIdentifier(line[idx:])
                if name is not None:
                    infunpro = True
                    lastname = name
                    if lastpkg is not None:
                        lastpkg.AddElement('function', taglib.Function(name, lnum))
                    else:
                        rtags.AddFunction(taglib.Function(name, lnum))
            elif parselib.IsToken(line, idx, u'procedure', True):
                # Skip whitespace
                idx = parselib.SkipWhitespace(line, idx + 9)
                name = parselib.GetFirstIdentifier(line[idx:])
                if name is not None:
                    infunpro = True
                    lastname = name
                    if lastpkg is not None:
                        lastpkg.AddElement('procedure', taglib.Procedure(name, lnum))
                    else:
                        rtags.AddElement('procedure', taglib.Procedure(name, lnum))
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
