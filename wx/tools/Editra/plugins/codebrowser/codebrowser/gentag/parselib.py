###############################################################################
# Name: parselib.py                                                           #
# Purpose: Common parseing utility functions                                  #
# Author: Cody Precord <cprecord@editra.org>                                  #
# Copyright: (c) 2008 Cody Precord <staff@editra.org>                         #
# License: wxWindows License                                                  #
###############################################################################

"""
Contains misc common parsing helper functions used by the various parsers
in this library.

@summary: Common helper functions for tag generators.

"""

__author__ = "Cody Precord <cprecord@editra.org>"
__svnid__ = "$Id$"
__revision__ = "$Revision$"

#--------------------------------------------------------------------------#
import pygments
from pygments.token import Token
from pygments.lexers import get_lexer_by_name

#--------------------------------------------------------------------------#

class TokenNotFound(Exception):
    """Parsing exception"""
    pass

#--------------------------------------------------------------------------#
# Helper functions for modules using pygments

def GetTokenValue(line, searchToken):
    """Get the first value associated with the given token type in the line
    will raise TokenNotFound if the value cannot be found
    @return: string

    """
    for token, value in line:
        if token == searchToken:
            return value
    raise TokenNotFound, "GetTokenValue: Not found: %s" % str(searchToken)

def HasToken(line, searchToken, searchValue=None):
    """Find if the token exists in the line.
    @param line: line of code
    @param searchToken: Token to look for
    @return: bool
    @note: use sparingly as this can be slow

    """
    for token, value in line:
        if token == searchToken:
            if searchValue != None:
                if searchValue == value.strip():
                    return True
            else:
                return True
    return False

def BeginsWithToken(line, searchToken, searchValue):
    """Returns true it the first non whitespace token in the
    given line is the given token.
    @param line: pygments line enumeration
    @param searchToken: pygments.Token.
    @param searchValue: unicode

    """
    bOk = False
    if len(line):
        for token, val in line:
            if token == Token.Text and val.isspace():
                continue
            bOk = (searchToken == token and val == searchValue)
            break
    return bOk

def BeginsWithAnyOf(line, searchToken, searchValueList):
    """Returns true if the line begins with any of the given values
    @param searchValueList: list of unicode
    @see: BeginsWithToken

    """
    for value in searchValueList:
        if BeginsWithToken(line, searchToken, value):
            return True
    return False

#--------------------------------------------------------------------------#
# Function Definitions

def GetFirstIdentifier(line):
    """Extract the first identifier from the given line. Identifiers are
    classified as the first contiguous string of characters that only contains
    AlphaNumeric or "_" character. In other words [a-zA-Z0-9_]+.
    @return: identifier name or None

    """
    name = ''
    for char in line.strip():
        if char.isalnum() or char == "_":
            name += char
        else:
            break

    if len(name):
        return name
    else:
        return None

def GetTokenParenLeft(line, exchars='_'):
    """Get the first identifier token to the left of the first opening paren
    found in the given line.
    Example: function myfunct(param1) => myfunct
    @param line: line to search
    @keyword exchars: Extra non-alphanumeric characters that can be in the token
    @return: string or None

    """
    pidx = line.find(u'(')
    if pidx != -1:
        token = u''
        # Walk back from the paren ignoring whitespace
        for char in reversed(line[:pidx]):
            if char.isspace():
                if len(token):
                    break
            elif char.isalnum() or char in exchars:
                token += char
            else:
                break

        if len(token):
            return u"".join([char for char in reversed(token)])

    return None

def IsGoodName(name, exchars='_'):
    """Check if the name is a valid identifier name or not. A valid identifier
    is a string that only has alpha numeric and/or the specified exchars in it.
    Also meaning it matches the following character class [a-zA-Z_][a-zA-Z0-8_]+
    @param name: name to check
    @keyword exchars: extra non alphanumeric characters that are valid
    @return: bool

    """
    if len(name) and (name[0].isalpha() or name[0] in exchars):
        for char in name:
            if char.isalnum() or char in exchars:
                continue
            else:
                return False
        return True
    else:
        return False

def IsToken(line, idx, name, ignorecase=False):
    """Check if the given item is a token or not. The function will return
    True if the item at the given index matches the name and is preceded and
    followed by whitespace. It will return False otherwise.
    @param line: string to check
    @param idx: index in string to look from
    @param name: name of token to look for match
    @keyword ignorecase: do case insensitive search
    @return: bool

    """
    nchar = idx + len(name)
    if not ignorecase:
        tline = line
    else:
        tline = line.lower()
        name = name.lower()

    if tline[idx:].startswith(name) and \
       (idx == 0 or tline[idx-1].isspace()) and \
       (len(tline) > nchar and tline[nchar].isspace()):
        return True
    else:
        return False

def SkipWhitespace(line, idx):
    """Increment and return the index in the current line past any whitespace
    @param line: string
    @param idx: index to check from in line
    @return: int

    """
    return idx + (len(line[idx:]) - len(line[idx:].lstrip()))

def FindStringEnd(line, idx):
   """Walk through the string until the next non escaped matching ending
   quotation is found. Returning the current state of the parse. The first
   character in the given line should be the beginning of the string.
   @param line: line of text
   @param idx: current index in parse document
   @return: (idx, still_string)

   """
   start = line[0] # Save the beginning quote so we can find the end quote
   escaped = False
   for pos, char in enumerate(line):
       idx += 1
       if escaped:
           escaped = False
           continue

       if char == '\\':
           escaped = True
           continue

       if not escaped and pos > 0 and char == start:
           still_string = False
           break
   else:
       still_string = True

   return (idx, still_string)

#-----------------------------------------------------------------------------#

class ELexer(object):
    """
    A wrapper to add peeking and line counting to pygments lexer.
    Example usage:

        import pygments
        from pygments.token import Token
        from pygments.lexers import get_lexer_by_name
        
        iterable = pygments.lex(buff.read(), 
                                lexers.get_lexer_by_name('lexer_name'))
        peekable = PeekableLexer(iterable)
    
    The peekable iterator pattern has been copied from Anthony Baxter's 
    Oscon 2005 slides.

    """
    def __init__(self, iterable, ignore = [ Token.Comment, Token.Text ]):
        self.it = iterable
        self.cache = []
        self.line_count = 1
        self.ignore = ignore

    def __iter__(self):
        return self

    def next(self):
        if self.cache:
            return self.cache.pop()
        while self.it:
            ttype, tval = self.it.next()
            if '\n' in tval:
                tline = self.line_count + 1
                self.line_count += tval.count('\n')
            else:
                tline = self.line_count
            if ttype in self.ignore:
                continue

            return (tline, ttype, tval)
            # alternatively, we could return a clearly defined object instead of a tuple.
            # I personally prefer the object-way because it allows you to write: 
            # peek().ttype = ...
            # return EToken(tline, ttype, tval)

    def peek(self):
        try:
            value = self.next()
        except StopIteration:
            raise
        self.cache.append(value)
        return value

    def __nonzero__(self):
        try:
            self.peek()
        except StopIteration:
            return False
        return True

class EToken(object):
    def __init__(self, line, type, value):
        self.line = line
        self.type = type
        self.value = value

    def __repr__(self):
        return '%s, %s, %s' % (self.line, self.type, self.value)
