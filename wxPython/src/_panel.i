/////////////////////////////////////////////////////////////////////////////
// Name:        _panel.i
// Purpose:     SWIG interface for wxPanel and wxScrolledWindow
//
// Author:      Robin Dunn
//
// Created:     24-June-1997
// RCS-ID:      $Id$
// Copyright:   (c) 2003 by Total Control Software
// Licence:     wxWindows license
/////////////////////////////////////////////////////////////////////////////

// Not a %module


//---------------------------------------------------------------------------

%{
%}

//---------------------------------------------------------------------------
%newgroup


MustHaveApp(wxPanel);

class wxPanel : public wxWindow
{
public:
    %pythonAppend wxPanel         "self._setOORInfo(self)"
    %pythonAppend wxPanel()       ""
    %typemap(out) wxPanel*;    // turn off this typemap

    wxPanel(wxWindow* parent,
            const wxWindowID id=-1,
            const wxPoint& pos = wxDefaultPosition,
            const wxSize& size = wxDefaultSize,
            long style = wxTAB_TRAVERSAL | wxNO_BORDER,
            const wxString& name = wxPyPanelNameStr);
    %RenameCtor(PrePanel, wxPanel());

    // Turn it back on again
    %typemap(out) wxPanel* { $result = wxPyMake_wxObject($1, $owner); }

    bool Create(wxWindow* parent,
                const wxWindowID id=-1,
                const wxPoint& pos = wxDefaultPosition,
                const wxSize& size = wxDefaultSize,
                long style = wxTAB_TRAVERSAL | wxNO_BORDER,
                const wxString& name = wxPyPanelNameStr);

    void InitDialog();


    DocDeclStr(
        virtual void , SetFocus(),
        "Overrides `wx.Window.SetFocus`.  This method uses the (undocumented)
mix-in class wxControlContainer which manages the focus and TAB logic
for controls which usually have child controls.  In practice, if you
call this method and the panel has at least one child window, then the
focus will be given to the child window.", "
:see: `wx.FocusEvent`, `wx.Window.SetFocus`, `SetFocusIgnoringChildren`");
    

    DocDeclStr(
        virtual void , SetFocusIgnoringChildren(),
        "In contrast to `SetFocus` (see above) this will set the focus to the
panel even of there are child windows in the panel. This is only
rarely needed.", "");
    

    
    static wxVisualAttributes
    GetClassDefaultAttributes(wxWindowVariant variant = wxWINDOW_VARIANT_NORMAL);
};

//---------------------------------------------------------------------------
%newgroup

enum wxScrollbarVisibility
{
    wxSHOW_SB_NEVER,        // never show the scrollbar at all
    wxSHOW_SB_DEFAULT,      // show scrollbar only if it is needed
    wxSHOW_SB_ALWAYS        // always show scrollbar, even if not needed
};


class wxScrollHelper
{
public:
    // ctor must be given the associated window
    wxScrollHelper(wxWindow *winToScroll);
    //virtual ~wxScrollHelper();

    // configure the scrolling
    virtual void SetScrollbars(int pixelsPerUnitX, int pixelsPerUnitY,
                               int noUnitsX, int noUnitsY,
                               int xPos = 0, int yPos = 0,
                               bool noRefresh = false );

    
    // scroll to the given (in logical coords) position
    %nokwargs Scroll;
    virtual void Scroll(int x, int y);
    virtual void Scroll(const wxPoint& pt);
        
    // get/set the page size for this orientation (wxVERTICAL/wxHORIZONTAL)
    int GetScrollPageSize(int orient) const;
    void SetScrollPageSize(int orient, int pageSize);

    // get the number of lines the window can scroll, 
    // returns 0 if no scrollbars are there.
    int GetScrollLines( int orient ) const;

    // Set the x, y scrolling increments.
    void SetScrollRate( int xstep, int ystep );

    DocDeclAStr(
        virtual void, GetScrollPixelsPerUnit(int *OUTPUT, int *OUTPUT) const,
        "GetScrollPixelsPerUnit() -> (xUnit, yUnit)",
        "Get the size of one logical unit in physical units.", "");

    void ShowScrollbars(wxScrollbarVisibility horz, wxScrollbarVisibility vert);

    // Enable/disable Windows scrolling in either direction. If true, wxWidgets
    // scrolls the canvas and only a bit of the canvas is invalidated; no
    // Clear() is necessary. If false, the whole canvas is invalidated and a
    // Clear() is necessary. Disable for when the scroll increment is used to
    // actually scroll a non-constant distance
    virtual void EnableScrolling(bool x_scrolling, bool y_scrolling);

    DocDeclStr( 
        wxPoint, GetViewStart() const,
        "Get the view start", "");
    
    // Disable use of keyboard keys for scrolling. By default cursor movement
    // keys (including Home, End, Page Up and Down) are used to scroll the
    // window appropriately. If the derived class uses these keys for something
    // else, e.g. changing the currently selected item, this function can be
    // used to disable this behaviour as it's not only not necessary then but
    // can actually be actively harmful if another object forwards a keyboard
    // event corresponding to one of the above keys to us using
    // ProcessWindowEvent() because the event will always be processed which
    // can be undesirable.
    void DisableKeyboardScrolling();

    
    // Set the scale factor, used in PrepareDC
    void SetScale(double xs, double ys);
    double GetScaleX() const;
    double GetScaleY() const;

    %nokwargs CalcScrolledPosition;
    %nokwargs CalcUnscrolledPosition;
    
    DocStr(CalcScrolledPosition, "Translate between scrolled and unscrolled coordinates.", "");
    wxPoint CalcScrolledPosition(const wxPoint& pt) const;
    DocDeclA(
        void, CalcScrolledPosition(int x, int y, int *OUTPUT, int *OUTPUT) const,
        "CalcScrolledPosition(int x, int y) -> (sx, sy)");

    
    DocStr(CalcUnscrolledPosition, "Translate between scrolled and unscrolled coordinates.", "");
    wxPoint CalcUnscrolledPosition(const wxPoint& pt) const;
    DocDeclA(
        void, CalcUnscrolledPosition(int x, int y, int *OUTPUT, int *OUTPUT) const,
        "CalcUnscrolledPosition(int x, int y) -> (ux, uy)");


    // Adjust the scrollbars
    virtual void AdjustScrollbars(void);

    // Calculate scroll increment
    virtual int CalcScrollInc(wxScrollWinEvent& event);

    // Normally the wxScrolledWindow will scroll itself, but in some rare
    // occasions you might want it to scroll [part of] another window (e.g. a
    // child of it in order to scroll only a portion the area between the
    // scrollbars (spreadsheet: only cell area will move).
    virtual void SetTargetWindow(wxWindow *target);
    virtual wxWindow *GetTargetWindow() const;

    void SetTargetRect(const wxRect& rect);
    wxRect GetTargetRect() const;

    // are we generating the autoscroll events?
    bool IsAutoScrolling() const { return m_timerAutoScroll != NULL; }

    // stop generating the scroll events when mouse is held outside the window
    void StopAutoScrolling();

    // this method can be overridden in a derived class to forbid sending the
    // auto scroll events - note that unlike StopAutoScrolling() it doesn't
    // stop the timer, so it will be called repeatedly and will typically
    // return different values depending on the current mouse position
    //
    // the base class version just returns true
    virtual bool SendAutoScrollEvents(wxScrollWinEvent& event) const;


    DocDeclStr(
        virtual void , DoPrepareDC( wxDC & dc ),
        "Call this function to prepare the device context for drawing a
scrolled image. It sets the device origin according to the current
scroll position.", "");
    %pythoncode { PrepareDC = DoPrepareDC }


    %property(ScaleX, GetScaleX);
    %property(ScaleY, GetScaleY);
    %property(TargetWindow, GetTargetWindow, SetTargetWindow);
    %property(ViewStart, GetViewStart);
};





MustHaveApp(wxScrolledWindow);

class wxScrolledWindow : public wxPanel, public wxScrollHelper
{
public:
    %pythonAppend wxScrolledWindow         "self._setOORInfo(self)"
    %pythonAppend wxScrolledWindow()       ""
    %typemap(out) wxScrolledWindow*;    // turn off this typemap

    wxScrolledWindow(wxWindow* parent,
                     const wxWindowID id = -1,
                     const wxPoint& pos = wxDefaultPosition,
                     const wxSize& size = wxDefaultSize,
                     long style = wxHSCROLL | wxVSCROLL,
                     const wxString& name = wxPyPanelNameStr);
    %RenameCtor(PreScrolledWindow, wxScrolledWindow());

    // Turn it back on again
    %typemap(out) wxScrolledWindow* { $result = wxPyMake_wxObject($1, $owner); }

    bool Create(wxWindow* parent,
                const wxWindowID id = -1,
                const wxPoint& pos = wxDefaultPosition,
                const wxSize& size = wxDefaultSize,
                long style = wxHSCROLL | wxVSCROLL,
                const wxString& name = wxPyPanelNameStr);
    
    static wxVisualAttributes
    GetClassDefaultAttributes(wxWindowVariant variant = wxWINDOW_VARIANT_NORMAL);
    
};

    
//---------------------------------------------------------------------------
