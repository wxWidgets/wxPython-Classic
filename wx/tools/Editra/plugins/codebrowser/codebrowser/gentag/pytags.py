###############################################################################
# Name: pytags.py                                                             #
# Purpose: Generate Python Tags                                               #
# Author: Cody Precord <cprecord@editra.org>                                  #
# Copyright: (c) 2008 Cody Precord <staff@editra.org>                         #
# License: wxWindows License                                                  #
###############################################################################

"""
FILE: pytags.py
AUTHOR: Cody Precord
AUTHOR: Luis Cortes
LANGUAGE: Python
SUMMARY:
  Generate a DocStruct object that captures the structure of a python document.
It supports parsing for global and class variables, class, method, and function
definitions.

@todo: add back support for class variables
@todo: document functions

"""

__author__ = "Cody Precord <cprecord@editra.org>"
__svnid__ = "$Id$"
__revision__ = "$Revision$"

#--------------------------------------------------------------------------#
# Dependencies
import taglib
import parselib
from pygments import highlight
from pygments.token import Token
from pygments.lexers import get_lexer_by_name
from pygments.formatter import Formatter

#--------------------------------------------------------------------------#

class PyFormatter(Formatter):

    def format(self, tokensource, outfile):
        self.rtags = taglib.DocStruct()
        self.rtags.SetElementDescription('function', "Function Definitions")
        self.rtags.SetElementDescription('class', "Class Definitions")
        self._levels = [0]
        self._toplevel = True

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

        self.getCFV(code_lines)

    def _getLevel(self, line):
        try:
            t, v = line[0]
            if t == Token.Text:
                return len(v)
        except:
            pass
        return 0

    def pushPopScope(self, level):
        """Push a scope onto the stack. If less than previous scope
        it will pop levels until it finds a matching indent level.

        """
        nlevels = list()
        for lvl in self._levels:
            if lvl < level:
                nlevels.append(lvl)
            else:
                break
        nlevels.append(level)
        self._levels = nlevels

    def insertClass(self, line, num, container_list):
        """Insert a class into the container"""
        cname = parselib.GetTokenValue(line, Token.Name.Class)
        clevel = self._getLevel(line)

        ctag = None
        # Top Level Class
        if clevel == 0:
            ctag = taglib.Class(cname, num)
            self.rtags.AddClass(ctag)

        # Somewhere else
        else:
            for l, c, ob in reversed(container_list):
                if l < clevel:
                    ctag = taglib.Class(cname, num, c)
                    ob.AddElement('class', ctag)
                    break

        if ctag:
            container_list.append((clevel, cname, ctag))

    def insertFunction(self, line, num, container_list):
        fname = parselib.GetTokenValue(line, Token.Name.Function)
        flevel = self._getLevel(line)

        ftag = None
        # top level function
        if flevel == 0:
            ftag = taglib.Function(fname, num)
            self.rtags.AddFunction(ftag)

        # Somewhere else
        else:
            for l, c, ob in reversed(container_list):
                if l < flevel:
                    if isinstance(ob, taglib.Class):
                        ftag = taglib.Method(fname, num, c)
                        ob.AddMethod(ftag)
                    else:
                        ftag = taglib.Function(fname, num, c)
                        ob.AddElement('function', ftag)
                    break

        if ftag:
            container_list.append((flevel, fname, ftag))

    def getCFV(self, code_lines):

        container_list = []
        vset = set()

        for num, line in code_lines:
            try:
                if len(line):
                    ltxt = u"".join([l[1].strip() for l in line])
                    if len(ltxt) and not ltxt.startswith(u"#"):
                        if parselib.BeginsWithAnyOf(line, Token.Keyword,
                                                    (u"def", u"class", u"if", u"else")):
                            self.pushPopScope(self._getLevel(line))
                            if len(self._levels) == 1:
                                container_list = [(0, u"", self.rtags)]

                # FUNCTION
                #
                if parselib.HasToken(line, Token.Keyword, "def"):
                    self.insertFunction(line, num, container_list)

                # CLASS
                #
                elif parselib.HasToken(line, Token.Keyword, "class"):
                    self.insertClass(line, num, container_list)

                # Global Variable Only
                #
                elif parselib.HasToken(line, Token.Operator, "="):
                    vname = parselib.GetTokenValue(line, Token.Name);
                    flevel = self._getLevel(line)

                    if flevel == 0:
                        if not vname in vset:
                            self.rtags.AddVariable(taglib.Variable(vname, num))
                            vset.add(vname)

            except parselib.TokenNotFound:
                pass
        return self.rtags

    def getTags(self):
        return self.rtags

#-----------------------------------------------------------------------------#

def GenerateTags(buff):
    """GenTag interface method
    @return: taglib.DocStruct

    """
    formatter = PyFormatter()
    highlight(buff.read(), get_lexer_by_name("python"), formatter)
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
