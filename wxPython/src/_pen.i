/////////////////////////////////////////////////////////////////////////////
// Name:        _pen.i
// Purpose:     SWIG interface for wxPen
//
// Author:      Robin Dunn
//
// Created:     7-July-1997
// RCS-ID:      $Id$
// Copyright:   (c) 2003 by Total Control Software
// Licence:     wxWindows license
/////////////////////////////////////////////////////////////////////////////

// Not a %module


//---------------------------------------------------------------------------

// wxDash is a signed char, byte is unsigned char...
%typemap(in) (int dashes, wxDash* dashes_array ) {
    $1 = PyList_Size($input);
    $2 = (wxDash*)byte_LIST_helper($input);
    if ($2 == NULL) SWIG_fail;
}
%typemap(freearg) (int dashes, wxDash* dashes_array ) {
    if ($2) delete [] $2;
}

//---------------------------------------------------------------------------
%newgroup


enum wxPenStyle
{
    wxPENSTYLE_INVALID,

    wxPENSTYLE_SOLID,
    wxPENSTYLE_DOT,
    wxPENSTYLE_LONG_DASH,
    wxPENSTYLE_SHORT_DASH,
    wxPENSTYLE_DOT_DASH,
    wxPENSTYLE_USER_DASH,

    wxPENSTYLE_TRANSPARENT,

    wxPENSTYLE_STIPPLE_MASK_OPAQUE,
    wxPENSTYLE_STIPPLE_MASK,
    wxPENSTYLE_STIPPLE,

    wxPENSTYLE_BDIAGONAL_HATCH,
    wxPENSTYLE_CROSSDIAG_HATCH,
    wxPENSTYLE_FDIAGONAL_HATCH,
    wxPENSTYLE_CROSS_HATCH,
    wxPENSTYLE_HORIZONTAL_HATCH,
    wxPENSTYLE_VERTICAL_HATCH,

    wxPENSTYLE_FIRST_HATCH,
    wxPENSTYLE_LAST_HATCH,
};

enum wxPenJoin
{
    wxJOIN_INVALID,

    wxJOIN_BEVEL,
    wxJOIN_MITER,
    wxJOIN_ROUND,
};

enum wxPenCap
{
    wxCAP_INVALID,

    wxCAP_ROUND,
    wxCAP_PROJECTING,
    wxCAP_BUTT
};





MustHaveApp(wxPen);

class wxPen : public wxGDIObject {
public:
    wxPen(wxColour& colour, int width=1, wxPenStyle style=wxSOLID);
    ~wxPen();

    wxPenCap GetCap();
    wxColour GetColour();
    wxPenJoin GetJoin();
    wxPenStyle GetStyle();
    int GetWidth();

    bool IsOk();
    %pythoncode { Ok = IsOk }

    void SetCap(wxPenCap cap_style);
    void SetColour(wxColour& colour);
    void SetJoin(wxPenJoin join_style);
    void SetStyle(wxPenStyle style);
    void SetWidth(int width);

    void SetDashes(int dashes, wxDash* dashes_array);
    //int GetDashes(wxDash **dashes);
    %extend {
        PyObject* GetDashes() {
            wxDash* dashes;
            int count = self->GetDashes(&dashes);
            wxPyBlock_t blocked = wxPyBeginBlockThreads();
            PyObject* retval = PyList_New(0);
            for (int x=0; x<count; x++) {
                PyObject* pyint = PyInt_FromLong(dashes[x]);
                PyList_Append(retval, pyint);
                Py_DECREF(pyint);
            }
            wxPyEndBlockThreads(blocked);
            return retval;
        }

        void _SetDashes(PyObject* _self, PyObject* pyDashes) {
            wxPyBlock_t blocked = wxPyBeginBlockThreads();
            int size = PyList_Size(pyDashes);
            wxDash* dashes = (wxDash*)byte_LIST_helper(pyDashes);

            // black magic warning!  The array of wxDashes needs to exist as
            // long as the pen does because wxPen does not copy the array.  So
            // stick a copy in a Python string object and attach it to _self,
            // and then call SetDashes with a pointer to that array.  Then
            // when the Python pen object is destroyed the array will be
            // cleaned up too.
            PyObject* strDashes = PyString_FromStringAndSize((char*)dashes, size*sizeof(wxDash));
            PyObject_SetAttrString(_self, "_dashes", strDashes);
                        
            self->SetDashes(size, (wxDash*)PyString_AS_STRING(strDashes));
            delete [] dashes;
            Py_DECREF(strDashes);
            wxPyEndBlockThreads(blocked);
        }
    }
    %pythoncode {
    def SetDashes(self, dashes):
        """
        Associate a list of dash lengths with the Pen.
        """
        self._SetDashes(self, dashes)
    }

    
#ifndef __WXMAC__
    int GetDashCount() const;
    %property(DashCount, GetDashCount, doc="See `GetDashCount`");
#endif
    
#ifdef __WXMSW__
    wxBitmap* GetStipple();
    void SetStipple(wxBitmap& stipple);
    %property(Stipple, GetStipple, SetStipple, doc="See `GetStipple` and `SetStipple`");
#endif

    bool IsTransparent() const;
    bool IsNonTransparent() const;
    

    %extend {
        bool __eq__(const wxPen* other) { return other ? (*self == *other) : false; }
        bool __ne__(const wxPen* other) { return other ? (*self != *other) : true;  }
    }
    %pythoncode { def __nonzero__(self): return self.IsOk() }

    %property(Cap, GetCap, SetCap, doc="See `GetCap` and `SetCap`");
    %property(Colour, GetColour, SetColour, doc="See `GetColour` and `SetColour`");
    %property(Dashes, GetDashes, SetDashes, doc="See `GetDashes` and `SetDashes`");
    %property(Join, GetJoin, SetJoin, doc="See `GetJoin` and `SetJoin`");
    %property(Style, GetStyle, SetStyle, doc="See `GetStyle` and `SetStyle`");
    %property(Width, GetWidth, SetWidth, doc="See `GetWidth` and `SetWidth`");
};


//---------------------------------------------------------------------------
