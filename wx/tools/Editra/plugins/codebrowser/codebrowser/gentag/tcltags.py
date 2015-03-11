###############################################################################
# Name: tcltags.py                                                            #
# Purpose: Generate Tags for Tcl Scripts                                      #
# Author: Cody Precord <cprecord@editra.org>                                  #
# Copyright: (c) 2008 Cody Precord <staff@editra.org>                         #
# License: wxWindows License                                                  #
###############################################################################

"""
FILE: tcltags.py
AUTHOR: Cody Precord
LANGUAGE: Python
SUMMARY:
  Generate a DocStruct object that captures the structure of a Tcl Scripts.
Currently supports searching for Procedure definitions.

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
    """Create a DocStruct object that represents a Tcl Script
    @param buff: a file like buffer object (StringIO)

    """
    rtags = taglib.DocStruct()
    rtags.SetElementDescription('procedure', "Procedure Definitions")
    rtags.SetElementDescription('class', "SNIT")

    # Scope tracking for SNIT blocks
    insnit = False
    cursnit = None
    openparens = 0

    for lnum, line in enumerate(buff):
        line = line.strip()

        # Skip comment and empty lines
        if line.startswith(u"#") or not line:
            continue

        if insnit and cursnit is not None:
            if parselib.IsToken(line, 0, u'method') or \
               parselib.IsToken(line, 0, u'typemethod'):
                parts = line.split()
                if len(parts) > 1:
                    name = parts[1]
                    cursnit.AddMethod(taglib.Method(name, lnum))
            elif parselib.IsToken(line, 0, u'typevariable') or \
                 parselib.IsToken(line, 0, u'variable'):
                parts = line.split()
                if len(parts) > 1:
                    name = parts[1]
                    cursnit.AddVariable(taglib.Variable(name, lnum))
            elif parselib.IsToken(u'constructor', 0, line) or \
                 parselib.IsToken(u'destructor', 0, line):
                 name = parselib.GetFirstIdentifier(line)
                 cursnit.AddMethod(taglib.Method(name, lnum))
            elif parselib.IsToken(line, 0, u"package"):
                 pkg = GetPackage(line, lnum)
                 if pkg:
                     cursnit.AddElement('package', pkg)

            # Update Scope
            openparens += GetParenCount(line)
            if openparens == 0:
                insnit = False
                cursnit = None
            continue

        # Check for Procedure defs
        if parselib.IsToken(line, 0, u'proc'):
            parts = line.split()
            if len(parts) > 1:
                name = parts[1]
                if u"::" in name:
                    spaces = name.split("::")
                    space_l = rtags.GetElement('namespace', spaces[0])
                    if space_l == None:
                        space_l = taglib.Namespace(spaces[0], lnum)
                        rtags.AddElement('namespace', space_l)
                    space_l.AddElement('procedure', taglib.Procedure(spaces[-1], lnum))
                else:
                    rtags.AddElement('procedure', taglib.Procedure(parts[1], lnum))
        elif line.startswith(u'snit::'):
            parts = line.split()
            if len(parts) > 1:
                insnit = True
                openparens = GetParenCount(line)
                name = parts[1]
                cursnit = taglib.Class(name, lnum)
                rtags.AddClass(cursnit)
        elif parselib.IsToken(line, 0, u"package"):
             pkg = GetPackage(line, lnum)
             if pkg:
                 rtags.AddElement('package', pkg)

    return rtags


# Helper functions

def GetParenCount(line):
    """Get the delta of parens on the given line"""
    openparens = line.count(u"{")
    openparens -= line.count(u"}")
    return openparens

def GetPackage(line, lnum):
    """Get a package object from the current line
    @precondition: line has a package def on it

    """
    package = None
    parts = line.split()
    # package require name version
    if len(parts) >= 3:
        name = u" ".join(parts[2:])
        package = taglib.Package(name, lnum)
    return package

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
