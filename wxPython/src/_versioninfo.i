/////////////////////////////////////////////////////////////////////////////
// Name:        _versioninfo.i
// Purpose:     SWIG interface for wxVersionInfo
//
// Author:      Robin Dunn
//
// Created:     27-Nov-2010
// RCS-ID:      $Id: _template.i 24541 2003-11-12 21:34:20Z RD $
// Copyright:   (c) 2010 by Total Control Software
// Licence:     wxWindows license
/////////////////////////////////////////////////////////////////////////////

// Not a %module


//---------------------------------------------------------------------------
%newgroup

class wxVersionInfo
{
public:
    wxVersionInfo(const wxString& name,
                  int major,
                  int minor,
                  int micro = 0,
                  const wxString& description = wxEmptyString,
                  const wxString& copyright = wxEmptyString);

    // Default copy ctor, assignment operator and dtor are ok.


    const wxString& GetName() const;

    int GetMajor() const;
    int GetMinor() const;
    int GetMicro() const;

    wxString ToString() const;

    wxString GetVersionString() const;

    bool HasDescription() const;
    const wxString& GetDescription() const;

    bool HasCopyright() const;
    const wxString& GetCopyright() const;
};


//---------------------------------------------------------------------------
