/////////////////////////////////////////////////////////////////////////////
// Name:        _filectrl.i
// Purpose:     SWIG interface for wxFileCtrl
//
// Author:      Robin Dunn
//
// Created:     4-Nov-2008
// RCS-ID:      $Id: $
// Copyright:   (c) 2008 by Total Control Software
// Licence:     wxWindows license
/////////////////////////////////////////////////////////////////////////////

// Not a %module

//---------------------------------------------------------------------------
%newgroup

MAKE_CONST_WXSTRING(FileCtrlNameStr);


enum
{
    wxFC_OPEN,
    wxFC_SAVE,
    wxFC_MULTIPLE,
    wxFC_NOSHOWHIDDEN,

    wxFC_DEFAULT_STYLE
};



MustHaveApp(wxFileCtrl);
DocStr(wxFileCtrl,
"
", "
");


class wxFileCtrl : public wxWindow  // wxControl on GTK, wxPanel on generic...
{
public:
    %pythonAppend wxFileCtrl         "self._setOORInfo(self)";
    %pythonAppend wxFileCtrl()       "";

    wxFileCtrl(wxWindow *parent,
               wxWindowID id=-1,
               const wxString& defaultDirectory = wxEmptyString,
               const wxString& defaultFilename = wxEmptyString,
               const wxString& wildCard = wxFileSelectorDefaultWildcardStr,
               long style = wxFC_DEFAULT_STYLE,
               const wxPoint& pos = wxDefaultPosition,
               const wxSize& size = wxDefaultSize,
               const wxString& name = wxPyFileCtrlNameStr);


    DocCtorStrName(
        wxFileCtrl(),
        "Precreate a wx.FileCtrl for 2-phase creation.", "",
        PreFileCtrl);

    bool Create(wxWindow *parent,
                wxWindowID id=-1,
                const wxString& defaultDirectory = wxEmptyString,
                const wxString& defaultFilename = wxEmptyString,
                const wxString& wildCard = wxFileSelectorDefaultWildcardStr,
                long style = wxFC_DEFAULT_STYLE,
                const wxPoint& pos = wxDefaultPosition,
                const wxSize& size = wxDefaultSize,
                const wxString& name = wxPyFileCtrlNameStr);

    
    virtual void SetWildcard( const wxString& wildCard );
    virtual void SetFilterIndex( int filterindex );
    virtual bool SetDirectory( const wxString& dir );
    virtual bool SetFilename( const wxString& name );
    virtual bool SetPath( const wxString& path );

    virtual wxString GetFilename() const;
    virtual wxString GetDirectory() const;
    virtual wxString GetWildcard() const;
    virtual wxString GetPath() const;
    virtual int GetFilterIndex() const;
    
    // virtual void GetPaths( wxArrayString& paths ) const;
    // virtual void GetFilenames( wxArrayString& files ) const;
    %extend {
        wxArrayString GetPaths() {
            wxArrayString rval;
            self->GetPaths(rval);
            return rval;
        }
        
        wxArrayString GetFilenames() {
            wxArrayString rval;
            self->GetFilenames(rval);
            return rval;
        }            
    }

    virtual bool HasMultipleFileSelection() const;
    virtual void ShowHidden(bool show);

    %property(Filename, GetFilename, SetFilename);
    %property(Directory, GetDirectory, SetDirectory);
    %property(Wildcard, GetWildcard, SetWildcard);
    %property(Path, GetPath, SetPath);
    %property(FilterIndex, GetFilterIndex, SetFilterIndex);
    %property(Paths, GetPaths);
    %property(Filenames, GetFilenames);

};



class  wxFileCtrlEvent : public wxCommandEvent
{
public:
    wxFileCtrlEvent( wxEventType type, wxObject *evtObject, int id );

    // no need for the copy constructor as the default one will be fine.
    virtual wxEvent *Clone() const;

    void SetFiles( const wxArrayString &files );
    void SetDirectory( const wxString &directory );
    void SetFilterIndex(int filterIndex);

    wxArrayString GetFiles() const;
    wxString GetDirectory() const;
    int GetFilterIndex() const;

    wxString GetFile() const;

    %property(Files, GetFiles, SetFiles);
    %property(Directory, GetDirectory, SetDirectory);
    %property(FilterIndex, GetFilterIndex, SetFilterIndex);
};


%constant wxEventType wxEVT_FILECTRL_SELECTIONCHANGED;
%constant wxEventType wxEVT_FILECTRL_FILEACTIVATED;
%constant wxEventType wxEVT_FILECTRL_FOLDERCHANGED;
%constant wxEventType wxEVT_FILECTRL_FILTERCHANGED;


%pythoncode {
    EVT_FILECTRL_SELECTIONCHANGED = wx.PyEventBinder( wxEVT_FILECTRL_SELECTIONCHANGED, 1)
    EVT_FILECTRL_FILEACTIVATED = wx.PyEventBinder( wxEVT_FILECTRL_FILEACTIVATED, 1)
    EVT_FILECTRL_FOLDERCHANGED = wx.PyEventBinder( wxEVT_FILECTRL_FOLDERCHANGED, 1)
    EVT_FILECTRL_FILTERCHANGED = wx.PyEventBinder( wxEVT_FILECTRL_FILTERCHANGED, 1)
}

//---------------------------------------------------------------------------

