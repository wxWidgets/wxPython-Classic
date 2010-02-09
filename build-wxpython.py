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

# Should we make this conditional?
if sys.platform.startswith("darwin"):
    os.environ["CXX"] = "g++-4.0"
    os.environ["CC"]  = "gcc-4.0"
    os.environ["CPP"] = "cpp-4.0"


def optionCleanCallback(option, opt_str, value, parser):
    if value is None:
        value = "all"
    if not value in ["all", "wx", "py", "pyext"]:
        raise optparse.OptionValueError("Invalid clean option")
    setattr(parser.values, option.dest, value)
    

option_dict = { 
    "clean"         : ("",    
                       "Clean files from build directories.  Default is all build files. "
                       "Specify 'wx' to clean just the wx build, 'py' for just the "
                       "wxPython build, and 'pyext' for just the built extension modules.", 
                       optionCleanCallback),
    "debug"         : (False, "Build wxPython with debug symbols"),
    "reswig"        : (False, "Allow SWIG to regenerate the wrappers"),
    "unicode"       : (True, "Build wxPython with unicode support (always on for wx2.9)"),
    "osx_cocoa"     : (False, "Build the OS X Cocoa port on Mac (experimental)"),
    "mac_lipo"      : (False, "EXPERIMENTAL: Create a universal binary by merging a PPC and Intel build together."),
    "mac_framework" : (False, "Build wxWidgets as a Mac framework."),
    "mac_universal_binary" : (False, "Build Mac version as a universal binary"),
    "force_config"  : (False, "Run configure when building even if the script determines it's not necessary."),
    "no_config"     : (False, "Turn off configure step on autoconf builds"),
    "prefix"        : ("/usr/local", "Prefix value to pass to the wx build."),
    "install"       : (False, "Install the built wxPython into installdir or standard location"),
    "installdir"    : ("", "Installation root for wxWidgets, files will go to {installdir}/{prefix}"),
    "build_dir"     : ("", "Directory to store wx build files. (Not used on Windows)"),
    "wxpy_installdir" : ("", "Installation root for wxPython, defaults to Python's site-packages."),
    "extra_setup"   : ("", "Extra args to pass on setup.py's command line."),
    "extra_make"    : ("", "Extra args to pass on [n]make's command line."),
}


options_changed = True
old_options = None
if os.path.exists("build-options.cache"):
    cache_file = open("build-options.cache")
    old_options = cPickle.load(cache_file)
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

# TODO: Instead of a simple compare we should allow for same args in different
# order to also match.  
if sys.argv[1:] == old_options:
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


scriptDir = os.path.abspath(sys.path[0])
scriptName = os.path.basename(sys.argv[0])
WXPYDIR = scriptDir

build_options = ['--wxpython']
wxpy_build_options = []

if os.environ.has_key("SWIG"):
    SWIG_BIN = os.environ["SWIG"]
elif sys.platform.startswith("win"):
    SWIG_BIN = 'C:\\SWIG-1.3.29\\swig.exe'
else:
    # WARNING: This is may not be the patched version of SWIG if the
    # user has installed a stock pacakge
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

    
if os.environ.has_key("WXWIN"):
    WXWIN = os.environ["WXWIN"]
else:
    if os.path.exists('../wxWidgets'):
        WXWIN = '../wxWidgets'  # assumes in parallel SVN tree
    else:
        WXWIN = '..'  # assumes wxPython is subdir
    WXWIN = os.path.abspath(os.path.join(WXPYDIR, WXWIN))
    

# Windows extension build stuff
build_type_ext = "h"
if options.debug:
    build_type_ext = "d"
    
dll_type = build_type_ext
if options.unicode:
    dll_type = "u" + dll_type

build_base = 'build'
if sys.platform.startswith("darwin"):
    if options.osx_cocoa:
        build_base += '.cocoa'
    else:
        build_base += '.carbon'
        
# Clean the wxPython build files and other things created or copied by previous builds.
# Cleaning of the wxWidgets build files is done below.
if options.clean in ['all', 'py']:
    if options.unicode:
        deleteIfExists(os.path.join(WXPYDIR, build_base + '.unicode'))            
    else:
        deleteIfExists(os.path.join(WXPYDIR, build_base))            
    
if options.clean in ['all', 'py', 'pyext']:
    files = glob.glob(os.path.join(WXPYDIR, "wx", "*.so"))
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
        port = "osx_carbon"
        if options.osx_cocoa:
            port = "osx_cocoa"
        WXPY_BUILD_DIR = WXPY_BUILD_DIR + "/" + port

    DESTDIR = options.installdir
    PREFIX = options.prefix
    if options.prefix:
        build_options.append('--prefix=%s' % options.prefix)
        
    if options.mac_framework and sys.platform.startswith("darwin"):
        # TODO:  Don't hard-code this path
        PREFIX = "/Library/Frameworks/wx.framework/Versions/%s" %  version2
    
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
    if options.mac_lipo and sys.platform.startswith("darwin"):
        blddir += '/bld-i386'
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

if options.mac_lipo and sys.platform.startswith("darwin"):
    build_options.append("--mac_lipo")
    
if not sys.platform.startswith("win"):
    # Change to what will be the wxWidgets build folder
    # (Note, this needs to be after any testing for file/path existance, etc.
    # because they may be specified as relative paths.)
    os.chdir(WXPY_BUILD_DIR)

try:
    # Import and run the wxWidgets build script
    wxscript = os.path.join(WXWIN, "build/tools/build-wxwidgets.py")
    sys.path.insert(0, os.path.dirname(wxscript))
    wxbuild = __import__('build-wxwidgets')
    print 'wxWidgets build options:', build_options
    wxbuild.main(wxscript, build_options)
except:
    print "ERROR: failed building wxWidgets"
    import traceback
    traceback.print_exc()
    sys.exit(1)

    
#-----------------------------------------------------------------------
# wxPython build

def doMacLipoBuild(arch, installDir, build_options, 
                   cxxcompiler="g++-4.0", cccompiler="gcc-4.0", target="10.4", flags=""):
    archInstallDir = installDir + "/" + arch
    old_env = dict(CXX = os.environ.get('CXX'),
                   CC = os.environ.get('CC'),
                   MACOSX_DEPLOYMENT_TARGET = os.environ.get('MACOSX_DEPLOYMENT_TARGET'),
                   )
    
    os.environ["CXX"] = "%s -arch %s %s" % (cxxcompiler, arch, flags)
    os.environ["CC"] = "%s -arch %s %s" % (cccompiler, arch, flags)
    os.environ["MACOSX_DEPLOYMENT_TARGET"] = target
    buildRoot = "bld-" + arch

    build_options.append("ARCH=" + arch)
    build_options.append("BUILD_BASE=bld-" + arch)
    build = 'build'
    if options.debug:
        build += " --debug"
    build_options.append('WX_CONFIG="%s/bin/wx-config --prefix=%s"' %
                              (WXPY_INSTALL_DIR, WXPY_INSTALL_DIR))
        
    cmd = "%s -u ./setup.py %s %s %s" % \
        (sys.executable, build, " ".join(build_options), options.extra_setup)
    exitIfError(runCmd(cmd), "ERROR: failed building wxPython for " + arch)

    cmd = "%s -u ./setup.py install --prefix=%s %s %s" % \
        (sys.executable, archInstallDir, " ".join(build_options), options.extra_setup)
    exitIfError(runCmd(cmd), "ERROR: failed installing wxPython for " + arch)

    for key, val in old_env.items():
        if val:
            os.environ[key] = val
        else:
            del os.environ[key]


def macFixDependencyInstallName(destdir, prefix, extension):
    pwd = os.getcwd()
    os.chdir(destdir+prefix+'/lib')
    dylibs = glob.glob('*.dylib')   
    for lib in dylibs:
        cmd = 'install_name_tool -change %s/lib/%s %s/lib/%s %s' % \
              (destdir+prefix,lib,  prefix,lib,  extension)
        print cmd
        os.system(cmd)        
    os.chdir(pwd)
    


if options.install:
    # only add the --prefix flag if we have an explicit request to do
    # so, otherwise let distutils install in the default location.
    install_dir = DESTDIR or PREFIX
    WXPY_PREFIX = ""
    if options.wxpy_installdir:
        install_dir = options.wxpy_installdir
        WXPY_PREFIX = "--prefix=%s" % options.wxpy_installdir
        
if options.mac_lipo and sys.platform.startswith("darwin"):
    os.chdir(WXPYDIR)
    doMacLipoBuild('ppc', install_dir, wxpy_build_options[:])
    doMacLipoBuild('i386', install_dir, wxpy_build_options[:])

    runCmd("python %s/distrib/scripts/mac/lipo-dir.py %s %s %s" %
           (WXWIN, install_dir + "/ppc", install_dir + "/i386", install_dir))
    
    shutil.rmtree(install_dir + "/ppc")
    shutil.rmtree(install_dir + "/i386")

else:    
    if sys.platform.startswith("win"):
        # Copy the wxWidgets DLLs to the wx Python pacakge folder
        dlls = glob.glob(os.path.join(dllDir, "wx*" + version2_nodot + dll_type + "*.dll")) + \
               glob.glob(os.path.join(dllDir, "wx*" + version3_nodot + dll_type + "*.dll")) 
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
        else:
            wxpy_build_options.append("WX_CONFIG=%s/wx-config" % WXPY_BUILD_DIR)
    
    os.chdir(WXPYDIR)
    command = sys.executable + " -u ./setup.py %s %s %s" % \
            (build_mode, " ".join(wxpy_build_options), options.extra_setup)
    exitIfError(runCmd(command), "ERROR: failed building wxPython.")

    if options.install:
        command = sys.executable + " -u ./setup.py install %s %s %s --record installed_files.txt" % \
                (WXPY_PREFIX, " ".join(wxpy_build_options), options.extra_setup)
        exitIfError(runCmd(command), "ERROR: failed installing wxPython.")

        if sys.platform.startswith("darwin") and DESTDIR:
            # Now that we are finished with the build fix the ids and
            # names in the wx .dylibs
            wxbuild.macFixupInstallNames(DESTDIR, PREFIX)

            # and also adjust the dependency names in the wxPython extensions
            for line in file("installed_files.txt"):
                line = line.strip()
                if line.endswith('.so'):
                    macFixDependencyInstallName(DESTDIR, PREFIX, line)
                    

        
# update the language files  TODO: this needs fixed...
command = sys.executable + " -u " + os.path.join(WXPYDIR, "distrib", "makemo.py")
exitIfError(runCmd(command), "ERROR: failed generating language files")


print "------------ BUILD FINISHED ------------"
print ""
print "To run the wxPython demo:"
print ""
print " - Set your PYTHONPATH variable to %s." % WXPYDIR
if not sys.platform.startswith("win") and not options.install:
    print " - Set your (DY)LD_LIBRARY_PATH to %s" % WXPY_BUILD_DIR + "/lib"
print " - Run python demo/demo.py"
print ""

