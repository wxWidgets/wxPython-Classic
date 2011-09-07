/////////////////////////////////////////////////////////////////////////////
// Name:        _button.i
// Purpose:     SWIG interface defs for wxButton, wxBitmapButton
//
// Author:      Robin Dunn
//
// Created:     10-June-1998
// RCS-ID:      $Id$
// Copyright:   (c) 2003 by Total Control Software
// Licence:     wxWindows license
/////////////////////////////////////////////////////////////////////////////

// Not a %module


//---------------------------------------------------------------------------
%newgroup;

MAKE_CONST_WXSTRING(ButtonNameStr);

enum {
    wxBU_LEFT,
    wxBU_TOP,
    wxBU_RIGHT,
    wxBU_BOTTOM,

    wxBU_ALIGN_MASK,

    wxBU_EXACTFIT,
    wxBU_AUTODRAW,
    wxBU_NOTEXT,
};

//---------------------------------------------------------------------------

class wxAnyButton : public wxControl
{
public:
    // wxAnyButtonBase();   **** it's an ABC, hide the ctor


    // show the image in the button in addition to the label: this method is
    // supported on all (major) platforms
    void SetBitmap(const wxBitmap& bitmap, wxDirection dir = wxLEFT);
    wxBitmap GetBitmap() const;
    %property(Bitmap, GetBitmap, SetBitmap);
    

    // Methods for setting individual images for different states: normal,
    // selected (meaning pushed or pressed), focused (meaning normal state for
    // a focused button), disabled or hover (a.k.a. hot or current).
    //
    // Remember that SetBitmap() itself must be called before any other
    // SetBitmapXXX() methods (except for SetBitmapLabel() which is a synonym
    // for it anyhow) and that all bitmaps passed to these functions should be
    // of the same size.
    void SetBitmapLabel(const wxBitmap& bitmap);
    void SetBitmapPressed(const wxBitmap& bitmap);
    void SetBitmapDisabled(const wxBitmap& bitmap);
    void SetBitmapCurrent(const wxBitmap& bitmap);
    void SetBitmapFocus(const wxBitmap& bitmap);
    

    wxBitmap GetBitmapLabel() const;
    wxBitmap GetBitmapPressed() const;
    wxBitmap GetBitmapDisabled() const;
    wxBitmap GetBitmapCurrent() const;
    wxBitmap GetBitmapFocus() const;

    %property(BitmapLabel, GetBitmapLabel, SetBitmapLabel );
    %property(BitmapPressed, GetBitmapPressed, SetBitmapPressed );
    %property(BitmapDisabled, GetBitmapDisabled, SetBitmapDisabled );
    %property(BitmapCurrent, GetBitmapCurrent, SetBitmapCurrent );
    %property(BitmapFocus, GetBitmapFocus, SetBitmapFocus );

    // backwards compatible names
    wxBitmap GetBitmapSelected() const { return GetBitmapPressed(); }
    wxBitmap GetBitmapHover() const { return GetBitmapCurrent(); }
    void SetBitmapSelected(const wxBitmap& bitmap) { SetBitmapPressed(bitmap); }
    void SetBitmapHover(const wxBitmap& bitmap) { SetBitmapCurrent(bitmap); }
    %property(BitmapSelected, GetBitmapSelected, SetBitmapSelected);
    %property(BitmapHover, GetBitmapHover, SetBitmapHover);

    
    // set the margins around the image
    %nokwargs SetBitmapMargins;
    void SetBitmapMargins(wxCoord x, wxCoord y);
    void SetBitmapMargins(const wxSize& sz);
    wxSize GetBitmapMargins();
    %property(BitmapMargins, GetBitmapMargins, SetBitmapMargins);
    

    // set the image position relative to the text, i.e. wxLEFT means that the
    // image is to the left of the text (this is the default)
    void SetBitmapPosition(wxDirection dir);

    // return true if this button shouldn't show the text label, either because
    // it doesn't have it or because it was explicitly disabled with wxBU_NOTEXT
    bool DontShowLabel() const;
    bool ShowsLabel() const;




    

    
};

//---------------------------------------------------------------------------

DocStr(wxButton,
"A button is a control that contains a text string, and is one of the most
common elements of a GUI.  It may be placed on a dialog box or panel, or
indeed almost any other window.", "

Window Styles
-------------
    ==============   ==========================================
    wx.BU_LEFT       Left-justifies the label. Windows and GTK+ only.
    wx.BU_TOP        Aligns the label to the top of the button.
                     Windows and GTK+ only.
    wx.BU_RIGHT      Right-justifies the bitmap label. Windows and GTK+ only.
    wx.BU_BOTTOM     Aligns the label to the bottom of the button.
                     Windows and GTK+ only.
    wx.BU_EXACTFIT   Creates the button as small as possible
                     instead of making it of the standard size
                     (which is the default behaviour.)
    wx.BU_NOTEXT
    ==============   ==========================================

Events
------
    ============     ==========================================
    EVT_BUTTON       Sent when the button is clicked.
    ============     ==========================================

:see: `wx.BitmapButton`
");


MustHaveApp(wxButton);
MustHaveApp(wxButton::GetDefaultSize);

class wxButton : public wxAnyButton
{
public:
    %pythonAppend wxButton         "self._setOORInfo(self)"
    %pythonAppend wxButton()       ""
    %typemap(out) wxButton*;    // turn off this typemap


    DocCtorStr(
        wxButton(wxWindow* parent, wxWindowID id=-1,
                 const wxString& label=wxPyEmptyString,
                 const wxPoint& pos = wxDefaultPosition,
                 const wxSize& size = wxDefaultSize,
                 long style = 0,
                 const wxValidator& validator = wxDefaultValidator,
                 const wxString& name = wxPyButtonNameStr),
        "Create and show a button.  The preferred way to create standard
buttons is to use a standard ID and an empty label.  In this case
wxWigets will automatically use a stock label that corresponds to the
ID given.  These labels may vary across platforms as the platform
itself will provide the label if possible.  In addition, the button
will be decorated with stock icons under GTK+ 2.", "

The stock IDs and sample labels are

    =====================   ======================
    wx.ID_ABOUT             '&About'
    wx.ID_ADD               'Add'
    wx.ID_APPLY             '&Apply'
    wx.ID_BOLD              '&Bold'
    wx.ID_CANCEL            '&Cancel'
    wx.ID_CLEAR             '&Clear'
    wx.ID_CLOSE             '&Close'
    wx.ID_COPY              '&Copy'
    wx.ID_CUT               'Cu&t'
    wx.ID_DELETE            '&Delete'
    wx.ID_EDIT              '&Edit'
    wx.ID_FIND              '&Find'
    wx.ID_FILE              '&File'
    wx.ID_REPLACE           'Rep&lace'
    wx.ID_BACKWARD          '&Back'
    wx.ID_DOWN              '&Down'
    wx.ID_FORWARD           '&Forward'
    wx.ID_UP                '&Up'
    wx.ID_HELP              '&Help'
    wx.ID_HOME              '&Home'
    wx.ID_INDENT            'Indent'
    wx.ID_INDEX             '&Index'
    wx.ID_ITALIC            '&Italic'
    wx.ID_JUSTIFY_CENTER    'Centered'
    wx.ID_JUSTIFY_FILL      'Justified'
    wx.ID_JUSTIFY_LEFT      'Align Left'
    wx.ID_JUSTIFY_RIGHT     'Align Right'
    wx.ID_NEW               '&New'
    wx.ID_NO                '&No'
    wx.ID_OK                '&OK'
    wx.ID_OPEN              '&Open'
    wx.ID_PASTE             '&Paste'
    wx.ID_PREFERENCES       '&Preferences'
    wx.ID_PRINT             '&Print'
    wx.ID_PREVIEW           'Print previe&w'
    wx.ID_PROPERTIES        '&Properties'
    wx.ID_EXIT              '&Quit'
    wx.ID_REDO              '&Redo'
    wx.ID_REFRESH           'Refresh'
    wx.ID_REMOVE            'Remove'
    wx.ID_REVERT_TO_SAVED   'Revert to Saved'
    wx.ID_SAVE              '&Save'
    wx.ID_SAVEAS            'Save &As...'
    wx.ID_SELECTALL         'Select all'
    wx.ID_STOP              '&Stop'
    wx.ID_UNDELETE          'Undelete'
    wx.ID_UNDERLINE         '&Underline'
    wx.ID_UNDO              '&Undo'
    wx.ID_UNINDENT          '&Unindent'
    wx.ID_YES               '&Yes'
    wx.ID_ZOOM_100          '&Actual Size'
    wx.ID_ZOOM_FIT          'Zoom to &Fit'
    wx.ID_ZOOM_IN           'Zoom &In'
    wx.ID_ZOOM_OUT          'Zoom &Out'
    =====================   ======================
");

    DocCtorStrName(
        wxButton(),
        "Precreate a Button for 2-phase creation.", "",
        PreButton);

    // Turn it back on again
    %typemap(out) wxButton* { $result = wxPyMake_wxObject($1, $owner); }


    DocDeclStr(
        bool , Create(wxWindow* parent, wxWindowID id=-1,
                      const wxString& label=wxPyEmptyString,
                      const wxPoint& pos = wxDefaultPosition,
                      const wxSize& size = wxDefaultSize,
                      long style = 0,
                      const wxValidator& validator = wxDefaultValidator,
                      const wxString& name = wxPyButtonNameStr),
        "Acutally create the GUI Button for 2-phase creation.", "");



    // show the authentication needed symbol on the button: this is currently
    // only implemented on Windows Vista and newer (on which it shows the UAC
    // shield symbol)
    void SetAuthNeeded(bool show = true);
    bool GetAuthNeeded() const;

    
    DocDeclStr(
        wxWindow* , SetDefault(),
        "This sets the button to be the default item for the panel or dialog box.", "");

    DocDeclStr(
        static wxSize , GetDefaultSize(),
        "Returns the default button size for this platform.", "");   

    
    static wxVisualAttributes
    GetClassDefaultAttributes(wxWindowVariant variant = wxWINDOW_VARIANT_NORMAL);
};



//---------------------------------------------------------------------------


DocStr(wxBitmapButton,
"A Button that contains a bitmap.  A bitmap button can be supplied with a
single bitmap, and wxWidgets will draw all button states using this bitmap. If
the application needs more control, additional bitmaps for the selected state,
unpressed focused state, and greyed-out state may be supplied.", "       

Window Styles
-------------
    ==============  =============================================
    wx.BU_AUTODRAW  If this is specified, the button will be drawn
                    automatically using the label bitmap only,
                    providing a 3D-look border. If this style is
                    not specified, the button will be drawn
                    without borders and using all provided
                    bitmaps. WIN32 only.
    wx.BU_LEFT      Left-justifies the label. WIN32 only.
    wx.BU_TOP       Aligns the label to the top of the button. WIN32
                    only.
    wx.BU_RIGHT     Right-justifies the bitmap label. WIN32 only.
    wx.BU_BOTTOM    Aligns the label to the bottom of the
                    button. WIN32 only.
    wx.BU_EXACTFIT  Creates the button as small as possible
                    instead of making it of the standard size
                    (which is the default behaviour.)
    ==============  =============================================

Events
------
     ===========   ==================================
     EVT_BUTTON    Sent when the button is clicked.
     ===========   ==================================

:see: `wx.Button`, `wx.Bitmap`
");

MustHaveApp(wxBitmapButton);

class wxBitmapButton : public wxButton
{
public:
    %pythonAppend wxBitmapButton         "self._setOORInfo(self)"
    %pythonAppend wxBitmapButton()       ""
    %typemap(out) wxBitmapButton*;    // turn off this typemap

    DocCtorStr(
        wxBitmapButton(wxWindow* parent, wxWindowID id=-1,
                       const wxBitmap& bitmap = wxNullBitmap,
                       const wxPoint& pos = wxDefaultPosition,
                       const wxSize& size = wxDefaultSize,
                       long style = wxBU_AUTODRAW,
                       const wxValidator& validator = wxDefaultValidator,
                       const wxString& name = wxPyButtonNameStr),
        "Create and show a button with a bitmap for the label.", "");

    DocCtorStrName(
        wxBitmapButton(),
        "Precreate a BitmapButton for 2-phase creation.", "",
        PreBitmapButton);

    // Turn it back on again
    %typemap(out) wxBitmapButton* { $result = wxPyMake_wxObject($1, $owner); }


    DocDeclStr(
        bool , Create(wxWindow* parent, wxWindowID id=-1,
                      const wxBitmap& bitmap = wxNullBitmap,
                      const wxPoint& pos = wxDefaultPosition,
                      const wxSize& size = wxDefaultSize,
                      long style = wxBU_AUTODRAW,
                      const wxValidator& validator = wxDefaultValidator,
                      const wxString& name = wxPyButtonNameStr),
        "Acutally create the GUI BitmapButton for 2-phase creation.", "");
};


//---------------------------------------------------------------------------
