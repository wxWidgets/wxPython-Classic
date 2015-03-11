###############################################################################
# Name: esstags.py                                                            #
# Purpose: Generate Tags for Editra Style Sheets                              #
# Author: Cody Precord <cprecord@editra.org>                                  #
# Copyright: (c) 2008 Cody Precord <staff@editra.org>                         #
# License: wxWindows License                                                  #
###############################################################################

"""
FILE: esstags.py
AUTHOR: Cody Precord
LANGUAGE: Python
SUMMARY:
  Generate a DocStruct object that captures the structure of Editra Style
Sheets. 

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
    """Create a DocStruct object that represents an Editra Style Sheet
    @param buff: a file like buffer object (StringIO)

    """
    rtags = taglib.DocStruct()
    rtags.SetElementDescription('styletag', "Style Tags")

    c_element = None  # Currently found document element
    incomment = False # Inside a comment
    indef = False     # Inside a style definition {}

    for lnum, line in enumerate(buff):
        line = line.strip()
        llen = len(line)
        idx = 0
        while idx < len(line):
        
            # Skip Whitespace
            idx = parselib.SkipWhitespace(line, idx)

            # Check if valid item to add to document
            if c_element is not None and line[idx] == u'{':
                rtags.AddElement('styletag', c_element)
                c_element = None

            # Check for coments
            if not incomment and line[idx:].startswith('/*'):
                idx += 2
                incomment = True
            elif incomment and line[idx:].startswith('*/'):
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
                indef = True
            elif indef and line[idx] == u'}':
                idx += 1
                indef = False
            elif not indef and line[idx].isalpha():
                # Found start of tag
                name = parselib.GetFirstIdentifier(line[idx:])
                if name is not None:
                    # Make a tag but don't add it to the DocStruct till we
                    # find if a { is the next non space character to follow
                    c_element = StyleTag(name, lnum)
                    idx += len(name)
                else:
                    # This should never happen but if it does there must
                    # be something wrong with the document or the parse has
                    # gone afowl.
                    idx += 1
            else:
                idx += 1

    return rtags

#-----------------------------------------------------------------------------#
# Utilities
class StyleTag(taglib.Code):
    """Style Tag Code Object"""
    def __init__(self, name, line, scope=None):
        taglib.Code.__init__(self, name, line, "styletag", scope)

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
