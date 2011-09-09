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

    bool KeyDown(int, int) { return false; }
    bool KeyUp(int, int) { return false; }
    bool Char(int, int) { return false; }
    bool Text(const char *) { return false; }
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

    // Mouse simulation
    %nokwargs MouseMove;
    bool MouseMove(long x, long y);
    bool MouseMove(const wxPoint& point);
    
    bool MouseDown(int button = wxMOUSE_BTN_LEFT);
    bool MouseUp(int button = wxMOUSE_BTN_LEFT);
    
    bool MouseClick(int button = wxMOUSE_BTN_LEFT);
    bool MouseDblClick(int button = wxMOUSE_BTN_LEFT);
    bool MouseDragDrop(long x1, long y1, long x2, long y2,
                              int button = wxMOUSE_BTN_LEFT);

    // Keyboard simulation
    // Low level methods for generating key presses and releases
    bool KeyDown(int keycode, int modifiers = wxMOD_NONE);

    bool KeyUp(int keycode, int modifiers = wxMOD_NONE);

    // Higher level methods for generating both the key press and release for a
    // single key or for all characters in the ASCII string "text" which can
    // currently contain letters only (no digits, no punctuation).
    bool Char(int keycode, int modifiers = wxMOD_NONE);
    bool Text(const char *text);


};


//---------------------------------------------------------------------------
