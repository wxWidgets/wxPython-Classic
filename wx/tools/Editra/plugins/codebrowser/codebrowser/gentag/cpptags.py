###############################################################################
# Name: cpptags.py                                                            #
# Purpose: Generate CPP Tags                                                  #
# Author: Luis Cortes                                                         #
# Copyright: (c) 2008 Cody Precord <staff@editra.org>                         #
# License: wxWindows License                                                  #
###############################################################################

"""
FILE: cpp.py
AUTHOR: Luis Cortes
LANGUAGE: CPP
SUMMARY:
  Generate a DocStruct object that captures the structure of a python document.
It supports parsing for global and class variables, class, method, and function
definitions.

@todo: add back support for class variables
@todo: document functions

@note: Not used, still too buggy. Currently using regex based parser in ctags.py

"""

__author__ = "Cody Precord <cprecord@editra.org>"
__svnid__ = "$Id$"
__revision__ = "$Revision$"

#--------------------------------------------------------------------------#
# Dependancies
import taglib
from CppSemantics import CppSemantics, NotUsed

from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.formatter import Formatter
import sys
import StringIO

#--------------------------------------------------------------------------#

class CppFormatter(Formatter):
    """ Do a little preprocessing, and pass list of tokens and lines
    to CppSemantics class.
    """

    def format(self, tokensource, outfile):
        """ take code, and convert to token, value, num list 
        """
    
        NotUsed( outfile )
    
        self.rtags = taglib.DocStruct()
        self.rtags.SetElementDescription('function', "Function Definitions")
        self.rtags.SetElementDescription('class', "Class Definitions")

        line_count = 0
        current_line = []

        # Parse the file into tokens and values
        for ttype, value in tokensource:
            #print "LINE:", value
            if '\n' in value:
                line_count += value.count('\n')
                continue
            #if ( len(value.strip()) != 0 ):
            current_line.append((ttype, value, line_count))

        #print current_line
        self.getFunctions(current_line)


    def getFunctions( self, current_line ):
        """ Give list of token, value, num, feed to state machine
        to create rtags.
        """

        state_machine = CppSemantics( self.rtags )
        for token, value, num in current_line:
            state_machine.Feed( token, value, num )
        return state_machine.rtags

#-----------------------------------------------------------------------------#

def GenerateTags(buff):
    """GenTag interface method
    @return: taglib.DocStruct

    """
    code = buff.read()
    # print "CODE", code
    lexer = get_lexer_by_name( "cpp", stripall = False )

    formatter = CppFormatter()
    highlight( code, lexer, formatter)
    return formatter.rtags

#-----------------------------------------------------------------------------#
# Test
if __name__ == '__main__':
    _FHANDLE = open(sys.argv[1])
    _TXT = _FHANDLE.read()
    _FHANDLE.close()
    _TAGS = GenerateTags(StringIO.StringIO( _TXT ))
    print "\n\nVARIABLES:"
    for var in _TAGS.GetVariables():
        print "%s [%d]" % (var.GetName(), var.GetLine())
    print "\n\nFUNCTIONS:"
    for fun in _TAGS.GetFunctions():
        print "%s [%d]" % (fun.GetName(), fun.GetLine())
    print "\n\nCLASSES:"
    for c in _TAGS.GetClasses():
        print "* %s [%d]" % (c.GetName(), c.GetLine())
    print "END"
