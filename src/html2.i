/////////////////////////////////////////////////////////////////////////////
// Name:        html2.i
// Purpose:     SWIG definitions for the wxWebView and related classes.
//              NOTE: We're using the html2 module name because the
//              wxWebKit project is already producing a wx.webview module,
//              so it makes sense to try and differentiate the two.
//
// Author:      Robin Dunn
//
// Created:     14-Nov-2011
// RCS-ID:      $Id: $
// Copyright:   (c) 2011 by Total Control Software
// Licence:     wxWindows license
/////////////////////////////////////////////////////////////////////////////

%define DOCSTRING
"Classes for embedding a full web browser rendering engine in a window."
%enddef

%module(package="wx", docstring=DOCSTRING)  html2

%{
#include "wx/wxPython/wxPython.h"
#include "wx/wxPython/pyclasses.h"
#include "wx/wxPython/pyistream.h"
    
#include <wx/webview.h>
#include <wx/webviewarchivehandler.h>
%}


//---------------------------------------------------------------------------

%import core.i
%pythoncode { wx = _core }
%pythoncode { __docfilter__ = wx.__DocFilter(globals()) }

//---------------------------------------------------------------------------

%{
#if !wxUSE_WEBVIEW
// Add some C++ stubs for when wxWebView is not available

#include <wx/sharedptr.h>
#include <wx/vector.h>
 


enum wxWebViewZoom
{
    wxWEBVIEW_ZOOM_TINY,
    wxWEBVIEW_ZOOM_SMALL,
    wxWEBVIEW_ZOOM_MEDIUM, 
    wxWEBVIEW_ZOOM_LARGE,
    wxWEBVIEW_ZOOM_LARGEST
};

enum wxWebViewZoomType
{
    wxWEBVIEW_ZOOM_TYPE_LAYOUT,
    wxWEBVIEW_ZOOM_TYPE_TEXT
};


enum wxWebViewNavigationError
{
    wxWEBVIEW_NAV_ERR_CONNECTION,
    wxWEBVIEW_NAV_ERR_CERTIFICATE,
    wxWEBVIEW_NAV_ERR_AUTH,
    wxWEBVIEW_NAV_ERR_SECURITY,
    wxWEBVIEW_NAV_ERR_NOT_FOUND,
    wxWEBVIEW_NAV_ERR_REQUEST,
    wxWEBVIEW_NAV_ERR_USER_CANCELLED,
    wxWEBVIEW_NAV_ERR_OTHER
};

enum wxWebViewReloadFlags
{
    wxWEBVIEW_RELOAD_DEFAULT,
    wxWEBVIEW_RELOAD_NO_CACHE 
};

enum wxWebViewFindFlags
{
    wxWEBVIEW_FIND_WRAP =             0x0001,
    wxWEBVIEW_FIND_ENTIRE_WORD =      0x0002,
    wxWEBVIEW_FIND_MATCH_CASE =       0x0004,
    wxWEBVIEW_FIND_HIGHLIGHT_RESULT = 0x0008,
    wxWEBVIEW_FIND_BACKWARDS =        0x0010,
    wxWEBVIEW_FIND_DEFAULT =          0
};

wxString wxWebViewBackendDefault("");
wxString wxWebViewBackendIE("");
wxString wxWebViewBackendWebKit("");
wxString wxWebViewDefaultURLStr("");
wxString wxWebViewNameStr("");

class wxWebView;

inline void _RaiseError()
{
    wxPyRaiseNotImplementedMsg("wx.html2 is not available on this platform.");
}


class wxWebViewHandler
{
public:
    wxWebViewHandler(const wxString& scheme) {};
    virtual wxFSFile* GetFile(const wxString &uri) {return NULL;}
    virtual wxString GetName() const { return wxEmptyString; }
};


class wxWebViewArchiveHandler : public wxWebViewHandler
{
public:
    wxWebViewArchiveHandler(const wxString& scheme)  : wxWebViewHandler(scheme) {}
    virtual wxFSFile* GetFile(const wxString &uri) { return NULL; }
};


class wxWebViewHistoryItem
{
public:
    wxWebViewHistoryItem(const wxString&, const wxString&) { _RaiseError(); }
    wxString GetUrl() { return wxEmptyString; }
    wxString GetTitle() { return wxEmptyString; }
};


class wxWebViewFactory : public wxObject
{
public:
    virtual wxWebView* Create() = 0;

    virtual wxWebView* Create(wxWindow* parent,
                              wxWindowID id,
                              const wxString& url = wxWebViewDefaultURLStr,
                              const wxPoint& pos = wxDefaultPosition,
                              const wxSize& size = wxDefaultSize,
                              long style = 0,
                              const wxString& name = wxWebViewNameStr) = 0;
};

class wxWebView : public wxControl
{
public:
    virtual bool Create(wxWindow*, wxWindowID, const wxString&, const wxPoint&,
                        const wxSize&, long, const wxString&) { _RaiseError(); return false; }
    static wxWebView* New(const wxString&) { _RaiseError(); return NULL; }
    static wxWebView* New(wxWindow*, wxWindowID, const wxString&, const wxPoint& ,
                          const wxSize& , const wxString&, long,
                          const wxString&) { _RaiseError(); return NULL; }

    virtual wxString GetCurrentTitle() const { return wxEmptyString; }
    virtual wxString GetCurrentURL() const { return wxEmptyString; }
    virtual wxString GetPageSource() const { return wxEmptyString; }
    virtual wxString GetPageText() const { return wxEmptyString; }
    virtual bool IsBusy() const { return false; }
    virtual bool IsEditable() const { return false; }
    virtual void LoadURL(const wxString& url) {}
    virtual void Print() {}
    virtual void RegisterHandler(wxSharedPtr<wxWebViewHandler> handler) {}
    virtual void Reload(wxWebViewReloadFlags flags = wxWEBVIEW_RELOAD_DEFAULT) {}
    virtual void RunScript(const wxString& javascript) {}
    virtual void SetEditable(bool enable = true) {}
    virtual void SetPage(const wxString& html, const wxString& baseUrl) {}
    virtual void SetPage(wxInputStream& html, wxString baseUrl) {}
    virtual void Stop() {}
    virtual bool CanCopy() const { return false; }
    virtual bool CanCut() const { return false; }
    virtual bool CanPaste() const { return false; }
    virtual void Copy() {}
    virtual void Cut() {}
    virtual void Paste() {}
    virtual bool CanGoBack() const { return false; }
    virtual bool CanGoForward() const { return false; }
    virtual void ClearHistory() {}
    virtual void EnableHistory(bool enable = true) {}
    //virtual wxVector<wxSharedPtr<wxWebViewHistoryItem> > GetBackwardHistory();
    //virtual wxVector<wxSharedPtr<wxWebViewHistoryItem> > GetForwardHistory();
    virtual void GoBack() {}
    virtual void GoForward() {}
    virtual void LoadHistoryItem(wxSharedPtr<wxWebViewHistoryItem> item) {}
    virtual void ClearSelection() {}
    virtual void DeleteSelection() {}
    virtual wxString GetSelectedSource() const { return wxEmptyString; }
    virtual wxString GetSelectedText() const  { return wxEmptyString; }
    virtual bool HasSelection() const { return false; }
    virtual void SelectAll() {}
    virtual bool CanRedo() const { return false; }
    virtual bool CanUndo() const { return false; }
    virtual void Redo() {}
    virtual void Undo() {}
    virtual bool CanSetZoomType(wxWebViewZoomType type) const { return false; }
    virtual wxWebViewZoom GetZoom() const { return wxWEBVIEW_ZOOM_MEDIUM; }
    virtual wxWebViewZoomType GetZoomType() const { return wxWEBVIEW_ZOOM_TYPE_LAYOUT; }
    virtual void SetZoom(wxWebViewZoom zoom) {}
    virtual void SetZoomType(wxWebViewZoomType zoomType) {}
    virtual void* GetNativeBackend() const { return NULL; }
    virtual long Find(const wxString& text, int flags = wxWEBVIEW_FIND_DEFAULT) { return 0; }
};



class wxWebViewEvent : public wxNotifyEvent
{
public:
    wxWebViewEvent(wxEventType type, int id, const wxString href,
                   const wxString target) { _RaiseError(); }
    const wxString& GetTarget() const { return m_empty; }
    const wxString& GetURL() const { return m_empty; }
private:
    wxString m_empty;
};


wxEventType wxEVT_WEBVIEW_NAVIGATING;
wxEventType wxEVT_WEBVIEW_NAVIGATED;
wxEventType wxEVT_WEBVIEW_LOADED;
wxEventType wxEVT_WEBVIEW_ERROR;
wxEventType wxEVT_WEBVIEW_NEWWINDOW;
wxEventType wxEVT_WEBVIEW_TITLE_CHANGED;

wxEventType wxEVT_COMMAND_WEBVIEW_NAVIGATING;
wxEventType wxEVT_COMMAND_WEBVIEW_NAVIGATED;
wxEventType wxEVT_COMMAND_WEBVIEW_LOADED;
wxEventType wxEVT_COMMAND_WEBVIEW_ERROR;
wxEventType wxEVT_COMMAND_WEBVIEW_NEWWINDOW;
wxEventType wxEVT_COMMAND_WEBVIEW_TITLE_CHANGED;


#endif  // !wxUSE_WEBVIEW
%}

//---------------------------------------------------------------------------
//---------------------------------------------------------------------------
%newgroup



enum wxWebViewZoom
{
    wxWEBVIEW_ZOOM_TINY,
    wxWEBVIEW_ZOOM_SMALL,
    wxWEBVIEW_ZOOM_MEDIUM, 
    wxWEBVIEW_ZOOM_LARGE,
    wxWEBVIEW_ZOOM_LARGEST
};

enum wxWebViewZoomType
{
    wxWEBVIEW_ZOOM_TYPE_LAYOUT,
    wxWEBVIEW_ZOOM_TYPE_TEXT
};


enum wxWebViewNavigationError
{
    wxWEBVIEW_NAV_ERR_CONNECTION,
    wxWEBVIEW_NAV_ERR_CERTIFICATE,
    wxWEBVIEW_NAV_ERR_AUTH,
    wxWEBVIEW_NAV_ERR_SECURITY,
    wxWEBVIEW_NAV_ERR_NOT_FOUND,
    wxWEBVIEW_NAV_ERR_REQUEST,
    wxWEBVIEW_NAV_ERR_USER_CANCELLED,
    wxWEBVIEW_NAV_ERR_OTHER
};

enum wxWebViewReloadFlags
{
    wxWEBVIEW_RELOAD_DEFAULT,
    wxWEBVIEW_RELOAD_NO_CACHE 
};

enum wxWebViewFindFlags
{
    wxWEBVIEW_FIND_WRAP =             0x0001,
    wxWEBVIEW_FIND_ENTIRE_WORD =      0x0002,
    wxWEBVIEW_FIND_MATCH_CASE =       0x0004,
    wxWEBVIEW_FIND_HIGHLIGHT_RESULT = 0x0008,
    wxWEBVIEW_FIND_BACKWARDS =        0x0010,
    wxWEBVIEW_FIND_DEFAULT =          0
};

MAKE_CONST_WXSTRING(WebViewBackendDefault);
MAKE_CONST_WXSTRING(WebViewBackendIE);
MAKE_CONST_WXSTRING(WebViewBackendWebKit);
MAKE_CONST_WXSTRING(WebViewDefaultURLStr);
MAKE_CONST_WXSTRING(WebViewNameStr);


//---------------------------------------------------------------------------

class wxWebViewHistoryItem
{
public:
    /**
        Construtor.
    */
    wxWebViewHistoryItem(const wxString& url, const wxString& title);
    
    /**
        @return The url of the page.
    */
    wxString GetUrl();
    
    /**
        @return The title of the page.
    */
    wxString GetTitle();
};


//---------------------------------------------------------------------------
class wxWebViewFactory : public wxObject
{
public:
    /**
        Function to create a new wxWebView with two-step creation,
        wxWebView::Create should be called on the returned object.
        @return the created wxWebView
     */
    virtual wxWebView* Create() = 0;

    /**
        Function to create a new wxWebView with parameters.
        @param parent Parent window for the control
        @param id ID of this control
        @param url Initial URL to load
        @param pos Position of the control
        @param size Size of the control
        @return the created wxWebView
    */
    virtual wxWebView* Create(wxWindow* parent,
                              wxWindowID id,
                              const wxString& url = wxWebViewDefaultURLStr,
                              const wxPoint& pos = wxDefaultPosition,
                              const wxSize& size = wxDefaultSize,
                              long style = 0,
                              const wxString& name = wxWebViewNameStr) = 0;
};

//---------------------------------------------------------------------------



//---------------------------------------------------------------------------


MustHaveApp(wxWebView);

class wxWebView : public wxControl
{
public:

    /**
        Creation function for two-step creation.
    */
    virtual bool Create(wxWindow* parent,
                        wxWindowID id = wxID_ANY,
                        const wxString& url = wxWebViewDefaultURLStr,
                        const wxPoint& pos = wxDefaultPosition,
                        const wxSize& size = wxDefaultSize,
                        long style = 0,
                        const wxString& name = wxWebViewNameStr);

    /**
        Factory function to create a new wxWebView for two-step creation
        (you need to call wxWebView::Create on the returned object)
        @param backend which web engine to use as backend for wxWebView
        @return the created wxWebView, or NULL if the requested backend is
                not available
     */
    %newobject New;
    %Rename(PreNew,
            static wxWebView*, New(const wxString& backend = wxWebViewBackendDefault));
    
    /**
        Factory function to create a new wxWebView
        @param parent parent window to create this view in
        @param id ID of this control
        @param url URL to load by default in the web view
        @param pos position to create this control at
               (you may use wxDefaultPosition if you use sizers)
        @param size size to create this control with
               (you may use wxDefaultSize if you use sizers)
        @param backend which web engine to use as backend for wxWebView
        @return the created wxWebView, or NULL if the requested backend
                is not available
    */
    %newobject New;
    %pythonAppend  New  "val._setOORInfo(val)"
    static wxWebView* New(wxWindow* parent,
           wxWindowID id = wxID_ANY,
           const wxString& url = wxWebViewDefaultURLStr,
           const wxPoint& pos = wxDefaultPosition,
           const wxSize& size = wxDefaultSize,
           const wxString& backend = wxWebViewBackendDefault,
           long style = 0,
           const wxString& name = wxWebViewNameStr);

    
    /**
        Get the title of the current web page, or its URL/path if title is not
        available.
    */
    virtual wxString GetCurrentTitle() const;

   /**
        Get the URL of the currently displayed document.
    */
    virtual wxString GetCurrentURL() const;

    /**
        Get the HTML source code of the currently displayed document.
        @return The HTML source code, or an empty string if no page is currently
                shown.
    */
    virtual wxString GetPageSource() const;
    
    /**
        Get the text of the current page.
    */
    virtual wxString GetPageText() const;
    
    /**
        Returns whether the web control is currently busy (e.g. loading a page).
    */
    virtual bool IsBusy() const;

    /**
        Returns whether the web control is currently editable
    */
    virtual bool IsEditable() const;

    /**
        Load a web page from a URL
        @param url The URL of the page to be loaded.
        @note Web engines generally report errors asynchronously, so if you wish
            to know whether loading the URL was successful, register to receive
            navigation error events.
    */
    virtual void LoadURL(const wxString& url);

    /**
        Opens a print dialog so that the user may print the currently
        displayed page.
    */
    virtual void Print();
    
    /**
        Registers a custom scheme handler.
        @param handler A shared pointer to a wxWebHandler.
    */
    virtual void RegisterHandler(wxSharedPtr<wxWebViewHandler> handler);

    /**
        Reload the currently displayed URL.
        @param flags A bit array that may optionally contain reload options.
    */
    virtual void Reload(wxWebViewReloadFlags flags = wxWEBVIEW_RELOAD_DEFAULT);
    
    /**
        Runs the given javascript code. 
    */
    virtual void RunScript(const wxString& javascript);
    
    /**
        Set the editable property of the web control. Enabling allows the user
        to edit the page even if the @c contenteditable attribute is not set.
        The exact capabilities vary with the backend being used.
    */
    virtual void SetEditable(bool enable = true);

    /**
        Set the displayed page source to the contents of the given string.
        @param html    The string that contains the HTML data to display.
        @param baseUrl URL assigned to the HTML data, to be used to resolve
                    relative paths, for instance.
    */
    %nokwargs SetPage;
    virtual void SetPage(const wxString& html, const wxString& baseUrl);

    /**
        Set the displayed page source to the contents of the given stream.
        @param html    The stream to read HTML data from.
        @param baseUrl URL assigned to the HTML data, to be used to resolve
                    relative paths, for instance.
    */
    virtual void SetPage(wxInputStream& html, wxString baseUrl);

    /**
        Stop the current page loading process, if any.
        May trigger an error event of type @c wxWEBVIEW_NAV_ERR_USER_CANCELLED.
        TODO: make @c wxWEBVIEW_NAV_ERR_USER_CANCELLED errors uniform across ports.
    */
    virtual void Stop();

    /**
        @name Clipboard
    */

    /**
        Returns @true if the current selection can be copied.
        
        @note This always returns @c true on the OSX WebKit backend.
    */
    virtual bool CanCopy() const;

    /**
        Returns @true if the current selection can be cut.
        
         @note This always returns @c true on the OSX WebKit backend.
    */
    virtual bool CanCut() const;

    /**
        Returns @true if data can be pasted.
        
        @note This always returns @c true on the OSX WebKit backend.
    */
    virtual bool CanPaste() const;

    /**
        Copies the current selection. 
    */
    virtual void Copy();

    /**
        Cuts the current selection.
    */
    virtual void Cut();

    /**
        Pastes the current data.
    */
    virtual void Paste();

    /**
        @name History
    */

    /** 
        Returns @true if it is possible to navigate backward in the history of
        visited pages.
    */
    virtual bool CanGoBack() const;

    /** 
        Returns @true if it is possible to navigate forward in the history of
        visited pages.
    */
    virtual bool CanGoForward() const;

    /**
        Clear the history, this will also remove the visible page.
    */
    virtual void ClearHistory();

    /**
        Enable or disable the history. This will also clear the history.
    */
    virtual void EnableHistory(bool enable = true);

    /**
        Returns a list of items in the back history. The first item in the
        vector is the first page that was loaded by the control.
    */
//    virtual wxVector<wxSharedPtr<wxWebViewHistoryItem> > GetBackwardHistory();

    /**
        Returns a list of items in the forward history. The first item in the 
        vector is the next item in the history with respect to the curently 
        loaded page.
    */
//    virtual wxVector<wxSharedPtr<wxWebViewHistoryItem> > GetForwardHistory();

    /** 
        Navigate back in the history of visited pages.
        Only valid if CanGoBack() returns true.
    */
    virtual void GoBack();

    /**
        Navigate forward in the history of visited pages.
        Only valid if CanGoForward() returns true.
    */
    virtual void GoForward();

    /**
        Loads a history item. 
    */
    virtual void LoadHistoryItem(wxSharedPtr<wxWebViewHistoryItem> item);
    
    /**
        @name Selection
    */
    
    /**
        Clears the current selection. 
    */
    virtual void ClearSelection();
    
    /**
        Deletes the current selection. Note that for @c wxWEBVIEW_BACKEND_WEBKIT
        the selection must be editable, either through SetEditable or the 
        correct HTML attribute.
    */
    virtual void DeleteSelection();
    
    /**
        Returns the currently selected source, if any.
    */
    virtual wxString GetSelectedSource() const;
    
    /**
        Returns the currently selected text, if any.
    */
    virtual wxString GetSelectedText() const;

    /**
        Returns @true if there is a current selection.
    */
    virtual bool HasSelection() const;

    /**
        Selects the entire page.
    */
    virtual void SelectAll();

    /**
        @name Undo / Redo
    */

    /**
        Returns @true if there is an action to redo.
    */
    virtual bool CanRedo() const;

    /**
        Returns @true if there is an action to undo.
    */
    virtual bool CanUndo() const;

    /**
        Redos the last action.
    */
    virtual void Redo();

    /**
        Undos the last action.
    */
    virtual void Undo();

    /**
        @name Zoom
    */

    /**
        Retrieve whether the current HTML engine supports a zoom type.
        @param type The zoom type to test.
        @return Whether this type of zoom is supported by this HTML engine
                (and thus can be set through SetZoomType()).
    */
    virtual bool CanSetZoomType(wxWebViewZoomType type) const;

    /**
        Get the zoom factor of the page.
        @return The current level of zoom.
    */
    virtual wxWebViewZoom GetZoom() const;

    /**
        Get how the zoom factor is currently interpreted.
        @return How the zoom factor is currently interpreted by the HTML engine.
    */
    virtual wxWebViewZoomType GetZoomType() const;

    /**
        Set the zoom factor of the page.
        @param zoom How much to zoom (scale) the HTML document.
    */
    virtual void SetZoom(wxWebViewZoom zoom);

    /**
        Set how to interpret the zoom factor.
        @param zoomType How the zoom factor should be interpreted by the
                        HTML engine.
        @note invoke    CanSetZoomType() first, some HTML renderers may not
                        support all zoom types.
    */
    virtual void SetZoomType(wxWebViewZoomType zoomType);

    virtual void* GetNativeBackend() const;
    virtual long Find(const wxString& text, int flags = wxWEBVIEW_FIND_DEFAULT);
};


//---------------------------------------------------------------------------

class wxWebViewEvent : public wxNotifyEvent
{
public:
    //wxWebViewEvent();
    wxWebViewEvent(wxEventType type, int id, const wxString href,
                   const wxString target);

    /**
        Get the name of the target frame which the url of this event
        has been or will be loaded into. This may return an emptry string
        if the frame is not avaliable.
    */
    const wxString& GetTarget() const;

    /**
        Get the URL being visited
    */
    const wxString& GetURL() const;
};


%constant wxEventType wxEVT_WEBVIEW_NAVIGATING;
%constant wxEventType wxEVT_WEBVIEW_NAVIGATED;
%constant wxEventType wxEVT_WEBVIEW_LOADED;
%constant wxEventType wxEVT_WEBVIEW_ERROR;
%constant wxEventType wxEVT_WEBVIEW_NEWWINDOW;
%constant wxEventType wxEVT_WEBVIEW_TITLE_CHANGED;

%constant wxEventType wxEVT_COMMAND_WEBVIEW_NAVIGATING;
%constant wxEventType wxEVT_COMMAND_WEBVIEW_NAVIGATED;
%constant wxEventType wxEVT_COMMAND_WEBVIEW_LOADED;
%constant wxEventType wxEVT_COMMAND_WEBVIEW_ERROR;
%constant wxEventType wxEVT_COMMAND_WEBVIEW_NEWWINDOW;
%constant wxEventType wxEVT_COMMAND_WEBVIEW_TITLE_CHANGED;

%pythoncode {
    EVT_WEBVIEW_NAVIGATING = wx.PyEventBinder( wxEVT_WEBVIEW_NAVIGATING, 1 )
    EVT_WEBVIEW_NAVIGATED = wx.PyEventBinder( wxEVT_WEBVIEW_NAVIGATED, 1 )
    EVT_WEBVIEW_LOADED = wx.PyEventBinder( wxEVT_WEBVIEW_LOADED, 1 )
    EVT_WEBVIEW_ERROR = wx.PyEventBinder( wxEVT_WEBVIEW_ERROR, 1 )
    EVT_WEBVIEW_NEWWINDOW = wx.PyEventBinder( wxEVT_WEBVIEW_NEWWINDOW, 1 )
    EVT_WEBVIEW_TITLE_CHANGED = wx.PyEventBinder( wxEVT_WEBVIEW_TITLE_CHANGED, 1 )
}

//---------------------------------------------------------------------------

class wxWebViewHandler
{
public:
    /**
        Constructor. Takes the name of the scheme that will be handled by this
        class for example @c file or @c zip.
    */
    wxWebViewHandler(const wxString& scheme);

    /**
        @return A pointer to the file represented by @c uri.
    */  
    virtual wxFSFile* GetFile(const wxString &uri) = 0;

    /**
        @return The name of the scheme, as passed to the constructor.
    */
    virtual wxString GetName() const = 0;
};


%{
class wxPyWebViewHandler : public wxWebViewHandler
{
public:
    wxPyWebViewHandler(const wxString& scheme)
        : wxWebViewHandler(scheme) {}

    virtual wxFSFile* GetFile(const wxString &uri)
    {
        wxPyBlock_t blocked = wxPyBeginBlockThreads();                          
        wxFSFile* rval=0;                                                       
        if (wxPyCBH_findCallback(m_myInst, "GetFile")) {                          
            PyObject* ro;                                                       
            ro = wxPyCBH_callCallbackObj(m_myInst, Py_BuildValue("()"));
            if (ro) {                                                           
                wxPyConvertSwigPtr(ro, (void **)&rval, wxT("wxFSFile"));        
                /* release ownership of the C++ wx.FSFile object. */            
                PyObject_SetAttrString(ro, "thisown", Py_False);                
                Py_DECREF(ro);                                                  
            }                                                                   
        }                                                                       
        wxPyEndBlockThreads(blocked);                                           
        return rval;                                                            
    }
    
    virtual wxString GetName() const
    {
        wxString rval;
        bool found;
        wxPyBlock_t blocked = wxPyBeginBlockThreads();
        if ((found = wxPyCBH_findCallback(m_myInst, "GetName"))) {
            PyObject* ro;
            ro = wxPyCBH_callCallbackObj(m_myInst, Py_BuildValue("()"));
            if (ro) {
                rval = Py2wxString(ro);
                Py_DECREF(ro);
            }
        }
        wxPyEndBlockThreads(blocked);
        return rval;        
    }

    PYPRIVATE;    
};
%}


class wxPyWebViewHandler : public wxWebViewHandler
{
public:
    %pythonAppend wxPyWebViewHandler  setCallbackInfo(PyWebViewHandler)

    wxPyWebViewHandler(const wxString& scheme);
    virtual wxFSFile* GetFile(const wxString &uri);
    virtual wxString GetName() const;
    
    void _setCallbackInfo(PyObject* self, PyObject* _class);
};


class wxWebViewArchiveHandler : public wxWebViewHandler
{
public:
    /**
        Constructor.
    */
    wxWebViewArchiveHandler(const wxString& scheme);
    virtual wxFSFile* GetFile(const wxString &uri);
};

//---------------------------------------------------------------------------
//---------------------------------------------------------------------------
//---------------------------------------------------------------------------



