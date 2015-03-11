###############################################################################
# Name: feritetags.py                                                         #
# Purpose: Generate Tags for Ferite Documents                                 #
# Author: Cody Precord <cprecord@editra.org>                                  #
# Copyright: (c) 2008 Cody Precord <staff@editra.org>                         #
# License: wxWindows License                                                  #
###############################################################################

"""
FILE: haxetags.py
AUTHOR: Cody Precord
LANGUAGE: Python
SUMMARY:
  Generate a DocStruct object that captures the structure of a Ferite document.
Supports parsing of Namespaces, Classes, Protocols, Functions.

@todo: Currently Parsing of Namespaces within Namespaces is not supported

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
    """Create a DocStruct object that represents a Ferite document
    @param buff: a file like buffer object (StringIO)

    """
    rtags = taglib.DocStruct()

    # Setup document structure
    rtags.SetElementDescription('namespace', "Namespaces")
    rtags.SetElementDescription('class', "Class Definitions")
    rtags.SetElementDescription('protocol', "Protocols")
    rtags.SetElementDescription('function', "Function Definitions")
    rtags.SetElementPriority('namespace', 4)
    rtags.SetElementPriority('class', 3)
    rtags.SetElementPriority('protocol', 2)
    rtags.SetElementPriority('function', 1)

    # Variables for tracking parse state
    incomment = False    # Inside a comment
    innamespace = False  # Inside a namespace
    inclass = False      # Inside a class defintion
    inprotocol = False   # Inside a protocol
    infundef = False     # Inside a function definition
    lastnspace = None    # Last Namespace
    lastclass = None     # Last Class
    lastprotocol = None  # Last Protocol
    lastfun = None       # last Function
    openb = 0            # Keep track of open brackets for scope resolution

    def InSubScope():
        return innamespace or inclass or inprotocol or infundef

    # Parse the contents of the buffer
    for lnum, line in enumerate(buff):
        line = line.strip()
        llen = len(line)
        idx = 0
        while idx < len(line):
            # Skip Whitespace
            idx = parselib.SkipWhitespace(line, idx)

            # Check for comments
            if line[idx:].startswith(u'/*'):
                idx += 2
                incomment = True
            elif line[idx:].startswith(u'//'):
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
                # Namespace/Class/Protocol names must be followed by a {
                if not InSubScope() and lastnspace is not None:
                    innamespace = True
                    rtags.AddElement('namespace', lastnspace)
                elif not inclass and lastclass is not None:
                    inclass = True
                    if lastnspace is not None:
                        # Class is in a namespace
                        lastnspace.AddElement('class', lastclass)
                    else:
                        # Class is at the global scope
                        rtags.AddClass(lastclass)
                elif not InSubScope() and lastprotocol is not None:
                    inprotocol = True
                    rtags.AddElement('protocol', lastprotocol)
                elif lastfun is not None:
                    infundef = True
                    lastfun = None
                else:
                    pass
            elif line[idx] == u'}':
                idx += 1
                openb -= 1
                # Check if the scope needs to change
                if innamespace and openb == 0:
                    innamespace = False
                    lastnspace = None
                elif innamespace and inclass and openb == 1:
                    inclass = False
                    lastclass = None
                elif (innamespace and inclass and infundef and openb == 2) or \
                     (innamespace and infundef and openb == 1):
                    infundef = False
                    lastfun = None
                elif inclass and openb == 0:
                    inclass = False
                    lastclass = None
                elif inclass and infundef and openb == 1:
                    infundef = False
                    lastfun = None
                elif inprotocol and openb == 0:
                    inprotocol = False
                    lastprotocol = None
                elif inprotocol and infundef and openb == 1:
                    infundef = False
                    lastfun = None
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
            elif not infundef and not inclass and \
                 parselib.IsToken(line, idx, 'namespace'):
                idx = parselib.SkipWhitespace(line, idx + 9)
                name = GetElementName(line[idx:])
                if name is not None:
                    idx += len(name)
                    lastnspace = taglib.Namespace(name, lnum)
            elif parselib.IsToken(line, idx, u'protocol'):
                idx = parselib.SkipWhitespace(line, idx + 8)
                name = parselib.GetFirstIdentifier(line[idx:])
                if name is not None:
                    idx += len(name)
                    lastprotocol = Protocol(name, lnum)
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

                    tfun = taglib.Function(name, lnum)
                    if innamespace and not inclass and lastnspace:
                        lastnspace.AddElement('function', tfun)
                    elif inclass and lastclass is not None:
                        lastclass.AddMethod(taglib.Method(name, lnum, lastclass.GetName()))
                    elif inprotocol and lastprotocol is not None:
                        lastprotocol.AddElement('function', tfun)
                    else:
                        rtags.AddFunction(tfun)
            else:
                idx += 1

    return rtags

#-----------------------------------------------------------------------------#
class Protocol(taglib.Scope):
    """Protocol Code Object"""
    def __init__(self, name, line, scope=None):
        taglib.Scope.__init__(self, name, line, "protocol", scope)

def GetElementName(line):
    """Get the first element name on the given line, ignoring whitespace and
    language keywords.
    @param line: string
    @return: string or None

    """
    for part in line.split():
        name = parselib.GetFirstIdentifier(part)
        if name is not None and name not in FERITE_KW:
            return name
        else:
            continue
    return None

FERITE_KW = ("false null self super true abstract alias and arguments "
             "attribute_missing break case class closure conformsToProtocol "
             "constructor continue default deliver destructor diliver "
             "directive do else extends eval final fix for function global "
             "handle if iferr implements include instanceof isa "
             "method_missing modifies monitor namespace new or private "
             "protected protocol public raise recipient rename return "
             "static switch uses using while")

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
