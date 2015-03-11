###############################################################################
# Name: perltags.py                                                           #
# Purpose: Generate Tags for Perl Scripts                                     #
# Author: Cody Precord <cprecord@editra.org>                                  #
# Copyright: (c) 2008 Cody Precord <staff@editra.org>                         #
# License: wxWindows License                                                  #
###############################################################################

"""
FILE: perltags.py
AUTHOR: Cody Precord
LANGUAGE: Python
SUMMARY:
  Generate a DocStruct object that captures the structure of a Perl Script.
Currently supports parsing of subroutines and their declarations, as well as
package declarations.

Subroutine Declarations can be in a number of forms
sub foo;
sub foo :attr;
sub foo (bar);
sub foo (bar) :attr;

"""

__author__ = "Cody Precord <cprecord@editra.org>"
__svnid__ = "$Id$"
__revision__ = "$Revision$"

#--------------------------------------------------------------------------#
# Dependancies
import taglib
import parselib

from pygments import highlight
from pygments.token import Token
from pygments.lexers import get_lexer_by_name
from pygments.formatter import Formatter

#--------------------------------------------------------------------------#

class PerlFormatter(Formatter):
    
    def format(self, tokensource, outfile):
        """Format the input text
        @note: overrides Formatter.format

        """
        self.rtags = taglib.DocStruct()
        self.rtags.SetElementDescription('package', "Packages")
        self.rtags.SetElementPriority('package', 3)
        self.rtags.SetElementDescription('subdec', "Subroutine Declarations")
        self.rtags.SetElementPriority('subdec', 2)
        self.rtags.SetElementDescription('subroutine', "Subroutines")
        self.rtags.SetElementPriority('subroutine', 1)

        line_count = 0
        current_line = []
        code_lines = []

        # Parse the file into tokens and values
        for ttype, value in tokensource:
            if '\n' in value:
                code_lines.append((line_count, current_line))
                current_line = []
                line_count += value.count('\n')
                continue
            current_line.append((ttype, value))

        self.parseTags(code_lines)

    def parseTags(self, code_lines):
        """Parse all the tokens found in the lines of code"""
        container_list = []
        vset = set()

        for num, line in code_lines:
            try:
                # Subroutine
                if parselib.HasToken(line, Token.Keyword, "sub"):
                    fname = parselib.GetTokenValue(line, Token.Name.Function)
                    self.rtags.AddElement('subroutine',
                                          taglib.Function(fname, num, "subroutine"))

                # Packages
                if parselib.HasToken(line, Token.Name.Builtin, "package"):
                    name = None
                    next = True
                    for token, value in line:
                        if not next:
                            name += value
                            break

                        if token == Token.Name.Namespace:
                            name = value
                            next = False

                    if name is not None:
                        self.rtags.AddElement('package', taglib.Package(name, num))

            except parselib.TokenNotFound:
                pass

    def getTags(self):
        return self.rtags

#--------------------------------------------------------------------------#

def GenerateTags(buff):
    """Create a DocStruct object that represents a Perl Script
    @param buff: a file like buffer object (StringIO)

    """
    formatter = PerlFormatter()
    highlight(buff.read(), get_lexer_by_name("perl"), formatter)
    return formatter.getTags()

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
