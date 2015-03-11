###############################################################################
# Name: rubytags.py                                                           #
# Purpose: Generate Ruby Tags                                                 #
# Author: Cody Precord <cprecord@editra.org>                                  #
# Copyright: (c) 2008 Cody Precord <staff@editra.org>                         #
# License: wxWindows License                                                  #
###############################################################################

"""
FILE: rubytags.py
AUTHOR: Cody Precord
LANGUAGE: Python
SUMMARY:
  Generate a DocStruct object that captures the structure of a ruby document.
It supports parsing for global and class variables, class, method, and function
definitions.

@todo: improve scoping, currently its just a best effort check
@todo: needs performance improvements, currently it can get a little slow

"""

__author__ = "Cody Precord <cprecord@editra.org>"
__svnid__ = "$Id$"
__revision__ = "$Revision$"

#--------------------------------------------------------------------------#
# Imports
import taglib
import parselib

from pygments import highlight
from pygments.token import Token
from pygments.lexers import get_lexer_by_name
from pygments.formatter import Formatter

#--------------------------------------------------------------------------#

class RbFormatter(Formatter):
    """Ruby code formatter"""
    def format(self, tokensource, outfile):
        """Format the tokens from the document"""
        self.rtags = taglib.DocStruct()
        self.rtags.SetElementDescription('function', "Function Definitions")
        self.rtags.SetElementDescription('class', "Class Definitions")
        self.rtags.SetElementDescription('module', "Modules")
        self.SetSortOrder(self.rtags)

        line_count = 0
        current_line = []
        code_lines = []

        # Parse the file into lines of tokens and values
        for ttype, value in tokensource:
            if '\n' in value:
                if len(current_line):
                    code_lines.append((line_count, current_line))
                current_line = []
                line_count += value.count('\n')
                continue

            # Skip comments, strings, and space tokens
            if ttype in (Token.Comment.Single,
                         Token.Literal.String.Double,
                         Token.Literal.String.Heredoc,
                         Token.Literal.String.Other):
                continue
            elif value.isspace():
                continue
            else:
                current_line.append((ttype, value))

        self.FindElements(code_lines)

    def FindElements(self, lines):
        """Find the code elements in the list of formatted lines
        @param lines: list of code items

        """
        # Parse state varibles
        containers = list()
        endcount = 0

        # Parse each line for elements
        for lnum, line in lines:
            try:
                for token, value in line:
                    if token == Token.Keyword:
                        if value == "end":
                            endcount = max(endcount - 1, 0)
                            ccount = len(containers)
                            dcount = endcount - ccount
                            if ccount == 1:
                                if not endcount:
                                    containers.pop()
                            elif ccount > 1 and dcount == ccount or dcount < 0:
                                containers.pop()
                        elif value in "begin case do for if unless until while":
                            # These items require an end clause
                            endcount = endcount + 1
                        elif value == "def":
                            nspace, fname = GetRubyFunction(line)
                            if endcount and len(containers):
                                meth = taglib.Method(fname, lnum)
                                if nspace is not None:
                                    self.InsertMethod(nspace, meth)
                                else:
                                    containers[-1].AddElement('method', meth)
                            else:
                                self.rtags.AddFunction(taglib.Function(fname, lnum))
                            endcount = endcount + 1
                        elif value == "class":
                            cname = parselib.GetTokenValue(line, Token.Name.Class)
                            cobj = taglib.Class(cname, lnum)
                            self.SetSortOrder(cobj)
                            if endcount and len(containers):
                                containers[-1].AddElement('class', cobj)
                            else:
                                self.rtags.AddClass(cobj)
                            containers.append(cobj)
                            endcount = endcount + 1
                        elif value == "module":
                            mname = parselib.GetTokenValue(line, Token.Name.Namespace)
                            mobj = taglib.Module(mname, lnum)
                            self.SetSortOrder(mobj)
                            if endcount and len(containers):
                                containers[-1].AddElement('module', mobj)
                            else:
                                self.rtags.AddElement('module', mobj)
                            containers.append(mobj)
                            endcount = endcount + 1
                        elif value == "raise":
                            break
                        continue
                    else:
                        continue
            except parselib.TokenNotFound, msg:
                pass

    def GetTags(self):
        return self.rtags

    def InsertMethod(self, nspace, meth):
        """Insert a method into the given namespace if it exists
        else insert it into the top level of the DocStruct.
        @param nspace: string
        @param meth: Method object

        """
        for cobj in self.rtags.GetScopes():
            if cobj.GetName() == nspace:
                cobj.AddElement('method', meth)
                break

    def SetSortOrder(self, cobj):
        """Set the element sort order of the code object
        @param cobj: Scope object

        """
        cobj.SetElementPriority('class', 4)
        cobj.SetElementPriority('module', 3)
        cobj.SetElementPriority('method', 2)
        cobj.SetElementPriority('function', 1)

#-----------------------------------------------------------------------------#
# Main Interface Function

def GenerateTags(buff):
    """GenTag interface method
    @return: taglib.DocStruct

    """
    formatter = RbFormatter()
    highlight(buff.read(), get_lexer_by_name("ruby"), formatter)
    return formatter.GetTags()

#-----------------------------------------------------------------------------#
# Utility Functions

def GetRubyFunction(line):
    """Get the ruby function name and namespace it belongs in
    if applicable.
    @param line: line of formatted tokens
    @return: tuple (nspace, fname)

    """
    fname = u''
    nspace = None
    for token, value in line:
        if token in (Token.Name.Function, Token.Name.Class) and nspace is None:
            fname = value
        elif token == Token.Operator and value in (u"::", u"."):
            nspace = fname
        elif token in (Token.Name, Token.Name.Function) and nspace is not None:
            fname = value
            break
    return (nspace, fname)

#-----------------------------------------------------------------------------#
# Test
if __name__ == '__main__':
    import sys
    import StringIO
    fhandle = open(sys.argv[1])
    txt = fhandle.read()
    fhandle.close()
    tags = GenerateTags(StringIO.StringIO(txt))
    print "\n\nVARIABLES:"
    for var in tags.GetVariables():
        print "%s [%d]" % (var.GetName(), var.GetLine())
    print "\n\nFUNCTIONS:"
    for fun in tags.GetFunctions():
        print "%s [%d]" % (fun.GetName(), fun.GetLine())
    print ""
    print "CLASSES:"
    for c in tags.GetClasses():
        print "* %s [%d]" % (c.GetName(), c.GetLine())


# get var and methods does not exist ( any more ?? )
#        for var in c.GetVariables():
#            print "VAR: ", var.GetName()
#        for meth in c.GetMethods():
#            print "    %s [%d]" % (meth.GetName(), meth.GetLine())
    print "END"
