###############################################################################
# Name: dtags.py                                                              #
# Purpose: Generate Tags for D Source code                                    #
# Author: Cody Precord <cprecord@editra.org>                                  #
# Copyright: (c) 2008 Cody Precord <staff@editra.org>                         #
# License: wxWindows License                                                  #
###############################################################################

"""
DocStruct generator for the D programming language.

@author: Cody Precord
@summary: Generate a DocStruct object that captures the structure of D source code.

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

RE_FUNC = re.compile(r"([A-Za-z0-9_]+\s+)+([*A-Za-z0-9_::]+)\s*\([^)]*\)")
RE_CLASS = re.compile(r"class\s([A-Za-z][A-Za-z0-9_]*)")
RE_METH = re.compile(r"(public|private|protected)\s([A-Za-z0-9_]+\s+)+([A-Za-z0-9_]+)\s*\([^)]*\)")

#--------------------------------------------------------------------------#

def GenerateTags(buff):
    """Create a DocStruct object that represents the structure of a D source
    file.
    @param buff: a file like buffer object (StringIO)

    """
    rtags = taglib.DocStruct()
    rtags.SetElementDescription('class', "Class Definitions")
    rtags.SetElementPriority('class', 3)
    rtags.SetElementDescription('function', "Function Definitions")
    rtags.SetElementPriority('function', 1)

    # State Variables
    incomment = False
    inclass = False
    lastclass = None

    # Note: comments can begin with // /* /+

    # Parse the buffer
    # Simple line based parser, likely not to be accurate in all cases
    for lnum, line in enumerate(buff):

        line = line.strip()

        if incomment:
            continue

        # Check for a class definition
        match = RE_CLASS.match(line)
        if match is not None:
            cname = match.groups()[0]
            cobj = taglib.Class(cname, lnum)
            rtags.AddClass(cobj)
            lastclass = cobj # save ref to the class obj
            continue

        if lastclass is not None:
            # Check for a class method
            match = RE_METH.match(line)
            if match is not None:
                groups = match.groups()
                lastclass.AddMethod(taglib.Method(groups[-1], lnum))
                continue

            fobj = CheckForFunction(line, lnum)
            if fobj is not None:
                fname = fobj.GetName()
                if fname == 'this':
                    lastclass.AddMethod(taglib.Method(fname, lnum))
#                else:
#                    print "OUT OF SCOPE", lnum
#                    lastclass = None # Must have left the classes scope
#                    rtags.AddFunction(fobj)
            continue

        fobj = CheckForFunction(line, lnum)
        if fobj is not None:
            rtags.AddFunction(fobj)

    return rtags

#-----------------------------------------------------------------------------#

def CheckForFunction(line, lnum):
    """Check for a function definition
    @param line: line to check
    @param lnum: line num
    @return: None or Function object

    """
    match = RE_FUNC.match(line)
    if match is not None:
        fname = match.groups()[-1]
        fobj = taglib.Function(fname, lnum)
        return fobj
    else:
        return None

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

            if isinstance(val, taglib.Scope):
                for sobj in val.GetElements():
                    for meth in sobj.values()[0]:
                        print "\t%s [%d]" % (meth.GetName(), meth.GetLine())
    print "END"
