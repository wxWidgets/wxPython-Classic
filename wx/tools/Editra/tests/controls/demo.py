###############################################################################
# Name: demo.py                                                               #
# Purpose: main demo launcher                                                 #
# Author: Cody Precord <cprecord@editra.org>                                  #
# Copyright: (c) 2009 Cody Precord <staff@editra.org>                         #
# Licence: wxWindows Licence                                                  #
###############################################################################

"""
Editra Control Library Demo / Test Application

This application is used for running the ui test modules for the Editra
Control Library. The demo modules loaded by this application are primarily
intended as samples for exercising the various control apis.

"""

__author__ = "Cody Precord <cprecord@editra.org>"
__svnid__ = "$Id$"
__revision__ = "$Revision$"

#-----------------------------------------------------------------------------#
# Imports
import os
import sys
import keyword
import wx
import wx.aui as aui
import wx.html as html
import wx.stc as stc

#-----------------------------------------------------------------------------#
# TODO
if os.getcwd().endswith('demo'):
    sys.path.insert(0, os.path.abspath('../'))
else:
    sys.path.insert(0, os.path.abspath('../../src'))

import eclib

#-----------------------------------------------------------------------------#

class EclibDemoApp(wx.App):
    def OnInit(self):
        self.SetAppName("Eclib Demo")

        # Attributes
        self.frame = EclibDemoFrame("Editra Control Library Demo")

        # Setup
        self.frame.Show()

        return True

    def GetLog(self):
        return TestLog()

#-----------------------------------------------------------------------------#

class EclibDemoFrame(wx.Frame):
    """Demo Main Window"""
    def __init__(self, title=u""):
        super(EclibDemoFrame, self).__init__(None, title=title, size=(850, 550))

        # Attributes
        self.mgr = aui.AuiManager(self, aui.AUI_MGR_ALLOW_ACTIVE_PANE)
        self.tree = EclibDemoTree(self)
        self.pane = EclibDemoBook(self)
        path = os.path.dirname(__file__)
        self._loader = ModuleLoader(FindDemoModules(os.path.abspath(path)))

        # Setup
        self.mgr.AddPane(self.tree,
                         aui.AuiPaneInfo().Left().Layer(0).\
                             Caption("Test Modules").CloseButton(False).\
                             MinSize((220,-1)))
        self.mgr.AddPane(self.pane,
                         aui.AuiPaneInfo().CenterPane().\
                             Layer(1).CloseButton(False).MinSize((450,400)))
        self.mgr.Update()

        self.CenterOnParent()

        self.Bind(wx.EVT_TREE_SEL_CHANGED, self.OnTreeSel, self.tree)

    def OnTreeSel(self, evt):
        self.Freeze()
        item = evt.GetItem()
        name = self.tree.GetItemText(item)
        module = self._loader.GetModule(name)
        if module:
            self.pane.RefreshPages(self.tree.GetItemPyData(item), module) 
        self.Thaw()

#-----------------------------------------------------------------------------#

class EclibDemoBook(wx.Notebook):
    """Main Window display panel"""
    def __init__(self, parent):
        super(EclibDemoBook, self).__init__(parent, size=(450, 400))

        # Attributes
        self.doc = html.HtmlWindow(self)
        self.code = PythonStc(self)

        # Setup
        f = open(__file__, 'r')
        t = f.read()
        f.close()
        self.code.SetText(t)
        self.AddPage(self.doc, "Info")
        self.SetDocText(__doc__)
        self.AddPage(self.code, "Demo Code")
        self.doc.SetFont(wx.FFont(12, wx.MODERN))

    def RefreshPages(self, path, module):
        sel = self.GetSelection()
        if self.GetPageCount() == 3:
            self.DeletePage(2) # Recreate demo page

        self.SetDocText(module.overview)
        f = open(path, 'r')
        t = f.read()
        f.close()
        self.code.Clear()
        self.code.SetText(t)

        # Init the demo object
        page = module.TestPanel(self, wx.GetApp().GetLog())
        self.AddPage(page, module.title)
        self.SetSelection(sel)

    def SetDocText(self, txt):
        overview = txt.replace('<', '&lt;').replace('>', '&gt;')
        self.doc.SetPage("<pre>%s</pre>" % overview)

#-----------------------------------------------------------------------------#

class EclibDemoTree(wx.TreeCtrl):
    """Tree to show all demo modules"""
    def __init__(self, parent):
        wx.TreeCtrl.__init__(self, parent,
                             style=wx.TR_FULL_ROW_HIGHLIGHT|wx.TR_HIDE_ROOT)

        # Attributes
        self.root = self.AddRoot("Demos")

        # Setup
        self.PopulateTree()

        # Event Handlers

    def PopulateTree(self):
        modules = FindDemoModules(os.path.abspath('.'))
        for label, path in modules:
            item = self.AppendItem(self.root, label)
            self.SetItemPyData(item, path)

#-----------------------------------------------------------------------------#

def GetFaces():
    font = wx.FFont(11, wx.MODERN)
    face = font.GetFaceName()
    if wx.Platform == '__WXMSW__':
        faces = { 'times': face,
                  'mono' : face,
                  'helv' : face,
                  'other': face,
                  'size' : 10,
                  'size2': 8,
                 }
    elif wx.Platform == '__WXMAC__':
        faces = { 'times': face,
                  'mono' : face,
                  'helv' : face,
                  'other': face,
                  'size' : 12,
                  'size2': 10,
                 }
    else:
        faces = { 'times': face,
                  'mono' : face,
                  'helv' : face,
                  'other': face,
                  'size' : 12,
                  'size2': 10,
                 }
    return faces

#----------------------------------------------------------------------

# Lazily grifted from the wxpython demo
class PythonStc(stc.StyledTextCtrl):
    def __init__(self, parent):
        stc.StyledTextCtrl.__init__(self, parent)

        self.SetLexer(stc.STC_LEX_PYTHON)
        self.SetKeyWords(0, " ".join(keyword.kwlist))

        self.SetProperty("fold", "1")
        self.SetProperty("tab.timmy.whinge.level", "1")
        self.SetMargins(3,3)

        self.SetMarginType(1, stc.STC_MARGIN_NUMBER)
        self.SetMarginMask(1, 0)
        self.SetMarginWidth(1, 25)
        
        # Global default styles for all languages
        faces = GetFaces()
        self.StyleSetSpec(stc.STC_STYLE_DEFAULT,     "face:%(helv)s,size:%(size)d" % faces)
        self.StyleClearAll()  # Reset all to be like the default

        # Global default styles for all languages
        self.StyleSetSpec(stc.STC_STYLE_DEFAULT,     "face:%(helv)s,size:%(size)d" % faces)
        self.StyleSetSpec(stc.STC_STYLE_LINENUMBER,  "back:#C0C0C0,face:%(helv)s,size:%(size2)d" % faces)
        self.StyleSetSpec(stc.STC_STYLE_CONTROLCHAR, "face:%(other)s" % faces)
        self.StyleSetSpec(stc.STC_STYLE_BRACELIGHT,  "fore:#FFFFFF,back:#0000FF,bold")
        self.StyleSetSpec(stc.STC_STYLE_BRACEBAD,    "fore:#000000,back:#FF0000,bold")

        # Python styles
        # Default 
        self.StyleSetSpec(stc.STC_P_DEFAULT, "fore:#000000,face:%(helv)s,size:%(size)d" % faces)
        # Comments
        self.StyleSetSpec(stc.STC_P_COMMENTLINE, "fore:#007F00,face:%(other)s,size:%(size)d" % faces)
        # Number
        self.StyleSetSpec(stc.STC_P_NUMBER, "fore:#007F7F,size:%(size)d" % faces)
        # String
        self.StyleSetSpec(stc.STC_P_STRING, "fore:#7F007F,face:%(helv)s,size:%(size)d" % faces)
        # Single quoted string
        self.StyleSetSpec(stc.STC_P_CHARACTER, "fore:#7F007F,face:%(helv)s,size:%(size)d" % faces)
        # Keyword
        self.StyleSetSpec(stc.STC_P_WORD, "fore:#00007F,bold,size:%(size)d" % faces)
        # Triple quotes
        self.StyleSetSpec(stc.STC_P_TRIPLE, "fore:#7F0000,size:%(size)d" % faces)
        # Triple double quotes
        self.StyleSetSpec(stc.STC_P_TRIPLEDOUBLE, "fore:#7F0000,size:%(size)d" % faces)
        # Class name definition
        self.StyleSetSpec(stc.STC_P_CLASSNAME, "fore:#0000FF,bold,size:%(size)d" % faces)
        # Function or method name definition
        self.StyleSetSpec(stc.STC_P_DEFNAME, "fore:#007F7F,bold,size:%(size)d" % faces)
        # Operators
        self.StyleSetSpec(stc.STC_P_OPERATOR, "bold,size:%(size)d" % faces)
        # Identifiers
        self.StyleSetSpec(stc.STC_P_IDENTIFIER, "fore:#000000,face:%(helv)s,size:%(size)d" % faces)
        # Comment-blocks
        self.StyleSetSpec(stc.STC_P_COMMENTBLOCK, "fore:#7F7F7F,size:%(size)d" % faces)
        # End of line where string is not closed
        self.StyleSetSpec(stc.STC_P_STRINGEOL, "fore:#000000,face:%(mono)s,back:#E0C0E0,eol,size:%(size)d" % faces)

#-----------------------------------------------------------------------------#

class TestLog:
    def __init__(self):
        pass

    def write(self, msg):
        print msg

#-----------------------------------------------------------------------------#

class ModuleLoader(object):
    """Dynamic module loader cache"""
    _loaded = dict()
    def __init__(self, modules):
        """@param modules: list of tuples [(name, path),]"""
        object.__init__(self)

        # Attributes
        self.modules = modules

    def GetModule(self, modname):
        """Get the reference to the requested demo module, importing
        it as necessary.

        """
        self.LoadModule(modname)
        if modname in ModuleLoader._loaded:
            return ModuleLoader._loaded[modname]

        return None

    def IsModLoaded(self, modname):
        """Checks if a module has already been loaded
        @param modname: name of module to lookup

        """
        if modname in sys.modules or modname in ModuleLoader._loaded:
            return True
        else:
            return False

    def LoadModule(self, modname):
        """Dynamically loads a module by name. The loading is only
        done if the modules data set is not already being managed

        """
        if modname == None:
            return False

        if not self.IsModLoaded(modname):
            try:
                ModuleLoader._loaded[modname] = __import__(modname, globals(), 
                                                         locals(), [''])
            except ImportError:
                return False
        return True

#-----------------------------------------------------------------------------#

def FindDemoModules(path):
    """Find all demo modules under the given path
    @param path: string
    @return: list of tuples [(filename, fullpath)]

    """
    demos = list()
    for demo in os.listdir(path):
        if demo.endswith('Demo.py'):
            demos.append((demo[:-3], os.path.join(path, demo)))
    return demos

#-----------------------------------------------------------------------------#

def Main():
    app = EclibDemoApp(False)
    print wx.version()
    app.MainLoop()

#-----------------------------------------------------------------------------#

if __name__ == '__main__':
    Main()
