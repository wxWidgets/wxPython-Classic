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

# $WXDIR/wxPython/wx/tools should be on the PTYHONPATH...
import Editra.src.info as info
import Editra.src.syntax.synextreg as synextreg

# NOTE: This is copied and adapted from Editra/setup.py, take care
# that they are kept in sync...
YEAR = 2008
PLIST = dict(CFBundleName = info.PROG_NAME,
             CFBundleIconFile = 'Editra.icns',
             CFBundleShortVersionString = info.VERSION,
             CFBundleGetInfoString = info.PROG_NAME + " " + info.VERSION,
             CFBundleExecutable = info.PROG_NAME,
             CFBundleIdentifier = "org.editra.%s" % info.PROG_NAME.title(),
             CFBundleDocumentTypes = [dict(CFBundleTypeExtensions=synextreg.GetFileExtensions(),
                                           CFBundleTypeIconFile='editra_doc.icns',
                                           CFBundleTypeRole="Editor"
                                          ),
                                     ],
       #      NSAppleScriptEnabled="YES",
             NSHumanReadableCopyright = u"Copyright %s 2005-%d" % (info.AUTHOR, YEAR),
             CFBundleDisplayName = info.PROG_NAME,             
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
    
        
