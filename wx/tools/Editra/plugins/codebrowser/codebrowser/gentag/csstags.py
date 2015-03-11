###############################################################################
# Name: csstags.py                                                            #
# Purpose: Generate Tags for Cascading Style Sheets                           #
# Author: Cody Precord <cprecord@editra.org>                                  #
# Copyright: (c) 2008 Cody Precord <staff@editra.org>                         #
# License: wxWindows License                                                  #
###############################################################################

"""
FILE: csstags.py
AUTHOR: Cody Precord
LANGUAGE: Python
SUMMARY:
  Generate a DocStruct object that captures the structure of a Cascading Style
Sheet. Currently supports parsing of global identities and classes.

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
    """Create a DocStruct object that represents a Cascading Style Sheets
    @param buff: a file like buffer object (StringIO)
    @todo: add support for parsing selectors and grouping classes and
           identities of each selector in a subscope.

    """
    rtags = taglib.DocStruct()

    # Setup document structure
    # Use variables node for global identities
    rtags.SetElementDescription('variable', "Identities")
    rtags.SetElementDescription('tag_red', "Elements")
    # Use classes for global classes
    # Uses DocStruct builtin

    c_tag = None      # Currently found tag
    incomment = False # Inside a comment
    indef = False     # Inside a style definition {}

    for lnum, line in enumerate(buff):
        line = line.strip()
        llen = len(line)
        idx = 0
        while idx < len(line):
            idx = parselib.SkipWhitespace(line, idx)

            # Check for comments
            if llen > idx+1 and line[idx] == u'/' and line[idx+1] == u'*':
                idx += 2
                incomment = True
            elif llen > idx+1 and line[idx] == u'*' and line[idx+1] == u'/':
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
            elif not indef and line[idx] in (u'.', u'#'):
                # Classes and ID's
                if idx == 0 or line[idx-1].isspace():
                    names = line[idx:].split()
                    if len(names):
                        name = names[0]
                    else:
                        name = None
                    if name is not None:
                        if line[idx] == u'.':
                            # See if we already have found previous
                            # defs using this class identifier
                            cobj = rtags.GetElement('class', name)
                            if cobj is None:
                                cobj = taglib.Class(name, lnum)
                                rtags.AddClass(cobj)

                            # Update the index
                            idx += len(name)
                            # Grab all other defs that may be children of
                            # the current one.
                            idx = CaptureClassElements(cobj, line, idx)
                        else:
                            # Stand alone ID
                            rtags.AddVariable(taglib.Variable(name, lnum))
                            idx += len(name)
                        continue
                # TODO: smarter skip ahead to speed up parse
                idx += 1
            elif not indef and not line[idx].isspace():
                # Possible element
                nparen = line[idx:].find(u'{') + idx
                token = line[idx:nparen]
                if token:
                    idx += len(token)
                    if not token.startswith(u"@"):
                        obj = CSSTag(token.strip(), lnum)
                        rtags.AddElement('tag_red', obj)
                else:
                    idx += 1
            else:
                # TODO: smarter skip ahead to speed up parse
                idx += 1

    return rtags

#-----------------------------------------------------------------------------#
# Utilities

class CSSTag(taglib.Code):
    """CSSTag object for representing css elements"""
    def __init__(self, name, line, scope=None):
        taglib.Code.__init__(self, name, line, "tag_red", scope)

def CaptureClassElements(scope, line, idx):
    """Get recursively capture all the elements defined on the line from
    the index.
    @param scope: Scope object to append element to
    @param line: string of text to parse
    @param idx: current index in line
    @return: new index

    """
    idx = parselib.SkipWhitespace(line, idx)
    dend = line[idx:].find(u"{") + idx
    if idx >= len(line) or idx == dend:
        return idx

    segments = line[idx:dend].strip().split()
    if len(segments):
        token = segments[0]
        idx += len(token)
        if token.startswith(u'.'):
            # Descendant class
            nextscope = taglib.Class(token, scope.GetLine())
            scope.AddElement('class', nextscope)
            # Recurse to look for more children
            idx = CaptureClassElements(nextscope, line, idx)
        elif token.startswith(u'#'):
            # An ID
            obj = taglib.Variable(token, scope.GetLine())
            scope.AddElement('variable', obj)
        else:
            # Element p, div, etc..
            obj = CSSTag(token, scope.GetLine())
            scope.AddElement('tag_red', obj)
    return idx

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
