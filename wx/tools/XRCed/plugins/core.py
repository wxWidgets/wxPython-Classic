# Name:         core.py
# Purpose:      Core componenets
# Author:       Roman Rolinsky <rolinsky@femagsoft.com>
# Created:      31.05.2007
# RCS-ID:       $Id$

from component import *
import images

# Test

print 'creating core components'

### wxFrame

c = Container('wxFrame', ['frame','window','top_level'], 
              ['pos', 'size', 'title', 'centered'],
              image=images.getTreeFrameImage())
c.isTopLevel = True
c.addStyles('wxDEFAULT_FRAME_STYLE', 'wxDEFAULT_DIALOG_STYLE', 'wxCAPTION', 
            'wxSTAY_ON_TOP', 'wxSYSTEM_MENU', 'wxTHICK_FRAME',
            'wxRESIZE_BORDER', 'wxRESIZE_BOX', 'wxCLOSE_BOX',
            'wxMAXIMIZE_BOX', 'wxMINIMIZE_BOX',
            'wxFRAME_NO_TASKBAR', 'wxFRAME_SHAPED', 'wxFRAME_TOOL_WINDOW',
            'wxFRAME_FLOAT_ON_PARENT',
            'wxNO_3D', 'wxTAB_TRAVERSAL')
c.addExStyles('wxFRAME_EX_METAL')
Manager.register(c)
Manager.setMenu(c, 'TOP_LEVEL', 'Frame', 'Frame window', 10)

### wxDialog

c = Container('wxDialog', ['frame','window','top_level'], 
              ['pos', 'size', 'title', 'centered'],
              image=images.getTreeFrameImage())
c.isTopLevel = True
c.addStyles('wxDEFAULT_DIALOG_STYLE', 'wxDEFAULT_FRAME_STYLE', 'wxCAPTION', 
            'wxSTAY_ON_TOP', 'wxSYSTEM_MENU', 'wxTHICK_FRAME',
            'wxRESIZE_BORDER', 'wxRESIZE_BOX', 'wxCLOSE_BOX',
            'wxMAXIMIZE_BOX', 'wxMINIMIZE_BOX',
            'wxDIALOG_MODAL', 'wxDIALOG_MODELESS', 'wxDIALOG_NO_PARENT',
            'wxNO_3D', 'wxTAB_TRAVERSAL')
c.addExStyles('wxDIALOG_EX_METAL')
Manager.register(c)
Manager.setMenu(c, 'TOP_LEVEL', 'Dialog', 'Dialog window', 20)

### wxPanel

c = Container('wxPanel', ['window','top_level','control'], 
              ['pos', 'size'],
              image=images.getTreePanelImage())
c.addStyles('wxNO_3D', 'wxTAB_TRAVERSAL')
Manager.register(c)
Manager.setMenu(c, 'TOP_LEVEL', 'Panel', 'Panel window', 30)
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

c = SimpleComponent('spacer', ['spacer'], ['size', 'option', 'flag', 'border'])
c.hasName = False
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

# Set special ParentChildGroup for notebook - notebookpage can't contain sizer
parentChildGroups['notebook'] = ['control', 'window', '!sizer']
c = SmartContainer('wxNotebook', ['notebook', 'window', 'control'], ['pos', 'size'], 
                   implicit_klass='notebookpage', 
                   implicit_page='NotebookPage', 
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

c = Container('wxMenuBar', ['menubar', 'top_level'], [],
              image=images.getTreeMenuBarImage())
c.windowAttributes = []
c.genericStyles = c.genericExStyles = []
c.addStyles('wxMB_DOCKABLE')
Manager.register(c)
Manager.setMenu(c, 'TOP_LEVEL', 'MenuBar', 'Menu bar', 40)
Manager.setMenu(c, 'bar', 'MenuBar', 'Menu bar', 10)

### wxMenu

c = Container('wxMenu', ['menu', 'top_level'], ['label', 'help'],
              image=images.getTreeMenuImage())
c.windowAttributes = []
c.genericStyles = c.genericExStyles = []
c.addStyles('wxMENU_TEAROFF')
Manager.register(c)
Manager.setMenu(c, 'TOP_LEVEL', 'Menu', 'Menu', 50)
Manager.setMenu(c, 'ROOT', 'Menu', 'Menu', 20)

### wxMenuItem

c = SimpleComponent('wxMenuItem', ['menu_item'],
                    ['label', 'bitmap', 'accel', 'help',
                     'checkable', 'radio', 'enabled', 'checked'],
                    image=images.getTreeMenuItemImage())
c.setSpecial('bitmap', BitmapAttribute)
Manager.register(c)
Manager.setMenu(c, 'ROOT', 'MenuItem', 'Menu item', 10)

### wxToolBar

c = Container('wxToolBar', ['toolbar', 'top_level'],
              ['bitmapsize', 'margins', 'packing', 'separation',
               'dontattachtoframe', 'pos', 'size'],
              image=images.getTreeToolBarImage())
c.windowAttributes = []
c.addStyles('wxTB_FLAT', 'wxTB_DOCKABLE', 'wxTB_VERTICAL', 'wxTB_HORIZONTAL',
            'wxTB_3DBUTTONS','wxTB_TEXT', 'wxTB_NOICONS', 'wxTB_NODIVIDER',
            'wxTB_NOALIGN', 'wxTB_HORZ_LAYOUT', 'wxTB_HORZ_TEXT')
c.renameDict = {'dontattachtoframe':'dontattach'}
c.genericStyles = c.genericExStyles = []
Manager.register(c)
Manager.setMenu(c, 'TOP_LEVEL', 'ToolBar', 'Tool bar', 50)
Manager.setMenu(c, 'bar', 'ToolBar', 'Tool bar', 20)

### wxTool

c = SimpleComponent('tool', ['tool'],
                    ['bitmap', 'bitmap2', 'radio', 'toggle',
                     'tooltip', 'longhelp', 'label'],
                    image=images.getTreeToolImage())
Manager.register(c)
c.setSpecial('bitmap', BitmapAttribute)
c.setSpecial('bitmap2', BitmapAttribute)
c.setParamClass('bitmap2', params.ParamBitmap)
c.setParamClass('toggle', params.ParamBool)
Manager.setMenu(c, 'ROOT', 'Tool', 'Tool', 10)

### wxSeparator

c = SimpleComponent('separator', ['separator'], [],
                    image=images.getTreeSeparatorImage())
c.hasName = False
Manager.register(c)
Manager.setMenu(c, 'ROOT', 'Separator', 'Separator', 20)

### wxStatusBar

c = SimpleComponent('wxStatusBar', ['statusbar'], ['fields', 'widths', 'styles'])
c.addStyles('wxST_SIZEGRIP')
c.setParamClass('fields', params.MetaParamIntNN(1))
Manager.register(c)
Manager.setMenu(c, 'bar', 'StatusBar', 'Status bar', 30)

### wxBitmap

c = SimpleComponent('wxBitmap', ['top_level'], ['object'])
c.renameDict = {'object': ''}
c.setSpecial('object', BitmapAttribute)
c.setParamClass('object', params.ParamBitmap)
Manager.register(c)
Manager.setMenu(c, 'TOP_LEVEL', 'Bitmap', 'Bitmap', 60)

### wxIcon

c = SimpleComponent('wxIcon', ['top_level'], ['object'])
c.renameDict = {'object': ''}
c.setSpecial('object', BitmapAttribute)
c.setParamClass('object', params.ParamBitmap)
Manager.register(c)
Manager.setMenu(c, 'TOP_LEVEL', 'Icon', 'Icon', 70)
