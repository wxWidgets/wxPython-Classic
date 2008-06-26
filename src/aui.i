/////////////////////////////////////////////////////////////////////////////
// Name:        aui.i
// Purpose:     Wrappers for the wxAUI classes.
//
// Author:      Robin Dunn
//
// Created:     5-July-2006
// RCS-ID:      $Id$
// Copyright:   (c) 2006 by Total Control Software
// Licence:     wxWindows license
/////////////////////////////////////////////////////////////////////////////

%define DOCSTRING
"The wx.aui module is an Advanced User Interface library that aims to
implement \"cutting-edge\" interface usability and design features so
developers can quickly and easily create beautiful and usable
application interfaces.

**Vision and Design Principles**

wx.aui attempts to encapsulate the following aspects of the user
interface:

  * Frame Management: Frame management provides the means to open,
    move and hide common controls that are needed to interact with the
    document, and allow these configurations to be saved into
    different perspectives and loaded at a later time.

  * Toolbars: Toolbars are a specialized subset of the frame
    management system and should behave similarly to other docked
    components. However, they also require additional functionality,
    such as \"spring-loaded\" rebar support, \"chevron\" buttons and
    end-user customizability.

  * Modeless Controls: Modeless controls expose a tool palette or set
    of options that float above the application content while allowing
    it to be accessed. Usually accessed by the toolbar, these controls
    disappear when an option is selected, but may also be \"torn off\"
    the toolbar into a floating frame of their own.

  * Look and Feel: Look and feel encompasses the way controls are
    drawn, both when shown statically as well as when they are being
    moved. This aspect of user interface design incorporates \"special
    effects\" such as transparent window dragging as well as frame
    animation.

**wx.aui adheres to the following principles**

  - Use native floating frames to obtain a native look and feel for
    all platforms;

  - Use existing wxPython code where possible, such as sizer
    implementation for frame management;

  - Use standard wxPython coding conventions.


**Usage**

The following example shows a simple implementation that utilizes
`wx.aui.AuiManager` to manage three text controls in a frame window::

    import wx
    import wx.aui

    class MyFrame(wx.Frame):

        def __init__(self, parent, id=-1, title='wx.aui Test',
                     pos=wx.DefaultPosition, size=(800, 600),
                     style=wx.DEFAULT_FRAME_STYLE):
            wx.Frame.__init__(self, parent, id, title, pos, size, style)

            self._mgr = wx.aui.AuiManager(self)

            # create several text controls
            text1 = wx.TextCtrl(self, -1, 'Pane 1 - sample text',
                                wx.DefaultPosition, wx.Size(200,150),
                                wx.NO_BORDER | wx.TE_MULTILINE)

            text2 = wx.TextCtrl(self, -1, 'Pane 2 - sample text',
                                wx.DefaultPosition, wx.Size(200,150),
                                wx.NO_BORDER | wx.TE_MULTILINE)

            text3 = wx.TextCtrl(self, -1, 'Main content window',
                                wx.DefaultPosition, wx.Size(200,150),
                                wx.NO_BORDER | wx.TE_MULTILINE)

            # add the panes to the manager
            self._mgr.AddPane(text1, wx.LEFT, 'Pane Number One')
            self._mgr.AddPane(text2, wx.BOTTOM, 'Pane Number Two')
            self._mgr.AddPane(text3, wx.CENTER)

            # tell the manager to 'commit' all the changes just made
            self._mgr.Update()

            self.Bind(wx.EVT_CLOSE, self.OnClose)


        def OnClose(self, event):
            # deinitialize the frame manager
            self._mgr.UnInit()
            # delete the frame
            self.Destroy()


    app = wx.App()
    frame = MyFrame(None)
    frame.Show()
    app.MainLoop()
"
%enddef



%module(package="wx", docstring=DOCSTRING) aui

%{
#include "wx/wxPython/wxPython.h"
#include "wx/wxPython/raiihelpers.h"
#include "wx/wxPython/pyclasses.h"
#include <wx/aui/aui.h>
%}

//---------------------------------------------------------------------------

%import core.i
%import windows.i

%pythoncode { wx = _core }
%pythoncode { __docfilter__ = wx.__DocFilter(globals()) }


%include _aui_docstrings.i

//---------------------------------------------------------------------------

// Preprocessor stuff so SWIG doesn't get confused when %include-ing
// the aui .h files.
%ignore wxUSE_AUI;
%ignore wxUSE_MENUS;
%ignore wxABI_VERSION;
#define wxUSE_AUI 1
#define wxUSE_MENUS 1
#define wxABI_VERSION 99999

#define WXDLLIMPEXP_AUI
#define WXDLLIMPEXP_FWD_AUI
#define unsigned
#define wxDEPRECATED(decl)
#define DECLARE_EVENT_TABLE()
#define DECLARE_DYNAMIC_CLASS(foo)



// We'll skip making wrappers for these, they have overloads that take a
// wxSize or wxPoint
%ignore wxAuiPaneInfo::MaxSize(int x, int y);
%ignore wxAuiPaneInfo::MinSize(int x, int y);
%ignore wxAuiPaneInfo::BestSize(int x, int y);
%ignore wxAuiPaneInfo::FloatingPosition(int x, int y);
%ignore wxAuiPaneInfo::FloatingSize(int x, int y);

// But for these we will do the overloading (see %pythoncode below) so let's
// rename the C++ versions
%rename(_GetPaneByWidget) wxAuiManager::GetPane(wxWindow* window);
%rename(_GetPaneByName)   wxAuiManager::GetPane(const wxString& name);

%rename(_AddPane1) wxAuiManager::AddPane(wxWindow* window, const wxAuiPaneInfo& pane_info);
%rename(_AddPane2) wxAuiManager::AddPane(wxWindow* window, int direction = wxLEFT,
                                         const wxString& caption = wxEmptyString);

%rename(AddPaneAtPos) wxAuiManager::AddPane(wxWindow* window,
                                            const wxPaneInfo& pane_info,
                                            const wxPoint& drop_pos);

// A typemap for the return value of wxAuiManager::GetAllPanes
%typemap(out) wxAuiPaneInfoArray& {
    $result = PyList_New(0);
    for (size_t i=0; i < $1->GetCount(); i++) {
        PyObject* pane_obj = SWIG_NewPointerObj((void*)(&$1->Item(i)), SWIGTYPE_p_wxAuiPaneInfo, 0);
        PyList_Append($result, pane_obj);
    }
}

//%ignore wxAuiManager::~wxAuiManager;

%nokwargs wxAuiTabContainer::SetActivePage;

%pythonAppend wxAuiTabCtrl::wxAuiTabCtrl "self._setOORInfo(self)";

%pythonAppend wxAuiNotebook::wxAuiNotebook    "self._setOORInfo(self)";
%pythonAppend wxAuiNotebook::wxAuiNotebook()  "val._setOORInfo(val)";
%ignore wxAuiiNotebook::~wxAuiNotebook;
%rename(PreAuiNotebook) wxAuiNotebook::wxAuiNotebook();

// NB: Since we can't target the use of a typemap to specific methods make
// sure to check that the disown is only applied where it is expected...
%disownarg( wxAuiDockArt* art_provider );
%disownarg( wxAuiTabArt* art );


// Link error...
%ignore wxAuiDefaultTabArt::SetWindow;        

// ignore this overload
%ignore wxAuiTabContainer::GetPage(size_t idx) const;



%pythonAppend wxAuiMDIParentFrame::wxAuiMDIParentFrame    "self._setOORInfo(self)";
%pythonAppend wxAuiMDIParentFrame::wxAuiMDIParentFrame()  "val._setOORInfo(val)";
%ignore wxAuiMDIParentFrame::~wxAuiMDIParentFrame;
%rename(PreAuiMDIParentFrame) wxAuiMDIParentFrame::wxAuiMDIParentFrame();

// Ignore these for now because they need a typemap for the return value, see below.
%ignore wxAuiMDIParentFrame::GetNotebook;
%ignore wxAuiMDIParentFrame::GetActiveChild;
%ignore wxAuiMDIParentFrame::GetClientWindow;

%pythonAppend wxAuiMDIChildFrame::wxAuiMDIChildFrame    "self._setOORInfo(self)";
%pythonAppend wxAuiMDIChildFrame::wxAuiMDIChildFrame()  "val._setOORInfo(val)";
%ignore wxAuiMDIChildFrame::~wxAuiMDIChildFrame;
%rename(PreAuiMDIChildFrame) wxAuiMDIChildFrame::wxAuiMDIChildFrame();

%pythonAppend wxAuiMDIClientWindow::wxAuiMDIClientWindow    "self._setOORInfo(self)";
%pythonAppend wxAuiMDIClientWindow::wxAuiMDIClientWindow()  "val._setOORInfo(val)";
%ignore wxAuiMDIClientWindow::~wxAuiMDIClientWindow;
%rename(PreAuiMDIClientWindow) wxAuiMDIClientWindow::wxAuiMDIClientWindow();


%typemap(out) wxEvtHandler*             { $result = wxPyMake_wxObject($1, $owner); }

//---------------------------------------------------------------------------
// Get all our defs from the REAL header files.

#define wxColor wxColour  // fix problem in dockart.h

%include framemanager.h
%include dockart.h
%include floatpane.h
%include auibook.h
%include tabmdi.h

#undef wxColor

//---------------------------------------------------------------------------
// Methods to inject into the AuiManager class that will sort out calls to
// the overloaded versions of GetPane and AddPane

%extend wxAuiManager {
    %pythoncode {
    def GetPane(self, item):
        """
        GetPane(self, window_or_info item) -> PaneInfo

        GetPane is used to search for a `PaneInfo` object either by
        widget reference or by pane name, which acts as a unique id
        for a window pane. The returned `PaneInfo` object may then be
        modified to change a pane's look, state or position. After one
        or more modifications to the `PaneInfo`, `AuiManager.Update`
        should be called to realize the changes to the user interface.

        If the lookup failed (meaning the pane could not be found in
        the manager) GetPane returns an empty `PaneInfo`, a condition
        which can be checked by calling `PaneInfo.IsOk`.
        """
        if isinstance(item, wx.Window):
            return self._GetPaneByWidget(item)
        else:
            return self._GetPaneByName(item)

    def AddPane(self, window, info=None, caption=None):
        """
        AddPane(self, window, info=None, caption=None) -> bool

        AddPane tells the frame manager to start managing a child
        window. There are two versions of this function. The first
        verison accepts a `PaneInfo` object for the ``info`` parameter
        and allows the full spectrum of pane parameter
        possibilities. (Say that 3 times fast!)

        The second version is used for simpler user interfaces which
        do not require as much configuration.  In this case the
        ``info`` parameter specifies the direction property of the
        pane info, and defaults to ``wx.LEFT``.  The pane caption may
        also be specified as an extra parameter in this form.
        """
        if type(info) == AuiPaneInfo:
            return self._AddPane1(window, info)
        else:
            # This Is AddPane2
            if info is None:
                info = wx.LEFT
            if caption is None:
                caption = ""
            return self._AddPane2(window, info, caption)
    }

    // For backwards compatibility
    %pythoncode {
         SetFrame = wx._deprecated(SetManagedWindow,
                                   "SetFrame is deprecated, use `SetManagedWindow` instead.")
         GetFrame = wx._deprecated(GetManagedWindow,
                                   "GetFrame is deprecated, use `GetManagedWindow` instead.")
    }
}

%extend wxAuiDockInfo {
    ~wxAuiDockInfo() {}
}

%extend wxAuiDockUIPart {
    ~wxAuiDockUIPart() {}
}

%extend wxAuiPaneButton {
    ~wxAuiPaneButton() {}
}

%extend wxAuiMDIParentFrame {
    %typemap(out) wxAuiNotebook*          { $result = wxPyMake_wxObject($1, $owner); }
    %typemap(out) wxAuiMDIChildFrame*     { $result = wxPyMake_wxObject($1, $owner); }
    %typemap(out) wxAuiMDIClientWindow*   { $result = wxPyMake_wxObject($1, $owner); }

    %rename(GetNotebook) _GetNotebook;
    %rename(GetActiveChild) _GetActiveChild;
    %rename(GetClientWindow) _GetClientWindow;
     
    wxAuiNotebook* _GetNotebook() const
    {
        return self->GetNotebook();
    }
    
    wxAuiMDIChildFrame* _GetActiveChild() const
    {
        return self->GetActiveChild();
    }
    
    wxAuiMDIClientWindow* _GetClientWindow() const
    {
        return self->GetClientWindow();
    }

    %typemap(out) wxAuiNotebook*;       
    %typemap(out) wxAuiMDIChildFrame*;  
    %typemap(out) wxAuiMDIClientWindow*;
}
     
     
//---------------------------------------------------------------------------

%{
inline wxPyObject &operator<<(wxPyObject &po, const wxAuiPaneInfo &p)
{
    po.Push(wxPyConstructObject((void*)&p, wxT("wxAuiPaneInfo"), 0));
    return po;
}

inline wxPyObject &operator<<(wxPyObject &po, const wxAuiNotebookPage &p)
{
    po.Push(wxPyConstructObject((void*)&p, wxT("wxAuiNotebookPage"), 0));
    return po;
}

%}

%{
// A wxDocArt class that knows how to forward virtuals to Python methods
class wxPyAuiDockArt :  public wxAuiDefaultDockArt
{
public:
    wxPyAuiDockArt() : wxAuiDefaultDockArt() {}

    PYCALLBACK_1_EXTRACT(wxAuiDefaultDockArt, int, rval = -1, GetMetric, (int a))
    PYCALLBACK_2_VOID(wxAuiDefaultDockArt, SetMetric, (int a, int b))
    PYCALLBACK_2_VOID(wxAuiDefaultDockArt, SetFont, (int a, const wxFont &b))
    PYCALLBACK_1_EXTRACT(wxAuiDefaultDockArt, wxFont, rval, GetFont, (int a))
    PYCALLBACK_2_VOID(wxAuiDefaultDockArt, SetColour, (int a, const wxColour &b))
    PYCALLBACK_1_EXTRACT(wxAuiDefaultDockArt, wxColour, rval, GetColor, (int a))
    PYCALLBACK_4_VOID(wxAuiDefaultDockArt, DrawSash, (wxDC &a, wxWindow *b, int c, const wxRect &d))
    PYCALLBACK_4_VOID(wxAuiDefaultDockArt, DrawBackground, (wxDC &a, wxWindow *b, int c, const wxRect &d))
    PYCALLBACK_5_VOID(wxAuiDefaultDockArt, DrawCaption, (wxDC &a, wxWindow *b, const wxString &c,
                                                        const wxRect &d, wxAuiPaneInfo &e))
    PYCALLBACK_4_VOID(wxAuiDefaultDockArt, DrawGripper, (wxDC &a, wxWindow *b, const wxRect &c, wxAuiPaneInfo &d))
    PYCALLBACK_4_VOID(wxAuiDefaultDockArt, DrawBorder, (wxDC &a, wxWindow *b, const wxRect &c, wxAuiPaneInfo &d))
    PYCALLBACK_6_VOID(wxAuiDefaultDockArt, DrawPaneButton, (wxDC &a, wxWindow *b, int c, int d, 
                                                            const wxRect &e, wxAuiPaneInfo &f))

    PYPRIVATE;

};

%}


DocStr(wxPyAuiDockArt,
"This version of the `AuiDockArt` class has been instrumented to be
subclassable in Python and to reflect all calls to the C++ base class
methods to the Python methods implemented in the derived class.", "");

class wxPyAuiDockArt :  public wxAuiDefaultDockArt
{
public:
    %pythonAppend wxPyAuiDockArt     setCallbackInfo(PyAuiDockArt)
    wxPyAuiDockArt();

    void _setCallbackInfo(PyObject* self, PyObject* _class);
};


//---------------------------------------------------------------------------

%extend wxAuiNotebook {
    %property(PageCount, GetPageCount, doc="See `GetPageCount`");
    %property(Selection, GetSelection, SetSelection, doc="See `GetSelection` and `SetSelection`");
}


%extend wxAuiNotebookEvent {
    %property(OldSelection, GetOldSelection, SetOldSelection, doc="See `GetOldSelection` and `SetOldSelection`");
    %property(Selection, GetSelection, SetSelection, doc="See `GetSelection` and `SetSelection`");
}


%extend wxAuiTabContainer {
    %property(ActivePage, GetActivePage, SetActivePage, doc="See `GetActivePage` and `SetActivePage`");
    %property(PageCount, GetPageCount, doc="See `GetPageCount`");
    %property(Pages, GetPages, doc="See `GetPages`");
}


%extend wxAuiManager {
    %property(AllPanes, GetAllPanes, doc="See `GetAllPanes`");
    %property(ArtProvider, GetArtProvider, SetArtProvider, doc="See `GetArtProvider` and `SetArtProvider`");
    %property(Flags, GetFlags, SetFlags, doc="See `GetFlags` and `SetFlags`");
    %property(ManagedWindow, GetManagedWindow, SetManagedWindow, doc="See `GetManagedWindow` and `SetManagedWindow`");
}


%extend wxAuiManagerEvent {
    %property(Button, GetButton, SetButton, doc="See `GetButton` and `SetButton`");
    %property(DC, GetDC, SetDC, doc="See `GetDC` and `SetDC`");
    %property(Pane, GetPane, SetPane, doc="See `GetPane` and `SetPane`");
}


//---------------------------------------------------------------------------

%{
// A wxTabArt class that knows how to forward virtuals to Python methods
class wxPyAuiTabArt :  public wxAuiDefaultTabArt
{
public:
    wxPyAuiTabArt() : wxAuiDefaultTabArt() {}


    PYCALLBACK_3_VOID(wxAuiDefaultTabArt, DrawBackground, (wxDC &a, wxWindow *b, const wxRect &c))   

    virtual void DrawTab( wxDC& dc,
                          wxWindow* wnd,
                          const wxAuiNotebookPage& pane,
                          const wxRect& in_rect,
                          int close_button_state,
                          wxRect* out_tab_rect,
                          wxRect* out_button_rect,
                          int* x_extent)
    {
        bool found;
        const char* errmsg = "DrawTab should return a sequence containing (tab_rect, button_rect, x_extent)";
        wxPyThreadBlocker blocker;
        if ((found = wxPyCBH_findCallback(m_myInst, "DrawTab"))) {
            wxPyTuple args(5);
            wxPySequence ro;
            ro = wxPyCBH_callCallbackObj(m_myInst, args << dc << wnd << pane << in_rect << close_button_state,
                    wxPCBH_ERR_THROW);
            if (ro.Ok()) {
                if (ro.IsSequence() && ro.Size() == 3)
                    ro >> *out_tab_rect >> *out_button_rect >> *x_extent;
                else {
                    PyErr_SetString(PyExc_TypeError, errmsg);
                    wxThrowPyException();
                }
            }
        }
        blocker.Unblock();
        if (!found)
            wxAuiDefaultTabArt::DrawTab(dc, wnd, pane, in_rect, close_button_state, out_tab_rect, out_button_rect, x_extent);
    }


    virtual void DrawButton( wxDC& dc,
                             wxWindow* wnd,
                             const wxRect& in_rect,
                             int bitmap_id,
                             int button_state,
                             int orientation,
                             wxRect* out_rect)
    {
        bool found;
        const char* errmsg = "DrawButton should return a wxRect";
        wxPyThreadBlocker blocker;
        if ((found = wxPyCBH_findCallback(m_myInst, "DrawButton"))) {
            wxPyTuple args(6);
            wxPyObject ro;
            ro = wxPyCBH_callCallbackObj(m_myInst, args << dc << wnd << in_rect << bitmap_id << button_state << orientation,
                    wxPCBH_ERR_THROW);
            if (ro.Ok() && !wxRect_helper(ro.Get(), &out_rect)) {
                PyErr_SetString(PyExc_TypeError, errmsg);
                wxThrowPyException();
            }
        }
        blocker.Unblock();
        if (!found)
            wxAuiDefaultTabArt::DrawButton(dc, wnd, in_rect, bitmap_id, button_state, orientation, out_rect);
    }


    virtual wxSize GetTabSize( wxDC& dc,
                               wxWindow* wnd,
                               const wxString& caption,
                               const wxBitmap& bitmap,
                               bool active,
                               int  close_button_state,
                               int* x_extent)
    {
        bool found;
        wxSize rv;
        const char* errmsg = "GetTabSize should return a sequence containing (size, x_extent)";
        wxPyThreadBlocker blocker;
        if ((found = wxPyCBH_findCallback(m_myInst, "GetTabSize"))) {
            wxPyTuple args(6);
            wxPySequence ro;
            ro = wxPyCBH_callCallbackObj(m_myInst, args << dc << wnd << caption << bitmap << active << close_button_state,
                    wxPCBH_ERR_THROW);
            if (ro.Ok()) {
                if (ro.IsSequence() && ro.Size() == 2)
                    ro >> rv >> *x_extent;
                else {
                    PyErr_SetString(PyExc_TypeError, errmsg);
                    wxThrowPyException();
                }
            }
        }
        blocker.Unblock();
        if (!found)
            rv = wxAuiDefaultTabArt::GetTabSize(dc, wnd, caption, bitmap, active, close_button_state, x_extent);
        return rv;
    }

// TODO    
//     virtual int ShowDropDown(
//                          wxWindow* wnd,
//                          const wxAuiNotebookPageArray& items,
//                          int active_idx);

//     virtual int GetIndentSize();

//     virtual int GetBestTabCtrlSize(wxWindow* wnd,
//                                    const wxAuiNotebookPageArray& pages, 
//                                    const wxSize& required_bmp_size);      
//     virtual wxAuiTabArt* Clone();
//     virtual void SetFlags(unsigned int flags);
//     virtual void SetSizingInfo(const wxSize& tab_ctrl_size,
//                                size_t tab_count);
//     virtual int GetIndentSize();
    


    PYCALLBACK_1_VOID(wxAuiDefaultTabArt, SetNormalFont, (const wxFont &a))
    PYCALLBACK_1_VOID(wxAuiDefaultTabArt, SetSelectedFont, (const wxFont &a))
    PYCALLBACK_1_VOID(wxAuiDefaultTabArt, SetMeasuringFont, (const wxFont &a))

    PYPRIVATE;
};

%}


DocStr(wxPyAuiTabArt,
"This version of the `TabArt` class has been instrumented to be
subclassable in Python and to reflect all calls to the C++ base class
methods to the Python methods implemented in the derived class.", "");

class wxPyAuiTabArt :  public wxAuiDefaultTabArt
{
public:
    %pythonAppend wxPyAuiTabArt     setCallbackInfo(PyAuiTabArt)
    wxPyAuiTabArt();

    void _setCallbackInfo(PyObject* self, PyObject* _class);   
};


//---------------------------------------------------------------------------


