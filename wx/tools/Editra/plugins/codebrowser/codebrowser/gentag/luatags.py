###############################################################################
# Name: luatags.py                                                            #
# Purpose: Generate Tags for Lua Scripts                                      #
# Author: Cody Precord <cprecord@editra.org>                                  #
# Copyright: (c) 2008 Cody Precord <staff@editra.org>                         #
# License: wxWindows License                                                  #
###############################################################################

"""
FILE: luatags.py
AUTHOR: Cody Precord
LANGUAGE: Python
SUMMARY:
  Generate a DocStruct object that captures the structure of a Lua Script

"""

__author__ = "Cody Precord <cprecord@editra.org>"
__svnid__ = "$Id$"
__revision__ = "$Revision$"

#--------------------------------------------------------------------------#
# Dependancies
import taglib

#--------------------------------------------------------------------------#

def GenerateTags(buff):
    """Create a DocStruct object that represents a Lua Script
    @param buff: a file like buffer object (StringIO)
    @todo: generate tags for lua tables?

    """
    rtags = taglib.DocStruct()
    rtags.SetElementDescription('function', "Function Definitions")

    for lnum, line in enumerate(buff):
        line = line.strip()

        # Skip comment and empty lines
        if line.startswith(u"--") or not line:
            continue

        # Check Regular Function Defs
        if u'function' in line:
            name = None
            if u'=' in line and line.index(u'=') < line.index(u'function'):
                name = line[:line.index(u'=')].strip()
            elif u'(' in line:
                idx = line.find(u'function')
                idx2 = line.find(u'(')
                if idx < idx2:
                    name = line[idx+9:idx2].strip()
            else:
                continue

            if name is not None:
                rtags.AddFunction(taglib.Function(name, lnum))

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
