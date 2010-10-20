// NOTE: This module is in the demo because I started adding support
// for the UIAction class but found that it was not fully implemented
// at the time and now its API is going to be having big changes in
// 2.9.2 so for now wxPython support for the class is on hold.  Just
// ignore this module for now...



/////////////////////////////////////////////////////////////////////////////
// Name:        _uiaction.i
// Purpose:     SWIG interface for wxUIActionSimulator
//
// Author:      Robin Dunn
//
// Created:     30-Mar-2010
// RCS-ID:      $Id: $
// Copyright:   (c) 2010 by Total Control Software
// Licence:     wxWindows license
/////////////////////////////////////////////////////////////////////////////

// Not a %module

%{
#include <wx/uiaction.h>
%}

//---------------------------------------------------------------------------
// Empty implementation of the class if wxWidgets doesn't have it

%{
#if !wxUSE_UIACTIONSIMULATOR    
class wxUIActionSimulator
{
public:
    wxUIActionSimulator() {
        wxPyRaiseNotImplementedMsg(
            "wx.UIActionSimulator is not available in this build of wxWidgets.");
    }
    ~wxUIActionSimulator() {}

    bool MouseMove(long, long) { return false; }
    bool MouseDown(int) { return false; }
    bool MouseUp(int) { return false; }
    bool MouseClick(int) { return false; }
    bool MouseDblClick(int) { return false; }
    bool MouseDragDrop(long, long, long, long, int) { return false; }
    bool KeyDown(int, bool, bool, bool) { return false; }
    bool KeyUp(int, bool, bool, bool) { return false; }
    bool Char(int, bool, bool, bool) { return false; }
};
#endif    
%}


//---------------------------------------------------------------------------
%newgroup

class wxUIActionSimulator
{
public:
    wxUIActionSimulator();
    ~wxUIActionSimulator();

    // Mouse related
    bool        MouseMove(long x, long y);
    bool        MouseDown(int button = wxMOUSE_BTN_LEFT);
    bool        MouseUp(int button = wxMOUSE_BTN_LEFT);
    bool        MouseClick(int button = wxMOUSE_BTN_LEFT);
    bool        MouseDblClick(int button = wxMOUSE_BTN_LEFT);
    bool        MouseDragDrop(long x1, long y1, long x2, long y2,
                              int button = wxMOUSE_BTN_LEFT);

    // Keyboard related
    bool        KeyDown(int keycode, bool shiftDown=false, bool cmdDown=false, bool altDown=false);
    bool        KeyUp(int keycode, bool shiftDown=false, bool cmdDown=false, bool altDown=false);
    bool        Char(int keycode, bool shiftDown=false, bool cmdDown=false, bool altDown=false);

};


//---------------------------------------------------------------------------
