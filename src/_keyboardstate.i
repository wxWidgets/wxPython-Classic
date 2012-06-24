/////////////////////////////////////////////////////////////////////////////
// Name:        _keyboardstate.i
// Purpose:     SWIG interface for wx.KeyboardState
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


DocStr(wxKeyboardState,
       "wx.KeyboardState stores the state of the keyboard modifier keys", "");

class wxKeyboardState
{
public:
    wxKeyboardState(bool controlDown = false,
                    bool shiftDown = false,
                    bool altDown = false,
                    bool metaDown = false);
    ~wxKeyboardState();
    
    DocDeclStr(
        int, GetModifiers() const,
        "Returns a bitmask of the current modifier settings.  Can be used to
check if the key event has exactly the given modifiers without having
to explicitly check that the other modifiers are not down.  For
example::

    if event.GetModifers() == wx.MOD_CONTROL:
        DoSomething()
", "");

    %property(Modifiers, GetModifiers, doc="See `GetModifiers`");


    DocDeclStr(
        bool , ControlDown() const,
        "Returns ``True`` if the Control key was down at the time of the event.", "");

    bool RawControlDown() const;
    void SetRawControlDown(bool down);

    DocDeclStr(
        bool , MetaDown() const,
        "Returns ``True`` if the Meta key was down at the time of the event.", "");

    DocDeclStr(
        bool , AltDown() const,
        "Returns ``True`` if the Alt key was down at the time of the event.", "");

    DocDeclStr(
        bool , ShiftDown() const,
        "Returns ``True`` if the Shift key was down at the time of the event.", "");


    DocDeclStr(
        bool , CmdDown() const,
        "\"Cmd\" is a pseudo key which is the same as Control for PC and Unix
platforms but the special \"Apple\" (a.k.a as \"Command\") key on
Macs. It makes often sense to use it instead of, say, `ControlDown`
because Cmd key is used for the same thing under Mac as Ctrl
elsewhere. The Ctrl still exists, it's just not used for this
purpose. So for non-Mac platforms this is the same as `ControlDown`
and Macs this is the same as `MetaDown`.", "");


    DocDeclStr(
        bool , HasModifiers() const,
        "Returns true if either CTRL or ALT keys was down at the time of the
key event. Note that this function does not take into account neither
SHIFT nor META key states (the reason for ignoring the latter is that
it is common for NUMLOCK key to be configured as META under X but the
key presses even while NUMLOCK is on should be still processed
normally).", "");


    void SetControlDown(bool down);
    void SetShiftDown(bool down);
    void SetAltDown(bool down);
    void SetMetaDown(bool down);


    %pythoncode {
        controlDown = property(ControlDown, SetControlDown)
        rawControlDown = property(RawControlDown, SetRawControlDown)
        shiftDown = property(ShiftDown, SetShiftDown)
        altDown = property(AltDown, SetAltDown)
        metaDown = property(MetaDown, SetMetaDown)
        cmdDown = property(CmdDown)

        # For 2.8 compatibility
        m_controlDown = wx.deprecated(controlDown)
        m_shiftDown = wx.deprecated(shiftDown)
        m_altDown = wx.deprecated(altDown)
        m_metaDown = wx.deprecated(metaDown)            
    }
};

