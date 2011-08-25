

import sys, os
from esky import bdist_esky
from setuptools import setup

import version


# platform specific settings for Windows/py2exe
if sys.platform == "win32":
    import py2exe
    
    FREEZER = 'py2exe'
    FREEZER_OPTIONS = dict(compressed = 0,
                           optimize = 0,
                           bundle_files = 3,
                           dll_excludes = ['MSVCP90.dll',
                                           'mswsock.dll',
                                           'powrprof.dll', 
                                           'USP10.dll',],
                        )
    exeICON = 'mondrian.ico'
    
                 
# platform specific settings for Mac/py2app
elif sys.platform == "darwin":
    import py2app
    
    FREEZER = 'py2app'
    FREEZER_OPTIONS = dict(argv_emulation = False, 
                           iconfile = 'mondrian.icns',
                           )
    exeICON = None
    

    
# Common settings    
NAME = "SuperDoodle"
APP = [bdist_esky.Executable("superdoodle.py", 
                             gui_only=True,
                             icon=exeICON,
                             )]
DATA_FILES = [ 'mondrian.ico' ]
ESKY_OPTIONS = dict( freezer_module     = FREEZER,
                     freezer_options    = FREEZER_OPTIONS,
                     enable_appdata_dir = True,
                     bundle_msvcrt      = True,
                     )
    

# Build the app and the esky bundle
setup( name       = NAME,
       scripts    = APP,
       version    = version.VERSION,
       data_files = DATA_FILES,
       options    = dict(bdist_esky=ESKY_OPTIONS),
       )


