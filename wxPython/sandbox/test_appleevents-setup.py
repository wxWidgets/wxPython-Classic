from setuptools import setup
import py2app

NAME = 'test_appleevents'
APP = ['test_appleevents.py']
VERSION = '1.2.3'

PList = dict(
    CFBundleName = NAME,
    CFBundleIconFile = 'mondrian.icns',
    CFBundleShortVersionString = VERSION,
    CFBundleGetInfoString = NAME + " " + VERSION,
    CFBundleExecutable = NAME,
    CFBundleIdentifier = "org.wxpython.%s" % NAME,
    NSHumanReadableCopyright = u"Copyright TCS 2008",
    )    
    
OPTIONS = {
    'argv_emulation': True,
    'iconfile': 'mondrian.icns',
    'plist': PList,
    }


setup( name = NAME,
       app = APP,
       version = VERSION,
       options = {'py2app': OPTIONS},
       )
