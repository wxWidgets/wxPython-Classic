/////////////////////////////////////////////////////////////////////////////
// Name:        _cmdlinkbtn.i
// Purpose:     SWIG interface for wxCommandLinkButton
//
// Author:      Robin Dunn
//
// Created:     20-Oct-2010
// RCS-ID:      $Id: $
// Copyright:   (c) 2010 by Total Control Software
// Licence:     wxWindows license
/////////////////////////////////////////////////////////////////////////////

// Not a %module


//---------------------------------------------------------------------------
%newgroup

class wxCommandLinkButton : public wxButton
{
public:

    %pythonAppend wxCommandLinkButton         "self._setOORInfo(self)"
    %pythonAppend wxCommandLinkButton()       ""
    %typemap(out) wxCommandLinkButton*;    // turn off this typemap
    
    
    wxCommandLinkButton(wxWindow *parent,
                        wxWindowID id = -1,
                        const wxString& mainLabel = wxEmptyString,
                        const wxString& note = wxEmptyString,
                        const wxPoint& pos = wxDefaultPosition,
                        const wxSize& size = wxDefaultSize,
                        long style = 0,
                        const wxValidator& validator = wxDefaultValidator,
                        const wxString& name = wxButtonNameStr);

    DocCtorStrName(
        wxCommandLinkButton(),
        "Precreate a Button for 2-phase creation.", "",
        PreCommandLinkButton);

    // Turn it back on again
    %typemap(out) wxCommandLinkButton* { $result = wxPyMake_wxObject($1, $owner); }

    bool Create(wxWindow *parent,
                wxWindowID id=-1,
                const wxString& mainLabel = wxEmptyString,
                const wxString& note = wxEmptyString,
                const wxPoint& pos = wxDefaultPosition,
                const wxSize& size = wxDefaultSize,
                long style = 0,
                const wxValidator& validator = wxDefaultValidator,
                const wxString& name = wxButtonNameStr);

    
    virtual void SetMainLabelAndNote(const wxString& mainLabel,
                                     const wxString& note);

    virtual void SetMainLabel(const wxString& mainLabel);
    virtual void SetNote(const wxString& note);
    virtual wxString GetMainLabel() const;
    virtual wxString GetNote() const;

    %property(MainLabel, GetMainLabel, SetMainLabel);
    %property(Note, GetNote, SetNote);

};


//---------------------------------------------------------------------------
