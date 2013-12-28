/////////////////////////////////////////////////////////////////////////////
// Name:        _defs.i
// Purpose:     Definitions and stuff
//
// Author:      Robin Dunn
//
// Created:     6/24/97
// RCS-ID:      $Id$
// Copyright:   (c) 1998 by Total Control Software
// Licence:     wxWindows license
/////////////////////////////////////////////////////////////////////////////


//---------------------------------------------------------------------------

// Globally turn on the autodoc feature
%feature("autodoc", "1");  // 0 == no param types, 1 == show param types

// Turn on kwargs by default
%feature("kwargs", "1");

// Don't generate separate wrappers for each default args combination
%feature("compactdefaultargs");

#if SWIG_VERSION < 0x010328
// Don't generate default ctors or dtors if the C++ doesn't have them
%feature("nodefault");
#else
// This is the SWIG 1.3.28 way to do the above...
%feature("nodefaultctor");
%feature("nodefaultdtor");
#endif

// For all items that don't have a %rename already, give them a %rename that
// removes the leading 'wx' (except for wxEVT_* items.)
%rename("%(wxpy)s") "";

// For now, just supress the warning about using Python keywords as parameter
// names.  Will need to come back later and correct these rather than just
// hide them...
#pragma SWIG nowarn=314

//---------------------------------------------------------------------------

// Tell SWIG to wrap all the wrappers with our thread protection
%define %threadWrapperOn
%exception {
    PyThreadState* __tstate = wxPyBeginAllowThreads();
    $action
    wxPyEndAllowThreads(__tstate);
    if (PyErr_Occurred()) SWIG_fail;
}
%enddef

// This one will turn off the generation of the thread wrapper code
%define %threadWrapperOff
%exception {
    $action
    if (PyErr_Occurred()) SWIG_fail;
}
%enddef

// Turn it on by default
%threadWrapperOn

// This one can be used to add a check for an existing wxApp before the real
// work is done.  An exception is raised if there isn't one.
%define MustHaveApp(name)
%exception name {
    if (!wxPyCheckForApp()) SWIG_fail;
    PyThreadState* __tstate = wxPyBeginAllowThreads();
    $action
    wxPyEndAllowThreads(__tstate);
    if (PyErr_Occurred()) SWIG_fail;
}
%enddef


// This macro can be used to disable the releasing of the GIL when calling the
// C++ function.  This is like using threadWrapperOff for just this function.
%define KeepGIL(name)
%exception name {
    $action
    if (PyErr_Occurred()) SWIG_fail;
}
%enddef
        
//---------------------------------------------------------------------------
// some type definitions to simplify things for SWIG

typedef int             wxEventType;
typedef unsigned int    size_t;
typedef unsigned int    time_t;
typedef unsigned char   byte;
typedef unsigned long   wxUIntPtr;
typedef double          wxDouble;

#define wxWindowID      int
#define wxCoord         int
#define wxInt32         int
#define wxUint32        unsigned int


//----------------------------------------------------------------------
// Various SWIG macros and such

#define %pythonAppend   %feature("pythonappend")
#define %pythonPrepend  %feature("pythonprepend")
#define %noautodoc      %feature("noautodoc")

#if SWIG_VERSION >= 0x010327
#undef %kwargs
#define %kwargs         %feature("kwargs", "1")
#define %nokwargs       %feature("kwargs", "0")
#else
#define %kwargs         %feature("kwargs")
#define %nokwargs       %feature("nokwargs")
#endif

#define %disownarg(typespec)   %typemap(in) typespec = SWIGTYPE* DISOWN
#define %cleardisown(typespec) %typemap(in) typespec
    
#define %ref   %feature("ref")
#define %unref %feature("unref")


#ifndef %pythoncode
#define %pythoncode     %insert("python")
#endif

#define WXUNUSED(x)     x


// Given the name of a wxChar (or wxString) constant in C++, make
// a static wxString for wxPython, and also let SWIG wrap it.
%define MAKE_CONST_WXSTRING(strname)
    %{ static const wxString wxPy##strname(wx##strname); %}
    %immutable;
    %rename(strname) wxPy##strname;
    const wxString wxPy##strname;
    %mutable;
%enddef

%define MAKE_CONST_WXSTRING2(strname, val)
    %{ static const wxString wxPy##strname(val); %}
    %immutable;
    %rename(strname) wxPy##strname;
    const wxString wxPy##strname;
    %mutable;
%enddef

%define MAKE_CONST_WXSTRING_NOSWIG(strname)
    %{ static const wxString wxPy##strname(wx##strname); %}
%enddef

// Generate code in the module init for the event types, since they may not be
// initialized yet when they are used in the static swig_const_table.
%typemap(consttab) wxEventType; // TODO: how to prevent code inserted into the consttab?
%typemap(constcode) wxEventType "PyDict_SetItemString(d, \"$symname\", PyInt_FromLong($value));";


%define %property(NAME, STUFF...)
    %pythoncode { NAME = property(STUFF) }
%enddef


%define setCallbackInfo(klass)
    "klass._setCallbackInfo(self, self, klass)"
%enddef


//----------------------------------------------------------------------
// Macros for the docstring and autodoc features of SWIG.  These will
// help make the code look more readable, and pretty, as well as help
// reduce typing in some cases.

// Set the docsring for the given full or partial declaration
#ifdef _DO_FULL_DOCS
    %define DocStr(decl, docstr, details)
        %feature("docstring") decl docstr details;
    %enddef
#else
    %define DocStr(decl, docstr, details)
        %feature("docstring") decl docstr;
    %enddef
#endif


// Set the autodoc string for a full or partial declaration
%define DocA(decl, astr)
    %feature("autodoc") decl astr;
%enddef


// Set both the autodoc and docstring for a full or partial declaration
#ifdef _DO_FULL_DOCS
    %define DocAStr(decl, astr, docstr, details)
        %feature("autodoc") decl astr;
        %feature("docstring") decl docstr details
    %enddef
#else
    %define DocAStr(decl, astr, docstr, details)
        %feature("autodoc") decl astr;
        %feature("docstring") decl docstr
    %enddef
#endif

        

    
// Set the docstring for a decl and then define the decl too.  Must use the
// full declaration of the item.
#ifdef _DO_FULL_DOCS
    %define DocDeclStr(type, decl, docstr, details)
        %feature("docstring") decl docstr details;
        type decl
    %enddef
#else
    %define DocDeclStr(type, decl, docstr, details)
        %feature("docstring") decl docstr;
        type decl
    %enddef
#endif

        
    
// As above, but also give the decl a new %name    
#ifdef _DO_FULL_DOCS
    %define DocDeclStrName(type, decl, docstr, details, newname)
        %feature("docstring") decl docstr details;
        %rename(newname) decl;
        type decl
    %enddef
#else
    %define DocDeclStrName(type, decl, docstr, details, newname)
        %feature("docstring") decl docstr;
        %rename(newname) decl;
        type decl
    %enddef
#endif
        
    
// Set the autodoc string for a decl and then define the decl too.  Must use the
// full declaration of the item.
%define DocDeclA(type, decl, astr)
    %feature("autodoc") decl astr;
    type decl
%enddef

// As above, but also give the decl a new %name    
%define DocDeclAName(type, decl, astr, newname)
    %feature("autodoc") decl astr;
    %rename(newname) decl;
    type decl
%enddef



// Set the autodoc and the docstring for a decl and then define the decl too.
// Must use the full declaration of the item.
#ifdef _DO_FULL_DOCS
    %define DocDeclAStr(type, decl, astr, docstr, details)
        %feature("autodoc") decl astr;
        %feature("docstring") decl docstr details;
        type decl
    %enddef
#else
    %define DocDeclAStr(type, decl, astr, docstr, details)
        %feature("autodoc") decl astr;
        %feature("docstring") decl docstr;
        type decl
    %enddef
#endif

        
// As above, but also give the decl a new %name    
#ifdef _DO_FULL_DOCS
    %define DocDeclAStrName(type, decl, astr, docstr, details, newname)
        %feature("autodoc") decl astr;
        %feature("docstring") decl docstr details;
        %rename(newname) decl;
        type decl
    %enddef
#else
    %define DocDeclAStrName(type, decl, astr, docstr, details, newname)
        %feature("autodoc") decl astr;
        %feature("docstring") decl docstr;
        %rename(newname) decl;
        type decl
    %enddef
#endif



// Set the docstring for a constructor decl and then define the decl too.
// Must use the full declaration of the item.
#ifdef _DO_FULL_DOCS
    %define DocCtorStr(decl, docstr, details)
        %feature("docstring") decl docstr details;
        decl
    %enddef
#else
    %define DocCtorStr(decl, docstr, details)
        %feature("docstring") decl docstr;
        decl
    %enddef
#endif

        
// As above, but also give the decl a new %name    
#ifdef _DO_FULL_DOCS
    %define DocCtorStrName(decl, docstr, details, newname)
        %feature("docstring") decl docstr details;
        %rename(newname) decl;
        decl
    %enddef
#else
    %define DocCtorStrName(decl, docstr, details, newname)
        %feature("docstring") decl docstr;
        %rename(newname) decl;
        decl
    %enddef
#endif

        
// Set the autodoc string for a constructor decl and then define the decl too.
// Must use the full declaration of the item.
%define DocCtorA(decl, astr)
    %feature("autodoc") decl astr;
    decl
%enddef

// As above, but also give the decl a new %name    
%define DocCtorAName(decl, astr, newname)
    %feature("autodoc") decl astr;
    %rename(newname) decl;
    decl
%enddef



// Set the autodoc and the docstring for a constructor decl and then define
// the decl too.  Must use the full declaration of the item.
#ifdef _DO_FULL_DOCS
    %define DocCtorAStr(decl, astr, docstr, details)
        %feature("autodoc") decl astr;
        %feature("docstring") decl docstr details;
        decl
    %enddef
#else
    %define DocCtorAStr(decl, astr, docstr, details)
        %feature("autodoc") decl astr;
        %feature("docstring") decl docstr;
        decl
    %enddef
#endif


        
// As above, but also give the decl a new %name    
#ifdef _DO_FULL_DOCS
    %define DocCtorAStrName(decl, astr, docstr, details, newname)
        %feature("autodoc") decl astr;
        %feature("docstring") decl docstr details;
        %rename(newname) decl;
        decl
    %enddef
#else
    %define DocCtorAStrName(decl, astr, docstr, details, newname)
        %feature("autodoc") decl astr;
        %feature("docstring") decl docstr;
        %rename(newname) decl;
        decl
    %enddef
#endif

       
    
%define %newgroup
%pythoncode {
%#---------------------------------------------------------------------------
}
%enddef


// A set of macros to make using %rename easier, since %name has been
// deprecated...
%define %Rename(newname, type, decl)
    %rename(newname) decl;
    type decl
%enddef

%define %RenameCtor(newname, decl)
    %rename(newname) decl;
    decl
%enddef

// Combine renaming and docstrings
#ifdef _DO_FULL_DOCS
    %define %RenameDocCtor(newname, docstr, details, decl)
        %feature("docstring") decl docstr details;
        %rename(newname) decl;
        decl
    %enddef
    %define %RenameADocCtor(newname, astr, docstr, details, decl)
        %feature("autodoc") decl astr;
        %feature("docstring") decl docstr details;
        %rename(newname) decl;
        decl
    %enddef
#else
    %define %RenameDocCtor(newname, docstr, details, decl)
        %feature("docstring") decl docstr;
        %rename(newname) decl;
        decl
    %enddef
    %define %RenameADocCtor(newname, astr, docstr, details, decl)
        %feature("autodoc") decl astr;
        %feature("docstring") decl docstr;
        %rename(newname) decl;
        decl
    %enddef
#endif

#ifdef _DO_FULL_DOCS
    %define %RenameDocStr(newname, docstr, details, type, decl)
        %feature("docstring") decl docstr;
        %rename(newname) decl;
        type decl
    %enddef        
#else
    %define %RenameDocStr(newname, docstr, details, type, decl)
        %feature("docstring") decl docstr details;
        %rename(newname) decl;
        type decl
    %enddef        
#endif


        
//---------------------------------------------------------------------------
// Generates a base_On* method that just wraps a call to the On*, and mark it
// deprecated.  We need this because there is no longer any need for a
// base_On* method to be able to call the C++ base class method, since our
// virtualization code can now sense when an attempt is being made to call
// the base class version from the derived class override.
        
%define %MAKE_BASE_FUNC(Class, Method)
    %pythoncode {
        def base_##Method(*args, **kw):
            return Class.Method(*args, **kw)
        base_##Method = wx.deprecated(base_##Method,
                                       "Please use Class.Method instead.")
    }
%enddef    
    
//---------------------------------------------------------------------------
// Forward declarations and %renames for some classes, so the autodoc strings
// will be able to use the right types even when the real class declaration is
// not in the module being processed or seen by %import's.

#ifdef BUILDING_RENAMERS
    #define FORWARD_DECLARE(wxName, Name)
#else
    %define FORWARD_DECLARE(wxName, Name)
        %rename(Name) wxName;
        class wxName;
    %enddef
#endif

FORWARD_DECLARE(wxString,         String);
FORWARD_DECLARE(wxBitmap,         Bitmap);
FORWARD_DECLARE(wxDateTime,       DateTime);
FORWARD_DECLARE(wxInputStream,    InputStream);
FORWARD_DECLARE(wxDC,             DC);
FORWARD_DECLARE(wxCursor,         Cursor);
FORWARD_DECLARE(wxRegion,         Region);
FORWARD_DECLARE(wxColour,         Colour);
FORWARD_DECLARE(wxFont,           Font);
FORWARD_DECLARE(wxCaret,          Caret);
FORWARD_DECLARE(wxToolTip,        ToolTip);
FORWARD_DECLARE(wxPyDropTarget,   DropTarget);
FORWARD_DECLARE(wxImageList,      ImageList);
FORWARD_DECLARE(wxMemoryDC,       MemoryDC);
FORWARD_DECLARE(wxHtmlTagHandler, HtmlTagHandler);
FORWARD_DECLARE(wxConfigBase,     ConfigBase);
FORWARD_DECLARE(wxIcon,           Icon);
FORWARD_DECLARE(wxStaticBox,      StaticBox);


//---------------------------------------------------------------------------
// These macros make a class to wrap a type specific class derived from wxList,
// and make it look like a Python sequence, including iterator support.


%define wxLIST_WRAPPER_TYPEDEF(ListClass, FakeListClass)
%{
    typedef ListClass FakeListClass;    
%}
%enddef

%define wxLIST_WRAPPER_MAIN(ListClass, ItemClass, RealItemClass)    
// first a bit of C++ code...    
%{
class ListClass##_iterator
{
public:
    ListClass##_iterator(ListClass::compatibility_iterator start)
        : m_node(start) {}
    
    ItemClass* next() {
        RealItemClass* obj = NULL;
        if (m_node) {
            obj = m_node->GetData();
            m_node = m_node->GetNext();
        }
        else PyErr_SetString(PyExc_StopIteration, "");
        return (ItemClass*)obj;
    }
private:
    ListClass::compatibility_iterator m_node;
};
%}

// Now declare the classes for SWIG

DocStr(ListClass##_iterator,
"This class serves as an iterator for a ListClass object.", "");

class ListClass##_iterator
{
public:
    //ListClass##_iterator();
    ~ListClass##_iterator();
    KeepGIL(next);
    ItemClass* next();
};


DocStr(ListClass,
"This class wraps a wxList-based class and gives it a Python
sequence-like interface.  Sequence operations supported are length,
index access and iteration.", "");

class ListClass
{
public:
    //ListClass();      This will always be created by some C++ function
    ~ListClass();

    %extend {
        KeepGIL(__len__);
        size_t __len__() {
            return self->size();
        }

        KeepGIL(__getitem__);
        ItemClass* __getitem__(size_t index) {
            if (index < self->size()) {
                ListClass::compatibility_iterator node = self->Item(index);
                if (node) return (ItemClass*)node->GetData();
            }
            PyErr_SetString(PyExc_IndexError, "sequence index out of range");
            return NULL;
        }

        KeepGIL(__contains__);
        bool __contains__(const ItemClass* obj) {
            ListClass::compatibility_iterator node;
            node = self->Find((RealItemClass*)obj);
            return node;
        }

        KeepGIL(__iter__);
        %newobject __iter__;
        ListClass##_iterator* __iter__() {
            return new ListClass##_iterator(self->GetFirst());
        }

        // TODO:  add support for index(value, [start, [stop]])
        KeepGIL(index);
        int index(ItemClass* obj) {
            int idx = self->IndexOf((RealItemClass*)obj);
            if (idx == wxNOT_FOUND)
                PyErr_SetString(PyExc_ValueError,
                                "sequence.index(x): x not in sequence");
            return idx;
        }        
    }
    %pythoncode {
        def __repr__(self):
            return "ListClass: " + repr(list(self))
    }
};
%enddef


// This is the one that will normally be used.  It wraps the real C++ classes
// as needed, with the same names.
%define wxLIST_WRAPPER(ListClass, ItemClass)
    wxLIST_WRAPPER_MAIN(ListClass, ItemClass, ItemClass)
%enddef


// This one can be used to do some SWIG trickery to pretend that the type
// contained in the list is a different (derived) type.  For example the item
// list used by a wxGridBagSizer contains wxGBSizerItems, not wxSizerItems.
%define wxLIST_WRAPPER_FAKE(ListClass, ItemClass, FakeListClass, FakeItemClass)
    wxLIST_WRAPPER_TYPEDEF(ListClass, FakeListClass)
    wxLIST_WRAPPER_MAIN(FakeListClass, FakeItemClass, ItemClass)
%enddef



// This macro is similar to the above, but it is to be used when there isn't a
// type-specific C++ list class to use.  In other words the C++ code is using
// a plain wxList and typecasting the node values, so we'll do the same.
%define wxUNTYPED_LIST_WRAPPER(ListClass, ItemClass)
// first a bit of C++ code...    
%{
class ListClass
{
public:
    ListClass(wxList* theList)
        : m_list(theList) {}
    ~ListClass() {}
public:
    wxList* m_list;
};

class ListClass##_iterator
{
public:
    ListClass##_iterator(wxList::compatibility_iterator start)
        : m_node(start) {}
    
    ItemClass* next() {
        ItemClass* obj = NULL;
        if (m_node) {
            obj = (ItemClass*)m_node->GetData();
            m_node = m_node->GetNext();
        }
        else PyErr_SetString(PyExc_StopIteration, "");
        return obj;
    }
private:
    wxList::compatibility_iterator m_node;
};
%}

// Now declare the classes for SWIG

DocStr(ListClass##_iterator,
"This class serves as an iterator for a ListClass object.", "");

class ListClass##_iterator
{
public:
    //ListClass##_iterator();
    ~ListClass##_iterator();
    KeepGIL(next);
    ItemClass* next();
};


DocStr(ListClass,
"This class wraps a wxList-based class and gives it a Python
sequence-like interface.  Sequence operations supported are length,
index access and iteration.", "");
class ListClass
{
public:
    //ListClass();      This will always be created by some C++ function
    ~ListClass();

    %extend {
        KeepGIL(__len__);
        size_t __len__() {
            return self->m_list->size();
        }

        KeepGIL(__getitem__);
        ItemClass* __getitem__(size_t index) {
            if (index < self->m_list->size()) {
                wxList::compatibility_iterator node = self->m_list->Item(index);
                if (node) return (ItemClass*)node->GetData();
            }
            PyErr_SetString(PyExc_IndexError, "Invalid list index");
            return NULL;
        }

        KeepGIL(__contains__);
        bool __contains__(const ItemClass* obj) {
            return self->m_list->Find(obj);
        }

        KeepGIL(__iter__);
        %newobject __iter__;
        ListClass##_iterator* __iter__() {
            return new ListClass##_iterator(self->m_list->GetFirst());
        }
    }
    %pythoncode {
        def __repr__(self):
            return "ListClass: " + repr(list(self))
    }
};

// A typemap to handle converting a wxList& return value to this new list
// type.  To use this just change the return value type in the class
// definition to this typedef instead of wxList, then SWIG will use the
// typemap.
%{
typedef wxList ListClass##_t;
%}
%typemap(out) ListClass##_t& {
    ListClass* mylist = new ListClass($1);
    $result = SWIG_NewPointerObj(SWIG_as_voidptr(mylist), SWIGTYPE_p_##ListClass, SWIG_POINTER_OWN );
}
%enddef




// and now something similar for wxArray

%define wxARRAY_WRAPPER(ArrayClass, ItemClass)
// first a bit of C++ code...    
%{
class ArrayClass##_iterator
{
public:
    ArrayClass##_iterator(ArrayClass &array)
    : m_array(array), m_idx(0) {}
    
    ItemClass* next() {
        ItemClass* obj = NULL;
        if (m_idx < m_array.GetCount()) {
            obj = (ItemClass*)&m_array.Item(m_idx);
            m_idx += 1;
        }
        else PyErr_SetString(PyExc_StopIteration, "");
        return obj;
    }
private:
    ArrayClass& m_array;
    size_t      m_idx;
};
%}

// Now declare the classes for SWIG

DocStr(ArrayClass##_iterator,
"This class serves as an iterator for a ArrayClass object.", "");

class ArrayClass##_iterator
{
public:
    //ArrayClass##_iterator();
    ~ArrayClass_iterator();
    KeepGIL(next);
    ItemClass* next();
};


DocStr(ArrayClass,
"This class wraps a wxArray-based class and gives it a Python
sequence-like interface.  Sequence operations supported are length,
index access and iteration.", "");

class ArrayClass
{
public:
    //ArrayClass();      This will always be created by some C++ function
    ~ArrayClass();

    %extend {
        KeepGIL(__len__);
        size_t __len__() {
            return self->GetCount();
        }

        KeepGIL(__getitem__);
        ItemClass* __getitem__(size_t index) {
            if (index < self->GetCount()) {
                return (ItemClass*)&self->Item(index);
            }
            PyErr_SetString(PyExc_IndexError, "sequence index out of range");
            return NULL;
        }

// TODO        
//         KeepGIL(__contains__);
//         bool __contains__(const ItemClass* obj) {
//         }
//         KeepGIL(index);
//         int index(ItemClass* obj) {
//         }

        KeepGIL(__iter__);
        %newobject __iter__;
        ArrayClass##_iterator* __iter__() {
            return new ArrayClass##_iterator(*self);
        }

        %disownarg( ItemClass *object );
        KeepGIL(append);
        void append(ItemClass* object){
            self->Add(*object);
        }
        KeepGIL(insert);
        void insert(size_t index, ItemClass* object) {
            self->Insert(*object, index);
        }
        %cleardisown( ItemClass *object );
    }
    
    %pythoncode {
        def __repr__(self):
            return "ArrayClass: " + repr(list(self))
    }
};
%enddef


//---------------------------------------------------------------------------

%{
#if !WXWIN_COMPATIBILITY_2_4
    #define wxHIDE_READONLY  0
#endif
%}    


// General numeric #define's and etc.  Making them all enums makes SWIG use the
// real macro when making the Python Int

enum {
//     wxMAJOR_VERSION,
//     wxMINOR_VERSION,
//     wxRELEASE_NUMBER,

    wxDefaultCoord,
    
    wxNOT_FOUND,
    wxNO_LEN,

    wxVSCROLL,
    wxHSCROLL,
    wxCAPTION,
    wxDOUBLE_BORDER,
    wxSUNKEN_BORDER,
    wxRAISED_BORDER,
    wxBORDER,
    wxSIMPLE_BORDER,
    wxSTATIC_BORDER,
    wxTRANSPARENT_WINDOW,
    wxNO_BORDER,
    wxDEFAULT_CONTROL_BORDER,
    wxDEFAULT_STATUSBAR_STYLE,
    
    wxTAB_TRAVERSAL,
    wxWANTS_CHARS,
    wxPOPUP_WINDOW,
    wxCENTER_FRAME,
    wxCENTRE_ON_SCREEN,
    wxCENTER_ON_SCREEN,

    wxCLIP_CHILDREN,
    wxCLIP_SIBLINGS,

    wxWINDOW_STYLE_MASK,
    
    wxALWAYS_SHOW_SB,
    
    wxRETAINED,
    wxBACKINGSTORE,

    wxCOLOURED,
    wxFIXED_LENGTH,

    wxLB_NEEDED_SB,
    wxLB_ALWAYS_SB,
    wxLB_SORT,
    wxLB_SINGLE,
    wxLB_MULTIPLE,
    wxLB_EXTENDED,
    wxLB_OWNERDRAW,
    wxLB_HSCROLL,

    wxCB_SIMPLE,
    wxCB_DROPDOWN,
    wxCB_SORT,
    wxCB_READONLY,
    wxRA_HORIZONTAL,
    wxRA_VERTICAL,
    wxRA_SPECIFY_ROWS,
    wxRA_SPECIFY_COLS,
    wxRB_GROUP,
    wxRB_SINGLE,
    wxSB_HORIZONTAL,
    wxSB_VERTICAL,
    
    wxTOOL_TOP,
    wxTOOL_BOTTOM,
    wxTOOL_LEFT,
    wxTOOL_RIGHT,
    wxOK,
    wxYES_NO,
    wxCANCEL,
    wxYES,
    wxNO,
    wxNO_DEFAULT,
    wxYES_DEFAULT,
    wxOK_DEFAULT,
    wxCANCEL_DEFAULT,
    wxAPPLY,
    wxCLOSE,
     
    wxICON_EXCLAMATION,
    wxICON_HAND,
    wxICON_QUESTION,
    wxICON_INFORMATION,
    wxICON_STOP,
    wxICON_ASTERISK,
    wxICON_MASK,
    wxICON_WARNING,
    wxICON_ERROR,
    wxICON_NONE,

    wxFORWARD,
    wxBACKWARD,
    wxRESET,
    wxHELP,
    wxMORE,
    wxSETUP,

    wxSIZE_AUTO_WIDTH,
    wxSIZE_AUTO_HEIGHT,
    wxSIZE_AUTO,
    wxSIZE_USE_EXISTING,
    wxSIZE_ALLOW_MINUS_ONE,
    wxSIZE_FORCE,
    wxSIZE_FORCE_EVENT,
    
    wxPRINT_QUALITY_HIGH,
    wxPRINT_QUALITY_MEDIUM,
    wxPRINT_QUALITY_LOW,
    wxPRINT_QUALITY_DRAFT,

    wxID_AUTO_LOWEST,
    wxID_AUTO_HIGHEST,

    wxID_ANY,
    wxID_SEPARATOR,
    wxID_NONE,

    wxID_LOWEST,
    wxID_OPEN,
    wxID_CLOSE,
    wxID_NEW,
    wxID_SAVE,
    wxID_SAVEAS,
    wxID_REVERT,
    wxID_EXIT,
    wxID_UNDO,
    wxID_REDO,
    wxID_HELP,
    wxID_PRINT,
    wxID_PRINT_SETUP,
    wxID_PAGE_SETUP,
    wxID_PREVIEW,
    wxID_ABOUT,
    wxID_HELP_CONTENTS,
    wxID_HELP_COMMANDS,
    wxID_HELP_PROCEDURES,
    wxID_HELP_CONTEXT,
    wxID_HELP_INDEX,
    wxID_HELP_SEARCH,
    wxID_CLOSE_ALL,
    wxID_PREFERENCES,

    wxID_EDIT,
    wxID_CUT,
    wxID_COPY,
    wxID_PASTE,
    wxID_CLEAR,
    wxID_FIND,
    wxID_DUPLICATE,
    wxID_SELECTALL,

    wxID_DELETE,
    wxID_REPLACE,
    wxID_REPLACE_ALL,
    wxID_PROPERTIES,

    wxID_VIEW_DETAILS,
    wxID_VIEW_LARGEICONS,
    wxID_VIEW_SMALLICONS,
    wxID_VIEW_LIST,
    wxID_VIEW_SORTDATE,
    wxID_VIEW_SORTNAME,
    wxID_VIEW_SORTSIZE,
    wxID_VIEW_SORTTYPE,

    wxID_FILE,
    wxID_FILE1,
    wxID_FILE2,
    wxID_FILE3,
    wxID_FILE4,
    wxID_FILE5,
    wxID_FILE6,
    wxID_FILE7,
    wxID_FILE8,
    wxID_FILE9,

    wxID_OK,
    wxID_CANCEL,
    wxID_APPLY,
    wxID_YES,
    wxID_NO,
    wxID_STATIC,
    wxID_FORWARD,
    wxID_BACKWARD,
    wxID_DEFAULT,
    wxID_MORE,
    wxID_SETUP,
    wxID_RESET,
    wxID_CONTEXT_HELP,
    wxID_YESTOALL,
    wxID_NOTOALL,
    wxID_ABORT,
    wxID_RETRY,
    wxID_IGNORE,

    wxID_ADD,
    wxID_REMOVE,

    wxID_UP,
    wxID_DOWN,
    wxID_HOME,
    wxID_REFRESH,
    wxID_STOP,
    wxID_INDEX,

    wxID_BOLD,
    wxID_ITALIC,
    wxID_JUSTIFY_CENTER,
    wxID_JUSTIFY_FILL,
    wxID_JUSTIFY_RIGHT,
    wxID_JUSTIFY_LEFT,
    wxID_UNDERLINE,
    wxID_INDENT,
    wxID_UNINDENT,
    wxID_ZOOM_100,
    wxID_ZOOM_FIT,
    wxID_ZOOM_IN,
    wxID_ZOOM_OUT,
    wxID_UNDELETE,
    wxID_REVERT_TO_SAVED,

    wxID_CDROM,
    wxID_CONVERT,
    wxID_EXECUTE,
    wxID_FLOPPY,
    wxID_HARDDISK,
    wxID_BOTTOM,
    wxID_FIRST,
    wxID_LAST,
    wxID_TOP,
    wxID_INFO,
    wxID_JUMP_TO,
    wxID_NETWORK,
    wxID_SELECT_COLOR,
    wxID_SELECT_FONT,
    wxID_SORT_ASCENDING,
    wxID_SORT_DESCENDING,
    wxID_SPELL_CHECK,
    wxID_STRIKETHROUGH,

    /*  System menu IDs (used by wxUniv): */
    wxID_SYSTEM_MENU,
    wxID_CLOSE_FRAME,
    wxID_MOVE_FRAME,
    wxID_RESIZE_FRAME,
    wxID_MAXIMIZE_FRAME,
    wxID_ICONIZE_FRAME,
    wxID_RESTORE_FRAME,

    /* MDI window menu ids */
    wxID_MDI_WINDOW_FIRST,
    wxID_MDI_WINDOW_CASCADE,
    wxID_MDI_WINDOW_TILE_HORZ,
    wxID_MDI_WINDOW_TILE_VERT,
    wxID_MDI_WINDOW_ARRANGE_ICONS,
    wxID_MDI_WINDOW_PREV,
    wxID_MDI_WINDOW_NEXT,
    wxID_MDI_WINDOW_LAST,

    wxID_OSX_MENU_FIRST,
    wxID_OSX_HIDE,
    wxID_OSX_HIDEOTHERS,
    wxID_OSX_SHOWALL,
    wxID_OSX_MENU_LAST,

    wxID_FILEDLGG,
    wxID_FILECTRL,
    wxID_HIGHEST,

    wxMENU_TEAROFF,
    wxMB_DOCKABLE,
    wxNO_FULL_REPAINT_ON_RESIZE,
    wxFULL_REPAINT_ON_RESIZE,
    
    wxLI_HORIZONTAL,
    wxLI_VERTICAL,

    wxWS_EX_VALIDATE_RECURSIVELY,
    wxWS_EX_BLOCK_EVENTS,
    wxWS_EX_TRANSIENT,

    wxWS_EX_THEMED_BACKGROUND,
    wxWS_EX_PROCESS_IDLE,
    wxWS_EX_PROCESS_UI_UPDATES,

};



enum wxGeometryCentre
{
    wxCENTRE                  = 0x0001,
    wxCENTER                  = wxCENTRE
};


enum wxOrientation
{
    wxHORIZONTAL,
    wxVERTICAL,
    wxBOTH,
    wxORIENTATION_MASK
};

enum wxDirection
{
    wxLEFT,
    wxRIGHT,
    wxUP,
    wxDOWN,

    wxTOP,
    wxBOTTOM,

    wxNORTH,
    wxSOUTH,
    wxWEST,
    wxEAST,

    wxALL,
    wxDIRECTION_MASK
};

enum wxAlignment
{
    wxALIGN_INVALID,
    wxALIGN_NOT,
    wxALIGN_CENTER_HORIZONTAL,
    wxALIGN_CENTRE_HORIZONTAL,
    wxALIGN_LEFT,
    wxALIGN_TOP,
    wxALIGN_RIGHT,
    wxALIGN_BOTTOM,
    wxALIGN_CENTER_VERTICAL,
    wxALIGN_CENTRE_VERTICAL,

    wxALIGN_CENTER,
    wxALIGN_CENTRE,

    wxALIGN_MASK,
};

enum wxSizerFlagBits
{
    wxFIXED_MINSIZE                = 0x8000,
    wxRESERVE_SPACE_EVEN_IF_HIDDEN = 0x0002,
    wxSIZER_FLAG_BITS_MASK         = 0x8002
};
%pythoncode { ADJUST_MINSIZE = 0 }

enum wxStretch
{
    wxSTRETCH_NOT,
    wxSHRINK,
    wxGROW,
    wxEXPAND,
    wxSHAPED,
    wxTILE,
    wxSTRETCH_MASK
};

enum wxBorder
{
    wxBORDER_DEFAULT,
    wxBORDER_NONE,
    wxBORDER_STATIC,
    wxBORDER_SIMPLE,
    wxBORDER_RAISED,
    wxBORDER_SUNKEN,
    wxBORDER_DOUBLE,
    wxBORDER_THEME,
    wxBORDER_MASK,
};


enum wxBackgroundStyle
{
    wxBG_STYLE_ERASE,
    wxBG_STYLE_SYSTEM,
    wxBG_STYLE_PAINT,
    wxBG_STYLE_TRANSPARENT,

    // these two are deprecated
    wxBG_STYLE_COLOUR,
    wxBG_STYLE_CUSTOM,
};


enum {
  wxDEFAULT ,
  wxDECORATIVE,
  wxROMAN,
  wxSCRIPT,
  wxSWISS,
  wxMODERN,
  wxTELETYPE,
  wxVARIABLE,
  wxFIXED,
  wxNORMAL,
  wxLIGHT,
  wxBOLD,
  wxITALIC,
  wxSLANT,
  wxSOLID,
  wxDOT,
  wxLONG_DASH,
  wxSHORT_DASH,
  wxDOT_DASH,
  wxUSER_DASH,
  wxTRANSPARENT,
  wxSTIPPLE,
  wxSTIPPLE_MASK,
  wxSTIPPLE_MASK_OPAQUE,
  wxBDIAGONAL_HATCH,
  wxCROSSDIAG_HATCH,
  wxFDIAGONAL_HATCH,
  wxCROSS_HATCH,
  wxHORIZONTAL_HATCH,
  wxVERTICAL_HATCH,
};


enum wxKeyCode {
    WXK_NONE = 0,
    
    WXK_CONTROL_A = 1,
    WXK_CONTROL_B,
    WXK_CONTROL_C,
    WXK_CONTROL_D,
    WXK_CONTROL_E,
    WXK_CONTROL_F,
    WXK_CONTROL_G,
    WXK_CONTROL_H,
    WXK_CONTROL_I,
    WXK_CONTROL_J,
    WXK_CONTROL_K,
    WXK_CONTROL_L,
    WXK_CONTROL_M,
    WXK_CONTROL_N,
    WXK_CONTROL_O,
    WXK_CONTROL_P,
    WXK_CONTROL_Q,
    WXK_CONTROL_R,
    WXK_CONTROL_S,
    WXK_CONTROL_T,
    WXK_CONTROL_U,
    WXK_CONTROL_V,
    WXK_CONTROL_W,
    WXK_CONTROL_X,
    WXK_CONTROL_Y,
    WXK_CONTROL_Z,
    
    WXK_BACK    =    8,
    WXK_TAB     =    9,
    WXK_RETURN  =    13,
    WXK_ESCAPE  =    27,
    WXK_SPACE   =    32,
    WXK_DELETE  =    127,

    WXK_START   = 300,
    WXK_LBUTTON,
    WXK_RBUTTON,
    WXK_CANCEL,
    WXK_MBUTTON,
    WXK_CLEAR,
    WXK_SHIFT,
    WXK_ALT,
    WXK_CONTROL,
    WXK_MENU,
    WXK_PAUSE,
    WXK_CAPITAL,
    WXK_END,
    WXK_HOME,
    WXK_LEFT,
    WXK_UP,
    WXK_RIGHT,
    WXK_DOWN,
    WXK_SELECT,
    WXK_PRINT,
    WXK_EXECUTE,
    WXK_SNAPSHOT,
    WXK_INSERT,
    WXK_HELP,
    WXK_NUMPAD0,
    WXK_NUMPAD1,
    WXK_NUMPAD2,
    WXK_NUMPAD3,
    WXK_NUMPAD4,
    WXK_NUMPAD5,
    WXK_NUMPAD6,
    WXK_NUMPAD7,
    WXK_NUMPAD8,
    WXK_NUMPAD9,
    WXK_MULTIPLY,
    WXK_ADD,
    WXK_SEPARATOR,
    WXK_SUBTRACT,
    WXK_DECIMAL,
    WXK_DIVIDE,
    WXK_F1,
    WXK_F2,
    WXK_F3,
    WXK_F4,
    WXK_F5,
    WXK_F6,
    WXK_F7,
    WXK_F8,
    WXK_F9,
    WXK_F10,
    WXK_F11,
    WXK_F12,
    WXK_F13,
    WXK_F14,
    WXK_F15,
    WXK_F16,
    WXK_F17,
    WXK_F18,
    WXK_F19,
    WXK_F20,
    WXK_F21,
    WXK_F22,
    WXK_F23,
    WXK_F24,
    WXK_NUMLOCK,
    WXK_SCROLL,
    WXK_PAGEUP,
    WXK_PAGEDOWN,

    WXK_NUMPAD_SPACE,
    WXK_NUMPAD_TAB,
    WXK_NUMPAD_ENTER,
    WXK_NUMPAD_F1,
    WXK_NUMPAD_F2,
    WXK_NUMPAD_F3,
    WXK_NUMPAD_F4,
    WXK_NUMPAD_HOME,
    WXK_NUMPAD_LEFT,
    WXK_NUMPAD_UP,
    WXK_NUMPAD_RIGHT,
    WXK_NUMPAD_DOWN,
    WXK_NUMPAD_PAGEUP,
    WXK_NUMPAD_PAGEDOWN,
    WXK_NUMPAD_END,
    WXK_NUMPAD_BEGIN,
    WXK_NUMPAD_INSERT,
    WXK_NUMPAD_DELETE,
    WXK_NUMPAD_EQUAL,
    WXK_NUMPAD_MULTIPLY,
    WXK_NUMPAD_ADD,
    WXK_NUMPAD_SEPARATOR,
    WXK_NUMPAD_SUBTRACT,
    WXK_NUMPAD_DECIMAL,
    WXK_NUMPAD_DIVIDE,

    WXK_WINDOWS_LEFT,
    WXK_WINDOWS_RIGHT,
    WXK_WINDOWS_MENU,
    WXK_RAW_CONTROL,
    WXK_COMMAND,

    // Hardware-specific buttons
    WXK_SPECIAL1 = 193,
    WXK_SPECIAL2,
    WXK_SPECIAL3,
    WXK_SPECIAL4,
    WXK_SPECIAL5,
    WXK_SPECIAL6,
    WXK_SPECIAL7,
    WXK_SPECIAL8,
    WXK_SPECIAL9,
    WXK_SPECIAL10,
    WXK_SPECIAL11,
    WXK_SPECIAL12,
    WXK_SPECIAL13,
    WXK_SPECIAL14,
    WXK_SPECIAL15,
    WXK_SPECIAL16,
    WXK_SPECIAL17,
    WXK_SPECIAL18,
    WXK_SPECIAL19,
    WXK_SPECIAL20
};

// deprecated synonymns
%pythoncode {
    WXK_PRIOR = WXK_PAGEUP
    WXK_NEXT  = WXK_PAGEDOWN
    WXK_NUMPAD_PRIOR = WXK_NUMPAD_PAGEUP
    WXK_NUMPAD_NEXT  = WXK_NUMPAD_PAGEDOWN    
}

typedef enum {
    wxPAPER_NONE,               // Use specific dimensions
    wxPAPER_LETTER,             // Letter, 8 1/2 by 11 inches
    wxPAPER_LEGAL,              // Legal, 8 1/2 by 14 inches
    wxPAPER_A4,                 // A4 Sheet, 210 by 297 millimeters
    wxPAPER_CSHEET,             // C Sheet, 17 by 22 inches
    wxPAPER_DSHEET,             // D Sheet, 22 by 34 inches
    wxPAPER_ESHEET,             // E Sheet, 34 by 44 inches
    wxPAPER_LETTERSMALL,        // Letter Small, 8 1/2 by 11 inches
    wxPAPER_TABLOID,            // Tabloid, 11 by 17 inches
    wxPAPER_LEDGER,             // Ledger, 17 by 11 inches
    wxPAPER_STATEMENT,          // Statement, 5 1/2 by 8 1/2 inches
    wxPAPER_EXECUTIVE,          // Executive, 7 1/4 by 10 1/2 inches
    wxPAPER_A3,                 // A3 sheet, 297 by 420 millimeters
    wxPAPER_A4SMALL,            // A4 small sheet, 210 by 297 millimeters
    wxPAPER_A5,                 // A5 sheet, 148 by 210 millimeters
    wxPAPER_B4,                 // B4 sheet, 250 by 354 millimeters
    wxPAPER_B5,                 // B5 sheet, 182-by-257-millimeter paper
    wxPAPER_FOLIO,              // Folio, 8-1/2-by-13-inch paper
    wxPAPER_QUARTO,             // Quarto, 215-by-275-millimeter paper
    wxPAPER_10X14,              // 10-by-14-inch sheet
    wxPAPER_11X17,              // 11-by-17-inch sheet
    wxPAPER_NOTE,               // Note, 8 1/2 by 11 inches
    wxPAPER_ENV_9,              // #9 Envelope, 3 7/8 by 8 7/8 inches
    wxPAPER_ENV_10,             // #10 Envelope, 4 1/8 by 9 1/2 inches
    wxPAPER_ENV_11,             // #11 Envelope, 4 1/2 by 10 3/8 inches
    wxPAPER_ENV_12,             // #12 Envelope, 4 3/4 by 11 inches
    wxPAPER_ENV_14,             // #14 Envelope, 5 by 11 1/2 inches
    wxPAPER_ENV_DL,             // DL Envelope, 110 by 220 millimeters
    wxPAPER_ENV_C5,             // C5 Envelope, 162 by 229 millimeters
    wxPAPER_ENV_C3,             // C3 Envelope, 324 by 458 millimeters
    wxPAPER_ENV_C4,             // C4 Envelope, 229 by 324 millimeters
    wxPAPER_ENV_C6,             // C6 Envelope, 114 by 162 millimeters
    wxPAPER_ENV_C65,            // C65 Envelope, 114 by 229 millimeters
    wxPAPER_ENV_B4,             // B4 Envelope, 250 by 353 millimeters
    wxPAPER_ENV_B5,             // B5 Envelope, 176 by 250 millimeters
    wxPAPER_ENV_B6,             // B6 Envelope, 176 by 125 millimeters
    wxPAPER_ENV_ITALY,          // Italy Envelope, 110 by 230 millimeters
    wxPAPER_ENV_MONARCH,        // Monarch Envelope, 3 7/8 by 7 1/2 inches
    wxPAPER_ENV_PERSONAL,       // 6 3/4 Envelope, 3 5/8 by 6 1/2 inches
    wxPAPER_FANFOLD_US,         // US Std Fanfold, 14 7/8 by 11 inches
    wxPAPER_FANFOLD_STD_GERMAN, // German Std Fanfold, 8 1/2 by 12 inches
    wxPAPER_FANFOLD_LGL_GERMAN, // German Legal Fanfold, 8 1/2 by 13 inches

    wxPAPER_ISO_B4,             // B4 (ISO) 250 x 353 mm
    wxPAPER_JAPANESE_POSTCARD,  // Japanese Postcard 100 x 148 mm
    wxPAPER_9X11,               // 9 x 11 in
    wxPAPER_10X11,              // 10 x 11 in
    wxPAPER_15X11,              // 15 x 11 in
    wxPAPER_ENV_INVITE,         // Envelope Invite 220 x 220 mm
    wxPAPER_LETTER_EXTRA,       // Letter Extra 9 \275 x 12 in
    wxPAPER_LEGAL_EXTRA,        // Legal Extra 9 \275 x 15 in
    wxPAPER_TABLOID_EXTRA,      // Tabloid Extra 11.69 x 18 in
    wxPAPER_A4_EXTRA,           // A4 Extra 9.27 x 12.69 in
    wxPAPER_LETTER_TRANSVERSE,  // Letter Transverse 8 \275 x 11 in
    wxPAPER_A4_TRANSVERSE,      // A4 Transverse 210 x 297 mm
    wxPAPER_LETTER_EXTRA_TRANSVERSE, // Letter Extra Transverse 9\275 x 12 in
    wxPAPER_A_PLUS,             // SuperA/SuperA/A4 227 x 356 mm
    wxPAPER_B_PLUS,             // SuperB/SuperB/A3 305 x 487 mm
    wxPAPER_LETTER_PLUS,        // Letter Plus 8.5 x 12.69 in
    wxPAPER_A4_PLUS,            // A4 Plus 210 x 330 mm
    wxPAPER_A5_TRANSVERSE,      // A5 Transverse 148 x 210 mm
    wxPAPER_B5_TRANSVERSE,      // B5 (JIS) Transverse 182 x 257 mm
    wxPAPER_A3_EXTRA,           // A3 Extra 322 x 445 mm
    wxPAPER_A5_EXTRA,           // A5 Extra 174 x 235 mm
    wxPAPER_B5_EXTRA,           // B5 (ISO) Extra 201 x 276 mm
    wxPAPER_A2,                 // A2 420 x 594 mm
    wxPAPER_A3_TRANSVERSE,      // A3 Transverse 297 x 420 mm
    wxPAPER_A3_EXTRA_TRANSVERSE, // A3 Extra Transverse 322 x 445 mm

    wxPAPER_DBL_JAPANESE_POSTCARD,/* Japanese Double Postcard 200 x 148 mm */
    wxPAPER_A6,                 /* A6 105 x 148 mm */
    wxPAPER_JENV_KAKU2,         /* Japanese Envelope Kaku #2 */
    wxPAPER_JENV_KAKU3,         /* Japanese Envelope Kaku #3 */
    wxPAPER_JENV_CHOU3,         /* Japanese Envelope Chou #3 */
    wxPAPER_JENV_CHOU4,         /* Japanese Envelope Chou #4 */
    wxPAPER_LETTER_ROTATED,     /* Letter Rotated 11 x 8 1/2 in */
    wxPAPER_A3_ROTATED,         /* A3 Rotated 420 x 297 mm */
    wxPAPER_A4_ROTATED,         /* A4 Rotated 297 x 210 mm */
    wxPAPER_A5_ROTATED,         /* A5 Rotated 210 x 148 mm */
    wxPAPER_B4_JIS_ROTATED,     /* B4 (JIS) Rotated 364 x 257 mm */
    wxPAPER_B5_JIS_ROTATED,     /* B5 (JIS) Rotated 257 x 182 mm */
    wxPAPER_JAPANESE_POSTCARD_ROTATED,/* Japanese Postcard Rotated 148 x 100 mm */
    wxPAPER_DBL_JAPANESE_POSTCARD_ROTATED,/* Double Japanese Postcard Rotated 148 x 200 mm */
    wxPAPER_A6_ROTATED,         /* A6 Rotated 148 x 105 mm */
    wxPAPER_JENV_KAKU2_ROTATED, /* Japanese Envelope Kaku #2 Rotated */
    wxPAPER_JENV_KAKU3_ROTATED, /* Japanese Envelope Kaku #3 Rotated */
    wxPAPER_JENV_CHOU3_ROTATED, /* Japanese Envelope Chou #3 Rotated */
    wxPAPER_JENV_CHOU4_ROTATED, /* Japanese Envelope Chou #4 Rotated */
    wxPAPER_B6_JIS,             /* B6 (JIS) 128 x 182 mm */
    wxPAPER_B6_JIS_ROTATED,     /* B6 (JIS) Rotated 182 x 128 mm */
    wxPAPER_12X11,              /* 12 x 11 in */
    wxPAPER_JENV_YOU4,          /* Japanese Envelope You #4 */
    wxPAPER_JENV_YOU4_ROTATED,  /* Japanese Envelope You #4 Rotated */
    wxPAPER_P16K,               /* PRC 16K 146 x 215 mm */
    wxPAPER_P32K,               /* PRC 32K 97 x 151 mm */
    wxPAPER_P32KBIG,            /* PRC 32K(Big) 97 x 151 mm */
    wxPAPER_PENV_1,             /* PRC Envelope #1 102 x 165 mm */
    wxPAPER_PENV_2,             /* PRC Envelope #2 102 x 176 mm */
    wxPAPER_PENV_3,             /* PRC Envelope #3 125 x 176 mm */
    wxPAPER_PENV_4,             /* PRC Envelope #4 110 x 208 mm */
    wxPAPER_PENV_5,             /* PRC Envelope #5 110 x 220 mm */
    wxPAPER_PENV_6,             /* PRC Envelope #6 120 x 230 mm */
    wxPAPER_PENV_7,             /* PRC Envelope #7 160 x 230 mm */
    wxPAPER_PENV_8,             /* PRC Envelope #8 120 x 309 mm */
    wxPAPER_PENV_9,             /* PRC Envelope #9 229 x 324 mm */
    wxPAPER_PENV_10,            /* PRC Envelope #10 324 x 458 mm */
    wxPAPER_P16K_ROTATED,       /* PRC 16K Rotated */
    wxPAPER_P32K_ROTATED,       /* PRC 32K Rotated */
    wxPAPER_P32KBIG_ROTATED,    /* PRC 32K(Big) Rotated */
    wxPAPER_PENV_1_ROTATED,     /* PRC Envelope #1 Rotated 165 x 102 mm */
    wxPAPER_PENV_2_ROTATED,     /* PRC Envelope #2 Rotated 176 x 102 mm */
    wxPAPER_PENV_3_ROTATED,     /* PRC Envelope #3 Rotated 176 x 125 mm */
    wxPAPER_PENV_4_ROTATED,     /* PRC Envelope #4 Rotated 208 x 110 mm */
    wxPAPER_PENV_5_ROTATED,     /* PRC Envelope #5 Rotated 220 x 110 mm */
    wxPAPER_PENV_6_ROTATED,     /* PRC Envelope #6 Rotated 230 x 120 mm */
    wxPAPER_PENV_7_ROTATED,     /* PRC Envelope #7 Rotated 230 x 160 mm */
    wxPAPER_PENV_8_ROTATED,     /* PRC Envelope #8 Rotated 309 x 120 mm */
    wxPAPER_PENV_9_ROTATED,     /* PRC Envelope #9 Rotated 324 x 229 mm */
    wxPAPER_PENV_10_ROTATED,    /* PRC Envelope #10 Rotated 458 x 324 m */
    wxPAPER_A0,                 /* A0 Sheet 841 x 1189 mm */
    wxPAPER_A1                  /* A1 Sheet 594 x 841 mm */
   
} wxPaperSize;


/* Printing orientation */
enum wxPrintOrientation
{
   wxPORTRAIT = 1,
   wxLANDSCAPE
};

typedef enum {
    wxDUPLEX_SIMPLEX, // Non-duplex
    wxDUPLEX_HORIZONTAL,
    wxDUPLEX_VERTICAL
} wxDuplexMode;



// menu and toolbar item kinds
enum wxItemKind
{
    wxITEM_SEPARATOR,
    wxITEM_NORMAL,
    wxITEM_CHECK,
    wxITEM_RADIO,
    wxITEM_DROPDOWN,
    wxITEM_MAX
};


enum wxCheckBoxState
{
    wxCHK_UNCHECKED,
    wxCHK_CHECKED,
    wxCHK_UNDETERMINED /* 3-state checkbox only */
};

enum wxHitTest
{
    wxHT_NOWHERE,

    // scrollbar
    wxHT_SCROLLBAR_FIRST = wxHT_NOWHERE,
    wxHT_SCROLLBAR_ARROW_LINE_1,    // left or upper arrow to scroll by line
    wxHT_SCROLLBAR_ARROW_LINE_2,    // right or down
    wxHT_SCROLLBAR_ARROW_PAGE_1,    // left or upper arrow to scroll by page
    wxHT_SCROLLBAR_ARROW_PAGE_2,    // right or down
    wxHT_SCROLLBAR_THUMB,           // on the thumb
    wxHT_SCROLLBAR_BAR_1,           // bar to the left/above the thumb
    wxHT_SCROLLBAR_BAR_2,           // bar to the right/below the thumb
    wxHT_SCROLLBAR_LAST,

    // window
    wxHT_WINDOW_OUTSIDE,            // not in this window at all
    wxHT_WINDOW_INSIDE,             // in the client area
    wxHT_WINDOW_VERT_SCROLLBAR,     // on the vertical scrollbar
    wxHT_WINDOW_HORZ_SCROLLBAR,     // on the horizontal scrollbar
    wxHT_WINDOW_CORNER,             // on the corner between 2 scrollbars

    wxHT_MAX
};



enum wxKeyModifier
{
    wxMOD_NONE,
    wxMOD_ALT,
    wxMOD_CONTROL,
    wxMOD_ALTGR,
    wxMOD_SHIFT,
    wxMOD_META,
    wxMOD_WIN,
    wxMOD_RAW_CONTROL,
    wxMOD_CMD,
    wxMOD_ALL       
};


enum wxUpdateUI
{
    wxUPDATE_UI_NONE          = 0x0000,
    wxUPDATE_UI_RECURSE       = 0x0001,
    wxUPDATE_UI_FROMIDLE      = 0x0002 // Invoked from On(Internal)Idle
};


// enum wxNotificationOptions
// {
//     wxNOTIFY_NONE           = 0x0000,
//     wxNOTIFY_ONCE           = 0x0001,
//     wxNOTIFY_REPEAT         = 0x0002
// };


enum wxLayoutDirection
{
    wxLayout_Default,
    wxLayout_LeftToRight,
    wxLayout_RightToLeft
};



//---------------------------------------------------------------------------

