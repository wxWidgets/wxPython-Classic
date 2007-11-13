#!/usr/bin/env python

"""
This is just a quick and dirty hack to update the Info.plist file for
the Editra application bundle since bundlebuilder doesn't have the
options available to control putting everything there that we want it
to.  One of these days I should just switch to py2app for making these
bundles, but until then this is easy enough to workaround...
"""

import sys, os
import plistlib

import wx.tools.Editra.src.ed_glob as ed_glob
import wx.tools.Editra.src.syntax.syntax as syntax

# NOTE: This is copied and adapted from Editra/setup.py, take care
# that they are kept in sync...
YEAR = 2007
PLIST = dict(CFBundleName = ed_glob.PROG_NAME,
             CFBundleIconFile = 'Editra.icns',
             CFBundleShortVersionString = ed_glob.VERSION,
             CFBundleGetInfoString = ed_glob.PROG_NAME + " " + ed_glob.VERSION,
             CFBundleExecutable = ed_glob.PROG_NAME,
             CFBundleIdentifier = "org.editra.%s" % ed_glob.PROG_NAME.title(),
             CFBundleDocumentTypes = [dict(CFBundleTypeExtensions=syntax.GetFileExtensions(),
                                           CFBundleTypeIconFile='editra_doc.icns',
                                           CFBundleTypeRole="Editor"
                                          ),
                                     ],
       #      NSAppleScriptEnabled="YES",
             NSHumanReadableCopyright = u"Copyright %s 2005-%d" % (ed_glob.AUTHOR, YEAR),
             CFBundleDisplayName = ed_glob.PROG_NAME,             
             )



def main():
    if len(sys.argv) != 2 or not os.path.exists(sys.argv[1]):
        sys.stderr.write("Missing Info.plist pathname!\n")
        sys.exit(1)

    print "Updating %s..." % sys.argv[1]
    pl = plistlib.readPlist(sys.argv[1])
    pl.update(PLIST)
    plistlib.writePlist(pl, sys.argv[1])
    print "...done"



if __name__ == "__main__":
    main()
    
        
