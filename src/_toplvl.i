/////////////////////////////////////////////////////////////////////////////
// Name:        _toplvl.i
// Purpose:     SWIG definitions for wxTopLevelWindow, wxFrame, wxDialog and etc.
//
// Author:      Robin Dunn
//
// Created:     27-Aug-1998
// RCS-ID:      $Id$
// Copyright:   (c) 2003 by Total Control Software
// Licence:     wxWindows license
/////////////////////////////////////////////////////////////////////////////

// Not a %module


//---------------------------------------------------------------------------

MAKE_CONST_WXSTRING(FrameNameStr);
MAKE_CONST_WXSTRING(DialogNameStr);
MAKE_CONST_WXSTRING(StatusLineNameStr);
MAKE_CONST_WXSTRING(ToolBarNameStr);

//---------------------------------------------------------------------------
%newgroup

enum
{
    wxSTAY_ON_TOP,
    wxICONIZE,
    wxMINIMIZE,
    wxMAXIMIZE,
    wxCLOSE_BOX,
    wxSYSTEM_MENU,
    wxMINIMIZE_BOX,
    wxMAXIMIZE_BOX,
    wxTINY_CAPTION_HORIZ,
    wxTINY_CAPTION_VERT,
    wxRESIZE_BORDER,

    wxDIALOG_NO_PARENT,

    wxDEFAULT_FRAME_STYLE,
    wxDEFAULT_DIALOG_STYLE,

    wxFRAME_TOOL_WINDOW,
    wxFRAME_FLOAT_ON_PARENT,
    wxFRAME_NO_WINDOW_MENU,
    wxFRAME_NO_TASKBAR,
    wxFRAME_SHAPED,
    wxFRAME_DRAWER,

    wxFRAME_EX_METAL,
    wxDIALOG_EX_METAL,
    wxWS_EX_CONTEXTHELP,

    wxFRAME_EX_CONTEXTHELP,
    wxDIALOG_EX_CONTEXTHELP,
};

%pythoncode {
    %# deprecated
    RESIZE_BOX  = MAXIMIZE_BOX
    THICK_FRAME = RESIZE_BORDER

    %# Obsolete
    wxDIALOG_MODAL = 0
    wxDIALOG_MODELESS = 0
    wxUSER_COLOURS = 0
    wxNO_3D = 0
}


enum
{
    wxFULLSCREEN_NOMENUBAR,
    wxFULLSCREEN_NOTOOLBAR,
    wxFULLSCREEN_NOSTATUSBAR,
    wxFULLSCREEN_NOBORDER,
    wxFULLSCREEN_NOCAPTION,
    wxFULLSCREEN_ALL,

    wxTOPLEVEL_EX_DIALOG,
};

// Styles for RequestUserAttention
enum
{
    wxUSER_ATTENTION_INFO = 1,
    wxUSER_ATTENTION_ERROR = 2
};


enum wxDialogModality
{
    wxDIALOG_MODALITY_NONE = 0,
    wxDIALOG_MODALITY_WINDOW_MODAL = 1,
    wxDIALOG_MODALITY_APP_MODAL = 2
};

//---------------------------------------------------------------------------

class  wxTopLevelWindow : public wxWindow
{
public:

    // No constructor as it can not be used directly from Python

    // maximize = True => maximize, otherwise - restore
    virtual void Maximize(bool maximize = true);

    // undo Maximize() or Iconize()
    virtual void Restore();

    // iconize = True => iconize, otherwise - restore
    virtual void Iconize(bool iconize = true);

    // return True if the frame is maximized
    virtual bool IsMaximized() const;

    // return true if the frame is always maximized
    // due to native guidelines or current policy
    virtual bool IsAlwaysMaximized() const;

    // return True if the frame is iconized
    virtual bool IsIconized() const;

    // get the frame icon
    wxIcon GetIcon() const;

    // set the frame icon
    virtual void SetIcon(const wxIcon& icon);

    // set the frame icons
    virtual void SetIcons(const wxIconBundle& icons);

    // maximize the window to cover entire screen
    virtual bool ShowFullScreen(bool show, long style = wxFULLSCREEN_ALL);

    // shows the window, but doesn't activate it. If the base code is being run,
    // it means the port doesn't implement this method yet and so alert the user.
    virtual void ShowWithoutActivating(); 

    // return True if the frame is in fullscreen mode
    virtual bool IsFullScreen() const;

    virtual void SetTitle(const wxString& title);
    virtual wxString GetTitle() const;

    // enable/disable close button [x]
    virtual bool EnableCloseButton(bool enable );

    // Set the shape of the window to the given region.
    // Returns True if the platform supports this feature
    // (and the operation is successful.)
    virtual bool SetShape(const wxRegion& region);

    // Attracts the users attention to this window if the application is inactive
    // (should be called when a background event occurs)
    virtual void RequestUserAttention(int flags = wxUSER_ATTENTION_INFO);

    // Is this the active frame (highlighted in the taskbar)?
    virtual bool IsActive();

    %extend {
        void MacSetMetalAppearance( bool on ) {
            int style = self->GetExtraStyle();
            if ( on )
                style |= wxFRAME_EX_METAL;
            else
                style &= ~wxFRAME_EX_METAL;
            self->SetExtraStyle(style);
        }
        
        bool MacGetMetalAppearance() const { return self->GetExtraStyle() & wxFRAME_EX_METAL; }

        bool MacGetUnifiedAppearance() const    { return true; }
    }

    %extend {
        long MacGetTopLevelWindowRef() {
        #ifdef __WXMAC__
            return (long)(self->MacGetTopLevelWindowRef());
        #else
            return 0;
        #endif
        }
    }

    DocDeclStr(
        void , CenterOnScreen(int dir = wxBOTH),
        "Center the window on screen", "");
    %pythoncode { CentreOnScreen = CenterOnScreen }


    // Get the default size for a new top level window. This is used when
    // creating a wxTLW under some platforms if no explicit size given.
    static wxSize GetDefaultSize();
    

    DocDeclStr(
        virtual wxWindow *, GetDefaultItem() const,
        "Get the default child of this parent, i.e. the one which is activated
by pressing <Enter> such as the OK button on a wx.Dialog.", "");

    DocDeclStr(
        virtual wxWindow *, SetDefaultItem(wxWindow * child),
        "Set this child as default, return the old default.", "");

    DocDeclStr(
        virtual void , SetTmpDefaultItem(wxWindow * win),
        "Set this child as temporary default", "");

    DocDeclStr(
        virtual wxWindow *, GetTmpDefaultItem() const,
        "Return the temporary default item, which can be None.", "");

    bool OSXIsModified() const;
    void OSXSetModified(bool modified);
    void SetRepresentedFilename(const wxString& filename);
    
    %property(DefaultItem, GetDefaultItem, SetDefaultItem, doc="See `GetDefaultItem` and `SetDefaultItem`");
    %property(Icon, GetIcon, SetIcon, doc="See `GetIcon` and `SetIcon`");
    %property(Title, GetTitle, SetTitle, doc="See `GetTitle` and `SetTitle`");
    %property(TmpDefaultItem, GetTmpDefaultItem, SetTmpDefaultItem, doc="See `GetTmpDefaultItem` and `SetTmpDefaultItem`");
    %property(OSXModified, OSXIsModified, OSXSetModified);
};


//---------------------------------------------------------------------------
%newgroup

// wxFrame is a top-level window with optional menubar, statusbar and toolbar
//
// For each of *bars, a frame may have several of them, but only one is
// managed by the frame, i.e. resized/moved when the frame is and whose size
// is accounted for in client size calculations - all others should be taken
// care of manually.

MustHaveApp(wxFrame);

class wxFrame : public wxTopLevelWindow
{
public:
    %pythonAppend wxFrame         "self._setOORInfo(self)"
    %pythonAppend wxFrame()       ""
    %typemap(out) wxFrame*;    // turn off this typemap

    wxFrame(wxWindow* parent,
            const wxWindowID id = -1,
            const wxString& title = wxPyEmptyString,
            const wxPoint& pos = wxDefaultPosition,
            const wxSize& size = wxDefaultSize,
            long style = wxDEFAULT_FRAME_STYLE,
            const wxString& name = wxPyFrameNameStr);
    %RenameCtor(PreFrame, wxFrame());

    // Turn it back on again
    %typemap(out) wxFrame* { $result = wxPyMake_wxObject($1, $owner); }

    bool Create(wxWindow* parent,
            const wxWindowID id = -1,
            const wxString& title = wxPyEmptyString,
            const wxPoint& pos = wxDefaultPosition,
            const wxSize& size = wxDefaultSize,
            long style = wxDEFAULT_FRAME_STYLE,
            const wxString& name = wxPyFrameNameStr);

    // frame state
    // -----------

    // get the origin of the client area (which may be different from (0, 0)
    // if the frame has a toolbar) in client coordinates
    virtual wxPoint GetClientAreaOrigin() const;


    // menu bar functions
    // ------------------

    virtual void SetMenuBar(wxMenuBar *menubar);
    virtual wxMenuBar *GetMenuBar() const;

    // find the item by id in the frame menu bar: this is an internal function
    // and exists mainly in order to be overridden in the MDI parent frame
    // which also looks at its active child menu bar
    virtual const wxMenuItem *FindItemInMenuBar(int menuId) const;

    // process menu command: returns True if processed
    %nokwargs ProcessCommand;
    bool ProcessCommand(int winid);
    bool ProcessCommand(wxMenuItem *item);

    // status bar functions
    // --------------------

    // create the main status bar by calling OnCreateStatusBar()
    virtual wxStatusBar* CreateStatusBar(int number = 1,
                                         long style = wxDEFAULT_STATUSBAR_STYLE,
                                         wxWindowID winid = 0,
                                         const wxString& name = wxPyStatusLineNameStr);

// TODO: with directors?
//     // return a new status bar
//     virtual wxStatusBar *OnCreateStatusBar(int number,
//                                            long style,
//                                            wxWindowID winid,
//                                            const wxString& name);

    // get the main status bar
    virtual wxStatusBar *GetStatusBar() const;

    // sets the main status bar
    void SetStatusBar(wxStatusBar *statBar);

    // forward these to status bar
    virtual void SetStatusText(const wxString &text, int number = 0);
    virtual void SetStatusWidths(int widths, const int* widths_field); // uses typemap above
    void PushStatusText(const wxString &text, int number = 0);
    void PopStatusText(int number = 0);

    // set the status bar pane the help will be shown in
    void SetStatusBarPane(int n);
    int GetStatusBarPane() const;

    // toolbar functions
    // -----------------

    // create main toolbar bycalling OnCreateToolBar()
    virtual wxToolBar* CreateToolBar(long style = -1,
                                     wxWindowID winid = -1,
                                     const wxString& name = wxPyToolBarNameStr);

// TODO: with directors?
//     // return a new toolbar
//     virtual wxToolBar *OnCreateToolBar(long style,
//                                        wxWindowID winid,
//                                        const wxString& name );

    // get/set the main toolbar
    virtual wxToolBar *GetToolBar() const;
    virtual void SetToolBar(wxToolBar *toolbar);

    // show help text (typically in the statusbar); show is False
    // if you are hiding the help, True otherwise
    virtual void DoGiveHelp(const wxString& text, bool show);

    // send wxUpdateUIEvents for all menu items in the menubar,
    // or just for menu if non-NULL
    void DoMenuUpdates(wxMenu* menu = NULL);

    static wxVisualAttributes
    GetClassDefaultAttributes(wxWindowVariant variant = wxWINDOW_VARIANT_NORMAL);

    %property(MenuBar, GetMenuBar, SetMenuBar, doc="See `GetMenuBar` and `SetMenuBar`");
    %property(StatusBar, GetStatusBar, SetStatusBar, doc="See `GetStatusBar` and `SetStatusBar`");
    %property(StatusBarPane, GetStatusBarPane, SetStatusBarPane, doc="See `GetStatusBarPane` and `SetStatusBarPane`");
    %property(ToolBar, GetToolBar, SetToolBar, doc="See `GetToolBar` and `SetToolBar`");
};

//---------------------------------------------------------------------------
%newgroup

enum {
    // Don't do any layout adaptation
    wxDIALOG_ADAPTATION_NONE,

    // Only look for wxStdDialogButtonSizer for non-scrolling part
    wxDIALOG_ADAPTATION_STANDARD_SIZER,

    // Also look for any suitable sizer for non-scrolling part
    wxDIALOG_ADAPTATION_ANY_SIZER,

    // Also look for 'loose' standard buttons for non-scrolling part
    wxDIALOG_ADAPTATION_LOOSE_BUTTONS,
};

// Layout adaptation mode, for SetLayoutAdaptationMode
enum wxDialogLayoutAdaptationMode
{
    wxDIALOG_ADAPTATION_MODE_DEFAULT = 0,   // use global adaptation enabled status
    wxDIALOG_ADAPTATION_MODE_ENABLED = 1,   // enable this dialog overriding global status
    wxDIALOG_ADAPTATION_MODE_DISABLED = 2   // disable this dialog overriding global status
};



MustHaveApp(wxDialog);

class wxDialog : public wxTopLevelWindow
{
public:
    %pythonAppend wxDialog   "self._setOORInfo(self)"
    %pythonAppend wxDialog() ""
    %typemap(out) wxDialog*;    // turn off this typemap

    wxDialog(wxWindow* parent,
             const wxWindowID id = -1,
             const wxString& title = wxPyEmptyString,
             const wxPoint& pos = wxDefaultPosition,
             const wxSize& size = wxDefaultSize,
             long style = wxDEFAULT_DIALOG_STYLE,
             const wxString& name = wxPyDialogNameStr);
    %RenameCtor(PreDialog, wxDialog());

    // Turn it back on again
    %typemap(out) wxDialog* { $result = wxPyMake_wxObject($1, $owner); }

    bool Create(wxWindow* parent,
                const wxWindowID id = -1,
                const wxString& title = wxPyEmptyString,
                const wxPoint& pos = wxDefaultPosition,
                const wxSize& size = wxDefaultSize,
                long style = wxDEFAULT_DIALOG_STYLE,
                const wxString& name = wxPyDialogNameStr);

    // the modal dialogs have a return code - usually the ID of the last
    // pressed button
    void SetReturnCode(int returnCode);
    int GetReturnCode() const;

    // Set the identifier for the affirmative button: this button will close
    // the dialog after validating data and calling TransferDataFromWindow()
    void SetAffirmativeId(int affirmativeId);
    int GetAffirmativeId() const;

    // Set identifier for Esc key translation: the button with this id will
    // close the dialog without doing anything else; special value wxID_NONE
    // means to not handle Esc at all while wxID_ANY means to map Esc to
    // wxID_CANCEL if present and GetAffirmativeId() otherwise
    void SetEscapeId(int escapeId);
    int GetEscapeId() const;

    // Returns the parent to use for modal dialogs if the user did not specify it
    // explicitly
    %nokwargs GetParentForModalDialog;
    wxWindow *GetParentForModalDialog(wxWindow *parent, long style) const;
    wxWindow *GetParentForModalDialog() const;

    // splits text up at newlines and places the
    // lines into a vertical wxBoxSizer
    wxSizer* CreateTextSizer( const wxString &message );
    
    // TODO:  wxSizer *CreateTextSizer( const wxString& message,
    //                           wxTextSizerWrapper& wrapper );


    // returns a sizer containing the given one and a static line separating it
    // from the preceding elements if it's appropriate for the current platform
    wxSizer *CreateSeparatedSizer(wxSizer *sizer);

    // returns a horizontal wxBoxSizer containing the given buttons
    //
    // notice that the returned sizer can be NULL if no buttons are put in the
    // sizer (this mostly happens under smart phones and other atypical
    // platforms which have hardware buttons replacing OK/Cancel and such)
   %Rename(_CreateButtonSizer,
           wxSizer* , CreateButtonSizer( long flags ));
    %pythoncode {
        def CreateButtonSizer(self, flags, *ignored):
            return self._CreateButtonSizer(flags)
    }

    // returns the sizer containing CreateButtonSizer() below a separating
    // static line for the platforms which use static lines for items
    // separation (i.e. not Mac)
    wxSizer *CreateSeparatedButtonSizer(long flags);

    wxStdDialogButtonSizer* CreateStdDialogButtonSizer( long flags );

    //void SetModal( bool flag );

    // is the dialog in modal state right now?
    virtual bool IsModal() const;

    // Shows the dialog and starts a nested event loop that returns when
    // EndModal is called.
    virtual int ShowModal();

    // may be called to terminate the dialog with the given return code
    virtual void EndModal(int retCode);

    
    // show the dialog frame-modally (needs a parent), using app-modal
    // dialogs on platforms that don't support it
    virtual void ShowWindowModal();
    virtual void SendWindowModalDialogEvent( wxEventType type );

    
    // Do layout adaptation
    virtual bool DoLayoutAdaptation();

    // Can we do layout adaptation?
    virtual bool CanDoLayoutAdaptation();

    // Returns a content window if there is one. This can be used by the layout adapter, for
    // example to make the pages of a book control into scrolling windows
    virtual wxWindow* GetContentWindow() const;

    // Add an id to the list of main button identifiers that should be in the button sizer
    void AddMainButtonId(wxWindowID id);
    wxArrayInt& GetMainButtonIds();

    // Is this id in the main button id array?
    bool IsMainButtonId(wxWindowID id) const;

    // Level of adaptation, from none (Level 0) to full (Level 3). To disable adaptation,
    // set level 0, for example in your dialog constructor. You might
    // do this if you know that you are displaying on a large screen and you don't want the
    // dialog changed.
    void SetLayoutAdaptationLevel(int level);
    int GetLayoutAdaptationLevel() const;

    /// Override global adaptation enabled/disabled status
    void SetLayoutAdaptationMode(wxDialogLayoutAdaptationMode mode);
    wxDialogLayoutAdaptationMode GetLayoutAdaptationMode() const;

    // Returns true if the adaptation has been done
    void SetLayoutAdaptationDone(bool adaptationDone);
    bool GetLayoutAdaptationDone() const;

    // Set layout adapter class, returning old adapter
    static wxDialogLayoutAdapter* SetLayoutAdapter(wxDialogLayoutAdapter* adapter);
    static wxDialogLayoutAdapter* GetLayoutAdapter();

    // Global switch for layout adaptation
    static bool IsLayoutAdaptationEnabled();
    static void EnableLayoutAdaptation(bool enable);

    // modality kind
    virtual wxDialogModality GetModality() const;

    
    static wxVisualAttributes
    GetClassDefaultAttributes(wxWindowVariant variant = wxWINDOW_VARIANT_NORMAL);

    // for the 'with' statement
    %pythoncode { 
        def __enter__(self):
            return self
        def __exit__(self, exc_type, exc_val, exc_tb):
            self.Destroy()
    }

    %property(AffirmativeId, GetAffirmativeId, SetAffirmativeId, doc="See `GetAffirmativeId` and `SetAffirmativeId`");
    %property(EscapeId, GetEscapeId, SetEscapeId, doc="See `GetEscapeId` and `SetEscapeId`");
    %property(ReturnCode, GetReturnCode, SetReturnCode, doc="See `GetReturnCode` and `SetReturnCode`");
};



/*!
 * Base class for layout adapters - code that, for example, turns a dialog into a
 * scrolling dialog if there isn't enough screen space. You can derive further
 * adapter classes to do any other kind of adaptation, such as applying a watermark, or adding
 * a help mechanism.
 */

// TODO:  Virtualize this for wxPython
class wxDialogLayoutAdapter: public wxObject
{
public:
    wxDialogLayoutAdapter() {}

    // Override this function to indicate that adaptation should be done
    virtual bool CanDoLayoutAdaptation(wxDialog* dialog) = 0;

    // Override this function to do the adaptation
    virtual bool DoLayoutAdaptation(wxDialog* dialog) = 0;
};

/*!
 * Standard adapter. Does scrolling adaptation for paged and regular dialogs.
 *
 */

class wxStandardDialogLayoutAdapter: public wxDialogLayoutAdapter
{
public:
    wxStandardDialogLayoutAdapter() {}


    // Indicate that adaptation should be done
    virtual bool CanDoLayoutAdaptation(wxDialog* dialog);

    // Do layout adaptation
    virtual bool DoLayoutAdaptation(wxDialog* dialog);


    // Create the scrolled window
    virtual wxScrolledWindow* CreateScrolledWindow(wxWindow* parent);

    // Find a standard or horizontal box sizer
    virtual wxSizer* FindButtonSizer(bool stdButtonSizer, wxDialog* dialog, wxSizer* sizer, int& retBorder, int accumlatedBorder = 0);

    // Check if this sizer contains standard buttons, and so can be repositioned in the dialog
    virtual bool IsOrdinaryButtonSizer(wxDialog* dialog, wxBoxSizer* sizer);

    // Check if this is a standard button
    virtual bool IsStandardButton(wxDialog* dialog, wxButton* button);

    // Find 'loose' main buttons in the existing layout and add them to the standard dialog sizer
    virtual bool FindLooseButtons(wxDialog* dialog, wxStdDialogButtonSizer* buttonSizer, wxSizer* sizer, int& count);

    // Reparent the controls to the scrolled window, except those in buttonSizer
    virtual void ReparentControls(wxWindow* parent, wxWindow* reparentTo, wxSizer* buttonSizer = NULL);
    static void DoReparentControls(wxWindow* parent, wxWindow* reparentTo, wxSizer* buttonSizer = NULL);

    // A function to fit the dialog around its contents, and then adjust for screen size.
    // If scrolled windows are passed, scrolling is enabled in the required orientation(s).
    virtual bool FitWithScrolling(wxDialog* dialog, wxScrolledWindow* scrolledWindow);
//    virtual bool FitWithScrolling(wxDialog* dialog, wxWindowList& windows);
    static bool DoFitWithScrolling(wxDialog* dialog, wxScrolledWindow* scrolledWindow);
//    static bool DoFitWithScrolling(wxDialog* dialog, wxWindowList& windows);

    // Find whether scrolling will be necessary for the dialog, returning wxVERTICAL, wxHORIZONTAL or both
    virtual int MustScroll(wxDialog* dialog, wxSize& windowSize, wxSize& displaySize);
    static int DoMustScroll(wxDialog* dialog, wxSize& windowSize, wxSize& displaySize);
};




class wxWindowModalDialogEvent  : public wxCommandEvent
{
public:
    wxWindowModalDialogEvent(wxEventType commandType = wxEVT_NULL, int id = 0);

    wxDialog *GetDialog() const;
    int GetReturnCode() const;

    %property(Dialog, GetDialog);
    %property(ReturnCode, GetReturnCode);
};


%constant wxEventType wxEVT_WINDOW_MODAL_DIALOG_CLOSED;
%pythoncode {
    EVT_WINDOW_MODAL_DIALOG_CLOSED = wx.PyEventBinder(wxEVT_WINDOW_MODAL_DIALOG_CLOSED)
}


//---------------------------------------------------------------------------
%newgroup

%{
#define wxDEFAULT_MINIFRAME_STYLE wxCAPTION | wxRESIZE_BORDER | wxTINY_CAPTION_HORIZ
%}

enum  {
    wxDEFAULT_MINIFRAME_STYLE
};


MustHaveApp(wxMiniFrame);

class wxMiniFrame : public wxFrame
{
public:
    %pythonAppend wxMiniFrame         "self._setOORInfo(self)"
    %pythonAppend wxMiniFrame()       ""

    wxMiniFrame(wxWindow* parent,
            const wxWindowID id = -1,
            const wxString& title = wxPyEmptyString,
            const wxPoint& pos = wxDefaultPosition,
            const wxSize& size = wxDefaultSize,
            long style = wxDEFAULT_MINIFRAME_STYLE,
            const wxString& name = wxPyFrameNameStr);
    %RenameCtor(PreMiniFrame, wxMiniFrame());

    bool Create(wxWindow* parent,
            const wxWindowID id = -1,
            const wxString& title = wxPyEmptyString,
            const wxPoint& pos = wxDefaultPosition,
            const wxSize& size = wxDefaultSize,
            long style = wxDEFAULT_MINIFRAME_STYLE,
            const wxString& name = wxPyFrameNameStr);
};


//---------------------------------------------------------------------------
%newgroup

%{
#define wxSPLASH_CENTER_ON_PARENT wxSPLASH_CENTRE_ON_PARENT
#define wxSPLASH_CENTER_ON_SCREEN wxSPLASH_CENTRE_ON_SCREEN
#define wxSPLASH_NO_CENTER wxSPLASH_NO_CENTRE
%}

enum
{
    wxSPLASH_CENTRE_ON_PARENT,
    wxSPLASH_CENTRE_ON_SCREEN,
    wxSPLASH_NO_CENTRE,
    wxSPLASH_CENTER_ON_PARENT,
    wxSPLASH_CENTER_ON_SCREEN,
    wxSPLASH_NO_CENTER,
    wxSPLASH_TIMEOUT,
    wxSPLASH_NO_TIMEOUT,
};


MustHaveApp(wxSplashScreenWindow);

class wxSplashScreenWindow: public wxWindow
{
public:
    %pythonAppend wxSplashScreenWindow         "self._setOORInfo(self)"

    wxSplashScreenWindow(const wxBitmap& bitmap,
             wxWindow* parent,
             wxWindowID id,
             const wxPoint& pos = wxDefaultPosition,
             const wxSize& size = wxDefaultSize,
             long style = wxNO_BORDER);

    void SetBitmap(const wxBitmap& bitmap);
    wxBitmap& GetBitmap();

    %property(Bitmap, GetBitmap, SetBitmap, doc="See `GetBitmap` and `SetBitmap`");
};


MustHaveApp(wxSplashScreen);

class wxSplashScreen : public wxFrame
{
public:
    %pythonAppend wxSplashScreen         "self._setOORInfo(self)"

    wxSplashScreen(const wxBitmap& bitmap,
            long splashStyle, int milliseconds,
            wxWindow* parent,
            wxWindowID id = -1,
            const wxPoint& pos = wxDefaultPosition,
            const wxSize& size = wxDefaultSize,
            long style = wxSIMPLE_BORDER | wxFRAME_NO_TASKBAR | wxSTAY_ON_TOP);

    long GetSplashStyle() const;
    wxSplashScreenWindow* GetSplashWindow() const;
    int GetTimeout() const;

    %property(SplashStyle, GetSplashStyle, doc="See `GetSplashStyle`");
    %property(SplashWindow, GetSplashWindow, doc="See `GetSplashWindow`");
    %property(Timeout, GetTimeout, doc="See `GetTimeout`");
};


//---------------------------------------------------------------------------
