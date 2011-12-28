/////////////////////////////////////////////////////////////////////////////
// Name:        _graphics.i
// Purpose:     Wrapper definitions for wx.GraphicsPath, wx.GraphicsContext
//
// Author:      Robin Dunn
//
// Created:     2-Oct-2006
// RCS-ID:      $Id$
// Copyright:   (c) 2006 by Total Control Software
// Licence:     wxWindows license
/////////////////////////////////////////////////////////////////////////////

// Not a %module


//---------------------------------------------------------------------------
%newgroup

%{
#include <wx/graphics.h>
%}

enum wxAntialiasMode
{
    wxANTIALIAS_NONE, // should be 0
    wxANTIALIAS_DEFAULT,
};

enum wxInterpolationQuality
{
    // default interpolation
    wxINTERPOLATION_DEFAULT,
    // no interpolation
    wxINTERPOLATION_NONE, 
    // fast interpolation, suited for interactivity
    wxINTERPOLATION_FAST,
    // better quality
    wxINTERPOLATION_GOOD,
    // best quality, not suited for interactivity
    wxINTERPOLATION_BEST
};


enum wxCompositionMode
{
    // R = Result, S = Source, D = Destination, premultiplied with alpha
    // Ra, Sa, Da their alpha components
    
    // classic Porter-Duff compositions
    // http://keithp.com/~keithp/porterduff/p253-porter.pdf

    wxCOMPOSITION_INVALID,
    
    wxCOMPOSITION_CLEAR, /* R = 0 */
    wxCOMPOSITION_SOURCE, /* R = S */
    wxCOMPOSITION_OVER, /* R = S + D*(1 - Sa) */
    wxCOMPOSITION_IN, /* R = S*Da */
    wxCOMPOSITION_OUT, /* R = S*(1 - Da) */
    wxCOMPOSITION_ATOP, /* R = S*Da + D*(1 - Sa) */

    wxCOMPOSITION_DEST, /* R = D, essentially a noop */
    wxCOMPOSITION_DEST_OVER, /* R = S*(1 - Da) + D */
    wxCOMPOSITION_DEST_IN, /* R = D*Sa */
    wxCOMPOSITION_DEST_OUT, /* R = D*(1 - Sa) */
    wxCOMPOSITION_DEST_ATOP, /* R = S*(1 - Da) + D*Sa */
    wxCOMPOSITION_XOR, /* R = S*(1 - Da) + D*(1 - Sa) */
    
    // mathematical compositions
    wxCOMPOSITION_ADD, /* R = S + D */
};

// Turn off the aquisition of the Global Interpreter Lock for the classes and
// functions in this file
%threadWrapperOff


//---------------------------------------------------------------------------
//---------------------------------------------------------------------------

%{
#if !wxUSE_GRAPHICS_CONTEXT
// C++ stub classes for platforms or build configurations that don't have
// wxGraphicsContext yet.

enum wxAntialiasMode
{
    wxANTIALIAS_NONE, // should be 0
    wxANTIALIAS_DEFAULT,
};

enum wxInterpolationQuality
{
    // default interpolation
    wxINTERPOLATION_DEFAULT,
    // no interpolation
    wxINTERPOLATION_NONE, 
    // fast interpolation, suited for interactivity
    wxINTERPOLATION_FAST,
    // better quality
    wxINTERPOLATION_GOOD,
    // best quality, not suited for interactivity
    wxINTERPOLATION_BEST
};

enum wxCompositionMode
{
    // R = Result, S = Source, D = Destination, premultiplied with alpha
    // Ra, Sa, Da their alpha components
    
    // classic Porter-Duff compositions
    // http://keithp.com/~keithp/porterduff/p253-porter.pdf
    
    wxCOMPOSITION_INVALID,

    wxCOMPOSITION_CLEAR, /* R = 0 */
    wxCOMPOSITION_SOURCE, /* R = S */
    wxCOMPOSITION_OVER, /* R = S + D*(1 - Sa) */
    wxCOMPOSITION_IN, /* R = S*Da */
    wxCOMPOSITION_OUT, /* R = S*(1 - Da) */
    wxCOMPOSITION_ATOP, /* R = S*Da + D*(1 - Sa) */

    wxCOMPOSITION_DEST, /* R = D, essentially a noop */
    wxCOMPOSITION_DEST_OVER, /* R = S*(1 - Da) + D */
    wxCOMPOSITION_DEST_IN, /* R = D*Sa */
    wxCOMPOSITION_DEST_OUT, /* R = D*(1 - Sa) */
    wxCOMPOSITION_DEST_ATOP, /* R = S*(1 - Da) + D*Sa */
    wxCOMPOSITION_XOR, /* R = S*(1 - Da) + D*(1 - Sa) */
    
    // mathematical compositions
    wxCOMPOSITION_ADD, /* R = S + D */
};
    
class wxGraphicsRenderer;
class wxGraphicsMatrix;


class wxGraphicsObject : public wxObject
{
public :
    wxGraphicsObject() {}
    wxGraphicsObject( wxGraphicsRenderer*  ) {
        PyErr_SetString(PyExc_NotImplementedError,
                        "wx.GraphicsObject is not available on this platform.");
    }
    wxGraphicsObject( const wxGraphicsObject&  ) {}
    virtual ~wxGraphicsObject() {}
    bool IsNull() const { return false; }
    wxGraphicsRenderer* GetRenderer() const { return NULL; }
} ;



class wxGraphicsPen : public wxGraphicsObject
{
public:
    wxGraphicsPen()  {}
    virtual ~wxGraphicsPen() {}
} ;
wxGraphicsPen wxNullGraphicsPen;



class wxGraphicsBrush : public wxGraphicsObject
{
public :
    wxGraphicsBrush() {}
    virtual ~wxGraphicsBrush() {}
} ;
wxGraphicsBrush wxNullGraphicsBrush;



class wxGraphicsFont : public wxGraphicsObject
{
public :
    wxGraphicsFont() {}
    virtual ~wxGraphicsFont() {}
} ;
wxGraphicsFont wxNullGraphicsFont;


class wxGraphicsBitmap : public wxGraphicsObject
{
public :
    wxGraphicsBitmap() {}
    virtual ~wxGraphicsBitmap() {}
} ;
wxGraphicsBitmap wxNullGraphicsBitmap;



class wxGraphicsPath : public wxGraphicsObject
{
public :
    wxGraphicsPath() { }
    wxGraphicsPath(wxGraphicsRenderer* ) {
        PyErr_SetString(PyExc_NotImplementedError,
                        "wx.GraphicsPath is not available on this platform.");
    }
    virtual ~wxGraphicsPath() {}

    void MoveToPoint( wxDouble, wxDouble ) {}
    void MoveToPoint( const wxPoint2DDouble& ) {}
    void AddLineToPoint( wxDouble, wxDouble ) {}
    void AddLineToPoint( const wxPoint2DDouble& ) {}
    void AddCurveToPoint( wxDouble, wxDouble, wxDouble, wxDouble, wxDouble, wxDouble ) {}
    void AddCurveToPoint( const wxPoint2DDouble&, const wxPoint2DDouble&, const wxPoint2DDouble&) {}
    void AddPath( const wxGraphicsPath& ) {}
    void CloseSubpath() {}
    void GetCurrentPoint( wxDouble&, wxDouble&) const {}
    wxPoint2DDouble GetCurrentPoint() const { return wxPoint2D(0,0); }
    void AddArc( wxDouble, wxDouble, wxDouble, wxDouble, wxDouble, bool ) {}
    void AddArc( const wxPoint2DDouble& , wxDouble, wxDouble , wxDouble , bool ) {}

    void AddQuadCurveToPoint( wxDouble, wxDouble, wxDouble, wxDouble ) {}
    void AddRectangle( wxDouble, wxDouble, wxDouble, wxDouble ) {}
    void AddCircle( wxDouble, wxDouble, wxDouble ) {}
    void AddArcToPoint( wxDouble, wxDouble , wxDouble, wxDouble, wxDouble )  {}

    void AddEllipse( wxDouble , wxDouble , wxDouble , wxDouble ) {}
    void AddRoundedRectangle( wxDouble , wxDouble , wxDouble , wxDouble , wxDouble ) {}
    void * GetNativePath() const { return NULL; }
    void UnGetNativePath(void *) const {}
    void Transform( const wxGraphicsMatrix& ) {}
    void GetBox(wxDouble *, wxDouble *, wxDouble *, wxDouble *) const {}
    wxRect2D GetBox() const { return wxRect2D(0,0,0,0); }

    bool Contains( wxDouble , wxDouble , wxPolygonFillMode ) const { return false; }
    bool Contains( const wxPoint2DDouble& , wxPolygonFillMode ) const { return false; }
};
wxGraphicsPath wxNullGraphicsPath;


class wxGraphicsMatrix : public wxGraphicsObject
{
public :
    wxGraphicsMatrix() { }
    wxGraphicsMatrix(wxGraphicsRenderer* ) {
        PyErr_SetString(PyExc_NotImplementedError,
                        "wx.GraphicsMatrix is not available on this platform.");
    }
    virtual ~wxGraphicsMatrix() {}
    virtual void Concat( const wxGraphicsMatrix & ) {}
    virtual void Copy( const wxGraphicsMatrix & )  {}
    virtual void Set(wxDouble , wxDouble , wxDouble , wxDouble ,
                     wxDouble , wxDouble ) {}
    virtual void Get(wxDouble*, wxDouble*, wxDouble*,
                     wxDouble*, wxDouble*, wxDouble*) {}
    virtual void Invert() {}
    virtual bool IsEqual( const wxGraphicsMatrix& t) const  { return false; }
    virtual bool IsIdentity() const { return false; }
    virtual void Translate( wxDouble , wxDouble ) {}
    virtual void Scale( wxDouble , wxDouble  ) {}
    virtual void Rotate( wxDouble  ) {}
    virtual void TransformPoint( wxDouble *, wxDouble * ) const {}
    virtual void TransformDistance( wxDouble *, wxDouble * ) const {}
    virtual void * GetNativeMatrix() const { return NULL; }
};
wxGraphicsMatrix wxNullGraphicsMatrix;


class wxGraphicsGradientStop
{
public:
    wxGraphicsGradientStop(wxColour col = wxTransparentColour,
                           float pos = 0.0) {} 
    ~wxGraphicsGradientStop() {}
    
    const wxColour& GetColour() const { return wxNullColour; }
    void SetColour(const wxColour& col) {}

    float GetPosition() const { return 0.0; }
    void SetPosition(float pos) {}
};

class wxGraphicsGradientStops
{
public:
    wxGraphicsGradientStops(wxColour, wxColour) {}
    ~wxGraphicsGradientStops() {}
    
    void Add(const wxGraphicsGradientStop& stop) {}
    void Add(wxColour col, float pos) {}
    unsigned GetCount() { return 0; }
    wxGraphicsGradientStop Item(unsigned n) const { return wxGraphicsGradientStop(); }
    void SetStartColour(wxColour col) {}
    wxColour GetStartColour() const { return wxNullColour; }
    void SetEndColour(wxColour col) {}
    wxColour GetEndColour() const { return wxNullColour; }
};



class wxGraphicsContext : public wxGraphicsObject
{
public:

    wxGraphicsContext(wxGraphicsRenderer* ) {
        PyErr_SetString(PyExc_NotImplementedError,
                        "wx.GraphicsContext is not available on this platform.");
    }

    virtual ~wxGraphicsContext() {}

    static wxGraphicsContext* Create()   {
        PyErr_SetString(PyExc_NotImplementedError,
                        "wx.GraphicsContext is not available on this platform.");
        return NULL;
    }

    static wxGraphicsContext* Create( const wxEnhMetaFileDC& )  {
        PyErr_SetString(PyExc_NotImplementedError,
                        "wx.GraphicsContext is not available on this platform.");
        return NULL;
    }

    static wxGraphicsContext* Create( const wxWindowDC& )  {
        PyErr_SetString(PyExc_NotImplementedError,
                        "wx.GraphicsContext is not available on this platform.");
        return NULL;
    }

    static wxGraphicsContext * Create( const wxMemoryDC& dc) {
        PyErr_SetString(PyExc_NotImplementedError,
                        "wx.GraphicsContext is not available on this platform.");
        return NULL;
    }

    static wxGraphicsContext * Create( const wxPrinterDC& dc) {
        PyErr_SetString(PyExc_NotImplementedError,
                        "wx.GraphicsContext is not available on this platform.");
        return NULL;
    }

    static wxGraphicsContext* CreateFromNative( void *  )  {
        PyErr_SetString(PyExc_NotImplementedError,
                        "wx.GraphicsContext is not available on this platform.");
        return NULL;
    }

    static wxGraphicsContext* CreateFromNativeWindow( void *  )  {
        PyErr_SetString(PyExc_NotImplementedError,
                        "wx.GraphicsContext is not available on this platform.");
        return NULL;
    }

    static wxGraphicsContext* Create( wxWindow*  )  {
        PyErr_SetString(PyExc_NotImplementedError,
                        "wx.GraphicsContext is not available on this platform.");
        return NULL;
    }

    static wxGraphicsContext* Create(wxImage& ) {
        PyErr_SetString(PyExc_NotImplementedError,
                        "wx.GraphicsContext is not available on this platform.");
        return NULL;
    }
    
    virtual bool StartDoc( const wxString& message ) { return false; }
    virtual void EndDoc() {}
    virtual void StartPage( wxDouble, wxDouble) {}
    virtual void EndPage() {}
    virtual void Flush() {}
    virtual void BeginLayer(wxDouble) {}
    virtual void EndLayer() {}

    wxGraphicsPath CreatePath()  { return wxNullGraphicsPath; }

    virtual wxGraphicsPen CreatePen(const wxPen& )  { return wxNullGraphicsPen; }

    virtual wxGraphicsBrush CreateBrush(const wxBrush& ) { return wxNullGraphicsBrush; }

    wxGraphicsBrush CreateLinearGradientBrush(
        wxDouble , wxDouble , wxDouble , wxDouble ,
        const wxColour&, const wxColour&) const { return wxNullGraphicsBrush; }
    wxGraphicsBrush
    CreateLinearGradientBrush(wxDouble x1, wxDouble y1,
                              wxDouble x2, wxDouble y2,
                              const wxGraphicsGradientStops& stops) const
         { return wxNullGraphicsBrush; }

    wxGraphicsBrush
    CreateRadialGradientBrush(wxDouble xo, wxDouble yo,
                              wxDouble xc, wxDouble yc, wxDouble radius,
                              const wxColour &oColor, const wxColour &cColor) const
        { return wxNullGraphicsBrush; }
    
    wxGraphicsBrush
    CreateRadialGradientBrush(wxDouble xo, wxDouble yo,
                              wxDouble xc, wxDouble yc, wxDouble radius,
                              const wxGraphicsGradientStops& stops) const
         { return wxNullGraphicsBrush; }

    virtual wxGraphicsFont CreateFont( const wxFont &, const wxColour & )  { return wxNullGraphicsFont; }
    virtual wxGraphicsFont CreateFont(double sizeInPixels,
                                      const wxString& facename,
                                      int flags = wxFONTFLAG_DEFAULT,
                                      const wxColour& col = *wxBLACK) const { return wxNullGraphicsFont; }

    virtual wxGraphicsBitmap CreateBitmap( const wxBitmap & ) const { return wxNullGraphicsBitmap; }
    wxGraphicsBitmap CreateBitmapFromImage(const wxImage& image) const { return wxNullGraphicsBitmap; }
    virtual wxGraphicsBitmap CreateSubBitmap( const wxGraphicsBitmap &, wxDouble, wxDouble, wxDouble, wxDouble ) const  { return wxNullGraphicsBitmap; }
    
    virtual wxGraphicsMatrix CreateMatrix( wxDouble, wxDouble, wxDouble, wxDouble,
                                            wxDouble, wxDouble)  { return wxNullGraphicsMatrix; }

    virtual void PushState() {}
    virtual void PopState() {}
    virtual void Clip( const wxRegion & ) {}
    virtual void Clip( wxDouble , wxDouble , wxDouble , wxDouble  ) {}
    virtual void ResetClip() {}
    virtual void * GetNativeContext() { return NULL; }
    virtual int GetAntialiasMode() const { return 0; }
    virtual bool SetAntialiasMode(wxAntialiasMode antialias) { return false; }

    virtual wxInterpolationQuality GetInterpolationQuality() const { return wxINTERPOLATION_DEFAULT; }
    virtual bool SetInterpolationQuality(wxInterpolationQuality) { return false; };

    virtual int GetCompositionMode() const { return 0; }
    virtual bool SetCompositionMode(wxCompositionMode op) { return false; }
    virtual void GetSize( wxDouble*, wxDouble* );
    virtual void GetDPI( wxDouble*, wxDouble* );
    
    virtual void Translate( wxDouble , wxDouble ) {}
    virtual void Scale( wxDouble , wxDouble ) {}
    virtual void Rotate( wxDouble ) {}
    virtual void ConcatTransform( const wxGraphicsMatrix& ) {}
    virtual void SetTransform( const wxGraphicsMatrix& ) {}
    virtual wxGraphicsMatrix GetTransform() const { return wxNullGraphicsMatrix; }

    virtual void SetPen( const wxGraphicsPen& ) {}
    void SetPen( const wxPen& ) {}

    virtual void SetBrush( const wxGraphicsBrush& ) {}
    void SetBrush( const wxBrush& ) {}

    virtual void SetFont( const wxGraphicsFont& ) {}
    void SetFont( const wxFont&, const wxColour& ) {}

    virtual void StrokePath( const wxGraphicsPath & ) {}
    virtual void FillPath( const wxGraphicsPath &, wxPolygonFillMode ) {}
    virtual void DrawPath( const wxGraphicsPath &, wxPolygonFillMode ) {}

    virtual void DrawText( const wxString &, wxDouble , wxDouble  )  {}
    virtual void DrawText( const wxString &, wxDouble , wxDouble , wxDouble ) {}
    virtual void DrawText( const wxString &, wxDouble , wxDouble , wxGraphicsBrush )  {}
    virtual void DrawText( const wxString &, wxDouble , wxDouble , wxDouble , wxGraphicsBrush ) {}
    virtual void GetTextExtent( const wxString &, wxDouble *, wxDouble *,
                                wxDouble *, wxDouble * ) const {}
    virtual void GetPartialTextExtents(const wxString& , wxArrayDouble& ) const  {}

    virtual void DrawBitmap( const wxGraphicsBitmap &, wxDouble, wxDouble, wxDouble, wxDouble ) {}
    virtual void DrawBitmap( const wxBitmap &, wxDouble , wxDouble , wxDouble , wxDouble  )  {}
    virtual void DrawIcon( const wxIcon &, wxDouble , wxDouble , wxDouble , wxDouble  )  {}

    virtual void StrokeLine( wxDouble , wxDouble , wxDouble , wxDouble ) {}
    virtual void StrokeLines( size_t , const wxPoint2DDouble *) {}
    virtual void StrokeLines( size_t , const wxPoint2DDouble *, const wxPoint2DDouble *) {}
    virtual void DrawLines( size_t , const wxPoint2DDouble *, wxPolygonFillMode ) {}
    virtual void DrawRectangle( wxDouble , wxDouble , wxDouble , wxDouble ) {}
    virtual void DrawEllipse( wxDouble , wxDouble , wxDouble , wxDouble ) {}
    virtual void DrawRoundedRectangle( wxDouble , wxDouble , wxDouble , wxDouble , wxDouble ) {}
    virtual bool ShouldOffset() const { return false; }

    virtual void EnableOffset(bool enable = true) {}
    void DisableOffset() { }
    bool OffsetEnabled() { return false; }
  
};


class wxGraphicsRenderer : public wxObject
{
public :
    wxGraphicsRenderer() {
        PyErr_SetString(PyExc_NotImplementedError,
                        "wx.GraphicsRenderer is not available on this platform.");
    }

    virtual ~wxGraphicsRenderer() {}

    static wxGraphicsRenderer* GetDefaultRenderer() {
        PyErr_SetString(PyExc_NotImplementedError,
                        "wx.GraphicsRenderer is not available on this platform.");
        return NULL;
    }
    static wxGraphicsRenderer* GetCairoRenderer() {
        PyErr_SetString(PyExc_NotImplementedError,
                        "wx.GraphicsRenderer is not available on this platform.");
        return NULL;
    }   

    virtual wxGraphicsContext * CreateContext( const wxEnhMetaFileDC& ) { return NULL; }
    virtual wxGraphicsContext * CreateContext( const wxWindowDC& ) { return NULL; }
    virtual wxGraphicsContext * CreateContext( const wxMemoryDC& ) { return NULL; }
    virtual wxGraphicsContext * CreateContext( const wxPrinterDC& ) { return NULL; }
    virtual wxGraphicsContext * CreateContextFromNativeContext( void *  ) { return NULL; }
    virtual wxGraphicsContext * CreateContextFromNativeWindow( void *  )  { return NULL; }
    virtual wxGraphicsContext * CreateContext( wxWindow*  ) { return NULL; }
    virtual wxGraphicsContext * CreateContextFromImage(wxImage&) { return NULL; }
    virtual wxGraphicsContext * CreateMeasuringContext() { return NULL; }

    virtual wxGraphicsPath CreatePath()  { return wxNullGraphicsPath; }

    virtual wxGraphicsMatrix CreateMatrix( wxDouble , wxDouble , wxDouble , wxDouble ,
                                             wxDouble , wxDouble ) { return wxNullGraphicsMatrix; }

    virtual wxGraphicsPen CreatePen(const wxPen& )  { return wxNullGraphicsPen; }
    virtual wxGraphicsBrush CreateBrush(const wxBrush&  )  { return wxNullGraphicsBrush; }

    wxGraphicsBrush
    CreateLinearGradientBrush(wxDouble x1, wxDouble y1,
                              wxDouble x2, wxDouble y2,
                              const wxGraphicsGradientStops& stops) const
    { return wxNullGraphicsBrush; }
    
    wxGraphicsBrush
    CreateRadialGradientBrush(wxDouble xo, wxDouble yo,
                              wxDouble xc, wxDouble yc, wxDouble radius,
                              const wxGraphicsGradientStops& stops) const
    { return wxNullGraphicsBrush; }

    virtual wxGraphicsFont CreateFont( const wxFont & , const wxColour & ) { return wxNullGraphicsFont; }
    virtual wxGraphicsFont CreateFont(double,
                                      const wxString&,
                                      int flags,
                                      const wxColour&)  { return wxNullGraphicsFont; }

    virtual wxGraphicsBitmap CreateBitmap( const wxBitmap & ) const { return wxNullGraphicsBitmap; }
    virtual wxGraphicsBitmap CreateBitmapFromImage(const wxImage&) { return wxNullGraphicsBitmap; }
    virtual wxGraphicsBitmap CreateSubBitmap( const wxGraphicsBitmap &, wxDouble, wxDouble, wxDouble, wxDouble ) const  { return wxNullGraphicsBitmap; }
};



class wxGCDC: public wxDC
{
public:
    wxGCDC(const wxWindowDC&)
        : wxDC(NULL)
    {
        wxPyBlock_t blocked = wxPyBeginBlockThreads();
        PyErr_SetString(PyExc_NotImplementedError,
                        "wxGCDC is not available on this platform.");
        wxPyEndBlockThreads(blocked);
     }

    wxGCDC(const wxMemoryDC&)
        : wxDC(NULL)
    {
        wxPyBlock_t blocked = wxPyBeginBlockThreads();
        PyErr_SetString(PyExc_NotImplementedError,
                        "wxGCDC is not available on this platform.");
        wxPyEndBlockThreads(blocked);
     }

    wxGCDC(const wxPrinterDC& dc)
        : wxDC(NULL)
    {
        wxPyBlock_t blocked = wxPyBeginBlockThreads();
        PyErr_SetString(PyExc_NotImplementedError,
                        "wxGCDC is not available on this platform.");
        wxPyEndBlockThreads(blocked);
     }

    wxGCDC(wxGraphicsContext*&)
        : wxDC(NULL)
    {
        wxPyBlock_t blocked = wxPyBeginBlockThreads();
        PyErr_SetString(PyExc_NotImplementedError,
                        "wxGCDC is not available on this platform.");
        wxPyEndBlockThreads(blocked);
     }
    
    wxGCDC(const wxGraphicsContext& ctx)
        : wxDC(NULL)
    {
        wxPyBlock_t blocked = wxPyBeginBlockThreads();
        PyErr_SetString(PyExc_NotImplementedError,
                        "wxGCDC is not available on this platform.");
        wxPyEndBlockThreads(blocked);
     }

    wxGCDC()
        : wxDC(NULL)
    {
        wxPyBlock_t blocked = wxPyBeginBlockThreads();
        PyErr_SetString(PyExc_NotImplementedError,
                        "wxGCDC is not available on this platform.");
        wxPyEndBlockThreads(blocked);
    }

    virtual ~wxGCDC() {}

    wxGraphicsContext* GetGraphicsContext() const { return NULL; }
    void SetGraphicsContext( wxGraphicsContext* ) {}
    void Flush() {}
};

#endif
%}

//---------------------------------------------------------------------------
//---------------------------------------------------------------------------
//---------------------------------------------------------------------------


%typemap(in) (size_t points, wxPoint2D* points_array ) {
    $2 = wxPoint2D_LIST_helper($input, &$1);
    if ($2 == NULL) SWIG_fail;
}
%typemap(freearg) (size_t points, wxPoint2D* points_array ) {
    if ($2) delete [] $2;
}



MustHaveApp(wxGraphicsPath);
MustHaveApp(wxGraphicsContext);
MustHaveApp(wxGCDC);

//---------------------------------------------------------------------------


DocStr(wxGraphicsObject,
"This class is the superclass of native graphics objects like pens
etc. It provides the internal reference counting.  It is not to be
instantiated by user code.", "");
class wxGraphicsObject : public wxObject
{
public :
    wxGraphicsObject( wxGraphicsRenderer* renderer = NULL );
    virtual ~wxGraphicsObject();
    
    DocDeclStr(
        bool , IsNull() const ,
        "Is this object valid (false) or still empty (true)?", "");
    
    DocDeclStr(
        wxGraphicsRenderer* , GetRenderer() const,
        "Returns the renderer that was used to create this instance, or
``None`` if it has not been initialized yet.", "");
    
};


DocStr(wxGraphicsPen,
"A wx.GraphicsPen is a native representation of a pen. It is used for
stroking a path on a `wx.GraphicsContext`. The contents are specific and
private to the respective renderer. The only way to get a valid instance
is via a CreatePen call on the graphics context or the renderer
instance.", "");
class wxGraphicsPen : public wxGraphicsObject
{
public :
    wxGraphicsPen();
    virtual ~wxGraphicsPen();
};

DocStr(wxGraphicsBrush,
"A wx.GraphicsBrush is a native representation of a brush. It is used
for filling a path on a `wx.GraphicsContext`. The contents are
specific and private to the respective renderer. The only way to get a
valid instance is via a Create...Brush call on the graphics context or
the renderer instance.", "");
class wxGraphicsBrush : public wxGraphicsObject
{
public :
    wxGraphicsBrush();
    virtual ~wxGraphicsBrush();
};


DocStr(wxGraphicsFont,
"A `wx.GraphicsFont` is a native representation of a font (including
text colour). The contents are specific an private to the respective
renderer.  The only way to get a valid instance is via a CreateFont
call on the graphics context or the renderer instance.", "");
class wxGraphicsFont : public wxGraphicsObject
{
public :
    wxGraphicsFont();
    virtual ~wxGraphicsFont();
};


DocStr(wxGraphicsBitmap,
"", "");
class wxGraphicsBitmap : public wxGraphicsObject
{
public :
    wxGraphicsBitmap();
    virtual ~wxGraphicsBitmap();
};


//---------------------------------------------------------------------------

DocStr(wxGraphicsMatrix,
"A wx.GraphicsMatrix is a native representation of an affine
matrix. The contents are specific and private to the respective
renderer. The only way to get a valid instance is via a CreateMatrix
call on the graphics context or the renderer instance.", "");
class wxGraphicsMatrix : public wxGraphicsObject
{
public :
//    wxGraphicsMatrix(); 
    virtual ~wxGraphicsMatrix();

    DocDeclStr(
        virtual void , Concat( const wxGraphicsMatrix& t ),
        "Concatenates the passed in matrix to the current matrix.", "");


    DocDeclStr(
        virtual void , Set(wxDouble a=1.0, wxDouble b=0.0, wxDouble c=0.0, wxDouble d=1.0,
                           wxDouble tx=0.0, wxDouble ty=0.0),
        "Sets the matrix to the specified values (default values are the
identity matrix.)", "");

    
    DocDeclAStr(
        virtual void , Get(wxDouble* OUTPUT, wxDouble* OUTPUT, wxDouble* OUTPUT,
                           wxDouble* OUTPUT, wxDouble* OUTPUT, wxDouble* OUTPUT),
        "Get(self) --> (a, b, c, d, tx, ty)",
        "Gets the component values of the matrix and returns them as a tuple.", "");
    

    DocDeclStr(
        virtual void , Invert(),
        "Inverts the matrix.", "");


    DocDeclStr(
        virtual bool , IsEqual( const wxGraphicsMatrix& t) const,
        "Returns ``True`` if the elements of the transformation matrix are
equal", "");


    DocDeclStr(
        virtual bool , IsIdentity() const,
        "Returns ``True`` if this is the identity matrix", "");


    DocDeclStr(
        virtual void , Translate( wxDouble dx , wxDouble dy ),
        "Add a translation to this matrix.", "");


    DocDeclStr(
        virtual void , Scale( wxDouble xScale , wxDouble yScale ),
        "Scales this matrix.", "");


    DocDeclStr(
        virtual void , Rotate( wxDouble angle ),
        "Rotates this matrix.  The angle should be specified in radians.", "");


    DocDeclAStr(
        virtual void , TransformPoint( wxDouble *INOUT, wxDouble *INOUT ) const,
        "TransformPoint(self, x, y) --> (x, y)",
        "Applies this matrix to a point, returns the resulting point values", "");


    DocDeclAStr(
        virtual void , TransformDistance( wxDouble *INOUT, wxDouble *INOUT ) const,
        "TransformDistance(self, dx, dy) --> (dx, dy)",
        "Applies this matrix to a distance (ie. performs all transforms except
translations)", "");


    DocDeclStr(
        virtual void * , GetNativeMatrix() const,
        "Returns the native representation of the matrix. For CoreGraphics this
is a CFAffineMatrix pointer. For GDIPlus a Matrix Pointer and for
Cairo a cairo_matrix_t pointer.  NOTE: For wxPython we still need a
way to make this value usable.", "");
};

//---------------------------------------------------------------------------

class wxGraphicsPath : public wxGraphicsObject
{
public :
//    wxGraphicsPath();
    virtual ~wxGraphicsPath();


    %nokwargs MoveToPoint;
    DocStr(MoveToPoint,
           "Begins a new subpath at the specified point.", "");
    virtual void  MoveToPoint( wxDouble x, wxDouble y );
    void MoveToPoint( const wxPoint2D& p);


    %nokwargs AddLineToPoint;
    DocStr(AddLineToPoint,
        "Adds a straight line from the current point to the specified point.", "");
    virtual void AddLineToPoint( wxDouble x, wxDouble y );
    void AddLineToPoint( const wxPoint2D& p);


    %nokwargs AddCurveToPoint;
    DocStr(AddCurveToPoint,
        "Adds a cubic Bezier curve from the current point, using two control
points and an end point", "");
    virtual void AddCurveToPoint( wxDouble cx1, wxDouble cy1,
                                  wxDouble cx2, wxDouble cy2,
                                  wxDouble x, wxDouble y );
    void AddCurveToPoint( const wxPoint2D& c1, const wxPoint2D& c2, const wxPoint2D& e);



    DocDeclStr(
        virtual void , AddPath( const wxGraphicsPath& path ),
        "Adds another path", "");


    DocDeclStr(
        virtual void , CloseSubpath(),
        "Closes the current sub-path.", "");


    DocDeclStr(
        wxPoint2D , GetCurrentPoint() const,
        "Gets the last point of the current path, (0,0) if not yet set", "");


    %nokwargs AddArc;
    DocStr(AddArc,
        "Adds an arc of a circle centering at (x,y) with radius (r) from
startAngle to endAngle", "");
    virtual void AddArc( wxDouble x, wxDouble y, wxDouble r,
                         wxDouble startAngle, wxDouble endAngle, bool clockwise=true );
    void AddArc( const wxPoint2D& c, wxDouble r, wxDouble startAngle, wxDouble endAngle, bool clockwise=true);


    DocDeclStr(
        virtual void , AddQuadCurveToPoint( wxDouble cx, wxDouble cy, wxDouble x, wxDouble y ),
        "Adds a quadratic Bezier curve from the current point, using a control
point and an end point", "");


    DocDeclStr(
        virtual void , AddRectangle( wxDouble x, wxDouble y, wxDouble w, wxDouble h ),
        "Appends a rectangle as a new closed subpath.", "");


    DocDeclStr(
        virtual void , AddCircle( wxDouble x, wxDouble y, wxDouble r ),
        "Appends a circle around (x,y) with radius r as a new closed subpath.", "");


    DocDeclStr(
        virtual void , AddArcToPoint( wxDouble x1, wxDouble y1 , wxDouble x2, wxDouble y2, wxDouble r ) ,
        "Appends an arc to two tangents connecting (current) to (x1,y1) and
(x1,y1) to (x2,y2), also a straight line from (current) to (x1,y1)", "");


    DocDeclStr(
        virtual void , AddEllipse( wxDouble x, wxDouble y, wxDouble w, wxDouble h),
        "Appends an ellipse fitting into the passed in rectangle.", "");


    DocDeclStr(
        virtual void , AddRoundedRectangle( wxDouble x, wxDouble y, wxDouble w, wxDouble h, wxDouble radius),
        "Appends a rounded rectangle.", "");


    DocDeclStr(
        virtual void * , GetNativePath() const,
        "Returns the native path (CGPathRef for Core Graphics, Path pointer for
GDIPlus and a cairo_path_t pointer for cairo).  NOTE: For wxPython we
still need a way to make this value usable.", "");


    DocDeclStr(
        virtual void , UnGetNativePath(void *p) const,
        "Gives back the native path returned by GetNativePath() because there
might be some deallocations necessary (eg on cairo the native path
returned by GetNativePath is newly allocated each time).", "");


    DocDeclStr(
        virtual void , Transform( const wxGraphicsMatrix& matrix ),
        "Transforms each point of this path by the matrix", "");


    DocDeclStr(
        wxRect2D , GetBox() const,
        "Gets the bounding box enclosing all points (possibly including control
points)", "");


    %nokwargs Contains;
    DocStr(Contains,
        "Returns ``True`` if the point is within the path.", "");
    virtual bool Contains( wxDouble x, wxDouble y, wxPolygonFillMode fillStyle = wxODDEVEN_RULE) const;
    bool Contains( const wxPoint2D& c, wxPolygonFillMode fillStyle = wxODDEVEN_RULE) const;

};


//---------------------------------------------------------------------------

%immutable;
const wxGraphicsPen     wxNullGraphicsPen;
const wxGraphicsBrush   wxNullGraphicsBrush;
const wxGraphicsFont    wxNullGraphicsFont;
const wxGraphicsBitmap  wxNullGraphicsBitmap;
const wxGraphicsMatrix  wxNullGraphicsMatrix;
const wxGraphicsPath    wxNullGraphicsPath;
%mutable;

//---------------------------------------------------------------------------

// Describes a single gradient stop.
class wxGraphicsGradientStop
{
public:
    wxGraphicsGradientStop(wxColour col = wxTransparentColour,
                           float pos = 0.0);
    ~wxGraphicsGradientStop();
    
    const wxColour& GetColour() const;
    void SetColour(const wxColour& col);

    float GetPosition() const;
    void SetPosition(float pos);

    %property(Position, GetPosition, SetPosition);
    %property(Colour, GetColour, SetColour);
};

// A collection of gradient stops ordered by their positions (from lowest to
// highest). The first stop (index 0, position 0.0) is always the starting
// colour and the last one (index GetCount() - 1, position 1.0) is the end
// colour.
class wxGraphicsGradientStops
{
public:
    wxGraphicsGradientStops(wxColour startCol = wxTransparentColour,
                            wxColour endCol = wxTransparentColour);
    ~wxGraphicsGradientStops();

    // Add a stop in correct order.
    %nokwargs Add;
    void Add(const wxGraphicsGradientStop& stop);
    void Add(wxColour col, float pos);

    // Get the number of stops.
    unsigned GetCount();

    // Return the stop at the given index (which must be valid).
    wxGraphicsGradientStop Item(unsigned n) const;

    // Get/set start and end colours.
    void SetStartColour(wxColour col);
    wxColour GetStartColour() const;
    void SetEndColour(wxColour col);
    wxColour GetEndColour() const;

    %extend {
        unsigned __len__()
            { return self->GetCount(); }
        wxGraphicsGradientStop __getitem__(unsigned n)
            { return self->Item(n); }
    }

    %property(Count, GetCount);
    %property(StartColour, GetStartColour, SetStartColour);
    %property(EndColour, GetEndColour, SetEndColour);
};



//---------------------------------------------------------------------------

DocStr(wxGraphicsContext,
"A `wx.GraphicsContext` instance is the object that is drawn upon. It is
created by a renderer using the CreateContext calls, this can be done
either directly using a renderer instance, or indirectly using the
static convenience CreateXXX functions of wx.GraphicsContext that
always delegate the task to the default renderer.", "");

class wxGraphicsContext : public wxGraphicsObject
{
public:
    //wxGraphicsContext();         This is an ABC, use Create to make an instance...
    virtual ~wxGraphicsContext();

    %newobject Create;
    %nokwargs Create;
    %pythonAppend Create
        "val.__dc = args[0] # save a ref so the dc will not be deleted before self";
    DocStr(Create,
           "Creates a wx.GraphicsContext either from a window or a DC.", "");
    static wxGraphicsContext* Create( const wxWindowDC& dc);
    static wxGraphicsContext* Create( const wxMemoryDC& dc);
    static wxGraphicsContext* Create( wxWindow* window ) ;
    static wxGraphicsContext* Create( const wxPrinterDC& dc) ;
#ifdef __WXMSW__
    static wxGraphicsContext* Create( const wxMetaFileDC& dc) ;
    static wxGraphicsContext* Create( const wxEnhMetaFileDC& dc) ;
#endif
    static wxGraphicsContext* Create(wxImage& );
    
    %pythonAppend Create "";
    DocDeclStrName(
        static wxGraphicsContext* , Create(),
        "Create a lightwieght context that can be used for measuring text only.", "",
        CreateMeasuringContext);
    
    %newobject CreateFromNative;
    DocDeclStr(
        static wxGraphicsContext* , CreateFromNative( void * context ) ,
        "Creates a wx.GraphicsContext from a native context. This native
context must be eg a CGContextRef for Core Graphics, a Graphics
pointer for GDIPlus or a cairo_t pointer for Cairo.  NOTE: For
wxPython we still need a way to make this value usable.", "");
    

    %newobject CreateFromNativeWindow;
    DocDeclStr(
        static wxGraphicsContext* , CreateFromNativeWindow( void * window ) ,
        "Creates a wx.GraphicsContext from a native window.  NOTE: For wxPython
we still need a way to make this value usable.", "");
    

    DocDeclStr(
        virtual bool , StartDoc( const wxString& message ) ,
        "Begin a new document (relevant only for printing / pdf etc) if there
is a progress dialog, message will be shown", "");
    
    
    DocDeclStr(
        virtual void , EndDoc(),
        "Done with that document (relevant only for printing / pdf etc) ", "");
    

    DocDeclStr(
        virtual void , StartPage( wxDouble width = 0, wxDouble height = 0 ),
        "Opens a new page (relevant only for printing / pdf etc) with the given
size in points (if both are null the default page size will be used)
", "");
    
    
    DocDeclStr(
        virtual void , EndPage(),
        "Ends the current page  (relevant only for printing / pdf etc) ", "");
    
    
    DocDeclStr(
        virtual void , Flush(),
        "Make sure that the current content of this context is immediately visible", "");
    
    DocDeclStr(
        virtual wxGraphicsPath , CreatePath(),
        "Creates a native graphics path which is initially empty.", "");


    DocDeclStr(
        virtual wxGraphicsPen , CreatePen(const wxPen& pen),
        "Creates a native pen from a `wx.Pen`.", "");


    DocDeclStr(
        virtual wxGraphicsBrush , CreateBrush(const wxBrush& brush ),
        "Creates a native brush from a `wx.Brush`.", "");


    DocStr(CreateLinearGradientBrush,
        "Creates a native brush, having a linear gradient, starting at (x1,y1)
to (x2,y2) with the given boundary colors or the specified stops.", "");
    %nokwargs CreateLinearGradientBrush;
    wxGraphicsBrush 
    CreateLinearGradientBrush( wxDouble x1, wxDouble y1, wxDouble x2, wxDouble y2,
                               const wxColour& c1, const wxColour& c2) const;
    wxGraphicsBrush
    CreateLinearGradientBrush(wxDouble x1, wxDouble y1,
                              wxDouble x2, wxDouble y2,
                              const wxGraphicsGradientStops& stops) const;

    
    DocStr(CreateRadialGradientBrush,
        "Creates a native brush, having a radial gradient originating at point
(xo,yo) and ending on a circle around (xc,yc) with the given radius; the colours may be
specified by just the two extremes or the full array of gradient stops.", "");
    %nokwargs CreateRadialGradientBrush;
    wxGraphicsBrush 
    CreateRadialGradientBrush( wxDouble xo, wxDouble yo,
                               wxDouble xc, wxDouble yc, wxDouble radius,
                               const wxColour &oColor, const wxColour &cColor) const;
    wxGraphicsBrush
    CreateRadialGradientBrush(wxDouble xo, wxDouble yo,
                              wxDouble xc, wxDouble yc, wxDouble radius,
                              const wxGraphicsGradientStops& stops) const;


    %nokwargs CreateFont;   
    DocDeclStr(
        virtual wxGraphicsFont , CreateFont( const wxFont &font , const wxColour &col = *wxBLACK ),
        "Creates a native graphics font from a `wx.Font` and a text colour.", "");

    virtual wxGraphicsFont CreateFont(double sizeInPixels,
                                      const wxString& facename,
                                      int flags = wxFONTFLAG_DEFAULT,
                                      const wxColour& col = *wxBLACK) const;

    DocDeclStr(
        virtual wxGraphicsBitmap , CreateBitmap( const wxBitmap &bitmap ) const,
        "Create a native bitmap representation.", "");

    wxGraphicsBitmap CreateBitmapFromImage(const wxImage& image) const;

    
    DocDeclStr(
        virtual wxGraphicsBitmap , CreateSubBitmap( const wxGraphicsBitmap &bitmap, wxDouble x, wxDouble y, wxDouble w, wxDouble h  ) const,
        "Create a native bitmap representation using a subset of a wx.Bitmap.", "");
    

    DocDeclStr(
        virtual wxGraphicsMatrix , CreateMatrix( wxDouble a=1.0, wxDouble b=0.0,
                                                 wxDouble c=0.0, wxDouble d=1.0,
                                                 wxDouble tx=0.0, wxDouble ty=0.0),
        "Creates a native affine transformation matrix from the passed in
values. The defaults result in an identity matrix.", "");



    DocDeclStr(
        virtual void , PushState(),
        "Push the current state of the context, (ie the transformation matrix)
on a stack", "");


    DocDeclStr(
        virtual void , PopState(),
        "Pops a stored state from the stack", "");


    DocDeclStrName(
        virtual void , Clip( const wxRegion &region ),
        "Clips drawings to the region intersected with the current clipping region.", "",
        ClipRegion);

    
    DocDeclStr(
        virtual void , Clip( wxDouble x, wxDouble y, wxDouble w, wxDouble h ),
        "Clips drawings to the rectangle intersected with the current clipping region..", "");


    DocDeclStr(
        virtual void , ResetClip(),
        "Resets the clipping to original shape.", "");


    DocDeclStr(
        virtual void * , GetNativeContext(),
        "Returns the native context (CGContextRef for Core Graphics, Graphics
pointer for GDIPlus and cairo_t pointer for cairo).", "");

    
    DocDeclStr(
        virtual wxAntialiasMode , GetAntialiasMode() const,
        "Returns the current shape antialiasing mode", "");
    
    DocDeclStr(
        virtual bool , SetAntialiasMode(wxAntialiasMode antialias),
        "Sets the antialiasing mode, returns true if it is supported", "");
    
    // returns the current interpolation quality
    virtual wxInterpolationQuality GetInterpolationQuality() const;
    
    // sets the interpolation quality, returns true if it supported
    virtual bool SetInterpolationQuality(wxInterpolationQuality interpolation);

    DocDeclStr(
        virtual wxCompositionMode , GetCompositionMode() const,
        "Returns the current compositing operator", "");
    
    
    DocDeclStr(
        virtual bool , SetCompositionMode(wxCompositionMode op),
        "Sets the compositing operator, returns True if it supported", "");

    
    DocDeclAStr(
        virtual void , GetSize( wxDouble* OUTPUT, wxDouble* OUTPUT),
        "GetSize(self) --> (width, height)",
        "Returns the size of the graphics context in device coordinates", "");
    

    DocDeclAStr(
        virtual void , GetDPI( wxDouble* OUTPUT, wxDouble* OUTPUT),
        "GetDPI(self) --> (dpiX, dpiY)",
        "Returns the resolution of the graphics context in device points per inch", "");
    

    DocDeclStr(
        virtual void , BeginLayer(wxDouble opacity),
        "all rendering is done into a fully transparent temporary context", "");
    

    DocDeclStr(
        virtual void , EndLayer(),
        "composites back the drawings into the context with the opacity given
at the BeginLayer call", "");
    
    

    DocDeclStr(
        virtual void , Translate( wxDouble dx , wxDouble dy ),
        "Translates the current transformation matrix.", "");


    DocDeclStr(
        virtual void , Scale( wxDouble xScale , wxDouble yScale ),
        "Scale the current transformation matrix of the context.", "");


    DocDeclStr(
        virtual void , Rotate( wxDouble angle ),
        "Rotate the current transformation matrix of the context.  ``angle`` is
specified in radians.", "");


    DocDeclStr(
        virtual void , ConcatTransform( const wxGraphicsMatrix& matrix ),
        "Concatenates the passed in transform with the current transform of
this context.", "");
    

    DocDeclStr(
        virtual void , SetTransform( const wxGraphicsMatrix& matrix ),
        "Sets the current transform of this context.", "");
    

    DocDeclStr(
        virtual wxGraphicsMatrix , GetTransform() const,
        "Gets the current transformation matrix of this context.", "");
        


    DocStr(SetPen, "Sets the stroke pen", "");
    %nokwargs SetPen;
    virtual void SetPen( const wxGraphicsPen& pen );
    void SetPen( const wxPen& pen );

    
    DocStr(SetBrush, "Sets the brush for filling", "");
    %nokwargs SetBrush;
    virtual void SetBrush( const wxGraphicsBrush& brush );
    void SetBrush( const wxBrush& brush );

    
    DocStr(SetFont, "Sets the font", "");
    %nokwargs SetFont;
    virtual void SetFont( const wxGraphicsFont& font );
    void SetFont( const wxFont& font, const wxColour& colour = *wxBLACK);

    
   
    DocDeclStr(
        virtual void , StrokePath( const wxGraphicsPath& path ),
        "Strokes along a path with the current pen.", "");

    
    DocDeclStr(
        virtual void , FillPath( const wxGraphicsPath& path, wxPolygonFillMode fillStyle = wxODDEVEN_RULE ),
        "Fills a path with the current brush.", "");

   
    DocDeclStr(
        virtual void , DrawPath( const wxGraphicsPath& path, wxPolygonFillMode fillStyle = wxODDEVEN_RULE ),
        "Draws the path by first filling and then stroking.", "");


    %extend {
        DocStr(DrawText,
               "Draws a text string at the defined position.", "");
        void DrawText( const wxString &str, wxDouble x, wxDouble y,
                       const wxGraphicsBrush& backgroundBrush = wxNullGraphicsBrush )
        {
            if ( !backgroundBrush.IsNull() )
                self->DrawText(str, x, y, backgroundBrush);
            else
                self->DrawText(str, x, y);
        }

        DocStr(DrawRotatedText,
               "Draws a text string at the defined position, at the specified angle,
which is given in radians.", "");
        void DrawRotatedText(  const wxString &str, wxDouble x, wxDouble y, wxDouble angle,
                               const wxGraphicsBrush& backgroundBrush = wxNullGraphicsBrush )
        {
            if ( !backgroundBrush.IsNull() )
                self->DrawText(str, x, y, angle, backgroundBrush);
            else
                self->DrawText(str, x, y, angle);
        }
    }
   


    DocDeclAStrName(
        virtual void , GetTextExtent( const wxString &text,
                                      wxDouble *OUTPUT /*width*/,
                                      wxDouble *OUTPUT /*height*/,
                                      wxDouble *OUTPUT /*descent*/,
                                      wxDouble *OUTPUT /*externalLeading*/ ) const ,
        "GetFullTextExtent(self, text) --> (width, height, descent, externalLeading)",
        "Gets the dimensions of the string using the currently selected
font. ``text`` is the string to measure, ``w`` and ``h`` are the total
width and height respectively, ``descent`` is the dimension from the
baseline of the font to the bottom of the descender, and
``externalLeading`` is any extra vertical space added to the font by
the font designer (usually is zero).", "",
        GetFullTextExtent);

    %extend {
        DocAStr(GetTextExtent,
                "GetTextExtent(self, text) --> (width, height)",
                "Gets the dimensions of the string using the currently selected
font. ``text`` is the string to measure, ``w`` and ``h`` are the total
width and height respectively.", "");

        PyObject* GetTextExtent( const wxString &text )
        {
            wxDouble width = 0.0,
                     height = 0.0;
            self->GetTextExtent(text, &width, &height, NULL, NULL);
            // thread wrapers are turned off for this .i file, so no need to acquire GIL...
            PyObject* rv = PyTuple_New(2);
            PyTuple_SET_ITEM(rv, 0, PyFloat_FromDouble(width));
            PyTuple_SET_ITEM(rv, 1, PyFloat_FromDouble(height));
            return rv;
        }
    }


    %extend {
        DocAStr(GetPartialTextExtents,
                "GetPartialTextExtents(self, text) -> [widths]",
                "Returns a list of widths from the beginning of ``text`` to the
coresponding character in ``text``.", "");
        wxArrayDouble GetPartialTextExtents(const wxString& text) {
            wxArrayDouble widths;
            self->GetPartialTextExtents(text, widths);
            return widths;
        }
    }


    %nokwargs DrawBitmap;
    DocStr(DrawBitmap,
           "Draws the bitmap. In case of a mono bitmap, this is treated as a mask
and the current brush is used for filling.", "");
#ifndef __WXGTK__
    virtual void DrawBitmap( const wxGraphicsBitmap &bmp, wxDouble x, wxDouble y, wxDouble w, wxDouble h );
#endif
    virtual void DrawBitmap( const wxBitmap &bmp, wxDouble x, wxDouble y, wxDouble w, wxDouble h );    


    DocDeclStr(
        virtual void , DrawIcon( const wxIcon &icon, wxDouble x, wxDouble y, wxDouble w, wxDouble h ),
        "Draws the icon.", "");



    DocDeclStr(
        virtual void , StrokeLine( wxDouble x1, wxDouble y1, wxDouble x2, wxDouble y2),
        "Strokes a single line.", "");

    
    DocDeclAStr(
        virtual void , StrokeLines( size_t points, const wxPoint2D *points_array),
        "StrokeLines(self, List points)",
        "Stroke lines connecting each of the points", "");


    %extend {
        DocAStr(StrokeLineSegements,
                "StrokeLineSegments(self, List beginPoints, List endPoints)",
                "Stroke disconnected lines from begin to end points", "");
        void StrokeLineSegements(PyObject* beginPoints, PyObject* endPoints)
        {
            size_t c1, c2, count;
            wxPoint2D* beginP = wxPoint2D_LIST_helper(beginPoints, &c1);
            wxPoint2D* endP =   wxPoint2D_LIST_helper(endPoints, &c2);

            if ( beginP != NULL && endP != NULL )
            {
                count = wxMin(c1, c2);
                self->StrokeLines(count, beginP, endP);
            }
            delete [] beginP;
            delete [] endP;
        }
    }


    DocDeclStr(
        virtual void , DrawLines( size_t points, const wxPoint2D *points_array,
                                  wxPolygonFillMode fillStyle = wxODDEVEN_RULE ),
        "Draws a polygon.", "");


    DocDeclStr(
        virtual void , DrawRectangle( wxDouble x, wxDouble y, wxDouble w, wxDouble h),
        "Draws a rectangle.", "");


    DocDeclStr(
        virtual void , DrawEllipse( wxDouble x, wxDouble y, wxDouble w, wxDouble h),
        "Draws an ellipse.", "");


    DocDeclStr(
        virtual void , DrawRoundedRectangle( wxDouble x, wxDouble y, wxDouble w, wxDouble h, wxDouble radius),
        "Draws a rounded rectangle", "");

    

    DocDeclStr(
        virtual bool , ShouldOffset() const,
        "helper to determine if a 0.5 offset should be applied for the drawing operation", "");


    // indicates whether the context should try to offset for pixel boundaries, this only makes sense on 
    // bitmap devices like screen, by default this is turned off
    virtual void EnableOffset(bool enable = true);
    void DisableOffset() { EnableOffset(false); }
    bool OffsetEnabled() { return m_enableOffset; }
      
};


//---------------------------------------------------------------------------

class wxGraphicsRenderer : public wxObject
{
public :
    // wxGraphicsRenderer();  This is an ABC, use GetDefaultRenderer

    virtual ~wxGraphicsRenderer();

    static wxGraphicsRenderer* GetDefaultRenderer();
    static wxGraphicsRenderer* GetCairoRenderer();

    %nokwargs CreateContext;
    %newobject CreateContext;
    virtual wxGraphicsContext * CreateContext( const wxWindowDC& dc) ;
    virtual wxGraphicsContext * CreateContext( const wxMemoryDC& dc) ;
    virtual wxGraphicsContext * CreateContext( const wxPrinterDC& dc) ;
    virtual wxGraphicsContext * CreateContext( wxWindow* window );
#ifdef __WXMSW__
    virtual wxGraphicsContext * CreateContext( const wxMetaFileDC& dc) ;
    virtual wxGraphicsContext * CreateContext( const wxEnhMetaFileDC& dc) ;
#endif

    virtual wxGraphicsContext * CreateContextFromImage(wxImage& image);
    
    // create a context that can be used for measuring texts only, no drawing allowed
    virtual wxGraphicsContext * CreateMeasuringContext();
    
    %newobject CreateContextFromNativeContext;
    virtual wxGraphicsContext * CreateContextFromNativeContext( void * context );

    %newobject CreateContextFromNativeWindow;
    virtual wxGraphicsContext * CreateContextFromNativeWindow( void * window );


    virtual wxGraphicsPath CreatePath();

    virtual wxGraphicsMatrix CreateMatrix( wxDouble a=1.0, wxDouble b=0.0, wxDouble c=0.0, wxDouble d=1.0, 
                                           wxDouble tx=0.0, wxDouble ty=0.0);
        
    virtual wxGraphicsPen CreatePen(const wxPen& pen) ;
    
    virtual wxGraphicsBrush CreateBrush(const wxBrush& brush ) ;
    
    wxGraphicsBrush
    CreateLinearGradientBrush(wxDouble x1, wxDouble y1,
                              wxDouble x2, wxDouble y2,
                              const wxGraphicsGradientStops& stops);
    
    wxGraphicsBrush
    CreateRadialGradientBrush(wxDouble xo, wxDouble yo,
                              wxDouble xc, wxDouble yc, wxDouble radius,
                              const wxGraphicsGradientStops& stops);


    virtual wxGraphicsFont CreateFont( const wxFont &font , const wxColour &col = *wxBLACK );
    virtual wxGraphicsFont CreateFont(double sizeInPixels,
                                      const wxString& facename,
                                      int flags = wxFONTFLAG_DEFAULT,
                                      const wxColour& col = *wxBLACK);

    virtual wxGraphicsBitmap CreateBitmap( const wxBitmap &bitmap );
    virtual wxGraphicsBitmap CreateBitmapFromImage(const wxImage& image);
    virtual wxGraphicsBitmap CreateSubBitmap( const wxGraphicsBitmap &bitmap, wxDouble x, wxDouble y, wxDouble w, wxDouble h  );
};



//---------------------------------------------------------------------------

%{
#include "wx/dcgraph.h"
%}

class wxGCDC: public wxDC
{
public:
    %nokwargs wxGCDC;
    %pythonAppend wxGCDC
        "self.__dc = args[0] # save a ref so the other dc will not be deleted before self";
    wxGCDC(const wxWindowDC& dc);
    wxGCDC(const wxMemoryDC& dc);
    wxGCDC(const wxPrinterDC& dc);
    wxGCDC(wxWindow* window);

    %disownarg( wxGraphicsContext* ctx );
    wxGCDC(wxGraphicsContext* ctx);
    %cleardisown( wxGraphicsContext* ctx );
    
    //wxGCDC();
    virtual ~wxGCDC();

    wxGraphicsContext* GetGraphicsContext() const; 

    %disownarg( wxGraphicsContext* ctx );
    virtual void SetGraphicsContext( wxGraphicsContext* ctx );
    %cleardisown( wxGraphicsContext* ctx );

    %property(GraphicsContext, GetGraphicsContext, SetGraphicsContext);
};


//---------------------------------------------------------------------------

// Turn GIL acquisition back on.
%threadWrapperOn

