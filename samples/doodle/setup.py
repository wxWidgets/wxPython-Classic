# A distutils script to make a standalone .exe or .zpp of superdoodle
# for Windows or OS X platforms.  You need the py2exe or py2app
# package installed to use this script (see google for pointers if you
# don't already have them) and then use this command to build the .exe
# and collect the other needed files:
#
#       python setup.py py2exe
# or
#       python setup.py py2app
#


import sys, os
##from esky import bdist_esky
from setuptools import setup

if sys.platform == "win32":
    


    setup( name = "superdoodle",
           #console = ["superdoodle.py"]
           windows = ["superdoodle.py"],
           #data_files = DATA,
           options = {"py2exe" : { "compressed": 0,
                                   "optimize": 2,
                                   "bundle_files": 1,
                                   }},
           zipfile = None
           )

elif sys.platform == "darwin":
    

    APP = ['superdoodle.py']
    DATA_FILES = []
    OPTIONS = {##'argv_emulation': True
               }

    setup( name='SuperDoodle',
           version='1.2.3',
           scripts=APP,

           app=APP,
           data_files=DATA_FILES,
           options={'py2app': OPTIONS},
           setup_requires=['py2app'],
           )


