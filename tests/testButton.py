"""Unit tests for wx.Button.

Methods yet to test:
__init__, Create"""

import unittest
import wx

import testControl

def getIdLabelPairs(without_mnemonic=True):
    """ID/Label pairs were copied from the docs, or alternately from
    the most recent version of _button.i (the docs should update shortly).
    The stock labels can be tough to peg down.
    For more information, see issue #1756947
    """
    pairs = (
                (wx.ID_ABOUT,       '&About...'),
                (wx.ID_ADD,         'Add'),
                (wx.ID_APPLY,       '&Apply'),
                (wx.ID_BOLD,        '&Bold'),
                (wx.ID_CLEAR,       '&Clear'),
                (wx.ID_CLOSE,       '&Close'),
                (wx.ID_COPY,        '&Copy'),
                (wx.ID_CUT,         'Cu&t'),
                (wx.ID_DELETE,      '&Delete'),
                (wx.ID_EDIT,        '&Edit'),
                (wx.ID_FIND,        '&Find'),
                (wx.ID_FILE,        '&File'),
                (wx.ID_REPLACE,     'Rep&lace'),
                (wx.ID_BACKWARD,    '&Back'),
                (wx.ID_DOWN,        '&Down'),
                (wx.ID_FORWARD,     '&Forward'),
                (wx.ID_UP,          '&Up'),
                (wx.ID_HELP,        '&Help'),
                (wx.ID_HOME,        '&Home'),
                (wx.ID_INDENT,      'Indent'),
                (wx.ID_INDEX,       '&Index'),
                (wx.ID_ITALIC,      '&Italic'),
                (wx.ID_JUSTIFY_CENTER, 'Centered'),
                (wx.ID_JUSTIFY_FILL, 'Justified'),
                (wx.ID_JUSTIFY_LEFT, 'Align Left'),
                (wx.ID_JUSTIFY_RIGHT, 'Align Right'),
                (wx.ID_NEW,         '&New'),
                (wx.ID_NO,          '&No'),
                (wx.ID_OK,          '&OK'),
                (wx.ID_OPEN,        '&Open...'),
                (wx.ID_PASTE,       '&Paste'),
                (wx.ID_PREFERENCES, '&Preferences'),
                (wx.ID_PRINT,       '&Print...'),
                (wx.ID_PREVIEW,     'Print previe&w'),
                (wx.ID_PROPERTIES,  '&Properties'),
                (wx.ID_EXIT,        '&Quit'),
                (wx.ID_REDO,        '&Redo'),
                (wx.ID_REFRESH,     'Refresh'),
                (wx.ID_REMOVE,      'Remove'),
                (wx.ID_REVERT_TO_SAVED, 'Revert to Saved'),
                (wx.ID_SAVE,        '&Save'),
                (wx.ID_SAVEAS,      'Save &As...'),
                (wx.ID_SELECTALL,   'Select All'),
                (wx.ID_STOP,        '&Stop'),
                (wx.ID_UNDELETE,    'Undelete'),
                (wx.ID_UNDERLINE,   '&Underline'),
                (wx.ID_UNDO,        '&Undo'),
                (wx.ID_UNINDENT,    '&Unindent'),
                (wx.ID_YES,         '&Yes'),
                (wx.ID_ZOOM_100,    '&Actual Size'),
                (wx.ID_ZOOM_FIT,    'Zoom to &Fit'),
                (wx.ID_ZOOM_IN,     'Zoom &In'),
                (wx.ID_ZOOM_OUT,    'Zoom &Out')
        )
    if without_mnemonic:
        return tuple( (id,label.replace('&','')) for id,label in pairs )
    else:
        return pairs
        

# -----------------------------------------------------------

class ButtonTest(testControl.ControlTest):
    def setUp(self):
        self.frame = wx.Frame(parent=None, id=wx.ID_ANY)
        self.testControl = wx.Button(parent=self.frame)
    
    def testGetDefaultSize_wxButtonOnly(self):
        """GetDefaultSize"""
        # (Static method)
        sz = wx.Button.GetDefaultSize()
        self.assert_(isinstance(sz, wx.Size))
        self.assert_(sz.IsFullySpecified())
        
    def testIdLabelPairs(self):
        """GetLabelText"""
        # Test the ID/Label pairs"""
        for id,label in getIdLabelPairs():
            b = wx.Button(self.frame, id)
            # On Mac, there is a special help button so there won't be
            # a label on the button
            if "__WXMAC__" in wx.PlatformInfo and id == wx.ID_HELP:
                label = ""
            self.assertEquals(label, b.GetLabelText())
    
    def testSetDefault(self):
        """SetDefault"""
        self.testControl.SetDefault()
        self.assertEquals(self.testControl, self.frame.DefaultItem)
        

if __name__ == '__main__':
    unittest.main()
