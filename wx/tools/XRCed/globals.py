# Name:         globals.py
# Purpose:      XRC editor, global variables
# Author:       Roman Rolinsky <rolinsky@mema.ucl.ac.be>
# Created:      02.12.2002
# RCS-ID:       $Id$

import os,sys
import wx
import wx.xrc as xrc
try:
    import wx.wizard
except:
    pass

# Global constants

progname = 'XRCed'
version = '0.2.0-0'
# Minimal wxWidgets version
MinWxVersion = (2,8,0)
if wx.VERSION[:3] < MinWxVersion:
    print '''\
******************************* WARNING **************************************
  This version of XRCed may not work correctly on your version of wxWidgets.
  Please upgrade wxWidgets to %d.%d.%d or higher.
******************************************************************************''' % MinWxVersion    

# Can be changed to set other default encoding different
#defaultEncoding = ''
# you comment above and can uncomment this:
defaultEncoding = wx.GetDefaultPyEncoding()

# Constant to define standart window name for tested component
STD_NAME = '_XRCED_T_W'
TEST_FILE = 'test.xrc'

# Global id constants
class ID:
    SHIFT = 1000                        # shift ids of replace commands
    MENU = wx.NewId()
    EXPAND = wx.NewId()
    COLLAPSE = wx.NewId()
    PASTE_SIBLING = wx.NewId()
    TOOL_PASTE = wx.NewId()
    INSERT = wx.NewId()
    APPEND = wx.NewId()
    SIBLING = wx.NewId()
    REPLACE = wx.NewId()
    SUBCLASS = wx.NewId()
    REF = wx.NewId()
    COMMENT = wx.NewId()

# Global variables

debug = True                    # default debug flag

def TRACE(msg, *args):
    if debug: print >> sys.stderr, 'TRACE: ' + (msg % args)

class Globals:
    undoMan = None
    currentEncoding = defaultEncoding
    conf = None

    def _makeFonts(self):
        self._sysFont = wx.SystemSettings.GetFont(wx.SYS_SYSTEM_FONT)
        self._labelFont = wx.Font(self._sysFont.GetPointSize(), wx.DEFAULT, wx.NORMAL, wx.BOLD)
        self._modernFont = wx.Font(self._sysFont.GetPointSize(), wx.MODERN, wx.NORMAL, wx.NORMAL)
        self._smallerFont = wx.Font(self._sysFont.GetPointSize()-2, wx.DEFAULT, wx.NORMAL, wx.NORMAL)
        
    def sysFont(self):
        if not hasattr(self, "_sysFont"): self._makeFonts()
        return self._sysFont
    def labelFont(self):
        if not hasattr(self, "_labelFont"): self._makeFonts()
        return self._labelFont
    def modernFont(self):
        if not hasattr(self, "_modernFont"): self._makeFonts()
        return self._modernFont
    def smallerFont(self):
        if not hasattr(self, "_smallerFont"): self._makeFonts()
        return self._smallerFont
    

g = Globals()

# Set application path for loading resources
if __name__ == '__main__':
    g.basePath = os.path.dirname(sys.argv[0])
else:
    g.basePath = os.path.dirname(__file__)
g.basePath = os.path.abspath(g.basePath)

# Data object used for clipboard
class MyDataObject(wx.PyDataObjectSimple):
    def __init__(self):
        wx.PyDataObjectSimple.__init__(self, wx.CustomDataFormat('XRCed_DND'))
        self.data = ''
    def GetDataSize(self):
        return len(self.data)
    def GetDataHere(self):
        return self.data  # returns a string  
    def SetData(self, data):
        self.data = data
        return True

# Test for object elements (!!! move somewhere?)
def is_object(node):
    return node.nodeType == node.ELEMENT_NODE and \
           node.tagName in ['object', 'object_ref', 'component']
#or \
#           node.nodeType == node.COMMENT_NODE

