/////////////////////////////////////////////////////////////////////////////
// Name:        propgrid.i
// Purpose:     Wrappers for wxPropertyGrid.
//
// Author:      Jaakko Salli
//
// Created:     17-Feb-2005
// RCS-ID:      $Id$
// Copyright:   (c) Jaakko Salli
// Licence:     wxWindows license
/////////////////////////////////////////////////////////////////////////////

%define DOCSTRING
"The `PropertyGrid` provides a specialized grid for editing
properties such as strings, numbers, colours, and string lists."
%enddef

%module(package="wx", docstring=DOCSTRING) propgrid

%{

#include "wx/wxPython/wxPython.h"
#include "wx/wxPython/pyclasses.h"

#include <wx/propgrid/propgriddefs.h>
#include <wx/propgrid/property.h>
#include <wx/propgrid/props.h>
#include <wx/propgrid/propgridiface.h>
#include <wx/propgrid/propgrid.h>
#include <wx/propgrid/advprops.h>
#include <wx/propgrid/manager.h>
#include <wx/propgrid/editors.h>

#include <wx/editlbox.h>
#include <wx/listctrl.h>

#if !defined(__WXMSW__) && !defined(OutputDebugString)
  #define OutputDebugString(A)
#endif

// Change to '#if 1' inorder to add debug messages from build
#if 0
  #define MySWIGOutputDebugString OutputDebugString
#else
  #define MySWIGOutputDebugString(A)
#endif

#ifndef Py_RETURN_NONE
    #define Py_RETURN_NONE return Py_INCREF(Py_None), Py_None
#endif

//
// wxVariant PyObject container

class wxPGVariantDataPyObject : public wxVariantData
{
protected:
    PyObject* m_value;
public:
    wxPGVariantDataPyObject()
    {
        m_value = NULL;
    }
    wxPGVariantDataPyObject( PyObject* value )
    {
        if (!value) value = Py_None;
        Py_INCREF(value);
        m_value = value;
    }
    virtual ~wxPGVariantDataPyObject()
    {
        // Avoid crashing on program exit
        if ( _PyThreadState_Current != NULL && m_value )
            Py_DECREF(m_value);
    }
    inline PyObject* GetValue() const { return m_value; }
    inline PyObject* GetValueRef() const { return m_value; }
    inline void SetValue(PyObject* value)
    {
        if (m_value)
            Py_DECREF(m_value);
        if (!value) value = Py_None;
        Py_INCREF(value);
        m_value = value;
    }
    // TODO
    virtual bool Eq(wxVariantData&) const { return false; }
    virtual wxString GetType() const { return wxS("PyObject*"); }
    virtual wxVariantData* Clone() { return new wxPGVariantDataPyObject(); }
    virtual bool Read(wxString &) { return false; }
    virtual bool Write(wxString &) const { return true; }
    virtual wxVariant GetDefaultValue() const
    {
        return wxVariant( new wxPGVariantDataPyObject(NULL) );
    }
public:
    virtual void* GetValuePtr() { return (void*)m_value; }
};

PyObject* operator <<( PyObject* value, const wxVariant &variant )
{
	wxPGVariantDataPyObject *data =
        wxDynamicCastVariantData( variant.GetData(), wxPGVariantDataPyObject );
    wxASSERT( data );
    value = data->GetValue();
    Py_INCREF(value);
    return value;
}

wxVariant& operator <<( wxVariant &variant, PyObject* value )
{
    wxPGVariantDataPyObject *data = new wxPGVariantDataPyObject( value );
    variant.SetData( data );
    return variant;
}

PyObject* PyObjectPtrFromVariant( const wxVariant& v )
{
	wxPGVariantDataPyObject *data =
        wxDynamicCastVariantData( v.GetData(), wxPGVariantDataPyObject );
    if ( !data )
        return NULL;
    PyObject* retval = data->GetValue();
    Py_INCREF(retval);
    return retval;
}

wxVariant PyObjectToVariant( PyObject* value )
{
    wxVariant variant( new wxPGVariantDataPyObject( value ) );
    return variant;
}


wxPGProperty* NewPropertyCategory( const wxString& label,
                                   const wxString& name )
{
    return new wxPropertyCategory( label, name );
}

wxPGProperty* NewStringProperty( const wxString& label, const wxString& name,
                                 const wxString& value )
{
    return new wxStringProperty( label, name, value );
}

wxPGProperty* NewIntProperty( const wxString& label, const wxString& name,
                              long value )
{
    return new wxIntProperty( label, name, value );
}

wxPGProperty* NewUIntProperty( const wxString& label, const wxString& name,
                               unsigned long value )
{
    return new wxUIntProperty( label, name, value );
}

wxPGProperty* NewFloatProperty( const wxString& label, const wxString& name,
                                double value )
{
    return new wxFloatProperty( label, name, value );
}

wxPGProperty* NewBoolProperty( const wxString& label, const wxString& name,
                               bool value )
{
    return new wxBoolProperty( label, name, value );
}

wxPGProperty* NewEnumProperty( const wxString& label, const wxString& name,
        const wxArrayString& labels, const wxArrayInt& values,
        int value )
{
    return new wxEnumProperty( label, name, labels, values, value );
}

wxPGProperty* NewEditEnumProperty( const wxString& label, const wxString& name,
        const wxArrayString& labels, const wxArrayInt& values,
        const wxString& value )
{
    return new wxEditEnumProperty( label, name, labels, values, value );
}

wxPGProperty* NewFlagsProperty( const wxString& label, const wxString& name,
        const wxArrayString& labels, const wxArrayInt& values,
        int value )
{
    return new wxFlagsProperty( label, name, labels, values, value );
}

wxPGProperty* NewFileProperty( const wxString& label, const wxString& name,
                               const wxString& value )
{
    return new wxFileProperty( label, name, value );
}

wxPGProperty* NewLongStringProperty( const wxString& label,
                                     const wxString& name,
                                     const wxString& value )
{
    return new wxLongStringProperty( label, name, value );
}

wxPGProperty* NewDirProperty( const wxString& label, const wxString& name,
                              const wxString& value )
{
    return new wxDirProperty( label, name, value );
}

wxPGProperty* NewArrayStringProperty( const wxString& label,
                                      const wxString& name,
                                      const wxArrayString& value )
{
    return new wxArrayStringProperty( label, name, value );
}

wxPGProperty* NewFontProperty( const wxString& label, const wxString& name,
                               const wxFont& value )
{
    return new wxFontProperty( label, name, value );
}

wxPGProperty* NewSystemColourProperty( const wxString& label,
                            const wxString& name,
                            const wxColourPropertyValue& value )
{
    return new wxSystemColourProperty( label, name, value );
}

wxPGProperty* NewColourProperty( const wxString& label,
                            const wxString& name,
                            const wxColour& value )
{
    return new wxColourProperty( label, name, value );
}

wxPGProperty* NewCursorProperty( const wxString& label,
                      const wxString& name,
                      int value )
{
    return new wxCursorProperty( label, name, value );
}

wxPGProperty* NewImageFileProperty( const wxString& label,
                         const wxString& name,
                         const wxString& value )
{
    return new wxImageFileProperty( label, name, value );
}

wxPGProperty* NewMultiChoiceProperty( const wxString& label,
                           const wxString& name,
                           const wxArrayString& choices,
                           const wxArrayString& value )
{
    return new wxMultiChoiceProperty( label, name, choices, value );
}

wxPGProperty* NewDateProperty( const wxString& label,
                    const wxString& name,
                    const wxDateTime& value )
{
    return new wxDateProperty( label, name, value );
}
#if 0
wxPGProperty* NewFontDataProperty( const wxString& label,
                    const wxString& name,
                    const wxFontData& value )
{
    return new wxFontDataProperty( label, name, value );
}

wxPGProperty* NewSizeProperty( const wxString& label, const wxString& name,
                    const wxSize& value )
{
    return new wxSizeProperty( label, name, value );
}

wxPGProperty* NewPointProperty( const wxString& label, const wxString& name,
                 const wxPoint& value )
{
    return new wxPointProperty( label, name, value );
}

wxPGProperty* NewDirsProperty( const wxString& label, const wxString& name,
                               const wxArrayString& value )
{
    return new wxDirsProperty( label, name, value );
}

wxPGProperty* NewArrayDoubleProperty( const wxString& label,
                           const wxString& name,
                           const wxArrayDouble& value )
{
    return new wxArrayDoubleProperty( label, name, value );
}
#endif

void RegisterEditor( wxPGEditor* editor, const wxString& editorName )
{
    wxPropertyGrid::DoRegisterEditorClass(editor, editorName);
}

#include <datetime.h>

bool PyObject_to_wxVariant( PyObject* input, wxVariant* v )
{
    PyDateTime_IMPORT;

    if ( input == Py_None )
    {
        v->MakeNull();
        return true;
    }
    else if ( PyBool_Check(input) )
    {
        *v = (bool) PyInt_AsLong(input);
        return true;
    }
    else if ( PyInt_Check(input) )
    {
        *v = (long) PyInt_AsLong(input);
        return true;
    }
    else if ( PyString_Check(input) || PyUnicode_Check(input) )
    {
        wxString* sptr = wxString_in_helper(input);
        if (sptr == NULL) return false;
        *v = *sptr;
        delete sptr;
        return true;
    }
    else if ( PyFloat_Check(input) )
    {
        *v = PyFloat_AsDouble(input);
        return true;
    }
    else if ( PyDate_Check(input) )
    {
        // Both date and datetime have these
        int year = PyDateTime_GET_YEAR(input);
        // Month is enumeration, make sure to match its first entry
        int month = PyDateTime_GET_MONTH(input) - 1 + (int) wxDateTime::Jan;
        int day = PyDateTime_GET_DAY(input);

        // Only datetime.datetime has the following
        int hour = 0;
        int minute = 0;
        int second = 0;
        int microsecond = 0;
        if ( PyDateTime_Check(input) )
        {
            hour = PyDateTime_DATE_GET_HOUR(input);
            minute = PyDateTime_DATE_GET_MINUTE(input);
            second = PyDateTime_DATE_GET_SECOND(input);
            microsecond = PyDateTime_DATE_GET_MICROSECOND(input);
        }

        wxDateTime wx_dateTime(day, (wxDateTime::Month)month, year,
                               hour, minute, second,
                               microsecond/1000);  // wx uses milliseconds
        *v = wx_dateTime;
        return true;
    }
    else if ( PyTuple_CheckExact(input) || PyList_CheckExact(input) )
    {
        int len = PySequence_Length(input);

        if ( len )
        {
            int i;
            PyObject* item = PySequence_GetItem(input, 0);
            bool failed = false;
            if ( PyString_CheckExact(item) || PyUnicode_CheckExact(item) )
            {
                wxArrayString arr;
                for (i=0; i<len; i++)
                {
                    item = PySequence_GetItem(input, i);
                    wxString* s = wxString_in_helper(item);
                    if ( PyErr_Occurred() )
                    {
                        delete s;
                        failed = true;
                        break;
                    }
                    arr.Add(*s);
                    delete s;
                    Py_DECREF(item);
                }

                if ( !failed )
                {
                    *v = arr;
                    return true;
                }
            }
            else if ( PyInt_CheckExact(item) || PyLong_CheckExact(item) )
            {
                wxArrayInt arr;
                for (i=0; i<len; i++)
                {
                    item = PySequence_GetItem(input, i);
                    long val;
                    if ( PyInt_CheckExact(item) )
                    {
                        val = PyInt_AS_LONG(item);
                    }
                    else if ( PyLong_CheckExact(item) )
                    {
                        val = PyLong_AsLong(item);
                    }
                    else
                    {
                        failed = true;
                        break;
                    }
                    arr.Add(val);
                    Py_DECREF(item);
                }

                if ( !failed )
                {
                    *v = WXVARIANT(arr);
                    return true;
                }
            }
        }
        else
        {
            *v = wxArrayString();
            return true;
        }
    }
    else if ( wxPySwigInstance_Check(input) )
    {
        // First try if it is a wxColour
        wxColour* col_ptr;
        if ( wxPyConvertSwigPtr(input, (void **)&col_ptr, wxS("wxColour")))
        {
            *v << *col_ptr;
            return true;
        }

        // Then wxPoint
        wxPoint* pt_ptr;
        if ( wxPyConvertSwigPtr(input, (void **)&pt_ptr, wxS("wxPoint")))
        {
            *v << *pt_ptr;
            return true;
        }

        // Then wxSize
        wxSize* sz_ptr;
        if ( wxPyConvertSwigPtr(input, (void **)&sz_ptr, wxS("wxSize")))
        {
            *v << *sz_ptr;
            return true;
        }

        // Then wxFont
        wxFont* font_ptr;
        if ( wxPyConvertSwigPtr(input, (void **)&font_ptr, wxS("wxFont")))
        {
            *v << *font_ptr;
            return true;
        }

        // Then wxColourPropertyValue
        wxColourPropertyValue* cpv_ptr;
        if ( wxPyConvertSwigPtr(input, (void **)&cpv_ptr,
                                wxS("wxColourPropertyValue")))
        {
            *v << *cpv_ptr;
            return true;
        }
    }

    //Py_TrackObject(input);
    // Last ditch - let's convert it to a wxVariant containing an arbitrary
    // PyObject
    wxVariant tempVariant = PyObjectToVariant(input);
    wxVariantData* vd = tempVariant.GetData();
    vd->IncRef();
    v->SetData(vd);

    return true;
}

PyObject* wxVariant_to_PyObject( const wxVariant* v )
{
    if ( !v || v->IsNull() )
        Py_RETURN_NONE;

    wxString variantType = v->GetType();
    //printf("%s\n", variantType.c_str());
    //OutputDebugString(variantType.c_str());
    if ( variantType == wxS("long") )
    {
        return PyInt_FromLong(v->GetLong());
    }
    else if ( variantType == wxS("string") )
    {
        wxString _wxvar_str = v->GetString();
#if wxUSE_UNICODE
        return PyUnicode_FromWideChar(_wxvar_str.c_str(), _wxvar_str.Len());
#else
        return PyString_FromStringAndSize(_wxvar_str.c_str(), _wxvar_str.Len());
#endif
    }
    else if ( variantType == wxS("double") )
    {
        return PyFloat_FromDouble(v->GetDouble());
    }
    else if ( variantType == wxS("bool") )
    {
        return PyBool_FromLong((long)v->GetBool());
    }
    else if ( variantType == wxS("arrstring") )
    {
        wxArrayString arr = v->GetArrayString();
        PyObject* list = PyList_New(arr.GetCount());
        unsigned int i;

        for ( i=0; i<arr.GetCount(); i++ )
        {
            const wxString& str = arr.Item(i);
    #if wxUSE_UNICODE
            PyObject* item = PyUnicode_FromWideChar
            (str.c_str(), str.Len());
    #else
            PyObject* item = PyString_FromStringAndSize(str.c_str(), str.Len());
    #endif

            // PyList_SetItem steals reference, so absence of Py_DECREF is ok
            PyList_SetItem(list, i, item);
        }

        return list;
    }
    else if ( variantType == wxS("wxArrayInt") )
    {
        const wxArrayInt& arr = wxArrayIntRefFromVariant(*v);
        PyObject* list = PyList_New(arr.GetCount());
        unsigned int i;

        for ( i=0; i<arr.GetCount(); i++ )
        {
            PyObject* item = PyInt_FromLong((long)arr.Item(i));
            // PyList_SetItem steals reference, so absence of Py_DECREF is ok
            PyList_SetItem(list, i, item);
        }

        return list;
    }
    else if ( variantType == wxS("datetime") )
    {
        wxDateTime dt = v->GetDateTime();
        int year = dt.GetYear();
        // Month is enumeration, make sure to match its first entry
        int month = dt.GetMonth() + 1 - (int) wxDateTime::Jan;
        int day = dt.GetDay();
        int hour = dt.GetHour();
        int minute = dt.GetMinute();
        int second = dt.GetSecond();
        int millisecond = dt.GetMillisecond();
        return PyDateTime_FromDateAndTime(year, month, day,
                                          hour, minute, second,
                                          millisecond*1000);
    }
    else if ( variantType == wxS("wxColour") )
    {
        wxColour col;
        col << *v;
        return SWIG_NewPointerObj(SWIG_as_voidptr(new wxColour(col)),
                                  SWIGTYPE_p_wxColour,
                                  SWIG_POINTER_OWN | 0 );
    }
    else if ( variantType == wxS("wxPoint") )
    {
        const wxPoint& point = wxPointRefFromVariant(*v);
        return SWIG_NewPointerObj(SWIG_as_voidptr(new wxPoint(point)),
                                  SWIGTYPE_p_wxPoint,
                                  SWIG_POINTER_OWN | 0 );
    }
    else if ( variantType == wxS("wxSize") )
    {
        const wxSize& size = wxSizeRefFromVariant(*v);
        return SWIG_NewPointerObj(SWIG_as_voidptr(new wxSize(size)),
                                  SWIGTYPE_p_wxSize,
                                  SWIG_POINTER_OWN | 0 );
    }
    else if ( variantType == wxS("PyObject*") )
    {
        // PyObjectPtrFromVariant already increments the reference count
        PyObject* o = PyObjectPtrFromVariant(*v);
        //Py_TrackObject(o);
        if ( !o )
            Py_RETURN_NONE;
        return o;
    }
    else if ( variantType == wxS("wxFont") )
    {
        wxFont font;
        font << *v;
        return SWIG_NewPointerObj(SWIG_as_voidptr(new wxFont(font)),
                                  SWIGTYPE_p_wxFont,
                                  SWIG_POINTER_OWN | 0 );
    }
    else if ( variantType == wxS("wxColourPropertyValue") )
    {
        wxColourPropertyValue cpv;
        cpv << *v;
        return
            SWIG_NewPointerObj(SWIG_as_voidptr(new wxColourPropertyValue(cpv)),
                               SWIGTYPE_p_wxColourPropertyValue,
                               SWIG_POINTER_OWN | 0 );
    }
    else
    {
        // TODO: Allow converting arbitrary wxObject-based variant datas,
        // including old-school wxObjectPtr (see wxPG 1.4), and new-style
        // variant data classes generated using DECLARE_VARIANT_OBJECT().
    }

    return NULL;
}

//
// wxPGVariantAndBool
//
// Helper class that wraps wxVariant and bool. Need to use this class
// instead of "writeback" arguments in some virtual methods of custom
// property classes (for some reason I couldn't get SWIG INOUT working.
// Actually, even trivial int* OUTPUT failed).
//
class wxPGVariantAndBool
{
public:

    wxPGVariantAndBool()
    {
        m_valueValid = false;
        m_result = false;
    }

    wxPGVariantAndBool( bool result, const wxVariant& variant )
    {
        m_valueValid = true;
        m_result = result;
        m_value = variant;
    }

    wxPGVariantAndBool( const wxVariant& variant )
    {
        m_valueValid = true;
        m_result = true;
        m_value = variant;
    }

    wxPGVariantAndBool( bool result )
    {
        Init(result);
    }

    ~wxPGVariantAndBool() { }

    void Init( bool result = false )
    {
        m_valueValid = false;
        m_result = result;
    }

    const wxVariant& GetValue() const
    {
        wxASSERT(m_valueValid);
        return m_value;
    }

public:
    wxVariant m_value;
    bool      m_valueValid;
    bool      m_result;
};

PyObject* wxPGVariantAndBool_to_PyObject( const wxPGVariantAndBool& vab )
{
    PyObject* tuple = PyTuple_New(2);

    PyObject* value;
    if ( vab.m_valueValid )
    {
        value = wxVariant_to_PyObject(&vab.m_value);
    }
    else
    {
        Py_INCREF(Py_None);
        value = Py_None;
    }

    PyTuple_SetItem(tuple, 0, PyInt_FromLong((long)vab.m_result));
    PyTuple_SetItem(tuple, 1, value);

    return tuple;
}

bool PyObject_to_wxPGVariantAndBool( PyObject* input,
                                     wxPGVariantAndBool& vab )
{
    PyObject* resObj = NULL;
    PyObject* valueObj = NULL;

    if ( PySequence_Check(input) && PySequence_Length(input) == 2 )
    {
        resObj = PySequence_GetItem(input, 0);
        if (PyErr_Occurred()) return false;
        valueObj = PySequence_GetItem(input, 1);
        if (PyErr_Occurred()) return false;
    }
    else
    {
        resObj = input;
    }

    // Also checks for bool, which is subclass of int
    if ( PyInt_Check(resObj) )
    {
        vab.Init((bool) PyInt_AsLong(resObj));
    }
    else if ( PyLong_Check(resObj) )
    {
        vab.Init((bool) PyLong_AsLong(resObj));
    }
    else
    {
        return false;
    }

    if ( valueObj )
    {
        // If valueObj is valid, then we can assume resObj was acquired from
        // sequence and must be decref'ed.
        Py_DECREF(resObj);

        if ( PyObject_to_wxVariant(valueObj, &vab.m_value) )
            vab.m_valueValid = true;
        else
            return false;

        Py_DECREF(valueObj);
    }

    return true;
}

bool PyObject_to_wxPGPropArgCls( PyObject* input, wxPGPropArgCls** v )
{
    if ( PyString_Check(input) || PyUnicode_Check(input) )
    {
        wxString* sptr = wxString_in_helper(input);
        if (sptr == NULL) return false;
        *v = new wxPGPropArgCls(sptr, true);
    }
    else if ( input == Py_None )
    {
        *v = new wxPGPropArgCls(reinterpret_cast< wxPGProperty * >(NULL));
    }
    else
    {
        void* valp;
        int res = SWIG_ConvertPtr(input, &valp,
                                  SWIGTYPE_p_wxPGProperty,
                                  0  | 0);
        if ( !SWIG_IsOK(res) ) return false;
        *v = new wxPGPropArgCls(reinterpret_cast< wxPGProperty * >(valp));
    }

    return true;
}

PyObject* wxPGPropArgCls_to_PyObject( const wxPGPropArgCls& v )
{
    if ( v.HasName() )
    {
        const wxString& _wxvar_str = v.GetName();
#if wxUSE_UNICODE
        return PyUnicode_FromWideChar(_wxvar_str.c_str(), _wxvar_str.Len());
#else
        return PyString_FromStringAndSize(_wxvar_str.c_str(), _wxvar_str.Len());
#endif
    }

    wxPGProperty* p = v.GetPtr();

    if ( !p )
        Py_RETURN_NONE;

    return SWIG_NewPointerObj(SWIG_as_voidptr(p),
                              SWIGTYPE_p_wxPGProperty,
                              0 |  0 );
}

PyObject* wxPGAttributeStorage_to_PyObject( const wxPGAttributeStorage* attrs )
{
    wxPGAttributeStorage::const_iterator it = attrs->StartIteration();
    wxVariant v;

    PyObject* dict = PyDict_New();
    if ( !dict ) return dict;

    while ( attrs->GetNext( it, v ) )
    {
        const wxString& name = v.GetName();
#if wxUSE_UNICODE
        PyObject* pyStr = PyUnicode_FromWideChar(name.c_str(), name.Len());
#else
        PyObject* pyStr = PyString_FromStringAndSize(name.c_str(), name.Len());
#endif
        PyObject* pyVal = wxVariant_to_PyObject(&v);
        int res = PyDict_SetItem( dict, pyStr, pyVal );
    }

    return dict;
}

PyObject* wxPoint_to_PyObject( const wxPoint* p )
{
    if ( p->x == -1 || p->y == -1 )
        Py_RETURN_NONE;

    PyObject* tuple = PyTuple_New(2);
    // PyTuple_SetItem steals reference, so absence of Py_DECREF is ok
    PyTuple_SetItem(tuple, 0, PyInt_FromLong(p->x));
    PyTuple_SetItem(tuple, 1, PyInt_FromLong(p->y));
    return tuple;
}

PyObject* wxSize_to_PyObject( const wxSize* p )
{
    if ( p->x == -1 || p->y == -1 )
        Py_RETURN_NONE;

    PyObject* tuple = PyTuple_New(2);
    // PyTuple_SetItem steals reference, so absence of Py_DECREF is ok
    PyTuple_SetItem(tuple, 0, PyInt_FromLong(p->x));
    PyTuple_SetItem(tuple, 1, PyInt_FromLong(p->y));
    return tuple;
}

PyObject* wxPGWindowList_to_PyObject( const wxPGWindowList* p )
{
    PyObject* o1 = NULL;
    PyObject* o2 = NULL;

    if ( p->m_primary )
        o1 = wxPyMake_wxObject(p->m_primary, false);

    if ( p->m_secondary )
        o2 = wxPyMake_wxObject(p->m_secondary, false);

    if ( o1 )
    {
        if ( o2 )
        {
            PyObject* tuple = PyTuple_New(2);
            // PyTuple_SetItem steals reference, so absence of Py_DECREF is ok
            PyTuple_SetItem(tuple, 0, o1);
            PyTuple_SetItem(tuple, 1, o2);
            return tuple;
        }
        else
        {
            return o1;
        }
    }

    Py_RETURN_NONE;
}

bool PyObject_to_wxPGWindowList( PyObject* o, wxPGWindowList* p )
{
    if ( PySequence_Check(o) )
    {
        if ( PySequence_Size(o) != 2 )
            return false;

        bool res;

        PyObject* m1 = PySequence_GetItem(o, 0);
        res = wxPyConvertSwigPtr(m1, (void **)&p->m_primary, wxS("wxWindow"));
        Py_DECREF(m1);
        if ( !res )
            return false;

        PyObject* m2 = PySequence_GetItem(o, 1);
        res = wxPyConvertSwigPtr(m2, (void **)&p->m_secondary,
                                 wxS("wxWindow"));
        Py_DECREF(m2);
        if ( !res )
            return false;

        return true;
    }

    p->m_secondary = NULL;

    if ( !wxPyConvertSwigPtr(o, (void **)&p->m_primary, wxS("wxWindow")) )
        return false;

    return true;
}

%}

%import core.i
%import windows.i

%pythoncode { wx = _core }
%pythoncode { __docfilter__ = wx.__DocFilter(globals()) }

//---------------------------------------------------------------------------

// Preprocessor stuff so SWIG doesn't get confused when %include-ing
// the .h files.
#define WXDLLIMPEXP_PROPGRID
#define WXDLLIMPEXP_FWD_CORE
#define WXDLLIMPEXP_FWD_ADV
#define WXDLLIMPEXP_FWD_PROPGRID
#define WXDLLIMPEXP_DATA_PROPGRID(decl) decl

%ignore wxUSE_PROPGRID;
%ignore wxABI_VERSION;
#ignore wxUSE_BMPBUTTON;
#ignore wxUSE_CHOICEDLG;
%ignore wxUSE_DATEPICKCTRL;
#ignore wxUSE_DATETIME;
%ignore wxUSE_IMAGE;
%ignore wxUSE_LONGLONG_NATIVE;
%ignore wxUSE_SPINBTN;
%ignore wxUSE_EDITABLELISTBOX;
%ignore wxUSE_STL;
%ignore wxUSE_THREADS;
%ignore wxUSE_TOOLBAR;
%ignore wxUSE_TOOLTIPS;
%ignore wxUSE_VALIDATORS;
%ignore wxUSE_WCHAR_T;
#define wxUSE_PROPGRID 1
#define wxABI_VERSION 99999
#ignore wxUSE_BMPBUTTON 1
#ignore wxUSE_CHOICEDLG 1
#define wxUSE_DATEPICKCTRL 1
#ignore wxUSE_DATETIME 1
#define wxUSE_IMAGE 1
#define wxUSE_LONGLONG_NATIVE 1
#define wxUSE_SPINBTN 1
#define wxUSE_EDITABLELISTBOX 1
#define wxUSE_STL 0
#define wxUSE_TOOLBAR 1
#define wxUSE_TOOLTIPS 1
#define wxUSE_VALIDATORS 1
#define wxUSE_WCHAR_T 0

#define unsigned
#define wxDEPRECATED(decl)
#define DECLARE_EVENT_TABLE()
#define DECLARE_CLASS(foo)
#define DECLARE_DYNAMIC_CLASS(foo)
#define DECLARE_DYNAMIC_CLASS_NO_ASSIGN(foo)
#define DECLARE_DYNAMIC_CLASS_NO_COPY(foo)
#define DECLARE_ABSTRACT_CLASS(foo)
#define WX_DEFINE_TYPEARRAY_WITH_DECL_PTR(a, b, c, d)
#define WX_DECLARE_STRING_HASH_MAP_WITH_DECL(a, b, c)
#define WX_DECLARE_VOIDPTR_HASH_MAP_WITH_DECL(a, b, c)
#define WX_DECLARE_HASH_MAP_WITH_DECL(a, b, c, d, e, f)

// Some classes, functions and variables we want to ignore completely
%ignore wxPGGlobalVarsClass;
%ignore wxPGGlobalVars;
%ignore wxPGInitResourceModule;

// Some functions that we do not want SWIG to know about
// TODO: Add more here and remove respective #ifndef SWIG from .h files
%ignore wxPropertyGridIterator::operator++;
%ignore wxPropertyGridIterator::operator--;
%ignore wxPropertyGridIterator::operator=;
%ignore wxPropertyGridIterator::operator *();
%ignore wxPropertyGridConstIterator::operator++;
%ignore wxPropertyGridConstIterator::operator--;
%ignore wxPropertyGridConstIterator::operator=;
%ignore wxPropertyGridConstIterator::operator *();
%ignore wxPGVIterator::operator=;

// propgriddefs.h
%ignore wxPG_LABEL;
%ignore wxPG_LABEL_STRING;
%ignore wxPG_NULL_BITMAP;
%ignore wxPG_COLOUR_BLACK;
%ignore DECLARE_VARIANT_OBJECT_EXPORTED;
#define DECLARE_VARIANT_OBJECT_EXPORTED(a, b)
%ignore WX_PG_DECLARE_EDITOR_WITH_DECL;
#define WX_PG_DECLARE_EDITOR_WITH_DECL(a, b)
%ignore wxPGStringTokenizer;

// property.h
%ignore wxPGCellRenderer;
%ignore wxPGDefaultRenderer;
%ignore wxPGCellData;
%ignore wxPGCell::operator=;
%ignore wxPGAttributeStorage;
%ignore wxPGChoiceEntry;
%ignore wxPGChoicesData;
%ignore wxPGChoices::operator=;
%ignore wxPGChoices::operator[];
%ignore wxPGProperty::ValidateValue;
%ignore wxPGProperty::StringToValue;
%ignore wxPGProperty::IntToValue;
%ignore wxPGProperty::GetValueRef;
%ignore wxPGProperty::SetEditor(const wxPGEditor*);
%ignore wxPGProperty::SetChoices;
%ignore wxPGProperty::GetClientData;
%ignore wxPGProperty::SetClientData;
%ignore wxPGProperty::GetClientObject;
%ignore wxPGProperty::SetClientObject;
%ignore wxPGProperty::GetParentState;
%ignore wxPGProperty::GetItemAtY(unsigned int, unsigned int, unsigned int*) const;
%ignore wxPGProperty::GetDisplayInfo;
%ignore wxPGProperty::sm_wxPG_LABEL;
%ignore wxPGProperty::m_clientData;
%ignore WX_PG_DECLARE_PROPERTY_CLASS;
#define WX_PG_DECLARE_PROPERTY_CLASS(a)
%ignore wxPGRootProperty;
%ignore wxPropertyCategory;

// editors.h
%ignore wxPGWindowList::wxPGWindowList(wxWindow*);
%ignore wxPGWindowList::wxPGWindowList(wxWindow*, wxWindow*);
%ignore wxPGEditor::GetValueFromControl;
%ignore wxPGChoiceAndButtonEditor;
%ignore wxPGTextCtrlAndButtonEditor;
%ignore wxPGCheckBoxEditor;

// propgridpagestate.h
%ignore wxPGVIterator::operator=;
%ignore wxPropertyGridPageState;

// propgridiface.h
%ignore wxPGPropArgCls;
%ignore wxPropertyGridInterface::GetPropertyClientData;
%ignore wxPropertyGridInterface::GetPropertyValueAsInt;
%ignore wxPropertyGridInterface::GetPropertyValues;
%ignore wxPropertyGridInterface::GetState;
%ignore wxPropertyGridInterface::SetPropertyClientData;
%ignore wxPropertyGridInterface::SetPropertyEditor(wxPGPropArg, const wxPGEditor*);
%ignore wxPropertyGridInterface::SetPropertyValues;
%ignore wxPropertyGridInterface::SetPropertyValue(wxPGPropArg id, long);
%ignore wxPropertyGridInterface::SetPropertyValue(wxPGPropArg id, int);
%ignore wxPropertyGridInterface::SetPropertyValue(wxPGPropArg id, bool);
%ignore wxPropertyGridInterface::SetPropertyValue(wxPGPropArg id, double);
%ignore wxPropertyGridInterface::SetPropertyValue(wxPGPropArg id, const wchar_t*);
%ignore wxPropertyGridInterface::SetPropertyValue(wxPGPropArg id, const char*);
%ignore wxPropertyGridInterface::SetPropertyValue(wxPGPropArg id, const wxString&);
%ignore wxPropertyGridInterface::SetPropertyValue(wxPGPropArg id, const wxArrayString&);
%ignore wxPropertyGridInterface::SetPropertyValue(wxPGPropArg id, const wxDateTime&);
%ignore wxPropertyGridInterface::SetPropertyValue(wxPGPropArg id, wxObject*);
%ignore wxPropertyGridInterface::SetPropertyValue(wxPGPropArg id, wxObject&);
%ignore wxPropertyGridInterface::SetPropertyValue(wxPGPropArg id, wxLongLong_t);
%ignore wxPropertyGridInterface::SetPropertyValue(wxPGPropArg id, wxULongLong_t);
%ignore wxPropertyGridInterface::SetPropertyValue(wxPGPropArg id, const wxArrayInt&);
%ignore wxPropertyGridInterface::SetPropVal;

// propgrid.h
%ignore wxPropertyGrid::RegisterEditorClass;
%ignore wxPropertyGrid::DoRegisterEditorClass;
%ignore wxPropertyGrid::ArrayStringToString;
%ignore wxPropertyGrid::SwitchState;
%ignore wxPropertyGrid::IncFrozen;
%ignore wxPropertyGrid::DecFrozen;
%ignore wxPropertyGrid::OnComboItemPaint;
%ignore wxPropertyGrid::DoPropertyChanged;
%ignore wxPropertyGrid::OnValidationFailure;
%ignore wxPropertyGrid::OnValidationFailureReset;
%ignore wxPropertyGrid::DoShowPropertyError;
%ignore wxPropertyGrid::DoOnValidationFailure;
%ignore wxPropertyGrid::DoOnValidationFailureReset;
%ignore wxPropertyGrid::SetWindowStyleFlag;
%ignore wxPropertyGrid::DrawItems;
%ignore wxPropertyGrid::DrawItem;
%ignore wxPropertyGrid::DrawItemAndChildren;
%ignore wxPropertyGrid::DrawItemAndValueRelated;
%ignore wxPropertyGrid::SetCurControlBoldFont;
%ignore wxPropertyGrid::DoSelectProperty;
%ignore wxPropertyGrid::Destroy;
%ignore wxPropertyGrid::Refresh;
%ignore wxPropertyGrid::SetFont;
%ignore wxPropertyGrid::SetToolTip;
%ignore wxPropertyGrid::Freeze;
%ignore wxPropertyGrid::Thaw;
%ignore wxPropertyGrid::Reparent;
%ignore wxPropertyGrid::SetExtraStyle;
%ignore wxPropertyGridEvent::wxPropertyGridEvent(const wxPropertyGridEvent&);
%ignore wxPropertyGridEvent::GetValidationFailureBehavior;
%ignore wxPropertyGridEvent::SetPropertyGrid;
%ignore wxPropertyGridEvent::SetPropertyValue;
%ignore wxPropertyGridEvent::SetupValidationInfo;

// props.h
%ignore wxPGInDialogValidator;
%ignore wxPGDoValidationConstants;
%ignore wxBoolProperty;
%ignore wxDirProperty;
%ignore wxArrayStringProperty::CreateEditorDialog;

// advprops.h
%ignore wxColourPropertyValue::operator=;
%ignore operator==(const wxArrayInt& array1, const wxArrayInt& array2);
%ignore operator==(const wxColourPropertyValue&,const wxColourPropertyValue&);
%ignore wxCursorProperty;
%ignore wxPGSpinCtrlEditor;
%ignore wxPGGetDefaultImageWildcard;
%ignore wxImageFileProperty;
%ignore wxMultiChoiceProperty;
%ignore wxDateProperty;

// manager.h

// Suppress warning 511 (kwargs not supported for overloaded functions)
#pragma SWIG nowarn=511

// wxPropertyGrid specific special code

%extend wxPGProperty {
    %extend {
        // We need to re-implement this in order to also allow the one below.
        bool SetPyChoices( const wxPGChoices& chs )
        {
            return self->SetChoices(chs);
        }

        // Useful for setting choices directly from a list of strings. Also
        // needed for wxPG 1.4 compatibility.
        bool SetPyChoices( const wxArrayString& labels,
                           const wxArrayInt& values=wxArrayInt() )
        {
            wxPGChoices chs(labels, values);
            return self->SetChoices(chs);
        }

        //
        // Some wxPGProperty member functions take a wxVariant write-back
        // argument, and as such are normally ignored by SWIG, and we need
        // to add versions of them that return wxPGVariantAndBool instead.
        //

        wxPGVariantAndBool PyBase_StringToValue(const wxString& text,
                                                int argFlags = 0)
        {
            wxVariant variant = self->GetValuePlain();
            bool res = self->StringToValue(variant, text, argFlags);
            return wxPGVariantAndBool(res, variant);
        }

        wxPGVariantAndBool PyBase_IntToValue(wxVariant& value, int number,
                                             int argFlags = 0 ) const
        {
            wxVariant variant = self->GetValuePlain();
            bool res = self->IntToValue(variant, number, argFlags);
            return wxPGVariantAndBool(res, variant);
        }

        %property(m_value, GetValuePlain, SetValuePlain);

        DocStr(GetPyClientData,
               "Returns the client data object for a property", "");
        PyObject* GetPyClientData() {
            wxPyClientData* data = (wxPyClientData*)self->GetClientObject();
            return wxPyClientData::SafeGetData(data);
        }

        DocStr(SetPyClientData,
               "Associate the given client data.", "");
        void SetPyClientData(PyObject* clientData) {
            wxPyClientData* data = new wxPyClientData(clientData);
            self->SetClientObject(data);
        }
    }
    %pythoncode {
         SetChoices = SetPyChoices
         StringToValue = PyBase_StringToValue
         IntToValue = PyBase_IntToValue
         GetClientObject = GetPyClientData
         SetClientObject = SetPyClientData
         GetClientData = GetPyClientData
         SetClientData = SetPyClientData
    }
}

%extend wxPropertyGridInterface {
    %pythoncode {
        def MapType(class_,factory):
            "Registers Python type/class to property mapping.\n\nfactory: "
            "Property builder function/class."
            global _type2property
            try:
                mappings = _type2property
            except NameError:
                raise AssertionError("call only after a propertygrid or "
                                     "manager instance constructed")

            mappings[class_] = factory


        def DoDefaultTypeMappings(self):
            "Map built-in properties."
            global _type2property
            try:
                mappings = _type2property

                return
            except NameError:
                mappings = {}
                _type2property = mappings

            mappings[str] = StringProperty
            mappings[unicode] = StringProperty
            mappings[int] = IntProperty
            mappings[float] = FloatProperty
            mappings[bool] = BoolProperty
            mappings[list] = ArrayStringProperty
            mappings[tuple] = ArrayStringProperty
            mappings[wx.Font] = FontProperty
            mappings[wx.Colour] = ColourProperty
            "mappings[wx.Size] = SizeProperty"
            "mappings[wx.Point] = PointProperty"
            "mappings[wx.FontData] = FontDataProperty"

        def DoDefaultValueTypeMappings(self):
            "Map pg value type ids to getter methods."
            global _vt2getter
            try:
                vt2getter = _vt2getter

                return
            except NameError:
                vt2getter = {}
                _vt2getter = vt2getter

        def GetPropertyValues(self,dict_=None, as_strings=False,
                              inc_attributes=False):
            "Returns values in the grid."
            ""
            "dict_: if not given, then a new one is created. dict_ can be"
            "  object as well, in which case it's __dict__ is used."
            "as_strings: if True, then string representations of values"
            "  are fetched instead of native types. Useful for config and "
            "such."
            "inc_attributes: if True, then property attributes are added"
            "  as @<propname>@<attr>."
            ""
            "Return value: dictionary with values. It is always a dictionary,"
            "so if dict_ was object with __dict__ attribute, then that "
            "attribute is returned."

            if dict_ is None:
                dict_ = {}
            elif hasattr(dict_,'__dict__'):
                dict_ = dict_.__dict__

            if not as_strings:
                getter = self.GetPropertyValue
            else:
                getter = self.GetPropertyValueAsString

            it = self.GetVIterator(PG_ITERATE_PROPERTIES)
            while not it.AtEnd():
                p = it.GetProperty()
                name = p.GetName()

                dict_[name] = getter(p)

                if inc_attributes:
                    attrs = p.GetAttributes()
                    if attrs and len(attrs):
                        dict_['@%s@attr'%name] = attrs

                it.Next()

            return dict_

        GetValues = GetPropertyValues


        def SetPropertyValues(self,dict_):
            "Sets property values from dict_, which can be either\ndictionary "
            "or an object with __dict__ attribute."
            ""
            "autofill: If true, keys with not relevant properties"
            "  are auto-created. For more info, see AutoFill."
            ""
            "Notes:"
            "  * Keys starting with underscore are ignored."
            "  * Attributes can be set with entries named @<propname>@<attr>."
            ""

            autofill = False

            if dict_ is None:
                dict_ = {}
            elif hasattr(dict_,'__dict__'):
                dict_ = dict_.__dict__

            attr_dicts = []

            def set_sub_obj(k0,dict_):
                for k,v in dict_.iteritems():
                    if k[0] != '_':
                        if k.endswith('@attr'):
                            attr_dicts.append((k[1:-5],v))
                        else:
                            try:
                                self.SetPropertyValue(k,v)
                            except:
                                try:
                                    if autofill:
                                        self._AutoFillOne(k0,k,v)
                                        continue
                                except:
                                    if isinstance(v,dict):
                                        set_sub_obj(k,v)
                                    elif hasattr(v,'__dict__'):
                                        set_sub_obj(k,v.__dict__)


            for k,v in attr_dicts:
                p = GetPropertyByName(k)
                if not p:
                    raise AssertionError("No such property: '%s'"%k)
                for an,av in v.iteritems():
                    p.SetAttribute(an, av)


            cur_page = False
            is_manager = isinstance(self,PropertyGridManager)

            try:
                set_sub_obj(self.GetGrid().GetRoot(),dict_)
            except:
                import traceback
                traceback.print_exc()

            self.Refresh()

        SetValues = SetPropertyValues

        def _AutoFillMany(self,cat,dict_):
            for k,v in dict_.iteritems():
                self._AutoFillOne(cat,k,v)


        def _AutoFillOne(self,cat,k,v):
            global _type2property

            factory = _type2property.get(v.__class__,None)

            if factory:
                self.AppendIn( cat, factory(k,k,v) )
            elif hasattr(v,'__dict__'):
                cat2 = self.AppendIn( cat, PropertyCategory(k) )
                self._AutoFillMany(cat2,v.__dict__)
            elif isinstance(v,dict):
                cat2 = self.AppendIn( cat, PropertyCategory(k) )
                self._AutoFillMany(cat2,v)
            elif not k.startswith('_'):
                raise AssertionError("member '%s' is of unregisted type/"
                                     "class '%s'"%(k,v.__class__))


        def AutoFill(self,obj,parent=None):
            "Clears properties and re-fills to match members and\nvalues of "
            "given object or dictionary obj."

            self.edited_objects[parent] = obj

            cur_page = False
            is_manager = isinstance(self,PropertyGridManager)

            if not parent:
                if is_manager:
                    page = self.GetCurrentPage()
                    page.Clear()
                    parent = page.GetRoot()
                else:
                    self.Clear()
                    parent = self.GetGrid().GetRoot()
            else:
                it = self.GetIterator(PG_ITERATE_PROPERTIES, parent)
                it.Next()  # Skip the parent
                while not it.AtEnd():
                    p = it.GetProperty()
                    if not p.IsSomeParent(parent):
                        break

                    self.DeleteProperty(p)

                    name = p.GetName()
                    it.Next()

            if not is_manager or page == self.GetCurrentPage():
                self.Freeze()
                cur_page = True

            try:
                self._AutoFillMany(parent,obj.__dict__)
            except:
                import traceback
                traceback.print_exc()

            if cur_page:
                self.Thaw()

        def RegisterEditor(self, editor, editorName=None):
            "Transform class into instance, if necessary."
            if not isinstance(editor, PGEditor):
                editor = editor()
            if not editorName:
                editorName = editor.__class__.__name__
            try:
                self._editor_instances.append(editor)
            except:
                self._editor_instances = [editor]
            RegisterEditor(editor, editorName)

        def GetPropertyClientData(self, p):
            if isinstance(p, basestring):
                p = self.GetPropertyByName(p)
            return p.GetClientData()

        def SetPropertyClientData(self, p, data):
            if isinstance(p, basestring):
                p = self.GetPropertyByName(p)
            return p.SetClientData(data)

        def GetPyIterator(self, flags=PG_ITERATE_DEFAULT,
                          firstProperty=None):
            """
            Returns a pythonic property iterator for a single `PropertyGrid`
            or page in `PropertyGridManager`. Arguments are same as for
            `GetIterator`. Following example demonstrates iterating absolutely
            all items in a single grid::

                iterator = propGrid.GetPyIterator(wx.propgrid.PG_ITERATE_ALL)
                for prop in iterator:
                    print(prop)

            :see: `wx.propgrid.PropertyGridInterface.Properties`
                  `wx.propgrid.PropertyGridInterface.Items`
            """
            it = self.GetIterator(flags, firstProperty)
            while not it.AtEnd():
                yield it.GetProperty()
                it.Next()

        def GetPyVIterator(self, flags=PG_ITERATE_DEFAULT):
            """
            Returns a pythonic property iterator for a single `PropertyGrid`
            or entire `PropertyGridManager`. Arguments are same as for
            `GetIterator`. Following example demonstrates iterating absolutely
            all items in an entire `PropertyGridManager`::

                iterator = propGridManager.GetPyVIterator(wx.propgrid.PG_ITERATE_ALL)
                for prop in iterator:
                    print(prop)

            :see: `wx.propgrid.PropertyGridInterface.Properties`
                  `wx.propgrid.PropertyGridInterface.Items`
            """
            it = self.GetVIterator(flags)
            while not it.AtEnd():
                yield it.GetProperty()
                it.Next()

        @property
        def Properties(self):
            """
            This attribute is a pythonic iterator over all properties in
            this `PropertyGrid` property container. It will only skip
            categories and private child properties. Usage is simple::

                for prop in propGrid.Properties:
                    print(prop)

            :see: `wx.propgrid.PropertyGridInterface.Items`
                  `wx.propgrid.PropertyGridInterface.GetPyIterator`
            """
            it = self.GetVIterator(PG_ITERATE_NORMAL)
            while not it.AtEnd():
                yield it.GetProperty()
                it.Next()

        @property
        def Items(self):
            """
            This attribute is a pythonic iterator over all items in this
            `PropertyGrid` property container, excluding only private child
            properties. Usage is simple::

                for prop in propGrid.Items:
                    print(prop)

            :see: `wx.propgrid.PropertyGridInterface.Properties`
                  `wx.propgrid.PropertyGridInterface.GetPyIterator`
            """
            it = self.GetVIterator(PG_ITERATE_NORMAL | PG_ITERATE_CATEGORIES)
            while not it.AtEnd():
                yield it.GetProperty()
                it.Next()
    }
}

%extend wxPropertyGrid {
    %pythonAppend wxPropertyGrid {
        self._setOORInfo(self)
        self.DoDefaultTypeMappings()
        self.edited_objects = {}
        self.DoDefaultValueTypeMappings()
        if not hasattr(self.__class__,'_vt2setter'):
            self.__class__._vt2setter = {}
    }
    %pythonAppend wxPropertyGrid() ""
}

%extend wxPropertyGridManager {
    %pythonAppend wxPropertyGridManager {
        self._setOORInfo(self)
        self.DoDefaultTypeMappings()
        self.edited_objects = {}
        self.DoDefaultValueTypeMappings()
        if not hasattr(self.__class__,'_vt2setter'):
            self.__class__._vt2setter = {}
    }
    %pythonAppend wxPropertyGridManager() ""

    %pythoncode {
        def GetValuesFromPage(self,
                              page,
                              dict_=None,
                              as_strings=False,
                              inc_attributes=False):
            "Same as GetValues, but returns values from specific page only."
            "For argument descriptions, see GetValues."
            return page.GetPropertyValues(dict_, as_strings, inc_attributes)
    }
}

%extend wxPGMultiButton {
    %pythonAppend wxPGMultiButton
    {
        self._setOORInfo(self)
    }

    void AddBitmapButton( const wxBitmap& bitmap, int id = -2 )
    {
        return self->Add(bitmap, id);
    }
    %pythoncode {
        def AddButton(self, *args, **kwargs):
            return self.Add(*args, **kwargs)
    }
}

%{
// We need these proxies or SWIG will fail (it has somewhat incomplete
// C++ syntax support, it seems).
static wxString& wxString_wxPG_LABEL = *((wxString*)NULL);
#define wxColour_BLACK          *wxBLACK
#define wxBitmap_NULL           wxNullBitmap
%}

//---------------------------------------------------------------------------

%include "typemaps.i"

//
// This macro creates typemaps for arrays of arbitrary C++ objects. Array
// class must support basic std::vector API.
//
%define PG_MAKE_ARRAY_TYPEMAPS(ITEM_CLASS, ARR_CLASS)
    %{
    PyObject* ARR_CLASS ## ToPyObject(const ARR_CLASS* arr)
    {
        PyObject* pyArr = PyList_New(arr->size());
        for ( unsigned int i=0; i< (unsigned int) arr->size(); i++ )
        {
            PyObject* pyItem = SWIG_NewPointerObj((void*)(*arr)[i],
                                                  SWIGTYPE_p_ ## ITEM_CLASS,
                                                  0);
            if ( !pyItem )
                return NULL;
            PyList_SetItem(pyArr, i, pyItem);
        }
        return pyArr;
    }
    bool PyObjectTo ## ARR_CLASS(PyObject* pyArr, ARR_CLASS* arr)
    {
        if (! PySequence_Check(pyArr)) {
            PyErr_SetString(PyExc_TypeError, "Sequence expected.");
            return false;
        }
        int i, len = PySequence_Length(pyArr);
        for ( i=0; i<len; i++ )
        {
            PyObject* item = PySequence_GetItem(pyArr, i);
            int res1;
            void* voidPtr;
            res1 = SWIG_ConvertPtr(item, &voidPtr,
                                   SWIGTYPE_p_ ## ITEM_CLASS, 0 |  0 );
            if ( !SWIG_IsOK(res1) ) return false;
            ITEM_CLASS* itemPtr = reinterpret_cast<ITEM_CLASS*>(voidPtr);
            if ( PyErr_Occurred() ) return false;
            arr->push_back(itemPtr);
            Py_DECREF(item);
        }
        return true;
    }
    %}

    %typemap(in) ARR_CLASS& (bool temp=false) {
        $1 = new ARR_CLASS();
        temp = true;
        if ( !PyObjectTo ## ARR_CLASS($input, $1) ) SWIG_fail;
    }

    %typemap(freearg) ARR_CLASS& {
        if (temp$argnum) delete $1;
    }

    %typemap(out) ARR_CLASS& {
        $result = ARR_CLASS ## ToPyObject($1);
        if ( !$result ) SWIG_fail;
    }

%enddef


PG_MAKE_ARRAY_TYPEMAPS(wxPGProperty, wxArrayPGProperty)


// We'll need some new 'out' types for our custom directors
%typemap(out) wxPoint& { $result = wxPoint_to_PyObject($1); }
%typemap(out) wxSize& { $result = wxSize_to_PyObject($1); }
%typemap(out) const wxChar* {
%#if wxUSE_UNICODE
    $result = PyUnicode_FromWideChar($1, wxStrlen($1));
%#else
    $result = PyString_FromStringAndSize($1, wxStrlen($1));
%#endif
}

//
// wxVariant typemap
//
%typemap(in) wxVariant {
    if ( !PyObject_to_wxVariant($input, &$1) ) {
        PyErr_SetString(PyExc_TypeError,
                        "this Python type cannot be converted to wxVariant");
        SWIG_fail;
    }
}

%typemap(in) wxVariant& {
    $1 = new wxVariant();
    if ( !PyObject_to_wxVariant($input, $1) ) {
        PyErr_SetString(PyExc_TypeError,
                        "this Python type cannot be converted to wxVariant");
        SWIG_fail;
    }
}

%typemap(freearg) wxVariant& {
    delete $1;
}

%typemap(in) const wxVariant& {
    $1 = new wxVariant();
    if ( !PyObject_to_wxVariant($input, $1) ) {
        PyErr_SetString(PyExc_TypeError,
                        "this Python type cannot be converted to wxVariant");
        SWIG_fail;
    }
}

%typemap(freearg) const wxVariant& {
    delete $1;
}

%typemap(out) wxVariant {
    $result = wxVariant_to_PyObject(&$1);
    if ( !$result ) {
        PyErr_SetString(PyExc_TypeError,
            "this wxVariant type cannot be converted to Python object");
        SWIG_fail;
    }
}

%typemap(out) wxVariant& {
    $result = wxVariant_to_PyObject($1);
    if ( !$result ) {
        PyErr_SetString(PyExc_TypeError,
            "this wxVariant type cannot be converted to Python object");
        SWIG_fail;
    }
}

%typemap(out) const wxVariant& {
    $result = wxVariant_to_PyObject($1);
    if ( !$result ) {
        PyErr_SetString(PyExc_TypeError,
            "this wxVariant type cannot be converted to Python object");
        SWIG_fail;
    }
}

%typecheck(SWIG_TYPECHECK_POINTER) wxVariant
{
    // We'll try to convert any Python object into wxVariant
    $1 = 1;
}

%typemap(in) const wxPGPropArgCls& {
    if ( !PyObject_to_wxPGPropArgCls($input, &$1) ) {
        PyErr_SetString(PyExc_TypeError,
            "this Python type cannot be converted to wxPGPropArgCls");
        SWIG_fail;
    }
}

%typemap(freearg) const wxPGPropArgCls& {
    delete $1;
}

%typemap(out) wxPGPropArgCls {
    $result = wxPGPropArgCls_to_PyObject($1);
}

%typemap(out) wxPGAttributeStorage {
    $result = wxPGAttributeStorage_to_PyObject($1);
}

%typemap(out) wxPGAttributeStorage& {
    $result = wxPGAttributeStorage_to_PyObject($1);
}

%typemap(out) const wxPGAttributeStorage& {
    $result = wxPGAttributeStorage_to_PyObject($1);
}

//
// wxPGVariantAndBool typemaps
//
%typemap(in) wxPGVariantAndBool {
    if ( !PyObject_to_wxPGVariantAndBool($input, $1) ) {
        PyErr_SetString(PyExc_TypeError,
            "this Python type cannot be converted to wxPGVariantAndBool");
        SWIG_fail;
    }
}

%typemap(out) wxPGVariantAndBool {
    $result = wxPGVariantAndBool_to_PyObject($1);
}

//
// wxPGWindowList typemap (used by wxPGEditor::CreateControls)
//
%typemap(in) wxPGWindowList {
    if ( !PyObject_to_wxPGWindowList($input, &$1) ) {
        PyErr_SetString(PyExc_TypeError,
            "expected wxWindow or tuple of two wxWindows");
        SWIG_fail;
    }
}

%typemap(out) wxPGWindowList {
    $result = wxPGWindowList_to_PyObject(&$1);
}


//---------------------------------------------------------------------------
// Get all our defs from the REAL header file.

%include propgriddefs.h
%include property.h
%include propgridpagestate.h
%include propgridiface.h
%include propgrid.h
%include editors.h
%include props.h
%include advprops.h
%include manager.h

// Property constructor functions
wxPGProperty* NewPropertyCategory( const wxString& label = wxPG_LABEL,
                                   const wxString& name = wxPG_LABEL );
wxPGProperty* NewStringProperty( const wxString& label = wxPG_LABEL,
                                 const wxString& name = wxPG_LABEL,
                                 const wxString& value = wxEmptyString );
wxPGProperty* NewUIntProperty( const wxString& label = wxPG_LABEL,
                               const wxString& name = wxPG_LABEL,
                               unsigned long value = 0 );
wxPGProperty* NewIntProperty( const wxString& label = wxPG_LABEL,
                              const wxString& name = wxPG_LABEL,
                              long value = 0 );
//wxPGProperty* NewIntProperty( const wxString& label = wxPG_LABEL,
//                                const wxString& name = wxPG_LABEL,
//                                wxInt64 value = wxLL(0) );
//wxPGProperty* NewUIntProperty( const wxString& label = wxPG_LABEL,
//                                 const wxString& name = wxPG_LABEL,
//                                 wxUint64 value = wxLL(0) );
wxPGProperty* NewFloatProperty( const wxString& label = wxPG_LABEL,
                                const wxString& name = wxPG_LABEL,
                                double value = 0.0 );
wxPGProperty* NewBoolProperty( const wxString& label = wxPG_LABEL,
                               const wxString& name = wxPG_LABEL,
                               bool value = false );
wxPGProperty* NewEnumProperty( const wxString& label = wxPG_LABEL,
                               const wxString& name = wxPG_LABEL,
                               const wxArrayString& labels = wxArrayString(),
                               const wxArrayInt& values = wxArrayInt(),
                               int value = 0 );
wxPGProperty* NewEditEnumProperty( const wxString& label = wxPG_LABEL,
                               const wxString& name = wxPG_LABEL,
                               const wxArrayString& labels = wxArrayString(),
                               const wxArrayInt& values = wxArrayInt(),
                               const wxString& value = wxEmptyString );
wxPGProperty* NewFlagsProperty( const wxString& label = wxPG_LABEL,
        const wxString& name = wxPG_LABEL,
        const wxArrayString& labels = wxArrayString(),
        const wxArrayInt& values = wxArrayInt(),
        int value = 0 );
wxPGProperty* NewLongStringProperty( const wxString& label = wxPG_LABEL,
        const wxString& name = wxPG_LABEL,
        const wxString& value = wxEmptyString );
wxPGProperty* NewFileProperty( const wxString& label = wxPG_LABEL,
        const wxString& name = wxPG_LABEL,
        const wxString& value = wxEmptyString );
wxPGProperty* NewDirProperty( const wxString& label = wxPG_LABEL,
        const wxString& name = wxPG_LABEL,
        const wxString& value = wxEmptyString );
wxPGProperty* NewArrayStringProperty( const wxString& label = wxPG_LABEL,
        const wxString& name = wxPG_LABEL,
        const wxArrayString& value = wxArrayString() );
wxPGProperty* NewFontProperty( const wxString& label = wxPG_LABEL,
        const wxString& name = wxPG_LABEL,
        const wxFont& value = wxFont() );
wxPGProperty* NewSystemColourProperty( const wxString& label = wxPG_LABEL,
        const wxString& name = wxPG_LABEL,
        const wxColourPropertyValue& value = wxColourPropertyValue() );
wxPGProperty* NewColourProperty( const wxString& label = wxPG_LABEL,
        const wxString& name = wxPG_LABEL,
        const wxColour& value = wxColour() );
wxPGProperty* NewCursorProperty( const wxString& label= wxPG_LABEL,
        const wxString& name= wxPG_LABEL,
        int value = 0 );
wxPGProperty* NewImageFileProperty( const wxString& label = wxPG_LABEL,
        const wxString& name = wxPG_LABEL,
        const wxString& value = wxEmptyString);
wxPGProperty* NewMultiChoiceProperty( const wxString& label,
        const wxString& name = wxPG_LABEL,
        const wxArrayString& choices = wxArrayString(),
        const wxArrayString& value = wxArrayString() );
wxPGProperty* NewDateProperty( const wxString& label = wxPG_LABEL,
        const wxString& name = wxPG_LABEL,
        const wxDateTime& value = wxDateTime() );
#if 0
wxPGProperty* NewFontDataProperty( const wxString& label = wxPG_LABEL,
        const wxString& name = wxPG_LABEL,
        const wxFontData& value = wxFontData() );
wxPGProperty* NewSizeProperty( const wxString& label = wxPG_LABEL,
        const wxString& name = wxPG_LABEL,
        const wxSize& value = wxSize() );
wxPGProperty* NewPointProperty( const wxString& label = wxPG_LABEL,
        const wxString& name = wxPG_LABEL,
        const wxPoint& value = wxPoint() );
wxPGProperty* NewDirsProperty( const wxString& label = wxPG_LABEL,
        const wxString& name = wxPG_LABEL,
        const wxArrayString& value = wxArrayString() );
wxPGProperty* NewArrayDoubleProperty( const wxString& label = wxPG_LABEL,
       const wxString& name = wxPG_LABEL,
       const wxArrayDouble& value = wxArrayDouble() );
#endif

%include "propgrid_cbacks.i"

void RegisterEditor( wxPGEditor* editor, const wxString& editorName );

//---------------------------------------------------------------------------
// Python functions to act like the event macros

%pythoncode {
EVT_PG_CHANGED = wx.PyEventBinder( wxEVT_PG_CHANGED, 1 )
EVT_PG_CHANGING = wx.PyEventBinder( wxEVT_PG_CHANGING, 1 )
EVT_PG_SELECTED = wx.PyEventBinder( wxEVT_PG_SELECTED, 1 )
EVT_PG_HIGHLIGHTED = wx.PyEventBinder( wxEVT_PG_HIGHLIGHTED, 1 )
EVT_PG_RIGHT_CLICK = wx.PyEventBinder( wxEVT_PG_RIGHT_CLICK, 1 )
EVT_PG_PAGE_CHANGED = wx.PyEventBinder( wxEVT_PG_PAGE_CHANGED, 1 )
EVT_PG_ITEM_COLLAPSED = wx.PyEventBinder( wxEVT_PG_ITEM_COLLAPSED, 1 )
EVT_PG_ITEM_EXPANDED = wx.PyEventBinder( wxEVT_PG_ITEM_EXPANDED, 1 )
EVT_PG_DOUBLE_CLICK = wx.PyEventBinder( wxEVT_PG_DOUBLE_CLICK, 1 )
EVT_PG_LABEL_EDIT_BEGIN = wx.PyEventBinder( wxEVT_PG_LABEL_EDIT_BEGIN, 1 )
EVT_PG_LABEL_EDIT_ENDING = wx.PyEventBinder( wxEVT_PG_LABEL_EDIT_ENDING, 1 )
EVT_PG_COL_BEGIN_DRAG = wx.PyEventBinder( wxEVT_PG_COL_BEGIN_DRAG, 1 )
EVT_PG_COL_DRAGGING = wx.PyEventBinder( wxEVT_PG_COL_DRAGGING, 1 )
EVT_PG_COL_END_DRAG = wx.PyEventBinder( wxEVT_PG_COL_END_DRAG, 1 )

LABEL_AS_NAME = "@!"
DEFAULT_IMAGE_SIZE = (-1,-1)
NO_IMAGE_SIZE = (0,0)

PG_BOOL_USE_CHECKBOX = "UseCheckbox"
PG_BOOL_USE_DOUBLE_CLICK_CYCLING = "UseDClickCycling"
PG_FLOAT_PRECISION = "Precision"
PG_STRING_PASSWORD = "Password"
PG_UINT_BASE = "Base"
PG_UINT_PREFIX = "Prefix"
PG_FILE_WILDCARD = "Wildcard"
PG_FILE_SHOW_FULL_PATH = "ShowFullPath"
PG_FILE_SHOW_RELATIVE_PATH = "ShowRelativePath"
PG_FILE_INITIAL_PATH = "InitialPath"
PG_FILE_DIALOG_TITLE = "DialogTitle"
PG_DIR_DIALOG_MESSAGE = "DialogMessage"
PG_DATE_FORMAT = "DateFormat"
PG_DATE_PICKER_STYLE = "PickerStyle"

}

//---------------------------------------------------------------------------

%init %{
    wxPGInitResourceModule();
%}


//---------------------------------------------------------------------------

%include "propgrid_cbacks.cpp"

%pythoncode {

PropertyCategory = NewPropertyCategory
StringProperty = NewStringProperty
IntProperty = NewIntProperty
UIntProperty = NewUIntProperty
FloatProperty = NewFloatProperty
BoolProperty = NewBoolProperty
EnumProperty = NewEnumProperty
EditEnumProperty = NewEditEnumProperty
FlagsProperty = NewFlagsProperty
LongStringProperty = NewLongStringProperty
FileProperty = NewFileProperty
DirProperty = NewDirProperty
ArrayStringProperty = NewArrayStringProperty
FontProperty = NewFontProperty
SystemColourProperty = NewSystemColourProperty
ColourProperty = NewColourProperty
CursorProperty = NewCursorProperty
ImageFileProperty = NewImageFileProperty
MultiChoiceProperty = NewMultiChoiceProperty
DateProperty = NewDateProperty
#FontDataProperty = NewFontDataProperty
#SizeProperty = NewSizeProperty
#PointProperty = NewPointProperty
#DirsProperty = NewDirsProperty
#ArrayDoubleProperty = NewArrayDoubleProperty

}
