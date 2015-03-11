###############################################################################
# Name: ctags.py                                                              #
# Purpose: Generate Tags for C Source code                                    #
# Author: Cody Precord <cprecord@editra.org>                                  #
# Copyright: (c) 2008 Cody Precord <staff@editra.org>                         #
# License: wxWindows License                                                  #
###############################################################################

"""
FILE: ctags.py
AUTHOR: Cody Precord
LANGUAGE: Python
SUMMARY:
  Generate a DocStruct object that captures the structure of C source code.

@todo: add support for typdefs/structs/enum
@todo: detection of cpp ctor/dtor does not work

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

RE_METH = re.compile(r"([A-Za-z0-9_*&]+\s+)+([&*~A-Za-z0-9_:]+)\s*\([^)]*\)\s*(const)*\s*\{")
RE_DEF = re.compile(r"#define[ \t]+([A-Za-z0-9_]+)")

#--------------------------------------------------------------------------#

def GenerateTags(buff):
    """Create a DocStruct object that represents the structure of a C source
    file.
    @param buff: a file like buffer object (StringIO)

    """
    rtags = taglib.DocStruct()
    rtags.SetElementDescription('macro', "Macros")
    rtags.SetElementPriority('macro', 3)
    rtags.SetElementDescription('class', "Class Definitions")
    rtags.SetElementPriority('class', 2)
    rtags.SetElementDescription('function', "Function Definitions")
    rtags.SetElementPriority('function', 1)

    kwords = ("if else for while switch case catch")
    txt = buff.read()

    # Get class/method/function definitions
    for match in RE_METH.finditer(txt):
        fname = match.group(2)
        if fname and fname not in kwords:
            line = txt.count('\n', 0, match.start(2))
            if u"::" in fname:
                scopes = fname.split("::")
                cname = scopes[0].lstrip('*')
                cname = scopes[0].lstrip('&')
                cobj = rtags.GetElement('class', cname)
                if cobj == None:
                    cobj = taglib.Class(cname, line)
                    rtags.AddClass(cobj)
                cobj.AddMethod(taglib.Method(u'::'.join(scopes[1:]), line))
            else:
                fname = fname.replace("*", "")
                fname = fname.replace("&", "")
                rtags.AddFunction(taglib.Function(fname, line))

    # Find all Macro definitions
    for match in RE_DEF.finditer(txt):
        line = txt.count('\n', 0, match.start(1))
        rtags.AddElement('macro', taglib.Macro(match.group(1), line))

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
