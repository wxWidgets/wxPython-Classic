/////////////////////////////////////////////////////////////////////////////
// Name:        _notebook.i
// Purpose:     SWIG interface defs for wxNotebook and such
//
// Author:      Robin Dunn
//
// Created:     2-June-1998
// RCS-ID:      $Id$
// Copyright:   (c) 2003 by Total Control Software
// Licence:     wxWindows license
/////////////////////////////////////////////////////////////////////////////

// Not a %module


//---------------------------------------------------------------------------

MAKE_CONST_WXSTRING(NotebookNameStr);

//---------------------------------------------------------------------------

//---------------------------------------------------------------------------
%newgroup

enum {
    // styles
    wxNB_FIXEDWIDTH,
    wxNB_TOP,
    wxNB_LEFT,
    wxNB_RIGHT,
    wxNB_BOTTOM,
    wxNB_MULTILINE,
    wxNB_NOPAGETHEME,

    // for backwards compatibility only
    wxNB_HITTEST_NOWHERE,
    wxNB_HITTEST_ONICON,
    wxNB_HITTEST_ONLABEL,
    wxNB_HITTEST_ONITEM,
    wxNB_HITTEST_ONPAGE,
};



MustHaveApp(wxNotebook);

class wxNotebook : public wxBookCtrlBase {
public:
    %pythonAppend wxNotebook         "self._setOORInfo(self)"
    %pythonAppend wxNotebook()       ""
    %typemap(out) wxNotebook*;    // turn off this typemap

    wxNotebook(wxWindow *parent,
               wxWindowID id=-1,
               const wxPoint& pos = wxDefaultPosition,
               const wxSize& size = wxDefaultSize,
               long style = 0,
               const wxString& name = wxPyNotebookNameStr);
    %RenameCtor(PreNotebook, wxNotebook());

    // Turn it back on again
    %typemap(out) wxNotebook* { $result = wxPyMake_wxObject($1, $owner); }

    bool Create(wxWindow *parent,
               wxWindowID id=-1,
               const wxPoint& pos = wxDefaultPosition,
               const wxSize& size = wxDefaultSize,
               long style = 0,
               const wxString& name = wxPyNotebookNameStr);


    // get the number of rows for a control with wxNB_MULTILINE style (not all
    // versions support it - they will always return 1 then)
    virtual int GetRowCount() const;

    // set the padding between tabs (in pixels)
    virtual void SetPadding(const wxSize& padding);

    // set the size of the tabs for wxNB_FIXEDWIDTH controls
    virtual void SetTabSize(const wxSize& sz);

    // implement some base class functions
    virtual wxSize CalcSizeFromPage(const wxSize& sizePage) const;

    // On platforms that support it, get the theme page background colour,
    // else invalid colour
    wxColour GetThemeBackgroundColour() const;

    static wxVisualAttributes
    GetClassDefaultAttributes(wxWindowVariant variant = wxWINDOW_VARIANT_NORMAL);

    // returns false if the change to nPage is vetoed by the program
    bool SendPageChangingEvent(int nPage);

    // sends the event about page change from old to new (or GetSelection() if
    // new is -1)
    void SendPageChangedEvent(int nPageOld, int nPageNew = -1);

    %property(RowCount, GetRowCount, doc="See `GetRowCount`");
    %property(ThemeBackgroundColour, GetThemeBackgroundColour, doc="See `GetThemeBackgroundColour`");
};



%pythoncode {
NotebookEvent = wx.BookCtrlEvent
}

// notebook control event types
%constant wxEventType wxEVT_COMMAND_NOTEBOOK_PAGE_CHANGED;
%constant wxEventType wxEVT_COMMAND_NOTEBOOK_PAGE_CHANGING;

%pythoncode {
    %# wxNotebook events
    EVT_NOTEBOOK_PAGE_CHANGED  = wx.PyEventBinder( wxEVT_COMMAND_NOTEBOOK_PAGE_CHANGED, 1 )
    EVT_NOTEBOOK_PAGE_CHANGING = wx.PyEventBinder( wxEVT_COMMAND_NOTEBOOK_PAGE_CHANGING, 1 )
}


%pythoncode {
%#----------------------------------------------------------------------------

class NotebookPage(wx.Panel):
    """
    There is an old (and apparently unsolvable) bug when placing a
    window with a nonstandard background colour in a wx.Notebook on
    wxGTK1, as the notbooks's background colour would always be used
    when the window is refreshed.  The solution is to place a panel in
    the notbook and the coloured window on the panel, sized to cover
    the panel.  This simple class does that for you, just put an
    instance of this in the notebook and make your regular window a
    child of this one and it will handle the resize for you.
    """
    def __init__(self, parent, id=-1,
                 pos=wx.DefaultPosition, size=wx.DefaultSize,
                 style=wx.TAB_TRAVERSAL, name="panel"):
        wx.Panel.__init__(self, parent, id, pos, size, style, name)
        self.child = None
        self.Bind(wx.EVT_SIZE, self.OnSize)

    def OnSize(self, evt):
        if self.child is None:
            children = self.GetChildren()
            if len(children):
                self.child = children[0]
        if self.child:
            self.child.SetPosition((0,0))
            self.child.SetSize(self.GetSize())

}

//---------------------------------------------------------------------------
%newgroup


enum
{
    // default alignment: left everywhere except Mac where it is top
    wxLB_DEFAULT = 0,

    // put the list control to the left/right/top/bottom of the page area
    wxLB_TOP    = 0x1,
    wxLB_BOTTOM = 0x2,
    wxLB_LEFT   = 0x4,
    wxLB_RIGHT  = 0x8,

    // the mask which can be used to extract the alignment from the style
    wxLB_ALIGN_MASK = 0xf,
};



MustHaveApp(wxListbook);

//  wxListCtrl and wxNotebook combination
class wxListbook : public wxBookCtrlBase
{
public:
    %pythonAppend wxListbook         "self._setOORInfo(self)"
    %pythonAppend wxListbook()       ""

    wxListbook(wxWindow *parent,
               wxWindowID id=-1,
               const wxPoint& pos = wxDefaultPosition,
               const wxSize& size = wxDefaultSize,
               long style = 0,
               const wxString& name = wxPyEmptyString);
    %RenameCtor(PreListbook, wxListbook());

    bool Create(wxWindow *parent,
                wxWindowID id=-1,
                const wxPoint& pos = wxDefaultPosition,
                const wxSize& size = wxDefaultSize,
                long style = 0,
                const wxString& name = wxPyEmptyString);

    wxListView* GetListView();
    %property(ListView, GetListView, doc="See `GetListView`");
};


%pythoncode {
ListbookEvent = wx.BookCtrlEvent
}

%constant wxEventType wxEVT_COMMAND_LISTBOOK_PAGE_CHANGED;
%constant wxEventType wxEVT_COMMAND_LISTBOOK_PAGE_CHANGING;

%pythoncode {
    EVT_LISTBOOK_PAGE_CHANGED  = wx.PyEventBinder( wxEVT_COMMAND_LISTBOOK_PAGE_CHANGED, 1 )
    EVT_LISTBOOK_PAGE_CHANGING = wx.PyEventBinder( wxEVT_COMMAND_LISTBOOK_PAGE_CHANGING, 1 )
}

//---------------------------------------------------------------------------


/*
 * wxChoicebook flags
 */
enum {
    wxCHB_DEFAULT,
    wxCHB_TOP,
    wxCHB_BOTTOM,
    wxCHB_LEFT,
    wxCHB_RIGHT,
    wxCHB_ALIGN_MASK
};


MustHaveApp(wxChoicebook);

class wxChoicebook : public wxBookCtrlBase
{
public:
    %pythonAppend wxChoicebook         "self._setOORInfo(self)"
    %pythonAppend wxChoicebook()       ""

    wxChoicebook(wxWindow *parent,
                 wxWindowID id,
                 const wxPoint& pos = wxDefaultPosition,
                 const wxSize& size = wxDefaultSize,
                 long style = 0,
                 const wxString& name = wxPyEmptyString);
    %RenameCtor(PreChoicebook, wxChoicebook());

    // quasi ctor
    bool Create(wxWindow *parent,
                wxWindowID id,
                const wxPoint& pos = wxDefaultPosition,
                const wxSize& size = wxDefaultSize,
                long style = 0,
                const wxString& name = wxPyEmptyString);


    // returns the choice control
    wxChoice* GetChoiceCtrl() const;

    virtual bool DeleteAllPages();

    %property(ChoiceCtrl, GetChoiceCtrl, doc="See `GetChoiceCtrl`");

};


%pythoncode {
ChoicebookEvent = wx.BookCtrlEvent
}

%constant wxEventType wxEVT_COMMAND_CHOICEBOOK_PAGE_CHANGED;
%constant wxEventType wxEVT_COMMAND_CHOICEBOOK_PAGE_CHANGING;

%pythoncode {
    EVT_CHOICEBOOK_PAGE_CHANGED  = wx.PyEventBinder( wxEVT_COMMAND_CHOICEBOOK_PAGE_CHANGED, 1 )
    EVT_CHOICEBOOK_PAGE_CHANGING = wx.PyEventBinder( wxEVT_COMMAND_CHOICEBOOK_PAGE_CHANGING, 1 )
}

//---------------------------------------------------------------------------
%newgroup;

MustHaveApp(wxTreebook);

class wxTreebook : public wxBookCtrlBase
{
public:
    %pythonAppend wxTreebook         "self._setOORInfo(self)"
    %pythonAppend wxTreebook()       ""


    // This ctor creates the tree book control
    wxTreebook(wxWindow *parent,
               wxWindowID id,
               const wxPoint& pos = wxDefaultPosition,
               const wxSize& size = wxDefaultSize,
               long style = wxBK_DEFAULT,
               const wxString& name = wxPyEmptyString);

    %RenameCtor(PreTreebook, wxTreebook());


    // Really creates the control
    bool Create(wxWindow *parent,
                wxWindowID id,
                const wxPoint& pos = wxDefaultPosition,
                const wxSize& size = wxDefaultSize,
                long style = wxBK_DEFAULT,
                const wxString& name = wxPyEmptyString);


    // Notice that page pointer may be NULL in which case the next non NULL
    // page (usually the first child page of a node) is shown when this page is
    // selected

    // Inserts a new page just before the page indicated by page.
    // The new page is placed on the same level as page.
    virtual bool InsertPage(size_t pos,
                            wxWindow *page,
                            const wxString& text,
                            bool select = false,
                            int imageId = wxNOT_FOUND);

    // Inserts a new sub-page to the end of children of the page at given pos.
    virtual bool InsertSubPage(size_t pos,
                               wxWindow *page,
                               const wxString& text,
                               bool select = false,
                               int imageId = wxNOT_FOUND);

    // Adds a new page at top level after all other pages.
    virtual bool AddPage(wxWindow *page,
                         const wxString& text,
                         bool select = false,
                         int imageId = wxNOT_FOUND);

    // Adds a new child-page to the last top-level page inserted.
    // Useful when constructing 1 level tree structure.
    virtual bool AddSubPage(wxWindow *page,
                            const wxString& text,
                            bool select = false,
                            int imageId = wxNOT_FOUND);

    // Deletes the page and ALL its children. Could trigger page selection
    // change in a case when selected page is removed. In that case its parent
    // is selected (or the next page if no parent).
    virtual bool DeletePage(size_t pos);


    // Tree operations
    // ---------------

    // Gets the page node state -- node is expanded or collapsed
    virtual bool IsNodeExpanded(size_t pos) const;

    // Expands or collapses the page node. Returns the previous state.
    // May generate page changing events (if selected page
    // is under the collapsed branch, then parent is autoselected).
    virtual bool ExpandNode(size_t pos, bool expand = true);

    // shortcut for ExpandNode(pos, false)
    bool CollapseNode(size_t pos);

    // get the parent page or wxNOT_FOUND if this is a top level page
    int GetPageParent(size_t pos) const;

    // the tree control we use for showing the pages index tree
    wxPyTreeCtrl* GetTreeCtrl() const;

    %property(TreeCtrl, GetTreeCtrl, doc="See `GetTreeCtrl`");
};



%pythoncode {
TreebookEvent = wx.BookCtrlEvent
}

%constant wxEventType wxEVT_COMMAND_TREEBOOK_PAGE_CHANGED;
%constant wxEventType wxEVT_COMMAND_TREEBOOK_PAGE_CHANGING;
%constant wxEventType wxEVT_COMMAND_TREEBOOK_NODE_COLLAPSED;
%constant wxEventType wxEVT_COMMAND_TREEBOOK_NODE_EXPANDED;

%pythoncode {
    EVT_TREEBOOK_PAGE_CHANGED = wx.PyEventBinder( wxEVT_COMMAND_TREEBOOK_PAGE_CHANGED, 1 )
    EVT_TREEBOOK_PAGE_CHANGING = wx.PyEventBinder( wxEVT_COMMAND_TREEBOOK_PAGE_CHANGING, 1)
    EVT_TREEBOOK_NODE_COLLAPSED = wx.PyEventBinder( wxEVT_COMMAND_TREEBOOK_NODE_COLLAPSED, 1 )
    EVT_TREEBOOK_NODE_EXPANDED = wx.PyEventBinder( wxEVT_COMMAND_TREEBOOK_NODE_EXPANDED, 1 )
}

//---------------------------------------------------------------------------
%newgroup;

MustHaveApp(wxTreebook);

class wxToolbook : public wxBookCtrlBase
{
public:
    %pythonAppend wxToolbook         "self._setOORInfo(self)"
    %pythonAppend wxToolbook()       ""


    // This ctor creates the tree book control
    wxToolbook(wxWindow *parent,
               wxWindowID id,
               const wxPoint& pos = wxDefaultPosition,
               const wxSize& size = wxDefaultSize,
               long style = wxBK_DEFAULT,
               const wxString& name = wxPyEmptyString);

    %RenameCtor(PreToolbook, wxToolbook());

    // quasi ctor
    bool Create(wxWindow *parent,
                wxWindowID id,
                const wxPoint& pos = wxDefaultPosition,
                const wxSize& size = wxDefaultSize,
                long style = 0,
                const wxString& name = wxEmptyString);


    wxToolBarBase* GetToolBar() const;

    // Not part of the wxBookctrl API, but must be called in OnIdle or
    // by application to realize the toolbar and select the initial page.
    void Realize();

    %property(ToolBar, GetToolBar, doc="See `GetToolBar`");
};


%pythoncode {
ToolbookEvent = wx.BookCtrlEvent
}

%constant wxEventType wxEVT_COMMAND_TOOLBOOK_PAGE_CHANGED;
%constant wxEventType wxEVT_COMMAND_TOOLBOOK_PAGE_CHANGING;


%pythoncode {
    EVT_TOOLBOOK_PAGE_CHANGED = wx.PyEventBinder( wxEVT_COMMAND_TOOLBOOK_PAGE_CHANGED, 1)
    EVT_TOOLBOOK_PAGE_CHANGING = wx.PyEventBinder( wxEVT_COMMAND_TOOLBOOK_PAGE_CHANGING, 1)
}

//---------------------------------------------------------------------------
