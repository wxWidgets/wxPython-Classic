#!/usr/bin/python

import commands
import cPickle
import glob
import optparse
import os
import shutil
import string
import sys
import types
import cfg_version as cfg

from distutils.dep_util  import newer


version2 = "%d.%d" % (cfg.VER_MAJOR, cfg.VER_MINOR) 
version3 = "%d.%d.%d" % (cfg.VER_MAJOR, cfg.VER_MINOR, cfg.VER_RELEASE)
version2_nodot = version2.replace(".", "")
version3_nodot = version3.replace(".", "")

CPU = os.environ.get('CPU', '')

scriptDir = os.path.abspath(sys.path[0])
scriptName = os.path.basename(sys.argv[0])
WXPYDIR = scriptDir

if os.environ.has_key("WXWIN"):
    WXWIN = os.environ["WXWIN"]
else:
    if os.path.exists('../wxWidgets'):
        WXWIN = '../wxWidgets'  # assumes in parallel SVN tree
    else:
        WXWIN = '..'  # assumes wxPython is in a subdir of wxWidgets
    WXWIN = os.path.abspath(os.path.join(WXPYDIR, WXWIN))

try:
    # Import the wxWidgets build script
    wxscript = os.path.join(WXWIN, "build/tools/build-wxwidgets.py")
    sys.path.insert(0, os.path.dirname(wxscript))
    wxbuild = __import__('build-wxwidgets')
except:
    print "Can't find or import %s/build/tools/build-wxwidgets.py, exiting." % WXWIN
    sys.exit(1)

    
def optionCleanCallback(option, opt_str, value, parser):
    if value is None:
        value = "all"
    if not value in ["all", "wx", "py", "pyext"]:
        raise optparse.OptionValueError("Invalid clean option")
    setattr(parser.values, option.dest, value)
    
    
    
# Set some default values for cmd-line options, to help keep the code below
# somewhat readable.
defJobs = str(wxbuild.numCPUs())
defFwPrefix = '/Library/Frameworks'
defPrefix = '/usr/local'

option_dict = { 
    "clean"         : ("",    
                       "Clean files from build directories.  Default is all build files. "
                       "Specify 'wx' to clean just the wx build, 'py' for just the "
                       "wxPython build, and 'pyext' for just the built extension modules.", 
                       optionCleanCallback),
    "debug"         : (False, "Build wxPython with debug symbols"),
    "reswig"        : (False, "Allow SWIG to regenerate the wrappers"),
    "jobs"          : (defJobs, "Number of make jobs to run at one time, if supported. Default: %s" % defJobs),
    "unicode"       : (True, "Build wxPython with unicode support (always on for wx2.9)"),
    "osx_cocoa"     : (False, "Build the OS X Cocoa port on Mac"),
    "osx_carbon"    : (True,  "Build the Carbon port on Mac (default)"),
    "mac_arch"      : ("", "Build just the specified architecture on Mac"),
    "mac_framework" : (False, "Build wxWidgets as a Mac framework."),
    "mac_framework_prefix" 
                    : (defFwPrefix, "Prefix where the framework should be installed. Default: %s" % defFwPrefix),    
    "mac_universal_binary" 
                    : (False, "Build Mac version as a universal binary"),
    "cairo"         : (False, "Enable dynamicly loading the Cairo lib for wxGraphicsContext on MSW"),
    "force_config"  : (False, "Run configure when building even if the script determines it's not necessary."),
    "no_config"     : (False, "Turn off wx configure step on autoconf builds"),
    "no_wxbuild"    : (False, "Turn off the wx build step (assumes that wx is already "
                              "built with the options and and in the location expected "
                              "based on the other flags."),
    "prefix"        : (defPrefix, "Prefix value to pass to the wx build. Default: %s" % defPrefix),
    "install"       : (False, "Install the built wxPython into installdir or standard location"),
    "installdir"    : ("", "Installation root for wxWidgets, files will go to {installdir}/{prefix}"),
    "build_dir"     : ("", "Directory to store wx build files. (Not used on Windows)"),
    "wxpy_installdir":("", "Installation root for wxPython, defaults to Python's site-packages."),
    "extra_setup"   : ("", "Extra args to pass on setup.py's command line."),
    "extra_make"    : ("", "Extra args to pass on [n]make's command line."),
}


options_changed = True
old_options = None
if os.path.exists("build-options.cache"):
    cache_file = open("build-options.cache")
    old_options = set(cPickle.load(cache_file))
    cache_file.close()

parser = optparse.OptionParser(usage="usage: %prog [options]", version="%prog 1.0")

keys = option_dict.keys()
keys.sort()
for opt in keys:
    default = option_dict[opt][0]
    action = "store"
    if type(default) == types.BooleanType:
        action = "store_true"
    if len(option_dict[opt]) > 2:
        # Even with the callback action we still have to workaround optparse's
        # checking for presense of a value or not. Check for a '=' and set
        # type accordingly.
        vtype = None
        for a in sys.argv:
            if a.startswith('--'+opt+'='):
                vtype = 'string'
                break
        parser.add_option("--" + opt, action='callback', type=vtype,
                          default=default, dest=opt, help=option_dict[opt][1],
                          callback=option_dict[opt][2], nargs=1)
    else:
        parser.add_option("--" + opt, default=default, action=action, 
                          dest=opt, help=option_dict[opt][1])
        
options, arguments = parser.parse_args()

# Compare current command line options to the saved set. If they match then we
# can save some time by skipping parts of the build.
if set(sys.argv[1:]) == old_options:
    options_changed = False
print "old_options = %r\nsys.argv = %r" % (old_options, sys.argv[1:]) 
cache_file = open("build-options.cache", "wb")
cPickle.dump(sys.argv[1:], cache_file)
cache_file.close()


#---------------------------------------------------------------------------
# Utility functions

def deleteIfExists(deldir, verbose=True):
    if os.path.exists(deldir) and os.path.isdir(deldir):
        if verbose:
            print "Removing folder: %s" % deldir
        shutil.rmtree(deldir)
        
def delFiles(fileList, verbose=True):
    for afile in fileList:
        if verbose:
            print "Removing file: %s" % afile
        os.remove(afile)


        
def runCmd(cmd):
    print '****', cmd
    return os.system(cmd)

def exitIfError(code, msg):
    if code != 0:
        print msg
        sys.exit(1)
        
#---------------------------------------------------------------------------


build_options = ['--wxpython', '--jobs=' + options.jobs]
wxpy_build_options = []

if os.environ.has_key("SWIG"):
    SWIG_BIN = os.environ["SWIG"]
elif sys.platform.startswith("win"):
    SWIG_BIN = 'C:\\SWIG-1.3.29\\swig.exe'
else:
    # WARNING: This is may not be the patched version of SWIG if the
    # user has installed a stock package
    SWIG_BIN = commands.getoutput("which swig")  
    
if options.reswig:
    if not os.path.exists(SWIG_BIN) and not sys.platform.startswith("win"):
        wxpy_build_options.append('SWIG="%s"' % "/opt/swig/bin/swig")
        
    if os.path.exists(SWIG_BIN):
        wxpy_build_options.append('SWIG="%s"' % SWIG_BIN)
        wxpy_build_options.append("USE_SWIG=%d" % 1)
    else:
        wxpy_build_options.append("USE_SWIG=%d" % 0)
        print "WARNING: Unable to find SWIG binary. Not re-SWIGing files."

# Windows extension build stuff
build_type_ext = ""
if options.debug:
    build_type_ext = "d"
    
dll_type = build_type_ext
if options.unicode:
    dll_type = "u" + dll_type

build_base = 'build'
if sys.platform.startswith("darwin"):
    if options.osx_cocoa:
        build_base += '/cocoa'
    else:
        build_base += '/carbon'
        
# Clean the wxPython build files and other things created or copied by previous builds.
# Cleaning of the wxWidgets build files is done below.
if options.clean in ['all', 'py']:
    if options.unicode:
        deleteIfExists(os.path.join(WXPYDIR, build_base + '.unicode'))            
    else:
        deleteIfExists(os.path.join(WXPYDIR, build_base))            
    
if options.clean in ['all', 'py', 'pyext']:
    files = glob.glob(os.path.join(WXPYDIR, "wx", "*.so"))
    files += glob.glob(os.path.join(WXPYDIR, "wx", "*.py"))
    files += glob.glob(os.path.join(WXPYDIR, "wx", "*.pyc"))
    if options.debug:
        files += glob.glob(os.path.join(WXPYDIR, "wx", "*_d.pyd"))
    else:
        allpyd = glob.glob(os.path.join(WXPYDIR, "wx", "*.pyd"))
        files += list( [pyd for pyd in allpyd if not pyd.endswith("_d.pyd")] )
        
    files += glob.glob(os.path.join(WXPYDIR, "wx", "wx*" + version2_nodot + dll_type + "*.dll")) 
    files += glob.glob(os.path.join(WXPYDIR, "wx", "wx*" + version3_nodot + dll_type + "*.dll")) 
    
    delFiles(files)

print "wxWidgets directory is: %s" % WXWIN

if sys.platform.startswith("win"):
    if CPU == 'AMD64':
        dllDir = os.path.join(WXWIN, "lib", "vc_amd64_dll")        
    else:
        dllDir = os.path.join(WXWIN, "lib", "vc_dll")
    buildDir = os.path.join(WXWIN, "build", "msw")
    
    if options.cairo:
        build_options.append("--cairo")
        if not os.environ.get("CAIRO_ROOT"):
            print "WARNING: Expected CAIRO_ROOT set in the environment!"

    if options.clean in ['all', 'wx']:    
        deleteIfExists(os.path.join(dllDir, "msw" + dll_type + ""))
        delFiles(glob.glob(os.path.join(dllDir, "wx*" + version2_nodot + dll_type + "*.*")))
        delFiles(glob.glob(os.path.join(dllDir, "wx*" + version3_nodot + dll_type + "*.*")))
        delFiles(glob.glob(os.path.join(dllDir, "*%s.*" % dll_type)))
        delFiles(glob.glob(os.path.join(dllDir, "*%s.*" % build_type_ext)))        
        deleteIfExists(os.path.join(buildDir, "vc_msw" + dll_type + "dll"))
        sys.exit(0)
    
          
else:
    WXPY_BUILD_DIR = os.path.join(os.getcwd(), "wxpy-bld")
    
    if options.build_dir != "":
        WXPY_BUILD_DIR = os.path.abspath(options.build_dir)

    if sys.platform.startswith("darwin"):
        port = "carbon"
        if options.osx_cocoa:
            port = "cocoa"
        WXPY_BUILD_DIR = os.path.join(WXPY_BUILD_DIR, port)

    DESTDIR = options.installdir
    PREFIX = options.prefix
    if options.prefix:
        build_options.append('--prefix=%s' % options.prefix)
    
    if options.clean in ['all', 'wx']:
        deleteIfExists(WXPY_BUILD_DIR)
    if options.clean in ['all', 'py'] and options.wxpy_installdir:
        deleteIfExists(options.wxpy_installdir)
    if options.clean:
        sys.exit(0)

    if not os.path.exists(WXPY_BUILD_DIR):
        os.makedirs(WXPY_BUILD_DIR)
        
    if options.mac_universal_binary:
        build_options.append("--mac_universal_binary")
    if  options.mac_arch: 
        build_options.append("--mac_arch=%s" % options.mac_arch)
        wxpy_build_options.append("ARCH=%s" % options.mac_arch)


# now that we've done platform setup, start the common build process
if options.unicode:
    build_options.append("--unicode")
    wxpy_build_options.append("UNICODE=1")
    
if options.debug:
    build_options.append("--debug")

if options.extra_make:
    build_options.append('--extra_make="%s"' % options.extra_make)
    
    
# Only disable configure if we don't need it
if not sys.platform.startswith("win") and options.no_config:
    build_options.append("--no_config")
    
elif ( not sys.platform.startswith("win") and 
     not options.force_config and 
     not options_changed ):

    dependencies = [ os.path.join(WXWIN, 'Makefile.in'),
                     os.path.join(WXWIN, 'configure'),
                     os.path.join(WXWIN, 'setup.h.in'),
                     os.path.join(WXWIN, 'version-script.in'),
                     os.path.join(WXWIN, 'wx-config.in'),
                     ]
    blddir = WXPY_BUILD_DIR
    for dep in dependencies:
        if newer(dep, os.path.join(blddir, "Makefile")):
            break
    else:
        build_options.append("--no_config")

if sys.platform.startswith("darwin") and options.osx_cocoa:
    build_options.append("--osx_cocoa")
    wxpy_build_options.append("WXPORT=osx_cocoa")

if not sys.platform.startswith("win") and options.install:
    build_options.append('--installdir=%s' % DESTDIR)
    build_options.append("--install")

if options.mac_framework and sys.platform.startswith("darwin"):
    build_options.append("--mac_framework")
    build_options.append("--mac_framework_prefix=%s" % options.mac_framework_prefix)
    
    # We'll automatically add the --install option because for the wxPython
    # build to be able to use the framework it must be fully constructed.
    if "--install" not in build_options:
        build_options.append("--install")

    PREFIX = wxbuild.getPrefixInFramework(options, WXWIN)
    
        
if not sys.platform.startswith("win"):
    build_options.append('--builddir=%s' % WXPY_BUILD_DIR)
    


if options.no_wxbuild:
    print 'Skipping wxWidgets build, assuming it is already done.'
else:
    try:
        print 'wxWidgets build options:', build_options
        wxbuild.main(wxscript, build_options)
    except:
        print "ERROR: failed building wxWidgets"
        import traceback
        traceback.print_exc()
        sys.exit(1)

    
#-----------------------------------------------------------------------
# wxPython build


def macFixupInstallNames2(destprefix, # prefix where the files are currently located
                          instprefix, # prefix to write into the files
                          oldprefix   # the prefix to be replaced, defaults to destprefix 
                         ):
    print "**** macFixupInstallNames2(%s, %s, %s)" % ( destprefix, instprefix, oldprefix)
    pwd = os.getcwd()
    os.chdir(destprefix+'/lib')
    dylibs = glob.glob('*.dylib')     # ('*[0-9].[0-9].[0-9].[0-9]*.dylib')
    for lib in dylibs:
        if not os.path.islink(lib):
            cmd = 'install_name_tool -id %s/lib/%s     %s/lib/%s' % \
                                  (instprefix,lib,  destprefix,lib)
            runCmd(cmd)

            for dep in dylibs:
                if not os.path.islink(dep):
                    cmd = 'install_name_tool -change %s/lib/%s   %s/lib/%s   %s/lib/%s' % \
                                 (oldprefix,dep,    instprefix,dep,    destprefix,lib)
                    runCmd(cmd)
    os.chdir(pwd)
    

def macFixDependencyInstallName(destdir, prefix, extension, buildDir):
    print "**** macFixDependencyInstallName(%s, %s, %s, %s)" % (destdir, prefix, extension, buildDir)
    pwd = os.getcwd()
    os.chdir(destdir+prefix+'/lib')
    dylibs = glob.glob('*.dylib')   
    for lib in dylibs:
        cmd = 'install_name_tool -change %s/lib/%s %s/lib/%s %s' % \
              (destdir+prefix,lib,  prefix,lib,  extension)
        #cmd = 'install_name_tool -change %s/lib/%s %s/lib/%s %s' % \
        #      (buildDir,lib,  prefix,lib,  extension)
        runCmd(cmd)        
    os.chdir(pwd)
    


if options.install:
    # only add the --prefix flag if we have an explicit request to do
    # so, otherwise let distutils install in the default location.
    install_dir = DESTDIR or PREFIX
    WXPY_PREFIX = ""
    if options.wxpy_installdir:
        install_dir = options.wxpy_installdir
        WXPY_PREFIX = "--prefix=%s" % options.wxpy_installdir
        

if sys.platform.startswith("win"):
    # Copy the wxWidgets DLLs to the wxPython package folder
    dlls = glob.glob(os.path.join(dllDir, "wx*" + version2_nodot + dll_type + "*.dll")) + \
           glob.glob(os.path.join(dllDir, "wx*" + version3_nodot + dll_type + "*.dll")) 

    # Also copy the cairo DLLs if needed
    if options.cairo:
        dlls += glob.glob(os.path.join(os.environ['CAIRO_ROOT'], 'bin', '*.dll'))

    for dll in dlls:
        shutil.copyfile(dll, os.path.join(WXPYDIR, "wx", os.path.basename(dll)))


wxpy_build_options.append("BUILD_BASE=%s" % build_base)
build_mode = "build_ext --inplace"
if options.install:
    build_mode = "build"
if options.debug:
    build_mode += " --debug"

        
if not sys.platform.startswith("win"):
    if options.install:
        wxlocation = DESTDIR + PREFIX
        print '-='*20
        print 'DESTDIR:', DESTDIR
        print 'PREFIX:', PREFIX
        print 'wxlocation:', wxlocation
        print '-='*20
        wxpy_build_options.append('WX_CONFIG="%s/bin/wx-config --prefix=%s"' %
                                  (wxlocation, wxlocation))
        
    elif options.mac_framework:
        wxpy_build_options.append("WX_CONFIG=%s/bin/wx-config" % PREFIX)        
    
    else:
        wxpy_build_options.append("WX_CONFIG=%s/wx-config" % WXPY_BUILD_DIR)

os.chdir(WXPYDIR)


if options.install and sys.platform.startswith("darwin") and DESTDIR:
    # Adjust the install_names in the wx libs so we can link with
    # the wx binaries in their temporary DESTDIR location
    macFixupInstallNames2(DESTDIR+PREFIX, DESTDIR+PREFIX, PREFIX)


command = sys.executable + " -u ./setup.py %s %s %s" % \
        (build_mode, " ".join(wxpy_build_options), options.extra_setup)
exitIfError(runCmd(command), "ERROR: failed building wxPython.")

if options.install:
    command = sys.executable + " -u ./setup.py install %s %s %s --record installed_files.txt" % \
            (WXPY_PREFIX, " ".join(wxpy_build_options), options.extra_setup)
    exitIfError(runCmd(command), "ERROR: failed installing wxPython.")

    if sys.platform.startswith("darwin") and DESTDIR:
        # Now that we are finished with the build fix the ids and
        # dependency names in the wx libs
        macFixupInstallNames2(DESTDIR+PREFIX, PREFIX, DESTDIR+PREFIX)

        # and also adjust the dependency names in the wxPython extensions
        for line in file("installed_files.txt"):
            line = line.strip()
            if line.endswith('.so'):
                macFixDependencyInstallName(DESTDIR, PREFIX, line, WXPY_BUILD_DIR)
                

        
# update the language files  TODO: this needs fixed...
command = sys.executable + " -u " + os.path.join(WXPYDIR, "distrib", "makemo.py")
exitIfError(runCmd(command), "ERROR: failed generating language files")


print "------------ BUILD FINISHED ------------"
print ""
print "To run the wxPython demo you may need to:"
print " - set your PYTHONPATH variable to %s" % WXPYDIR
if options.mac_framework:
    print " - set your DYLD_FRAMEWORK_PATH to %s" % os.path.abspath(options.mac_framework_prefix)
elif sys.platform.startswith("darwin"):
    print " - set your DYLD_LIBRARY_PATH to %s" % WXPY_BUILD_DIR + "/lib"
elif not sys.platform.startswith("win") and not options.install:
    print " - set your LD_LIBRARY_PATH to %s" % WXPY_BUILD_DIR + "/lib"
print "\nAnd then:"
print " - Run python demo/demo.py"
print ""

