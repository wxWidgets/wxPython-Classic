#!/usr/bin/python

import commands
import glob
import optparse
import os
import shutil
import string
import sys
import types

version = "2.8"

version_nodot = version.replace(".", "")

option_dict = { 
            "clean"     : (False, "Clean all files from build directories"),
            "debug"     : (False, "Build wxPython with debug symbols"),
            "reswig"    : (False, "Re-generate the SWIG wrappers"),
            "unicode"   : (False, "Build wxPython with unicode support"),
            "py_version": ("2.5", "Version of Python to build against"),
            "no_config" : (False, "Don't run configure when building."),
            "install"   : (False, "Install the built wxPython into installdir"),
            "install_dir": ("", "Directory to install wxPython to."),
            "build_dir" : ("", "Directory to store wx build files."),
          }

parser = optparse.OptionParser(usage="usage: %prog [options]", version="%prog 1.0")

for opt in option_dict:
    default = option_dict[opt][0]
    
    action = "store"
    if type(default) == types.BooleanType:
        action = "store_true"
    parser.add_option("--" + opt, default=default, action=action, dest=opt, help=option_dict[opt][1])

options, arguments = parser.parse_args()

pyversion_nodot = options.py_version.replace(".", "")

# for cleaning up
def deleteIfExists(deldir):
    if os.path.exists(deldir):
        shutil.rmtree(deldir)
        
def delFiles(fileList):
    for afile in fileList:
        os.remove(afile)

scriptDir = os.path.abspath(sys.path[0])
scriptName = os.path.basename(sys.argv[0])

WXWIN = os.path.abspath(os.path.join(scriptDir, ".."))
myenv = os.environ

if myenv.has_key("WXWIN"):
    WXWIN = myenv["WXWIN"]

# clean the wxPython build files, this part is platform-agnostic
# we do the platform-specific clean below.
if options.clean:
    deleteIfExists(os.path.join(scriptDir, "build"))    
    deleteIfExists(os.path.join(scriptDir, "build.unicode"))
        
    files = glob.glob(os.path.join(scriptDir, "wx", "*.pyd")) + \
            glob.glob(os.path.join(scriptDir, "wx", "*.so"))

    delFiles(files)

print "wxWidgets directory is: %s" % WXWIN

# TODO: Move the Windows build process to using build-wxwidgets.py
if sys.platform.startswith("win"):
    if not myenv.has_key("OSTYPE") or myenv["OSTYPE"] != "cygwin":
        print "ERROR: Must run this script from Cygwin."
        sys.exit(1)
        
    WXWIN_CYGPATH = commands.getoutput("cygpath %s" % WXWIN)

    if options.clean:
        for adir in glob.glob(os.path.join(WXWIN, "build", "msw", "vc_msw*")):
            deleteIfExists(adir)
    
        # TODO: test using .make with a clean argument
        dllDir = os.path.join(WXWIN, "lib", "vc_dll")
        if options.unicode:
            for adir in glob.glob(os.path.join(dllDir, "wxmsw" + version_nodot + "uh*")):
                deleteIfExists(adir)
                
            deleteIfExists(os.path.join(dllDir, "vc_mswuhdll"))            
        else:
            for adir in glob.glob(os.path.join(dllDir, "wxmsw" + version_nodot + "h*")):
                deleteIfExists(adir)
                
            deleteIfExists(os.path.join(dllDir, "vc_mswhdll"))

        delFiles(glob.glob(os.path.join(WXWIN, "lib", "*h.lib")))

      # do setup of build environment vars
    if not myenv.has_key("TOOLS"):
        myenv["TOOLS"] = os.system("cygpath C:\\\\")
    
    if not myenv.has_key("SWIGDIR"):
        myenv["SWIGDIR"] = os.path.join(myenv["TOOLS"], "SWIG-1.3.29")
    
    DEBUG_FLAG = ""
    UNICODE_FLAG = ""
    if options["debug"]:
        DEBUG_FLAG = "--debug"
    
    if options["unicode"]:
        UNICODE_FLAG = "UNICODE=1"

    # copy wxPython build scripts
    for script in glob.glob(os.path.join(WXWIN, "wxPython", "distrib", "msw", ".m*")):
        shutil.copyfile(script, os.path.join(WXWIN, "build", "msw"))
  
    os.chdir(os.path.join(WXWIN, "build", "msw"))

    UNI = ""
    if options.unicode:
        UNI = "-uni"
  
    retval = os.system("./.make hybrid" + UNI)
  
    if retval != 0:
        print "ERROR: failed building wxWidgets"
        sys.exit(retval)
  
    os.chdir(os.path.join(WXWIN, "wxPython"))

    # update the language files
    retval = os.system("python " + os.path.join(WXWIN, "wxPython", "distrib", "makemo.py"))
    
    if retval != 0:
        print "ERROR: failed generating language files"
        sys.exit(retval)
  
    # re-generate SWIG files
    if options.reswig:
        os.system("./b " + py_version + "t")
  
    # build the hybrid extension
    # NOTE: Win Python needs Windows-style pathnames, so we 
    # need to convert
    myenv["SWIGDIR"] = commands.getoutput("cygpath -w " + myenv["SWIGDIR"])
  
    # TODO: Currently the b script used here doesn't exit with
    # non-zero even if there's an error. Once it's been updated to do
    # so, make sure build-wxpython.sh exits with that same error code.
  
    os.system("./b " + pyversion_nodot + " h " + DEBUG_FLAG + " " + UNICODE_FLAG)

    dlls = glob.glob(os.path.join(dllDir, "*.dll"))
    for dll in dlls:
        shutil.copyfile(dll, os.path.join(WXWIN, "wxPython", "wx"))
  
else:
    WXPY_BUILD_DIR = os.path.join(os.getcwd(), "wxpy-bld")
    WXPY_INSTALL_DIR = os.path.join(os.environ["HOME"], "wxpython-" + version)
    
    if options.build_dir != "":
        WXPY_BUILD_DIR = options.build_dir
    
    if options.install_dir != "":
        WXPY_INSTALL_DIR = options.install_dir
        
    if options.clean:
        deleteIfExists(WXPY_BUILD_DIR)
        deleteIfExists(WXPY_INSTALL_DIR)
        sys.exit(0)

    build_options = []
    wxpy_build_options = []
    if options.unicode:
        build_options.append("--unicode")
        wxpy_build_options.append("UNICODE=1")
        
    if options.debug:
        build_options.append("--debug")
        
    if options.no_config:
        build_options.append("--no_config")

    if not os.path.exists(WXPY_BUILD_DIR):
        os.mkdir(WXPY_BUILD_DIR)
        
    os.chdir(WXPY_BUILD_DIR)
    build_options.append('--installdir="%s"' % WXPY_INSTALL_DIR)
    build_options.append("--install")
  
    retval = os.system(WXWIN + "/build/tools/build-wxwidgets.py --wxpython %s" % string.join(build_options, " "))
    if retval != 0:
        print "ERROR: failed building wxWidgets"
        sys.exit(1)
  
    USE_SWIG = 0
    SWIG_BIN = commands.getoutput("which swig")
    if options.reswig:
        if os.path.exists(SWIG_BIN):
            wxpy_build_options.append('SWIG_BIN="%s"' % SWIG_BIN)
        else:
            wxpy_build_options.append('SWIG_BIN="%s"' % os.path.join(SWIGDIR, "swig"))
            
        if os.path.exists(SWIG_BIN):
            wxpy_build_options.append("USE_SWIG=%d" % 1)
        else:
            wxpy_build_options.append("USE_SWIG=%d" % 0)
            print "WARNING: Unable to find SWIG binary. Not re-SWIGing files."

    build_mode = "build_ext --inplace"
    
    if options.install:
        build_mode = "install --install-headers=%s/include --root=%s --install-platlib=wxPython --install-scripts=wxPython --install-purelib=wxPython" % (WXPY_INSTALL_DIR, WXPY_INSTALL_DIR)

    os.chdir(scriptDir)
    command = "python ./setup.py %s WX_CONFIG=%s/bin/wx-config %s" % \
                (build_mode, WXPY_INSTALL_DIR, string.join(wxpy_build_options, " "))
    print command
    retval = os.system(command)
    
    if retval != 0:
        print "ERROR: failed building wxPython."
        sys.exit(retval)


print "------------ BUILD FINISHED ------------"
print ""
print "To run the wxPython demo:"
print ""
print "1) set your PYTHONPATH variable to $WXWIN."
print "2) run python demo/demo.py"
print ""

