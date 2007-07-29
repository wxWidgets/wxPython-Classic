# Name:         controls.py
# Purpose:      Control components
# Author:       Roman Rolinsky <rolinsky@femagsoft.com>
# Created:      31.05.2007
# RCS-ID:       $Id: core.py 47823 2007-07-29 19:24:35Z ROL $

from component import *
import images
import _bitmaps as bitmaps

TRACE('*** creating control components')

# Set panel images
Manager.panelImages['Controls'] = images.getToolPanel_ControlsImage()

### wxStaticText

c = Component('wxStaticText', ['control','tool'],
              ['pos', 'size', 'label'], 
              defaults={'label': 'LABEL'})
c.addStyles('wxALIGN_LEFT', 'wxALIGN_RIGHT', 'wxALIGN_CENTRE', 'wxST_NO_AUTORESIZE')
Manager.register(c)
Manager.setMenu(c, 'control', 'label', 'wxStaticText', 10)
Manager.setTool(c, 'Controls', pos=(0,0))

### wxStaticLine

c = Component('wxStaticLine', ['control','tool'],
              ['pos', 'size'])
c.addStyles('wxLI_HORIZONTAL', 'wxLI_VERTICAL')
Manager.register(c)
Manager.setMenu(c, 'control', 'line', 'wxStaticLine', 20)
Manager.setTool(c, 'Controls', pos=(0,3))

### wxStaticBitmap

c = Component('wxStaticBitmap', ['control','tool'],
              ['pos', 'size', 'bitmap'])
c.setSpecial('bitmap', BitmapAttribute)
Manager.register(c)
Manager.setMenu(c, 'control', 'bitmap', 'wxStaticLine', 30)
Manager.setTool(c, 'Controls', pos=(1,0))

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
c.addEvents('EVT_TEXT', 'EVT_TEXT_ENTER', 'EVT_TEXT_URL', 'EVT_TEXT_MAXLEN')
Manager.register(c)
Manager.setMenu(c, 'control', 'text ctrl', 'wxTextCtrl', 40)
Manager.setTool(c, 'Controls', pos=(0,2))

### wxChoice

c = Component('wxChoice', ['control','tool'],
              ['pos', 'size', 'content', 'selection'])
c.addStyles('wxCB_SORT')
c.setSpecial('content', ContentAttribute)
c.addEvents('EVT_CHOICE')
Manager.register(c)
Manager.setMenu(c, 'control', 'choice', 'wxChoice', 50)
Manager.setTool(c, 'Controls', pos=(3,2))

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
c.addEvents('EVT_SCROLL', 'EVT_SCROLL_TOP', 'EVT_SCROLL_BOTTOM',
            'EVT_SCROLL_LINEUP', 'EVT_SCROLL_LINEDOWN', 'EVT_SCROLL_PAGEUP',
            'EVT_SCROLL_PAGEDOWN', 'EVT_SCROLL_THUMBTRACK', 'EVT_SCROLL_THUMBRELEASE',
            'EVT_SCROLL_CHANGED', 'EVT_SCROLL', 'EVT_SCROLL_TOP',
            'EVT_SCROLL_BOTTOM', 'EVT_SCROLL_LINEUP', 
            'EVT_SCROLL_LINEDOWN', 'EVT_SCROLL_PAGEUP',
            'EVT_SCROLL_PAGEDOWN', 'EVT_SCROLL_THUMBTRACK',
            'EVT_SCROLL_THUMBRELEASE', 'EVT_SCROLL_CHANGED')
Manager.setMenu(c, 'control', 'slider', 'wxSlider', 60)
Manager.setTool(c, 'Controls', pos=(2,3))

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
Manager.setTool(c, 'Controls', pos=(1,3))

### wxSpinCtrl

c = Component('wxSpinCtrl', ['control','tool'],
              ['pos', 'size', 'value', 'min', 'max'])
c.addStyles('wxSP_HORIZONTAL', 'wxSP_VERTICAL', 'wxSP_ARROW_KEYS', 'wxSP_WRAP')
c.setParamClass('value', params.ParamInt)
c.addEvents('EVT_SPINCTRL')
Manager.register(c)
Manager.setMenu(c, 'control', 'spin ctrl', 'wxSpinCtrl', 80)
Manager.setTool(c, 'Controls', pos=(1,2))

### wxScrollBar

c = Component('wxScrollBar', ['control'],
              ['pos', 'size', 'value', 'thumbsize', 'range', 'pagesize'])
c.addStyles('wxSB_HORIZONTAL', 'wxSB_VERTICAL')
c.setParamClass('range', params.ParamIntNN)
c.setParamClass('value', params.ParamIntNN)
c.setParamClass('thumbsize', params.ParamUnit)
c.setParamClass('pagesize', params.ParamUnit)
c.addEvents('EVT_SCROLL', 'EVT_SCROLL_TOP', 'EVT_SCROLL_BOTTOM',
            'EVT_SCROLL_LINEUP', 'EVT_SCROLL_LINEDOWN', 'EVT_SCROLL_PAGEUP',
            'EVT_SCROLL_PAGEDOWN', 'EVT_SCROLL_THUMBTRACK', 'EVT_SCROLL_THUMBRELEASE',
            'EVT_SCROLL_CHANGED', 'EVT_SCROLL', 'EVT_SCROLL_TOP',
            'EVT_SCROLL_BOTTOM', 'EVT_SCROLL_LINEUP', 
            'EVT_SCROLL_LINEDOWN', 'EVT_SCROLL_PAGEUP',
            'EVT_SCROLL_PAGEDOWN', 'EVT_SCROLL_THUMBTRACK',
            'EVT_SCROLL_THUMBRELEASE', 'EVT_SCROLL_CHANGED')
Manager.register(c)
Manager.setMenu(c, 'control', 'scroll bar', 'wxScrollBar', 90)
Manager.setTool(c, 'Controls', pos=(3,3))

### wxListCtrl

c = Component('wxListCtrl', ['control','tool'], ['pos', 'size'])
c.addStyles('wxLC_LIST', 'wxLC_REPORT', 'wxLC_ICON', 'wxLC_SMALL_ICON',
            'wxLC_ALIGN_TOP', 'wxLC_ALIGN_LEFT', 'wxLC_AUTOARRANGE',
            'wxLC_USER_TEXT', 'wxLC_EDIT_LABELS', 'wxLC_NO_HEADER',
            'wxLC_SINGLE_SEL', 'wxLC_SORT_ASCENDING', 'wxLC_SORT_DESCENDING',
            'wxLC_VIRTUAL', 'wxLC_HRULES', 'wxLC_VRULES', 'wxLC_NO_SORT_HEADER')
c.addEvents('EVT_LIST_BEGIN_DRAG',
            'EVT_LIST_BEGIN_RDRAG', 
            'EVT_LIST_BEGIN_LABEL_EDIT', 
            'EVT_LIST_END_LABEL_EDIT', 
            'EVT_LIST_DELETE_ITEM', 
            'EVT_LIST_DELETE_ALL_ITEMS', 
            'EVT_LIST_ITEM_SELECTED', 
            'EVT_LIST_ITEM_DESELECTED', 
            'EVT_LIST_KEY_DOWN', 
            'EVT_LIST_INSERT_ITEM', 
            'EVT_LIST_COL_CLICK', 
            'EVT_LIST_ITEM_RIGHT_CLICK', 
            'EVT_LIST_ITEM_MIDDLE_CLICK', 
            'EVT_LIST_ITEM_ACTIVATED', 
            'EVT_LIST_CACHE_HINT', 
            'EVT_LIST_COL_RIGHT_CLICK', 
            'EVT_LIST_COL_BEGIN_DRAG', 
            'EVT_LIST_COL_DRAGGING', 
            'EVT_LIST_COL_END_DRAG', 
            'EVT_LIST_ITEM_FOCUSED')
Manager.register(c)
Manager.setMenu(c, 'control', 'list ctrl', 'wxListCtrl', 100)
Manager.setTool(c, 'Panels', pos=(0,1))

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
c.addEvents('EVT_TREE_BEGIN_DRAG', 
            'EVT_TREE_BEGIN_RDRAG', 
            'EVT_TREE_BEGIN_LABEL_EDIT', 
            'EVT_TREE_END_LABEL_EDIT', 
            'EVT_TREE_DELETE_ITEM', 
            'EVT_TREE_GET_INFO', 
            'EVT_TREE_SET_INFO', 
            'EVT_TREE_ITEM_EXPANDED', 
            'EVT_TREE_ITEM_EXPANDING', 
            'EVT_TREE_ITEM_COLLAPSED', 
            'EVT_TREE_ITEM_COLLAPSING', 
            'EVT_TREE_SEL_CHANGED', 
            'EVT_TREE_SEL_CHANGING', 
            'EVT_TREE_KEY_DOWN', 
            'EVT_TREE_ITEM_ACTIVATED', 
            'EVT_TREE_ITEM_RIGHT_CLICK', 
            'EVT_TREE_ITEM_MIDDLE_CLICK', 
            'EVT_TREE_END_DRAG', 
            'EVT_TREE_STATE_IMAGE_CLICK', 
            'EVT_TREE_ITEM_GETTOOLTIP', 
            'EVT_TREE_ITEM_MENU')
Manager.register(c)
Manager.setMenu(c, 'control', 'tree ctrl', 'wxTreeCtrl', 110)
Manager.setTool(c, 'Panels', pos=(0,2))

### wxHtmlWindow

c = Component('wxHtmlWindow', ['control'],
              ['pos', 'size', 'borders', 'url', 'htmlcode'])
c.addStyles('wxHW_SCROLLBAR_NEVER', 'wxHW_SCROLLBAR_AUTO', 'wxHW_NO_SELECTION')
c.setParamClass('url', params.ParamLongText)
c.setParamClass('htmlcode', params.ParamMultilineText)
c.addEvents('EVT_HTML_CELL_CLICKED', 'EVT_HTML_CELL_HOVER',
            'EVT_HTML_LINK_CLICKED')
Manager.register(c)
Manager.setMenu(c, 'control', 'HTML window', 'wxHtmlWindow', 120)

### wxCalendarCtrl

c = Component('wxCalendarCtrl', ['control', 'tool'], ['pos', 'size'])
c.addStyles('wxCAL_SUNDAY_FIRST', 'wxCAL_MONDAY_FIRST', 'wxCAL_SHOW_HOLIDAYS',
            'wxCAL_NO_YEAR_CHANGE', 'wxCAL_NO_MONTH_CHANGE',
            'wxCAL_SEQUENTIAL_MONTH_SELECTION', 'wxCAL_SHOW_SURROUNDING_WEEKS')
c.addEvents('EVT_CALENDAR_SEL_CHANGED', 'EVT_CALENDAR_DAY_CHANGED',
            'EVT_CALENDAR_MONTH_CHANGED', 'EVT_CALENDAR_YEAR_CHANGED',
            'EVT_CALENDAR_DOUBLECLICKED', 'EVT_CALENDAR_WEEKDAY_CLICKED')
Manager.register(c)
Manager.setMenu(c, 'control', 'calendar ctrl', 'wxCalendarCtrl', 130)

### wxGenericDirCtrl

c = Component('wxGenericDirCtrl', ['control'],
              ['pos', 'size', 'defaultfolder', 'filter', 'defaultfilter'])
c.addStyles('wxDIRCTRL_DIR_ONLY', 'wxDIRCTRL_3D_INTERNAL', 'wxDIRCTRL_SELECT_FIRST',
            'wxDIRCTRL_SHOW_FILTERS', 'wxDIRCTRL_EDIT_LABELS')
Manager.register(c)
Manager.setMenu(c, 'control', 'generic dir ctrl', 'wxGenericDirCtrl', 160)

### wxFilePickerCtrl

c = Component('wxFilePickerCtrl', ['control'],
              ['pos', 'size', 'value', 'message', 'wildcard'])
c.addStyles('wxFLP_OPEN', 'wxFLP_SAVE', 'wxFLP_OVERWRITE_PROMPT',
            'wxFLP_FILE_MUST_EXIST', 'wxFLP_CHANGE_DIR',
            'wxFLP_DEFAULT_STYLE')
Manager.register(c)
Manager.setMenu(c, 'control', 'file picker ctrl', 'wxFilePickerCtrl', 170)
Manager.setTool(c, 'Controls', pos=(4,2))

### wxDatePickerCtrl

c = Component('wxDatePickerCtrl', ['control'], ['pos', 'size', 'borders'])
c.addStyles('wxDP_DEFAULT', 'wxDP_SPIN', 'wxDP_DROPDOWN',
            'wxDP_ALLOWNONE', 'wxDP_SHOWCENTURY')
Manager.register(c)
Manager.setMenu(c, 'control', 'date picker ctrl', 'wxDateCtrl', 180)

### wxGrid

c = Component('wxGrid', ['control'], ['pos', 'size'])
c.addEvents('EVT_GRID_CELL_LEFT_CLICK', 
            'EVT_GRID_CELL_RIGHT_CLICK', 
            'EVT_GRID_CELL_LEFT_DCLICK', 
            'EVT_GRID_CELL_RIGHT_DCLICK', 
            'EVT_GRID_LABEL_LEFT_CLICK', 
            'EVT_GRID_LABEL_RIGHT_CLICK', 
            'EVT_GRID_LABEL_LEFT_DCLICK', 
            'EVT_GRID_LABEL_RIGHT_DCLICK', 
            'EVT_GRID_ROW_SIZE', 
            'EVT_GRID_COL_SIZE', 
            'EVT_GRID_RANGE_SELECT', 
            'EVT_GRID_CELL_CHANGE', 
            'EVT_GRID_SELECT_CELL', 
            'EVT_GRID_EDITOR_SHOWN', 
            'EVT_GRID_EDITOR_HIDDEN', 
            'EVT_GRID_EDITOR_CREATED', 
            'EVT_GRID_CELL_BEGIN_DRAG')
Manager.register(c)
Manager.setMenu(c, 'control', 'grid', 'wxGrid', 190)
Manager.setTool(c, 'Panels', pos=(2,1), span=(1,2))

################################################################################
# Buttons

### wxButton

c = Component('wxButton', ['control', 'tool', 'stdbtn'],
              ['pos', 'size', 'label', 'default'])
c.addStyles('wxBU_LEFT', 'wxBU_TOP', 'wxBU_RIGHT', 'wxBU_BOTTOM', 'wxBU_EXACTFIT',
            'wxNO_BORDER')
c.setParamClass('default', params.ParamBool)
c.addEvents('EVT_BUTTON')
Manager.register(c)
Manager.setMenu(c, 'button', 'button', 'wxButton', 10)
Manager.setTool(c, 'Controls', pos=(0,1))

### wxBitmapButton

c = Component('wxBitmapButton', ['control', 'tool'],
              ['pos', 'size', 'bitmap', 'selected', 'focus', 'disabled', 'default'])
c.addStyles('wxBU_AUTODRAW', 'wxBU_LEFT', 'wxBU_RIGHT', 'wxBU_TOP', 'wxBU_BOTTOM')
c.setSpecial('bitmap', BitmapAttribute)
c.addEvents('EVT_BUTTON')
Manager.register(c)
Manager.setMenu(c, 'button', 'bitmap button', 'wxBitmapButton', 20)
Manager.setTool(c, 'Controls', pos=(1,1))

### wxRadioButton

c = Component('wxRadioButton', ['control', 'tool'], ['pos', 'size', 'label', 'value'])
c.addStyles('wxRB_GROUP', 'wxRB_SINGLE')
c.addEvents('EVT_RADIOBUTTON')
Manager.register(c)
Manager.setMenu(c, 'button', 'radio button', 'wxRadioButton', 30)
Manager.setTool(c, 'Controls', pos=(3,1))

### wxSpinButton

c = Component('wxSpinButton', ['control', 'tool'],
              ['pos', 'size', 'value', 'min', 'max'])
c.addStyles('wxSP_HORIZONTAL', 'wxSP_VERTICAL', 'wxSP_ARROW_KEYS', 'wxSP_WRAP')
c.addEvents('EVT_SPIN', 'EVT_SPIN_UP', 'EVT_SPIN_DOWN')
Manager.register(c)
Manager.setMenu(c, 'button', 'spin button', 'wxSpinButton', 40)
Manager.setTool(c, 'Controls', pos=(2,0))

### wxToggleButton

c = Component('wxToggleButton', ['control', 'tool'],
              ['pos', 'size', 'label', 'checked'])
c.addEvents('EVT_TOGGLEBUTTON')
Manager.register(c)
Manager.setMenu(c, 'button', 'toggle button', 'wxToggleButton', 50)
Manager.setTool(c, 'Controls', pos=(2,1))

################################################################################
# Boxes

### wxCheckBox

c = Component('wxCheckBox', ['control','tool'],
              ['pos', 'size', 'label', 'checked'])
c.addEvents('EVT_CHECKBOX')
Manager.register(c)
Manager.setMenu(c, 'box', 'check box', 'wxCheckBox', 10)
Manager.setTool(c, 'Controls', pos=(4,1))

### wxComboBox

c = Component('wxComboBox', ['control','tool'],
              ['pos', 'size', 'content', 'selection', 'value'])
c.setSpecial('content', ContentAttribute)
c.addEvents('EVT_COMBOBOX', 'EVT_TEXT', 'EVT_TEXT_ENTER')
Manager.register(c)
Manager.setMenu(c, 'box', 'combo box', 'wxComboBox', 20)
Manager.setTool(c, 'Controls', pos=(2,2))

### wxRadioBox

c = Component('wxRadioBox', ['control','tool'],
              ['pos', 'size', 'label', 'content', 'selection', 'dimension'])
c.addStyles('wxRA_SPECIFY_ROWS', 'wxRA_SPECIFY_COLS', 'wxRA_HORIZONTAL',
            'wxRA_VERTICAL')
c.setSpecial('content', ContentAttribute)
c.addEvents('EVT_RADIOBOX')
Manager.register(c)
Manager.setMenu(c, 'box', 'radio box', 'wxRadioBox', 30)
#Manager.setTool(c, 'Panels')

### wxListBox

c = Component('wxListBox', ['control','tool'],
              ['pos', 'size', 'content', 'selection'])
c.setSpecial('content', ContentAttribute)
c.addEvents('EVT_LISTBOX', 'EVT_LISTBOX_DCLICK')
Manager.register(c)
Manager.setMenu(c, 'box', 'list box', 'wxListBox', 40)
Manager.setTool(c, 'Panels', pos=(0,0))

### wxCheckListBox

c = Component('wxCheckListBox', ['control','tool'],
              ['pos', 'size', 'content', 'selection'])
c.setSpecial('content', CheckContentAttribute)
c.setParamClass('content', params.ParamContentCheckList)
c.addEvents('EVT_CHECKLISTBOX')
Manager.register(c)
Manager.setMenu(c, 'box', 'check list box', 'wxCheckListBox', 50)
#Manager.setTool(c, 'Panels', pos=(0,0))

### wxStaticBox

c = Component('wxStaticBox', ['control','tool'],
              ['pos', 'size', 'label'])
Manager.register(c)
Manager.setMenu(c, 'box', 'static box', 'wxStaticBox', 60)
Manager.setTool(c, 'Panels', pos=(2,0))

### wxXXX

#c = Component('wxXXX', ['control','tool'],
#              ['pos', 'size', ...])
#c.addStyles(...)
#Manager.register(c)
#Manager.setMenu(c, 'control', 'XXX', 'wxXXX', NN)
