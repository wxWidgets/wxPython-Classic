"""
This script will rewrite the manifest resource in the python.exe and 
pythonw.exe files so it will include a dependency on the themed version
of the common controls DLL.  This will allow GUI applications launched 
from the stock python or pythonw to load and use the themed controls 
on XP and Vista.  This is only needed wih Python 2.6+.  Python 2.5 and 
prior did not have an embedded manifest so using the external manifest 
file was good enough. 
"""

import sys
import os
import ctypes

BeginUpdateResource = ctypes.windll.kernel32.BeginUpdateResourceA
UpdateResource = ctypes.windll.kernel32.UpdateResourceA
EndUpdateResource = ctypes.windll.kernel32.EndUpdateResourceA

base = os.path.dirname(sys.argv[0])

print __doc__
raw_input("Press ENTER to continue...")


try:

    for name in ['python.exe', 'pythonw.exe']:
        handle = BeginUpdateResource(os.path.join(base, name), 0)
        if handle == 0:
            raise ctypes.WinError()
        MANIFEST = file(os.path.join(base, name)+'.manifest').read()
        res = UpdateResource(handle, 24, 1, 1033, MANIFEST, len(MANIFEST))
        if not res:
            raise ctypes.WinError()
        res = EndUpdateResource(handle, 0)
        if not res:
            raise ctypes.WinError()
except WindowsError:
    print """
Unable to modify the Python executable.  It may be "in use", see wxPython's 
README file for hints on how to work around this.
"""
