# Name:         core.py
# Purpose:      Core componenets
# Author:       Roman Rolinsky <rolinsky@femagsoft.com>
# Created:      31.05.2007
# RCS-ID:       $Id$

from component import *
import images

# Test

print 'creating core components'

# Dictionary for renaming some attributes
#renameDict = {'orient':'orientation', 'option':'proportion',
#              'usenotebooksizer':'usesizer', 'dontattachtoframe':'dontattach',
#              }

### wxFrame

class CFrame(Container):
    def makeTestWin(self, res, name, pos=wx.DefaultPosition, size=wx.DefaultSize):
        testWin = res.LoadFrame(None, STD_NAME)
        # Create status bar
        testWin.panel = testWin
        if size != wx.DefaultSize:
            testWin.SetClientSize(testWin.GetBestSize())
        if pos != wx.DefaultPosition:
            testWin.SetPosition(g.testWinPos)
        return testWin

c = CFrame('wxFrame', ['frame','window','top_level'], 
           ['pos', 'size', 'title', 'centered'],
           image=images.getTreeFrameImage())
c.addStyles('wxDEFAULT_FRAME_STYLE', 'wxDEFAULT_DIALOG_STYLE', 'wxCAPTION', 
            'wxSTAY_ON_TOP', 'wxSYSTEM_MENU', 'wxTHICK_FRAME',
            'wxRESIZE_BORDER', 'wxRESIZE_BOX', 'wxCLOSE_BOX',
            'wxMAXIMIZE_BOX', 'wxMINIMIZE_BOX',
            'wxFRAME_NO_TASKBAR', 'wxFRAME_SHAPED', 'wxFRAME_TOOL_WINDOW',
            'wxFRAME_FLOAT_ON_PARENT',
            'wxNO_3D', 'wxTAB_TRAVERSAL')
c.addExStyles('wxWS_EX_VALIDATE_RECURSIVELY', 'wxFRAME_EX_METAL')
Manager.register(c)
Manager.setMenu(c, 'root', 'Frame', 'Frame window', 10)

### wxDialog

class CDialog(Container):
    def makeTestWin(self, res, name, pos=wx.DefaultPosition, size=wx.DefaultSize):
        testWin = res.LoadDialog(None, STD_NAME)
        # Create status bar
        testWin.panel = testWin
        if size != wx.DefaultSize:
            testWin.SetClientSize(testWin.GetBestSize())
        if pos != wx.DefaultPosition:
            testWin.SetPosition(g.testWinPos)
        return testWin
        
c = CDialog('wxDialog', ['frame','window','top_level'], 
            ['pos', 'size', 'title', 'centered'],
            image=images.getTreeFrameImage())
c.addStyles('wxDEFAULT_DIALOG_STYLE', 'wxDEFAULT_FRAME_STYLE', 'wxCAPTION', 
            'wxSTAY_ON_TOP', 'wxSYSTEM_MENU', 'wxTHICK_FRAME',
            'wxRESIZE_BORDER', 'wxRESIZE_BOX', 'wxCLOSE_BOX',
            'wxMAXIMIZE_BOX', 'wxMINIMIZE_BOX',
            'wxDIALOG_MODAL', 'wxDIALOG_MODELESS', 'wxDIALOG_NO_PARENT',
            'wxNO_3D', 'wxTAB_TRAVERSAL')
c.addExStyles('wxWS_EX_VALIDATE_RECURSIVELY', 'wxDIALOG_EX_METAL')
Manager.register(c)
Manager.setMenu(c, 'root', 'Dialog', 'Dialog window', 20)

### wxPanel

class CPanel(Container):
    def makeTestWin(self, res, name, pos=wx.DefaultPosition, size=wx.DefaultSize):
        # Create containing frame
        testWin = wx.Frame(None, -1, 'Panel: ' + name,
                           pos=pos, name=STD_NAME)
        testWin.panel = res.LoadPanel(testWin, STD_NAME)
        if size != wx.DefaultSize:
            testWin.panel.SetSize(size)
        if pos != wx.DefaultPosition:
            testWin.SetPosition(g.testWinPos)
        return testWin

c = CPanel('wxPanel', ['window','top_level','control'], 
           ['pos', 'size'],
           image=images.getTreePanelImage())
c.addStyles('wxNO_3D', 'wxTAB_TRAVERSAL')
c.addExStyles('wxWS_EX_VALIDATE_RECURSIVELY')
Manager.register(c)
Manager.setMenu(c, 'root', 'Panel', 'Panel window', 30)
Manager.setMenu(c, 'container', 'Panel', 'Panel window', 10)

### wxBoxSizer

c = BoxSizer('wxBoxSizer', ['sizer'], ['orient'], 
             defaults={'orient': 'wxVERTICAL'},
             images=[images.getTreeSizerVImage(), images.getTreeSizerHImage()])
Manager.register(c)
Manager.setMenu(c, 'sizer', 'BoxSizer', 'Box sizer', 10)

### wxStaticBoxSizer

c = BoxSizer('wxStaticBoxSizer', ['sizer'], ['label', 'orient'], 
             defaults={'orient': 'wxVERTICAL'},
             images=[images.getTreeSizerVImage(), images.getTreeSizerHImage()])
Manager.register(c)
Manager.setMenu(c, 'sizer', 'StaticBoxSizer', 'StaticBox sizer', 20)

### wxGridSizer

c = Sizer('wxGridSizer', ['sizer'],
          ['cols', 'rows', 'vhap', 'hgap'], 
          defaults={'cols': '2', 'rows': '2'},
          image=images.getTreeSizerGridImage())
Manager.register(c)
Manager.setMenu(c, 'sizer', 'GridSizer', 'Grid sizer', 30)

### wxFlexGridSizer

c = Sizer('wxFlexGridSizer', ['sizer'],
          ['cols', 'rows', 'vhap', 'hgap', 'growablecols', 'growablerows'],
          defaults={'cols': '2', 'rows': '2'},
          image=images.getTreeSizerFlexGridImage())
c.setSpecial('growablecols', MultiAttribute)
c.setParamClass('growablecols', params.ParamIntList)
c.setSpecial('growablerows', MultiAttribute)
c.setParamClass('growablerows', params.ParamIntList)
Manager.register(c)
Manager.setMenu(c, 'sizer', 'FlexGridSizer', 'FlexGrid sizer', 40)

### wxGridBagSizer

c = Sizer('wxGridBagSizer', ['sizer'],
          ['vhap', 'hgap', 'growablecols', 'growablerows'],
          image=images.getTreeSizerGridBagImage(),
          implicit_attributes=['option', 'flag', 'border', 'minsize', 'ratio', 'cellpos', 'cellspan'])
c.setSpecial('growablecols', MultiAttribute)
c.setParamClass('growablecols', params.ParamIntList)
c.setSpecial('growablerows', MultiAttribute)
c.setParamClass('growablerows', params.ParamIntList)
c.setImplicitParamClass('cellpos', params.ParamPosSize)
c.setImplicitParamClass('cellspan', params.ParamPosSize)
Manager.register(c)
Manager.setMenu(c, 'sizer', 'GridBagSizer', 'GridBag sizer', 50)

### spacer

c = Component('spacer', ['spacer'], ['size', 'option', 'flag', 'border'])
c.hasName = False
c.windowAttributes = []
Manager.register(c)
Manager.setMenu(c, 'sizer', 'spacer', 'spacer', 60)

### wxStaticText

c = Component('wxStaticText', ['control','tool'],
              ['pos', 'size', 'label'], 
              defaults={'label': 'LABEL'})
c.addStyles('wxALIGN_LEFT', 'wxALIGN_RIGHT', 'wxALIGN_CENTRE', 'wxST_NO_AUTORESIZE')
Manager.register(c)
Manager.setMenu(c, 'control', 'Label', 'Label', 10)

### wxTextCtrl

c = Component('wxTextCtrl', ['control','tool'],
              ['pos', 'size', 'value'])
c.addStyles('wxTE_NO_VSCROLL',
            'wxTE_AUTO_SCROLL',
            'wxTE_PROCESS_ENTER',
            'wxTE_PROCESS_TAB',
            'wxTE_MULTILINE',
            'wxTE_PASSWORD',
            'wxTE_READONLY',
            'wxHSCROLL',
            'wxTE_RICH',
            'wxTE_RICH2',
            'wxTE_AUTO_URL',
            'wxTE_NOHIDESEL',
            'wxTE_LEFT',
            'wxTE_CENTRE',
            'wxTE_RIGHT',
            'wxTE_DONTWRAP',
            'wxTE_LINEWRAP',
            'wxTE_WORDWRAP')
c.setParamClass('value', params.ParamMultilineText)
Manager.register(c)
Manager.setMenu(c, 'control', 'TextCtrl', 'Text field', 20)

### wxChoice

c = Component('wxChoice', ['control','tool'],
              ['pos', 'size', 'content', 'selection'])
c.addStyles('wxCB_SORT')
c.setSpecial('content', ContentAttribute)
Manager.register(c)
Manager.setMenu(c, 'control', 'Choice', 'Choice control', 30)

### wxNotebook

c = SmartContainer('wxNotebook', ['window', 'control'], ['pos', 'size'], 
                   implicit_name='notebookpage', 
                   implicit_page='Page Attributes', 
                   implicit_attributes=['label', 'selected'],
                   implicit_params={'selected': params.ParamBool})
c.addStyles('wxNB_TOP', 'wxNB_LEFT', 'wxNB_RIGHT', 'wxNB_BOTTOM',
            'wxNB_FIXEDWIDTH', 'wxNB_MULTILINE', 'wxNB_NOPAGETHEME', 
            'wxNB_FLAT')
c.setParamClass('selected', params.ParamBool)
c.setParamClass('label', params.ParamText)
Manager.register(c)
Manager.setMenu(c, 'container', 'Notebook', 'Notebook control', 20)

### wxMenuBar

class CMenuBar(Container):
    windowAttributes = []
    def makeTestWin(self, res, name, pos=wx.DefaultPosition):
        testWin = wx.Frame(None, -1, 'MenuBar: ' + name,
                           pos=pos, name=STD_NAME)
        testWin.panel = None
        # Set status bar to display help
        testWin.CreateStatusBar()
        testWin.menuBar = res.LoadMenuBar(STD_NAME)
        testWin.SetMenuBar(testWin.menuBar)
        return testWin

c = CMenuBar('wxMenuBar', ['menubar', 'top_level'], [],
             image=images.getTreeMenuBarImage())
c.addStyles('wxMB_DOCKABLE')
c.setParamClass('style', params.ParamNonGenericStyle)
Manager.register(c)
Manager.setMenu(c, 'root', 'MenuBar', 'Menu bar', 40)

### wxMenu

class CMenu(Container):
    windowAttributes = []
    def makeTestWin(self, res, name, pos=wx.DefaultPosition):
        testWin = wx.Frame(None, -1, 'Menu: ' + name,
                           pos=pos, name=STD_NAME)
        testWin.panel = None
        # Set status bar to display help
        testWin.CreateStatusBar()
        testWin.menuBar = res.LoadMenu(STD_NAME)
        testWin.SetMenuBar(testWin.menuBar)
        return testWin

c = CMenu('wxMenu', ['menu', 'top_level'], ['label', 'help'],
          image=images.getTreeMenuImage())
c.addStyles('wxMENU_TEAROFF')
c.setParamClass('style', params.ParamNonGenericStyle)
Manager.register(c)
Manager.setMenu(c, 'root', 'Menu', 'Menu', 50)
Manager.setMenu(c, 'item', 'Menu', 'Menu', 20)

### wxMenuItem

c = Component('wxMenuItem', ['menu_item'],
              ['label', 'bitmap', 'accel', 'help',
               'checkable', 'radio', 'enabled', 'checked'],
              image=images.getTreeMenuItemImage())
Manager.register(c)
Manager.setMenu(c, 'item', 'MenuItem', 'Menu item', 10)

### wxToolBar

class CToolBar(Container):
    windowAttributes = []
    styles = ['wxTB_FLAT', 'wxTB_DOCKABLE', 'wxTB_VERTICAL', 'wxTB_HORIZONTAL',
              'wxTB_3DBUTTONS','wxTB_TEXT', 'wxTB_NOICONS', 'wxTB_NODIVIDER',
              'wxTB_NOALIGN', 'wxTB_HORZ_LAYOUT', 'wxTB_HORZ_TEXT']
    def makeTestWin(self, res, name, pos=wx.DefaultPosition):
        testWin = wx.Frame(None, -1, 'ToolBar: ' + name,
                           pos=pos, name=STD_NAME)
        testWin.panel = None
        # Set status bar to display help
        testWin.CreateStatusBar()
        testWin.toolBar = res.LoadToolBar(testWin, STD_NAME)
        testWin.SetToolBar(testWin.toolBar)
        return testWin

c = CToolBar('wxToolBar', ['toolbar', 'top_level'],
             ['bitmapsize', 'margins', 'packing', 'separation',
              'dontattachtoframe', 'pos', 'size'],
             image=images.getTreeToolBarImage())
c.setParamClass('style', params.ParamNonGenericStyle)
Manager.register(c)
Manager.setMenu(c, 'root', 'ToolBar', 'Tool bar', 50)

### wxTool

c = Component('wxTool', ['tool'],
              ['bitmap', 'bitmap2', 'radio', 'toggle',
               'tooltip', 'longhelp', 'label'],
              image=images.getTreeToolImage())
Manager.register(c)
Manager.setMenu(c, 'item', 'Tool', 'Tool', 10)

### wxSeparator

c = Component('separator', ['separator'], [],
              image=images.getTreeSeparatorImage())
c.windowAttributes = []
Manager.register(c)
Manager.setMenu(c, 'item', 'Separator', 'Separator', 20)


