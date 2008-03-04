#!/usr/bin/python

# use as
# ./extract-interface-headers.py wxPython-path/src wxWidgets-path/html-manual-path
#

# turn on/off the INJECT_MODE
#INJECT_MODE = True
INJECT_MODE = False
TOPIC_OVERVIEWS = False
GFUNCTIONS = True

import sys, os, re
import glob
from docparser.wxclasses import *
from docparser.wxhtmlparse import *

arg = """\s*?(.*?)\s*?"""
quoted_arg = """\s*?"(.*?)"\s*?"""

DocDeclA_re = re.compile("""(DocDeclA\()%s,%s,%s\);""" % (arg, arg, quoted_arg), re.MULTILINE | re.DOTALL)
DocDeclStr_re = re.compile("""(DocDeclStr\()(.*?),%s,%s,%s\);*?""" % (arg, quoted_arg, quoted_arg), 
                    re.MULTILINE | re.DOTALL)
DocDeclAStr_re = re.compile("""(DocDeclAStr\()(.*?),%s,%s,%s\);""" % (arg, quoted_arg, quoted_arg), 
                    re.MULTILINE | re.DOTALL)
DocDeclAStrName_re = re.compile("""(DocDeclAStrName\()(.*?),\s*?(.*?)\s*?,\s*?"(.*?)"\s*?,\s*?"(.*?)"\s*?,\s*?(.*?)\s*?\);""", 
                    re.MULTILINE | re.DOTALL)


DocDeclStrName_re = re.compile("""(DocDeclStrName\()(.*?),\s*?(.*?)\s*?,\s*?"(.*?)"\s*?,\s*?"(.*?)",\s*?(.*?)\s*?\);""", 
                    re.MULTILINE | re.DOTALL)
DocDeclAName_re = re.compile("""(DocDeclAName\()(.*?),\s*?(.*?)\s*?,\s*?"(.*?)"\s*?,\s*?(.*?)\s*?\);""", 
                    re.MULTILINE | re.DOTALL)
DocStr_re = re.compile("""(DocStr\()\s*?(.*?)\s*?,\s*?"(.*?)"\s*?,\s*?"(.*?)"\s*?\);""", re.MULTILINE | re.DOTALL)
DocAStr_re = re.compile("""(DocAStr\()%s,%s,%s,%s\);""" % (arg, quoted_arg, quoted_arg, quoted_arg), re.MULTILINE | re.DOTALL)
DocCtorStr_re = re.compile("""(DocCtorStr\()\s*?(.*?)\s*?,\s*?"(.*?)"\s*?,\s*?"(.*?)"\s*?\);""", re.MULTILINE | re.DOTALL)
DocCtorAStr_re = re.compile("""(DocCtorAStr\()%s,%s,%s,%s\);""" % (arg, quoted_arg, quoted_arg, quoted_arg), re.MULTILINE | re.DOTALL)
DocCtorStrName_re = re.compile("""(DocCtorStrName\()\s*?(.*?)\s*?,\s*?"(.*?)"\s*?,\s*?"(.*?)"\s*?,\s*?(.*?)\s*?\);""", re.MULTILINE | re.DOTALL)

#class_re = re.compile("""(^\s*?class )(.*?)$""", re.MULTILINE)
class_re = re.compile("""(^\s*?class )([^\;]*?)(\s*?{)(.*?)(\n^\s*?};)""", re.MULTILINE | re.DOTALL)


pymacros_block1_re = re.compile("""(%\w+\s*?{.*?}\s*?})""", re.MULTILINE | re.DOTALL)
pymacros_inline_re = re.compile("""(%inline\s*?%{.*?%})""", re.MULTILINE | re.DOTALL)
pymacros_pythoncode_re = re.compile("""(%pythoncode\s*?{.*?})""", re.MULTILINE | re.DOTALL)
pymacros_pythoncode_string_re = re.compile("""(%pythoncode\s*?".*?")""", re.MULTILINE | re.DOTALL)
pymacros_insert_re = re.compile("""(%{.*?%})""", re.MULTILINE | re.DOTALL)
pymacros_rename_re = re.compile("""(%Rename\(.*?,.*?,.*?\);)""", re.MULTILINE | re.DOTALL)
pymacros_renamector_re = re.compile("""(%RenameCtor\(.*?,.*?\);)""", re.MULTILINE | re.DOTALL)
pymacros_constant_re = re.compile("""(%constant.*?;)""", re.MULTILINE | re.DOTALL)
pymacros_rename_small_re = re.compile("""(%rename\(.*?\).*?;)""", re.MULTILINE | re.DOTALL)
pymacros_disownarg_re = re.compile("""(%disownarg\(.*?\);)""", re.MULTILINE | re.DOTALL)
pymacros_property_re = re.compile("""(%property\(.*?\)(?:;|))""", re.MULTILINE | re.DOTALL)
pymacros_cleardisown_re = re.compile("""(%cleardisown\(.*?\);)""", re.MULTILINE | re.DOTALL)
pymacros_immutable_re = re.compile("""(%immutable;)""", re.MULTILINE | re.DOTALL)
pymacros_mutable_re = re.compile("""(%mutable;)""", re.MULTILINE | re.DOTALL)
pymacros_nokwargs_re = re.compile("""(%nokwargs.*?;)""", re.MULTILINE | re.DOTALL)
pymacros_musthaveapp_re = re.compile("""(MustHaveApp\(.*?\);)""", re.MULTILINE | re.DOTALL)
pymacros_foopend_re = re.compile("""(%python(Ap|Pre)pend\s*\w*\s*.*)""", re.MULTILINE)
pymacros_makebasefunc_re = re.compile("""(%MAKE_BASE_FUNC\(.*?,.*?\);)""", re.MULTILINE)
pymacros_typemap_re = re.compile("""(%typemap\(\w+\)\s*?.*?(;|{.*?;\s*?}))""", re.MULTILINE | re.DOTALL)
pymacros_apply_re = re.compile("""(%apply.*?{.*?};)""", re.MULTILINE | re.DOTALL)
pymacros_newobject_re = re.compile("""(%newobject.*?;)""", re.MULTILINE | re.DOTALL)
pymacros_noautodoc_re = re.compile("""(%noautodoc.*?;)""", re.MULTILINE | re.DOTALL)


pymacros_args_re = re.compile("""(%\w+\s*?\(.*?\);)""")
pymacros_re = re.compile("""(%\w+.*?)""")

classes_in_header = {}
classes = {}
ignore_ifiles = ["_defs.i", "_core_api.i"]
undocumented = []
documented_count = 0
broken_sig = []

baseclass_mapping = { "wxBookCtrlBase" : [ "wxNotebook", "wxListbook", "wxToolbook", "wxTreebook", "wxChoiceBook" ], }

def stripArgsFromFunction(name):
    parenspos = name.find("(")
    if parenspos != -1:
        name = name[0:parenspos]
        
    return name

def inject_docs_into_header(classname, text):
    global undocumented
    global broken_sig
    global documented_count
    
    outtext = text
    classname = classname.strip()
    
    #if classname=='wxColourData':
        #print "outtext: ",outtext
    
    if classname in classes: 
        methods = classes[classname].methods
            
        for method in methods:
            type = "(virtual void )"
            methodname = methods[method].name
            if len(methods[method].prototypes) > 0:
                
                outtype = methods[method].prototypes[0][0].strip()
                
                
                x = HTMLStripper()
                x.feed(outtype)
                type = x.get_fed_data()
                
                # fix wxDateTime& being transformed erraneously to wxDateTime
                if outtype[-1:] == '&':
                    type = type+ '&'
                
                #print "outtype is", outtype, "type is", type
                
                # usually headers don't declare methods as virtual, so we add it ourself.
                # however, if they do declare it, we'll get virtual virtual unless we 
                # remove one of them.
                type = type.replace("virtual ", "")
                type = "(virtual " + type.replace("*", "\*") + " )"
            
            #pos = outtext.find(methodname)
            #if pos > -1:
            #    print "Found %s!" % methodname
            #    linestart = outtext.rfind("\n", 0, pos)
            #    print "pos = %d, linestart = %d" % (pos, linestart)
            #    indent = pos - linestart 
            #    print "indent is: %d" % indent
            #    outtext = outtext[:linestart-1] + "\n" + methods[method].asDoxygen(indent) + outtext[linestart:] 
            
            methodname = methodname.strip() + "\\("
            methodregexstr = type + "(" + methodname + ")"
            
            methodregex = """(.*?)(\s*?)%s(.*?)""" % methodregexstr.replace(" ", "\s*?")
            #print "methodregexstr: ", methodregex
            
            #print "method is: %s, %s" % (classname, methodregex)
            try:
                regex = re.compile(methodregex, re.DOTALL)
            except:
                print "methodregex is ", methodregex
            result = regex.match(outtext)
            found=False
            if result:
                found=True
            else:
                # try looking for the method without the virtual prefix
                methodregexstr = type.replace("virtual ", "") + "(" + methodname + ")"
            
                methodregex = """(.*?)(\s*?)%s(.*?)""" % methodregexstr.replace(" ", "\s*?")
                regex = re.compile(methodregex, re.DOTALL)
                result = regex.match(outtext)
                if result:
                    found = True

            if found:
                documented_count += 1
                indent = len(result.group(2).split("\n")[-1])
                #print "indent is %d" % indent
                #outtext = result.group(1) + methods[method].asDoxygen(indent) + "\n" + result.group(2) + result.group(3) + result.group(4)
                # don't add the docs for all signatures
                outtext = regex.sub("\\1\\2\\n%s\\n\\n%s\\3\\4\\5" % \
                    (methods[method].asDoxygen(indent), " " * indent), outtext, count=1)
            else:
                
                # try one more time to see if the method's there, but it's  got the wrong signature...
                methodregexstr = "(" + methodname + ")"
                
                methodstring = methodname.replace("\\","")
                result = outtext.find(methodstring)
                #methodregex = """(.*?)%s(.*?)""" % methodregexstr
                #print "methodregex = %s" % methodregex
                #regex = re.compile(methodregex, re.DOTALL)
                #result = regex.match(outtext)
                #if classname == "wxWindow" and methodstring == "LineUp(":
                #    print outtext
                    
                outtype = ""
                if len(methods[method].prototypes) > 0:
                    outtype = methods[method].prototypes[0][0].strip() + " "
                    
                if result != -1:
                    broken_sig.append(type + classname + "::" + methodstring)
                else:
                    undocumented.append(type + classname + "::" + methodstring)
                    print "  WARNING: couldn't find %s in %s" % (methodstring, classname)
    
    return outtext
    
def replace_class_in_header(match):
    classname = match.group(2).split(":")[0].strip()
    classname = classname.strip()
    classdocs = ""
    
    if classname in classes:
        classdocs = classes[classname].asDoxygen() + "\n\n"
        
    #if classname=='wxConfigBase' or classname=='wxAboutDialogInfo':
        #print "matches:\nmatch1:%s\nmatch2:%s\nmatch3:%s\nmatch4:%s\nmatch5:%s" \
            #% (match.group(1), match.group(2), match.group(3), match.group(4), match.group(5))
        
    return classdocs + match.group(1) + match.group(2) + match.group(3) + \
           inject_docs_into_header(classname, match.group(4)) + match.group(5)

def replace_ctor_str_in_header(match):
    return match.group(2) + ";"
    
def replace_decl_str_in_header(match):
    return match.group(2) + " " + match.group(3)
    
def replace_decl_strname_in_header(match):
    return """%s %s""" % (match.group(2), match.group(3))

def replace_decl_aname_in_header(match):
    return """%s %s;""" % (match.group(2), match.group(3))
    
def swigify_macro(match):
    return "#ifdef SWIG\n%s\n#endif // ifdef SWIG" % (match.group(0))
    
def replace_bracketed_text(match):
    text = match.group(0)
    #textlen = len(text)

    nestedbrackets=0
    bracketpos = text.find("{")
    closebracketpos = text.find("}")
    
    nextbracketpos = text.find("{", bracketpos+1)
    # remove everything up to the first closing bracket if we don't have nested brackets
    if nextbracketpos == -1:
        return text[closebracketpos:]
    
    while nextbracketpos < closebracketpos:
        print "nextbracketpos=%d" % nextbracketpos
        nextbracketpos = text.find("{", nextbracketpos+1)
        if nextbracketpos == -1:
            break
        nestedbrackets += 1
    
    while nestedbrackets > 0:
        closebracketpos = text.find("}", closebracketpos+1)
        nestedbrackets -= 1
        
    return text[closebracketpos+1:]
            
    
        
def replace_empty(match):
    return ""

def i_file_to_header_and_docstring_file(filename, outdir="."):
    global classes_in_header
    basename = os.path.splitext(os.path.basename(filename))[0]
    
    inputfile = open(filename, "r")
    header = basename + ".h"
    if header[0] == "_":
        header = header[1:]
        
    # overwrite any preexisting header
    outputheader = open(os.path.join(outdir, header), "w")
    outdocstring = open(os.path.join(outdir, basename + ".i"), "w")
    
    classes_in_header[header] = []
    input = inputfile.read()
    inputfile.close()
    
    # grab the docs and spit them out to another file, but in the 
    # header file, just remove the doc definitions.
    headertext = input
    docstringtext = ""
    
    headertext = DocDeclA_re.sub(replace_decl_str_in_header, headertext)
    headertext = DocDeclStr_re.sub(replace_decl_str_in_header, headertext)
    headertext = DocCtorStr_re.sub(replace_ctor_str_in_header, headertext)
    headertext = DocCtorAStr_re.sub(replace_ctor_str_in_header, headertext)
    headertext = DocCtorStrName_re.sub(replace_ctor_str_in_header, headertext)
    headertext = DocDeclAStr_re.sub(replace_decl_str_in_header, headertext)
    headertext = DocDeclStrName_re.sub(replace_decl_strname_in_header, headertext)
    headertext = DocDeclAStrName_re.sub(replace_decl_strname_in_header, headertext)
    headertext = DocDeclAName_re.sub(replace_decl_aname_in_header, headertext)
    headertext = DocAStr_re.sub(replace_empty, headertext)
    
    #headertext = pymacros_block1_re.sub(replace_bracketed_text, headertext)
    headertext = pymacros_rename_re.sub(replace_empty, headertext)
    headertext = pymacros_renamector_re.sub(replace_empty, headertext)
    headertext = pymacros_rename_small_re.sub(replace_empty, headertext)
    headertext = pymacros_constant_re.sub(replace_empty, headertext)
    headertext = pymacros_foopend_re.sub(replace_empty, headertext)
    headertext = pymacros_makebasefunc_re.sub(replace_empty, headertext)
    headertext = pymacros_typemap_re.sub(replace_empty, headertext)
    headertext = pymacros_musthaveapp_re.sub(replace_empty, headertext)
    headertext = pymacros_disownarg_re.sub(swigify_macro, headertext)
    headertext = pymacros_cleardisown_re.sub(swigify_macro, headertext)
    headertext = pymacros_immutable_re.sub(swigify_macro, headertext)
    headertext = pymacros_mutable_re.sub(swigify_macro, headertext)
    headertext = pymacros_nokwargs_re.sub(replace_empty, headertext)
    headertext = pymacros_inline_re.sub(replace_empty, headertext)
    headertext = pymacros_insert_re.sub(replace_empty, headertext)
    headertext = pymacros_pythoncode_re.sub(replace_empty, headertext)
    headertext = pymacros_pythoncode_string_re.sub(replace_empty, headertext)
    headertext = pymacros_property_re.sub(replace_empty, headertext)
    headertext = pymacros_apply_re.sub(replace_empty, headertext)
    headertext = pymacros_newobject_re.sub(replace_empty, headertext)
    headertext = pymacros_noautodoc_re.sub(replace_empty, headertext)
    
    # rename special cases
    headertext = headertext.replace("wxPyEmptyString", "wxEmptyString")
    headertext = headertext.replace("wxPyInputStream", "wxInputStream")
    headertext = headertext.replace("wxPyOutputStream", "wxOutputStream")
    headertext = headertext.replace("wxPyListCtrl", "wxListCtrl")
    headertext = headertext.replace("wxPyVListBox", "wxVListBox")
    headertext = headertext.replace("wxPyHtmlListBox", "wxHtmlListBox")
    headertext = headertext.replace("wxPyTreeCtrl", "wxTreeCtrl")
    headertext = headertext.replace("wxPyFontEnumerator", "wxFontEnumerator")
    headertext = headertext.replace("wxPyVScrolledWindow", "wxVScrolledWindow")
    headertext = headertext.replace("wxPyApp", "wxApp")
    headertext = headertext.replace("wxPyDropSource", "wxDropSource")
    headertext = headertext.replace("wxPyDropTarget", "wxDropTarget")
    headertext = headertext.replace("wxPyTextDropTarget", "wxTextDropTarget")
    headertext = headertext.replace("wxPyFileDropTarget", "wxFileDropTarget")
    headertext = headertext.replace("wxPyTaskBarIcon", "wxTaskBarIcon")
    headertext = headertext.replace("wxPyArtProvider", "wxArtProvider")
    headertext = headertext.replace("wxPyProcess", "wxProcess")
    headertext = headertext.replace("wxPyPopupTransientWindow", "wxPopupTransientWindow")
    headertext = headertext.replace("wxPyPrintout", "wxPrintout")
    headertext = headertext.replace("wxPyTimer", "wxTimer")
    headertext = headertext.replace("wxPyXmlResourceHandler", "wxXmlResourceHandler")
    headertext = headertext.replace("wxPyTreeItemData", "wxTreeItemData")
    headertext = headertext.replace("%newgroup;", "")
    headertext = headertext.replace("%newgroup", "")
    
    # get rid of useless stuff
    headertext = headertext.replace("// Not a %module\n", "")
    
    for match in DocDeclStr_re.findall(input):
        name = stripArgsFromFunction(match[2])
        text = """DocStr(%s, "%s", "%s"); \n\n""" % (name, match[3], match[4])
        docstringtext += text
        
    for match in DocDeclStrName_re.findall(input):
        docstringtext += """%s%s,%s,"%s","%s",%s);\n\n""" % match
    
    for match in DocDeclAStrName_re.findall(input):
        docstringtext += """%s%s,%s,"%s","%s",%s);\n\n""" % match

    for match in DocDeclAName_re.findall(input):
        docstringtext += """%s%s,%s,"%s",%s);\n\n""" % match
        
    for match in DocCtorStr_re.findall(input):
        docstringtext += """%s%s,"%s","%s");\n\n""" % match
        
    for match in DocCtorStrName_re.findall(input):
        docstringtext += """%s%s,"%s","%s",%s);\n\n""" % match
        #docstringtext += text
    #docstringtext = doc_decl_str_re.sub(replace_decl_str, headertext)
    
    #for match in pymacros_re.findall(input):
    #    print string.join(match, "")
        
    # now that we've removed docs that might trip up our class regex,
    # get a list of wx classes in the docs.
    for match in class_re.findall(headertext):
        classname = match[1].split(":")[0].strip()
        classname = classname.split(" ")[0].strip()
        
        if not classname.startswith("wx"):
            print "WARNING: found class %s with non wx prefix. SKipping it" % classname
        else:
            #print "Class %s in header %s" % (classname, header)
            classes_in_header[header].append(classname)
    
    headertext = DocStr_re.sub("", headertext)
    
    outputheader.write(headertext)
    outdocstring.write(docstringtext)




##
## the MAIN of this script
##
    
if __name__ == "__main__":
    if len(sys.argv) < 3:
        print "usage: %s <path to swig .i files> <path to wx HTML docs>" % os.path.basename(sys.argv[0])
        print "Pulls wx interface headers out of swig .i files, and generates new .i files for"
        print "use by wxPython. Output is stored in ./wx_interface."
        sys.exit(1)
    
    idir = sys.argv[1]
    outdir = "./wx_interface"
    if not os.path.exists(outdir):
        os.makedirs(outdir)
    
    # now, we parse the docs, and integrate the .i file into the docs
    docspath = sys.argv[2]
    if not os.path.isdir(docspath):
        # get default directory
        print "Please specify the directory where docs are located."
    
    classes_page = os.path.join(docspath, "wx_classref.html")
    print "docspath: %s" % (classes_page)
    if not os.path.exists(classes_page):
        sys.exit(1)
    
    func_page = os.path.join(docspath, "wx_functionsalphabetically.html")
    print "docspath: %s" % (func_page)
    if not os.path.exists(func_page):
        sys.exit(1)
    
    to_page = os.path.join(docspath, "wx_overviews.html")
    print "docspath: %s" % (to_page)
    if not os.path.exists(to_page):
        sys.exit(1)
    
    # now, parse the classes.
    print "parsing wx HTML docs..."
    classes = getClasses(classes_page)
    names = classes.keys()
    names.sort()
    
    # parse global functions
    functions = getFunctions(func_page)
    
    # parse topic overviews
    topicOverviews = getTO(to_page)
    
    headerkeys = classes_in_header.keys()
    headerkeys.sort()
    
    processed_classes = []
    not_recognized = []
    
    #print "List of recognized classes: %s" % names
    #print len(names)
    #sys.exit(1)
    
    if INJECT_MODE:
        # first, we split the headers and the .i file apart
        for ifile in glob.glob(os.path.join(idir, "_*.i")):
            #print "ifile = %s" % ifile
            if not os.path.basename(ifile) in ignore_ifiles:
                i_file_to_header_and_docstring_file(ifile, outdir)
        
        # reformat nicely the *.h files before injecting docs into them
        ##os.system("astyle -n -s4 wx_interface/*h") #  -- makes things worse
        
        # now inject docs
        for headerfile in headerkeys:
            headerpath = os.path.join(outdir, headerfile)
            afile = open(headerpath, "r")
            headertext = afile.read()
            afile.close()
            
            #if headerfile=='cmndlgs.h':
            print "injecting docs into headers for %s: %s" % (headerfile, "")
            ###headertext = class_re.sub(replace_class_in_header, headertext)
            
            while 1:
                matches = class_re.findall(headertext)
                
                ok = False
                for match in matches:
                    classname = match[1].split(":")[0].strip()
                    classname = classname.split(" ")[0].strip()
                    
                    if classname not in classes:
                        print "WARNING: %s is not in classes list" % classname
                        not_recognized.append(classname)
                        continue
                    if classname not in processed_classes:
                        ok = True
                        break
                    #else:
                        #print "WARNING: %s has already been processed" %classname
                
                if not ok:
                    break
                
                print "  found", classname
                
                # get the text ranging from the beginning of the class declaration
                # down to the end of the file
                line = match[0]+match[1]
                endpos = startpos = headertext.find(line)
                if startpos == -1:
                    print "ERROR: can't find %s" % line
                    sys.exit(1)
                    
                classtxt = headertext[startpos+len(line)+1:]
                endpos += len(line)+1
                
                if classtxt.find("{")>40:
                    print "ERROR; can't find start bracket"
                    sys.exit(1)
                    
                tmp = classtxt.find("{")+1
                classtxt = classtxt[tmp:]
                endpos += tmp
                
                # search the matching close bracket of this class decl
                nestlevel = 1
                for n in range(len(classtxt)):
                    if nestlevel==0:
                        break
                    c = classtxt[n]
                    if c=='{': nestlevel+=1
                    if c=='}': nestlevel-=1
                
                # now we've got the text belonging to the class
                classtxt = classtxt[:n-1]
                endpos += n+2
                
                # add class docs
                classdocs = classes[classname].asDoxygen() + "\n\n"
        
                if not line.endswith("\n"):
                    line += "\n"
        
                newclasstxt = "\n\n" + classdocs.strip() +"\n"+ line.strip() + "\n{\n" + \
                    inject_docs_into_header(classname, classtxt) + "\n};\n"
                
                #if classname=='wxUpdateUIEvent':
                    #print "classtxt:", classtxt
                    #print "\n\n\n\nnewclasstxt:", newclasstxt, "\n\n"
    
                # substitute classtxt with newclasstxt
                headertext = headertext[:startpos] + newclasstxt + headertext[endpos:]
                
                processed_classes.append(classname)
                #print "processed_classes:",processed_classes
    
            afile = open(headerpath, "w")
            afile.write(headertext)
            afile.close()
        
    
    # reformat the headers
    ###os.system("astyle -n -s4 wx_interface/*h")
     

        
    not_processed = set(classes).difference(set(processed_classes))
    #print "list of classes in HTML docs but NOT in SWIG headers (BIG PROBLEM): %s" % not_processed
    
    # for classes which were not in the SWIG headers, generate new headers
    for cn in not_processed:
        
        # by FM
        fname = classes[cn].inclusionFile
        #fname = cn.lower().replace(" ", "") + ".h"
        #if fname.startswith("wx"):
            #fname = fname[2:]
        
        dirname = "wx_interface/" + fname
        dirname = dirname[:dirname.rfind("/")]
        if not os.path.exists(dirname):
            if "<" in dirname or ">" in dirname:
                print "ERROR: invalid recognized include file name: ", dirname
                sys.exit(1)
            print "making dir", dirname
            os.makedirs(dirname)
        
        
        funcs=""
        funcs_list = classes[cn].methods.keys()
        funcs_list.sort()
        
        def doxifyFormatting(txt):
            txt = txt.replace("true", "@true")
            txt = txt.replace("@@true", "@true")
            txt = txt.replace("@c @true", "@true")
            txt = txt.replace("false", "@false")
            txt = txt.replace("@@false", "@false")
            txt = txt.replace("@c @false", "@false")
            txt = txt.replace("NULL", "@NULL")
            txt = txt.replace("@c @NULL", "@NULL")
            return txt
        
        # first process all ctors
        for mn in funcs_list:
            m=classes[cn].methods[mn]
            if m.isCtor:
                funcs += doxifyFormatting(m.asDoxygen()) + "\n"
                funcs += m.getPrototype() + "\n"
                funcs += "\n"
                documented_count += 1
        
        # now process all dtors
        for mn in funcs_list:
            m=classes[cn].methods[mn]
            if m.isDtor:
                funcs += doxifyFormatting(m.asDoxygen()) + "\n"
                funcs += m.getPrototype() + "\n"
                funcs += "\n"
                documented_count += 1
        
        # now process everything else
        for mn in funcs_list:
            m=classes[cn].methods[mn]
            if not m.isCtor and not m.isDtor:
                funcs += doxifyFormatting(m.asDoxygen()) + "\n"
                funcs += m.getPrototype() + "\n"
                funcs += "\n"
                documented_count += 1
        
        derived_from = ""
        if classes[cn].derivedFrom != []:
            derived_from = ": public " + classes[cn].derivedFrom[0]
        
        cdesc = doxifyFormatting(classes[cn].asDoxygen()).strip()
        
        if os.path.exists("wx_interface/" + fname):
            
            print "appending %s docs to the header %s" % (cn, fname)
        
            # append to the existing header
            txt = """

%s
class %s %s
{
public:
%s
};
""" % (cdesc, cn, derived_from, "    "+funcs.strip())

            afile = open("wx_interface/" + fname, "a+")
            afile.write(txt)
            afile.close()
        else:
            
            print "creating the header for %s as %s" % (cn, fname)
            
            # create a brand new header
            
            txt = """/////////////////////////////////////////////////////////////////////////////
// Name:        %s
// Purpose:     documentation for %s class
// Author:      wxWidgets team
// RCS-ID:      $Id$
// Licence:     wxWindows license
/////////////////////////////////////////////////////////////////////////////

%s
class %s %s
{
public:
%s
};
""" % (fname, cn, cdesc, cn, derived_from, "    "+funcs.strip() )
        
            afile = open("wx_interface/" + fname, "w")
            afile.write(txt)
            afile.close()
            
    
    if GFUNCTIONS==True:
        # now output global functions
        print "OUTPUTTING GLOBAL FUNCTIONS NOW"
    
        # for classes which were not in the SWIG headers, generate new headers
        touched_files = []
        for fn in functions:
            
            # by FM
            fname = functions[fn].inclusionFile
            #fname = cn.lower().replace(" ", "") + ".h"
            #if fname.startswith("wx"):
                #fname = fname[2:]
            
            dirname = "wx_interface/" + fname
            dirname = dirname[:dirname.rfind("/")]
            if not os.path.exists(dirname):
                print "making dir", dirname
                os.makedirs(dirname)
            
            txt = doxifyFormatting(functions[fn].asDoxygen()) + "\n"
            txt += functions[fn].getPrototype() + "\n"
            txt += "\n"
            
            # remove indentation
            txt = txt[4:]
            txt = txt.replace("\n    ", "\n")
            
            documented_count += 1
            
            if os.path.exists("wx_interface/" + fname):
                
                print "appending %s docs to the header %s" % (fn, fname)
                
                if fname not in touched_files:
                    touched_files.append(fname)
                    txt = """
    
    // ============================================================================
    // Global functions
    // ============================================================================
    
    """ + txt
                
                afile = open("wx_interface/" + fname, "a+")
                afile.write(txt)
                afile.close()
            else:
                
                print "creating the header for %s as %s" % (fn, fname)
                touched_files.append(fname)
                
                # create a brand new header
                
                txt = """/////////////////////////////////////////////////////////////////////////////
    // Name:        %s
    // Purpose:     documentation for global functions
    // Author:      wxWidgets team
    // RCS-ID:      $Id$
    // Licence:     wxWindows license
    /////////////////////////////////////////////////////////////////////////////
    
    %s
    """ % (fname, txt)
            
                afile = open("wx_interface/" + fname, "w")
                afile.write(txt)
                afile.close()
    
    
    if TOPIC_OVERVIEWS==True:
        # now generate topic overviews
        print "OUTPUTTING TOPIC OVERVIEWS NOW"
        
        topicOverviews=[]
        for to in topicOverviews:
    
            dirname = "overviews/" + to + ".h"
            if not os.path.exists("overviews"):
                os.makedirs("overviews")
            
            txt = doxifyFormatting(topicOverviews[to])
            print "creating the to for %s as %s" % (to, dirname)
                
            # create a brand new header
            
            txt = """/////////////////////////////////////////////////////////////////////////////
    // Name:        %s
    // Purpose:     topic overview
    // Author:      wxWidgets team
    // RCS-ID:      $Id$
    // Licence:     wxWindows license
    /////////////////////////////////////////////////////////////////////////////
    
    %s
    """ % (to, txt)
            
            afile = open(dirname, "w")
            afile.write(txt)
            afile.close()
        
        
        # generally there are big number of newlines attached...
        for file in glob.glob("wx_interface/*.h"):
            afile = open(file, "r")
            headertext = afile.read()
            afile.close()
            
            #separator = "//---------------------------------------------------------------------------\n\n"
            #headertext = headertext.replace("\n\n\n\n", "\n\n")
            #headertext = headertext.replace("\n\n\n\n", "\n\n")
            #headertext = headertext.replace("\n\n\n\n", "\n\n")
            #headertext = headertext.replace(separator + "\n\n", separator)
            
            headertext = headertext.replace("If the default size (-1, -1) is specified",
                                            "If wxDefaultSize is specified")
            headertext = headertext.replace("A value of -1 indicates a default value",
                                            "The value wxID_ANY indicates a default value")
            
            # don't know why these are left around:
            headertext = headertext.replace("</B> <B>", "")
            headertext = headertext.replace("&lt;", "<")
            headertext = headertext.replace("&gt;", ">")
                
            afile = open(file, "w")
            afile.write(headertext)
            afile.close()
    
    print "list of classes NOT in HTML docs but in SWIG headers (probably not meant to be documented): %s" % set(not_recognized)
    print "There were %d classes in HTML docs; %d were in SWIG headers; %d were generated" % (len(classes), len(processed_classes), len(not_processed))
    print "There were %d functions which had documentation added/generated." % documented_count
    print "There are %d functions that couldn't be found in the SWIG headers but are in the HTML docs." % (len(undocumented))
    
    #undocumented.sort()
    #afile = open(os.path.join(outdir, "unfound_functions.txt"), "w")
    #for func in undocumented:
        #afile.write(func + "\n")
    #afile.close()
    
    #print "There are %d functions where the docs likely have an incorrect method signature (HTML doc signature != SWIG header signature)." % (len(broken_sig))
    
    #broken_sig.sort()
    #afile = open(os.path.join(outdir, "broken_sig_functions.txt"), "w")
    #for func in broken_sig:
        #afile.write(func + "\n")
    #afile.close()

    #print classes.keys()
