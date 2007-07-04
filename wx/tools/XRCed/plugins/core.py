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
Manager.setMenu(c, 'TOP_LEVEL', 'frame', 'wxFrame', 10)

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
Manager.setMenu(c, 'TOP_LEVEL', 'dialog', 'wxDialog', 20)

### wxPanel

c = Container('wxPanel', ['window', 'top_level', 'control'], 
              ['pos', 'size'],
              image=images.getTreePanelImage())
c.addStyles('wxNO_3D', 'wxTAB_TRAVERSAL')
Manager.register(c)
Manager.setMenu(c, 'TOP_LEVEL', 'panel', 'wxPanel', 30)
Manager.setMenu(c, 'container', 'panel', 'wxPanel', 10)

### wxBoxSizer

c = BoxSizer('wxBoxSizer', ['sizer'], ['orient'], 
             defaults={'orient': 'wxVERTICAL'},
             images=[images.getTreeSizerVImage(), images.getTreeSizerHImage()])
Manager.register(c)
Manager.setMenu(c, 'sizer', 'box sizer', 'wxBoxSizer', 10)

### wxStaticBoxSizer

c = BoxSizer('wxStaticBoxSizer', ['sizer'], ['label', 'orient'], 
             defaults={'orient': 'wxVERTICAL'},
             images=[images.getTreeSizerVImage(), images.getTreeSizerHImage()])
Manager.register(c)
Manager.setMenu(c, 'sizer', 'static box sizer', 'wxStaticBoxSizer', 20)

### wxGridSizer

c = Sizer('wxGridSizer', ['sizer'],
          ['cols', 'rows', 'vhap', 'hgap'], 
          defaults={'cols': '2', 'rows': '2'},
          image=images.getTreeSizerGridImage())
Manager.register(c)
Manager.setMenu(c, 'sizer', 'grid sizer', 'wxGridSizer', 30)

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
Manager.setMenu(c, 'sizer', 'flex grid sizer', 'wxFlexGridSizer', 40)

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
Manager.setMenu(c, 'sizer', 'grid bag sizer', 'wxGridBagSizer', 50)

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
Manager.setMenu(c, 'control', 'label', 'wxStaticText', 10)

### wxStaticLine

c = Component('wxStaticLine', ['control','tool'],
              ['pos', 'size'])
c.addStyles('wxLI_HORIZONTAL', 'wxLI_VERTICAL')
Manager.register(c)
Manager.setMenu(c, 'control', 'line', 'wxStaticLine', 20)

### wxStaticBitmap

c = Component('wxStaticBitmap', ['control','tool'],
              ['pos', 'size', 'bitmap'])
c.setSpecial('bitmap', BitmapAttribute)
Manager.register(c)
Manager.setMenu(c, 'control', 'bitmap', 'wxStaticLine', 30)

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
Manager.setMenu(c, 'control', 'text ctrl', 'wxTextCtrl', 40)

### wxChoice

c = Component('wxChoice', ['control','tool'],
              ['pos', 'size', 'content', 'selection'])
c.addStyles('wxCB_SORT')
c.setSpecial('content', ContentAttribute)
Manager.register(c)
Manager.setMenu(c, 'control', 'choice', 'wxChoice', 50)

### wxSlider

c = Component('wxSlider', ['control','tool'],
              ['pos', 'size', 'value', 'min', 'max', 
               'tickfreq', 'pagesize', 'linesize', 'thumb', 'tick',
               'selmin', 'selmax'])
c.addStyles('wxSL_HORIZONTAL', 'wxSL_VERTICAL', 'wxSL_AUTOTICKS', 'wxSL_LABELS',
            'wxSL_LEFT', 'wxSL_RIGHT', 'wxSL_TOP', 'wxSL_BOTTOM',
            'wxSL_BOTH', 'wxSL_SELRANGE', 'wxSL_INVERSE')
Manager.register(c)
c.setParamClass('value', params.ParamInt)
c.setParamClass('tickfreq', params.ParamIntNN)
c.setParamClass('pagesize', params.ParamIntNN)
c.setParamClass('linesize', params.ParamIntNN)
c.setParamClass('thumb', params.ParamUnit)
c.setParamClass('tick', params.ParamInt)
c.setParamClass('selmin', params.ParamInt)
c.setParamClass('selmax', params.ParamInt)
Manager.setMenu(c, 'control', 'slider', 'wxSlider', 60)

### wxGauge

c = Component('wxGauge', ['control','tool'],
              ['pos', 'size', 'range', 'value', 'shadow', 'bezel'])
c.addStyles('wxGA_HORIZONTAL', 'wxGA_VERTICAL', 'wxGA_PROGRESSBAR', 'wxGA_SMOOTH')
c.setParamClass('range', params.ParamIntNN)
c.setParamClass('value', params.ParamIntNN)
c.setParamClass('shadow', params.ParamUnit)
c.setParamClass('bezel', params.ParamUnit)
Manager.register(c)
Manager.setMenu(c, 'control', 'gauge', 'wxGauge', 70)

### wxSpinCtrl

c = Component('wxSpinCtrl', ['control','tool'],
              ['pos', 'size', 'value', 'min', 'max'])
c.addStyles('wxSP_HORIZONTAL', 'wxSP_VERTICAL', 'wxSP_ARROW_KEYS', 'wxSP_WRAP')
c.setParamClass('value', params.ParamInt)
Manager.register(c)
Manager.setMenu(c, 'control', 'spin ctrl', 'wxSpinCtrl', 75)

### wxScrollBar

c = Component('wxScrollBar', ['control'],
              ['pos', 'size', 'value', 'thumbsize', 'range', 'pagesize'])
c.addStyles('wxSB_HORIZONTAL', 'wxSB_VERTICAL')
c.setParamClass('range', params.ParamIntNN)
c.setParamClass('value', params.ParamIntNN)
c.setParamClass('thumbsize', params.ParamUnit)
c.setParamClass('pagesize', params.ParamUnit)
Manager.register(c)
Manager.setMenu(c, 'control', 'scroll bar', 'wxScrollBar', 80)

### wxListCtrl

c = Component('wxListCtrl', ['control','tool'], ['pos', 'size'])
c.addStyles('wxLC_LIST', 'wxLC_REPORT', 'wxLC_ICON', 'wxLC_SMALL_ICON',
            'wxLC_ALIGN_TOP', 'wxLC_ALIGN_LEFT', 'wxLC_AUTOARRANGE',
            'wxLC_USER_TEXT', 'wxLC_EDIT_LABELS', 'wxLC_NO_HEADER',
            'wxLC_SINGLE_SEL', 'wxLC_SORT_ASCENDING', 'wxLC_SORT_DESCENDING',
            'wxLC_VIRTUAL', 'wxLC_HRULES', 'wxLC_VRULES', 'wxLC_NO_SORT_HEADER')
Manager.register(c)
Manager.setMenu(c, 'control', 'list ctrl', 'wxListCtrl', 90)

### wxTreeCtrl

c = Component('wxTreeCtrl', ['control','tool'], ['pos', 'size'])
c.addStyles('wxTR_EDIT_LABELS',
            'wxTR_NO_BUTTONS',
            'wxTR_HAS_BUTTONS',
            'wxTR_TWIST_BUTTONS',
            'wxTR_NO_LINES',
            'wxTR_FULL_ROW_HIGHLIGHT',
            'wxTR_LINES_AT_ROOT',
            'wxTR_HIDE_ROOT',
            'wxTR_ROW_LINES',
            'wxTR_HAS_VARIABLE_ROW_HEIGHT',
            'wxTR_SINGLE',
            'wxTR_MULTIPLE',
            'wxTR_EXTENDED',
            'wxTR_DEFAULT_STYLE')
Manager.register(c)
Manager.setMenu(c, 'control', 'tree ctrl', 'wxTreeCtrl', )

### wxHtmlWindow

c = Component('wxHtmlWindow', ['control'],
              ['pos', 'size', 'borders', 'url', 'htmlcode'])
c.addStyles('wxHW_SCROLLBAR_NEVER', 'wxHW_SCROLLBAR_AUTO', 'wxHW_NO_SELECTION')
c.setParamClass('url', params.ParamLongText)
c.setParamClass('htmlcode', params.ParamMultilineText)
Manager.register(c)
Manager.setMenu(c, 'control', 'HTML window', 'wxHtmlWindow', 100)

### wxCalendarCtrl

c = Component('wxCalendarCtrl', ['control', 'tool'], ['pos', 'size'])
c.addStyles('wxCAL_SUNDAY_FIRST', 'wxCAL_MONDAY_FIRST', 'wxCAL_SHOW_HOLIDAYS',
            'wxCAL_NO_YEAR_CHANGE', 'wxCAL_NO_MONTH_CHANGE',
            'wxCAL_SEQUENTIAL_MONTH_SELECTION', 'wxCAL_SHOW_SURROUNDING_WEEKS')
Manager.register(c)
Manager.setMenu(c, 'control', 'calendar ctrl', 'wxCalendarCtrl', 110)

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
Manager.setMenu(c, 'container', 'notebook', 'Notebook control', 120)

### wxChoicebook

c = Component('wxChoicebook', ['control'], ['pos', 'size'])
c.addStyles('wxCHB_DEFAULT', 'wxCHB_LEFT', 'wxCHB_RIGHT', 'wxCHB_TOP', 'wxCHB_BOTTOM')
Manager.register(c)
Manager.setMenu(c, 'control', 'choicebook', 'wxChoicebook', 130)

### wxListbook

c = Component('wxListbook', ['control'], ['pos', 'size'])
c.addStyles('wxLB_DEFAULT', 'wxLB_LEFT', 'wxLB_RIGHT', 'wxLB_TOP', 'wxLB_BOTTOM')
Manager.register(c)
Manager.setMenu(c, 'control', 'listbook', 'wxListbook', 140)

### wxSplitterWindow

c = Component('wxSplitterWindow', ['control'],
              ['pos', 'size', 'orientation', 'sashpos', 'minsize'],
              params={'orientation': params.ParamOrientation, 
                      'sashpos': params.ParamUnit, 
                      'minsize': params.ParamUnit})
c.addStyles('wxSP_3D', 'wxSP_3DSASH', 'wxSP_3DBORDER', 
            'wxSP_FULLSASH', 'wxSP_NOBORDER', 'wxSP_PERMIT_UNSPLIT', 'wxSP_LIVE_UPDATE',
            'wxSP_NO_XP_THEME')
Manager.register(c)
Manager.setMenu(c, 'control', 'splitter window', 'wxSplitterWindow', 150)

### wxGenericDirCtrl

c = Component('wxGenericDirCtrl', ['control'],
              ['pos', 'size', 'defaultfolder', 'filter', 'defaultfilter'])
c.addStyles('wxDIRCTRL_DIR_ONLY', 'wxDIRCTRL_3D_INTERNAL', 'wxDIRCTRL_SELECT_FIRST',
            'wxDIRCTRL_SHOW_FILTERS')
Manager.register(c)
Manager.setMenu(c, 'control', 'generic dir ctrl', 'wxGenericDirCtrl', 160)

### wxDateCtrl

c = Component('wxDateCtrl', ['control'], ['pos', 'size', 'borders'])
c.addStyles('wxDP_DEFAULT', 'wxDP_SPIN', 'wxDP_DROPDOWN',
            'wxDP_ALLOWNONE', 'wxDP_SHOWCENTURY')
Manager.register(c)
Manager.setMenu(c, 'control', 'date ctrl', 'wxDateCtrl', 180)

### wxGrid

c = Component('wxGrid', ['control'], ['pos', 'size'])
Manager.register(c)
Manager.setMenu(c, 'control', 'grid', 'wxGrid', 190)

### wxFilePickerCtrl

c = Component('wxFilePickerCtrl', ['control'],
              ['pos', 'size', 'value', 'message', 'wildcard'])
c.addStyles('wxFLP_OPEN', 'wxFLP_SAVE', 'wxFLP_OVERWRITE_PROMPT',
            'wxFLP_FILE_MUST_EXIST', 'wxFLP_CHANGE_DIR',
            'wxFLP_DEFAULT_STYLE')
Manager.register(c)
Manager.setMenu(c, 'control', 'file picker ctrl', 'wxFilePickerCtrl', 200)

################################################################################
# Buttons

### wxButton

c = Component('wxButton', ['control', 'tool'],
              ['pos', 'size', 'label', 'default'])
c.addStyles('wxBU_LEFT', 'wxBU_TOP', 'wxBU_RIGHT', 'wxBU_BOTTOM', 'wxBU_EXACTFIT',
            'wxNO_BORDER')
Manager.register(c)
Manager.setMenu(c, 'button', 'button', 'wxButton', 10)

### wxBitmapButton

c = Component('wxBitmapButton', ['control', 'tool'],
              ['pos', 'size', 'bitmap', 'selected', 'focus', 'disabled', 'default'])
c.addStyles('wxBU_AUTODRAW', 'wxBU_LEFT', 'wxBU_RIGHT', 'wxBU_TOP', 'wxBU_BOTTOM')
c.setSpecial('bitmap', BitmapAttribute)
Manager.register(c)
Manager.setMenu(c, 'button', 'bitmap button', 'wxBitmapButton', 20)

### wxRadioButton

c = Component('wxRadioButton', ['control', 'tool'], ['pos', 'size', 'label', 'value'])
c.addStyles('wxRB_GROUP', 'wxRB_SINGLE')
Manager.register(c)
Manager.setMenu(c, 'button', 'radio button', 'wxRadioButton', 30)

### wxSpinButton

c = Component('wxSpinButton', ['control', 'tool'],
              ['pos', 'size', 'value', 'min', 'max'])
c.addStyles('wxSP_HORIZONTAL', 'wxSP_VERTICAL', 'wxSP_ARROW_KEYS', 'wxSP_WRAP')
Manager.register(c)
Manager.setMenu(c, 'button', 'spin button', 'wxSpinButton', 40)

### wxToggleButton

c = Component('wxToggleButton', ['control', 'tool'],
              ['pos', 'size', 'label', 'checked'])
Manager.register(c)
Manager.setMenu(c, 'button', 'toggle button', 'wxToggleButton', 50)

################################################################################
# Boxes

### wxStaticBox

c = Component('wxStaticBox', ['control','tool'],
              ['pos', 'size', 'label'])
Manager.register(c)
Manager.setMenu(c, 'box', 'static box', 'wxStaticBox', 10)

### wxRadioBox

c = Component('wxRadioBox', ['control','tool'],
              ['pos', 'size', 'label', 'content', 'selection', 'dimension'])
c.addStyles('wxRA_SPECIFY_ROWS', 'wxRA_SPECIFY_COLS', 'wxRA_HORIZONTAL',
            'wxRA_VERTICAL')
Manager.register(c)
Manager.setMenu(c, 'box', 'radio box', 'wxRadioBox', 20)

################################################################################
# Windows

### wxScrolledWindow

c = Component('wxScrolledWindow', ['window', 'control'], ['pos', 'size'])
c.addStyles('wxHSCROLL', 'wxVSCROLL', 'wxNO_3D', 'wxTAB_TRAVERSAL')
Manager.register(c)
Manager.setMenu(c, 'container', 'scrolled window', 'wxScrolledWindow', 170)




################################################################################
# Menus

### wxMenuBar

class CMenuBar(SimpleContainer):
    # Menubar should be shown in a normal frame
    def makeTestWin(self, res, name):
        '''Method can be overrided by derived classes to create test view.'''
        frame = wx.Frame(None, -1, '%s: %s' % (self.klass, name), name=STD_NAME)
        object = res.LoadMenuBarOnFrame(frame, STD_NAME)
        return None, frame

c = CMenuBar('wxMenuBar', ['menubar', 'top_level'], [],
             image=images.getTreeMenuBarImage())
c.addStyles('wxMB_DOCKABLE')
Manager.register(c)
Manager.setMenu(c, 'TOP_LEVEL', 'MenuBar', 'Menu bar', 40)
Manager.setMenu(c, 'bar', 'menu bar', 'wxMenuBar', 10)

### wxMenu

c = SimpleContainer('wxMenu', ['menu', 'top_level'], ['label', 'help'],
                    image=images.getTreeMenuImage())
c.addStyles('wxMENU_TEAROFF')
Manager.register(c)
Manager.setMenu(c, 'TOP_LEVEL', 'menu', 'wxMenu', 50)
Manager.setMenu(c, 'ROOT', 'menu', 'wxMenu', 20)

### wxMenuItem

c = SimpleComponent('wxMenuItem', ['menu_item'],
                    ['label', 'bitmap', 'accel', 'help',
                     'checkable', 'radio', 'enabled', 'checked'],
                    image=images.getTreeMenuItemImage())
c.setSpecial('bitmap', BitmapAttribute)
Manager.register(c)
Manager.setMenu(c, 'ROOT', 'menu item', 'wxMenuItem', 10)

### wxToolBar

class CToolBar(SimpleContainer):
    # Toolbar should be shown in a normal frame
    def makeTestWin(self, res, name):
        '''Method can be overrided by derived classes to create test view.'''
        frame = wx.Frame(None, -1, '%s: %s' % (self.klass, name), name=STD_NAME)
        object = res.LoadToolBar(frame, STD_NAME)
        return None, frame

c = CToolBar('wxToolBar', ['toolbar', 'top_level'],
             ['bitmapsize', 'margins', 'packing', 'separation',
              'dontattachtoframe', 'pos', 'size'],
             image=images.getTreeToolBarImage())
c.addStyles('wxTB_FLAT', 'wxTB_DOCKABLE', 'wxTB_VERTICAL', 'wxTB_HORIZONTAL',
            'wxTB_3DBUTTONS','wxTB_TEXT', 'wxTB_NOICONS', 'wxTB_NODIVIDER',
            'wxTB_NOALIGN', 'wxTB_HORZ_LAYOUT', 'wxTB_HORZ_TEXT')
c.setParamClass('dontattachtoframe', params.ParamBool)
c.setParamClass('bitmapsize', params.ParamPosSize)
c.setParamClass('margins', params.ParamPosSize)
c.setParamClass('packing', params.ParamUnit)
c.setParamClass('separation', params.ParamUnit)
c.renameDict = {'dontattachtoframe': "don't attach"}
Manager.register(c)
Manager.setMenu(c, 'TOP_LEVEL', 'ToolBar', 'Tool bar', 50)
Manager.setMenu(c, 'bar', 'tool bar', 'wxToolBar', 20)

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
Manager.setMenu(c, 'ROOT', 'tool', 'wxTool', 10)

### wxSeparator

c = SimpleComponent('separator', ['separator'], [],
                    image=images.getTreeSeparatorImage())
c.hasName = False
Manager.register(c)
Manager.setMenu(c, 'ROOT', 'separator', 'separator', 20)

### wxStatusBar

c = SimpleComponent('wxStatusBar', ['statusbar'], ['fields', 'widths', 'styles'])
c.addStyles('wxST_SIZEGRIP')
c.setParamClass('fields', params.ParamIntP)
Manager.register(c)
Manager.setMenu(c, 'bar', 'status bar', 'wxStatusBar', 30)

### wxBitmap

c = SimpleComponent('wxBitmap', ['top_level'], ['object'])
c.renameDict = {'object': ''}
c.setSpecial('object', BitmapAttribute)
c.setParamClass('object', params.ParamBitmap)
Manager.register(c)
Manager.setMenu(c, 'TOP_LEVEL', 'bitmap', 'wxBitmap', 60)

### wxIcon

c = SimpleComponent('wxIcon', ['top_level'], ['object'])
c.renameDict = {'object': ''}
c.setSpecial('object', BitmapAttribute)
c.setParamClass('object', params.ParamBitmap)
Manager.register(c)
Manager.setMenu(c, 'TOP_LEVEL', 'icon', 'wxIcon', 70)


### wxXXX

#c = Component('wxXXX', ['control','tool'],
#              ['pos', 'size', ...])
#c.addStyles(...)
#Manager.register(c)
#Manager.setMenu(c, 'control', 'XXX', 'wxXXX', NN)
