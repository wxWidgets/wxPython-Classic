/////////////////////////////////////////////////////////////////////////////
// Name:        dataview.i
// Purpose:     Contains the wxDataViewCtrl and related classes
//
// Author:      Robin Dunn
//
// Created:     21-Jan-2008
// RCS-ID:      $Id: $
// Copyright:   (c) 2008 by Total Control Software
// Licence:     wxWindows license
/////////////////////////////////////////////////////////////////////////////

%define DOCSTRING
"The `DataViewCtrl` class can display data in either a tree-like
fashion, in a tabular form, or in a combination of the two.  It is a
native widget on the platforms that provide such a control, (currently
OS X and GTK) and generic elsewhere."
%enddef

%module(package="wx", docstring=DOCSTRING) dataview

%{
#include "wx/wxPython/wxPython.h"
#include "wx/wxPython/pyclasses.h"
#include "wx/wxPython/printfw.h"

#include <wx/dataview.h>

%}

//---------------------------------------------------------------------------

%import core.i
%pythoncode { wx = _core }
%pythoncode { __docfilter__ = wx.__DocFilter(globals()) }

MAKE_CONST_WXSTRING_NOSWIG(EmptyString);
MAKE_CONST_WXSTRING(DataViewCtrlNameStr);

enum {
    wxDVC_DEFAULT_WIDTH,
    wxDVC_TOGGLE_DEFAULT_WIDTH,
    wxDVC_DEFAULT_MINWIDTH,
    wxDVR_DEFAULT_ALIGNMENT
};

//---------------------------------------------------------------------------
// Macros, similar to what's in wxPython_int.h, to aid in the creation of
// virtual methods that are able to make callbacks to Python.


%{
#define PYCALLBACK_BOOL_DVIDVI_pure(PCLASS, CBNAME)                             \
    bool CBNAME(const wxDataViewItem &a, const wxDataViewItem &b) {             \
        bool rval = false;                                                      \
        bool found;                                                             \
        wxPyBlock_t blocked = wxPyBeginBlockThreads();                          \
        if ((found = wxPyCBH_findCallback(m_myInst, #CBNAME))) {                \
            PyObject* ao = wxPyConstructObject((void*)&a, wxT("wxDataViewItem"), 0); \
            PyObject* bo = wxPyConstructObject((void*)&b, wxT("wxDataViewItem"), 0); \
            rval = wxPyCBH_callCallback(m_myInst, Py_BuildValue("(OO)", ao, bo)); \
            Py_DECREF(ao);                                                      \
            Py_DECREF(bo);                                                      \
        }                                                                       \
        wxPyEndBlockThreads(blocked);                                           \
        return rval;                                                            \
    }


#define PYCALLBACK_BOOL_DVI_pure(PCLASS, CBNAME)                                \
    bool CBNAME(const wxDataViewItem &a) {                                      \
        bool rval = false;                                                      \
        bool found;                                                             \
        wxPyBlock_t blocked = wxPyBeginBlockThreads();                          \
        if ((found = wxPyCBH_findCallback(m_myInst, #CBNAME))) {                \
            PyObject* ao = wxPyConstructObject((void*)&a, wxT("wxDataViewItem"), 0); \
            rval = wxPyCBH_callCallback(m_myInst, Py_BuildValue("(O)", ao));    \
            Py_DECREF(ao);                                                      \
        }                                                                       \
        wxPyEndBlockThreads(blocked);                                           \
        return rval;                                                            \
    }


#define PYCALLBACK_BOOL_DVIDVIA(PCLASS, CBNAME)                                 \
    bool CBNAME(const wxDataViewItem &a, const wxDataViewItemArray &b) {        \
        bool rval = false;                                                      \
        bool found;                                                             \
        wxPyBlock_t blocked = wxPyBeginBlockThreads();                          \
        if ((found = wxPyCBH_findCallback(m_myInst, #CBNAME))) {                \
            PyObject* ao = wxPyConstructObject((void*)&a, wxT("wxDataViewItem"), 0); \
            PyObject* bo = wxPyConstructObject((void*)&b, wxT("wxDataViewItemArray"), 0); \
            rval = wxPyCBH_callCallback(m_myInst, Py_BuildValue("(OO)", ao, bo)); \
            Py_DECREF(ao);                                                      \
            Py_DECREF(bo);                                                      \
        }                                                                       \
        wxPyEndBlockThreads(blocked);                                           \
        if (! found)                                                            \
            rval = PCLASS::CBNAME(a, b);                                        \
        return rval;                                                            \
    }


#define PYCALLBACK_BOOL_DVIA(PCLASS, CBNAME)                                    \
    bool CBNAME(const wxDataViewItemArray &a) {                                 \
        bool rval = false;                                                      \
        bool found;                                                             \
        wxPyBlock_t blocked = wxPyBeginBlockThreads();                          \
        if ((found = wxPyCBH_findCallback(m_myInst, #CBNAME))) {                \
            PyObject* ao = wxPyConstructObject((void*)&a, wxT("wxDataViewItemArray"), 0); \
            rval = wxPyCBH_callCallback(m_myInst, Py_BuildValue("(O)", ao));    \
            Py_DECREF(ao);                                                      \
        }                                                                       \
        wxPyEndBlockThreads(blocked);                                           \
        if (! found)                                                            \
            rval = PCLASS::CBNAME(a);                                           \
        return rval;                                                            \
    }


#define PYCALLBACK_BOOL_DVIUINT_pure(PCLASS, CBNAME)                            \
    bool CBNAME(const wxDataViewItem &a, unsigned int b) {                      \
        bool rval = false;                                                      \
        bool found;                                                             \
        wxPyBlock_t blocked = wxPyBeginBlockThreads();                          \
        if ((found = wxPyCBH_findCallback(m_myInst, #CBNAME))) {                \
            PyObject* ao = wxPyConstructObject((void*)&a, wxT("wxDataViewItem"), 0); \
            rval = wxPyCBH_callCallback(m_myInst, Py_BuildValue("(Oi)", ao, b));\
            Py_DECREF(ao);                                                      \
        }                                                                       \
        wxPyEndBlockThreads(blocked);                                           \
        return rval;                                                            \
    }


#define PYCALLBACK_VOID__pure(PCLASS, CBNAME)                                   \
    void CBNAME() {                                                             \
        bool found;                                                             \
        wxPyBlock_t blocked = wxPyBeginBlockThreads();                          \
        if ((found = wxPyCBH_findCallback(m_myInst, #CBNAME)))                  \
            wxPyCBH_callCallback(m_myInst, Py_BuildValue("()"));                \
        wxPyEndBlockThreads(blocked);                                           \
    }


#define PYCALLBACK_BOOL__pure(PCLASS, CBNAME)                                   \
    bool CBNAME() {                                                             \
        bool found;                                                             \
        bool rval = false;                                                      \
        wxPyBlock_t blocked = wxPyBeginBlockThreads();                          \
        if ((found = wxPyCBH_findCallback(m_myInst, #CBNAME)))                  \
            rval = wxPyCBH_callCallback(m_myInst, Py_BuildValue("()"));         \
        wxPyEndBlockThreads(blocked);                                           \
        return rval;                                                            \
    }


%}




//---------------------------------------------------------------------------
// wxVariant stuff.  This should be moved someplace else...

%inline {
    wxVariant VariantTest(wxVariant& variant)
    {
        wxVariant other = variant;
        return other;
    }
}

//---------------------------------------------------------------------------
// wxDataViewItem

class wxDataViewItem
{
public:
    wxDataViewItem( void* id = NULL );
    ~wxDataViewItem();

    bool IsOk() const;
    void* GetID() const;
};

wxARRAY_WRAPPER(wxDataViewItemArray, wxDataViewItem);

//---------------------------------------------------------------------------
// wxDataViewModelNotifier
%newgroup

class wxDataViewModelNotifier {
public:
    //wxDataViewModelNotifier();    **** It's an ABC.
    virtual ~wxDataViewModelNotifier();

    virtual bool ItemAdded( const wxDataViewItem &parent, const wxDataViewItem &item );
    virtual bool ItemDeleted( const wxDataViewItem &parent, const wxDataViewItem &item );
    virtual bool ItemChanged( const wxDataViewItem &item );
    virtual bool ItemsAdded( const wxDataViewItem &parent, const wxDataViewItemArray &items );
    virtual bool ItemsDeleted( const wxDataViewItem &parent, const wxDataViewItemArray &items );
    virtual bool ItemsChanged( const wxDataViewItemArray &items );
    virtual bool ValueChanged( const wxDataViewItem &item, unsigned int col );
    virtual bool Cleared();
    virtual void Resort();

    void SetOwner( wxDataViewModel *owner );
    wxDataViewModel *GetOwner();
};



%{ // Derive from the class in C++ for virtualization
class wxPyDataViewModelNotifier : public wxDataViewModelNotifier {
public:
    wxPyDataViewModelNotifier() {}

    PYCALLBACK_BOOL_DVIDVI_pure(wxDataViewModelNotifier, ItemAdded)
    PYCALLBACK_BOOL_DVIDVI_pure(wxDataViewModelNotifier, ItemDeleted)
    PYCALLBACK_BOOL_DVI_pure(wxDataViewModelNotifier, ItemChanged)

    PYCALLBACK_BOOL_DVIDVIA(wxDataViewModelNotifier, ItemsAdded)
    PYCALLBACK_BOOL_DVIDVIA(wxDataViewModelNotifier, ItemsDeleted)
    PYCALLBACK_BOOL_DVIA(wxDataViewModelNotifier, ItemsChanged)

    PYCALLBACK_BOOL_DVIUINT_pure(wxDataViewModelNotifier, ValueChanged)
    PYCALLBACK_BOOL__pure(wxDataViewModelNotifier, Cleared)
    PYCALLBACK_VOID__pure(wxDataViewModelNotifier, Resort)

    PYPRIVATE;
};
%}


class wxPyDataViewModelNotifier : public wxDataViewModelNotifier {
public:
    %pythonAppend wxPyDataViewModelNotifier  "self._setOORInfo(self);"  setCallbackInfo(PyDataViewModelNotifier);

    wxPyDataViewModelNotifier();
    void _setCallbackInfo(PyObject* self, PyObject* _class);
};

//---------------------------------------------------------------------------
// wxDataViewItemAttr: a structure containing the visual attributes of an item

class wxDataViewItemAttr
{
public:
    wxDataViewItemAttr();
    ~wxDataViewItemAttr();

    void SetColour(const wxColour& colour);
    void SetBold( bool set );
    void SetItalic( bool set );

    bool HasColour() const;
    const wxColour& GetColour() const;

    bool GetBold() const;
    bool GetItalic() const;
};

//---------------------------------------------------------------------------
// wxDataViewModel


// First, the base class...
class wxDataViewModel: public wxObjectRefData
{
public:
    // wxDataViewModel();     ****  It's an ABC

    virtual unsigned int GetColumnCount() const;

    // return type as reported by wxVariant
    virtual wxString GetColumnType( unsigned int col ) const;

// TODO: ****  Change semantics such that the value is the return value    
    // get value into a wxVariant
    virtual void GetValue( wxVariant &variant,
                           const wxDataViewItem &item, unsigned int col ) const;

    // set value, call ValueChanged() afterwards!
    virtual bool SetValue( const wxVariant &variant,
                           const wxDataViewItem &item, unsigned int col );

// TODO: ****  Change semantics such that the attribute is the return value    
    // Get text attribute, return false if default attributes should be used
    virtual bool GetAttr( const wxDataViewItem &item, unsigned int col,
                          wxDataViewItemAttr &attr );

    // define hierachy
    virtual wxDataViewItem GetParent( const wxDataViewItem &item ) const;
    virtual bool IsContainer( const wxDataViewItem &item ) const;

    // Is the container just a header or an item with all columns
    virtual bool HasContainerColumns(const wxDataViewItem& item) const;
    virtual unsigned int GetChildren( const wxDataViewItem &item,
                                      wxDataViewItemArray &children ) const;

    // define DnD capabilities
    virtual bool IsDraggable( const wxDataViewItem &item );

// TODO: **** Is the format supposed to be a return value? If so
//            perhaps it should be split into two methods...
    virtual size_t GetDragDataSize( const wxDataViewItem &item,
                                    const wxDataFormat &format );

// TODO: **** Data should be the return value.  How is format used here?    
    virtual bool GetDragData( const wxDataViewItem &item,
                              const wxDataFormat &format, 
                              void* data, size_t size );

    // delegated notifiers
    virtual bool ItemAdded( const wxDataViewItem &parent, const wxDataViewItem &item );
    virtual bool ItemsAdded( const wxDataViewItem &parent, const wxDataViewItemArray &items );
    virtual bool ItemDeleted( const wxDataViewItem &parent, const wxDataViewItem &item );
    virtual bool ItemsDeleted( const wxDataViewItem &parent, const wxDataViewItemArray &items );
    virtual bool ItemChanged( const wxDataViewItem &item );
    virtual bool ItemsChanged( const wxDataViewItemArray &items );
    virtual bool ValueChanged( const wxDataViewItem &item, unsigned int col );
    virtual bool Cleared();

    // delegatd action
    virtual void Resort();

    void AddNotifier( wxDataViewModelNotifier *notifier );
    void RemoveNotifier( wxDataViewModelNotifier *notifier );

    // default compare function
    virtual int Compare( const wxDataViewItem &item1, const wxDataViewItem &item2,
                         unsigned int column, bool ascending );
    virtual bool HasDefaultCompare() const;
    
    // internal
    virtual bool IsIndexListModel() const;
};


//---------------------------------------------------------------------------
//---------------------------------------------------------------------------

%init %{
%}

//---------------------------------------------------------------------------
