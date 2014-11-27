/////////////////////////////////////////////////////////////////////////////
// Name:        _infobar.i
// Purpose:     SWIG interface for wxInfoBar
//
// Author:      Robin Dunn
//
// Created:     2-March-2010
// RCS-ID:      $Id: $
// Copyright:   (c) 2010 by Total Control Software
// Licence:     wxWindows license
/////////////////////////////////////////////////////////////////////////////

// Not a %module

//---------------------------------------------------------------------------
%newgroup

MustHaveApp(wxInfoBar);
DocStr(wxInfoBar,
"An info bar is a transient window shown at top or bottom of its parent
window to display non-critical information to the user.  It works
similarly to message bars in current web browsers.", "");


class wxInfoBar : public wxControl
{
public:
    %pythonAppend wxInfoBar         "self._setOORInfo(self)";
    %pythonAppend wxInfoBar()       "";

    wxInfoBar(wxWindow *parent, wxWindowID winid = wxID_ANY);
    %RenameCtor(PreInfoBar, wxInfoBar());

    bool Create(wxWindow *parent, wxWindowID winid = wxID_ANY);


    // show the info bar with the given message and optionally an icon
    virtual void ShowMessage(const wxString& msg,
                             int flags = wxICON_INFORMATION);

    // hide the info bar
    virtual void Dismiss();

    // add an extra button to the bar, near the message (replacing the default
    // close button which is only shown if no extra buttons are used)
    virtual void AddButton(wxWindowID btnid,
                           const wxString& label = wxEmptyString);

    // remove a button previously added by AddButton()
    virtual void RemoveButton(wxWindowID btnid);


    // Generic version only.  GTK doesn't have these??
    void SetShowHideEffects(wxShowEffect showEffect, wxShowEffect hideEffect);
    wxShowEffect GetShowEffect() const;
    wxShowEffect GetHideEffect() const;
    void SetEffectDuration(int duration);
    int GetEffectDuration() const;
    
};

//---------------------------------------------------------------------------
