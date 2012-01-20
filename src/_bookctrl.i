/////////////////////////////////////////////////////////////////////////////
// Name:        _bookctrl.i
// Purpose:     SWIG interface defs for wxBookCtrlBase
//
// Author:      Robin Dunn
//
// Created:     19-Oct-2011
// RCS-ID:      $Id: $
// Copyright:   (c) 2011 by Total Control Software
// Licence:     wxWindows license
/////////////////////////////////////////////////////////////////////////////

// Not a %module


//---------------------------------------------------------------------------
%newgroup

enum {
    wxBK_DEFAULT,
    wxBK_TOP,
    wxBK_BOTTOM,
    wxBK_LEFT,
    wxBK_RIGHT,
    wxBK_ALIGN_MASK,

    wxBK_BUTTONBAR,   // deprecated
    wxTBK_BUTTONBAR,   
    wxTBK_HORZ_LAYOUT,

    // hittest flags
    wxBK_HITTEST_NOWHERE = 1,   // not on tab
    wxBK_HITTEST_ONICON  = 2,   // on icon
    wxBK_HITTEST_ONLABEL = 4,   // on label
    wxBK_HITTEST_ONITEM  = wxBK_HITTEST_ONICON | wxBK_HITTEST_ONLABEL,
    wxBK_HITTEST_ONPAGE  = 8,   // not on tab control, but over the selected page
};


MustHaveApp(wxBookCtrlBase);

//  Common base class for wxList/Tree/Notebook
class wxBookCtrlBase : public wxControl, public wxWithImages
{
public:
    // This is an ABC, it can't be constructed...

//     wxBookCtrlBase(wxWindow *parent,
//                wxWindowID id,
//                const wxPoint& pos = wxDefaultPosition,
//                const wxSize& size = wxDefaultSize,
//                long style = 0,
//                const wxString& name = wxPyEmptyString);
//     %RenameCtor(PreBookCtrlBase, wxBookCtrlBase());
//     bool Create(wxWindow *parent,
//                 wxWindowID id,
//                 const wxPoint& pos = wxDefaultPosition,
//                 const wxSize& size = wxDefaultSize,
//                 long style = 0,
//                 const wxString& name = wxPyEmptyString);


    // get number of pages in the dialog
    virtual size_t GetPageCount() const;

    // get the panel which represents the given page
    virtual wxWindow *GetPage(size_t n);

    // get the current page or NULL if none
    wxWindow* GetCurrentPage() const;

    // get the currently selected page or wxNOT_FOUND if none
    virtual int GetSelection() const/* = 0*/;

    // set/get the title of a page
    virtual bool SetPageText(size_t n, const wxString& strText)/* = 0*/;
    virtual wxString GetPageText(size_t n) const/* = 0*/;


    // sets/returns item's image index in the current image list
    virtual int GetPageImage(size_t n) const/* = 0*/;
    virtual bool SetPageImage(size_t n, int imageId)/* = 0*/;


    // resize the notebook so that all pages will have the specified size
    virtual void SetPageSize(const wxSize& size);

    // calculate the size of the control from the size of its page
    virtual wxSize CalcSizeFromPage(const wxSize& sizePage) const/* = 0*/;


    // get/set size of area between book control area and page area
    unsigned int GetInternalBorder() const;
    void SetInternalBorder(unsigned int internalBorder);

    // returns true if we have wxCHB_TOP or wxCHB_BOTTOM style
    bool IsVertical() const;

    // Sets/gets the margin around the controller
    void SetControlMargin(int margin);
    int GetControlMargin() const;

    // set/get option to shrink to fit current page
    void SetFitToCurrentPage(bool fit);
    bool GetFitToCurrentPage() const;

    // returns the sizer containing the control, if any
    wxSizer* GetControlSizer() const;


    // remove one page from the control and delete it
    virtual bool DeletePage(size_t n);

    // remove one page from the notebook, without deleting it
    virtual bool RemovePage(size_t n);

    // remove all pages and delete them
    virtual bool DeleteAllPages();

    // adds a new page to the control
    virtual bool AddPage(wxWindow *page,
                         const wxString& text,
                         bool select = false,
                         int imageId = -1);

    // the same as AddPage(), but adds the page at the specified position
    virtual bool InsertPage(size_t n,
                            wxWindow *page,
                            const wxString& text,
                            bool select = false,
                            int imageId = -1)/* = 0*/;

    // set the currently selected page, return the index of the previously
    // selected one (or -1 on error)
    //
    // NB: this function will _not_ generate PAGE_CHANGING/ED events
    virtual int SetSelection(size_t n)/* = 0*/;

    
    // acts as SetSelection but does not generate events
    virtual int ChangeSelection(size_t n)/* = 0*/;

    // cycle thru the pages
    void AdvanceSelection(bool forward = true);

    DocDeclAStr(
        virtual int, HitTest(const wxPoint& pt, long* OUTPUT) const,
        "HitTest(Point pt) -> (tab, where)",
        "Returns the page/tab which is hit, and flags indicating where using
wx.NB_HITTEST flags.", "");

    static wxVisualAttributes
    GetClassDefaultAttributes(wxWindowVariant variant = wxWINDOW_VARIANT_NORMAL);

    %property(ControlMargin, GetControlMargin, SetControlMargin, doc="See `GetControlMargin` and `SetControlMargin`");
    %property(ControlSizer, GetControlSizer, doc="See `GetControlSizer`");
    %property(CurrentPage, GetCurrentPage, doc="See `GetCurrentPage`");
    %property(FitToCurrentPage, GetFitToCurrentPage, SetFitToCurrentPage, doc="See `GetFitToCurrentPage` and `SetFitToCurrentPage`");
    %property(InternalBorder, GetInternalBorder, SetInternalBorder, doc="See `GetInternalBorder` and `SetInternalBorder`");
    %property(PageCount, GetPageCount, doc="See `GetPageCount`");
    %property(PageImage, GetPageImage, SetPageImage, doc="See `GetPageImage` and `SetPageImage`");
    %property(PageText, GetPageText, SetPageText, doc="See `GetPageText` and `SetPageText`");
    %property(Selection, GetSelection, SetSelection, doc="See `GetSelection` and `SetSelection`");

};



//---------------------------------------------------------------------------

class wxBookCtrlEvent : public wxNotifyEvent
{
public:
    wxBookCtrlEvent(wxEventType commandType = wxEVT_NULL, int id = 0,
                    int nSel = -1, int nOldSel = -1);

        // the currently selected page (-1 if none)
    int GetSelection() const;
    void SetSelection(int nSel);
        // the page that was selected before the change (-1 if none)
    int GetOldSelection() const;
    void SetOldSelection(int nOldSel);

    %property(OldSelection, GetOldSelection, SetOldSelection, doc="See `GetOldSelection` and `SetOldSelection`");
    %property(Selection, GetSelection, SetSelection, doc="See `GetSelection` and `SetSelection`");

};


//---------------------------------------------------------------------------

