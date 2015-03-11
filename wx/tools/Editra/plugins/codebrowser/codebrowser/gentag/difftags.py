###############################################################################
# Name: patchtags.py                                                          #
# Purpose: Generate Tags for patch files (diff)                               #
# Author: Eric Gaudet                                                         #
# License: wxWindows License                                                  #
###############################################################################

"""
DocStruct generator for for patch files (diff). Unified diff based on svn format

@author: Eric Gaudet
@summary: Generate a DocStruct object that captures the files in a patch
"""

__author__ = "Eric Gaudet"
__svnid__ = "$Id$"
__revision__ = "$Revision$"

#--------------------------------------------------------------------------#

# Imports
import re

# Local Imports
import taglib
import parselib

#--------------------------------------------------------------------------#

RE_FILE = re.compile(r"^(Index|diff).*\s+(.+)$")

#--------------------------------------------------------------------------#

def GenerateTags(buff):
    """Create a DocStruct object that represents the list of files in a patch
    @param buff: a file like buffer object (StringIO)
    """
    rtags = taglib.DocStruct()
    rtags.SetElementDescription('variable', "Files")

    # Parse the buffer
    for lnum, line in enumerate(buff):

        line = line.strip()
        if len(line)==0:
            continue

        match = RE_FILE.match(line)
        if match:
            cname = match.groups()[-1]
            cobj = taglib.Variable(cname, lnum)
            rtags.AddVariable(cobj)
            continue
    return rtags

#-----------------------------------------------------------------------------#

# Test
if __name__ == '__main__':
    import sys
    import StringIO
    fhandle = open(sys.argv[1])
    txt = fhandle.read()
    fhandle.close()
    tags = GenerateTags(StringIO.StringIO(txt))
    for element in tags.GetElements():
        print "\n%s:" % element.keys()[0]
        for val in element.values()[0]:
            print "%s [%d]" % (val.GetName(), val.GetLine())
    print "END"


