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
        else {                                                                  \
            PyErr_SetString(PyExc_NotImplementedError,                          \
              "The " #CBNAME " method should be implemented in derived class"); \
        }                                                                       \
        wxPyEndBlockThreads(blocked);                                           \
        return rval;                                                            \
    }


#define PYCALLBACK_BOOL_DVI(PCLASS, CBNAME)                                     \
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
        if (! found)                                                            \
            rval = PCLASS::CBNAME(a);                                           \
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
        else {                                                                  \
            PyErr_SetString(PyExc_NotImplementedError,                          \
              "The " #CBNAME " method should be implemented in derived class"); \
        }                                                                       \
        wxPyEndBlockThreads(blocked);                                           \
        return rval;                                                            \
    }


#define PYCALLBACK_BOOL_DVI_pure_const(PCLASS, CBNAME)                          \
    bool CBNAME(const wxDataViewItem &a) const {                                \
        bool rval = false;                                                      \
        bool found;                                                             \
        wxPyBlock_t blocked = wxPyBeginBlockThreads();                          \
        if ((found = wxPyCBH_findCallback(m_myInst, #CBNAME))) {                \
            PyObject* ao = wxPyConstructObject((void*)&a, wxT("wxDataViewItem"), 0); \
            rval = wxPyCBH_callCallback(m_myInst, Py_BuildValue("(O)", ao));    \
            Py_DECREF(ao);                                                      \
        }                                                                       \
        else {                                                                  \
            PyErr_SetString(PyExc_NotImplementedError,                          \
              "The " #CBNAME " method should be implemented in derived class"); \
        }                                                                       \
        wxPyEndBlockThreads(blocked);                                           \
        return rval;                                                            \
    }


#define PYCALLBACK_BOOL_DVI_const(PCLASS, CBNAME)                               \
    bool CBNAME(const wxDataViewItem &a) const {                                \
        bool rval = false;                                                      \
        bool found;                                                             \
        wxPyBlock_t blocked = wxPyBeginBlockThreads();                          \
        if ((found = wxPyCBH_findCallback(m_myInst, #CBNAME))) {                \
            PyObject* ao = wxPyConstructObject((void*)&a, wxT("wxDataViewItem"), 0); \
            rval = wxPyCBH_callCallback(m_myInst, Py_BuildValue("(O)", ao));    \
            Py_DECREF(ao);                                                      \
        }                                                                       \
        wxPyEndBlockThreads(blocked);                                           \
        if (! found)                                                            \
            rval = PCLASS::CBNAME(a);                                           \
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


#define PYCALLBACK_UINT_DVIDVIA_pure_const(PCLASS, CBNAME)                      \
    unsigned int CBNAME(const wxDataViewItem &a, wxDataViewItemArray &b) const { \
        unsigned int rval;                                                      \
        bool found;                                                             \
        wxPyBlock_t blocked = wxPyBeginBlockThreads();                          \
        if ((found = wxPyCBH_findCallback(m_myInst, #CBNAME))) {                \
            PyObject* ao = wxPyConstructObject((void*)&a, wxT("wxDataViewItem"), 0); \
            PyObject* bo = wxPyConstructObject((void*)&b, wxT("wxDataViewItemArray"), 0); \
            rval = wxPyCBH_callCallback(m_myInst, Py_BuildValue("(OO)", ao, bo)); \
            Py_DECREF(ao);                                                      \
            Py_DECREF(bo);                                                      \
        }                                                                       \
        else {                                                                  \
            PyErr_SetString(PyExc_NotImplementedError,                          \
              "The " #CBNAME " method should be implemented in derived class"); \
        }                                                                       \
        wxPyEndBlockThreads(blocked);                                           \
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
        else {                                                                  \
            PyErr_SetString(PyExc_NotImplementedError,                          \
              "The " #CBNAME " method should be implemented in derived class"); \
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
        else {                                                                  \
            PyErr_SetString(PyExc_NotImplementedError,                          \
              "The " #CBNAME " method should be implemented in derived class"); \
        }                                                                       \
        wxPyEndBlockThreads(blocked);                                           \
    }


#define PYCALLBACK_BOOL__pure(PCLASS, CBNAME)                                   \
    bool CBNAME() {                                                             \
        bool found;                                                             \
        bool rval = false;                                                      \
        wxPyBlock_t blocked = wxPyBeginBlockThreads();                          \
        if ((found = wxPyCBH_findCallback(m_myInst, #CBNAME)))                  \
            rval = wxPyCBH_callCallback(m_myInst, Py_BuildValue("()"));         \
        else {                                                                  \
            PyErr_SetString(PyExc_NotImplementedError,                          \
              "The " #CBNAME " method should be implemented in derived class"); \
        }                                                                       \
        wxPyEndBlockThreads(blocked);                                           \
        return rval;                                                            \
    }


#define PYCALLBACK_BOOL__pure(PCLASS, CBNAME)                                   \
    bool CBNAME() {                                                             \
        bool found;                                                             \
        bool rval = false;                                                      \
        wxPyBlock_t blocked = wxPyBeginBlockThreads();                          \
        if ((found = wxPyCBH_findCallback(m_myInst, #CBNAME)))                  \
            rval = wxPyCBH_callCallback(m_myInst, Py_BuildValue("()"));         \
        else {                                                                  \
            PyErr_SetString(PyExc_NotImplementedError,                          \
              "The " #CBNAME " method should be implemented in derived class"); \
        }                                                                       \
        wxPyEndBlockThreads(blocked);                                           \
        return rval;                                                            \
    }


#define PYCALLBACK_BOOL__const(PCLASS, CBNAME)                                  \
    bool CBNAME() const {                                                       \
        bool found;                                                             \
        bool rval = false;                                                      \
        wxPyBlock_t blocked = wxPyBeginBlockThreads();                          \
        if ((found = wxPyCBH_findCallback(m_myInst, #CBNAME)))                  \
            rval = wxPyCBH_callCallback(m_myInst, Py_BuildValue("()"));         \
        wxPyEndBlockThreads(blocked);                                           \
        if (! found)                                                            \
            rval = PCLASS::CBNAME();                                            \
        return rval;                                                            \
    }

    
#define PYCALLBACK_UINT__pure_const(PCLASS, CBNAME)                             \
    unsigned int CBNAME() const {                                               \
        bool found;                                                             \
        unsigned int rval;                                                      \
        wxPyBlock_t blocked = wxPyBeginBlockThreads();                          \
        if ((found = wxPyCBH_findCallback(m_myInst, #CBNAME)))                  \
            rval = wxPyCBH_callCallback(m_myInst, Py_BuildValue("()"));         \
        else {                                                                  \
            PyErr_SetString(PyExc_NotImplementedError,                          \
              "The " #CBNAME " method should be implemented in derived class"); \
        }                                                                       \
        wxPyEndBlockThreads(blocked);                                           \
        return rval;                                                            \
    }


#define PYCALLBACK_STRING_UINT_pure_const(PCLASS, CBNAME)                       \
    wxString CBNAME(unsigned int a) const {                                     \
        wxString rval;                                                          \
        bool found;                                                             \
        wxPyBlock_t blocked = wxPyBeginBlockThreads();                          \
        if ((found = wxPyCBH_findCallback(m_myInst, #CBNAME))) {                \
            PyObject* ro;                                                       \
            ro = wxPyCBH_callCallbackObj(m_myInst, Py_BuildValue("(i)", a));    \
            if (ro) {                                                           \
                rval = Py2wxString(ro);                                         \
                Py_DECREF(ro);                                                  \
            }                                                                   \
        }                                                                       \
        else {                                                                  \
            PyErr_SetString(PyExc_NotImplementedError,                          \
              "The " #CBNAME " method should be implemented in derived class"); \
        }                                                                       \
        wxPyEndBlockThreads(blocked);                                           \
        return rval;                                                            \
    }                                                                           \

    
#define PYCALLBACK_DVI_DVI_pure_const(PCLASS, CBNAME)                           \
    wxDataViewItem CBNAME(const wxDataViewItem &a) const {                      \
        wxDataViewItem rval;                                                    \
        bool found;                                                             \
        wxPyBlock_t blocked = wxPyBeginBlockThreads();                          \
        if ((found = wxPyCBH_findCallback(m_myInst, #CBNAME))) {                \
            PyObject* ro;                                                       \
            wxDataViewItem* ptr;                                                \
            PyObject* ao = wxPyConstructObject((void*)&a, wxT("wxDataViewItem"), 0); \
            ro = wxPyCBH_callCallbackObj(m_myInst, Py_BuildValue("(O)", ao));   \
            Py_DECREF(ao);                                                      \
            if (ro) {                                                           \
                if (wxPyConvertSwigPtr(ro, (void**)&ptr, wxT("wxDataViewItem")))  \
                    rval = *ptr;                                                \
                Py_DECREF(ro);                                                  \
            }                                                                   \
        }                                                                       \
        else {                                                                  \
            PyErr_SetString(PyExc_NotImplementedError,                          \
              "The " #CBNAME " method should be implemented in derived class"); \
        }                                                                       \
        wxPyEndBlockThreads(blocked);                                           \
        return rval;                                                            \
    }


#define PYCALLBACK_INT_DVIDVIINTBOOL(PCLASS, CBNAME)                            \
    int CBNAME(const wxDataViewItem &a, const wxDataViewItem &b,                \
               unsigned int c, bool d ) {                                       \
        int rval;                                                               \
        bool found;                                                             \
        wxPyBlock_t blocked = wxPyBeginBlockThreads();                          \
        if ((found = wxPyCBH_findCallback(m_myInst, #CBNAME))) {                \
            PyObject* ro;                                                       \
            wxDataViewItem* ptr;                                                \
            PyObject* ao = wxPyConstructObject((void*)&a, wxT("wxDataViewItem"), 0); \
            PyObject* bo = wxPyConstructObject((void*)&b, wxT("wxDataViewItem"), 0); \
            rval = wxPyCBH_callCallback(m_myInst, Py_BuildValue("(OOii)", ao, bo, c, d)); \
            Py_DECREF(ao);                                                      \
            Py_DECREF(bo);                                                      \
        }                                                                       \
        wxPyEndBlockThreads(blocked);                                           \
        if (! found)                                                            \
            rval = PCLASS::CBNAME(a, b, c, d);                                  \
        return rval;                                                            \
    }


%}




//---------------------------------------------------------------------------
// wxDataViewItem
%newgroup

DocStr(wxDataViewItem,
"wxDataViewItem is a small opaque class that represents an item in a
`DataViewCtrl` in a persistent way, i.e. indepent of the position of
the item in the control or changes to its contents.  It contains a C
void pointer which is used as the internal ID value for the item.  If
the ID is NULL then the DataViewItem is considered invalid and the
`IsOk` method will return False, which is used in many places in the
API to indicate that no item was found.", "");

class wxDataViewItem
{
public:
    wxDataViewItem( void* id = NULL );
    ~wxDataViewItem();

    DocDeclStr(
        bool , IsOk() const,
        "Returns ``True`` if the object refers to an actual item in the data
view control.", "");
    
    DocDeclStr(
        void* , GetID() const,
        "Get the opaque value of the ID object.", "");

    %extend {
        // methods to allow items to be dictionary keys
        long __hash__()
        {
            return (long)self->GetID();
        }

        int __cmp__(wxDataViewItem* other)
        {
            if ( self->GetID() < other->GetID() ) return -1;
            if ( self->GetID() > other->GetID() ) return  1;
            return 0;
        }
    }
};

wxARRAY_WRAPPER(wxDataViewItemArray, wxDataViewItem);

//---------------------------------------------------------------------------
// wxDataViewModelNotifier
%newgroup

DocStr(wxDataViewModelNotifier,
"This class allows multiple entities to be notified when a change
happens in a `DataViewModel` instance, and it mirrors the notification
interface in that class.  To add your own notifier object to a model,
derive a new class from `PyDataViewModelNotifier`, override the
methods you are interested in, and assign an instance of it to the
model with `DataViewModel.AddNotifier`.", "");

class wxDataViewModelNotifier {
public:
    //wxDataViewModelNotifier();    **** It's an ABC.
    virtual ~wxDataViewModelNotifier();

    DocDeclStr(
        virtual bool , ItemAdded( const wxDataViewItem &parent, const wxDataViewItem &item ),
        "Override this to be informed that an item has been added to the data
model.", "");
    
    DocDeclStr(
        virtual bool , ItemDeleted( const wxDataViewItem &parent, const wxDataViewItem &item ),
        "Override this to be informed that an item has been deleted.", "");
    
    DocDeclStr(
        virtual bool , ItemChanged( const wxDataViewItem &item ),
        "Override this to be informed that an item's value has changed.", "");
    
    DocDeclStr(
        virtual bool , ItemsAdded( const wxDataViewItem &parent, const wxDataViewItemArray &items ),
        "Override this to be informed that several items have been added to the model.", "");
    
    DocDeclStr(
        virtual bool , ItemsDeleted( const wxDataViewItem &parent, const wxDataViewItemArray &items ),
        "Override this to be informed that several items have been deleted.", "");
    
    DocDeclStr(
        virtual bool , ItemsChanged( const wxDataViewItemArray &items ),
        "Override this to be informed that several items have been changed.", "");
    
    DocDeclStr(
        virtual bool , ValueChanged( const wxDataViewItem &item, unsigned int col ),
        "Override this to be informed that a value has changed in the model.
This differs from `ItemChanged` in that this method is sensitive to
changes in sub-elements of an item, not just the whole item (row).", "");
    
    DocDeclStr(
        virtual bool , Cleared(),
        "Override this to be informed that all data has been cleared.  The
control will read the visible data items from the model again.", "");
    
    DocDeclStr(
        virtual void , Resort(),
        "Override this to be informed that a resort has been initiated after
the sort function has been changed.", "");
    

    DocDeclStr(
        void , SetOwner( wxDataViewModel *owner ),
        "Sets the owner (the model) of this notifier.  Used internally.", "");
    
    DocDeclStr(
        wxDataViewModel *, GetOwner(),
        "Returns the owner (the model) of this notifier.", "");
    

    %property(Owner, GetOwner, SetOwner);
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



DocStr(wxPyDataViewModelNotifier,
"This class is a version of `DataViewModelNotifier` that has been
engineered to know how to reflect the C++ virtual method calls to
Python methods in the derived class.  Use this class as your base
class instead of `DataViewModelNotifier`.", "");

class wxPyDataViewModelNotifier : public wxDataViewModelNotifier {
public:
    %pythonAppend wxPyDataViewModelNotifier  "self._setOORInfo(self);"  setCallbackInfo(PyDataViewModelNotifier);
    wxPyDataViewModelNotifier();
    void _setCallbackInfo(PyObject* self, PyObject* _class);
};

//---------------------------------------------------------------------------
// wxDataViewItemAttr: a structure containing the visual attributes of an item
%newgroup

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
%newgroup


// First, the base class...

DocStr(wxDataViewModel,
"`DataViewModel` is the base class for managing all data to be
displayed by a `DataViewCtrl`. All other models derive from it and
must implement several of its methods in order to define a complete
data model. In detail, you need to override `IsContainer`,
`GetParent`, `GetChildren`, `GetColumnCount`, `GetColumnType` and
`GetValue` in order to define the data model which acts as an
interface between your actual data and the `DataViewCtrl`. Since you
will usually also allow the `DataViewCtrl` to change your data through
its graphical interface, you will also have to override `SetValue`
which the `DataViewCtrl` will call when a change to some data has been
commited.  To implement a custom data model derive a new class from
`PyDataViewModel` and implement the required methods.

The data that is presented through this data model is expected to
change at run-time. You need to inform the data model when a change
happened. Depending on what happened you need to call one of the
following methods: `ValueChanged`, `ItemAdded`, `ItemDeleted`,
`ItemChanged`, `Cleared`. There are plural forms for notification of
addition, change or removal of several item at once. See `ItemsAdded`,
`ItemsDeleted`, `ItemsChanged`.

Note that ``DataViewModel`` does not define the position or index of
any item in the control because different controls might display the
same data differently. ``DataViewModel`` does provide a `Compare`
method which the `DataViewCtrl` may use to sort the data either in
conjunction with a column header or without (see `HasDefaultCompare`).

This class maintains a list of `DataViewModelNotifier` objects which
link this class to the specific implementations on the supported
platforms so that e.g. calling `ValueChanged` on this model will just
call `DataViewModelNotifier.ValueChanged` for each notifier that has
been added. You can also add your own notifier in order to get
informed about any changes to the data in the list model.

Currently wxWidgets provides the following models in addition to this
base class: `DataViewIndexListModel`, `DataViewTreeStore`.  To create
your own model from Python you will need to use the `PyDataViewModel`
as your base class.

:note: The C++ DataView classes use the wxVariant class to pass around
    dynamically typed data values.  In wxPython we have typemaps that
    will convert variants to Python objects of appropriate types, and
    if the type of object is not one that wxVariant will understand
    then the raw PyObject is passed through, with appropriate
    ref-counting.  The wxVariant type names and the Python types they
    are converted to or from are listed in this table:

    ============= =======================
    'bool'        Boolean
    'long'        Integer
    'double'      Float
    'string'      String or Unicode
    'PyObject'    any other Python type
    ============= =======================
", "");

class wxDataViewModel: public wxObjectRefData
{
public:
    // wxDataViewModel();     ****  It's an ABC

    DocDeclStr(
        virtual unsigned int , GetColumnCount() const,
        "Override this to indicate the number of columns in the model.", "");
    

    // return type as reported by wxVariant
    DocDeclStr(
        virtual wxString , GetColumnType( unsigned int col ) const,
        "Override this to indicate what type of data is stored in the column
specified by col. This should return a string indicating the type name of
data type, as used by wxVariant.", "");
    

    %extend {
    //  ****  Changed semantics such that the value is the return value    
    //virtual void GetValue( wxVariant &variant,
    //                       const wxDataViewItem &item, unsigned int col ) const;
        DocDeclStr(
            virtual wxVariant , GetValue(const wxDataViewItem &item,
                                         unsigned int col ) const,
            "Override this and return the value to be used for the item, in the
given column.  The type of the return value should match that given by
`GetColumnType`.", "")
        {
            wxVariant var;
            self->GetValue(var, item, col);
            return var;
        }
    }
        
    
    DocDeclStr(
        virtual bool , SetValue( const wxVariant &variant,
                                 const wxDataViewItem &item, unsigned int col ),
        "This gets called in order to set a value in the data model.  The most
common scenario is that the `DataViewCtrl` calls this method after the
user has changed some data in the view.  The model should then update
whatever it is using for storing the data values and then call
`ValueChanged` so proper notifications are performed.", "");
    

    DocDeclStr(
        virtual bool , GetAttr( const wxDataViewItem &item, unsigned int col,
                                wxDataViewItemAttr &attr ),
        "Override this to indicate that the item has special font
attributes. This only affects the `DataViewTextRendererText` renderer.
Return ``False`` if the default attributes should be used.", "");
    

    DocDeclStr(
        virtual wxDataViewItem , GetParent( const wxDataViewItem &item ) const,
        "Override this to indicate which item is the parent of the given item.
If the item is a child of the (hidden) root, then simply return an
invalid item, (one constructed with no ID.)", "");

    
    DocDeclStr(
        virtual bool , IsContainer( const wxDataViewItem &item ) const,
        "Override this to indicate whether an item is a container, in other
words, if it is a parent item that can have children.", "");
    

    DocDeclStr(
        virtual bool , HasContainerColumns(const wxDataViewItem& item) const,
        "Override this method to indicate if a container item merely acts as a
headline (such as for categorisation) or if it also acts a normal item with
entries for the other columns. The default implementation returns ``False``.", "");

    
    DocDeclStr(
        virtual unsigned int , GetChildren( const wxDataViewItem &item,
                                            wxDataViewItemArray &children ) const,
        "Override this so the control can find the children of a container
item.  The children array should be filled with the child items of the
given item, and the number of children should be returned.", "");
    

//     TODO:  define DnD capabilities
//     virtual bool IsDraggable( const wxDataViewItem &item );

// // TODO: **** Is the format supposed to be a return value? If so
// //            perhaps it should be split into two methods...
//     virtual size_t GetDragDataSize( const wxDataViewItem &item,
//                                     const wxDataFormat &format );

// // TODO: **** Data should be the return value.  How is format used here?    
//     virtual bool GetDragData( const wxDataViewItem &item,
//                               const wxDataFormat &format, 
//                               void* data, size_t size );

    DocDeclStr(
        virtual bool , ItemAdded( const wxDataViewItem &parent, const wxDataViewItem &item ),
        "Call this to inform the registered notifiers that an item has been
added to the model.", "");
    
    DocDeclStr(
        virtual bool , ItemsAdded( const wxDataViewItem &parent, const wxDataViewItemArray &items ),
        "Call this to inform the registered notifiers that multiple items have
been added to the data model.", "");
    
    DocDeclStr(
        virtual bool , ItemDeleted( const wxDataViewItem &parent, const wxDataViewItem &item ),
        "Call this to inform the registered notifiers that an item has been
deleted from the model.", "");
    
    DocDeclStr(
        virtual bool , ItemsDeleted( const wxDataViewItem &parent, const wxDataViewItemArray &items ),
        "Call this to inform the registered notifiers that multiple items have
been deleted from the data model.", "");
    
    DocDeclStr(
        virtual bool , ItemChanged( const wxDataViewItem &item ),
        "Call this to inform the registered notifiers that an item has changed.
This will eventually result in a EVT_DATAVIEW_ITEM_VALUE_CHANGED
event, in which the column field will not be set.", "");
    
    DocDeclStr(
        virtual bool , ItemsChanged( const wxDataViewItemArray &items ),
        "Call this to inform the registered notifiers that multiple items have
changed.  This will eventually result in EVT_DATAVIEW_ITEM_VALUE_CHANGED
events, in which the column field will not be set.", "");
    
    DocDeclStr(
        virtual bool , ValueChanged( const wxDataViewItem &item, unsigned int col ),
        "Call this to inform the registered notifiers that a value in the model
has been changed.  This will eventually result in a EVT_DATAVIEW_ITEM_VALUE_CHANGED
event.", "");
    
    DocDeclStr(
        virtual bool , Cleared(),
        "Call this to inform the registered notifiers that all data has been
cleared.  The contorl will then reread the data from the model again.", "");
    
    DocDeclStr(
        virtual void , Resort(),
        "Call this to initiate a resort after the sort function has been changed.", "");
    

    %disownarg( wxDataViewModelNotifier *notifier );
    void AddNotifier( wxDataViewModelNotifier *notifier );
    %cleardisown( wxDataViewModelNotifier *notifier );

    %pythonAppend RemoveNotifier "args[1].thisown = 1";
    void RemoveNotifier( wxDataViewModelNotifier *notifier );

    
    DocDeclStr(
        virtual int , Compare( const wxDataViewItem &item1, const wxDataViewItem &item2,
                               unsigned int column, bool ascending ),
        "The compare function to be used by the control. The default compare
function sorts by container and other items separately and in
ascending order. Override this for a different sorting behaviour.", "");
    
    DocDeclStr(
        virtual bool , HasDefaultCompare() const,
        "Override this to indicate that the model provides a default compare
function that the control should use if no column has been chosen for
sorting. Usually, the user clicks on a column header for sorting and
the data will be sorted alphanumerically. If any other order (e.g. by
index or order of appearance) is required, then this should be used.", "");
    
    
    // internal
    virtual bool IsIndexListModel() const;
};



%{
// Create a C++ class for the Py version

class wxPyDataViewModel: public wxDataViewModel
{
public:
    wxPyDataViewModel() {}

    PYCALLBACK_UINT__pure_const(wxDataViewModel, GetColumnCount);
    PYCALLBACK_STRING_UINT_pure_const(wxDataViewModel, GetColumnType);

    PYCALLBACK_DVI_DVI_pure_const(wxDataViewModel, GetParent);
    PYCALLBACK_BOOL_DVI_pure_const(wxDataViewModel, IsContainer);
    PYCALLBACK_BOOL_DVI_const(wxDataViewModel, HasContainerColumns);
    PYCALLBACK_UINT_DVIDVIA_pure_const(wxDataViewModel, GetChildren);

    PYCALLBACK_BOOL_DVI(wxDataViewModel, IsDraggable);
    // GetDragDataSize
    // GetDragData

    PYCALLBACK_INT_DVIDVIINTBOOL(wxDataViewModel, Compare);
    PYCALLBACK_BOOL__const(wxDataViewModel, HasDefaultCompare);


    void GetValue( wxVariant &variant,
                   const wxDataViewItem &item, unsigned int col ) const
    {
        // The wxPython version of this method returns the variant as
        // a return value instead of modifying the parameter.
        bool found;
        wxPyBlock_t blocked = wxPyBeginBlockThreads();
        if ((found = wxPyCBH_findCallback(m_myInst, "GetValue"))) {
            PyObject* ro;
            PyObject* io = wxPyConstructObject((void*)&item, wxT("wxDataViewItem"), 0);
            ro = wxPyCBH_callCallbackObj(m_myInst, Py_BuildValue("(Oi)", io, col));
            Py_DECREF(io);
            if (ro) {
                variant = wxVariant_in_helper(ro);
                Py_DECREF(ro);
            }
        }
        else {                                                                  
            PyErr_SetString(PyExc_NotImplementedError,                          
              "The GetValue method should be implemented in derived class"); 
        }                                                                       
        wxPyEndBlockThreads(blocked);                                                   
    }

    
    bool SetValue( const wxVariant &variant,
                   const wxDataViewItem &item, unsigned int col )
    {
        bool rval = false;
        bool found;
        wxPyBlock_t blocked = wxPyBeginBlockThreads();
        if ((found = wxPyCBH_findCallback(m_myInst, "GetValue"))) {
            PyObject* vo = wxVariant_out_helper(variant);
            PyObject* io = wxPyConstructObject((void*)&item, wxT("wxDataViewItem"), 0);
            rval = wxPyCBH_callCallback(m_myInst, Py_BuildValue("(OOi)", vo, io, col));
            Py_DECREF(vo);
            Py_DECREF(io);
        }
        else {                                                                  
            PyErr_SetString(PyExc_NotImplementedError,                          
              "The SetValue method should be implemented in derived class"); 
        }                                                                       
        wxPyEndBlockThreads(blocked);
        return rval;
    }

    bool GetAttr( const wxDataViewItem &item, unsigned int col, wxDataViewItemAttr &attr )
    {
        bool rval = false;
        bool found;
        wxPyBlock_t blocked = wxPyBeginBlockThreads();
        if ((found = wxPyCBH_findCallback(m_myInst, "GetAttr"))) {
            PyObject* io = wxPyConstructObject((void*)&item, wxT("wxDataViewItem"), 0);
            PyObject* ao = wxPyConstructObject((void*)&attr, wxT("wxDataViewItemAttr"), 0);
            rval = wxPyCBH_callCallback(m_myInst, Py_BuildValue("(OiO)", io, col, ao));
            Py_DECREF(io);
            Py_DECREF(ao);
        }
        else {                                                                  
            PyErr_SetString(PyExc_NotImplementedError,                          
              "The SetValue method should be implemented in derived class"); 
        }                                                                       
        wxPyEndBlockThreads(blocked);
        return rval;
    }    
    
    PYPRIVATE;
};

%}


// tell SWIG about the Py class  (TODO)

DocStr(wxPyDataViewModel,
"This class is a version of `DataViewModel` that has been
engineered to know how to reflect the C++ virtual method calls to
Python methods in the derived class.  Use this class as your base
class instead of `DataViewModel`.", "");

class wxPyDataViewModel: public wxDataViewModel
{
public:
    %pythonAppend wxPyDataViewModel  "self._setOORInfo(self);"  setCallbackInfo(PyDataViewModel);
    wxPyDataViewModel();
    void _setCallbackInfo(PyObject* self, PyObject* _class);
};


//---------------------------------------------------------------------------
%newgroup



DocStr(wxDataViewIndexListModel,
"DataViewIndexListModel is a specialized data model which lets you
address an item by its position (row) rather than its `DataViewItem`
(which you can obtain from this class). This model also provides its
own `Compare` method which sorts the model's data by the index.

This model is special in that it is implemented differently under OS X
and other platforms. Under OS X a DataViewItem is always persistent
and this is also the case for this class. Under other platforms, the
meaning of a DataViewItem is changed to reflect a row number for
DataViewIndexListModel. The consequence of this is that
DataViewIndexListModel can be used as a virtual model with an almost
infinate number of items on platforms other than OS X.", "");
    
class wxDataViewIndexListModel: public wxDataViewModel
{
public:
    // wxDataViewIndexListModel( unsigned int initial_size = 0 );   **** ABC
    ~wxDataViewIndexListModel();


    %extend {
    //  ****  Changed semantics such that the data value is the return value    
    //virtual void GetValue( wxVariant &variant,
    //                       unsigned int row, unsigned int col ) const;
        DocDeclStr(
            virtual wxVariant , GetValue( unsigned int row, unsigned int col ) const,
            "Override this method to return the data value to be used for the item
at the given row and column.", "")
        {
            wxVariant var;
            self->GetValue(var, row, col);
            return var;
        }
    }

    DocDeclStr(
        virtual bool , SetValue( const wxVariant &variant,
                                 unsigned int row, unsigned int col ),
        "This is called in order to set a value in the data model.", "");
    

    DocDeclStr(
        virtual bool , GetAttr( unsigned int row, unsigned int col,
                                wxDataViewItemAttr &attr ),
        "Override this to indicate that the item has special font
attributes. This only affects the `DataViewTextRendererText` renderer.
Return ``False`` if the default attributes should be used.", "");
    

    DocDeclStr(
        void , RowPrepended(),
        "Call this after a row has been prepended to the model.", "");
    
    DocDeclStr(
        void , RowInserted( unsigned int before ),
        "Call this after a row has been inserted at the given position", "");
    
    DocDeclStr(
        void , RowAppended(),
        "Call this after a row has been appended to the model.", "");
    
    DocDeclStr(
        void , RowDeleted( unsigned int row ),
        "Call this after a row has been deleted.", "");
    
    DocDeclStr(
        void , RowsDeleted( const wxArrayInt &rows ),
        "Call this after rows have been deleted. The array will internally get
copied and sorted in descending order so that the rows with the
highest position will be deleted first.", "");
    
    DocDeclStr(
        void , RowChanged( unsigned int row ),
        "Call this after a row has been changed.", "");
    
    DocDeclStr(
        void , RowValueChanged( unsigned int row, unsigned int col ),
        "Call this after a value has been changed.", "");
    
    DocDeclStr(
        void , Reset( unsigned int new_size ),
        "Call this if the data has to be read again from the model. This is
useful after major changes when calling methods like `RowChanged` or
`RowDeleted` (possibly thousands of times) doesn't make sense.", "");
    


    DocDeclStr(
        unsigned int , GetRow( const wxDataViewItem &item ) const,
        "Returns the row position of item.", "");
    
    DocDeclStr(
        wxDataViewItem , GetItem( unsigned int row ) const,
        "Returns the DataViewItem for the item at row.", "");
    

    // internal
    virtual bool IsIndexListModel() const;
    unsigned int GetLastIndex() const;
};



// Create a C++ class for the Py version  (TODO)


// tell SWIG about the Py class  (TODO)




//---------------------------------------------------------------------------
//---------------------------------------------------------------------------
//---------------------------------------------------------------------------


%init %{
%}

//---------------------------------------------------------------------------
