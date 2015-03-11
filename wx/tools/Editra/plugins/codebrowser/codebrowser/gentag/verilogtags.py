###############################################################################
# Name: verilogtags.py                                                        #
# Purpose: Generate Tags for Verilog and System Verilog Source Files          #
# Author: Cody Precord <cprecord@editra.org>                                  #
# Copyright: (c) 2008 Cody Precord <staff@editra.org>                         #
# License: wxWindows License                                                  #
###############################################################################

"""
FILE: verilogtags.py
AUTHOR: Cody Precord
LANGUAGE: Python
SUMMARY:
  Generate a DocStruct object that captures the structure of Verilog and System
Verilog files.

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
    """Create a DocStruct object that represents a Verilog document
    @param buff: a file like buffer object (StringIO)
    @todo: add support for parsing module definitions / class variables

    """
    rtags = taglib.DocStruct()
    rtags.SetElementDescription('class', "Class Definitions")
    rtags.SetElementDescription('task', "Task Definitions")
    rtags.SetElementDescription('function', "Function Definitions")
    rtags.SetElementPriority('class', 3)
    rtags.SetElementPriority('task', 2)
    rtags.SetElementPriority('function', 1)

    # Variables to track parse state
    inclass = False      # Inside a class defintion
    incomment = False    # Inside a comment
    intask = False       # Inside a task definition
    infunction = False   # Inside a function definition

    # Parse the text
    for lnum, line in enumerate(buff):
        line = line.strip()
        llen = len(line)
        idx = 0
        while idx < len(line):
            # Skip any leading Whitespace
            idx = parselib.SkipWhitespace(line, idx)

            # Check for coments
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
            elif parselib.IsToken(line, idx, u'class'):
                idx = parselib.SkipWhitespace(line, idx + 5)
                cname = parselib.GetFirstIdentifier(line[idx:])
                if cname is not None:
                    inclass = True
                    rtags.AddClass(taglib.Class(cname, lnum))
                break # go to next line
            elif inclass and parselib.IsToken(line, idx, u'endclass'):
                inclass = False
                break # go to next line
            elif parselib.IsToken(line, idx, u'task'):
                idx += 4
                tname = parselib.GetTokenParenLeft(line[idx:])
                if tname is not None:
                    intask = True
                    if inclass:
                        lclass = rtags.GetLastClass()
                        task = taglib.Function(tname, lnum, 'task',
                                               lclass.GetName())
                        lclass.AddElement('task', task)
                    else:
                        task = taglib.Function(tname, lnum, 'task')
                        rtags.AddElement('task', task)
                break # goto next line
            elif parselib.IsToken(line, idx, u'function'):
                idx += 8
                fname = parselib.GetTokenParenLeft(line[idx:])
                if fname is not None:
                    infunction = True
                    if inclass:
                        lclass = rtags.GetLastClass()
                        lclass.AddMethod(taglib.Method(fname, lnum))
                    else:
                        rtags.AddFunction(taglib.Function(fname, lnum))
                break
            elif intask and parselib.IsToken(line, idx, u'endtask'):
                intask = False
                break # go to next line
            elif infunction and parselib.IsToken(line, idx, 'endfunction'):
                infunction = False
                break
            else:
                idx += 1

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
