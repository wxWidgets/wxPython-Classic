/////////////////////////////////////////////////////////////////////////////
// Name:        _colour.i
// Purpose:     SWIG interface for wxColour
//
// Author:      Robin Dunn
//
// Created:     7-July-1997
// RCS-ID:      $Id$
// Copyright:   (c) 2003 by Total Control Software
// Licence:     wxWindows license
/////////////////////////////////////////////////////////////////////////////

// Not a %module


%{
#ifdef __WXMAC__
#include <wx/osx/private.h>
#endif
%}

//---------------------------------------------------------------------------
%newgroup;


enum {
    wxC2S_NAME,             // return colour name, when possible
    wxC2S_CSS_SYNTAX,       // return colour in rgb(r,g,b) syntax
    wxC2S_HTML_SYNTAX,      // return colour in #rrggbb syntax     
};

enum {
    wxALPHA_TRANSPARENT,
    wxALPHA_OPAQUE
};


DocStr(wxColour,
"A colour is an object representing a combination of Red, Green, and
Blue (RGB) intensity values, and is used to determine drawing colours,
window colours, etc.  Valid RGB values are in the range 0 to 255.

In wxPython there are typemaps that will automatically convert from a
colour name, from a '#RRGGBB' colour hex value string, or from a 3 or 4
integer tuple to a wx.Colour object when calling C++ methods that
expect a wxColour.  This means that the following are all
equivallent::

    win.SetBackgroundColour(wxColour(0,0,255))
    win.SetBackgroundColour('BLUE')
    win.SetBackgroundColour('#0000FF')
    win.SetBackgroundColour((0,0,255))

In addition to the RGB values, the alpha transparency can optionally
be set.  This is supported by the typemaps as well as the wx.Colour
constructors and setters.  (The alpha value is ignored in many places
that take a wx.Colour object, but it is honored in things like wx.GCDC
or wx.GraphicsContext.)  Adding an alpha value of 0xC0 (192) to the
above samples looks like this:

    win.SetBackgroundColour(wxColour(0,0,255,192))
    win.SetBackgroundColour('BLUE:C0')
    win.SetBackgroundColour('#0000FFC0')
    win.SetBackgroundColour((0,0,255,192))

Additional colour names and their coresponding values can be added
using `wx.ColourDatabase`. Also see `wx.lib.colourdb` for a large set
of colour names and values.  Various system colours (as set in the
user's system preferences or control panel) can be retrieved with
`wx.SystemSettings.GetColour`.
", "");


MustHaveApp( wxColour(const wxString& colorName) );

class wxColour : public wxObject {
public:
    
    DocCtorStr(
        wxColour(byte red=0, byte green=0, byte blue=0, byte alpha=wxALPHA_OPAQUE),
        "Constructs a colour from red, green, blue and alpha values.

:see: Alternate constructors `wx.NamedColour`, `wx.ColourRGB` and `MacThemeColour`.
", "");
    
    %RenameADocCtor(
        NamedColour,
        "NamedColour(String colourName) -> Colour",
        "Constructs a colour object using a colour name listed in
``wx.TheColourDatabase``, or any string format supported by the
wxColour typemaps.", "",
        // NOTE: We say String in the docstring but use wxColour for
        // real so the typemap will be applied.
        wxColour( const wxColour& colourName ));

    
    %RenameDocCtor(
        ColourRGB,
        "Constructs a colour from a packed RGB value.", "",
        wxColour( unsigned long colRGB ));

    %extend {
        %RenameDocCtor(
            MacThemeColour,
            "Creates a color (or pattern) from a Mac theme brush ID.  Raises a
NotImplemented exception on other platforms.", "",
            wxColour( int themeBrushID ))
            {
#ifdef __WXMAC__
                return new wxColour(wxMacCreateCGColorFromHITheme(themeBrushID));
#else
                wxPyRaiseNotImplemented(); return NULL;
#endif
            }
    }
    
    ~wxColour();

    
    DocDeclStr(
        byte , Red(),
        "Returns the red intensity.", "");
    
    DocDeclStr(
        byte , Green(),
        "Returns the green intensity.", "");
    
    DocDeclStr(
        byte , Blue(),
        "Returns the blue intensity.", "");
    
    DocDeclStr(
        byte , Alpha(),
        "Returns the Alpha value.", "");
    
    DocDeclStr(
        bool , IsOk(),
        "Returns True if the colour object is valid (the colour has been
initialised with RGB values).", "");
    %pythoncode { Ok = IsOk }
    
    DocDeclStr(
        void , Set(byte red, byte green, byte blue, byte alpha=wxALPHA_OPAQUE),
        "Sets the RGB intensity values.", "");

    %pythoncode {
        def SetFromString(self, colourName):
            """
            Sets the RGB intensity values using a colour name listed in
            ``wx.TheColourDatabase``, or any string format supported by
            the wxColour typemaps.
            """
            c = wx.NamedColour(colourName)
            self.Set(c.red, c.green, c.blue, c.alpha)
        SetFromName = SetFromString
    }

    // TODO: This needs to be updated to include alpha in the html
    // syntax to match our typemaps
    DocDeclStr(
        wxString , GetAsString(long flags = wxC2S_NAME | wxC2S_CSS_SYNTAX) const,
        "Return the colour as a string.  Acceptable flags are:

            =================== ==================================
            wx.C2S_NAME          return colour name, when possible
            wx.C2S_CSS_SYNTAX    return colour in rgb(r,g,b) syntax
            wx.C2S_HTML_SYNTAX   return colour in #rrggbb syntax     
            =================== ==================================", "");

    
    DocDeclStr(
        void , SetRGB(wxUint32 colRGB),
        "Sets the RGB colour values from a single 32 bit value.

The argument colRGB should be of the form 0x00BBGGRR and where 0xRR,
0xGG and 0xBB are the values of the red, green and blue components.", "");
    
    DocDeclStr(
        void , SetRGBA(wxUint32 colRGBA),
        "Sets the RGBA colour values from a single 32 bit value.

The argument colRGBA should be of the form 0xAABBGGRR where 0xRR,
0xGG, 0xBB and 0xAA are the values of the red, green, blue and alpha
components.", "");
    
    DocDeclStr(
        wxUint32 , GetRGB() const,
        "", "");
    
    DocDeclStr(
        wxUint32 , GetRGBA() const,
        "", "");
    

    
    // TODO: deal with these...
    
    // static void MakeMono    (byte* r, byte* g, byte* b, bool on);
    // static void MakeDisabled(byte* r, byte* g, byte* b, byte brightness = 255);
    // static void MakeGrey    (byte* r, byte* g, byte* b); // integer version
    // static void MakeGrey    (byte* r, byte* g, byte* b, 
    //                          double weight_r, double weight_g, double weight_b); // floating point version
    // static byte AlphaBlend  (byte fg, byte bg, double alpha);
    // static void ChangeLightness(byte* r, byte* g, byte* b, int ialpha);
    // wxColour ChangeLightness(int ialpha) const;

    
    %extend {
        DocStr(GetPixel, 
        "Returns a pixel value which is platform-dependent. On Windows, a
COLORREF is returned. On X, an allocated pixel value is returned.  -1
is returned if the pixel is invalid (on X, unallocated).", "");

        long GetPixel() {
            %#ifndef __WXGTK3__
                return (long)self->GetPixel();
            %#else
                return -1;
            %#endif
        }
    }
    
    %extend {
        KeepGIL(__eq__);
        DocStr(__eq__, "Compare colours for equality.", "");
        bool __eq__(PyObject* other) {
            wxColour  temp, *obj = &temp;
            if ( other == Py_None ) return false;
            if ( ! wxColour_helper(other, &obj) ) {
                PyErr_Clear();
                return false;
            }
            return self->operator==(*obj);
        }

        
        KeepGIL(__ne__);
        DocStr(__ne__, "Compare colours for inequality.", "");
        bool __ne__(PyObject* other) {
            wxColour  temp, *obj = &temp;
            if ( other == Py_None ) return true;
            if ( ! wxColour_helper(other, &obj)) {
                PyErr_Clear();
                return true;
            }
            return self->operator!=(*obj);
        }
    }


    %extend {
        KeepGIL(Get);
        DocAStr(Get,
                "Get(self, bool includeAlpha=False) -> (r,g,b) or (r,g,b,a)",
                "Returns the RGB intensity values as a tuple, optionally the alpha value as well.", "");
        PyObject* Get(bool includeAlpha=false) {
            PyObject* rv = PyTuple_New(includeAlpha ? 4 : 3);
            int red = -1;
            int green = -1;
            int blue = -1;
            int alpha = wxALPHA_OPAQUE;
            if (self->IsOk()) {
                red =   self->Red();
                green = self->Green();
                blue =  self->Blue();
                alpha = self->Alpha();
            }
            PyTuple_SetItem(rv, 0, PyInt_FromLong(red));
            PyTuple_SetItem(rv, 1, PyInt_FromLong(green));
            PyTuple_SetItem(rv, 2, PyInt_FromLong(blue));
            if (includeAlpha)
                PyTuple_SetItem(rv, 3, PyInt_FromLong(alpha));                
            return rv;
        }

        KeepGIL(GetRGB);
        DocStr(GetRGB,
               "Return the colour as a packed RGB value", "");
        unsigned long GetRGB() {
            return self->Red() | (self->Green() << 8) | (self->Blue() << 16);
        }
    }


    %pythoncode {
        asTuple = wx.deprecated(Get, "asTuple is deprecated, use `Get` instead")
        def __str__(self):                  return str(self.Get(True))

        %# help() can access the stock colors before they are created,  
        %# so make sure there is a this attribute before calling any wrapper method.
        def __repr__(self): 
            if hasattr(self, 'this'):
                return 'wx.Colour' + str(self.Get(True))
            else:
                return 'wx.Colour()'

        def __len__(self):                  return len(self.Get())
        def __getitem__(self, index):       return self.Get()[index]
        def __nonzero__(self):              return self.IsOk()
        __safe_for_unpickling__ = True
        def __reduce__(self):               return (Colour, self.Get(True))
        }

    %property(Pixel, GetPixel, doc="See `GetPixel`");
    %property(RGB, GetRGB, SetRGB, doc="See `GetRGB` and `SetRGB`");
    %property(red,   Red);
    %property(green, Green);
    %property(blue,  Blue);
    %property(alpha, Alpha);                           
};

//---------------------------------------------------------------------------

