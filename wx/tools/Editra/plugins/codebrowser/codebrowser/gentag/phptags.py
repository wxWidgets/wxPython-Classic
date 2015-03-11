###############################################################################
# Name: phptags.py                                                            #
# Purpose: Generate Tags for Php documents                                    #
# Author: Cody Precord <cprecord@editra.org>                                  #
# Copyright: (c) 2008 Cody Precord <staff@editra.org>                         #
# License: wxWindows License                                                  #
###############################################################################

"""
FILE: phptags.py
AUTHOR: Cody Precord
LANGUAGE: Python
SUMMARY:
  Generate a DocStruct object that captures the structure of a Php document.
Currently it supports parsing for Classes, Class Variables, Class Methods, and
Function Definitions.

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
    """Create a DocStruct object that represents a Php Script
    @param buff: a file like buffer object (StringIO)

    """
    rtags = taglib.DocStruct()

    # Setup document structure
    rtags.SetElementDescription('function', "Function Definitions")

    inphp = False        # Are we in a php section or not
    inclass = False      # Inside a class defintion
    incomment = False    # Inside a comment
    infundef = False     # Inside a function definition
    lastclass = None
    lastfun = None
    instring = False
    openb = 0            # Keep track of open brackets

    for lnum, line in enumerate(buff):
        line = line.strip()
        llen = len(line)
        idx = 0
        while idx < len(line):
            # Skip Whitespace
            idx = parselib.SkipWhitespace(line, idx)

            # Walk through strings ignoring contents
            if instring or line[idx] in (u"'", u'"'):
                idx, instring = parselib.FindStringEnd(line[idx:], idx)
                # For multiline strings
                if instring:
                    continue

            # Check if in a <?php ?> block or not
            if line[idx:].startswith(u'<?'):
                idx += 2
                if line[idx:].startswith(u'php'):
                    idx += 5
                inphp = True
            elif line[idx:].startswith(u'?>'):
                idx += 2
                inphp = False

            # Skip anything not in side of a php section
            if not inphp:
                idx += 1
                continue

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
            elif not infundef and parselib.IsToken(line, idx, u'class'):
                # Skip whitespace
                idx = parselib.SkipWhitespace(line, idx + 5)
                name = parselib.GetFirstIdentifier(line[idx:])
                if name is not None:
                    idx += len(name) # Move past the class name
                    lastclass = taglib.Class(name, lnum)
            elif parselib.IsToken(line, idx, u'function'):
                # Skip whitespace
                idx = parselib.SkipWhitespace(line, idx + 8)
                name = parselib.GetFirstIdentifier(line[idx:])
                if name is not None:
                    lastfun = name
                    # Skip whitespace
                    idx = parselib.SkipWhitespace(line, idx + len(name))

                    if line[idx] != u'(':
                        continue

                    if inclass and lastclass is not None:
                        lastclass.AddMethod(taglib.Method(name, lnum, lastclass.GetName()))
                    else:
                        rtags.AddFunction(taglib.Function(name, lnum))
            elif inclass and parselib.IsToken(line, idx, u'var'):
                # Look for class variables
                idx += 3
                parts = line[idx:].split()
                if len(parts) and parts[0].startswith(u'$'):
                    name = parselib.GetFirstIdentifier(parts[0][1:])
                    if name is not None and lastclass is not None:
                        name = u'$' + name
                        lastclass.AddVariable(taglib.Variable(name, lnum, lastclass.GetName()))
                        idx += len(name)
            else:
                idx += 1

    return rtags

#-----------------------------------------------------------------------------#
# Test
# Test
if __name__ == '__main__':
   import sys
   import StringIO

   fhandle = open(sys.argv[1])
   txt = fhandle.read()
   fhandle.close()
   tags = GenerateTags(StringIO.StringIO(txt))
   print "\n\nElements:"

   def printElements(elements):
       for element in elements:
           print "\n%s:" % element.keys()[0]
           for val in element.values()[0]:
               print "%s [%d]" % (val.GetName(), val.GetLine())
               if isinstance(val, taglib.Scope):
                   print "----"
                   printElements(val.GetElements())

   elements = tags.GetElements()
   printElements(elements)
   print "END"
