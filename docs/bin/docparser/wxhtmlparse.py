import sys, os, string, glob
import re
from docparser.wxclasses import *
import wx


outputdir = "output"

#
# Class REs
#

class_desc_re = """<H2>.*?</H2>(.*?)<B><FONT COLOR="#FF0000">"""
win_styles_re = """<B><FONT COLOR="#FF0000">Window styles</FONT></B><P>(.*?)<B><FONT COLOR="#FF0000">"""
win_styles_extra_re = """<B><FONT COLOR="#FF0000">Extra window styles</FONT></B><P>(.*?)<B><FONT COLOR="#FF0000">"""
derived_re = """<B><FONT COLOR="#FF0000">Derived from</FONT></B><P>(.*?)<P>"""
derived_class_re = """<A HREF=".*?">(.*?)</A>"""
include_re = """<FONT COLOR="#FF0000">Include files</FONT></B>\s?<P>(.*?)<P>"""
library_re = """<FONT COLOR="#FF0000">Library</FONT></B>\s?<P>(.*?)<P>"""
seealso_re = """<FONT COLOR="#FF0000">See also</FONT></B>\s?<P>(.*?)<P>"""
event_re = """<FONT COLOR="#FF0000">Event handling</FONT></B><P>(.*?)<P>"""
objects_re = """<FONT COLOR="#FF0000">Predefined objects</FONT></B><P>(.*?)<FONT COLOR="#FF0000">"""
table_row_re = """<TR><TD VALIGN=TOP.*?>\s*?<FONT FACE=".*?">\s*?<B>(.*?)</B>\s*?</FONT></TD>\s*?<TD VALIGN=TOP>\s*?<FONT FACE=".*?">(.*?)</FONT></TD></TR>"""


#
# Method REs
#

# groups - header, description
method_re = "<H3>(.*?)</H3>\s*?<P>(.*?)<HR>"
lastmethod_re = "<H3>(.*?)</H3>\s*?<P>(.*?)\s*?<P>\s*?</FONT>"
headings_re = "<B><FONT COLOR=\"#FF0000\">(.*?)</FONT></B><P>(.*?)"
# groups = param name, param value 
param_re = "<I>(.*?)</I><UL><UL>(.*?)</UL></UL>"
# groups - return type, method name, arguments
proto_re = "<B>(.*?)</B>.*?<B>(.*?)</B>\s*?\((.*?)\)"
# groups - arg type, arg name
args_re = "<B>(.*?)</B>.*?<I>(.*?)</I>"
code_re = "<PRE>(.*?)</PRE>"
link_re = "<A href=\"(.*?)\"><B>(.*?)</B></A><BR>"

remarks_re = """<B><FONT COLOR="#FF0000">Remarks</FONT></B><P>(.*?)<P>"""
retval_re = """<B><FONT COLOR="#FF0000">Return value</FONT></B><P>(.*?)<P>"""


#
# Formatting REs
#

basic_link_re = "<A href=\"(.*?)\">(.*?)</A>"
basic_bold_re = "<B>(.*?)</B>"
basic_italic_re = "<I>(.*?)</I>"
basic_typetext_re = "<TT>(.*?)</TT>"

#
# wxPython/wxPerl note REs
# 

wx_re = "wx[A-Z]\S+"
wxperl_overload_re = "<B><FONT COLOR=\"#0000C8\">wxPerl note:</FONT></B> In wxPerl there are two methods instead of a single overloaded method:<P>\s*?<UL><UL>(.*?)</UL></UL>"
wxperl_re = "<B><FONT COLOR=\"#0000C8\">wxPerl note:</FONT></B>(.*?)<P>"

wxpython_constructors_re = """<B><FONT COLOR="#0000C8">wxPython note:</FONT></B> Constructors supported by wxPython are:<P>\s*?<UL><UL>(.*?)</UL></UL>"""
wxpython_overload_re = """<TR><TD VALIGN=TOP.*?>\s*?<FONT FACE=".*?">\s*?<B>(.*?)</B>\s*?</FONT></TD>\s*?<TD VALIGN=TOP>\s*?<FONT FACE=".*?">(.*?)</FONT></TD></TR>"""

wxpython_overloads_re = "<B><FONT COLOR=\"#0000C8\">wxPython note:</FONT></B> In place of a single overloaded method name, wxPython\s*?implements the following methods:<P>\s*?<UL><UL>(.*?)</UL></UL>"
wxpython_re = "<B><FONT COLOR=\"#0000C8\">wxPython note:</FONT></B>(.*?)<P>"


# convert wxWhatever to wx.Whatever
def namespacify_wxClasses(contents):
    wx_regex = re.compile(wx_re, re.MULTILINE | re.DOTALL)
    
    result = wx_regex.sub(wxReplaceFunc, contents)
    return result

def wxReplaceFunc(match):
    text = match.group()
    
    return text
    
    #if text.find("wxWidgets") == -1 and text.find("wxPython") == -1 and text.find("wxPerl") == -1:
        #text = text.replace("wx", "wx.")
    #return text



# Methods to de-C++itize data.
def pythonize_text(contents):
    """
    Remove C++isms that definitely shouldn't be in any text.
    """
    
    #contents = contents.replace("false", "@false")
    #contents = contents.replace("true", "@true")
    #contents = contents.replace("non-NULL", "not None")
    #contents = contents.replace("NULL", "None")
    #contents = contents.replace("const ", "")
    #contents = contents.replace("::", ".")
    #contents = contents.replace("\r\n", "\n")
    #contents = contents.replace("\r", "\n")
    #contents = contents.replace("''", "\"")
    #return namespacify_wxClasses(contents)
    return contents

def pythonize_args(contents):
    """
    Remove C++isms from arguments (some of these terms may be used in other
    contexts in actual documentation, so we don't remove them there).
    """
    return contents
    
    #contents = contents.replace("static", "")
    #contents = contents.replace("virtual void", "")
    #contents = contents.replace("virtual", "")
    #contents = contents.replace("void*", "int")
    #contents = contents.replace("void", "")
    
    #contents = contents.replace("off_t", "long")
    #contents = contents.replace("size_t", "long")
    #contents = contents.replace("*", "")
    #contents = contents.replace("&amp;", "")
    #contents = contents.replace("&", "")
    #contents = contents.replace("char", "string") 
    #contents = contents.replace("wxChar", "string") 
    #contents = contents.replace("wxCoord", "int")
    #contents = contents.replace("<A HREF=\"wx_wxstring.html#wxstring\">wxString</A>", "string")
    
    return pythonize_text(contents)
    
def formatMethodProtos(protos):
    """
    Remove C++isms in the method prototypes. 
    """
    for proto in protos:
        proto[0] = pythonize_args(proto[0])
        proto[0] = proto[0].strip()
        
        proto[1] = namespacify_wxClasses(proto[1])
        for arg in proto[2]:
            arg[0] = pythonize_args(arg[0])
            arg[0].strip()
            
            # for arg names, we should be more careful about what we replace
            arg[1] = pythonize_text(arg[1])
            arg[1] = arg[1].replace("*", "")
            arg[1] = arg[1].replace("&", "")
    
    return protos

def convertFormatting(text):
    def replace_basic_link(match):
        ret = match.group(2).strip()
        if ret=="":
            return ""
        elif " " in ret:
            if "(" in ret and ")" in ret:
                # this is something like "wxDateTime(long tm)" and it's valid
                # to give to doxygen also the list of arguments:
                return "#" + ret
            else:
                ret = match.group(1).strip()
                if "#" not in ret and "http:" in ret:
                    return ret          # http link
                
                # this is probably a link to a topic overview or similar
                ret = ret.split("#")[1]
                ret = ret.replace("overview", "").strip()
                if ret.startswith("wx"):
                    ret = ret[2:]
                return "@ref " + ret + "_overview"
        elif "::" not in ret:
            ret = "#" + ret

        return ret
    
    # the desc could contain links which need an initial # in doxy world
    basic_link_regex = re.compile(basic_link_re, re.MULTILINE | re.DOTALL | re.IGNORECASE)
    text = basic_link_regex.sub(replace_basic_link, text)


    def replace_bold(match):
        ret = match.group(1).strip()
        return "@b " + ret

    basic_bold_regex = re.compile(basic_bold_re, re.MULTILINE | re.DOTALL | re.IGNORECASE)
    text = basic_bold_regex.sub(replace_bold, text)
    
    
    def replace_italic(match):
        ret = match.group(1).strip()
        return "@e " + ret

    basic_italic_regex = re.compile(basic_italic_re, re.MULTILINE | re.DOTALL | re.IGNORECASE)
    text = basic_italic_regex.sub(replace_italic, text)
    
    
    def replace_typetext(match):
        ret = match.group(1).strip()
        return "@c " + ret

    basic_typetext_regex = re.compile(basic_typetext_re, re.MULTILINE | re.DOTALL | re.IGNORECASE)
    text = basic_typetext_regex.sub(replace_typetext, text)


    def replace_code(match):
        ret = match.group(1).strip()
        return "\n@code\n" + ret + "\n@endcode\n"

    code_regex = re.compile(code_re, re.MULTILINE | re.DOTALL | re.IGNORECASE)
    text = code_regex.sub(replace_code, text)

    return text


# functions for getting data from methods 
def getMethodWxPythonOverrides(text, isConstructor=False):
    overloads_re = wxpython_overloads_re
    if isConstructor:
        overloads_re = wxpython_constructors_re
    overload_regex = re.compile(overloads_re, re.MULTILINE | re.DOTALL | re.IGNORECASE)
    match = overload_regex.search(text, 0)
    note = ""
    start = -1
    end = -1
    overrides = []
    if match:
        def getWxPythonOverridesFromMatch(match):
            return [namespacify_wxClasses(match.group(1)), pythonize_text(match.group(2))]
            
        start = match.start()
        end = match.end()
        overrides, returntext = findAllMatches(wxpython_overload_re, match.group(1), getWxPythonOverridesFromMatch)
        
    returntext = text
    
    if start != -1 and end != -1:
        #print "note is: " + text[start:end]
        returntext = text.replace(text[start:end], "")
        
    return overrides, returntext

def getMethodWxPythonNote(text):
    python_regex = re.compile(wxpython_re, re.MULTILINE | re.DOTALL | re.IGNORECASE)
    match = python_regex.search(text)
    start = -1
    end = -1
    note = ""
    if match:
        start = match.start()
        end = match.end()
        note = match.group(1)
            
    returntext = text
    
    if start != -1 and end != -1:
        #print "note is: " + text[start:end]
        returntext = text.replace(text[start:end], "")
            
    return note, returntext
    
def findAllMatches(re_string, text, handler, start=0):
    """
    findAllMatches finds matches for a given regex, then runs the handler function
    on each match, and returns a list of objects, along with a version of the 
    text with the area matches were found stripped.
    Note the stripping of text is not generally usable yet, it assumes matches
    are in continuous blocks, which is true of the wx docs.
    """
    regex = re.compile(re_string, re.MULTILINE | re.DOTALL | re.IGNORECASE)
    match = regex.search(text, start)
    results = []
    
    startpoint = -1
    endpoint = -1
    
    if match:
        startpoint = match.start()
    
    while match:
        start = match.end()
        results.append(handler(match))
        endpoint = match.end()
        match = regex.search(text, start)
        
    returntext = text
    if startpoint != -1 and endpoint != -1:
        returntext = text.replace(text[startpoint:endpoint], "")

    return results, returntext

def getMethodParams(text):
    paramstart = text.find("<B><FONT COLOR=\"#FF0000\">Parameters</FONT></B><P>")
    params, returntext = findAllMatches(param_re, text, getMethodParamsFromMatch, paramstart)
    
    return params, returntext
    
def getMethodParamsFromMatch(match):
    return [match.group(1).strip(), pythonize_text(match.group(2)).strip()]

def getPrototypeFromMatch(match):
    return [match.group(1), match.group(2), getProtoArgs(match.group(3))]

def getProtoArgsFromMatch(match):
    return [match.group(1), match.group(2)]

def getMethodRemarks(text):
    remarks_regex = re.compile(remarks_re, re.MULTILINE | re.DOTALL | re.IGNORECASE)
    match = remarks_regex.search(text)
    if match:
        return match.group(1).strip()
    return ""

def getMethodRetDesc(text):
    retval_regex = re.compile(retval_re, re.MULTILINE | re.DOTALL | re.IGNORECASE)
    match = retval_regex.search(text)
    if match:
        return match.group(1).strip()
    return ""

def getMethodSeeAlso(text):
    seealso_regex = re.compile(seealso_re, re.MULTILINE | re.DOTALL | re.IGNORECASE)
    match = seealso_regex.search(text)
    if match:
        ret = match.group(1).strip()
        ret = stripHTML(convertFormatting(ret))
        ret = ret.replace("\n", ", ").replace("  ", " ").replace(", , ", ", ").strip()
        ret = ret.replace(",,", ",")
        return ret
    return ""

# These methods parse the docs, finding matches and then using the FromMatch
# functions to parse the data. After that, the results are "Pythonized"
# by removing C++isms.
def getMethodProtos(text):
    protos, returntext = findAllMatches(proto_re, text, getPrototypeFromMatch)
    return formatMethodProtos(protos), returntext
    
def getProtoArgs(text):
    args, returntext = findAllMatches(args_re, text, getProtoArgsFromMatch)
    return args
    
def getMethodDesc(text):
    heading_text = "<B><FONT COLOR=\"#FF0000\">"
    return_text = text
    end = text.find(heading_text)
    if end != -1:
        return_text = text[0:end]
        
    return pythonize_text(convertFormatting(return_text))
    

def removeWxPerlNotes(text):
    perl_overload_regex = re.compile(wxperl_overload_re, re.MULTILINE | re.DOTALL | re.IGNORECASE)
    result = perl_overload_regex.sub("", text)
    
    perl_regex = re.compile(wxperl_re, re.MULTILINE | re.DOTALL | re.IGNORECASE)
    result = perl_regex.sub("", result)
    
    return result
    
def removeCPPCode(text):
    code_regex = re.compile(code_re, re.MULTILINE | re.DOTALL | re.IGNORECASE)
    
    result = code_regex.sub("", text)
    return result


def getMethod(match, parent):
    name = match.group(1)
    if name.find("::") != -1:
        name = name.split("::")[1]
    name = namespacify_wxClasses(name).strip()
    start = match.end()
    protos, remainder = getMethodProtos(match.group(2))
    
    isConstructor = False
    isDestructor = False
    if name == parent.name:
        isConstructor = True
    elif name == "~" + parent.name:
        isDestructor = True
    overrides, remainder = getMethodWxPythonOverrides(remainder, isConstructor)
    
    #print "name: %s, parent name: %s, ctor=%s, dtor=%s" % (name, parent.name, isConstructor, isDestructor)
    
    note, remainder = getMethodWxPythonNote(remainder)
    params, remainder = getMethodParams(remainder)
    desc = getMethodDesc(remainder)
    remarks = getMethodRemarks(remainder)
    retdesc = getMethodRetDesc(remainder)
    sa = getMethodSeeAlso(remainder)
    
    method = wxMethod(name, parent, protos, params, desc, isConstructor, isDestructor, remarks, retdesc, sa)
    method.pythonNote = note
    method.pythonOverrides = overrides
    ##if len(method.pythonOverrides) > 0:
        ##print "has overrides!\n\n\n\n"
    return method


def getFunction(match):
    name = match.group(1)
    if name.find("::") != -1:
        name = name.split("::")[1]
    name = namespacify_wxClasses(name).strip()
    start = match.end()
    protos, remainder = getMethodProtos(match.group(2))
    
    #print "name: %s" % name
    #print remainder
    
    note, remainder = getMethodWxPythonNote(remainder)
    params, remainder = getMethodParams(remainder)
    desc = getMethodDesc(remainder)
    remarks = getMethodRemarks(remainder)
    retdesc = getMethodRetDesc(remainder)
    sa = getMethodSeeAlso(remainder)
    
    method = wxMethod(name, "", protos, params, desc, False, False, remarks, retdesc, sa)
    method.pythonNote = note
    method.inclusionFile = getFuncIncludeFile(remainder)
    return method


def getClassDerivedFrom(text):

    def getDerivedClassesFromMatch(match):
        return namespacify_wxClasses(match.group(1))

    derived_classes = []
    derived_regex = re.compile(derived_re, re.MULTILINE | re.DOTALL | re.IGNORECASE)
    match = derived_regex.search(text)
    if match:
        derived_classes, returntext = findAllMatches(derived_class_re, match.group(1), getDerivedClassesFromMatch)
        
    return derived_classes
    

def getClassIncludeFile(text):

    include_regex = re.compile(include_re, re.MULTILINE | re.DOTALL | re.IGNORECASE)
    match = include_regex.search(text)
    if match:
        ret = match.group(1).strip().replace("&lt;", "").replace("&gt;", "")
        if ".h" not in ret:
            print "ERROR: cannot get include file from %s" % text
            sys.exit(1)
        ret = ret[:ret.find(".h")+2]
        if ret.startswith("wx/"):
            ret = ret[3:]
        return ret
    print "ERROR: cannot get include file from %s" % text
    sys.exit(1)

def getFuncIncludeFile(text):

    include_regex = re.compile(include_re, re.MULTILINE | re.DOTALL | re.IGNORECASE)
    match = include_regex.search(text)
    if match:
        ret = match.group(1).strip().replace("&lt;", "").replace("&gt;", "")
        if ".h" not in ret:
            return "functions.h"
        ret = ret[:ret.find(".h")+2]
        if ret.startswith("wx/"):
            ret = ret[3:]
        return ret
    return "functions.h"
    

def getClassLibrary(text):

    library_regex = re.compile(library_re, re.MULTILINE | re.DOTALL | re.IGNORECASE)
    match = library_regex.search(text)
    if match:
        ret = match.group(1).strip()
        
        x = HTMLStripper()
        x.feed(ret)
        return x.get_fed_data()
    
    #print "ERROR: cannot get library file from %s" % text
    #sys.exit(1)
    return "wxBase"
    

def getClassPredefinedObjects(text):

    objects_regex = re.compile(objects_re, re.MULTILINE | re.DOTALL | re.IGNORECASE)
    match = objects_regex.search(text)
    if match:
        ret = match.group(1).strip()
        
        x = HTMLStripper()
        x.feed(ret)
        return x.get_fed_data()
    
    #print "ERROR: cannot get library file from %s" % text
    #sys.exit(1)
    return ""

def getClassSeeAlso(text):

    seealso_regex = re.compile(seealso_re, re.MULTILINE | re.DOTALL | re.IGNORECASE)
    match = seealso_regex.search(text)
    if match:
        ret = match.group(1).strip()
        ret = stripHTML(convertFormatting(ret))
        ret = ret.replace("\n", ", ").replace("  ", " ").replace(", , ", ", ").strip()
        ret = ret.replace(",,", ",")
        
        #out = ""
        #for word in ret.split(","):
            #word = word.strip()
            #if " " not in word:
                ## should be a link probably...
                #out += "#" + word + ", "
            #else:
                #out += word + ", "
        #if len(out)>0:
            #out = out[:-2]
                
        return ret
    
    #print "ERROR: cannot get library file from %s" % text
    #sys.exit(1)
    return ""

def getClassDescription(text):
    def getClassDescriptionFromMatch(match):
        return match.group(1)
    
    desc, returntext = findAllMatches(class_desc_re, text, getClassDescriptionFromMatch)
    return convertFormatting(desc[0])  # pythonize_text(desc[0])
    
def getClassStyles(text, extraStyles=False):
    styles_re = win_styles_re
    if extraStyles:
        styles_re = win_styles_extra_re
    styles_regex = re.compile(styles_re, re.MULTILINE | re.DOTALL | re.IGNORECASE)
    match = styles_regex.search(text)
    
    styles = []
    if match:
        def getClassStyleFromMatch(match):
            return [namespacify_wxClasses(match.group(1)), pythonize_text(match.group(2))]
            
        styles, remainder = findAllMatches(table_row_re, match.group(1), getClassStyleFromMatch)
        
    return styles

def getClassEvents(text):
    event_regex = re.compile(event_re, re.MULTILINE | re.DOTALL | re.IGNORECASE)
    match = event_regex.search(text)
    
    events = []
    if match:
        def getClassEventFromMatch(match):
            return [namespacify_wxClasses(match.group(1)), pythonize_text(match.group(2))]
            
        events, remainder = findAllMatches(table_row_re, match.group(1), getClassEventFromMatch)
        
    return events
    
# Main functions - these drive the process.
def getClassMethods(doc, parent):
    contents = open(doc, "rb").read()
    
    # get rid of some particularly tricky parts before parsing
    contents = contents.replace("<B>const</B>", "")
    contents = removeWxPerlNotes(contents)
    contents = removeCPPCode(contents)
    
    method_regex = re.compile(method_re, re.MULTILINE | re.DOTALL | re.IGNORECASE)
    match = method_regex.search(contents)
    start = 0
    methods = {}
    while match:
        start = match.end()
        newmethod = getMethod(match, parent)
        basename = parent.name.replace("wx", "")
        #isConstructor = (basename == newmethod.name.replace("wx.", ""))
        #if isConstructor or eval("newmethod.name in dir(wx.%s)" % basename):
            ###print "Adding %s.%s" % (parent.name, newmethod.name)
        methods[newmethod.name] = newmethod
        match = method_regex.search(contents, start)
    
    lastmethod_regex = re.compile(lastmethod_re, re.MULTILINE | re.DOTALL | re.IGNORECASE)
    match = lastmethod_regex.search(contents, start)
    if match: 
        newmethod = getMethod(match, parent)
        basename = parent.name.replace("wx", "")
        #isConstructor = (basename == newmethod.name.replace("wx.", ""))
        #if isConstructor or eval("newmethod.name in dir(wx.%s)" % basename):
            ###print "Adding %s.%s" % (parent.name, newmethod.name)
        methods[newmethod.name] = newmethod
    
    #for name in methods:
        #if name[0:3] == "Get":
            #propname = name[3:]
            #basename = parent.name.replace("wx", "")
            #if not propname in eval("dir(wx.%s)" % basename):
                #parent.props.append(propname)
            #else:
                #parent.propConflicts.append(parent.name + "." + propname)
    ## get rid of the destructor and operator methods
    #ignore_methods = ["~" + namespacify_wxClasses(parent.name), "operator ==", 
                        #"operator &lt;&lt;", "operator &gt;&gt;", "operator =", 
                        #"operator !=", "operator*", "operator++" ]
    #for method in ignore_methods:
        #if method in methods:
            #methods.pop(method)
            
    return methods
        
def getClasses(doc):
    global docspath
    contents = open(doc, "rb").read()
    link_regex = re.compile(link_re, re.MULTILINE | re.DOTALL | re.IGNORECASE)
    start = contents.find("<H2>Alphabetical class reference</H2>")
    result = link_regex.search(contents, start)
    classes = {}
    while result:
        start = result.end()
        name = result.group(2).strip()
        classpage = result.group(1).split("#")[0]
        basename = name.replace("wx", "")
        
        #if basename in dir(wx):
        classfile = os.path.join(os.path.dirname(doc), classpage)
        if not os.path.exists(classfile):
            print "could not open %s" % classfile
            sys.exit(1)
        
        #print "Parsing ", classfile
        classtext = open(classfile, "rb").read()
        derivedClasses = getClassDerivedFrom(classtext)
        description = getClassDescription(classtext)
        styles = getClassStyles(classtext)
        
        extra_styles = getClassStyles(classtext, extraStyles=True)
        lib = getClassLibrary(classtext)
        sa = getClassSeeAlso(classtext)
        events = getClassEvents(classtext)
        
        classes[name] = wxClass(name, description, derivedClasses, events, styles, extra_styles, lib, sa)
        classes[name].methods = getClassMethods(classfile, classes[name])
        classes[name].inclusionFile = getClassIncludeFile(classtext)
        classes[name].objects = getClassPredefinedObjects(classtext)
        
        result = link_regex.search(contents, start)

    return classes


def getFunctions(doc):
    global docspath
    contents = open(doc, "rb").read()
    link_regex = re.compile(basic_link_re, re.MULTILINE | re.DOTALL | re.IGNORECASE)
    funcstart = contents.find("<H2>Alphabetical functions and macros list</H2>")
    result = link_regex.search(contents, funcstart)
    
    processed_files = []
    functions = {}
    while result:
        funcstart = result.end()
        name = result.group(2).strip()
        classpage = result.group(1).split("#")[0]
        basename = name.replace("wx", "")
        
        #if basename in dir(wx):
        funcfile = os.path.join(os.path.dirname(doc), classpage)
        if not os.path.exists(funcfile):
            print "could not open %s" % funcfile
            sys.exit(1)
        
        if funcfile in processed_files:
            result = link_regex.search(contents, funcstart)
            continue
        
        #print "Parsing ", funcfile
        functext = open(funcfile, "rb").read()
        
            
        method_regex = re.compile(method_re, re.MULTILINE | re.DOTALL | re.IGNORECASE)
        match = method_regex.search(functext)
        start = 0
        methods = {}
        while match:
            start = match.end()
            newmethod = getFunction(match)
            functions[newmethod.name] = newmethod
            match = method_regex.search(functext, start)
        
        lastmethod_regex = re.compile(lastmethod_re, re.MULTILINE | re.DOTALL | re.IGNORECASE)
        match = lastmethod_regex.search(functext, start)
        if match: 
            newmethod = getFunction(match)
            
        processed_files.append(funcfile)
        result = link_regex.search(contents, funcstart)

    print "functions are: ", functions.keys()

    return functions
        
        

def getTO(doc):
    global docspath
    contents = open(doc, "rb").read()
    link_regex = re.compile(basic_link_re, re.MULTILINE | re.DOTALL | re.IGNORECASE)
    funcstart = contents.find("<H2>Topic overviews</H2>")
    result = link_regex.search(contents, funcstart)
    
    processed_files = []
    to = {}
    while result:
        funcstart = result.end()
        name = result.group(2).strip()
        classpage = result.group(1).split("#")[0]
        basename = name.replace("wx", "")
        
        #if basename in dir(wx):
        funcfile = os.path.join(os.path.dirname(doc), classpage)
        if not os.path.exists(funcfile):
            print "could not open %s" % funcfile
            sys.exit(1)
        
        if funcfile in processed_files:
            result = link_regex.search(contents, funcstart)
            continue
        
        #print "Parsing TO ", funcfile
        totext = open(funcfile, "rb").read()
        
        # get long name
        to_regex = re.compile("""<H2>(.*?)</H2>""", re.MULTILINE | re.DOTALL | re.IGNORECASE)
        match = to_regex.search(totext)
        if not match:
            print "Can't match in", totext
            sys.exit(1)
        start = match.end()
        longname = match.group(1).strip()
        
        # get shortname
        to_link_regex = re.compile("""<A NAME="(.*?)"></A><CENTER>""", re.MULTILINE | re.DOTALL | re.IGNORECASE)
        match = to_link_regex.search(totext)
        if not match:
            print "Can't match in", totext
            sys.exit(1)

        shortname = match.group(1).strip()
        if shortname.startswith("wx"):
            shortname = shortname[2:]
        shortname = shortname.replace("overview", "")

        doxytext = totext[start:]

        # substitute subsections
        to_regex = re.compile("""<HR>\n<A NAME="(.*?)"></A>\n<H3>(.*?)</H3>""", re.MULTILINE | re.DOTALL | re.IGNORECASE)
        
        def replace_sect(match):
            return "@section %s %s" % (match.group(1).strip(), match.group(2).strip())
        
        doxytext = to_regex.sub(replace_sect, doxytext)
        
        # elaborate to text
        doxytext = stripHTML(convertFormatting(doxytext))
        doxytext = "/*!\n\n@page %s_overview %s\n\n%s\n\n*/\n\n" % (shortname, longname, doxytext.strip())
        
        #indent_regex = re.compile("""\*  \S""", re.MULTILINE | re.DOTALL | re.IGNORECASE)
        #doxtext = indent_regex.sub("* ", doxytext)
        
        to[shortname] = doxytext.replace("\n", "\n ")
            
        processed_files.append(funcfile)
        result = link_regex.search(contents, funcstart)

    print "topic overviews are: ", to.keys()

    return to
        
        