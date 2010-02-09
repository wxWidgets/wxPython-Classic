/////////////////////////////////////////////////////////////////////////////
// Name:        _mousestate.i
// Purpose:     SWIG interface for wx.MouseState
//
// Author:      Robin Dunn
//
// Created:     1-Feb-2010
// RCS-ID:      $Id$
// Copyright:   (c) 2010 by Total Control Software
// Licence:     wxWindows license
/////////////////////////////////////////////////////////////////////////////

// Not a %module



//---------------------------------------------------------------------------
%newgroup;

// the symbolic names for the mouse buttons
enum wxMouseButton
{
    wxMOUSE_BTN_ANY,
    wxMOUSE_BTN_NONE,
    wxMOUSE_BTN_LEFT,
    wxMOUSE_BTN_MIDDLE,
    wxMOUSE_BTN_RIGHT,
    wxMOUSE_BTN_AUX1,
    wxMOUSE_BTN_AUX2,
    wxMOUSE_BTN_MAX
};



DocStr(wxMouseState,
"`wx.MouseState` is used to hold information about mouse button and
modifier key states and is what is returned from `wx.GetMouseState`.",
"");

class wxMouseState : public wxKeyboardState
{
public:
    wxMouseState();
    ~wxMouseState();

    wxCoord     GetX();
    wxCoord     GetY();
    wxPoint     GetPosition() const;
    DocDeclAName(
        void, GetPosition(long *OUTPUT, long *OUTPUT),
        "GetPositionTuple() -> (x,y)",
        GetPositionTuple);
    
    bool        LeftIsDown();
    bool        MiddleIsDown();
    bool        RightIsDown();
    bool        Aux1IsDown();
    bool        Aux2IsDown();

    bool ButtonIsDown(wxMouseButton but) const;

    %pythoncode {
        LeftDown = wx._deprecated(LeftIsDown)
        MiddleDown = wx._deprecated(MiddleIsDown)
        RightDown = wx._deprecated(RightIsDown)            
    }
    
    void        SetX(wxCoord x);
    void        SetY(wxCoord y);
    void        SetPosition(wxPoint pos);
    
    void        SetLeftDown(bool down);
    void        SetMiddleDown(bool down);
    void        SetRightDown(bool down);
    void        SetAux1Down(bool down);
    void        SetAux2Down(bool down);

    void        SetState(const wxMouseState& state);
    

    %pythoncode {
        x = property(GetX, SetX)
        y = property(GetY, SetY)
        leftIsDown = property(LeftIsDown, SetLeftDown)
        middleIsDown = property(MiddleIsDown, SetMiddleDown)
        rightIsDown = property(RightIsDown, SetRightDown)
        aux1IsDown = property(Aux1IsDown, SetAux1Down)
        aux2IsDown = property(Aux2IsDown, SetAux2Down)
    }
    %property(Position, GetPosition, doc="See `GetPosition`");
};


DocDeclStr(
    wxMouseState , wxGetMouseState(),
    "Returns the current state of the mouse.  Returns an instance of a
`wx.MouseState` object that contains the current position of the mouse
pointer in screen coordinants, as well as boolean values indicating
the up/down status of the mouse buttons and the modifier keys.", "");


