###############################################################################
# Name: xtxttags.py                                                           #
# Purpose: Generate Tags for XText                                            #
# Author: Igor Dejanovic <igor.dejanovic@gmail.com>                           #
# Copyright: (c) 2009 Igor Dejanovic <igor.dejanovic@gmail.com>               #
# License: wxWindows License                                                  #
###############################################################################

"""
FILE: xtxttags.py
AUTHOR: Igor Dejanovic
LANGUAGE: Python
SUMMARY:
  Generate a DocStruct object that captures the structure of a XText.
Currently supports parsing for ParserRules, Features, Enums, Literals and rule CrossRefs.

"""

__author__ = "Igor Dejanovic <igor.dejanovic@gmail.com>"
__svnid__ = "$Id$"
__revision__ = "$Revision$"

#--------------------------------------------------------------------------#
# Dependencies
import taglib
#import parselib
from syntax.xtext import lexer
from pygments.token import Keyword, Name, Token


#--------------------------------------------------------------------------#
# Document objects
class ParserRule(taglib.Class):
    """ParserRule Object"""
    def __init__(self, name, line, scope=None):
        taglib.Class.__init__(self, name, line, scope)
        self.SetType("parserrule")

class Feature(taglib.Variable):
    """Feature Object"""
    def __init__(self, name, line, scope=None):
        taglib.Variable.__init__(self, name, line, scope)
        self.SetType("feature")

class Terminal(taglib.Scope):
    """Terminal Object"""
    def __init__(self, name, line, scope=None):
        taglib.Scope.__init__(self, name, line, "terminal", scope)

class Enum(taglib.Scope):
    """Enum Object"""
    def __init__(self, name, line, scope=None):
        taglib.Scope.__init__(self, name, line, "enum", scope)

class Literal(taglib.Code):
    """Literal Object"""
    def __init__(self, name, line, scope=None):
        taglib.Code.__init__(self, name, line, "literal", scope)


def GenerateTags(buff):
    """Create a DocStruct object that represents a XText file
    @param buff: a file like buffer object (StringIO)

    """
    rtags = taglib.DocStruct()
    rtags.SetElementDescription('parserrule', "Parser Rule Definitions")
    rtags.SetElementDescription('terminal', "Terminal Definitions")
    rtags.SetElementPriority('terminal', 2)
    rtags.SetElementDescription('enum', "Enum Definitions")
    rtags.SetElementPriority('enum', 1)
    rtags.SetElementDescription('literal', "Literal")
    
    scope_metatype = None
    # scope_elements list for preventing duplicates
    scope_elements = []
    scope = None
    feature = None
    line = 0
    
    for index, token, txt in lexer.get_tokens_unprocessed(buff.read()):
#        print index, token, txt
        if token is Token.EndOfLine:
            line += 1
            continue
        elif token is Keyword and txt in ['enum', 'terminal']:
            scope = txt
            continue
        
        if token is Name.CrossRef:
            if feature and not '->' in feature.GetName():
                feature.SetName("%s->%s" % (feature.GetName(), txt))

        if token is Name.AbstractRule:
            if scope is None:
                scope_metatype = ParserRule(txt, line)
                rtags.AddElement('parserrule', scope_metatype)
            elif scope == 'enum':
                scope_metatype = Enum(txt, line)
                rtags.AddElement('enum', scope_metatype)
            elif scope == 'terminal':
                scope_metatype = Terminal(txt, line)
                rtags.AddElement('terminal', scope_metatype)

            scope = None
            feature = None
            del scope_elements[:]
            
        elif token is Name.Feature:
            if scope is None or scope == 'terminal':
                if not txt in scope_elements:
                    feature = Feature(txt, line)
                    scope_metatype.AddElement('feature', feature)
                    scope_elements.append(txt)
            elif scope == 'enum':
                scope_metatype.AddElement('literal', Literal(txt, line))

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

