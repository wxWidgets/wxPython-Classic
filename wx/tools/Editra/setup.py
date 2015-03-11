#!/usr/bin/env python
###############################################################################
# Name: setup.py                                                              #
# Purpose: Setup/build script for Editra                                      #
# Author: Cody Precord <cprecord@editra.org>                                  #
# Copyright: (c) 2008-2013 Cody Precord <staff@editra.org>                    #
# License: wxWindows License                                                  #
###############################################################################

"""
 Editra Setup Script

 USAGE:

   1) Windows:
      - python setup.py py2exe

   2) MacOSX:
      - python setup.py py2app

   3) Boil an Egg
      - python setup.py bdist_egg

   4) Install as a python package
      - python setup.py install
            - '--no-clean' can be specified to skip old file cleanup

 @summary: Used for building the editra distribution files and installations

"""
__author__ = "Cody Precord <cprecord@editra.org>"
__svnid__ = "$Id$"
__revision__ = "$Revision$"

#---- Imports ----#
import os
import sys
import glob
import shutil
import zipfile
import time
import src.info as info
import src.syntax.synextreg as synextreg # So we can get file extensions

# Version Check(s)
if sys.version_info < (2, 5):
    sys.stderr.write("[ERROR] Not a supported Python version. Need 2.5+\n")
    sys.exit(1)

try:
    import wx
except ImportError:
    if 'bdist_egg' not in sys.argv:
        sys.stderr.write("[ERROR] wxPython2.8 is required.\n")
        sys.exit(1)
else:
    if wx.VERSION < (2, 8, 8):
        sys.stderr.write("[ERROR] wxPython 2.8.8+ is required.\n")
        sys.exit(1)

#---- System Platform ----#
__platform__ = os.sys.platform

#---- Global Settings ----#
APP = ['src/Editra.py']
AUTHOR = "Cody Precord"
AUTHOR_EMAIL = "staff@editra.org"
YEAR = 2013

CLASSIFIERS = [
            'Development Status :: 3 - Alpha',
            'Environment :: MacOS X',
            'Environment :: Win32 (MS Windows)',
            'Environment :: X11 Applications :: GTK',
            'Intended Audience :: Developers',
            'Intended Audience :: Information Technology',
            'Intended Audience :: End Users/Desktop',
            'License :: OSI Approved',
            'Natural Language :: English',
            'Natural Language :: Chinese (Simplified)',
            'Natural Language :: Chinese (Traditional)',
            'Natural Language :: Croatian',
            'Natural Language :: Czech',
            'Natural Language :: Danish',
            'Natural Language :: Dutch',
            'Natural Language :: French',
            'Natural Language :: Hungarian',
            'Natural Language :: German',
            'Natural Language :: Italian',
            'Natural Language :: Latvian',
            'Natural Language :: Japanese',
            'Natural Language :: Norwegian',
            'Natural Language :: Polish',
            'Natural Language :: Portuguese (Brazilian)',
            'Natural Language :: Romanian',
            'Natural Language :: Russian',
            'Natural Language :: Serbian',
            'Natural Language :: Slovak',
            'Natural Language :: Slovenian',
            'Natural Language :: Spanish',
            'Natural Language :: Swedish',
            'Natural Language :: Turkish',
            'Operating System :: MacOS :: MacOS X',
            'Operating System :: Microsoft :: Windows',
            'Operating System :: POSIX',
            'Programming Language :: Python',
            'Topic :: Software Development',
            'Topic :: Text Editors'
            ]

def GenerateBinPackageFiles():
    """Generate the list of files needed for py2exe/py2app package files"""
    data = [("include/python2.5",
               glob.glob("include/python2.5/%s/*" % __platform__)),
              ("pixmaps/theme/Default", ["pixmaps/theme/Default/README"]),
              ("pixmaps/theme/Tango",["pixmaps/theme/Tango/AUTHORS",
                                      "pixmaps/theme/Tango/COPYING"]),
              ("pixmaps/theme/Tango/toolbar",
               glob.glob("pixmaps/theme/Tango/toolbar/*.png")),
              ("pixmaps/theme/Tango/menu",
               glob.glob("pixmaps/theme/Tango/menu/*.png")),
              ("pixmaps/theme/Tango/mime",
               glob.glob("pixmaps/theme/Tango/mime/*.png")),
              ("pixmaps/theme/Tango/other",
               glob.glob("pixmaps/theme/Tango/other/*.png")),
              ("styles", glob.glob("styles/*.ess")),
              ("ekeys", glob.glob("ekeys/*.ekeys")),
              ("tests/syntax", glob.glob("tests/syntax/*")),
              ("docs", glob.glob("docs/*.txt")), "AUTHORS", "FAQ", "INSTALL",
              "README","CHANGELOG","COPYING", "NEWS", "THANKS", "TODO",
              "setup.cfg"
            ]

    # Get the locale files
    for loc_dir in os.listdir("locale"):
        tmp = "locale/" + loc_dir + "/LC_MESSAGES"
        if os.path.isdir(tmp):
            tmp2 = tmp + "/Editra.mo"
            if os.path.exists(tmp2):
                data.append((tmp, [tmp2]))

    # Only bundle the plugins for the running version of python being used for
    # the build.
    data.append(("plugins",
                 glob.glob("plugins/*py%d.%d.egg" % sys.version_info[:2])))

    # Get platform specific icons
    pixlist = ["pixmaps/editra.png", "pixmaps/editra_doc.png"]

    if "darwin" in sys.platform:
        data.append("pixmaps/editra_doc.icns")
        pixlist.extend(["pixmaps/editra.icns", "pixmaps/editra_doc.icns"])
    elif sys.platform.startswith("win"):
        data.extend(glob.glob("include/windows/*.*"))
        pixlist.append("pixmaps/editra.ico")

    data.append(("pixmaps", pixlist))

    return data

def GenerateSrcPackageFiles():
    """Generate the list of files to include in a source package dist/install"""
    data = [ "src/*.py", "src/syntax/*.py", "src/autocomp/*.py", 
             "src/eclib/*.py", "docs/*.txt", "pixmaps/*.png", "pixmaps/*.ico",
             "src/ebmlib/*.py",
             "ekeys/*.ekeys",
             "Editra",
             "src/extern/*.py",
             "src/extern/aui/*.py",
             "src/extern/dexml/*.py",
             "src/extern/pygments/*.py",
             "src/extern/pygments/formatters/*.py",
             "src/extern/pygments/filters/*.py",
             "src/extern/pygments/lexers/*.py",
             "src/extern/pygments/styles/*.py",
             "pixmaps/*.icns",
             "pixmaps/theme/Default/README",
             "pixmaps/theme/Tango/AUTHOR",
             "pixmaps/theme/Tango/COPYING",
             "pixmaps/theme/Tango/toolbar/*.png",
             "pixmaps/theme/Tango/menu/*.png",
             "pixmaps/theme/Tango/mime/*.png",
             "pixmaps/theme/Default/README",
             "pixmaps/theme/Tango/other/*.png",
             "styles/*.ess", "tests/syntax/*",
             "AUTHORS", "CHANGELOG","COPYING", "FAQ", "INSTALL", "NEWS", 
             "README", "THANKS", "TODO", "setup.cfg" ]

    # Get the local files
    for loc_dir in os.listdir("locale"):
        tmp = "locale/" + loc_dir
        if os.path.isdir(tmp):
            tmp = tmp + "/LC_MESSAGES/Editra.mo"
            if os.path.exists(tmp):
                data.append(tmp)

    # NOTE: plugins selected to package in build step
    
    return data


DESCRIPTION = "Developer's Text Editor"

LONG_DESCRIPT = \
r"""
========
Overview
========
Editra is a multi-platform text editor with an implementation that focuses on
creating an easy to use interface and features that aid in code development.
Currently it supports syntax highlighting and variety of other useful features
for over 70 programing languages. For a more complete list of features and
screenshots visit the projects homepage at `Editra.org
<http://www.editra.org/>`_.

============
Dependencies
============
  * Python 2.6+
  * wxPython 2.8.3+ (Unicode build suggested)
  * setuptools 0.6+

"""

ICON = { 'Win' : "pixmaps/editra.ico",
         'WinDoc' : "pixmaps/editra_doc.ico",
         'Mac' : "pixmaps/Editra.icns"
}

# Explicitly include some libraries that are either loaded dynamically
# or otherwise not able to be found by py2app/exe
INCLUDES = ['syntax.*', 'ed_bookmark', 'ed_log', 'shutil', 'subprocess', 'zipfile',
            'pygments.*', 'pygments.lexers.*', 'pygments.formatters.*',
            'pygments.filters.*', 'pygments.styles.*', 'ftplib', 'xmlrpclib',
            'hmac', 'SimpleXMLRPCServer', 'SocketServer', 'commands', 
            'BaseHTTPServer', 'wx.gizmos', 'wx.lib.intctrl',
            'extern.flatnotebook'] # temporary till all references can be removed
if sys.platform.startswith('win'):
    INCLUDES.extend(['ctypes', 'ctypes.wintypes'])
else:
    INCLUDES.extend(['pty', 'tty'])

LICENSE = "wxWindows"

NAME = "Editra"

URL = "http://editra.org"

VERSION = info.VERSION

MANIFEST_TEMPLATE = """
<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<assembly xmlns="urn:schemas-microsoft-com:asm.v1" manifestVersion="1.0">
  <assemblyIdentity
    version="5.0.0.0"
    processorArchitecture="x86"
    name="%(prog)s"
    type="win32"
  />
  <description>%(prog)s</description>
  <trustInfo xmlns="urn:schemas-microsoft-com:asm.v3">
    <security>
      <requestedPrivileges>
        <requestedExecutionLevel
            level="asInvoker"
            uiAccess="false">
        </requestedExecutionLevel>
      </requestedPrivileges>
    </security>
  </trustInfo>
  <dependency>
    <dependentAssembly>
      <assemblyIdentity
            type="win32"
            name="Microsoft.VC90.CRT"
            version="9.0.21022.8"
            processorArchitecture="x86"
            publicKeyToken="1fc8b3b9a1e18e3b">
      </assemblyIdentity>
    </dependentAssembly>
  </dependency>
  <dependency>
    <dependentAssembly>
        <assemblyIdentity
            type="win32"
            name="Microsoft.Windows.Common-Controls"
            version="6.0.0.0"
            processorArchitecture="X86"
            publicKeyToken="6595b64144ccf1df"
            language="*"
        />
    </dependentAssembly>
  </dependency>
</assembly>
"""

RT_MANIFEST = 24
#---- End Global Settings ----#


#---- Packaging Functions ----#

def BuildPy2Exe():
    """Generate the Py2exe files"""
    from distutils.core import setup
    try:
        import py2exe
    except ImportError:
        print "\n!! You dont have py2exe installed. !!\n"
        exit()

    # put package on path for py2exe
    sys.path.append(os.path.abspath('src/'))
    sys.path.append(os.path.abspath('src/extern'))

    DATA_FILES = GenerateBinPackageFiles()
    try:
        import enchant
    except ImportError:
        pass
    else:
        from enchant import utils as enutil
        DATA_FILES += enutil.win32_data_files()

    setup(
        name = NAME,
        version = VERSION,
        options = {"py2exe" : {"compressed" : 1,
                               "optimize" : 1,
                               "bundle_files" : 2,
                               "includes" : INCLUDES,
                               "excludes" : ["Tkinter", "Tkconstants", "tcl"],
                               "dll_excludes": [ "MSVCP90.dll",
                                                 "tk85.dll",
                                                 "tcl85.dll" ] }},
        windows = [{"script": "src/Editra.py",
                    "icon_resources": [(1, ICON['Win'])],
                    "other_resources" : [(RT_MANIFEST, 1,
                                          MANIFEST_TEMPLATE % dict(prog=NAME))],
                  }],
        description = NAME,
        author = AUTHOR,
        author_email = AUTHOR_EMAIL,
        maintainer = AUTHOR,
        maintainer_email = AUTHOR_EMAIL,
        license = LICENSE,
        url = URL,
        data_files = DATA_FILES,
        )
    shutil.copy2(".\\editra-installer.nsi", ".\\dist\\editra-installer.nsi")

def BuildOSXApp():
    """Build the OSX Applet"""
    # Check for setuptools and ask to download if it is not available
    import src.extern.ez_setup as ez_setup
    ez_setup.use_setuptools()
    from setuptools import setup

    CleanBuild()
    fextents = synextreg.GetFileExtensions()
    fextents.append("*")
    PLIST = dict(CFBundleName = info.PROG_NAME,
             CFBundleIconFile = 'Editra.icns',
             CFBundleShortVersionString = info.VERSION,
             CFBundleGetInfoString = info.PROG_NAME + " " + info.VERSION,
             CFBundleExecutable = info.PROG_NAME,
             CFBundleIdentifier = "org.editra.%s" % info.PROG_NAME.title(),
             CFBundleDocumentTypes = [dict(CFBundleTypeExtensions=fextents,
                                           CFBundleTypeIconFile='editra_doc',
                                           CFBundleTypeRole="Editor"
                                          ),
                                     ],
             CFBundleTypeMIMETypes = ['text/plain',],
             CFBundleDevelopmentRegion = 'English',
# TODO Causes errors with the system menu translations and text rendering
#             CFBundleLocalizations = ['English', 'Spanish', 'French', 'Japanese'],
#             ['de_DE', 'en_US', 'es_ES', 'fr_FR',
#                                      'it_IT', 'ja_JP', 'nl_NL', 'nn_NO',
#                                      'pt_BR', 'ru_RU', 'sr_SR', 'tr_TR',
#                                      'uk_UA', 'zh_CN'],
       #      NSAppleScriptEnabled="YES",
             NSHumanReadableCopyright = u"Copyright %s 2005-%d" % (AUTHOR, YEAR)
             )

    PY2APP_OPTS = dict(iconfile = ICON['Mac'],
                       argv_emulation = True,
                       optimize = True,
                       includes = INCLUDES,
                       plist = PLIST)

    # Add extra mac specific files
    DATA_FILES = GenerateBinPackageFiles()
    DATA_FILES.append("scripts/editramac.sh")

    # Put extern package on path for py2app
    sys.path.append(os.path.abspath('src/extern'))

    setup(
        app = APP,
        version = VERSION,
        options = dict( py2app = PY2APP_OPTS),
        description = DESCRIPTION,
        author = AUTHOR,
        author_email = AUTHOR_EMAIL,
        maintainer = AUTHOR,
        maintainer_email = AUTHOR_EMAIL,
        license = LICENSE,
        url = URL,
        data_files = DATA_FILES,
        setup_requires = ['py2app'],
        )

    CreateDMG(VERSION)

def CreateDMG(version):
    """Create an OSX DMG
    @param version: version number string
    @todo: cleanup and generalize

    """
    Log("Creating DMG for osx installer...")

    assert os.path.exists('dist')
    os.chdir('dist')
    vname = "Editra-%s" % version
    fname = vname + ".dmg"
    mpath = "/Volumes/Editra-%s" % version
    comp = "Editra-%s_2.dmg" % version

    if os.path.exists("dist/%s" % fname):
        Log("Found image from previous running")
        os.remove("dist/%s" % fname)

    # Create the temporary image
    Log("Creating disk image...")
    os.system("hdiutil create -size 75m -fs HFS+ -volname %s %s" % (vname, fname))
    Log("Mounting disk image...")
    os.system("hdiutil mount %s" % fname) # Mount the image

    # Move installation files to the new image
    Log("Copying installation files to installer image...")
    if not os.path.exists(mpath + "/.bk"):
        os.mkdir(mpath + "/.bk")
    shutil.copy2("../pixmaps/installer/inst_bk.png", mpath + "/.bk/inst_bk.png")
    os.system("ditto -rsrcFork Editra.app %s/Editra.app" % mpath)
    
    Log("Configuring Finder View Options...")
#    shutil.copy2("../scripts/installer/INSTALLER_DS_Store", mpath + "/.DS_Store")
#    os.chmod(mpath + "/.DS_Store", 777)
    f = open("tmpscript", 'w')
    f.write(APPLE_SCRIPT % vname)
    f.close()
    status = os.system("osascript tmpscript")
    os.remove("tmpscript")
    Log("Applescript return status: %d" % status)

    # Unmount the image
    Log("Unmounting the installer image...")
    os.system("hdiutil eject %s" % mpath)

    # Create the compressed image
    Log("Converting the disk image to a compressed format...")
    os.system("hdiutil convert %s -format UDZO -imagekey zlib-level=9 -o %s" % (fname, comp))

    # Cleanup
    Log("Cleaning up temporary installer build files...")
    os.remove(fname)
    os.rename(comp, fname)

# Template for controlling some finder options via apple script
APPLE_SCRIPT = """
tell application "Finder"
    tell disk ("%s" as string)
        open
        
        tell container window
            set current view to icon view
            set toolbar visible to false
            set statusbar visible to false
            set the bounds to {10, 60, 522, 402}
            set statusbar visible to false
        end tell

        set opts to the icon view options of container window
        tell opts
            set icon size to 128
        end tell
        set background picture of opts to file ".bk:inst_bk.png"
        set position of item "Editra.app" to {260, 145}

        update without registering applications
    end tell
end tell
"""

def DoSourcePackage():
    """Build a source package or do a source install"""
    # Get the package data
    DATA = GenerateSrcPackageFiles()

    # Force optimization
    if 'install' in sys.argv and ('O1' not in sys.argv or '02' not in sys.argv):
        sys.argv.append('-O2')

        # Install the plugins for this version of Python
        DATA.append("plugins/*py%d.%d.egg" % sys.version_info[:2])

    # Import proper setup function
    if 'bdist_egg' in sys.argv:
        try:
            from setuptools import setup

            # Only bundle eggs for the given python version
            DATA.append("plugins/*py%d.%d.egg" % sys.version_info[:2])
        except ImportError:
            print "To build an egg setuptools must be installed"
    else:
        from distutils.core import setup

    # Try to remove possibly conflicting files from an old install
    if '--no-clean' not in sys.argv:
        try:
            import Editra
            path = Editra.__file__
            if '__init__' in path:
                path = os.path.dirname(path)
                path = os.path.join(path, 'src')
                del sys.modules['Editra']
                shutil.rmtree(path)
        except (ImportError, OSError):
            pass
        except:
            sys.stderr.write("[ERROR] Failed to remove old source files")
    else:
        sys.argv.remove('--no-clean')

    # Make sure to delete any existing MANIFEST file beforehand to
    # prevent stale file lists
    if os.path.exists('MANIFEST'):
        try:
            os.remove('MANIFEST')
        except OSError:
            pass

    setup(
        name = NAME,
        scripts = ['editra',],
        version = VERSION,
        description = DESCRIPTION,
        long_description = LONG_DESCRIPT,
        author = AUTHOR,
        author_email = AUTHOR_EMAIL,
        maintainer = AUTHOR,
        maintainer_email = AUTHOR_EMAIL,
        url = URL,
        download_url = "http://editra.org/download",
        license = LICENSE,
        platforms = [ "Many" ],
        packages = [ NAME ],
        package_dir = { NAME : '.' },
        package_data = { NAME : DATA },
        classifiers= CLASSIFIERS,
        install_requires = ['wxPython',]
        )

def BuildECLibDemo():
    """Build the Editra Control Library Demo package"""
    assert 'eclib' in sys.argv, "Should only be called for eclib build"

    DATA = [ "../src/eclib/*.py", "../tests/controls/*.py"]
    OUT = 'dist/eclibdemo'

    Log("Cleaning up files")
    if not os.path.exists('dist'):
        os.mkdir('dist')

    if os.path.exists('dist/eclibdemo.zip'):
        os.remove('dist/eclibdemo.zip')

    if os.path.exists(OUT):
        shutil.rmtree(OUT)

    # Copy the Files
    Log("Preparing output package...")
    os.mkdir(OUT)
    shutil.copytree('src/eclib', 'dist/eclibdemo/eclib')
    shutil.copytree('tests/controls', 'dist/eclibdemo/demo')
    shutil.copy('COPYING', 'dist/eclibdemo/')
    f = open(os.path.abspath('./dist/eclibdemo/__init__.py'), 'wb')
    f.close()

    # Make the launcher
    f = open(os.path.abspath('./dist/eclibdemo/RunDemo.py'), 'wb')
    f.write("import os\nos.chdir('demo')\n"
            "import demo.demo as demo\n"
            "demo.Main()\nos.chdir('..')")
    f.close()

    # Zip it up
    Log("Create zip file")
    os.chdir('dist')
    zfile = zipfile.ZipFile('eclibdemo.zip', 'w',
                            compression=zipfile.ZIP_DEFLATED)
    files = list()
    for dpath, dname, fnames in os.walk('eclibdemo'):
        files.extend([ os.path.join(dpath, fname).\
                       lstrip(os.path.sep) 
                       for fname in fnames])
    for fname in files:
        zfile.write(fname.encode(sys.getfilesystemencoding()))
    os.chdir('../')
    Log("ECLIB Demo build is complete")

def CleanBuild():
    """Cleanup all build related files"""
    if os.path.exists('MANIFEST'):
        os.remove('MANIFEST')
    for path in ('dist', 'build', 'tmp'):
        if os.path.exists(path):
            Log("Cleaning %s..." % path)
            shutil.rmtree(path)

def Log(msg):
    """Write to the build log"""
    # TODO add log file, just write to console for now
    print(msg)

#----------------------------------------------------------------------------#

if __name__ == '__main__':
    if __platform__ == "win32" and 'py2exe' in sys.argv:
        BuildPy2Exe()
    elif __platform__ == "darwin" and 'py2app' in sys.argv:
        BuildOSXApp()
    elif 'eclib' in sys.argv:
        BuildECLibDemo()
    elif 'clean' in sys.argv:
        CleanBuild()
    else:
        DoSourcePackage()
