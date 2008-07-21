# This module is used from the wxhack.pth file on OSX installs to move
# the items added to the sys.path by that .pth file to a location
# nearer the beginning of the list, so this install of wxPython will be
# found first but can still be overridden by PYTHONPATH.

import sys

def fixpath(pyver, num):
    """
    Look for the position in the sys.path of the std library zip file
    and move the last num items to that position. This puts us before
    the stock paths, but after any PYTHONPATH settings or eggs.
    """
    if '.' in pyver:
        pyver = ''.join(pyver.split('.'))
    tail = 'python%s.zip' % pyver
    pos = [i for i,v in enumerate(sys.path) if v.endswith(tail)]
    if not pos:
        pos = 0
    else:
        pos = pos[0]
    sys.path[pos:pos] = sys.path[-num:]
    del sys.path[-num:]
