###############################################################################
# Name: xmltags.py
# Purpose: Generate Tags for XML documents
# Author: Rudi Pettazzi <rudi.pettazzi@gmail.com>
# Copyright: (c) 2008 Cody Precord <staff@editra.org>
# License: wxWindows License
###############################################################################

"""
FILE: xmltags.py
AUTHOR: Rudi Pettazzi
LANGUAGE: Python
SUMMARY:  Generate a DocStruct object that captures the structure of
an XML document.

"""

__author__ = "Rudi Pettazzi <rudi.pettazzi@gmail.com>"
__svnid__ = "$Id$"
__revision__ = "$Revision$"

#--------------------------------------------------------------------------#
# Dependencies
import taglib
import parselib
from pygments import lex
from pygments.token import Token
from pygments.lexers import get_lexer_by_name

#-----------------------------------------------------------------------------#
# Utilities
class XmlTagsBuilder(object):

    TAG_ID = 'tag_blue'     # DocStruct tag id

    def __init__(self):
        self.stack = []

    def BuildTags(self, buff, lexer):
        """
        @param buff: code buffer
        @param lexer: xml lexer
        @return: taglib.DocStruct instance for the given buff
        """
        rtags = taglib.DocStruct()
        rtags.SetElementDescription(self.TAG_ID, '/')
        line_count = 0
        current_line = []
        code_lines = []

        # Parse the file into tokens and values
        for ttype, value in lex(buff.read(), lexer):
            if '\n' in value:
                if len(current_line) > 0:
                    code_lines.append((line_count, current_line))
                current_line = []
                line_count += value.count('\n')
                continue
            if ttype == Token.Name.Tag and len(value) > 1:
                current_line.append((ttype, value))
        docroot = self.Parse(code_lines)
        if docroot != None:
            rtags.AddElement(self.TAG_ID, docroot)
        return rtags

    def Parse(self, code_lines):
        """Create a tree of xmltags.Node objects to represent the dom of an XML document.

        The algorithm uses a stack to build the correct hierarchy and a few naif heuristics
        aimed to fit somehow every node into a DOM (that is, the tree view always shows every
        node, even if it is a start tag with no end tag or viceversa).

        When a end tag is processed, the start tag should be on the top of the stack. If not,
        the document DOM is invalid and the tree is adjusted trying 2 strategies:
        1) peek deeply into the stack (but not deeper than a constant otherwise some corner cases on
           big documents could bring performance penalties): if the start tag is found, the node is created
           and everything in between is popped-off and re-parented with the immediate preceding node.
           This should fixes the case when a cascade of unclosed tags "hides" a candidate start tag:

           example:
           @verbatim <a><b><c><d></a> is transformed to <a><b><c><d></d></c></b></a>. @endverbatim

        2) otherwise save the node treating as it were an empty-element tag and attaching it to its parent.
           If the stack is empty the node is pushed on the stack and treated as a start tag (the root).

           example: 
           @verbatim <a></b><c></c></a> is transformed to <a><b></b><c></c></a>. @endverbatim
           example: 
           @verbatim </a></b></c> is transformed to <a><b></b><c></c></a> @endverbatim

        Start tag with no end tag and unrooted DOMs are handled by emptying the stack before leaving
        the procedure (3rd strategy).

           example: 
           @verbatim <a><b><c> is transformed to <a><b><c></c></b></a> @endverbatim

        @param code_lines: a list of tuples (line_num, [(token type, token value), ... ])
        @return: the taglib.Scope root of the nodes defined into an XML document

        """
        node = None
        for num, line in code_lines:
            for ttype, value in line:
                # start tag
                if value[:2] not in ['</', '/>']:
                    node = NodeTag(value[1:], num)
                    self.stack.append(node)
                # end tag
                else:
                    if value != '/>':
                        value = value[2:-1].strip()
                    if self._PeekNode(value):
                        node = self.stack.pop()
                        self._SaveNode(node)
                    elif self._NodeExists(value, 70): # 1st strategy
                        while len(self.stack) > 0:
                            node = self.stack.pop()
                            self._SaveNode(node)
                            if node.name == value:
                                break
                    else: # 2nd strategy
                        node = NodeTag(value, num)
                        self._SaveNode(node)

        # 3rd strategy
        while len(self.stack) > 0:
            node = self.stack.pop()
            self._Connect(node)

        return node

    def _Connect(self, node):
        """ Connect the node to its parent, if any.
        @param node: the node object
        @return True if the node has been actually connected, that is,
        if there was a parent on the stack
        """
        if len(self.stack) > 0:
            last = self.stack[-1]
            if last is not node:
                last.AddElement(self.TAG_ID, node)
            return True
        return False

    def _SaveNode(self, node):
        """ Save the node connecting it to its parent or pushing it on the stack
        if it is the root.
        @param node: the node object
        """
        if not self._Connect(node):
            self.stack.append(node)

    def _PeekNode(self, value, depth=1):
        """Return true if the given node value matches the node (opening tag)
        found in the stack at the given depth. Note that a value of '/>' always matches.
        @param value: closing node value
        @keyword depth: stack depth
        @return True if value closes the tag found in the stack at the given depth
        """
        if depth > len(self.stack):
            return False
        peek = self.stack[-depth].name
        return value == '/>' or value == peek

    def _NodeExists(self, value, maxdepth):
        """Return true if the given node value matches one of the nodes (opening tag)
        saved on the stack.
        @param value: closing node value
        @param maxdepth: maximum depth to peek into the stack
        @return True if the opening node is found
        """
        for i, node in enumerate(self.stack):
            if i == maxdepth:
                break
            elif node.name == value:
                return True
        return False

class NodeTag(taglib.Scope):
    """Node Code Object"""
    def __init__(self, name, line, scope=None):
        taglib.Scope.__init__(self, name, line, 'tag_blue', scope)

    def GetElements(self):
        """Return the one-item dictionary of nodes (unsorted) contained in this Node.
        @return: list of dict
        """
        sorder = [ key for key, val in self.prio.items() ]
        rlist = []
        for key in sorder:
            if key in self.elements:
                rlist.append({key:self.elements[key]})
        return rlist

def GenerateTags(buff):
    """Create a DocStruct object that represents an XML document
    @param buff: a file like buffer object (StringIO)
    """
    b = XmlTagsBuilder()
    rtags = b.BuildTags(buff, get_lexer_by_name('xml', stripall=True))
    return rtags

def _PrintTree(node, indent=''):
    """Debug helper: recursively print the given tree"""
    indent = indent + '--'
    for elt in node.GetElements():
        for elt in elt[XmlTagsBuilder.TAG_ID]:
            print indent + elt.name
            _PrintTree(elt, indent)

#-----------------------------------------------------------------------------#
# Test
if __name__ == '__main__':
    import sys
    import StringIO
    import os, os.path, pytags
    fhandle = open(sys.argv[1])
    txt = fhandle.read()
    fhandle.close()
    tags = GenerateTags(StringIO.StringIO(txt))
    _PrintTree(tags)
