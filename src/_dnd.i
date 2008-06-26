/////////////////////////////////////////////////////////////////////////////
// Name:        _dnd.i
// Purpose:     SWIG definitions for the Drag-n-drop classes
//
// Author:      Robin Dunn
//
// Created:     31-October-1999
// RCS-ID:      $Id$
// Copyright:   (c) 2003 by Total Control Software
// Licence:     wxWindows license
/////////////////////////////////////////////////////////////////////////////

// Not a %module


//---------------------------------------------------------------------------
#ifndef __WXX11__

%newgroup

// flags for wxDropSource::DoDragDrop()
//
// NB: wxDrag_CopyOnly must be 0 (== False) and wxDrag_AllowMove must be 1
//     (== True) for compatibility with the old DoDragDrop(bool) method!
enum
{
    wxDrag_CopyOnly    = 0, // allow only copying
    wxDrag_AllowMove   = 1, // allow moving (copying is always allowed)
    wxDrag_DefaultMove = 3  // the default operation is move, not copy
};

// result of wxDropSource::DoDragDrop() call
enum wxDragResult
{
    wxDragError,    // error prevented the d&d operation from completing
    wxDragNone,     // drag target didn't accept the data
    wxDragCopy,     // the data was successfully copied
    wxDragMove,     // the data was successfully moved (MSW only)
    wxDragLink,     // operation is a drag-link
    wxDragCancel    // the operation was cancelled by user (not an error)
};

bool wxIsDragResultOk(wxDragResult res);

//---------------------------------------------------------------------------


%{
// Extractor to cast int to wxDragResult
inline wxPyObject &operator>>(wxPyObject &po, wxDragResult &out)
{
    int iout = 0;
    po >> iout;
    out = (wxDragResult)iout;
    return po; 
}
%}

// wxDropSource is the object you need to create (and call DoDragDrop on it)
// to initiate a drag-and-drop operation



%{
IMP_PYCALLBACK_1_EXTRACT(wxPyDropSource, wxDropSource, bool, rval = false, GiveFeedback, 
                            (wxDragResult a))
%}


%rename(DropSource) wxPyDropSource;
class wxPyDropSource {
public:
    %pythonAppend wxPyDropSource setCallbackInfo(DropSource)
#ifndef __WXGTK__
     wxPyDropSource(wxWindow *win,
                    const wxCursor &copy = wxNullCursor,
                    const wxCursor &move = wxNullCursor,
                    const wxCursor &none = wxNullCursor);
#else
    wxPyDropSource(wxWindow *win,
                   const wxIcon& copy = wxNullIcon,
                   const wxIcon& move = wxNullIcon,
                   const wxIcon& none = wxNullIcon);
#endif

    void _setCallbackInfo(PyObject* self, PyObject* _class, int incref=0);
    ~wxPyDropSource();

    // set the data which is transfered by drag and drop
    void SetData(wxDataObject& data);

    wxDataObject *GetDataObject();

    // set the icon corresponding to given drag result
    void SetCursor(wxDragResult res, const wxCursor& cursor);

    wxDragResult DoDragDrop(int flags = wxDrag_CopyOnly);

    bool GiveFeedback(wxDragResult effect);
    %MAKE_BASE_FUNC(DropSource, GiveFeedback);

    %property(DataObject, GetDataObject, SetData, doc="See `GetDataObject` and `SetData`");
};


%pythoncode {
def DROP_ICON(filename):
    """
    Returns either a `wx.Cursor` or `wx.Icon` created from the image file
    ``filename``.  This function is useful with the `wx.DropSource` class
    which, depending on platform accepts either a icon or a cursor.
    """
    img = wx.Image(filename)
    if wx.Platform == '__WXGTK__':
        return wx.IconFromBitmap(wx.BitmapFromImage(img))
    else:
        return wx.CursorFromImage(img)
}


//---------------------------------------------------------------------------

// wxDropTarget should be associated with a window if it wants to be able to
// receive data via drag and drop.
//
// To use this class, you should derive from wxDropTarget and implement
// OnData() pure virtual method. You may also wish to override OnDrop() if you
// want to accept the data only inside some region of the window (this may
// avoid having to copy the data to this application which happens only when
// OnData() is called)


// Just a place holder for the type system.  The real base class for
// wxPython is wxPyDropTarget
// class wxDropTarget {
// public:
// };


%{
IMP_PYCALLBACK_0_VOID(wxPyDropTarget, wxDropTarget, OnLeave)
IMP_PYCALLBACK_3_EXTRACT(wxPyDropTarget, wxDropTarget, wxDragResult, rval = (wxDragResult)0, OnEnter, 
                            (wxCoord a, wxCoord b, wxDragResult c))
IMP_PYCALLBACK_3_EXTRACT(wxPyDropTarget, wxDropTarget, wxDragResult, rval = (wxDragResult)0, OnDragOver,
                            (wxCoord a, wxCoord b, wxDragResult c))
IMP_PYCALLBACK_3_EXTRACT(wxPyDropTarget, wxDropTarget, wxDragResult, rval = (wxDragResult)0, OnData,
                            (wxCoord a, wxCoord b, wxDragResult c))
IMP_PYCALLBACK_2_EXTRACT(wxPyDropTarget, wxDropTarget, bool, rval = false, OnDrop, (int a, int b))
%}


%rename(DropTarget) wxPyDropTarget;
class wxPyDropTarget // : public wxDropTarget
{
public:
    %pythonAppend wxPyDropTarget      setCallbackInfo(DropTarget)

    %disownarg( wxDataObject *dataObject );

    wxPyDropTarget(wxDataObject *dataObject = NULL);
    void _setCallbackInfo(PyObject* self, PyObject* _class);

    ~wxPyDropTarget();

    // get/set the associated wxDataObject
    wxDataObject *GetDataObject();
    void SetDataObject(wxDataObject *dataObject);

    %cleardisown( wxDataObject *dataObject );

    wxDragResult OnEnter(wxCoord x, wxCoord y, wxDragResult def);
    wxDragResult OnDragOver(wxCoord x, wxCoord y, wxDragResult def);
    void OnLeave();
    bool OnDrop(wxCoord x, wxCoord y);

    %MAKE_BASE_FUNC(DropTarget, OnEnter);
    %MAKE_BASE_FUNC(DropTarget, OnDragOver);
    %MAKE_BASE_FUNC(DropTarget, OnLeave);
    %MAKE_BASE_FUNC(DropTarget, OnDrop);

    
    // may be called *only* from inside OnData() and will fill m_dataObject
    // with the data from the drop source if it returns True
    bool GetData();

    // sets the default action for drag and drop:
    // use wxDragMove or wxDragCopy to set deafult action to move or copy
    // and use wxDragNone (default) to set default action specified by
    // initialization of draging (see wxDropSourceBase::DoDragDrop())
    void SetDefaultAction(wxDragResult action);

    // returns default action for drag and drop or
    // wxDragNone if this not specified
    wxDragResult GetDefaultAction();
    
    %property(DataObject, GetDataObject, SetDataObject, doc="See `GetDataObject` and `SetDataObject`");
    %property(DefaultAction, GetDefaultAction, SetDefaultAction, doc="See `GetDefaultAction` and `SetDefaultAction`");
};


%pythoncode { PyDropTarget = DropTarget }

//---------------------------------------------------------------------------

// A simple wxDropTarget derived class for text data: you only need to
// override OnDropText() to get something working


%{
class wxPyTextDropTarget : public wxTextDropTarget {
public:
    wxPyTextDropTarget() {}

    PYCALLBACK_3_EXTRACT_PURE(bool, rval = false, OnDropText, (int a, int b, const wxString &c))
    PYCALLBACK_0_VOID(wxTextDropTarget, OnLeave)
    PYCALLBACK_3_EXTRACT(wxTextDropTarget, wxDragResult, rval = (wxDragResult)0, OnEnter, 
                            (wxCoord a, wxCoord b, wxDragResult c))
    PYCALLBACK_3_EXTRACT(wxTextDropTarget, wxDragResult, rval = (wxDragResult)0, OnDragOver, 
                            (wxCoord a, wxCoord b, wxDragResult c))
    PYCALLBACK_3_EXTRACT(wxTextDropTarget, wxDragResult, rval = (wxDragResult)0, OnData, 
                            (wxCoord a, wxCoord b, wxDragResult c))
    PYCALLBACK_2_EXTRACT(wxTextDropTarget, bool, rval = false, OnDrop, (int a, int b)) 

    PYPRIVATE;
};

%}

%rename(TextDropTarget) wxPyTextDropTarget;
class wxPyTextDropTarget : public wxPyDropTarget {
public:
    %pythonAppend wxPyTextDropTarget   setCallbackInfo(TextDropTarget)

    wxPyTextDropTarget();
    void _setCallbackInfo(PyObject* self, PyObject* _class);

    bool OnDropText(wxCoord x, wxCoord y, const wxString& text);
    wxDragResult OnEnter(wxCoord x, wxCoord y, wxDragResult def);
    wxDragResult OnDragOver(wxCoord x, wxCoord y, wxDragResult def);
    void OnLeave();
    bool OnDrop(wxCoord x, wxCoord y);
    wxDragResult OnData(wxCoord x, wxCoord y, wxDragResult def);

    %MAKE_BASE_FUNC(TextDropTarget, OnDropText);
    %MAKE_BASE_FUNC(TextDropTarget, OnEnter);
    %MAKE_BASE_FUNC(TextDropTarget, OnDragOver);
    %MAKE_BASE_FUNC(TextDropTarget, OnLeave);
    %MAKE_BASE_FUNC(TextDropTarget, OnDrop);
    %MAKE_BASE_FUNC(TextDropTarget, OnData);    
};

//---------------------------------------------------------------------------

// A drop target which accepts files (dragged from File Manager or Explorer)


%{
class wxPyFileDropTarget : public wxFileDropTarget {
public:
    wxPyFileDropTarget() {}

    PYCALLBACK_3_EXTRACT_PURE(bool, rval = false, OnDropFiles, 
                            (wxCoord a, wxCoord b, const wxArrayString& c))
    PYCALLBACK_3_EXTRACT_PURE(bool, rval = false, OnDropText, 
                            (int a, int b, const wxString &c))
    PYCALLBACK_0_VOID(wxFileDropTarget, OnLeave)
    PYCALLBACK_3_EXTRACT(wxFileDropTarget, wxDragResult, rval = (wxDragResult)0, OnEnter, 
                            (wxCoord a, wxCoord b, wxDragResult c))
    PYCALLBACK_3_EXTRACT(wxFileDropTarget, wxDragResult, rval = (wxDragResult)0, OnDragOver, 
                            (wxCoord a, wxCoord b, wxDragResult c))
    PYCALLBACK_3_EXTRACT(wxFileDropTarget, wxDragResult, rval = (wxDragResult)0, OnData, 
                            (wxCoord a, wxCoord b, wxDragResult c))
    PYCALLBACK_2_EXTRACT(wxFileDropTarget, bool, rval = false, OnDrop, (int a, int b)) 

    PYPRIVATE;
};

%}


%rename(FileDropTarget) wxPyFileDropTarget;
class wxPyFileDropTarget : public wxPyDropTarget
{
public:
    %pythonAppend wxPyFileDropTarget   setCallbackInfo(FileDropTarget)

    wxPyFileDropTarget();
    void _setCallbackInfo(PyObject* self, PyObject* _class);

    bool OnDropFiles(wxCoord x, wxCoord y, const wxArrayString& filenames);
    wxDragResult OnEnter(wxCoord x, wxCoord y, wxDragResult def);
    wxDragResult OnDragOver(wxCoord x, wxCoord y, wxDragResult def);
    void OnLeave();
    bool OnDrop(wxCoord x, wxCoord y);
    wxDragResult OnData(wxCoord x, wxCoord y, wxDragResult def);
    
    %MAKE_BASE_FUNC(FileDropTarget, OnDropFiles);
    %MAKE_BASE_FUNC(FileDropTarget, OnEnter);
    %MAKE_BASE_FUNC(FileDropTarget, OnDragOver);
    %MAKE_BASE_FUNC(FileDropTarget, OnLeave);
    %MAKE_BASE_FUNC(FileDropTarget, OnDrop);
    %MAKE_BASE_FUNC(FileDropTarget, OnData);    
};


//---------------------------------------------------------------------------
%init %{
    wxPyPtrTypeMap_Add("wxDropSource",     "wxPyDropSource");
    wxPyPtrTypeMap_Add("wxDropTarget",     "wxPyDropTarget");
    wxPyPtrTypeMap_Add("wxTextDropTarget", "wxPyTextDropTarget");
    wxPyPtrTypeMap_Add("wxFileDropTarget", "wxPyFileDropTarget");
%}
//---------------------------------------------------------------------------

#endif
