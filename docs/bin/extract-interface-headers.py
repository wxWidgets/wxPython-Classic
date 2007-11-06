#!/usr/bin/python

import sys, os, re
import glob
from docparser.wxclasses import *
from docparser.wxhtmlparse import *

DocDeclStr_re = re.compile("""(DocDeclStr\()(.*?),\s*?(.*?)\s*?,\s*?"(.*?)"\s*?,\s*?"(.*?)"\s*?\);""", 
                    re.MULTILINE | re.DOTALL)
DocDeclAStr_re = re.compile("""(DocDeclAStr\()(.*?),\s*?(.*?)\s*?,\s*?"(.*?)"\s*?,\s*?"(.*?)"\s*?\);""", 
                    re.MULTILINE | re.DOTALL)
DocDeclAStrName_re = re.compile("""(DocDeclAStrName\()(.*?),\s*?(.*?)\s*?,\s*?"(.*?)"\s*?,\s*?"(.*?)"\s*?,\s*?(.*?)\s*?\);""", 
                    re.MULTILINE | re.DOTALL)


DocDeclStrName_re = re.compile("""(DocDeclStrName\()(.*?),\s*?(.*?)\s*?,\s*?"(.*?)"\s*?,\s*?"(.*?)",\s*?(.*?)\s*?\);""", 
                    re.MULTILINE | re.DOTALL)
DocDeclAName_re = re.compile("""(DocDeclAName\()(.*?),\s*?(.*?)\s*?,\s*?"(.*?)"\s*?,\s*?(.*?)\s*?\);""", 
                    re.MULTILINE | re.DOTALL)
DocStr_re = re.compile("""(DocStr\()\s*?(.*?)\s*?,\s*?"(.*?)"\s*?,\s*?"(.*?)"\s*?\);""", re.MULTILINE | re.DOTALL)
DocCtorStr_re = re.compile("""(DocCtorStr\()\s*?(.*?)\s*?,\s*?"(.*?)"\s*?,\s*?"(.*?)"\s*?\);""", re.MULTILINE | re.DOTALL)
DocCtorStrName_re = re.compile("""(DocCtorStrName\()\s*?(.*?)\s*?,\s*?"(.*?)"\s*?,\s*?"(.*?)"\s*?,\s*?(.*?)\s*?\);""", re.MULTILINE | re.DOTALL)

class_re = re.compile("""(^\s*?class )([^\;]*?)(\s*?{)(.*?)(};)""", re.MULTILINE | re.DOTALL)

classes_in_header = {}
classes = {}
ignore_ifiles = ["_defs.i", "_core_api.i"]
undocumented = []
broken_sig = []

def stripArgsFromFunction(name):
    parenspos = name.find("(")
    if parenspos != -1:
        name = name[0:parenspos]
        
    return name

def inject_docs_into_header(classname, text):
    global undocumented
    global broken_sig
    outtext = text
    classname = classname.strip()
    if classname in classes: 
        methods = classes[classname].methods
        for method in methods:
            type = "(void )"
            methodname = methods[method].name
            if len(methods[method].prototypes) > 0:
                x = HTMLStripper()
                x.feed(methods[method].prototypes[0][0].strip())
                type = x.get_fed_data()
                #type = type.replace("virtual ", "") # the virtual status isn't always reflected in interface headers
                type = "(" + type.replace("*", "\*") + " )"
            
            #pos = outtext.find(methodname)
            #if pos > -1:
            #    print "Found %s!" % methodname
            #    linestart = outtext.rfind("\n", 0, pos)
            #    print "pos = %d, linestart = %d" % (pos, linestart)
            #    indent = pos - linestart 
            #    print "indent is: %d" % indent
            #    outtext = outtext[:linestart-1] + "\n" + methods[method].asDoxygen(indent) + outtext[linestart:] 
            
            methodname = methodname.strip()
            methodregexstr = type + "(" + methodname + ")"
            
            methodregex = """(.*?)(\s*?)%s(.*?)""" % methodregexstr.replace(" ", "\s*?")
            #print "method is: %s, %s" % (classname, methodregex)
            regex = re.compile(methodregex, re.DOTALL)
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
                indent = len(result.group(2).split("\n")[-1])
                #print "indent is %d" % indent
                #outtext = result.group(1) + methods[method].asDoxygen(indent) + "\n" + result.group(2) + result.group(3) + result.group(4)
                # don't add the docs for all signatures
                outtext = regex.sub("\\1\\2\\n%s\\n\\n%s\\3\\4\\5" % (methods[method].asDoxygen(indent), " " * indent), outtext, count=1)            
            else:
                
                # try one more time to see if the method's there, but it's  got the wrong signature...
                methodregexstr = "(" + methodname + ")"
            
                methodregex = """(.*?)%s(.*?)""" % methodregexstr
                regex = re.compile(methodregex, re.DOTALL)
                result = regex.match(outtext)
                if result:
                    broken_sig.append(classname + "::" + methodname)
                else:
                    undocumented.append(classname + "::" + methodname)           
    
    return outtext
    
def replace_class_in_header(match):
    return match.group(1) + match.group(2) + match.group(3) + inject_docs_into_header(match.group(2).split(":")[0], match.group(4)) + match.group(5)

def replace_ctor_str_in_header(match):
    return match.group(2) + ";"
    
def replace_decl_str_in_header(match):
    return match.group(2) + " " + match.group(3) + ";"
    
def replace_decl_strname_in_header(match):
    return """%s %s;""" % (match.group(2), match.group(3))

def replace_decl_aname_in_header(match):
    return """%s %s;""" % (match.group(2), match.group(3))

def i_file_to_header_and_docstring_file(filename, outdir="."):
    global classes_in_header
    basename = os.path.splitext(os.path.basename(filename))[0]
    
    inputfile = open(filename, "r")
    header = basename + ".h"
    if header[0] == "_":
        header = header[1:]
    outputheader = open(os.path.join(outdir, header), "w")
    outdocstring = open(os.path.join(outdir, basename + ".i"), "w")
    
    classes_in_header[header] = []
    input = inputfile.read()
    inputfile.close()
    
    # grab the docs and spit them out to another file, but in the 
    # header file, just remove the doc definitions.
    headertext = input
    docstringtext = ""
    
    headertext = DocDeclStr_re.sub(replace_decl_str_in_header, headertext)
    headertext = DocCtorStr_re.sub(replace_ctor_str_in_header, headertext)
    headertext = DocCtorStrName_re.sub(replace_ctor_str_in_header, headertext)
    headertext = DocDeclAStr_re.sub(replace_decl_str_in_header, headertext)
    headertext = DocDeclStrName_re.sub(replace_decl_strname_in_header, headertext)
    headertext = DocDeclAStrName_re.sub(replace_decl_strname_in_header, headertext)
    headertext = DocDeclAName_re.sub(replace_decl_aname_in_header, headertext)
    
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
    
    # now that we've removed docs that might trip up our class regex,
    # get a list of wx classes in the docs.
    for match in class_re.findall(headertext):
        classname = match[1].split(":")[0].strip()
        print "Class %s in header %s" % (classname, header)
        classes_in_header[header].append(classname) 
    
    headertext = DocStr_re.sub("", headertext)
    
    outputheader.write(headertext)
    outdocstring.write(docstringtext)
    
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
    
    # first, we split the headers and the .i file apart
    for ifile in glob.glob(os.path.join(idir, "_*.i")):
        #print "ifile = %s" % ifile
        if not os.path.basename(ifile) in ignore_ifiles:
            i_file_to_header_and_docstring_file(ifile, outdir)

    # now, we parse the docs, and integrate the .i file into the docs
    docspath = sys.argv[2]
    if not os.path.isdir(docspath):
        # get default directory
        print "Please specify the directory where docs are located."
    
    classes_page = os.path.join(docspath, "wx_classref.html")
    print "docspath: %s" % (classes_page)
    if os.path.exists(classes_page):
        # now, parse the classes.
        print "parsing wx HTML docs..."
        classes = getClasses(classes_page)
        names = classes.keys()
        names.sort()
        
        for headerfile in classes_in_header.keys():
            headerpath = os.path.join(outdir, headerfile)
            afile = open(headerpath, "r")
            headertext = afile.read()
            afile.close()
            
            print "injecting docs into headers for %s" % headerfile
            headertext = class_re.sub(replace_class_in_header, headertext)
            
            afile = open(headerpath, "w")
            afile.write(headertext)
            afile.close()
            
        print "There are %d functions that couldn't be found in the headers." % (len(undocumented))
        
        undocumented.sort()
        afile = open(os.path.join(outdir, "unfound_functions.txt"), "w")
        for func in undocumented:
            afile.write(func + "\n")
        afile.close()
        
        print "There are %d functions where the docs likely have an incorrect method signature." % (len(broken_sig))
        
        broken_sig.sort()
        afile = open(os.path.join(outdir, "broken_sig_functions.txt"), "w")
        for func in broken_sig:
            afile.write(func + "\n")
        afile.close()
