###############################################################################
# Name: javatags.py                                                           #
# Purpose: Generate Tags for Java Source code                                 #
# Author: Eric Gaudet                                                         #
# License: wxWindows License                                                  #
###############################################################################

"""
DocStruct generator for Java, inspired by dtags.py

@author: Eric Gaudet
@summary: Generate a DocStruct object that captures the structure of Java source code.

"""

__author__ = "Eric Gaudet"

#--------------------------------------------------------------------------#

# Imports
import re

# Local Imports
import taglib
import parselib

#--------------------------------------------------------------------------#

STR_SCOPE = r"public|private|protected"
STR_TYPE = r"[A-Za-z0-9_.<>\[\], ]+"
STR_FINAL_AND_STATIC = r"final\s+static|static\s+final"
STR_FINAL_OR_STATIC = r"static|final|" + STR_FINAL_AND_STATIC
STR_NAME = r"[A-Za-z][A-Za-z0-9_]+"
STR_CLASS_PATH = r"[*A-Za-z0-9_.]+"
STR_METHOD_DECLARATION = r"synchronized|abstract|synchronized\s+abstract|abstract\s+synchronized"

RE_PACKAGE = re.compile(r"package\s+("+STR_CLASS_PATH+");")
RE_IMPORT = re.compile(r"import\s+("+STR_CLASS_PATH+");")
RE_CONST = re.compile(r"("+STR_SCOPE+")?\s*("+STR_FINAL_AND_STATIC+")\s*("+STR_TYPE+")\s+("+STR_NAME+")\s*[^;]*")
RE_VAR   = re.compile(r"("+STR_SCOPE+")?\s*("+STR_FINAL_OR_STATIC+")?\s*("+STR_TYPE+")\s+("+STR_NAME+")\s*[^;]*")
RE_CLASS = re.compile(r"("+STR_SCOPE+")?\s*.*\s*(class|interface)\s+("+STR_NAME+")")
RE_METH  = re.compile(r"("+STR_SCOPE+")?\s*("+STR_FINAL_OR_STATIC+")?\s*("+STR_METHOD_DECLARATION+")?\s*("+STR_TYPE+")?\s+("+STR_NAME+")\s*\(([^)]*)\(?")

RE_COMMENT_INLINE = re.compile('(/\*.*?\*/)')
RE_STRING_INLINE  = re.compile('(".*?")')
RE_BACKSLASHEDQUOTE_INLINE  = re.compile(r'(\\")')
RE_CHARACTER_INLINE = re.compile(r"('[{}]')")

#--------------------------------------------------------------------------#

def GenerateTags(buff):
    """Create a DocStruct object that represents the structure of a Java source
    file.
    @param buff: a file like buffer object (StringIO)
    """
    rtags = taglib.DocStruct()
    rtags.SetElementDescription('class', "<no package>")
    rtags.SetElementDescription('variable', "Imports")

    # State Variables
    inComment    = False

    currentLevel = 0
    methodSignature = None
    methodLnum   = 0
    methodClass  = None

    lastClass = []
    imports = None

    # Parse the buffer
    # Simple line based parser, likely not to be accurate in all cases
    for lnum, line in enumerate(buff):

        lastLevel = currentLevel

        lineCodeOnly = line[:]
        lineCodeOnly = RE_BACKSLASHEDQUOTE_INLINE.sub("'",lineCodeOnly)
        lineCodeOnly = RE_STRING_INLINE.sub('',lineCodeOnly)
        lineCodeOnly = RE_CHARACTER_INLINE.sub('',lineCodeOnly)
        #print "[[[",lineCodeOnly,"]]]"
        
        # remove trailing comments
        cut = line.find('//')
        if cut>-1:
            line = line[:cut]

        line = RE_COMMENT_INLINE.sub('',line)

        if inComment:
            cut = line.find('*/')
            if cut>-1:
                line = line[cut+2:]
                inComment = False
            else:
                continue

        # remove starting comments
        cut = line.find('/*')
        if cut>-1:
            line = line[:cut]
            inComment = True

        line = line.strip()
        if len(line)==0:
            continue

        diff = lineCodeOnly.count('{') - lineCodeOnly.count('}')
        currentLevel += diff

#        print "<<<",line,">>>", lnum, currentLevel, diff, len(lastClass), inComment
        if diff < 0:
            while len(lastClass) > currentLevel:
                #print "POP", len(lastClass), currentLevel, lastClass[-1]
                lastClass.pop()

        # handle multi-line method definition
        if methodSignature:
            cl = line.find(')')
            if cl > -1:
                if cl==0:
                    methodSignature += ')'
                else:
                    methodSignature += ' ' + line[:cl]
                methodClass.AddMethod(taglib.Method(methodSignature, methodLnum))
                #print "METH == ", methodSignature
                methodSignature = None
                continue
            else:
                methodSignature += ' ' + line
                #print "METH ++ ", methodSignature
                continue

        if currentLevel == 0:
            match = RE_PACKAGE.match(line)
            if match:
                groups = match.groups()
                #print "PACKAGE", groups
                rtags.SetElementDescription('class', groups[-1])
                continue

            match = RE_IMPORT.match(line)
            if match:
                groups = match.groups()
                #print "IMPORT", groups
                cobj = taglib.Variable(groups[-1], lnum)
                rtags.AddVariable(cobj)
                continue

        match = RE_CLASS.match(line)
        if match:
            cname = match.groups()[-1]
            if len(lastClass) > 0:
                cname = '$ '+cname
            cobj = taglib.Class(cname, lnum)
            rtags.AddClass(cobj)
            lastClass.append(cobj)
            #print "CLASS", cname
            continue

        if len(lastClass) == lastLevel:
            match = RE_METH.match(line)
            if match:
                groups = match.groups()
                prefix = ''
                methodSignature = groups[-2]
                warning = None
                if groups[3] == None:
                    contructor_for = lastClass[-1].GetName()
                    if contructor_for[0] == '$':
                      contructor_for = contructor_for[2:]
                    if groups[-2] == contructor_for:
                        prefix = '>'
                    else:
                        warning = 'tag_red'
                        methodSignature += ' - ???'
                else:
                    methodSignature += ' - ' +  groups[3]
                methodSignature += ' ('
                if groups[1] and (groups[1].find('static') > -1):
                    prefix += '_'
                if groups[2] and (groups[2].find('abstract') > -1):
                    prefix += '@'
                if len(prefix) > 0:
                    methodSignature = prefix + ' ' + methodSignature
                if groups[-1]:
                    methodSignature += groups[-1]
                if line.find(')') > -1:
                    methodSignature += ')'
                    cobj = taglib.Method(methodSignature, lnum)
                    if warning:
                        cobj.type = warning
                    lastClass[-1].AddMethod(cobj)
                    #print "METH", groups, methodSignature, lastClass[-1]
                    methodSignature = None
                else:
                    methodLnum = lnum
                    methodClass = lastClass[-1]
                continue

            match = RE_CONST.match(line)
            if match:
                groups = match.groups()
                #print "CONST", groups, lastClass[-1]
                cname = groups[-1] + ' -- ' +  groups[-2]
                cobj = taglib.Macro(cname, lnum)
                lastClass[-1].AddVariable(cobj)
                continue

            match = RE_VAR.match(line)
            if match:
                groups = match.groups()
                #print "VAR", groups, lastClass[-1]
                cname = groups[-1] + ' - ' +  groups[-2]
                #print groups[-2]
                if groups[-2][:6]=='throws':
                    continue
                if groups[1] and (groups[1].find('static') > -1):
                    cname = '_ ' + cname
                cobj = taglib.Variable(cname, lnum)
                lastClass[-1].AddVariable(cobj)
                continue

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
    for element in tags.GetElements():
        print "\n%s:" % element.keys()[0]
        for val in element.values()[0]:
            print "%s [%d]" % (val.GetName(), val.GetLine())
            if isinstance(val, taglib.Scope):
                for sobj in val.GetElements():
                    for meth in sobj.values()[0]:
                        t = type(meth).__name__
                        if t=='Macro':
                            t = 'C'
                        elif t=='Variable':
                            t = 'V'
                        elif t=='Method':
                            t = 'M'
                        print "\t%s - %s [%d]" % (t, meth.GetName(), meth.GetLine())
    print "END"


