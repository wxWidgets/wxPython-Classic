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
    wxDVC_DEFAULT_RENDERER_SIZE,
    wxDVC_DEFAULT_WIDTH,
    wxDVC_TOGGLE_DEFAULT_WIDTH,
    wxDVC_DEFAULT_MINWIDTH,

    wxDVR_DEFAULT_ALIGNMENT
};


//---------------------------------------------------------------------------
// Variant helpers that know about the wxDVC types

%{

wxVariant wxDVCVariant_in_helper(PyObject* source)
{
    wxVariant ret;

    if (wxPySimple_typecheck(source, wxT("wxDataViewIconText"), -1)) {
        wxDataViewIconText* ptr;
        wxPyConvertSwigPtr(source, (void**)&ptr, wxT("wxDataViewIconText"));
        ret << *ptr;
    }  
    else
        ret = wxVariant_in_helper(source);
    return ret;
}

PyObject* wxDVCVariant_out_helper(const wxVariant& value)
{
    PyObject* ret;

    if ( value.IsType("wxDataViewIconText") )
    {
        wxDataViewIconText val;
        val << value;
        ret = wxPyConstructObject(new wxDataViewIconText(val), wxT("wxDataViewIconText"), 0);
    }
    else
        ret = wxVariant_out_helper(value);
    return ret;
}

%}
    
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


#define PYCALLBACK_BOOL_DVIRECT(PCLASS, CBNAME)                                 \
    bool CBNAME(const wxDataViewItem &a, wxRect b) {                            \
        bool rval = false;                                                      \
        bool found;                                                             \
        wxPyBlock_t blocked = wxPyBeginBlockThreads();                          \
        if ((found = wxPyCBH_findCallback(m_myInst, #CBNAME))) {                \
            PyObject* ao = wxPyConstructObject((void*)&a, wxT("wxDataViewItem"), 0); \
            PyObject* bo = wxPyConstructObject((void*)&b, wxT("wxRect"), 0);    \
            rval = wxPyCBH_callCallback(m_myInst, Py_BuildValue("(OO)", ao, bo));\
            Py_DECREF(ao);                                                      \
            Py_DECREF(bo);                                                      \
        }                                                                       \
        wxPyEndBlockThreads(blocked);                                           \
        if (! found)                                                            \
            rval = PCLASS::CBNAME(a, b);                                        \
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


#define PYCALLBACK_UINT_DVIDVIA_const(PCLASS, CBNAME)                           \
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


#define PYCALLBACK_VOID_(PCLASS, CBNAME)                                        \
    void CBNAME() {                                                             \
        bool found;                                                             \
        wxPyBlock_t blocked = wxPyBeginBlockThreads();                          \
        if ((found = wxPyCBH_findCallback(m_myInst, #CBNAME)))                  \
            wxPyCBH_callCallback(m_myInst, Py_BuildValue("()"));                \
        wxPyEndBlockThreads(blocked);                                           \
        if (!found)                                                             \
            PCLASS::CBNAME();                                                   \
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


#define PYCALLBACK_BOOL_(PCLASS, CBNAME)                                        \
    bool CBNAME() {                                                             \
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


#define PYCALLBACK_DVI_DVI_const(PCLASS, CBNAME)                                \
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
        wxPyEndBlockThreads(blocked);                                           \
        if (! found)                                                            \
            rval = PCLASS::CBNAME(a);                                           \
        return rval;                                                            \
    }


#define PYCALLBACK_INT_DVIDVIUINTBOOL_const(PCLASS, CBNAME)                     \
    int CBNAME(const wxDataViewItem &a, const wxDataViewItem &b,                \
               unsigned int c, bool d ) const {                                 \
        int rval;                                                               \
        bool found;                                                             \
        wxPyBlock_t blocked = wxPyBeginBlockThreads();                          \
        if ((found = wxPyCBH_findCallback(m_myInst, #CBNAME))) {                \
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


    // TODO:  Why doesn't this just use wxSize_helper?  (See also similar macro in wxPython_int.h)
#define PYCALLBACK_SIZE__constpure(PCLASS, CBNAME)                              \
    wxSize CBNAME() const {                                                     \
        const char* errmsg = #CBNAME " should return a 2-tuple of integers.";   \
        bool found; wxSize rval(0,0);                                           \
        wxPyBlock_t blocked = wxPyBeginBlockThreads();                          \
        if ((found = wxPyCBH_findCallback(m_myInst, #CBNAME))) {                \
            PyObject* ro;                                                       \
            ro = wxPyCBH_callCallbackObj(m_myInst, Py_BuildValue("()"));        \
            if (ro) {                                                           \
                if (PySequence_Check(ro) && PyObject_Length(ro) == 2) {         \
                    PyObject* o1 = PySequence_GetItem(ro, 0);                   \
                    PyObject* o2 = PySequence_GetItem(ro, 1);                   \
                    if (PyNumber_Check(o1) && PyNumber_Check(o2)) {             \
                        rval = wxSize(PyInt_AsLong(o1), PyInt_AsLong(o2));      \
                    }                                                           \
                    else                                                        \
                        PyErr_SetString(PyExc_TypeError, errmsg);               \
                    Py_DECREF(o1);                                              \
                    Py_DECREF(o2);                                              \
                }                                                               \
                else {                                                          \
                    PyErr_SetString(PyExc_TypeError, errmsg);                   \
                }                                                               \
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


#define PYCALLBACK_BOOL_RECTDCINT_pure(PCLASS, CBNAME)                          \
    bool CBNAME(wxRect a, wxDC* b, int c) {                                     \
        bool found;                                                             \
        bool rval = false;                                                      \
        wxPyBlock_t blocked = wxPyBeginBlockThreads();                          \
        if ((found = wxPyCBH_findCallback(m_myInst, #CBNAME))) {                \
            PyObject* ao = wxPyConstructObject((void*)&a, wxT("wxRect"), 0);    \
            PyObject* bo = wxPyMake_wxObject(b,false);                          \
            rval = wxPyCBH_callCallback(m_myInst, Py_BuildValue("(OOi)", ao,bo,c)); \
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


#define PYCALLBACK_BOOL_RECTDVMDVIUINT(PCLASS, CBNAME)                         \
    bool CBNAME(const wxRect& a, wxDataViewModel* b, const wxDataViewItem& c, unsigned int d) { \
        bool found;                                                             \
        bool rval = false;                                                      \
        wxPyBlock_t blocked = wxPyBeginBlockThreads();                          \
        if ((found = wxPyCBH_findCallback(m_myInst, #CBNAME))) {                \
            PyObject* ao = wxPyConstructObject((void*)&a, wxT("wxRect"), 0);    \
            PyObject* bo = wxPyConstructObject((void*)b, wxT("wxDataViewModel"), 0);   \
            PyObject* co = wxPyConstructObject((void*)&c, wxT("wxDataViewItem"), 0);   \
            rval = wxPyCBH_callCallback(m_myInst, Py_BuildValue("(OOOi)", ao,bo,co,d)); \
            Py_DECREF(ao);                                                      \
            Py_DECREF(bo);                                                      \
            Py_DECREF(co);                                                      \
        }                                                                       \
        wxPyEndBlockThreads(blocked);                                           \
        if (! found)                                                            \
            rval = PCLASS::CBNAME(a, b, c, d);                                  \
        return rval;                                                            \
    }


#define PYCALLBACK_BOOL_POINTRECTDVMDVIUINT(PCLASS, CBNAME)                     \
    bool CBNAME(const wxPoint& a, const wxRect& b, wxDataViewModel* c, const wxDataViewItem& d, unsigned int e) { \
        bool found;                                                             \
        bool rval = false;                                                      \
        wxPyBlock_t blocked = wxPyBeginBlockThreads();                          \
        if ((found = wxPyCBH_findCallback(m_myInst, #CBNAME))) {                \
            PyObject* ao = wxPyConstructObject((void*)&b, wxT("wxPoint"), 0);   \
            PyObject* bo = wxPyConstructObject((void*)&b, wxT("wxRect"), 0);    \
            PyObject* co = wxPyConstructObject((void*)c, wxT("wxDataViewModel"), 0);   \
            PyObject* dp = wxPyConstructObject((void*)&d, wxT("wxDataViewItem"), 0);   \
            rval = wxPyCBH_callCallback(m_myInst, Py_BuildValue("(OOOOi)", ao,bo,co,dp,e)); \
            Py_DECREF(ao);                                                      \
            Py_DECREF(bo);                                                      \
            Py_DECREF(co);                                                      \
            Py_DECREF(dp);                                                      \
        }                                                                       \
        wxPyEndBlockThreads(blocked);                                           \
        if (! found)                                                            \
            rval = PCLASS::CBNAME(a, b, c, d, e);                               \
        return rval;                                                            \
    }


%}




//---------------------------------------------------------------------------
// wxDataViewItem
%newgroup

// Typmaps to allow a Python long integer object to be used for the
// void pointer in wxDataViewItem.
%{
typedef void* PyLong;
%}

%typemap(in) PyLong {
    $1 = PyLong_AsVoidPtr($input);
}

%typemap(out) PyLong {
    $result = PyLong_FromVoidPtr($1);
}


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
    wxDataViewItem( PyLong ID = 0 );
    ~wxDataViewItem();

    DocDeclStr(
        bool , IsOk() const,
        "Returns ``True`` if the object refers to an actual item in the data
view control.", "");
    %pythoncode { def __nonzero__(self): return self.IsOk() }

    PyLong GetID() const;    
    %property(ID, GetID);
    
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

%pythoncode { NullDataViewItem = DataViewItem() }

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

    virtual bool BeforeReset();
    virtual bool AfterReset();

    
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
    PYCALLBACK_BOOL_(wxDataViewModelNotifier, BeforeReset)
    PYCALLBACK_BOOL_(wxDataViewModelNotifier, AfterReset)
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
    %pythonAppend wxPyDataViewModelNotifier  setCallbackInfo(PyDataViewModelNotifier);
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
    const wxColour GetColour() const;

    bool HasFont() const;
    bool GetBold() const;
    bool GetItalic() const;

    bool IsDefault() const;

    // Return the font based on the given one with this attribute applied to it.
    wxFont GetEffectiveFont(const wxFont& font) const;

    %property(Colour, GetColour, SetColour);
    %property(Bold, GetBold, SetBold);
    %property(Italic, GetItalic, SetItalic);
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
base class: `DataViewIndexListModel`, `DataViewVirtualListModel-, and
`DataViewTreeStore`.  To create your own model from Python you will
need to use the `PyDataViewModel` as your base class.

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

class wxDataViewModel: public wxRefCounter
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
specified by col. This should return a string indicating the type name of the
data type of the column, as used by wxVariant.", "");


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
        bool , HasValue(const wxDataViewItem& item, unsigned col) const,
        "return true if the given item has a value to display in the given
column: this is always true except for container items which by
default only show their label in the first column (but see
HasContainerColumns())", "");
    

    DocDeclStr(
        virtual bool , SetValue( const wxVariant &variant,
                                 const wxDataViewItem &item, unsigned int col ),
        "This gets called in order to set a value in the data model.  The most
common scenario is that the `DataViewCtrl` calls this method after the
user has changed some data in the view.  The model should then update
whatever it is using for storing the data values and then call
`ValueChanged` so proper notifications are performed.", "");

    
    bool ChangeValue(const wxVariant& variant,
                     const wxDataViewItem& item,
                     unsigned int col);

        
    DocDeclStr(
        virtual bool , GetAttr( const wxDataViewItem &item, unsigned int col,
                                wxDataViewItemAttr &attr ) const,
        "Override this to indicate that the item has special font
attributes. This only affects the `DataViewTextRenderer` renderer.
Return ``False`` if the default attributes should be used.", "");

    
    DocDeclStr(
        virtual bool , IsEnabled(const wxDataViewItem &item,
                                 unsigned int col) const,
        "Override this if you want to disable specific items", "");
    

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


    DocDeclStr(
        bool , ItemAdded( const wxDataViewItem &parent, const wxDataViewItem &item ),
        "Call this to inform the registered notifiers that an item has been
added to the model.", "");

    DocDeclStr(
        bool , ItemsAdded( const wxDataViewItem &parent, const wxDataViewItemArray &items ),
        "Call this to inform the registered notifiers that multiple items have
been added to the data model.", "");

    DocDeclStr(
        bool , ItemDeleted( const wxDataViewItem &parent, const wxDataViewItem &item ),
        "Call this to inform the registered notifiers that an item has been
deleted from the model.", "");

    DocDeclStr(
        bool , ItemsDeleted( const wxDataViewItem &parent, const wxDataViewItemArray &items ),
        "Call this to inform the registered notifiers that multiple items have
been deleted from the data model.", "");

    DocDeclStr(
        bool , ItemChanged( const wxDataViewItem &item ),
        "Call this to inform the registered notifiers that an item has changed.
This will eventually result in a EVT_DATAVIEW_ITEM_VALUE_CHANGED
event, in which the column field will not be set.", "");

    DocDeclStr(
        bool , ItemsChanged( const wxDataViewItemArray &items ),
        "Call this to inform the registered notifiers that multiple items have
changed.  This will eventually result in EVT_DATAVIEW_ITEM_VALUE_CHANGED
events, in which the column field will not be set.", "");

    DocDeclStr(
        bool , ValueChanged( const wxDataViewItem &item, unsigned int col ),
        "Call this to inform the registered notifiers that a value in the model
has been changed.  This will eventually result in a EVT_DATAVIEW_ITEM_VALUE_CHANGED
event.", "");

    DocDeclStr(
        bool , Cleared(),
        "Call this to inform the registered notifiers that all data has been
cleared.  The control will then reread the data from the model again.", "");

    
    bool BeforeReset();
    bool AfterReset();

    
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
    virtual bool IsListModel() const;
    virtual bool IsVirtualListModel() const;
    
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

    PYCALLBACK_INT_DVIDVIUINTBOOL_const(wxDataViewModel, Compare);
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
                variant = wxDVCVariant_in_helper(ro);
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
        if ((found = wxPyCBH_findCallback(m_myInst, "SetValue"))) {
            PyObject* vo = wxDVCVariant_out_helper(variant);
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

    bool GetAttr( const wxDataViewItem &item, unsigned int col, wxDataViewItemAttr &attr ) const
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
            rval = wxDataViewModel::GetAttr(item, col, attr);
        }
        wxPyEndBlockThreads(blocked);
        return rval;
    }

    bool IsEnabled(const wxDataViewItem &item, unsigned int col) const
    {
        bool rval = false;                                                      
        bool found;                                                             
        wxPyBlock_t blocked = wxPyBeginBlockThreads();                          
        if ((found = wxPyCBH_findCallback(m_myInst, "IsEnabled"))) {                
            PyObject* ao = wxPyConstructObject((void*)&item, wxT("wxDataViewItem"), 0);
            rval = wxPyCBH_callCallback(m_myInst, Py_BuildValue("(Oi)", ao, col));
            Py_DECREF(ao);                                                      
        }                                                                       
        else {                                                                  
            rval = wxDataViewModel::IsEnabled(item, col);
        }                                                                       
        wxPyEndBlockThreads(blocked);                                           
        return rval;                                                            
    }
    

    PYPRIVATE;
};

%}


%pythoncode {

class DataViewItemObjectMapper(object):
    """
    This class provides a mechanism for mapping between Python objects and the
    DataViewItem objects used by the DataViewModel for tracking the items in
    the view. The ID used for the item is the id() of the Python object. Use
    `ObjectToItem` to create a DataViewItem using a Python object as its ID,
    and use `ItemToObject` to fetch that Python object again later for a given
    DataViewItem.
    
    By default a regular dictionary is used to implement the ID to object
    mapping. Optionally a WeakValueDictionary can be useful when there will be
    a high turnover of objects and mantaining an extra reference to the
    objects would be unwise.  If weak references are used then the objects
    associated with data items must be weak-referenceable.  (Things like
    stock lists and dictionaries are not.)  See `UseWeakRefs`.
    
    Each `PyDataViewModel` has an instance of this class named objmapper.
    """
    def __init__(self):
        self.mapper = dict()
        self.usingWeakRefs = False
        
    def ObjectToItem(self, obj):
        """
        Create a DataViewItem for the object, and remember the ID-->obj mapping.
        """
        oid = id(obj)
        self.mapper[oid] = obj
        return DataViewItem(oid)

    def ItemToObject(self, item):
        """
        Retrieve the object that was used to create an item.
        """
        oid = item.GetID()
        return self.mapper[oid]

    def UseWeakRefs(self, flag):
        """
        Switch to or from using a weak value dictionary for keeping the ID to
        object map.
        """
        if flag == self.usingWeakRefs:
            return
        if flag:
            import weakref
            newmap = weakref.WeakValueDictionary()
        else:
            newmap = dict()
        newmap.update(self.mapper)
        self.mapper = newmap
        self.usingWeakRefs = flag
        
}    

// tell SWIG about the Py class
DocStr(wxPyDataViewModel,
"This class is a version of `DataViewModel` that has been
engineered to know how to reflect the C++ virtual method calls to
Python methods in the derived class.  Use this class as your base
class instead of `DataViewModel`.", "");

class wxPyDataViewModel: public wxDataViewModel
{
public:
    %pythonAppend wxPyDataViewModel setCallbackInfo(PyDataViewModel) "; self.objmapper = DataViewItemObjectMapper()
";
    wxPyDataViewModel();
    void _setCallbackInfo(PyObject* self, PyObject* _class);

    %pythoncode {
    def ObjectToItem(self, obj):
        "Convenience access to DataViewItemObjectMapper.ObjectToItem."
        return self.objmapper.ObjectToItem(obj)
    
    def ItemToObject(self, item):
        "Convenience access to DataViewItemObjectMapper.ItemToObject."
        return self.objmapper.ItemToObject(item)
   }
};


//---------------------------------------------------------------------------
%newgroup

// The wxDataViewIndexListModel and wxDataViewVirtualIndexModel both have the
// same API and semantics, so use a macro for declaring them, and the related
// Py classes.
%define DECLARE_INDEX_MODEL(ClassName, PyClassName)

class ClassName: public wxDataViewModel
{
public:
    // ClassName( unsigned int initial_size = 0 );   **** ABC
    ~ClassName();


    %extend {
    //  ****  Changed semantics such that the data value is the return value
    //virtual void GetValueByRow( wxVariant &variant,
    //                       unsigned int row, unsigned int col ) const;
        DocDeclStr(
            virtual wxVariant , GetValueByRow( unsigned int row, unsigned int col ) const,
            "Override this method to return the data value to be used for the item
at the given row and column.", "")
        {
            wxVariant var;
            self->GetValueByRow(var, row, col);
            return var;
        }
    }

    DocDeclStr(
        virtual bool , SetValueByRow( const wxVariant &variant,
                                 unsigned int row, unsigned int col ),
        "This is called in order to set a value in the data model.", "");


    DocDeclStr(
        virtual bool , GetAttrByRow( unsigned int row, unsigned int col,
                                wxDataViewItemAttr &attr ),
        "Override this to indicate that the item has special font
attributes. This only affects the `DataViewTextRenderer` renderer.
Return ``False`` if the default attributes should be used.", "");

    
    virtual bool IsEnabledByRow(unsigned int row,
                                unsigned int col) const;


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
        virtual unsigned int , GetCount() const,
        "returns the number of rows", "");
    

    DocDeclStr(
        wxDataViewItem , GetItem( unsigned int row ) const,
        "Returns the DataViewItem for the item at row.", "");
};


%{
// Create a C++ class for the Py version

class PyClassName : public ClassName
{
public:
    PyClassName( unsigned int initial_size = 0)
        : ClassName(initial_size) {}

    PYCALLBACK_UINT__pure_const(ClassName, GetColumnCount);
    PYCALLBACK_STRING_UINT_pure_const(ClassName, GetColumnType);

    //PYCALLBACK_UINT__pure_const(ClassName, GetCount);
    PYCALLBACK_DVI_DVI_const(ClassName, GetParent);
    PYCALLBACK_BOOL_DVI_const(ClassName, IsContainer);
    PYCALLBACK_BOOL_DVI_const(ClassName, HasContainerColumns);
    PYCALLBACK_UINT_DVIDVIA_const(ClassName, GetChildren);

    PYCALLBACK_INT_DVIDVIUINTBOOL_const(ClassName, Compare);
    PYCALLBACK_BOOL__const(ClassName, HasDefaultCompare);

    unsigned int GetCount() const
    {                                             
        bool found;                                                            
        unsigned int rval;                                                     
        wxPyBlock_t blocked = wxPyBeginBlockThreads();                         
        if ((found = wxPyCBH_findCallback(m_myInst, "GetCount")))              
            rval = wxPyCBH_callCallback(m_myInst, Py_BuildValue("()"));        
        else {                                                                 
            PyErr_SetString(PyExc_NotImplementedError,                         
              "The GetCount method should be implemented in derived class"); 
        }                                                                    
        wxPyEndBlockThreads(blocked);                                        
        return rval;                                                         
    }


    virtual void GetValueByRow( wxVariant &variant,
                                unsigned int row, unsigned int col ) const
    {
        // The wxPython version of this method returns the variant as
        // a return value instead of modifying the parameter.
        bool found;
        wxPyBlock_t blocked = wxPyBeginBlockThreads();
        if ((found = wxPyCBH_findCallback(m_myInst, "GetValueByRow"))) {
            PyObject* ro;
            ro = wxPyCBH_callCallbackObj(m_myInst, Py_BuildValue("(ii)", row, col));
            if (ro) {
                variant = wxDVCVariant_in_helper(ro);
                Py_DECREF(ro);
            }
        }
        else {
            PyErr_SetString(PyExc_NotImplementedError,
              "The GetValueByRow method should be implemented in derived class");
        }
        wxPyEndBlockThreads(blocked);
    }


    virtual bool SetValueByRow( const wxVariant &variant,
                                unsigned int row, unsigned int col )
    {
        bool rval = false;
        bool found;
        wxPyBlock_t blocked = wxPyBeginBlockThreads();
        if ((found = wxPyCBH_findCallback(m_myInst, "SetValueByRow"))) {
            PyObject* vo = wxDVCVariant_out_helper(variant);
            rval = wxPyCBH_callCallback(m_myInst, Py_BuildValue("(Oii)", vo, row, col));
            Py_DECREF(vo);
        }
        else {
            PyErr_SetString(PyExc_NotImplementedError,
              "The SetValueByRow method should be implemented in derived class");
        }
        wxPyEndBlockThreads(blocked);
        return rval;
    }


    virtual bool GetAttrByRow( unsigned row, unsigned col,
                               wxDataViewItemAttr &attr ) const
    {
        bool rval = false;
        bool found;
        wxPyBlock_t blocked = wxPyBeginBlockThreads();
        if ((found = wxPyCBH_findCallback(m_myInst, "GetAttrByRow"))) {
            PyObject* ao = wxPyConstructObject((void*)&attr, wxT("wxDataViewItemAttr"), 0);
            rval = wxPyCBH_callCallback(m_myInst, Py_BuildValue("(iiO)", row, col, ao));
            Py_DECREF(ao);
        }
        else {
            rval = wxDataViewListModel::GetAttrByRow(row, col, attr);
        }
        wxPyEndBlockThreads(blocked);
        return rval;
    }


    virtual bool IsEnabledByRow(unsigned int row,
                                unsigned int col) const
    {
        bool rval = false;
        bool found;
        wxPyBlock_t blocked = wxPyBeginBlockThreads();
        if ((found = wxPyCBH_findCallback(m_myInst, "IsEnabledByRow"))) {
            rval = wxPyCBH_callCallback(m_myInst, Py_BuildValue("(ii)", row, col));
        }
        else {
            rval = wxDataViewListModel::IsEnabledByRow(row, col);
        }
        wxPyEndBlockThreads(blocked);
        return rval;
    }


    
    // TODO: Should we also allow to override the other (non-list) virtuals
    // from wxDataViewModel too?  GetValue, SetValue, GetAttr...
    
    PYPRIVATE;
};
%}


// tell SWIG about the Py class
class PyClassName: public ClassName
{
public:
    %pythonAppend PyClassName  setCallbackInfo(PyClassName);
     //         setCallbackInfo(PyDataViewIndexListModel);

    PyClassName(unsigned int initial_size = 0);
    void _setCallbackInfo(PyObject* self, PyObject* _class);
};

%enddef    //------- end of macro -----------




DocStr(wxDataViewIndexListModel,
"DataViewIndexListModel is a specialized data model which lets you
address an item by its position (row) rather than its `DataViewItem`
(which you can obtain from this class if needed). This model also
provides its own `Compare` method which sorts the model's data by the
index.  To implement a custom list-based data model derive a new class
from `PyDataViewIndexListModel` and implement the required methods.

This model is not a virtual model since the control stores each
`DataViewItem` in memory. Use a `DataViewVirtualListModel` if you need
to display millions of items or have other reasons to use a virtual
control.", "");

DocStr(wxPyDataViewIndexListModel,
"This class is a version of `DataViewIndexListModel` that has been
engineered to know how to reflect the C++ virtual method calls to
Python methods in the derived class.  Use this class as your base
class instead of `DataViewIndexListModel`.", "");

DECLARE_INDEX_MODEL(wxDataViewIndexListModel, PyDataViewIndexListModel);


DocStr(wxDataViewVirtualListModel,
"DataViewVirtualListModel is a specialized data model which lets you
address an item by its position (row) rather than its `DataViewItem`
and as such offers the exact same interface as
`DataViewIndexListModel`. The important difference is that under
platforms other than OS X, using this model will result in a truely
virtual control able to handle millions of items as the control
doesn't store any per-item data in memory (a feature not supported by
the Carbon API under OS X).

To implement a custom list-based data model derive a new class from
`PyDataViewVirtualListModel` and implement the required methods.", "");

DocStr(wxPyDataViewVirtualListModel,
"This class is a version of `DataViewVirtualListModel` that has been
engineered to know how to reflect the C++ virtual method calls to
Python methods in the derived class.  Use this class as your base
class instead of `DataViewVirtualListModel`.", "");

DECLARE_INDEX_MODEL(wxDataViewVirtualListModel, PyDataViewVirtualListModel);



//---------------------------------------------------------------------------
//---------------------------------------------------------------------------
// wxDataViewRenderer

enum wxDataViewCellMode
{
    wxDATAVIEW_CELL_INERT,
    wxDATAVIEW_CELL_ACTIVATABLE,
    wxDATAVIEW_CELL_EDITABLE
};

enum wxDataViewCellRenderState
{
    wxDATAVIEW_CELL_SELECTED    = 1,
    wxDATAVIEW_CELL_PRELIT      = 2,
    wxDATAVIEW_CELL_INSENSITIVE = 4,
    wxDATAVIEW_CELL_FOCUSED     = 8
};

DocStr(wxDataViewRenderer,
"This class is used by `DataViewCtrl` to render (or draw) the
individual cells. One instance of a renderer class is owned by each
`DataViewColumn`. There is a number of ready-to-use renderers
provided: `DataViewTextRenderer`, 
`DataViewIconTextRenderer`, `DataViewToggleRenderer`,
`DataViewProgressRenderer`, `DataViewBitmapRenderer`,
`DataViewDateRenderer`, `DataViewSpinRenderer`,
`DataViewChoiceRenderer`.

To create your own custom renderer derive a new class from
`PyDataViewCustomRenderer`.

The mode flag controls what actions the cell data
allows. ``DATAVIEW_CELL_ACTIVATABLE`` indicates that the user can double
click the cell and something will happen (e.g. a window for editing a
date will pop up). ``DATAVIEW_CELL_EDITABLE`` indicates that the user
can edit the data in-place, i.e. an control will show up after a slow
click on the cell. This behaviour is best known from changing the
filename in most file managers etc.
", "");

class wxDataViewRenderer: public wxObject
{
public:
//     ****  It's an ABC
//     wxDataViewRenderer( const wxString &varianttype,
//                         wxDataViewCellMode mode = wxDATAVIEW_CELL_INERT,
//                         int alignment = wxDVR_DEFAULT_ALIGNMENT );
    ~wxDataViewRenderer();

    virtual bool Validate( wxVariant& value );

    void SetOwner( wxDataViewColumn *owner );
    wxDataViewColumn* GetOwner();

    virtual bool SetValue( const wxVariant& value );

    // Change this to return the value or None
    // virtual bool GetValue( wxVariant& value ) const;
    %extend {
        virtual wxVariant  GetValue( ) const
        {
            wxVariant var;
            if (! self->GetValue(var))
                var = wxDVCVariant_in_helper(Py_None);
            return var;
        }
    }

    virtual void SetAttr(const wxDataViewItemAttr& attr);
    virtual void SetEnabled(bool enabled);

    
    wxString GetVariantType() const;

    // helper that calls SetValue and SetAttr:
    void PrepareForItem(const wxDataViewModel *model,
                        const wxDataViewItem& item, unsigned column);

    virtual void SetMode( wxDataViewCellMode mode );
    virtual wxDataViewCellMode GetMode() const;

    virtual void SetAlignment( int align );
    virtual int GetAlignment() const;

    virtual void EnableEllipsize(wxEllipsizeMode mode = wxELLIPSIZE_MIDDLE);
    void DisableEllipsize();
    virtual wxEllipsizeMode GetEllipsizeMode() const;

    // in-place editing
    virtual bool HasEditorCtrl();
    virtual wxWindow* CreateEditorCtrl(wxWindow * parent,
                                        wxRect labelRect,
                                        const wxVariant& value);

    // Change this to return the value or None (maybe it should raise an exception?)
    //virtual bool GetValueFromEditorCtrl(wxWindow * editor,
    //                                    wxVariant& value);
    %extend {
        virtual wxVariant GetValueFromEditorCtrl(wxWindow * editor)
        {
            wxVariant var;
            if (! self->GetValueFromEditorCtrl(editor, var))
                var = wxDVCVariant_in_helper(Py_None);
            return var;
        }
    }

    virtual bool StartEditing( const wxDataViewItem &item, wxRect labelRect );
    virtual void CancelEditing();
    virtual bool FinishEditing();

    wxWindow *GetEditorCtrl();

    %property(Owner, GetOwner, SetOwner);
    %property(Value, GetValue, SetValue);
    %property(VariantType, GetVariantType);
    %property(Mode, GetMode, SetMode);
    %property(Alignment, GetAlignment, SetAlignment);
    %property(EditorCtrl, GetEditorCtrl);
};


//---------------------------------------------------------------------------
// wxDataViewTextRenderer

DocStr(wxDataViewTextRenderer,
"This class is used for rendering text. It supports in-place editing if
desired.", "");

class wxDataViewTextRenderer: public wxDataViewRenderer
{
public:
    wxDataViewTextRenderer(const wxString& varianttype="string",
                           wxDataViewCellMode mode=wxDATAVIEW_CELL_INERT,
                           int align=wxDVR_DEFAULT_ALIGNMENT);
};


//---------------------------------------------------------------------------
// wxDataViewBitmapRenderer

DocStr(wxDataViewBitmapRenderer,
"DataViewBitmapRenderer", "");

class wxDataViewBitmapRenderer: public wxDataViewRenderer
{
public:
    wxDataViewBitmapRenderer(const wxString& varianttype="wxBitmap",
                             wxDataViewCellMode mode=wxDATAVIEW_CELL_INERT,
                             int align=wxDVR_DEFAULT_ALIGNMENT);
};

//---------------------------------------------------------------------------
// wxDataViewIconTextRenderer

DocStr(wxDataViewIconTextRenderer,
"The `DataViewIconTextRenderer` class is used to display text with a
small icon next to it as it is typically done in a file manager. This
class uses the `DataViewIconText` helper class to store its
data.", "");

class  wxDataViewIconTextRenderer: public wxDataViewRenderer
{
public:
  wxDataViewIconTextRenderer(const wxString& varianttype = "wxDataViewIconText",
                             wxDataViewCellMode mode = wxDATAVIEW_CELL_INERT,
                             int align=wxDVR_DEFAULT_ALIGNMENT);
};



DocStr(wxDataViewIconText,
"DataViewIconText is used to hold the data for columns using the
`DataViewIconTextRenderer`", "");

class wxDataViewIconText: public wxObject
{
public:
    wxDataViewIconText( const wxString &text = wxEmptyString,
                        const wxIcon& icon = wxNullIcon );


    void SetText( const wxString &text );
    wxString GetText() const;
    void SetIcon( const wxIcon &icon );
    const wxIcon &GetIcon() const;
};




//---------------------------------------------------------------------------
// wxDataViewToggleRenderer

DocStr(wxDataViewToggleRenderer,
"DataViewToggleRenderer", "");

class wxDataViewToggleRenderer: public wxDataViewRenderer
{
public:
    wxDataViewToggleRenderer(const wxString & varianttype = "bool",
                             wxDataViewCellMode mode = wxDATAVIEW_CELL_INERT,
                             int align=wxDVR_DEFAULT_ALIGNMENT);
};


//---------------------------------------------------------------------------
// wxDataViewProgressRenderer

DocStr(wxDataViewProgressRenderer,
"DataViewProgressRenderer", "");

class wxDataViewProgressRenderer: public wxDataViewRenderer
{
public:
    wxDataViewProgressRenderer(const wxString& label = wxEmptyString,
                               const wxString& varianttype="long",
                               wxDataViewCellMode mode=wxDATAVIEW_CELL_INERT,
                               int align=wxDVR_DEFAULT_ALIGNMENT);
};

//---------------------------------------------------------------------------
// wxDataViewSpinRenderer

DocStr(wxDataViewSpinRenderer,
"This is a specialized renderer for rendering integer values. It
supports modifying the values in-place by using a `wx.SpinCtrl`. The
renderer only support integer data items.", "");

class wxDataViewSpinRenderer: public wxDataViewRenderer
{
public:
    wxDataViewSpinRenderer( int min, int max,
                            wxDataViewCellMode mode = wxDATAVIEW_CELL_EDITABLE,
                            int alignment = wxDVR_DEFAULT_ALIGNMENT );
};

//---------------------------------------------------------------------------
// wxDataViewCustomRenderer

DocStr(wxDataViewCustomRenderer,
"See `PyDataViewCustomRenderer`.", "");

class wxDataViewCustomRenderer: public wxDataViewRenderer
{
public:
    virtual void SetAttr(const wxDataViewItemAttr& attr);
    const wxDataViewItemAttr& GetAttr() const;

    virtual void SetEnabled(bool enabled);
    bool GetEnabled() const;
};

//---------------------------------------------------------------------------
// wxDataViewChoiceRenderer

DocStr(wxDataViewChoiceRenderer,
"","");

class wxDataViewChoiceRenderer: public wxDataViewCustomRenderer
{
public:
    wxDataViewChoiceRenderer( const wxArrayString &choices,
                              wxDataViewCellMode mode = wxDATAVIEW_CELL_EDITABLE,
                              int alignment = wxDVR_DEFAULT_ALIGNMENT );

    wxString GetChoice(size_t index) const;
    const wxArrayString& GetChoices() const;
};



#ifndef __WXOSX_COCOA__
//---------------------------------------------------------------------------
// wxDataViewChoiceByIndexRenderer

DocStr(wxDataViewChoiceByIndexRenderer,
"","");

class wxDataViewChoiceByIndexRenderer: public wxDataViewChoiceRenderer
{
public:
    wxDataViewChoiceByIndexRenderer( const wxArrayString &choices,
                                     wxDataViewCellMode mode = wxDATAVIEW_CELL_EDITABLE,
                                     int alignment = wxDVR_DEFAULT_ALIGNMENT );
};
#endif

//---------------------------------------------------------------------------
// wxDataViewDateRenderer

DocStr(wxDataViewDateRenderer,
"","");

class wxDataViewDateRenderer: public wxDataViewRenderer
{
public:
  wxDataViewDateRenderer(const wxString& varianttype="datetime",
                         wxDataViewCellMode mode=wxDATAVIEW_CELL_ACTIVATABLE,
                         int align=wxDVR_DEFAULT_ALIGNMENT);
};


//---------------------------------------------------------------------------
// a wxDataViewCustomRenderer vitualized for Python

%{ // Derive from the class in C++ for virtualization

class wxPyDataViewCustomRenderer : public wxDataViewCustomRenderer
{
public:
    wxPyDataViewCustomRenderer(const wxString& varianttype="string",
                               wxDataViewCellMode mode=wxDATAVIEW_CELL_INERT,
                               int align=wxDVR_DEFAULT_ALIGNMENT)
        : wxDataViewCustomRenderer(varianttype, mode, align)
    {}

    // Make some protected methods visible
    wxSize GetTextExtent(const wxString& str) const
    {
        return wxDataViewCustomRenderer::GetTextExtent(str);
    }

    const wxDataViewCtrl* GetView() const
    {
        return wxDataViewCustomRenderer::GetView();
    }

    
    PYCALLBACK_SIZE__constpure(wxDataViewCustomRenderer, GetSize);
    PYCALLBACK_BOOL_RECTDCINT_pure(wxDataViewCustomRenderer, Render);
    PYCALLBACK_BOOL_RECTDVMDVIUINT(wxDataViewCustomRenderer, Activate);
    PYCALLBACK_BOOL_POINTRECTDVMDVIUINT(wxDataViewCustomRenderer, LeftClick);
    PYCALLBACK_BOOL_POINTRECTDVMDVIUINT(wxDataViewCustomRenderer, StartDrag);

    
    virtual bool SetValue( const wxVariant& value )
    {
        bool found;
        bool rval = false;
        wxPyBlock_t blocked = wxPyBeginBlockThreads();
        if ((found = wxPyCBH_findCallback(m_myInst, "SetValue"))) {
            PyObject* v = wxDVCVariant_out_helper(value);
            rval = wxPyCBH_callCallback(m_myInst, Py_BuildValue("(O)", v));
            Py_DECREF(v);
        }
        else {
            PyErr_SetString(PyExc_NotImplementedError,
              "The SetValue method should be implemented in derived class");
        }
        wxPyEndBlockThreads(blocked);
        return rval;
    }


    virtual bool GetValue( wxVariant& value ) const
    {
        // The wxPython version of this method returns the variant as
        // a return value instead of modifying the parameter.
        bool found;
        wxPyBlock_t blocked = wxPyBeginBlockThreads();
        if ((found = wxPyCBH_findCallback(m_myInst, "GetValue"))) {
            PyObject* ro;
            ro = wxPyCBH_callCallbackObj(m_myInst, Py_BuildValue("()"));
            if (ro) {
                value = wxDVCVariant_in_helper(ro);
                Py_DECREF(ro);
            }
        }
        else {
            PyErr_SetString(PyExc_NotImplementedError,
              "The GetValue method should be implemented in derived class");
        }
        wxPyEndBlockThreads(blocked);
        return true;
    }

    PYCALLBACK_BOOL__const(wxDataViewCustomRenderer, HasEditorCtrl);

    virtual wxWindow* CreateEditorCtrl(wxWindow * parent,
                                        wxRect labelRect,
                                        const wxVariant& value)
    {
        bool found;
        wxControl* ret = NULL;
        wxPyBlock_t blocked = wxPyBeginBlockThreads();
        if ((found = wxPyCBH_findCallback(m_myInst, "CreateEditorCtrl"))) {
            PyObject* ro;
            PyObject* po = wxPyConstructObject((void*)parent, wxT("wxWindow"), 0);
            PyObject* rto = wxPyConstructObject((void*)&labelRect, wxT("wxRect"), 0);
            PyObject* vo = wxDVCVariant_out_helper(value);
            ro = wxPyCBH_callCallbackObj(m_myInst, Py_BuildValue("(OOO)", po, rto, vo));
            Py_DECREF(po);
            Py_DECREF(rto);
            Py_DECREF(vo);
            if (ro) {
                wxPyConvertSwigPtr(ro, (void**)&ret, wxT("wxControl"));
                Py_DECREF(ro);
            }
        }
        wxPyEndBlockThreads(blocked);
        if (!found)
            return wxDataViewCustomRenderer::CreateEditorCtrl(parent, labelRect, value);
        else
            return ret;
    }

    virtual bool GetValueFromEditorCtrl(wxControl * editor,
                                        wxVariant& value)
    {
        // The wxPython version of this method returns the variant as
        // a return value instead of modifying the parameter.
        bool found;
        wxPyBlock_t blocked = wxPyBeginBlockThreads();
        if ((found = wxPyCBH_findCallback(m_myInst, "GetValueFromEditorCtrl"))) {
            PyObject* ro;
            PyObject* io = wxPyMake_wxObject2(editor, false, true);
            ro = wxPyCBH_callCallbackObj(m_myInst, Py_BuildValue("(O)", io));
            Py_DECREF(io);
            if (ro) {
                value = wxDVCVariant_in_helper(ro);
                Py_DECREF(ro);
            }
        }
        wxPyEndBlockThreads(blocked);
        if (!found)
            return wxDataViewCustomRenderer::GetValueFromEditorCtrl(editor, value);
        else
            return true;
    }

    PYCALLBACK_BOOL_DVIRECT(wxDataViewCustomRenderer, StartEditing);
    PYCALLBACK_VOID_(wxDataViewCustomRenderer, CancelEditing);
    PYCALLBACK_BOOL_(wxDataViewCustomRenderer, FinishEditing);

    void SetAttr(const wxDataViewItemAttr &a)
    {                                  
        bool found;                                                             
        wxPyBlock_t blocked = wxPyBeginBlockThreads();                          
        if ((found = wxPyCBH_findCallback(m_myInst, "SetAttr"))) {                
            PyObject* ao = wxPyConstructObject((void*)&a, wxT("wxDataViewItemAttr"), 0);
            wxPyCBH_callCallback(m_myInst, Py_BuildValue("(O)", ao));           
            Py_DECREF(ao);                                                      
        }                                                                       
        wxPyEndBlockThreads(blocked);                                           
        if (! found)                                                            
            wxDataViewCustomRenderer::SetAttr(a);                                                  
    }

    virtual void SetEnabled(bool enabled)
    {
        bool found;                                                     
        wxPyBlock_t blocked = wxPyBeginBlockThreads();                  
        if ((found = wxPyCBH_findCallback(m_myInst, "SetEnabled")))          
            wxPyCBH_callCallback(m_myInst, Py_BuildValue("(i)",enabled));  
        wxPyEndBlockThreads(blocked);                                   
        if (! found)                                                    
            wxDataViewCustomRenderer::SetEnabled(enabled);                                        
    }                        
    
   
    PYPRIVATE;
};

%}



DocStr(wxDataViewCustomRenderer,
"", "");

class wxPyDataViewCustomRenderer: public wxDataViewCustomRenderer
{
public:

    %pythonAppend wxPyDataViewCustomRenderer  setCallbackInfo(PyDataViewCustomRenderer);

    wxPyDataViewCustomRenderer(const wxString& varianttype="string",
                               wxDataViewCellMode mode=wxDATAVIEW_CELL_INERT,
                               int align=wxDVR_DEFAULT_ALIGNMENT);

    void _setCallbackInfo(PyObject* self, PyObject* _class);

    DocDeclStr(
        void , RenderText( const wxString &text, int xoffset, wxRect cell, wxDC *dc, int state ),
        "This method should be called from within your `Render` override
whenever you need to render simple text. This will help ensure that the
correct colour, font and vertical alignment will be chosen so the text
will look the same as text drawn by native renderers.", "");

    DocDeclStr(
        virtual wxSize , GetSize() const,
        "Returns the size required to show content.  This must be overridden in
derived classes.", "");

    DocDeclStr(
        virtual bool , Render(wxRect cell, wxDC* dc, int state),
        "Override this to render the cell. Before this is called, `SetValue`
was called so that this instance knows what to render.  This must be
overridden in derived classes.", "");

    DocDeclStr(
        virtual bool , Activate(wxRect cell,
                                wxDataViewModel *model,
                                const wxDataViewItem & item, 
                                unsigned int col),
        "Override this to react to double clicks or <ENTER>.", "");

    DocDeclStr(
        virtual bool , LeftClick(wxPoint cursor,
                                 wxRect cell,
                                 wxDataViewModel *model,
                                 const wxDataViewItem & item, 
                                 unsigned int col),
        "Overrride this to react to a left click.", "");

//     DocDeclStr(
//         virtual bool , RightClick(wxPoint cursor,
//                                   wxRect cell,
//                                   wxDataViewModel *model,
//                                   const wxDataViewItem & item, 
//                                   unsigned int col),
//         "Overrride this to react to a right click.", "");

    DocDeclStr(
        virtual bool , StartDrag(wxPoint cursor,
                                 wxRect cell,
                                 wxDataViewModel *model,
                                 const wxDataViewItem & item, 
                                 unsigned int col),
        "Overrride this to react to the start of a drag operation.", "");

    DocDeclStr(
        virtual wxDC* , GetDC(void),
        "Create DC on request.", "");

//    void SetDC(wxDC* newDCPtr); // this method takes ownership of the pointer

    
    wxSize GetTextExtent(const wxString& str) const;
    const wxDataViewCtrl* GetView() const;

};


//---------------------------------------------------------------------------
//---------------------------------------------------------------------------


enum wxDataViewColumnFlags
{
    wxDATAVIEW_COL_RESIZABLE,
    wxDATAVIEW_COL_SORTABLE,
    wxDATAVIEW_COL_REORDERABLE,
    wxDATAVIEW_COL_HIDDEN 
};

class wxDataViewColumn: public wxSettableHeaderColumn
{
public:
    // make a custom overloading of the ctor to be able to keep the kw args
    %disownarg(wxDataViewRenderer* renderer);
    %extend {
        wxDataViewColumn(PyObject* title_or_bitmap,
                         wxDataViewRenderer* renderer,
                         unsigned int model_column,
                         int width=80,
                         wxAlignment align=wxALIGN_CENTER,
                         int flags=wxDATAVIEW_COL_RESIZABLE)
        {
            bool wasString;
            wxString label;
            wxBitmap bitmap;
            if (! wxPyTextOrBitmap_helper(title_or_bitmap, wasString, label, bitmap))
                return NULL;
            return wasString ?
                new wxDataViewColumn(label, renderer, model_column, width, align, flags)
                :  new wxDataViewColumn(bitmap, renderer, model_column, width, align, flags);
        }
    }
    %cleardisown(wxDataViewRenderer* renderer);


    virtual void SetOwner( wxDataViewCtrl *owner );

    unsigned int GetModelColumn() const;
    wxDataViewCtrl *GetOwner() const;
    wxDataViewRenderer* GetRenderer() const;

    %property(ModelColumn, GetModelColumn);
    %property(Owner, GetOwner, SetOwner);
    %property(Renderer, GetRenderer);

};


//---------------------------------------------------------------------------
// wxDataViewCtrl

enum {
    wxDV_SINGLE,
    wxDV_MULTIPLE,

    wxDV_NO_HEADER,
    wxDV_HORIZ_RULES,
    wxDV_VERT_RULES,

    wxDV_ROW_LINES,
    wxDV_VARIABLE_LINE_HEIGHT,
};


DocStr(wxDataViewCtrl,
"", "");

class wxDataViewCtrl: public wxControl
{
public:
    %pythonAppend wxDataViewCtrl         "self._setOORInfo(self)"
    %pythonAppend wxDataViewCtrl()       ""
    %typemap(out) wxDataViewCtrl*;       // turn off this typemap

    wxDataViewCtrl(wxWindow *parent, wxWindowID id=wxID_ANY,
                   const wxPoint& pos = wxDefaultPosition,
                   const wxSize& size = wxDefaultSize,
                   long style = 0,
                   const wxValidator& validator = wxDefaultValidator,
                   const wxString& name = wxDataViewCtrlNameStr);
    %RenameCtor(PreDataViewCtrl, wxDataViewCtrl());

    // Turn it back on again
    %typemap(out) wxDataViewCtrl* { $result = wxPyMake_wxObject($1, $owner); }

    bool Create(wxWindow *parent,
                wxWindowID id=-1,
                const wxPoint& pos = wxDefaultPosition,
                const wxSize& size = wxDefaultSize, long style = 0,
                const wxValidator& validator = wxDefaultValidator,
                const wxString& name = wxDataViewCtrlNameStr);

    
    virtual bool AssociateModel( wxDataViewModel *model );
    wxDataViewModel* GetModel();
    //%pythoncode { SetModel = AssociateModel }
    

    // All these Prepend and Append convenience methods are overloaded
    // on the first parameter, which can be either a wxString or a
    // wxBitmap.  So we'll handle the overloading ourselves in order
    // to still allow kwargs to be used for the other params.
    %extend {
    wxDataViewColumn*
        PrependTextColumn(PyObject* label_or_bitmap, unsigned int model_column,
                          wxDataViewCellMode mode = wxDATAVIEW_CELL_INERT,
                          int width = -1,
                          wxAlignment align = wxALIGN_NOT,
                          int flags = wxDATAVIEW_COL_RESIZABLE )
    {
        bool wasString; wxString label; wxBitmap bitmap;
        if (! wxPyTextOrBitmap_helper(label_or_bitmap, wasString, label, bitmap))
            return NULL;
        return wasString ?
            self->PrependTextColumn(label, model_column, mode, width, align, flags)
            : self->PrependTextColumn(bitmap, model_column, mode, width, align, flags);
    }


    wxDataViewColumn*
        PrependIconTextColumn( PyObject* label_or_bitmap, unsigned int model_column,
                               wxDataViewCellMode mode = wxDATAVIEW_CELL_INERT,
                               int width = -1,
                               wxAlignment align = wxALIGN_NOT,
                               int flags = wxDATAVIEW_COL_RESIZABLE )
    {
        bool wasString; wxString label; wxBitmap bitmap;
        if (! wxPyTextOrBitmap_helper(label_or_bitmap, wasString, label, bitmap))
            return NULL;
        return wasString ?
            self->PrependIconTextColumn(label, model_column, mode, width, align, flags)
            : self->PrependIconTextColumn(bitmap, model_column, mode, width, align, flags);
    }


    wxDataViewColumn*
        PrependToggleColumn( PyObject* label_or_bitmap, unsigned int model_column,
                             wxDataViewCellMode mode = wxDATAVIEW_CELL_INERT,
                             int width = wxDVC_TOGGLE_DEFAULT_WIDTH,
                             wxAlignment align = wxALIGN_CENTER,
                             int flags = wxDATAVIEW_COL_RESIZABLE )
    {
        bool wasString; wxString label; wxBitmap bitmap;
        if (! wxPyTextOrBitmap_helper(label_or_bitmap, wasString, label, bitmap))
            return NULL;
        return wasString ?
            self->PrependToggleColumn(label, model_column, mode, width, align, flags)
            : self->PrependToggleColumn(bitmap, model_column, mode, width, align, flags);
    }

    wxDataViewColumn*
        PrependProgressColumn( PyObject* label_or_bitmap, unsigned int model_column,
                               wxDataViewCellMode mode = wxDATAVIEW_CELL_INERT,
                               int width = wxDVC_DEFAULT_WIDTH,
                               wxAlignment align = wxALIGN_CENTER,
                               int flags = wxDATAVIEW_COL_RESIZABLE )
    {
        bool wasString; wxString label; wxBitmap bitmap;
        if (! wxPyTextOrBitmap_helper(label_or_bitmap, wasString, label, bitmap))
            return NULL;
        return wasString ?
            self->PrependProgressColumn(label, model_column, mode, width, align, flags)
            : self->PrependProgressColumn(bitmap, model_column, mode, width, align, flags);
    }

    wxDataViewColumn*
        PrependDateColumn( PyObject* label_or_bitmap, unsigned int model_column,
                           wxDataViewCellMode mode = wxDATAVIEW_CELL_ACTIVATABLE,
                           int width = -1,
                           wxAlignment align = wxALIGN_NOT,
                           int flags = wxDATAVIEW_COL_RESIZABLE )
    {
        bool wasString; wxString label; wxBitmap bitmap;
        if (! wxPyTextOrBitmap_helper(label_or_bitmap, wasString, label, bitmap))
            return NULL;
        return wasString ?
            self->PrependDateColumn(label, model_column, mode, width, align, flags)
            : self->PrependDateColumn(bitmap, model_column, mode, width, align, flags);
    }

    wxDataViewColumn*
        PrependBitmapColumn( PyObject* label_or_bitmap, unsigned int model_column,
                             wxDataViewCellMode mode = wxDATAVIEW_CELL_INERT,
                             int width = -1,
                             wxAlignment align = wxALIGN_CENTER,
                             int flags = wxDATAVIEW_COL_RESIZABLE )
    {
        bool wasString; wxString label; wxBitmap bitmap;
        if (! wxPyTextOrBitmap_helper(label_or_bitmap, wasString, label, bitmap))
            return NULL;
        return wasString ?
            self->PrependBitmapColumn(label, model_column, mode, width, align, flags)
            : self->PrependBitmapColumn(bitmap, model_column, mode, width, align, flags);
    }



    wxDataViewColumn*
        AppendTextColumn( PyObject* label_or_bitmap, unsigned int model_column,
                          wxDataViewCellMode mode = wxDATAVIEW_CELL_INERT,
                          int width = -1,
                          wxAlignment align = wxALIGN_NOT,
                          int flags = wxDATAVIEW_COL_RESIZABLE )
    {
        bool wasString; wxString label; wxBitmap bitmap;
        if (! wxPyTextOrBitmap_helper(label_or_bitmap, wasString, label, bitmap))
            return NULL;
        return wasString ?
            self->AppendTextColumn(label, model_column, mode, width, align, flags)
            : self->AppendTextColumn(bitmap, model_column, mode, width, align, flags);
    }

    wxDataViewColumn*
        AppendIconTextColumn( PyObject* label_or_bitmap, unsigned int model_column,
                              wxDataViewCellMode mode = wxDATAVIEW_CELL_INERT,
                              int width = -1,
                              wxAlignment align =  wxALIGN_NOT,
                              int flags = wxDATAVIEW_COL_RESIZABLE )
    {
        bool wasString; wxString label; wxBitmap bitmap;
        if (! wxPyTextOrBitmap_helper(label_or_bitmap, wasString, label, bitmap))
            return NULL;
        return wasString ?
            self->AppendIconTextColumn(label, model_column, mode, width, align, flags)
            : self->AppendIconTextColumn(bitmap, model_column, mode, width, align, flags);
    }

    wxDataViewColumn*
        AppendToggleColumn( PyObject* label_or_bitmap, unsigned int model_column,
                            wxDataViewCellMode mode = wxDATAVIEW_CELL_INERT,
                            int width = wxDVC_TOGGLE_DEFAULT_WIDTH,
                            wxAlignment align = wxALIGN_CENTER,
                            int flags = wxDATAVIEW_COL_RESIZABLE )
    {
        bool wasString; wxString label; wxBitmap bitmap;
        if (! wxPyTextOrBitmap_helper(label_or_bitmap, wasString, label, bitmap))
            return NULL;
        return wasString ?
            self->AppendToggleColumn(label, model_column, mode, width, align, flags)
            : self->AppendToggleColumn(bitmap, model_column, mode, width, align, flags);
    }

    wxDataViewColumn*
        AppendProgressColumn( PyObject* label_or_bitmap, unsigned int model_column,
                              wxDataViewCellMode mode = wxDATAVIEW_CELL_INERT,
                              int width = wxDVC_DEFAULT_WIDTH,
                              wxAlignment align = wxALIGN_CENTER,
                              int flags = wxDATAVIEW_COL_RESIZABLE )
    {
        bool wasString; wxString label; wxBitmap bitmap;
        if (! wxPyTextOrBitmap_helper(label_or_bitmap, wasString, label, bitmap))
            return NULL;
        return wasString ?
            self->AppendProgressColumn(label, model_column, mode, width, align, flags)
            : self->AppendProgressColumn(bitmap, model_column, mode, width, align, flags);
    }

    wxDataViewColumn*
        AppendDateColumn( PyObject* label_or_bitmap, unsigned int model_column,
                          wxDataViewCellMode mode = wxDATAVIEW_CELL_ACTIVATABLE,
                          int width = -1,
                          wxAlignment align =  wxALIGN_NOT,
                          int flags = wxDATAVIEW_COL_RESIZABLE )
    {
        bool wasString; wxString label; wxBitmap bitmap;
        if (! wxPyTextOrBitmap_helper(label_or_bitmap, wasString, label, bitmap))
            return NULL;
        return wasString ?
            self->AppendDateColumn(label, model_column, mode, width, align, flags)
            : self->AppendDateColumn(bitmap, model_column, mode, width, align, flags);
    }

    wxDataViewColumn*
        AppendBitmapColumn( PyObject* label_or_bitmap, unsigned int model_column,
                            wxDataViewCellMode mode = wxDATAVIEW_CELL_INERT,
                            int width = -1,
                            wxAlignment align = wxALIGN_CENTER,
                            int flags = wxDATAVIEW_COL_RESIZABLE )
    {
        bool wasString; wxString label; wxBitmap bitmap;
        if (! wxPyTextOrBitmap_helper(label_or_bitmap, wasString, label, bitmap))
            return NULL;
        return wasString ?
            self->AppendBitmapColumn(label, model_column, mode, width, align, flags)
            : self->AppendBitmapColumn(bitmap, model_column, mode, width, align, flags);
    }

    }


    %disownarg( wxDataViewColumn *col );
    virtual bool PrependColumn( wxDataViewColumn *col );
    virtual bool InsertColumn( unsigned int pos, wxDataViewColumn *col );
    virtual bool AppendColumn( wxDataViewColumn *col );
    %cleardisown( wxDataViewColumn *col );

    
    virtual unsigned int GetColumnCount() const;
    virtual wxDataViewColumn* GetColumn( unsigned int pos ) const;
    %pythoncode {
        def GetColumns(self):
            """Returns a list of column objects."""
            return [self.GetColumn(i) for i in range(self.GetColumnCount())]
    }
    
    virtual int GetColumnPosition( const wxDataViewColumn *column ) const;
    virtual bool DeleteColumn( wxDataViewColumn *column );
    virtual bool ClearColumns();

    void SetExpanderColumn( wxDataViewColumn *col );
    wxDataViewColumn *GetExpanderColumn() const;

    virtual wxDataViewColumn *GetSortingColumn() const;

    void SetIndent( int indent );
    int GetIndent() const;

    wxDataViewItem GetCurrentItem() const;
    void SetCurrentItem(const wxDataViewItem& item);
        
    virtual wxDataViewItem GetSelection() const;

    //virtual int GetSelections( wxDataViewItemArray & sel ) const;
    %extend {
        wxDataViewItemArray GetSelections() const {
            wxDataViewItemArray selections;
            self->GetSelections(selections);
            return selections;
        }
    }
    virtual void SetSelections( const wxDataViewItemArray & sel );
    virtual void Select( const wxDataViewItem & item );
    virtual void Unselect( const wxDataViewItem & item );
    virtual bool IsSelected( const wxDataViewItem & item ) const;

    virtual void SelectAll();
    virtual void UnselectAll();

    virtual void Expand( const wxDataViewItem & item );
    virtual void ExpandAncestors( const wxDataViewItem & item );
    virtual void Collapse( const wxDataViewItem & item );
    virtual bool IsExpanded( const wxDataViewItem & item ) const;

    virtual void EnsureVisible( const wxDataViewItem & item,
                                const wxDataViewColumn *column = NULL );

    // TODO:  Should probably change this to return the item and col as a tuple...)
    virtual void HitTest( const wxPoint & point, wxDataViewItem &item, wxDataViewColumn* &column ) const;
    
    virtual wxRect GetItemRect( const wxDataViewItem & item, const wxDataViewColumn *column = NULL ) const;

    virtual bool SetRowHeight( int rowHeight );

    virtual void StartEditor( const wxDataViewItem & item, unsigned int column );
    
    virtual bool EnableDragSource(const wxDataFormat& format);
    virtual bool EnableDropTarget(const wxDataFormat& format);

    %property(Model, GetModel, AssociateModel);
    %property(ColumnCount, GetColumnCount);
    %property(Columns, GetColumns);
    %property(ExpanderColumn, GetExpanderColumn, SetExpanderColumn);
    %property(SortingColumn, GetSortingColumn);
    %property(Indent, GetIndent, SetIndent);
    %property(Selection, GetSelection);

    static wxVisualAttributes
    GetClassDefaultAttributes(wxWindowVariant variant = wxWINDOW_VARIANT_NORMAL);

};

//---------------------------------------------------------------------------

class wxDataViewEvent : public wxNotifyEvent
{
public:
    wxDataViewEvent(wxEventType commandType = wxEVT_NULL, int winid = 0);
    wxDataViewItem GetItem() const;
    void SetItem( const wxDataViewItem &item );

    int GetColumn() const;
    void SetColumn( int col );

    wxDataViewModel* GetModel() const;
    void SetModel( wxDataViewModel *model );

    const wxVariant &GetValue() const;
    void SetValue( const wxVariant &value );

    // for wxEVT_DATAVIEW_COLUMN_HEADER_CLICKED only
    void SetDataViewColumn( wxDataViewColumn *col );
    wxDataViewColumn *GetDataViewColumn() const;

    // for wxEVT_DATAVIEW_CONTEXT_MENU only
    wxPoint GetPosition() const;
    void SetPosition( int x, int y );

    // For wxEVT_COMMAND_DATAVIEW_CACHE_HINT
    int GetCacheFrom() const;
    int GetCacheTo() const;
    void SetCache(int from, int to);
    
    // For drag operations
    void SetDataObject( wxDataObject *obj );
    wxDataObject *GetDataObject() const;

    // For drop operations
    void SetDataFormat( const wxDataFormat &format );
    wxDataFormat GetDataFormat() const;

    // TODO: Use a Python buffer object here instead of void pointers and
    // sizes...
    void SetDataSize( size_t size );
    size_t GetDataSize() const;
    void SetDataBuffer( void* buf );
    void *GetDataBuffer() const;

    %property(Column, GetColumn, SetColumn);
    %property(Model, GetModel, SetModel);
    %property(Value, GetValue, SetValue);
    %property(DataViewColumn, GetDataViewColumn, SetDataViewColumn);
    %property(Position, GetPosition, SetPosition);
    %property(DataObject, GetDataObject, SetDataObject);
    %property(DataFormat, GetDataFormat, SetDataFormat);
    
};

%constant wxEventType wxEVT_COMMAND_DATAVIEW_SELECTION_CHANGED;
%constant wxEventType wxEVT_COMMAND_DATAVIEW_ITEM_ACTIVATED;
%constant wxEventType wxEVT_COMMAND_DATAVIEW_ITEM_COLLAPSED;
%constant wxEventType wxEVT_COMMAND_DATAVIEW_ITEM_EXPANDED;
%constant wxEventType wxEVT_COMMAND_DATAVIEW_ITEM_COLLAPSING;
%constant wxEventType wxEVT_COMMAND_DATAVIEW_ITEM_EXPANDING;
%constant wxEventType wxEVT_COMMAND_DATAVIEW_ITEM_START_EDITING;
%constant wxEventType wxEVT_COMMAND_DATAVIEW_ITEM_EDITING_STARTED;
%constant wxEventType wxEVT_COMMAND_DATAVIEW_ITEM_EDITING_DONE;
%constant wxEventType wxEVT_COMMAND_DATAVIEW_ITEM_VALUE_CHANGED;
%constant wxEventType wxEVT_COMMAND_DATAVIEW_ITEM_CONTEXT_MENU;
%constant wxEventType wxEVT_COMMAND_DATAVIEW_COLUMN_HEADER_CLICK;
%constant wxEventType wxEVT_COMMAND_DATAVIEW_COLUMN_HEADER_RIGHT_CLICK;
%constant wxEventType wxEVT_COMMAND_DATAVIEW_COLUMN_SORTED;
%constant wxEventType wxEVT_COMMAND_DATAVIEW_COLUMN_REORDERED;
%constant wxEventType wxEVT_COMMAND_DATAVIEW_ITEM_BEGIN_DRAG;
%constant wxEventType wxEVT_COMMAND_DATAVIEW_ITEM_DROP_POSSIBLE;
%constant wxEventType wxEVT_COMMAND_DATAVIEW_ITEM_DROP;           
%constant wxEventType wxEVT_COMMAND_DATAVIEW_CACHE_HINT;


%pythoncode {

EVT_DATAVIEW_SELECTION_CHANGED         = wx.PyEventBinder( wxEVT_COMMAND_DATAVIEW_SELECTION_CHANGED, 1)
EVT_DATAVIEW_ITEM_ACTIVATED            = wx.PyEventBinder( wxEVT_COMMAND_DATAVIEW_ITEM_ACTIVATED, 1)
EVT_DATAVIEW_ITEM_COLLAPSED            = wx.PyEventBinder( wxEVT_COMMAND_DATAVIEW_ITEM_COLLAPSED, 1)
EVT_DATAVIEW_ITEM_EXPANDED             = wx.PyEventBinder( wxEVT_COMMAND_DATAVIEW_ITEM_EXPANDED, 1)
EVT_DATAVIEW_ITEM_COLLAPSING           = wx.PyEventBinder( wxEVT_COMMAND_DATAVIEW_ITEM_COLLAPSING, 1)
EVT_DATAVIEW_ITEM_EXPANDING            = wx.PyEventBinder( wxEVT_COMMAND_DATAVIEW_ITEM_EXPANDING, 1)
EVT_DATAVIEW_ITEM_START_EDITING        = wx.PyEventBinder( wxEVT_COMMAND_DATAVIEW_ITEM_START_EDITING, 1)    
EVT_DATAVIEW_ITEM_EDITING_STARTED      = wx.PyEventBinder( wxEVT_COMMAND_DATAVIEW_ITEM_EDITING_STARTED, 1)
EVT_DATAVIEW_ITEM_EDITING_DONE         = wx.PyEventBinder( wxEVT_COMMAND_DATAVIEW_ITEM_EDITING_DONE, 1)
EVT_DATAVIEW_ITEM_VALUE_CHANGED        = wx.PyEventBinder( wxEVT_COMMAND_DATAVIEW_ITEM_VALUE_CHANGED, 1)
EVT_DATAVIEW_ITEM_CONTEXT_MENU         = wx.PyEventBinder( wxEVT_COMMAND_DATAVIEW_ITEM_CONTEXT_MENU, 1)
EVT_DATAVIEW_COLUMN_HEADER_CLICK       = wx.PyEventBinder( wxEVT_COMMAND_DATAVIEW_COLUMN_HEADER_CLICK, 1)
EVT_DATAVIEW_COLUMN_HEADER_RIGHT_CLICK = wx.PyEventBinder( wxEVT_COMMAND_DATAVIEW_COLUMN_HEADER_RIGHT_CLICK, 1)
EVT_DATAVIEW_COLUMN_SORTED             = wx.PyEventBinder( wxEVT_COMMAND_DATAVIEW_COLUMN_SORTED, 1)
EVT_DATAVIEW_COLUMN_REORDERED          = wx.PyEventBinder( wxEVT_COMMAND_DATAVIEW_COLUMN_REORDERED, 1)
EVT_DATAVIEW_ITEM_BEGIN_DRAG           = wx.PyEventBinder( wxEVT_COMMAND_DATAVIEW_ITEM_BEGIN_DRAG, 1)
EVT_DATAVIEW_ITEM_DROP_POSSIBLE        = wx.PyEventBinder( wxEVT_COMMAND_DATAVIEW_ITEM_DROP_POSSIBLE, 1)      
EVT_DATAVIEW_ITEM_DROP                 = wx.PyEventBinder( wxEVT_COMMAND_DATAVIEW_ITEM_DROP, 1)
EVT_DATAVIEW_CACHE_HINT                = wx.PyEventBinder( wxEVT_COMMAND_DATAVIEW_CACHE_HINT, 1 )
    
}


//---------------------------------------------------------------------------

// help SWIG understand this template
%{
    typedef wxVector<wxVariant> wxVariantVector;
%}

// and how to convert a squence object to it
%typemap(in) wxVariantVector& (wxVariantVector temp) {
    if (! PySequence_Check($input)) {
        PyErr_SetString(PyExc_TypeError, "Sequence of data values expected");
        SWIG_fail;
    }
    Py_ssize_t size = PySequence_Length($input);
    Py_ssize_t idx;
    for (idx=0; idx<size; idx+=1) {
        PyObject* item = PySequence_GetItem($input, idx);
        temp.push_back( wxDVCVariant_in_helper(item) );
        Py_DECREF(item);
    }
    $1 = &temp;
}


// A typemap to wrap a wxPyClientData around any PyObject input value.
%typemap(in) wxClientData* {
        $1 = new wxPyClientData($input);
}

// This one extracts the PyObject from the wxPyClientData for the return value.
%typemap(out) wxClientData* {
    if (! $1)
        $result = Py_None;
    else 
        $result = ((wxPyClientData*)$1)->m_obj;
    Py_INCREF($result);
}

//---------------------------------------------------------------------------
// wxDataViewListStoreLine
// wxDataViewListStore
// wxDataViewListCtrl


class wxDataViewListStore: public wxDataViewIndexListModel
{
public:
    wxDataViewListStore();

// public:
//     wxVector<wxDataViewListStoreLine*> m_data;
//     wxArrayString                      m_cols;
};


class wxDataViewListCtrl: public wxDataViewCtrl
{
public:
    %pythonAppend wxDataViewListCtrl         "self._setOORInfo(self)"
    %pythonAppend wxDataViewListCtrl()       ""
    
    wxDataViewListCtrl( wxWindow *parent, wxWindowID id = -1,
                        const wxPoint& pos = wxDefaultPosition,
                        const wxSize& size = wxDefaultSize,
                        long style = wxDV_ROW_LINES,
                        const wxValidator& validator = wxDefaultValidator );
    %RenameCtor(PreDataViewListCtrl, wxDataViewListCtrl());

    
    bool Create( wxWindow *parent, wxWindowID id = -1,
           const wxPoint& pos = wxDefaultPosition,
           const wxSize& size = wxDefaultSize, long style = wxDV_ROW_LINES,
           const wxValidator& validator = wxDefaultValidator );

    wxDataViewListStore *GetStore();

    int ItemToRow(const wxDataViewItem &item) const;
    wxDataViewItem RowToItem(int row) const;

    int GetSelectedRow() const;
    void SelectRow(unsigned row);
    void UnselectRow(unsigned row);
    bool IsRowSelected(unsigned row) const;

    
    bool AppendColumn( wxDataViewColumn *column, const wxString &varianttype="string" );
    bool PrependColumn( wxDataViewColumn *column, const wxString &varianttype="string" );
    bool InsertColumn( unsigned int pos, wxDataViewColumn *column,
                       const wxString &varianttype="string" );

    // // overridden from base class
    // virtual bool PrependColumn( wxDataViewColumn *col );
    // virtual bool InsertColumn( unsigned int pos, wxDataViewColumn *col );
    // virtual bool AppendColumn( wxDataViewColumn *col );

    wxDataViewColumn *AppendTextColumn(
        const wxString &label,
        wxDataViewCellMode mode = wxDATAVIEW_CELL_INERT,
        int width = -1, wxAlignment align = wxALIGN_LEFT,
        int flags = wxDATAVIEW_COL_RESIZABLE );

    wxDataViewColumn *AppendToggleColumn(
        const wxString &label,
        wxDataViewCellMode mode = wxDATAVIEW_CELL_ACTIVATABLE,
        int width = -1, wxAlignment align = wxALIGN_LEFT,
        int flags = wxDATAVIEW_COL_RESIZABLE );

    wxDataViewColumn *AppendProgressColumn(
        const wxString &label,
        wxDataViewCellMode mode = wxDATAVIEW_CELL_INERT,
        int width = -1, wxAlignment align = wxALIGN_LEFT,
        int flags = wxDATAVIEW_COL_RESIZABLE );

    wxDataViewColumn *AppendIconTextColumn(
        const wxString &label,
        wxDataViewCellMode mode = wxDATAVIEW_CELL_INERT,
        int width = -1, wxAlignment align = wxALIGN_LEFT,
        int flags = wxDATAVIEW_COL_RESIZABLE );

    void AppendItem( const wxVariantVector &values, wxClientData *data = NULL );
    void PrependItem( const wxVariantVector &values, wxClientData *data = NULL );
    void InsertItem(  unsigned int row, const wxVariantVector &values,
                      wxClientData *data = NULL );

    void DeleteItem( unsigned row );
    void DeleteAllItems();

    void SetValue( const wxVariant &value, unsigned int row, unsigned int col );
    //void GetValue( wxVariant &value, unsigned int row, unsigned int col );
    %extend {
        wxVariant GetValue(unsigned int row, unsigned int col )
        {
            wxVariant value;
            self->GetValue( value, row, col);
            return value;
        }
    }

    void SetTextValue( const wxString &value, unsigned int row, unsigned int col );
    wxString GetTextValue( unsigned int row, unsigned int col ) const;

    void SetToggleValue( bool value, unsigned int row, unsigned int col );
    bool GetToggleValue( unsigned int row, unsigned int col ) const;

    
    %extend {
        PyObject* GetItemData(unsigned int row)
        {
            wxCHECK_MSG(row < self->GetStore()->m_data.size(), NULL, "Invalid row");
            wxDataViewListStoreLine* line = self->GetStore()->m_data[row];
            wxPyClientData* data = (wxPyClientData*)line->GetData();
            if (data) {
                Py_INCREF(data->m_obj);
                return data->m_obj;
            } else {
                Py_INCREF(Py_None);
                return Py_None;
            }
        }

        void SetItemData(unsigned int row, PyObject* data)
        {
            wxCHECK_RET(row < self->GetStore()->m_data.size(), "Invalid row");
            wxDataViewListStoreLine* line = self->GetStore()->m_data[row];
            delete line->GetData();
            line->SetData(new wxPyClientData(data));
        }
    }
    
};



//---------------------------------------------------------------------------
// wxDataViewTreeStoreNode
// wxDataViewTreeStoreContainerNode
// wxDataViewTreeStore
// wxDataViewTreeCtrl



class wxDataViewTreeStoreNode
{
public:
    wxDataViewTreeStoreNode( wxDataViewTreeStoreNode *parent,
                             const wxString &text,
                             const wxIcon &icon = wxNullIcon,
                             wxClientData *data = NULL );
    virtual ~wxDataViewTreeStoreNode();

    void SetText( const wxString &text );
    wxString GetText() const;
    void SetIcon( const wxIcon &icon );
    const wxIcon &GetIcon() const;
    void SetData( wxClientData *data );
    wxClientData *GetData() const;

    wxDataViewItem GetItem() const;

    virtual bool IsContainer();

    wxDataViewTreeStoreNode *GetParent();
};


wxLIST_WRAPPER(wxDataViewTreeStoreNodeList,
               wxDataViewTreeStoreNode);



class wxDataViewTreeStoreContainerNode: public wxDataViewTreeStoreNode
{
public:
    wxDataViewTreeStoreContainerNode( wxDataViewTreeStoreNode *parent,
                                      const wxString &text,
                                      const wxIcon &icon = wxNullIcon,
                                      const wxIcon &expanded = wxNullIcon,
                                      wxClientData *data = NULL );
    virtual ~wxDataViewTreeStoreContainerNode();

    const wxDataViewTreeStoreNodeList &GetChildren() const;
    wxDataViewTreeStoreNodeList &GetChildren();

    void SetExpandedIcon( const wxIcon &icon );
    const wxIcon &GetExpandedIcon() const;

    void SetExpanded( bool expanded = true );
    bool IsExpanded() const;

    virtual bool IsContainer();
};



class wxDataViewTreeStore: public wxDataViewModel
{
public:
    wxDataViewTreeStore();
    ~wxDataViewTreeStore();

    wxDataViewItem AppendItem( const wxDataViewItem& parent,
                               const wxString &text,
                               const wxIcon &icon = wxNullIcon,
                               wxClientData *data = NULL );
    wxDataViewItem PrependItem( const wxDataViewItem& parent,
                                const wxString &text,
                                const wxIcon &icon = wxNullIcon,
                                wxClientData *data = NULL );
    wxDataViewItem InsertItem( const wxDataViewItem& parent,
                               const wxDataViewItem& previous,
                               const wxString &text,
                               const wxIcon &icon = wxNullIcon,
                               wxClientData *data = NULL );

    wxDataViewItem PrependContainer( const wxDataViewItem& parent,
                                     const wxString &text,
                                     const wxIcon &icon = wxNullIcon,
                                     const wxIcon &expanded = wxNullIcon,
                                     wxClientData *data = NULL );
    wxDataViewItem AppendContainer( const wxDataViewItem& parent,
                                    const wxString &text,
                                    const wxIcon &icon = wxNullIcon,
                                    const wxIcon &expanded = wxNullIcon,
                                    wxClientData *data = NULL );
    wxDataViewItem InsertContainer( const wxDataViewItem& parent,
                                    const wxDataViewItem& previous,
                                    const wxString &text,
                                    const wxIcon &icon = wxNullIcon,
                                    const wxIcon &expanded = wxNullIcon,
                                    wxClientData *data = NULL );

    wxDataViewItem GetNthChild( const wxDataViewItem& parent, unsigned int pos ) const;
    int GetChildCount( const wxDataViewItem& parent ) const;

    void SetItemText( const wxDataViewItem& item, const wxString &text );
    wxString GetItemText( const wxDataViewItem& item ) const;
    
    void SetItemIcon( const wxDataViewItem& item, const wxIcon &icon );
    const wxIcon &GetItemIcon( const wxDataViewItem& item ) const;
    
    void SetItemExpandedIcon( const wxDataViewItem& item, const wxIcon &icon );
    const wxIcon &GetItemExpandedIcon( const wxDataViewItem& item ) const;

    void SetItemData( const wxDataViewItem& item, wxClientData *data );
    wxClientData *GetItemData( const wxDataViewItem& item ) const;

    void DeleteItem( const wxDataViewItem& item );
    void DeleteChildren( const wxDataViewItem& item );
    void DeleteAllItems();

};




class wxDataViewTreeCtrl: public wxDataViewCtrl
{
public:
    %pythonAppend wxDataViewTreeCtrl         "self._setOORInfo(self)"
    %pythonAppend wxDataViewTreeCtrl()       ""

    wxDataViewTreeCtrl( wxWindow *parent, wxWindowID id = -1,
                        const wxPoint& pos = wxDefaultPosition,
                        const wxSize& size = wxDefaultSize,
                        long style = wxDV_NO_HEADER | wxDV_ROW_LINES,
                        const wxValidator& validator = wxDefaultValidator );
    %RenameCtor(PreDataViewTreeCtrl, wxDataViewTreeCtrl());


    bool Create( wxWindow *parent, wxWindowID id = -1,
                 const wxPoint& pos = wxDefaultPosition,
                 const wxSize& size = wxDefaultSize,
                 long style = wxDV_NO_HEADER | wxDV_ROW_LINES,
                 const wxValidator& validator = wxDefaultValidator );

    wxDataViewTreeStore *GetStore();
    bool IsContainer( const wxDataViewItem& item ) const;

    %disownarg( wxImageList *imagelist );
    void SetImageList( wxImageList *imagelist );
    %cleardisown( wxImageList *imageList );

    wxImageList* GetImageList();

    wxDataViewItem AppendItem( const wxDataViewItem& parent,
                               const wxString &text,
                               int icon = -1,
                               wxClientData *data = NULL );
    wxDataViewItem PrependItem( const wxDataViewItem& parent,
                                const wxString &text,
                                int icon = -1,
                                wxClientData *data = NULL );
    wxDataViewItem InsertItem( const wxDataViewItem& parent,
                               const wxDataViewItem& previous,
                               const wxString &text,
                               int icon = -1,
                               wxClientData *data = NULL );

    wxDataViewItem PrependContainer( const wxDataViewItem& parent,
                                     const wxString &text,
                                     int icon = -1,
                                     int expanded = -1,
                                     wxClientData *data = NULL );
    wxDataViewItem AppendContainer( const wxDataViewItem& parent,
                                    const wxString &text,
                                    int icon = -1,
                                    int expanded = -1,
                                    wxClientData *data = NULL );
    wxDataViewItem InsertContainer( const wxDataViewItem& parent,
                                    const wxDataViewItem& previous,
                                    const wxString &text,
                                    int icon = -1,
                                    int expanded = -1,
                                    wxClientData *data = NULL );

    wxDataViewItem GetNthChild( const wxDataViewItem& parent, unsigned int pos ) const;
    int GetChildCount( const wxDataViewItem& parent ) const;

    void SetItemText( const wxDataViewItem& item, const wxString &text );
    wxString GetItemText( const wxDataViewItem& item ) const;
    
    void SetItemIcon( const wxDataViewItem& item, const wxIcon &icon );
    const wxIcon &GetItemIcon( const wxDataViewItem& item ) const;
    
    void SetItemExpandedIcon( const wxDataViewItem& item, const wxIcon &icon );
    const wxIcon &GetItemExpandedIcon( const wxDataViewItem& item ) const;
    
    void SetItemData( const wxDataViewItem& item, wxClientData *data );
    wxClientData *GetItemData( const wxDataViewItem& item ) const;

    void DeleteItem( const wxDataViewItem& item );
    void DeleteChildren( const wxDataViewItem& item );
    void DeleteAllItems();

};



//---------------------------------------------------------------------------

%init %{
%}

//---------------------------------------------------------------------------
