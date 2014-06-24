/////////////////////////////////////////////////////////////////////////////
// Name:        _richtextbuffer.i
// Purpose:     wxTextAttrEx, wxRichTextRange, wxRichTextObject and derived classes
//
// Author:      Robin Dunn
//
// Created:     11-April-2006
// RCS-ID:      $Id$
// Copyright:   (c) 2006 by Total Control Software
// Licence:     wxWindows license
/////////////////////////////////////////////////////////////////////////////

// Not a %module


//---------------------------------------------------------------------------

%{
#include <wx/sstream.h>
#include "wx/wxPython/pyistream.h"
%}

//---------------------------------------------------------------------------
%newgroup

enum wxRichTextFileType {
/*!
 * File types
 */
    wxRICHTEXT_TYPE_ANY,
    wxRICHTEXT_TYPE_TEXT,
    wxRICHTEXT_TYPE_XML,
    wxRICHTEXT_TYPE_HTML,
    wxRICHTEXT_TYPE_RTF,
    wxRICHTEXT_TYPE_PDF,

/*!
 * Flags determining the available space, passed to Layout
 */
    wxRICHTEXT_FIXED_WIDTH,
    wxRICHTEXT_FIXED_HEIGHT,
    wxRICHTEXT_VARIABLE_WIDTH,
    wxRICHTEXT_VARIABLE_HEIGHT,


    wxRICHTEXT_LAYOUT_SPECIFIED_RECT,
    wxRICHTEXT_DRAW_IGNORE_CACHE,

/*!
 * Flags for GetRangeSize
 */
    wxRICHTEXT_FORMATTED,
    wxRICHTEXT_UNFORMATTED,
    wxRICHTEXT_CACHE_SIZE,
    wxRICHTEXT_HEIGHT_ONLY,

/*!
 * Flags for SetStyle/SetListStyle
 */
    wxRICHTEXT_SETSTYLE_NONE,
    wxRICHTEXT_SETSTYLE_WITH_UNDO,
    wxRICHTEXT_SETSTYLE_OPTIMIZE,
    wxRICHTEXT_SETSTYLE_PARAGRAPHS_ONLY,
    wxRICHTEXT_SETSTYLE_CHARACTERS_ONLY,
    wxRICHTEXT_SETSTYLE_RENUMBER,
    wxRICHTEXT_SETSTYLE_SPECIFY_LEVEL,
    wxRICHTEXT_SETSTYLE_RESET,
    wxRICHTEXT_SETSTYLE_REMOVE,

/*!
 * Flags for text insertion
 */
    wxRICHTEXT_INSERT_NONE,
    wxRICHTEXT_INSERT_WITH_PREVIOUS_PARAGRAPH_STYLE,
    wxRICHTEXT_INSERT_INTERACTIVE,

    
// A special flag telling the buffer to keep the first paragraph style
// as-is, when deleting a paragraph marker. In future we might pass a
// flag to InsertFragment and DeleteRange to indicate the appropriate mode.
    wxTEXT_ATTR_KEEP_FIRST_PARA_STYLE,
};



/*!
 * Flags returned from hit-testing
 */
enum wxRichTextHitTestFlags {
    wxRICHTEXT_HITTEST_NONE,
    wxRICHTEXT_HITTEST_BEFORE,
    wxRICHTEXT_HITTEST_AFTER,
    wxRICHTEXT_HITTEST_ON,
    wxRICHTEXT_HITTEST_OUTSIDE,
    wxRICHTEXT_HITTEST_NO_NESTED_OBJECTS,
    wxRICHTEXT_HITTEST_NO_FLOATING_OBJECTS
};

typedef unsigned short wxTextAttrDimensionFlags;

// Miscelaneous text box flags
enum wxTextBoxAttrFlags
{
    wxTEXT_BOX_ATTR_FLOAT,
    wxTEXT_BOX_ATTR_CLEAR,
    wxTEXT_BOX_ATTR_COLLAPSE_BORDERS,
    wxTEXT_BOX_ATTR_VERTICAL_ALIGNMENT,
    wxTEXT_BOX_ATTR_BOX_STYLE_NAME
};

// Whether a value is present, used in dimension flags
enum wxTextAttrValueFlags
{
//     wxTEXT_ATTR_VALUE_PRESENT               = 0x1000,
//     wxTEXT_ATTR_VALUE_PRESENT_MASK          = 0x1000
};

// Units - included in the dimension value
enum wxTextAttrUnits
{
    wxTEXT_ATTR_UNITS_TENTHS_MM             = 0x0001,
    wxTEXT_ATTR_UNITS_PIXELS                = 0x0002,
    wxTEXT_ATTR_UNITS_PERCENTAGE            = 0x0004,
    wxTEXT_ATTR_UNITS_POINTS                = 0x0008,

    wxTEXT_ATTR_UNITS_MASK                  = 0x000F
};

// Position - included in the dimension flags
enum wxTextBoxAttrPosition
{
    wxTEXT_BOX_ATTR_POSITION_STATIC         = 0x0000, // Default is static, i.e. as per normal layout
    wxTEXT_BOX_ATTR_POSITION_RELATIVE       = 0x0010,
    wxTEXT_BOX_ATTR_POSITION_ABSOLUTE       = 0x0020,

    wxTEXT_BOX_ATTR_POSITION_MASK           = 0x00F0
};


//---------------------------------------------------------------------------
%newgroup

// Dimension, including units and position
class wxTextAttrDimension
{
public:
    %nokwargs wxTextAttrDimension;
    wxTextAttrDimension() { Reset(); }
    wxTextAttrDimension(int value, wxTextAttrUnits units = wxTEXT_ATTR_UNITS_TENTHS_MM);

    ~wxTextAttrDimension();
    
    void Reset();

    // Partial equality test
    bool EqPartial(const wxTextAttrDimension& dim) const;

    // Apply
    bool Apply(const wxTextAttrDimension& dim, const wxTextAttrDimension* compareWith = NULL);

    // Collects the attributes that are common to a range of content, building up a note of
    // which attributes are absent in some objects and which clash in some objects.
    void CollectCommonAttributes(const wxTextAttrDimension& attr, wxTextAttrDimension& clashingAttr, wxTextAttrDimension& absentAttr);

    bool operator==(const wxTextAttrDimension& dim) const;
    
    int GetValue() const; 
    float GetValueMM() const; 
    void SetValueMM(float value);

    %nokwargs SetValue;
    void SetValue(int value);
    void SetValue(int value, wxTextAttrDimensionFlags flags);
    void SetValue(const wxTextAttrDimension& dim);
    
    wxTextAttrUnits GetUnits() const;
    void SetUnits(wxTextAttrUnits units);
    
    wxTextBoxAttrPosition GetPosition() const;
    void SetPosition(wxTextBoxAttrPosition pos);
    
    wxTextAttrDimensionFlags GetFlags() const;
    void SetFlags(wxTextAttrDimensionFlags flags);
    
    int                         m_value;
    wxTextAttrDimensionFlags    m_flags;
};


// A class for left, right, top and bottom dimensions
class  wxTextAttrDimensions
{
public:
    wxTextAttrDimensions();
    ~wxTextAttrDimensions();
    
    void Reset() { m_left.Reset(); m_top.Reset(); m_right.Reset(); m_bottom.Reset(); }
    
    bool operator==(const wxTextAttrDimensions& dims) const { return m_left == dims.m_left && m_top == dims.m_top && m_right == dims.m_right && m_bottom == dims.m_bottom; }
    
    // Partial equality test
    bool EqPartial(const wxTextAttrDimensions& dims) const;

    // Apply border to 'this', but not if the same as compareWith
    bool Apply(const wxTextAttrDimensions& dims, const wxTextAttrDimensions* compareWith = NULL);

    // Collects the attributes that are common to a range of content, building up a note of
    // which attributes are absent in some objects and which clash in some objects.
    void CollectCommonAttributes(const wxTextAttrDimensions& attr, wxTextAttrDimensions& clashingAttr, wxTextAttrDimensions& absentAttr);

    // Remove specified attributes from this object
    bool RemoveStyle(const wxTextAttrDimensions& attr);

    wxTextAttrDimension& GetLeft() { return m_left; }

    wxTextAttrDimension& GetRight() { return m_right; }

    wxTextAttrDimension& GetTop() { return m_top; }

    wxTextAttrDimension& GetBottom() { return m_bottom; }

    bool IsValid() const;
    
    wxTextAttrDimension         m_left;
    wxTextAttrDimension         m_top;
    wxTextAttrDimension         m_right;
    wxTextAttrDimension         m_bottom;
};


// A class to make it easier to convert dimensions
class  wxTextAttrDimensionConverter
{
public:
    %nokwargs wxTextAttrDimensionConverter;
    wxTextAttrDimensionConverter(wxDC& dc, double scale = 1.0, const wxSize& parentSize = wxDefaultSize);
    wxTextAttrDimensionConverter(int ppi, double scale = 1.0, const wxSize& parentSize = wxDefaultSize);
    ~wxTextAttrDimensionConverter();
    
    int GetPixels(const wxTextAttrDimension& dim, int direction = wxHORIZONTAL) const;
    int GetTenthsMM(const wxTextAttrDimension& dim) const;

    int ConvertTenthsMMToPixels(int units) const;
    int ConvertPixelsToTenthsMM(int pixels) const;

    int     m_ppi;
    double  m_scale;
    wxSize  m_parentSize;
};


//---------------------------------------------------------------------------

// Border styles
enum wxTextAttrBorderStyle
{
    wxTEXT_BOX_ATTR_BORDER_NONE             = 0,
    wxTEXT_BOX_ATTR_BORDER_SOLID            = 1,
    wxTEXT_BOX_ATTR_BORDER_DOTTED           = 2,
    wxTEXT_BOX_ATTR_BORDER_DASHED           = 3,
    wxTEXT_BOX_ATTR_BORDER_DOUBLE           = 4,
    wxTEXT_BOX_ATTR_BORDER_GROOVE           = 5,
    wxTEXT_BOX_ATTR_BORDER_RIDGE            = 6,
    wxTEXT_BOX_ATTR_BORDER_INSET            = 7,
    wxTEXT_BOX_ATTR_BORDER_OUTSET           = 8
};

// Border style presence flags
enum wxTextAttrBorderFlags
{
    wxTEXT_BOX_ATTR_BORDER_STYLE            = 0x0001,
    wxTEXT_BOX_ATTR_BORDER_COLOUR           = 0x0002
};

// Border width symbols for qualitative widths
enum wxTextAttrBorderWidth
{
    wxTEXT_BOX_ATTR_BORDER_THIN             = -1,
    wxTEXT_BOX_ATTR_BORDER_MEDIUM           = -2,
    wxTEXT_BOX_ATTR_BORDER_THICK            = -3
};

// Float styles
enum wxTextBoxAttrFloatStyle
{
    wxTEXT_BOX_ATTR_FLOAT_NONE              = 0,
    wxTEXT_BOX_ATTR_FLOAT_LEFT              = 1,
    wxTEXT_BOX_ATTR_FLOAT_RIGHT             = 2
};

// Clear styles
enum wxTextBoxAttrClearStyle
{
    wxTEXT_BOX_ATTR_CLEAR_NONE              = 0,
    wxTEXT_BOX_ATTR_CLEAR_LEFT              = 1,
    wxTEXT_BOX_ATTR_CLEAR_RIGHT             = 2,
    wxTEXT_BOX_ATTR_CLEAR_BOTH              = 3
};

// Collapse mode styles. TODO: can they be switched on per side?
enum wxTextBoxAttrCollapseMode
{
    wxTEXT_BOX_ATTR_COLLAPSE_NONE           = 0,
    wxTEXT_BOX_ATTR_COLLAPSE_FULL           = 1
};

// Vertical alignment values
enum wxTextBoxAttrVerticalAlignment
{
    wxTEXT_BOX_ATTR_VERTICAL_ALIGNMENT_NONE =       0,
    wxTEXT_BOX_ATTR_VERTICAL_ALIGNMENT_TOP  =       1,
    wxTEXT_BOX_ATTR_VERTICAL_ALIGNMENT_CENTRE =     2,
    wxTEXT_BOX_ATTR_VERTICAL_ALIGNMENT_BOTTOM  =    3
};

/**
    @class wxTextAttrBorder
    A class representing a rich text object border.

    @library{wxrichtext}
    @category{richtext}

    @see wxRichTextAttr, wxRichTextCtrl, wxRichTextAttrBorders
*/

class wxTextAttrBorder
{
public:
    /**
        Default constructor.
    */
    wxTextAttrBorder() { Reset(); }

    /**
        Equality operator.
    */
    bool operator==(const wxTextAttrBorder& border) const
    {
        return m_flags == border.m_flags && m_borderStyle == border.m_borderStyle &&
               m_borderColour == border.m_borderColour && m_borderWidth == border.m_borderWidth;
    }

    /**
        Resets the border style, colour, width and flags.
    */
    void Reset() { m_borderStyle = 0; m_borderColour = 0; m_flags = 0; m_borderWidth.Reset(); }

    /**
        Partial equality test.
    */
    bool EqPartial(const wxTextAttrBorder& border) const;

    /**
        Applies the border to this object, but not if the same as @a compareWith.

    */
    bool Apply(const wxTextAttrBorder& border, const wxTextAttrBorder* compareWith = NULL);

    /**
        Removes the specified attributes from this object.
    */
    bool RemoveStyle(const wxTextAttrBorder& attr);

    /**
        Collects the attributes that are common to a range of content, building up a note of
        which attributes are absent in some objects and which clash in some objects.
    */
    void CollectCommonAttributes(const wxTextAttrBorder& attr, wxTextAttrBorder& clashingAttr, wxTextAttrBorder& absentAttr);

    /**
        Sets the border style.
    */
    void SetStyle(int style) { m_borderStyle = style; m_flags |= wxTEXT_BOX_ATTR_BORDER_STYLE; }

    /**
        Gets the border style.

    */
    int GetStyle() const { return m_borderStyle; }

    /**
        Sets the border colour.
    */
    void SetColour(unsigned long colour) { m_borderColour = colour; m_flags |= wxTEXT_BOX_ATTR_BORDER_COLOUR; }

    /**
        Sets the border colour.
    */
    void SetColour(const wxColour& colour) { m_borderColour = colour.GetRGB(); m_flags |= wxTEXT_BOX_ATTR_BORDER_COLOUR; }

    /**
        Gets the colour as a long.
    */
    unsigned long GetColourLong() const { return m_borderColour; }

    /**
        Gets the colour.
    */
    wxColour GetColour() const { return wxColour(m_borderColour); }

    /**
        Gets the border width.
    */
    wxTextAttrDimension& GetWidth() { return m_borderWidth; }
    const wxTextAttrDimension& GetWidth() const { return m_borderWidth; }

    /**
        Sets the border width.
    */
    void SetWidth(const wxTextAttrDimension& width) { m_borderWidth = width; }
    /**
        Sets the border width.
    */
    void SetWidth(int value, wxTextAttrUnits units = wxTEXT_ATTR_UNITS_TENTHS_MM) { SetWidth(wxTextAttrDimension(value, units)); }

    /**
        True if the border has a valid style.
    */
    bool HasStyle() const { return (m_flags & wxTEXT_BOX_ATTR_BORDER_STYLE) != 0; }

    /**
        True if the border has a valid colour.
    */
    bool HasColour() const { return (m_flags & wxTEXT_BOX_ATTR_BORDER_COLOUR) != 0; }

    /**
        True if the border has a valid width.
    */
    bool HasWidth() const { return m_borderWidth.IsValid(); }

    /**
        True if the border is valid.
    */
    bool IsValid() const { return HasWidth(); }

    /**
        Set the valid flag for this border.
    */
    void MakeValid() { m_borderWidth.SetValid(true); }

    /**
        Returns the border flags.
    */
    int GetFlags() const { return m_flags; }

    /**
        Sets the border flags.
    */
    void SetFlags(int flags) { m_flags = flags; }

    /**
        Adds a border flag.
    */
    void AddFlag(int flag) { m_flags |= flag; }

    /**
        Removes a border flag.
    */
    void RemoveFlag(int flag) { m_flags &= ~flag; }

    int                         m_borderStyle;
    unsigned long               m_borderColour;
    wxTextAttrDimension         m_borderWidth;
    int                         m_flags;
};

/**
    @class wxTextAttrBorders
    A class representing a rich text object's borders.

    @library{wxrichtext}
    @category{richtext}

    @see wxRichTextAttr, wxRichTextCtrl, wxRichTextAttrBorder
*/

class wxTextAttrBorders
{
public:
    /**
        Default constructor.
    */
    wxTextAttrBorders() { }

    /**
        Equality operator.
    */
    bool operator==(const wxTextAttrBorders& borders) const
    {
        return m_left == borders.m_left && m_right == borders.m_right &&
               m_top == borders.m_top && m_bottom == borders.m_bottom;
    }

    /**
        Sets the style of all borders.
    */
    void SetStyle(int style);

    /**
        Sets colour of all borders.
    */
    void SetColour(unsigned long colour);

    /**
        Sets the colour for all borders.
    */
    void SetColour(const wxColour& colour);

    /**
        Sets the width of all borders.
    */
    void SetWidth(const wxTextAttrDimension& width);

    /**
        Sets the width of all borders.
    */
    void SetWidth(int value, wxTextAttrUnits units = wxTEXT_ATTR_UNITS_TENTHS_MM) { SetWidth(wxTextAttrDimension(value, units)); }

    /**
        Resets all borders.
    */
    void Reset() { m_left.Reset(); m_right.Reset(); m_top.Reset(); m_bottom.Reset(); }

    /**
        Partial equality test.
    */
    bool EqPartial(const wxTextAttrBorders& borders) const;

    /**
        Applies border to this object, but not if the same as @a compareWith.
    */
    bool Apply(const wxTextAttrBorders& borders, const wxTextAttrBorders* compareWith = NULL);

    /**
        Removes the specified attributes from this object.
    */
    bool RemoveStyle(const wxTextAttrBorders& attr);

    /**
        Collects the attributes that are common to a range of content, building up a note of
        which attributes are absent in some objects and which clash in some objects.
    */
    void CollectCommonAttributes(const wxTextAttrBorders& attr, wxTextAttrBorders& clashingAttr, wxTextAttrBorders& absentAttr);

    /**
        Returns @true if all borders are valid.
    */
    bool IsValid() const { return m_left.IsValid() || m_right.IsValid() || m_top.IsValid() || m_bottom.IsValid(); }

    /**
        Returns the left border.
    */
    const wxTextAttrBorder& GetLeft() const { return m_left; }
    wxTextAttrBorder& GetLeft() { return m_left; }

    /**
        Returns the right border.
    */
    const wxTextAttrBorder& GetRight() const { return m_right; }
    wxTextAttrBorder& GetRight() { return m_right; }

    /**
        Returns the top border.
    */
    const wxTextAttrBorder& GetTop() const { return m_top; }
    wxTextAttrBorder& GetTop() { return m_top; }

    /**
        Returns the bottom border.
    */
    const wxTextAttrBorder& GetBottom() const { return m_bottom; }
    wxTextAttrBorder& GetBottom() { return m_bottom; }

    wxTextAttrBorder m_left, m_right, m_top, m_bottom;

};

/**
    @class wxTextBoxAttr
    A class representing the box attributes of a rich text object.

    @library{wxrichtext}
    @category{richtext}

    @see wxRichTextAttr, wxRichTextCtrl
*/

class wxTextBoxAttr
{
public:
    /**
        Default constructor.
    */
    wxTextBoxAttr() { Init(); }

    /**
        Copy constructor.
    */
    wxTextBoxAttr(const wxTextBoxAttr& attr) { Init(); (*this) = attr; }

    /**
        Initialises this object.
    */
    void Init() { Reset(); }

    /**
        Resets this object.
    */
    void Reset();

    // Copy. Unnecessary since we let it do a binary copy
    //void Copy(const wxTextBoxAttr& attr);

    // Assignment
    //void operator= (const wxTextBoxAttr& attr);

    /**
        Equality test.
    */
    bool operator== (const wxTextBoxAttr& attr) const;

    /**
        Partial equality test, ignoring unset attributes.

    */
    bool EqPartial(const wxTextBoxAttr& attr) const;

    /**
        Merges the given attributes. If @a compareWith is non-NULL, then it will be used
        to mask out those attributes that are the same in style and @a compareWith, for
        situations where we don't want to explicitly set inherited attributes.
    */
    bool Apply(const wxTextBoxAttr& style, const wxTextBoxAttr* compareWith = NULL);

    /**
        Collects the attributes that are common to a range of content, building up a note of
        which attributes are absent in some objects and which clash in some objects.
    */
    void CollectCommonAttributes(const wxTextBoxAttr& attr, wxTextBoxAttr& clashingAttr, wxTextBoxAttr& absentAttr);

    /**
        Removes the specified attributes from this object.
    */
    bool RemoveStyle(const wxTextBoxAttr& attr);

    /**
        Sets the flags.
    */
    void SetFlags(int flags) { m_flags = flags; }

    /**
        Returns the flags.
    */
    int GetFlags() const { return m_flags; }

    /**
        Is this flag present?
    */
    bool HasFlag(wxTextBoxAttrFlags flag) const { return (m_flags & flag) != 0; }

    /**
        Removes this flag.
    */
    void RemoveFlag(wxTextBoxAttrFlags flag) { m_flags &= ~flag; }

    /**
        Adds this flag.
    */
    void AddFlag(wxTextBoxAttrFlags flag) { m_flags |= flag; }

    /**
        Returns @true if no attributes are set.
    */
//    bool IsDefault() const;

    /**
        Returns the float mode.
    */
    wxTextBoxAttrFloatStyle GetFloatMode() const { return m_floatMode; }

    /**
        Sets the float mode.
    */
    void SetFloatMode(wxTextBoxAttrFloatStyle mode) { m_floatMode = mode; m_flags |= wxTEXT_BOX_ATTR_FLOAT; }

    /**
        Returns @true if float mode is active.
    */
    bool HasFloatMode() const { return HasFlag(wxTEXT_BOX_ATTR_FLOAT); }

    /**
        Returns @true if this object is floating?
    */
    bool IsFloating() const { return HasFloatMode() && GetFloatMode() != wxTEXT_BOX_ATTR_FLOAT_NONE; }

    /**
        Returns the clear mode - whether to wrap text after object. Currently unimplemented.
    */
    wxTextBoxAttrClearStyle GetClearMode() const { return m_clearMode; }

    /**
        Set the clear mode. Currently unimplemented.
    */
    void SetClearMode(wxTextBoxAttrClearStyle mode) { m_clearMode = mode; m_flags |= wxTEXT_BOX_ATTR_CLEAR; }

    /**
        Returns @true if we have a clear flag.
    */
    bool HasClearMode() const { return HasFlag(wxTEXT_BOX_ATTR_CLEAR); }

    /**
        Returns the collapse mode - whether to collapse borders. Currently unimplemented.
    */
    wxTextBoxAttrCollapseMode GetCollapseBorders() const { return m_collapseMode; }

    /**
        Sets the collapse mode - whether to collapse borders. Currently unimplemented.
    */
    void SetCollapseBorders(wxTextBoxAttrCollapseMode collapse) { m_collapseMode = collapse; m_flags |= wxTEXT_BOX_ATTR_COLLAPSE_BORDERS; }

    /**
        Returns @true if the collapse borders flag is present.
    */
    bool HasCollapseBorders() const { return HasFlag(wxTEXT_BOX_ATTR_COLLAPSE_BORDERS); }

    /**
        Returns the vertical alignment.
    */
    wxTextBoxAttrVerticalAlignment GetVerticalAlignment() const { return m_verticalAlignment; }

    /**
        Sets the vertical alignment.
    */
    void SetVerticalAlignment(wxTextBoxAttrVerticalAlignment verticalAlignment) { m_verticalAlignment = verticalAlignment; m_flags |= wxTEXT_BOX_ATTR_VERTICAL_ALIGNMENT; }

    /**
        Returns @true if a vertical alignment flag is present.
    */
    bool HasVerticalAlignment() const { return HasFlag(wxTEXT_BOX_ATTR_VERTICAL_ALIGNMENT); }

    /**
        Returns the margin values.
    */
    wxTextAttrDimensions& GetMargins() { return m_margins; }
    const wxTextAttrDimensions& GetMargins() const { return m_margins; }

    /**
        Returns the left margin.
    */
    wxTextAttrDimension& GetLeftMargin() { return m_margins.m_left; }
    const wxTextAttrDimension& GetLeftMargin() const { return m_margins.m_left; }

    /**
        Returns the right margin.
    */
    wxTextAttrDimension& GetRightMargin() { return m_margins.m_right; }
    const wxTextAttrDimension& GetRightMargin() const { return m_margins.m_right; }

    /**
        Returns the top margin.
    */
    wxTextAttrDimension& GetTopMargin() { return m_margins.m_top; }
    const wxTextAttrDimension& GetTopMargin() const { return m_margins.m_top; }

    /**
        Returns the bottom margin.
    */
    wxTextAttrDimension& GetBottomMargin() { return m_margins.m_bottom; }
    const wxTextAttrDimension& GetBottomMargin() const { return m_margins.m_bottom; }

    /**
        Returns the position.
    */
    wxTextAttrDimensions& GetPosition() { return m_position; }
    const wxTextAttrDimensions& GetPosition() const { return m_position; }

    /**
        Returns the left position.
    */
    wxTextAttrDimension& GetLeft() { return m_position.m_left; }
    const wxTextAttrDimension& GetLeft() const { return m_position.m_left; }

    /**
        Returns the right position.
    */
    wxTextAttrDimension& GetRight() { return m_position.m_right; }
    const wxTextAttrDimension& GetRight() const { return m_position.m_right; }

    /**
        Returns the top position.
    */
    wxTextAttrDimension& GetTop() { return m_position.m_top; }
    const wxTextAttrDimension& GetTop() const { return m_position.m_top; }

    /**
        Returns the bottom position.
    */
    wxTextAttrDimension& GetBottom() { return m_position.m_bottom; }
    const wxTextAttrDimension& GetBottom() const { return m_position.m_bottom; }

    /**
        Returns the padding values.
    */
    wxTextAttrDimensions& GetPadding() { return m_padding; }
    const wxTextAttrDimensions& GetPadding() const { return m_padding; }

    /**
        Returns the left padding value.
    */
    wxTextAttrDimension& GetLeftPadding() { return m_padding.m_left; }
    const wxTextAttrDimension& GetLeftPadding() const { return m_padding.m_left; }

    /**
        Returns the right padding value.
    */
    wxTextAttrDimension& GetRightPadding() { return m_padding.m_right; }
    const wxTextAttrDimension& GetRightPadding() const { return m_padding.m_right; }

    /**
        Returns the top padding value.
    */
    wxTextAttrDimension& GetTopPadding() { return m_padding.m_top; }
    const wxTextAttrDimension& GetTopPadding() const { return m_padding.m_top; }

    /**
        Returns the bottom padding value.
    */
    wxTextAttrDimension& GetBottomPadding() { return m_padding.m_bottom; }
    const wxTextAttrDimension& GetBottomPadding() const { return m_padding.m_bottom; }

    /**
        Returns the borders.
    */
    wxTextAttrBorders& GetBorder() { return m_border; }
    const wxTextAttrBorders& GetBorder() const { return m_border; }

    /**
        Returns the left border.
    */
    wxTextAttrBorder& GetLeftBorder() { return m_border.m_left; }
    const wxTextAttrBorder& GetLeftBorder() const { return m_border.m_left; }

    /**
        Returns the top border.
    */
    wxTextAttrBorder& GetTopBorder() { return m_border.m_top; }
    const wxTextAttrBorder& GetTopBorder() const { return m_border.m_top; }

    /**
        Returns the right border.
    */
    wxTextAttrBorder& GetRightBorder() { return m_border.m_right; }
    const wxTextAttrBorder& GetRightBorder() const { return m_border.m_right; }

    /**
        Returns the bottom border.
    */
    wxTextAttrBorder& GetBottomBorder() { return m_border.m_bottom; }
    const wxTextAttrBorder& GetBottomBorder() const { return m_border.m_bottom; }

    /**
        Returns the outline.
    */
    wxTextAttrBorders& GetOutline() { return m_outline; }
    const wxTextAttrBorders& GetOutline() const { return m_outline; }

    /**
        Returns the left outline.
    */
    wxTextAttrBorder& GetLeftOutline() { return m_outline.m_left; }
    const wxTextAttrBorder& GetLeftOutline() const { return m_outline.m_left; }

    /**
        Returns the top outline.
    */
    wxTextAttrBorder& GetTopOutline() { return m_outline.m_top; }
    const wxTextAttrBorder& GetTopOutline() const { return m_outline.m_top; }

    /**
        Returns the right outline.
    */
    wxTextAttrBorder& GetRightOutline() { return m_outline.m_right; }
    const wxTextAttrBorder& GetRightOutline() const { return m_outline.m_right; }

    /**
        Returns the bottom outline.
    */
    wxTextAttrBorder& GetBottomOutline() { return m_outline.m_bottom; }
    const wxTextAttrBorder& GetBottomOutline() const { return m_outline.m_bottom; }

    /**
        Returns the object size.
    */
    wxTextAttrSize& GetSize() { return m_size; }
    const wxTextAttrSize& GetSize() const { return m_size; }

    /**
        Sets the object size.
    */
    void SetSize(const wxTextAttrSize& sz) { m_size = sz; }

    /**
        Returns the object width.
    */
    wxTextAttrDimension& GetWidth() { return m_size.m_width; }
    const wxTextAttrDimension& GetWidth() const { return m_size.m_width; }

    /**
        Returns the object height.
    */
    wxTextAttrDimension& GetHeight() { return m_size.m_height; }
    const wxTextAttrDimension& GetHeight() const { return m_size.m_height; }

    /**
        Returns the box style name.
    */
    const wxString& GetBoxStyleName() const { return m_boxStyleName; }

    /**
        Sets the box style name.
    */
    void SetBoxStyleName(const wxString& name) { m_boxStyleName = name; AddFlag(wxTEXT_BOX_ATTR_BOX_STYLE_NAME); }

    /**
        Returns @true if the box style name is present.
    */
    bool HasBoxStyleName() const { return HasFlag(wxTEXT_BOX_ATTR_BOX_STYLE_NAME); }
    
public:

    int                             m_flags;

    wxTextAttrDimensions            m_margins;
    wxTextAttrDimensions            m_padding;
    wxTextAttrDimensions            m_position;

    wxTextAttrSize                  m_size;

    wxTextAttrBorders               m_border;
    wxTextAttrBorders               m_outline;

    wxTextBoxAttrFloatStyle         m_floatMode;
    wxTextBoxAttrClearStyle         m_clearMode;
    wxTextBoxAttrCollapseMode       m_collapseMode;
    wxTextBoxAttrVerticalAlignment  m_verticalAlignment;
    wxString                        m_boxStyleName;
};


//---------------------------------------------------------------------------
%newgroup

// RTC is now using the same attr class as wx.TextCtrl.
class wxTextAttr;


class wxRichTextAttr: public wxTextAttr
{
public:
    %nokwargs wxRichTextAttr;
    wxRichTextAttr(const wxTextAttr& attr) { wxTextAttr::Copy(attr); }
    wxRichTextAttr(const wxRichTextAttr& attr) { Copy(attr); }
    wxRichTextAttr() {}

    ~wxRichTextAttr();
    
    
    // Copy
    void Copy(const wxRichTextAttr& attr);
    
    // Assignment
//    void operator=(const wxRichTextAttr& attr) { Copy(attr); }
//    void operator=(const wxTextAttr& attr) { wxTextAttr::Copy(attr); }
    
    // Equality test
    bool operator==(const wxRichTextAttr& attr) const;

    // Partial equality test taking comparison object into account
    bool EqPartial(const wxRichTextAttr& attr) const;

    // Merges the given attributes. If compareWith
    // is non-NULL, then it will be used to mask out those attributes that are the same in style
    // and compareWith, for situations where we don't want to explicitly set inherited attributes.
    bool Apply(const wxRichTextAttr& style, const wxRichTextAttr* compareWith = NULL);

    // Collects the attributes that are common to a range of content, building up a note of
    // which attributes are absent in some objects and which clash in some objects.
    void CollectCommonAttributes(const wxRichTextAttr& attr, wxRichTextAttr& clashingAttr, wxRichTextAttr& absentAttr);

    // Remove specified attributes from this object
    bool RemoveStyle(const wxRichTextAttr& attr);

    wxTextBoxAttr& GetTextBoxAttr() { return m_textBoxAttr; }
    const wxTextBoxAttr& GetTextBoxAttr() const { return m_textBoxAttr; }
    void SetTextBoxAttr(const wxTextBoxAttr& attr) { m_textBoxAttr = attr; }
    
    wxTextBoxAttr    m_textBoxAttr;
};





// class WXDLLIMPEXP_RICHTEXT wxRichTextProperties: public wxObject
// {
// DECLARE_DYNAMIC_CLASS(wxRichTextProperties)
// public:
//     wxRichTextProperties() {}
//     wxRichTextProperties(const wxRichTextProperties& props) { Copy(props); }

//     void operator=(const wxRichTextProperties& props) { Copy(props); }
//     bool operator==(const wxRichTextProperties& props) const;
//     void Copy(const wxRichTextProperties& props) { m_properties = props.m_properties; }
//     const wxVariant& operator[](size_t idx) const { return m_properties[idx]; }
//     wxVariant& operator[](size_t idx) { return m_properties[idx]; }
//     void Clear() { m_properties.Clear(); }

//     const wxRichTextVariantArray& GetProperties() const { return m_properties; }
//     wxRichTextVariantArray& GetProperties() { return m_properties; }
//     void SetProperties(const wxRichTextVariantArray& props) { m_properties = props; }

//     wxArrayString GetPropertyNames() const;

//     size_t GetCount() const { return m_properties.GetCount(); }

//     int HasProperty(const wxString& name) const { return Find(name) != -1; }

//     int Find(const wxString& name) const;
//     const wxVariant& GetProperty(const wxString& name) const;
//     wxVariant* FindOrCreateProperty(const wxString& name);

//     wxString GetPropertyString(const wxString& name) const;
//     long GetPropertyLong(const wxString& name) const;
//     bool GetPropertyBool(const wxString& name) const;
//     double GetPropertyDouble(const wxString& name) const;

//     void SetProperty(const wxVariant& variant);
//     void SetProperty(const wxString& name, const wxVariant& variant);
//     void SetProperty(const wxString& name, const wxString& value);
//     void SetProperty(const wxString& name, long value);
//     void SetProperty(const wxString& name, double value);
//     void SetProperty(const wxString& name, bool value);

// protected:
//     wxRichTextVariantArray  m_properties;
// };



//---------------------------------------------------------------------------



class wxRichTextFontTable: public wxObject
{
public:
    wxRichTextFontTable();
    virtual ~wxRichTextFontTable();

    bool IsOk() const;

    wxFont FindFont(const wxRichTextAttr& fontSpec);
    void Clear();
};


//---------------------------------------------------------------------------

%typemap(in) wxRichTextRange& (wxRichTextRange temp) {
    $1 = &temp;
    if ( ! wxRichTextRange_helper($input, &$1)) SWIG_fail;
}
%typemap(typecheck, precedence=SWIG_TYPECHECK_POINTER) wxRichTextRange& {
    $1 = wxPySimple_typecheck($input, wxT("wxRichTextRange"), 2);
}


%{
bool wxRichTextRange_helper(PyObject* source, wxRichTextRange** obj)
{
    if (source == Py_None) {
        **obj = wxRICHTEXT_NONE;
        return true;
    }
    return wxPyTwoIntItem_helper(source, obj, wxT("wxRichTextRange"));
}
%}


DocStr(wxRichTextRange,
"RichTextRange is a data structure that represents a range of text
within a `RichTextCtrl`.  It simply contains integer ``start`` and
``end`` properties and a few operations useful for dealing with
ranges.  In most places in wxPython where a RichTextRange is expected a
2-tuple containing (start, end) can be used instead.", "");

// Turn off the generation of code that aquires the Global Interpreter Lock
%threadWrapperOff

class wxRichTextRange
{
public:
    DocCtorStr(
        wxRichTextRange(long start=0, long end=0),
        "Creates a new range object.", "");

    ~wxRichTextRange();

    %extend {
        DocStr(__eq__, "Test for equality of RichTextRange objects.", "");
        bool __eq__(PyObject* other) {
            wxRichTextRange  temp, *obj = &temp;
            if ( other == Py_None ) return false;
            if ( ! wxRichTextRange_helper(other, &obj) ) {
                PyErr_Clear();
                return false;
            }
            return self->operator==(*obj);
        }
    }


    DocDeclStr(
        wxRichTextRange , operator -(const wxRichTextRange& range) const,
        "", "");

    DocDeclStr(
        wxRichTextRange , operator +(const wxRichTextRange& range) const,
        "", "");


    DocDeclStr(
        void , SetRange(long start, long end),
        "", "");


    DocDeclStr(
        void , SetStart(long start),
        "", "");
    DocDeclStr(
        long , GetStart() const,
        "", "");
    %pythoncode { start = property(GetStart, SetStart) }

    
    DocDeclStr(
        void , SetEnd(long end),
        "", "");
    DocDeclStr(
        long , GetEnd() const,
        "", "");
    %pythoncode { end = property(GetEnd, SetEnd) }


    DocDeclStr(
        bool , IsOutside(const wxRichTextRange& range) const,
        "Returns true if this range is completely outside 'range'", "");


    DocDeclStr(
        bool , IsWithin(const wxRichTextRange& range) const,
        "Returns true if this range is completely within 'range'", "");


    DocDeclStr(
        bool , Contains(long pos) const,
        "Returns true if the given position is within this range. Allow for the
possibility of an empty range - assume the position is within this
empty range.", "");


    DocDeclStr(
        bool , LimitTo(const wxRichTextRange& range) ,
        "Limit this range to be within 'range'", "");


    DocDeclStr(
        long , GetLength() const,
        "Gets the length of the range", "");


    DocDeclStr(
        void , Swap(),
        "Swaps the start and end", "");


    DocDeclStr(
        wxRichTextRange , ToInternal() const,
        "Convert to internal form: (n, n) is the range of a single character.", "");


    DocDeclStr(
        wxRichTextRange , FromInternal() const,
        "Convert from internal to public API form: (n, n+1) is the range of a
single character.", "");


    %extend {
        DocAStr(Get,
               "Get() -> (start,end)",
               "Returns the start and end properties as a tuple.", "");
        PyObject* Get() {
            PyObject* tup = PyTuple_New(2);
            PyTuple_SET_ITEM(tup, 0, PyInt_FromLong(self->GetStart()));
            PyTuple_SET_ITEM(tup, 1, PyInt_FromLong(self->GetEnd()));
            return tup;
        }
    }
    %pythoncode {
    def __str__(self):                   return str(self.Get())
    def __repr__(self):                  return 'RichTextRange'+str(self.Get())
    def __len__(self):                   return len(self.Get())
    def __getitem__(self, index):        return self.Get()[index]
    def __setitem__(self, index, val):
        if index == 0: self.start = val
        elif index == 1: self.end = val
        else: raise IndexError
    def __nonzero__(self):               return self.Get() != (0,0)
    __safe_for_unpickling__ = True
    def __reduce__(self):                return (RichTextRange, self.Get())
    }

    %property(End, GetEnd, SetEnd, doc="See `GetEnd` and `SetEnd`");
    %property(Length, GetLength, doc="See `GetLength`");
    %property(Start, GetStart, SetStart, doc="See `GetStart` and `SetStart`");
};



%{
    wxRichTextRange wxPy_RTR_ALL(wxRICHTEXT_ALL);
    wxRichTextRange wxPy_RTR_NONE(wxRICHTEXT_NONE);
%}

%rename(RICHTEXT_ALL)   wxPy_RTR_ALL;
%rename(RICHTEXT_NONE)  wxPy_RTR_NONE;

%immutable;
wxRichTextRange wxPy_RTR_ALL;
wxRichTextRange wxPy_RTR_NONE;
%mutable;

// Turn back on the generation of code that aquires the Global Interpreter Lock
%threadWrapperOn



//---------------------------------------------------------------------------
//---------------------------------------------------------------------------


// TODO TODO TODO
// There's still lots to do for these classes...
//
// 1. Decide how to coalesce overloaded methods and ctors
// 2. correctly set disown flags and re-ownership as needed
// 3. Implement PyRichTextObject
// 4. Decide how to typemap and tweak the virtuals that pass back
//    values in their parameters (yuck! damn C++)
// 5. better handling of streams
// 6. Add more properties



class wxRichTextDrawingContext: public wxObject
{
public:

    /**
        Pass the buffer to the context so the context can retrieve information
        such as virtual attributes.
    */
    wxRichTextDrawingContext(wxRichTextBuffer* buffer);
    void Init();

    /**
        Does this object have virtual attributes?
        Virtual attributes can be provided for visual cues without
        affecting the actual styling.
    */
    bool HasVirtualAttributes(wxRichTextObject* obj) const;

    /**
        Returns the virtual attributes for this object.
        Virtual attributes can be provided for visual cues without
        affecting the actual styling.
    */
    wxRichTextAttr GetVirtualAttributes(wxRichTextObject* obj) const;

    /**
        Applies any virtual attributes relevant to this object.
    */
    bool ApplyVirtualAttributes(wxRichTextAttr& attr, wxRichTextObject* obj) const;

    wxRichTextBuffer*   m_buffer;
};



DocStr(wxRichTextObject,
"This is the base class for all drawable objects in a `RichTextCtrl`.

The data displayed in a `RichTextCtrl` is handled by `RichTextBuffer`,
and a `RichTextCtrl` always has one such buffer.

The content is represented by a hierarchy of objects, all derived from
`RichTextObject`. An object might be an image, a fragment of text, a
paragraph, or a whole buffer. Objects store a an attribute object
containing style information; a paragraph object can contain both
paragraph and character information, but content objects such as text
can only store character information. The final style displayed in the
control or in a printout is a combination of base style, paragraph
style and content (character) style.

The top of the hierarchy is the buffer, a kind of
`RichTextParagraphLayoutBox`. containing further `RichTextParagraph`
objects, each of which can include text, images and potentially other
types of objects.

Each object maintains a range (start and end position) measured from
the start of the main parent object.

When Layout is called on an object, it is given a size which the
object must limit itself to, or one or more flexible directions
(vertical or horizontal). So, for example, a centred paragraph is
given the page width to play with (minus any margins), but can extend
indefinitely in the vertical direction. The implementation of Layout
caches the calculated size and position.

When the buffer is modified, a range is invalidated (marked as
requiring layout), so that only the minimum amount of layout is
performed.

A paragraph of pure text with the same style contains just one further
object, a `RichTextPlainText` object. When styling is applied to part
of this object, the object is decomposed into separate objects, one
object for each different character style. So each object within a
paragraph always has just one attribute object to denote its character
style. Of course, this can lead to fragmentation after a lot of edit
operations, potentially leading to several objects with the same style
where just one would do. So a Defragment function is called when
updating the control's display, to ensure that the minimum number of
objects is used.

To implement your own RichTextObjects in Python you must derive a
class from `PyRichTextObject`, which has been instrumented to forward
the virtual C++ method calls to the Python methods in the derived
class. (This class hasn't been implemented yet!)", "");

// argout typemap for wxPoint
%typemap(in, numinputs=0, noblock=1) wxPoint& OUTPUT (wxPoint temp) {
    $1 = &temp;
}
%typemap(argout, noblock=1) wxPoint& OUTPUT {
    %append_output(SWIG_NewPointerObj((void*)new wxPoint(*$1), $1_descriptor, SWIG_POINTER_OWN));
}

// argout typemap for wxSize
%typemap(in, numinputs=0, noblock=1) wxSize& OUTPUT (wxSize temp) {
    $1 = &temp;
}
%typemap(argout, noblock=1) wxSize& OUTPUT {
    %append_output(SWIG_NewPointerObj((void*)new wxSize(*$1), $1_descriptor, SWIG_POINTER_OWN));
}


// Typemap to use wxRTTI to return a proxy object whose type matches the real
// type of the C++ pointer.  NOTE: It's not a true OOR like can be done for
// wxWindow pointers, but at least the type is corerct.
%typemap(out) wxRichTextObject* {
    $result = wxPyMake_wxObject($1, (bool)$owner);
}


class wxRichTextObject: public wxObject
{
public:
    // wxRichTextObject(wxRichTextObject* parent = NULL);  // **** This is an ABC
    virtual ~wxRichTextObject();


// Overrideables

    /// Draw the item, within the given range. Some objects may ignore the range (for
    /// example paragraphs) while others must obey it (lines, to implement wrapping)
    virtual bool Draw(wxDC& dc,
                      wxRichTextDrawingContext& context, 
                      const wxRichTextRange& range,
                      const wxRichTextSelection& selection,
                      const wxRect& rect, int descent, int style);

    /// Lay the item out at the specified position with the given size constraint.
    /// Layout must set the cached size.
    virtual bool Layout(wxDC& dc,
                        wxRichTextDrawingContext& context,
                        const wxRect& rect, const wxRect& parentRect,
                        int style);

    /// Hit-testing: returns a flag indicating hit test details, plus
    /// information about position
    virtual int HitTest(wxDC& dc,
                        wxRichTextDrawingContext& context,
                        const wxPoint& pt, long& OUTPUT /*textPosition*/,
                        wxRichTextObject** obj, wxRichTextObject** contextObj,
                        int flags = 0);

    /// Finds the absolute position and row height for the given character position
    virtual bool FindPosition(wxDC& dc,
                              wxRichTextDrawingContext& context,
                              long index, wxPoint& OUTPUT /*pt*/,
                              int* OUTPUT /*height*/, bool forceLineStart);
    

    /// Get the best size, i.e. the ideal starting size for this object irrespective
    /// of available space. For a short text string, it will be the size that exactly encloses
    /// the text. For a longer string, it might use the parent width for example.
    virtual wxSize GetBestSize() const;

    /// Get the object size for the given range. Returns false if the range
    /// is invalid for this object.
    virtual bool GetRangeSize(const wxRichTextRange& range,
                              wxSize& OUTPUT /*size*/,
                              int& OUTPUT /*descent*/,
                              wxDC& dc,
                              wxRichTextDrawingContext& context,
                              int flags,
                              wxPoint position = wxPoint(0,0)
          /** TODO */         /*wxArrayInt* partialExtents=NULL*/
                              ) const;

    /// Do a split, returning an object containing the second part, and setting
    /// the first part in 'this'.
    %newobject DoSplit;
    virtual wxRichTextObject* DoSplit(long pos);

    /// Calculate range. By default, guess that the object is 1 unit long.
    virtual void CalculateRange(long start, long& OUTPUT /*end*/);

    /// Delete range
    virtual bool DeleteRange(const wxRichTextRange& range);

    /// Returns true if the object is empty
    virtual bool IsEmpty() const;

    /// Whether this object floatable
    virtual bool IsFloatable() const { return false; }

    /// Whether this object is currently floating
    virtual bool IsFloating() const { return GetAttributes().GetTextBoxAttr().IsFloating(); }

    /// Whether this object is a place holding one
    // virtual bool IsPlaceHolding() const { return false; }

    /// The floating direction
    virtual int GetFloatDirection() const { return GetAttributes().GetTextBoxAttr().GetFloatMode(); }

    
    /// Get any text in this object for the given range
    virtual wxString GetTextForRange(const wxRichTextRange& range) const;

    /// Returns true if this object can merge itself with the given one.
    virtual bool CanMerge(wxRichTextObject* object, wxRichTextDrawingContext& context) const;

    /// Returns true if this object merged itself with the given one.
    /// The calling code will then delete the given object.
    %feature("shadow") Merge %{
      def Merge(self, obj, context):
            """Merge(self, RichTextObject object) -> bool"""
            val = _richtext.RichTextObject_Merge(self, obj, context)
            if val:
                obj.this.own(True)
            return val
    %}
    virtual bool Merge(wxRichTextObject* object, wxRichTextDrawingContext& context);

    /// Dump to output stream for debugging
    //virtual void Dump(wxTextOutputStream& stream);
    %extend {
        wxString Dump() {
            wxStringOutputStream strstream;
            wxTextOutputStream txtstream(strstream);
            self->Dump(txtstream);
            return strstream.GetString();
        }
    }

    /// Can we edit properties via a GUI?
    virtual bool CanEditProperties() const { return false; }

    /// Edit properties via a GUI
    virtual bool EditProperties(wxWindow* WXUNUSED(parent), wxRichTextBuffer* WXUNUSED(buffer)) { return false; }

    /// Import this object from XML
    virtual bool ImportFromXML(wxRichTextBuffer* buffer,
                               wxXmlNode* node,
                               wxRichTextXMLHandler* handler,
                               bool* recurse);

    /// Export this object directly to the given stream.
    virtual bool ExportXML(wxOutputStream& stream, int indent, wxRichTextXMLHandler* handler);

    /// Export this object to the given parent node, usually creating at least one child node.
    virtual bool ExportXML(wxXmlNode* parent, wxRichTextXMLHandler* handler);

    /// Does this object take note of paragraph attributes? Text and image objects don't.
    virtual bool UsesParagraphAttributes() const { return true; }
    
    /// What is the XML node name of this object?
    virtual wxString GetXMLNodeName() const { return wxT("unknown"); }

// Accessors

    /// Get/set the cached object size as calculated by Layout.
    virtual wxSize GetCachedSize() const;
    virtual void SetCachedSize(const wxSize& sz);
    %property(CachedSize, GetCachedSize, SetCachedSize);

    /// Get/set the object position
    virtual wxPoint GetPosition() const;
    virtual void SetPosition(const wxPoint& pos);
    %property(Position, GetPosition, SetPosition);

    /// Get the rectangle enclosing the object
    virtual wxRect GetRect() const;
    %property(Rect, GetRect);


    /// Set the range
    void SetRange(const wxRichTextRange& range);
    /// Get the range
    wxRichTextRange GetRange();
    %property(Range, GetRange, SetRange);


    /// Is this composite?
    virtual bool IsComposite() const;

    /// Get/set the parent.
    virtual wxRichTextObject* GetParent() const;
    virtual void SetParent(wxRichTextObject* parent);
    %property(Parent, GetParent, SetParent);


    // TODO: Morph these into SetLeftMargin and etc. for wxPython so
    // there can be proper properties

    /// Set the margin around the object
    %Rename(SetSameMargins,
            virtual void , SetMargins(int margin));
    virtual void SetMargins(int leftMargin, int rightMargin, int topMargin, int bottomMargin);
    virtual int GetLeftMargin() const;
    virtual int GetRightMargin() const;
    virtual int GetTopMargin() const;
    virtual int GetBottomMargin() const;


    /// Set attributes object
    void SetAttributes(const wxRichTextAttr& attr);
    wxRichTextAttr GetAttributes();
    %property(Attributes, GetAttributes, SetAttributes);

    // /// Set/get properties
    // wxRichTextProperties& GetProperties() { return m_properties; }
    // const wxRichTextProperties& GetProperties() const { return m_properties; }
    // void SetProperties(const wxRichTextProperties& props) { m_properties = props; }
    
    /// Set/get stored descent
    void SetDescent(int descent);
    int GetDescent() const;
    %property(Descent, GetDescent, SetDescent);

    /// Gets the containing buffer
    wxRichTextBuffer* GetBuffer() const;

// Operations

    /// Clone the object
    %newobject Clone;  
    virtual wxRichTextObject* Clone() const;

    /// Copy
    void Copy(const wxRichTextObject& obj);

    /// Reference-counting allows us to use the same object in multiple
    /// lists (not yet used)
    void Reference();
    void Dereference();

    /// Convert units in tenths of a millimetre to device units
    %Rename(ConvertTenthsMMToPixelsDC,
            int, ConvertTenthsMMToPixels(wxDC& dc, int units));
    static int ConvertTenthsMMToPixels(int ppi, int units, double scale = 1.0);


    /// Convert units in pixels to tenths of a millimetre
    int ConvertPixelsToTenthsMM(wxDC& dc, int pixels) const;
    static int ConvertPixelsToTenthsMM(int ppi, int pixels, double scale = 1.0);
    
    /// Draw the borders and background for the given rectangle and attributes.
    /// Width and height are taken to be the content size, so excluding any
    /// border, margin and padding.
    static bool DrawBoxAttributes(wxDC& dc,
                                  wxRichTextBuffer* buffer,
                                  const wxRichTextAttr& attr,
                                  const wxRect& boxRect,
                                  int flags = 0);

    /// Draw a border
    static bool DrawBorder(wxDC& dc, wxRichTextBuffer* buffer, const wxTextAttrBorders& attr, const wxRect& rect, int flags = 0);


    /// Get the various rectangles of the box model in pixels. You can either specify contentRect (inner)
    /// or marginRect (outer), and the other must be the default rectangle (no width or height).
    /// Note that the outline doesn't affect the position of the rectangle, it's drawn in whatever space
    /// is available.
    static bool GetBoxRects(wxDC& dc, wxRichTextBuffer* buffer, const wxRichTextAttr& attr, wxRect& marginRect, wxRect& borderRect, wxRect& contentRect, wxRect& paddingRect, wxRect& outlineRect);
    
    /// Get the total margin for the object in pixels, taking into account margin, padding and border size
    static bool GetTotalMargin(wxDC& dc, wxRichTextBuffer* buffer, const wxRichTextAttr& attr, int& leftMargin, int& rightMargin,
        int& topMargin, int& bottomMargin);

    /// Returns the rectangle which the child has available to it given restrictions specified in the
    /// child attribute, e.g. 50% width of the parent, 400 pixels, x position 20% of the parent, etc.
    static wxRect AdjustAvailableSpace(wxDC& dc, wxRichTextBuffer* buffer,
                                       const wxRichTextAttr& parentAttr,
                                       const wxRichTextAttr& childAttr,
                                       const wxRect& availableParentSpace,
                                       const wxRect& availableContainerSpace);
};




wxLIST_WRAPPER(wxRichTextObjectList, wxRichTextObject);

    
DocStr(wxRichTextCompositeObject,
       "Objects of this class can contain other rich text objects.", "");


class wxRichTextCompositeObject: public wxRichTextObject
{
public:
    // wxRichTextCompositeObject(wxRichTextObject* parent = NULL);   **** This is an ABC
    virtual ~wxRichTextCompositeObject();

// Accessors

    /// Get the children
    wxRichTextObjectList& GetChildren();

    /// Get the child count
    size_t GetChildCount() const ;

    /// Get the nth child
    wxRichTextObject* GetChild(size_t n) const ;

// Operations

    /// Copy
    void Copy(const wxRichTextCompositeObject& obj);

    %disownarg(wxRichTextObject* child);
    
    /// Append a child, returning the position
    size_t AppendChild(wxRichTextObject* child) ;

    /// Insert the child in front of the given object, or at the beginning
    bool InsertChild(wxRichTextObject* child, wxRichTextObject* inFrontOf) ;

    %cleardisown(wxRichTextObject* child);

    
    /// Delete the child
    %feature("shadow") RemoveChild %{
        def RemoveChild(self, child, deleteChild=False):
            val = _richtext.RichTextCompositeObject_RemoveChild(self, child, deleteChild)
            self.this.own(not deleteChild)
            return val
    %}
    bool RemoveChild(wxRichTextObject* child, bool deleteChild = false) ;

    /// Delete all children
    bool DeleteChildren();

    /// Recursively merge all pieces that can be merged.
    bool Defragment(wxRichTextDrawingContext& context, const wxRichTextRange& range = wxRICHTEXT_ALL);
};





DocStr(wxRichTextParagraphLayoutBox,
       "This box knows how to lay out paragraphs.", "");

class wxRichTextParagraphLayoutBox: public wxRichTextCompositeObject
{
public:
    %nokwargs wxRichTextParagraphLayoutBox;
    wxRichTextParagraphLayoutBox(wxRichTextObject* parent = NULL);
    wxRichTextParagraphLayoutBox(const wxRichTextParagraphLayoutBox& obj): wxRichTextCompositeObject() { Init(); Copy(obj); }
    ~wxRichTextParagraphLayoutBox();


// Accessors

    /// Associate a control with the buffer, for operations that for example require refreshing the window.
    void SetRichTextCtrl(wxRichTextCtrl* ctrl) { m_ctrl = ctrl; }

    /// Get the associated control.
    wxRichTextCtrl* GetRichTextCtrl() const { return m_ctrl; }

    /// Get/set whether the last paragraph is partial or complete
    void SetPartialParagraph(bool partialPara) { m_partialParagraph = partialPara; }
    bool GetPartialParagraph() const { return m_partialParagraph; }

    /// If this is a buffer, returns the current style sheet. The base layout box
    /// class doesn't have an associated style sheet.
    virtual wxRichTextStyleSheet* GetStyleSheet() const { return NULL; }

// Operations
    /// Draw the floats of this buffer
    void DrawFloats(wxDC& dc, wxRichTextDrawingContext& context,
                    const wxRichTextRange& range,
                    const wxRichTextSelection& selection,
                    const wxRect& rect, int descent, int style);

    /// Move an anchored object to another paragraph
    void MoveAnchoredObjectToParagraph(wxRichTextParagraph* from, wxRichTextParagraph* to, wxRichTextObject* obj);

    /// Initialize the object.
    void Init();

    /// Clear all children
    virtual void Clear();

    /// Clear and initialize with one blank paragraph
    virtual void Reset();

    /// Convenience function to add a paragraph of text
    virtual wxRichTextRange AddParagraph(const wxString& text, wxRichTextAttr* paraStyle = NULL);

    /// Convenience function to add an image
    virtual wxRichTextRange AddImage(const wxImage& image, wxRichTextAttr* paraStyle = NULL);

    /// Adds multiple paragraphs, based on newlines.
    virtual wxRichTextRange AddParagraphs(const wxString& text, wxRichTextAttr* paraStyle = NULL);

    /// Get the line at the given position. If caretPosition is true, the position is
    /// a caret position, which is normally a smaller number.
    virtual wxRichTextLine* GetLineAtPosition(long pos, bool caretPosition = false) const;

    /// Get the line at the given y pixel position, or the last line.
    virtual wxRichTextLine* GetLineAtYPosition(int y) const;

    /// Get the paragraph at the given character or caret position
    virtual wxRichTextParagraph* GetParagraphAtPosition(long pos, bool caretPosition = false) const;

    /// Get the line size at the given position
    virtual wxSize GetLineSizeAtPosition(long pos, bool caretPosition = false) const;

    /// Given a position, get the number of the visible line (potentially many to a paragraph),
    /// starting from zero at the start of the buffer. We also have to pass a bool (startOfLine)
    /// that indicates whether the caret is being shown at the end of the previous line or at the start
    /// of the next, since the caret can be shown at 2 visible positions for the same underlying
    /// position.
    virtual long GetVisibleLineNumber(long pos, bool caretPosition = false, bool startOfLine = false) const;

    /// Given a line number, get the corresponding wxRichTextLine object.
    virtual wxRichTextLine* GetLineForVisibleLineNumber(long lineNumber) const;

    /// Get the leaf object in a paragraph at this position.
    /// Given a line number, get the corresponding wxRichTextLine object.
    virtual wxRichTextObject* GetLeafObjectAtPosition(long position) const;

    /// Get the paragraph by number
    virtual wxRichTextParagraph* GetParagraphAtLine(long paragraphNumber) const;

    /// Get the paragraph for a given line
    virtual wxRichTextParagraph* GetParagraphForLine(wxRichTextLine* line) const;

    /// Get the length of the paragraph
    virtual int GetParagraphLength(long paragraphNumber) const;

    /// Get the number of paragraphs
    virtual int GetParagraphCount() const { return static_cast<int>(GetChildCount()); }

    /// Get the number of visible lines
    virtual int GetLineCount() const;

    /// Get the text of the paragraph
    virtual wxString GetParagraphText(long paragraphNumber) const;

    /// Convert zero-based line column and paragraph number to a position.
    virtual long XYToPosition(long x, long y) const;

    /// Convert zero-based position to line column and paragraph number
    virtual bool PositionToXY(long pos, long* x, long* y) const;

    /// Set text attributes: character and/or paragraph styles.
    virtual bool SetStyle(const wxRichTextRange& range, const wxRichTextAttr& style, int flags = wxRICHTEXT_SETSTYLE_WITH_UNDO);

    /// Get the conbined text attributes for this position.
    virtual bool GetStyle(long position, wxRichTextAttr& style);

    /// Get the content (uncombined) attributes for this position.
    virtual bool GetUncombinedStyle(long position, wxRichTextAttr& style);

    /// Implementation helper for GetStyle. If combineStyles is true, combine base, paragraph and
    /// context attributes.
    virtual bool DoGetStyle(long position, wxRichTextAttr& style, bool combineStyles = true);

    /// Get the combined style for a range - if any attribute is different within the range,
    /// that attribute is not present within the flags
    virtual bool GetStyleForRange(const wxRichTextRange& range, wxRichTextAttr& style);

    /// Combines 'style' with 'currentStyle' for the purpose of summarising the attributes of a range of
    /// content.
    bool CollectStyle(wxRichTextAttr& currentStyle, const wxRichTextAttr& style, wxRichTextAttr& clashingAttr, wxRichTextAttr& absentAttr);

    /// Set list style
    virtual bool SetListStyle(const wxRichTextRange& range, wxRichTextListStyleDefinition* def, int flags = wxRICHTEXT_SETSTYLE_WITH_UNDO, int startFrom = 1, int specifiedLevel = -1);
    virtual bool SetListStyle(const wxRichTextRange& range, const wxString& defName, int flags = wxRICHTEXT_SETSTYLE_WITH_UNDO, int startFrom = 1, int specifiedLevel = -1);

    /// Clear list for given range
    virtual bool ClearListStyle(const wxRichTextRange& range, int flags = wxRICHTEXT_SETSTYLE_WITH_UNDO);

    /// Number/renumber any list elements in the given range.
    /// def/defName can be NULL/empty to indicate that the existing list style should be used.
    virtual bool NumberList(const wxRichTextRange& range, wxRichTextListStyleDefinition* def = NULL, int flags = wxRICHTEXT_SETSTYLE_WITH_UNDO, int startFrom = 1, int specifiedLevel = -1);
    virtual bool NumberList(const wxRichTextRange& range, const wxString& defName, int flags = wxRICHTEXT_SETSTYLE_WITH_UNDO, int startFrom = 1, int specifiedLevel = -1);

    /// Promote the list items within the given range. promoteBy can be a positive or negative number, e.g. 1 or -1
    /// def/defName can be NULL/empty to indicate that the existing list style should be used.
    virtual bool PromoteList(int promoteBy, const wxRichTextRange& range, wxRichTextListStyleDefinition* def = NULL, int flags = wxRICHTEXT_SETSTYLE_WITH_UNDO, int specifiedLevel = -1);
    virtual bool PromoteList(int promoteBy, const wxRichTextRange& range, const wxString& defName, int flags = wxRICHTEXT_SETSTYLE_WITH_UNDO, int specifiedLevel = -1);

    /// Helper for NumberList and PromoteList, that does renumbering and promotion simultaneously
    /// def/defName can be NULL/empty to indicate that the existing list style should be used.
    virtual bool DoNumberList(const wxRichTextRange& range, const wxRichTextRange& promotionRange, int promoteBy, wxRichTextListStyleDefinition* def, int flags = wxRICHTEXT_SETSTYLE_WITH_UNDO, int startFrom = 1, int specifiedLevel = -1);

    /// Fills in the attributes for numbering a paragraph after previousParagraph.
    virtual bool FindNextParagraphNumber(wxRichTextParagraph* previousParagraph, wxRichTextAttr& attr) const;

    /// Test if this whole range has character attributes of the specified kind. If any
    /// of the attributes are different within the range, the test fails. You
    /// can use this to implement, for example, bold button updating. style must have
    /// flags indicating which attributes are of interest.
    virtual bool HasCharacterAttributes(const wxRichTextRange& range, const wxRichTextAttr& style) const;

    /// Test if this whole range has paragraph attributes of the specified kind. If any
    /// of the attributes are different within the range, the test fails. You
    /// can use this to implement, for example, centering button updating. style must have
    /// flags indicating which attributes are of interest.
    virtual bool HasParagraphAttributes(const wxRichTextRange& range, const wxRichTextAttr& style) const;

    /// Clone
    virtual wxRichTextObject* Clone() const { return new wxRichTextParagraphLayoutBox(*this); }

    /// Insert fragment into this box at the given position. If partialParagraph is true,
    /// it is assumed that the last (or only) paragraph is just a piece of data with no paragraph
    /// marker.
    virtual bool InsertFragment(long position, wxRichTextParagraphLayoutBox& fragment);

    /// Make a copy of the fragment corresponding to the given range, putting it in 'fragment'.
    virtual bool CopyFragment(const wxRichTextRange& range, wxRichTextParagraphLayoutBox& fragment);

    /// Apply the style sheet to the buffer, for example if the styles have changed.
    virtual bool ApplyStyleSheet(wxRichTextStyleSheet* styleSheet);

    /// Copy
    void Copy(const wxRichTextParagraphLayoutBox& obj);

    /// Assignment
    void operator= (const wxRichTextParagraphLayoutBox& obj) { Copy(obj); }

    /// Calculate ranges
    virtual void UpdateRanges() { long end; CalculateRange(0, end); }

    /// Get all the text
    virtual wxString GetText() const;

    /// Set default style for new content. Setting it to a default attribute
    /// makes new content take on the 'basic' style.
    virtual bool SetDefaultStyle(const wxRichTextAttr& style);

    /// Get default style
    virtual const wxRichTextAttr& GetDefaultStyle() const { return m_defaultAttributes; }

    /// Set basic (overall) style
    virtual void SetBasicStyle(const wxRichTextAttr& style) { m_attributes = style; }

    /// Get basic (overall) style
    virtual const wxRichTextAttr& GetBasicStyle() const { return m_attributes; }

    /// Invalidate the buffer. With no argument, invalidates whole buffer.
    void Invalidate(const wxRichTextRange& invalidRange = wxRICHTEXT_ALL);

    /// Gather information about floating objects. If untilObj is non-NULL,
    /// will stop getting information if the current object is this, since we
    /// will collect the rest later.
    virtual bool UpdateFloatingObjects(const wxRect& availableRect, wxRichTextObject* untilObj = NULL);

    /// Get invalid range, rounding to entire paragraphs if argument is true.
    wxRichTextRange GetInvalidRange(bool wholeParagraphs = false) const;

    /// Get the wxRichTextFloatCollector of this object
    wxRichTextFloatCollector* GetFloatCollector() { return m_floatCollector; }

};



class  wxRichTextBox: public wxRichTextCompositeObject
{
public:
// Constructors

    wxRichTextBox(wxRichTextObject* parent = NULL);
    wxRichTextBox(const wxRichTextBox& obj);

// Accessors

// Operations

    /// Clone
    virtual wxRichTextObject* Clone() const { return new wxRichTextBox(*this); }

    /// Copy
    void Copy(const wxRichTextBox& obj);

};







DocStr(wxRichTextLine,
       "This object represents a line in a paragraph, and stores offsets from
the start of the paragraph representing the start and end positions of
the line.", "");

class wxRichTextLine
{
public:
    wxRichTextLine(wxRichTextParagraph* parent);
    virtual ~wxRichTextLine();

    /// Set the range
    void SetRange(const wxRichTextRange& range);

    /// Get the parent paragraph
    wxRichTextParagraph* GetParent();

    /// Get the range
    wxRichTextRange GetRange();

    /// Get the absolute range
    wxRichTextRange GetAbsoluteRange() const;

    /// Get/set the line size as calculated by Layout.
    virtual wxSize GetSize() const;
    virtual void SetSize(const wxSize& sz);

    /// Get/set the object position relative to the parent
    virtual wxPoint GetPosition() const;
    virtual void SetPosition(const wxPoint& pos);

    /// Get the absolute object position
    virtual wxPoint GetAbsolutePosition() const;

    /// Get the rectangle enclosing the line
    virtual wxRect GetRect() const;

    /// Set/get stored descent
    void SetDescent(int descent);
    int GetDescent() const;


// Operations

    /// Initialisation
    void Init(wxRichTextParagraph* parent);

    /// Copy
    void Copy(const wxRichTextLine& obj);

    /// Clone
    virtual wxRichTextLine* Clone() const;
};






DocStr(wxRichTextParagraph,
       "This object represents a single paragraph (or in a straight text
editor, a line).", "");

class wxRichTextParagraph: public wxRichTextBox
{
public:
    wxRichTextParagraph(const wxString& text, wxRichTextObject* parent = NULL,
                        wxRichTextAttr* paraStyle = NULL, wxRichTextAttr* charStyle = NULL);

    virtual ~wxRichTextParagraph();


// Accessors

    /// Get the cached lines
    wxRichTextLineList& GetLines();

// Operations

    /// Copy
    void Copy(const wxRichTextParagraph& obj);

    /// Clone
    virtual wxRichTextObject* Clone() const;

    /// Clear the cached lines
    void ClearLines();

// Implementation

    /// Apply paragraph styles such as centering to the wrapped lines
    virtual void ApplyParagraphStyle(wxRichTextLine* line, const wxRichTextAttr& attr, const wxRect& rect, wxDC& dc);

    /// Insert text at the given position
    virtual bool InsertText(long pos, const wxString& text);

    /// Split an object at this position if necessary, and return
    /// the previous object, or NULL if inserting at beginning.
    virtual wxRichTextObject* SplitAt(long pos, wxRichTextObject** previousObject = NULL);

    /// Move content to a list from this point
    virtual void MoveToList(wxRichTextObject* obj, wxList& list);

    /// Add content back from list
    virtual void MoveFromList(wxList& list);

    /// Get the plain text searching from the start or end of the range.
    /// The resulting string may be shorter than the range given.
    bool GetContiguousPlainText(wxString& text, const wxRichTextRange& range, bool fromStart = true);

    /// Find a suitable wrap position. wrapPosition is the last position in the line to the left
    /// of the split.
    bool FindWrapPosition(const wxRichTextRange& range, wxDC& dc,
                          wxRichTextDrawingContext& context,
                          int availableSpace, long& wrapPosition,
                          wxArrayInt* partialExtents);

    /// Find the object at the given position
    wxRichTextObject* FindObjectAtPosition(long position);

    /// Get the bullet text for this paragraph.
    wxString GetBulletText();

    /// Allocate or reuse a line object
    wxRichTextLine* AllocateLine(int pos);

    /// Clear remaining unused line objects, if any
    bool ClearUnusedLines(int lineCount);

    /// Get combined attributes of the base style, paragraph style and
    /// character style. We use this to dynamically retrieve the actual style.
    %extend {
        wxRichTextAttr GetCombinedAttributes(wxRichTextAttr* contentStyle=NULL)
        {
            if (contentStyle)
                return self->GetCombinedAttributes(*contentStyle);
            else
                return self->GetCombinedAttributes();
        }
    }
    

    /// Get the first position from pos that has a line break character.
    long GetFirstLineBreakPosition(long pos);

    /// Create default tabstop array
    static void InitDefaultTabs();

    /// Clear default tabstop array
    static void ClearDefaultTabs();

    /// Get default tabstop array
    static const wxArrayInt& GetDefaultTabs() { return sm_defaultTabs; }
};







DocStr(wxRichTextPlainText,
       "This object represents a single piece of text.", "");

class wxRichTextPlainText: public wxRichTextObject
{
public:
    wxRichTextPlainText(const wxString& text = wxEmptyString,
                        wxRichTextObject* parent = NULL,
                        wxRichTextAttr* style = NULL);

    /// Get the first position from pos that has a line break character.
    long GetFirstLineBreakPosition(long pos);

    /// Get the text
    const wxString& GetText() const;

    /// Set the text
    void SetText(const wxString& text);

// Operations

    /// Copy
    void Copy(const wxRichTextPlainText& obj);

    /// Clone
    virtual wxRichTextObject* Clone() const;

};






#if 0
// TODO: we may not even need wrappers for this class.  It looks to me
// like wxRichTextImage might be enough...
DocStr(wxRichTextImageBlock,
       "Stores information about an image, in binary in-memory form.", "");

class wxRichTextImageBlock: public wxObject
{
public:
    wxRichTextImageBlock();
    virtual ~wxRichTextImageBlock();

    void Init();
    void Clear();

    // Load the original image into a memory block.
    // If the image is not a JPEG, we must convert it into a JPEG
    // to conserve space.
    // If it's not a JPEG we can make use of 'image', already scaled, so we don't have to
    // load the image a 2nd time.
    virtual bool MakeImageBlock(const wxString& filename, wxBitmapType imageType, wxImage& image, bool convertToJPEG = true);

    // Make an image block from the wxImage in the given
    // format.
    virtual bool MakeImageBlock(wxImage& image, wxBitmapType imageType, int quality = 80);

    // Write to a file
    bool Write(const wxString& filename);

    // Write data in hex to a stream
    bool WriteHex(wxOutputStream& stream);

    // Read data in hex from a stream
    bool ReadHex(wxInputStream& stream, int length, wxBitmapType imageType);

    // Copy from 'block'
    void Copy(const wxRichTextImageBlock& block);

    // Load a wxImage from the block
    bool Load(wxImage& image);


//// Accessors

    unsigned char* GetData() const;
    size_t GetDataSize() const;
    wxBitmapType GetImageType() const;

    void SetData(unsigned char* image);
    void SetDataSize(size_t size);
    void SetImageType(wxBitmapType imageType);

    bool IsOk() const;

    // Gets the extension for the block's type
    wxString GetExtension() const;

/// Implementation

    // Allocate and read from stream as a block of memory
    static unsigned char* ReadBlock(wxInputStream& stream, size_t size);
    static unsigned char* ReadBlock(const wxString& filename, size_t size);

    // Write memory block to stream
    static bool WriteBlock(wxOutputStream& stream, unsigned char* block, size_t size);

    // Write memory block to file
    static bool WriteBlock(const wxString& filename, unsigned char* block, size_t size);
};
#endif






DocStr(wxRichTextImage,
       "This object represents an image.", "");

class wxRichTextImage: public wxRichTextObject
{
public:
    %nokwargs wxRichTextImage;
    wxRichTextImage(wxRichTextObject* parent = NULL): wxRichTextObject(parent) { }
    wxRichTextImage(const wxImage& image, wxRichTextObject* parent = NULL, wxRichTextAttr* charStyle = NULL);
    wxRichTextImage(const wxRichTextImageBlock& imageBlock, wxRichTextObject* parent = NULL, wxRichTextAttr* charStyle = NULL);
    wxRichTextImage(const wxRichTextImage& obj): wxRichTextObject(obj) { Copy(obj); }

// Overrideables

    /// Returns true if the object is empty. An image is never empty; if the image is broken, that's not the same thing as empty.
    virtual bool IsEmpty() const { return false; /* !m_imageBlock.Ok(); */ }

    /// Can we edit properties via a GUI?
    virtual bool CanEditProperties() const { return true; }

    /// Edit properties via a GUI
    virtual bool EditProperties(wxWindow* parent, wxRichTextBuffer* buffer);

    /// Does this object take note of paragraph attributes? Text and image objects don't.
    virtual bool UsesParagraphAttributes() const { return false; }

    /// Export this object directly to the given stream.
    virtual bool ExportXML(wxOutputStream& stream, int indent, wxRichTextXMLHandler* handler);

    /// Export this object to the given parent node, usually creating at least one child node.
    virtual bool ExportXML(wxXmlNode* parent, wxRichTextXMLHandler* handler);

    // Images can be floatable (optionally).
    virtual bool IsFloatable() const { return true; }

    /// What is the XML node name of this object?
    virtual wxString GetXMLNodeName() const { return wxT("image"); }

// Accessors

    /// Get the image cache (scaled bitmap)
    const wxBitmap& GetImageCache() const { return m_imageCache; }

    /// Set the image cache
    void SetImageCache(const wxBitmap& bitmap) { m_imageCache = bitmap; }

    /// Reset the image cache
    void ResetImageCache() { m_imageCache = wxNullBitmap; }

    /// Get the image block containing the raw data
    wxRichTextImageBlock& GetImageBlock() { return m_imageBlock; }

// Operations

    /// Copy
    void Copy(const wxRichTextImage& obj);

    /// Clone
    virtual wxRichTextObject* Clone() const { return new wxRichTextImage(*this); }

    /// Create a cached image at the required size
    virtual bool LoadImageCache(wxDC& dc, bool resetCache = false);
};






%typemap(out) wxRichTextFileHandler*  { $result = wxPyMake_wxObject($1, (bool)$owner); }
wxUNTYPED_LIST_WRAPPER(wxRichTextFileHandlerList, wxRichTextFileHandler);

DocStr(wxRichTextBuffer,
       "This is a kind of box, used to represent the whole buffer.", "");

class wxRichTextCommand;
class wxRichTextAction;

class wxRichTextBuffer: public wxRichTextParagraphLayoutBox
{
public:
    wxRichTextBuffer();
    virtual ~wxRichTextBuffer() ;

// Accessors

    /// Gets the command processor
    wxCommandProcessor* GetCommandProcessor() const;

    /// Set style sheet, if any.
    void SetStyleSheet(wxRichTextStyleSheet* styleSheet);
    virtual wxRichTextStyleSheet* GetStyleSheet() const;

    /// Set style sheet and notify of the change
    bool SetStyleSheetAndNotify(wxRichTextStyleSheet* sheet);

    /// Push style sheet to top of stack
    bool PushStyleSheet(wxRichTextStyleSheet* styleSheet);

    /// Pop style sheet from top of stack
    wxRichTextStyleSheet* PopStyleSheet();

    /// Set/get table storing fonts
    wxRichTextFontTable& GetFontTable();
    void SetFontTable(const wxRichTextFontTable& table);
    
    
// Operations

    /// Initialisation
    void Init();

    /// Clears the buffer, adds an empty paragraph, and clears the command processor.
    virtual void ResetAndClearCommands();

    /// Load a file
    virtual bool LoadFile(const wxString& filename, wxRichTextFileType type = wxRICHTEXT_TYPE_ANY);

    /// Save a file
    virtual bool SaveFile(const wxString& filename, wxRichTextFileType type = wxRICHTEXT_TYPE_ANY);

    /// Load from a stream
    %Rename(LoadStream,
            virtual bool , LoadFile(wxInputStream& stream, wxRichTextFileType type = wxRICHTEXT_TYPE_ANY));

    /// Save to a stream
    %Rename(SaveStream,
            virtual bool , SaveFile(wxOutputStream& stream, wxRichTextFileType type = wxRICHTEXT_TYPE_ANY));

    /// Set the handler flags, controlling loading and saving
    void SetHandlerFlags(int flags) { m_handlerFlags = flags; }

    /// Get the handler flags, controlling loading and saving
    int GetHandlerFlags() const { return m_handlerFlags; }

    /// Convenience function to add a paragraph of text
    virtual wxRichTextRange AddParagraph(const wxString& text,
                                         wxRichTextAttr* paraStyle = NULL);

    /// Begin collapsing undo/redo commands. Note that this may not work properly
    /// if combining commands that delete or insert content, changing ranges for
    /// subsequent actions.
    virtual bool BeginBatchUndo(const wxString& cmdName);

    /// End collapsing undo/redo commands
    virtual bool EndBatchUndo();

    /// Collapsing commands?
    virtual bool BatchingUndo() const;

    /// Submit immediately, or delay according to whether collapsing is on
    virtual bool SubmitAction(wxRichTextAction* action);

    /// Get collapsed command
    virtual wxRichTextCommand* GetBatchedCommand() const;

    /// Begin suppressing undo/redo commands. The way undo is suppressed may be implemented
    /// differently by each command. If not dealt with by a command implementation, then
    /// it will be implemented automatically by not storing the command in the undo history
    /// when the action is submitted to the command processor.
    virtual bool BeginSuppressUndo();

    /// End suppressing undo/redo commands.
    virtual bool EndSuppressUndo();

    /// Collapsing commands?
    virtual bool SuppressingUndo() const;

    /// Copy the range to the clipboard
    virtual bool CopyToClipboard(const wxRichTextRange& range);

    /// Paste the clipboard content to the buffer
    virtual bool PasteFromClipboard(long position);

    /// Can we paste from the clipboard?
    virtual bool CanPasteFromClipboard() const;

    /// Begin using a style
    virtual bool BeginStyle(const wxRichTextAttr& style);

    /// End the style
    virtual bool EndStyle();

    /// End all styles
    virtual bool EndAllStyles();

    /// Clear the style stack
    virtual void ClearStyleStack();

    /// Get the size of the style stack, for example to check correct nesting
    virtual size_t GetStyleStackSize() const;

    /// Begin using bold
    bool BeginBold();

    /// End using bold
    bool EndBold();

    /// Begin using italic
    bool BeginItalic();

    /// End using italic
    bool EndItalic();

    /// Begin using underline
    bool BeginUnderline();

    /// End using underline
    bool EndUnderline();

    /// Begin using point size
    bool BeginFontSize(int pointSize);

    /// End using point size
    bool EndFontSize();

    /// Begin using this font
    bool BeginFont(const wxFont& font);

    /// End using a font
    bool EndFont();

    /// Begin using this colour
    bool BeginTextColour(const wxColour& colour);

    /// End using a colour
    bool EndTextColour();

    /// Begin using alignment
    bool BeginAlignment(wxTextAttrAlignment alignment);

    /// End alignment
    bool EndAlignment();

    /// Begin left indent
    bool BeginLeftIndent(int leftIndent, int leftSubIndent = 0);

    /// End left indent
    bool EndLeftIndent();

    /// Begin right indent
    bool BeginRightIndent(int rightIndent);

    /// End right indent
    bool EndRightIndent();

    /// Begin paragraph spacing
    bool BeginParagraphSpacing(int before, int after);

    /// End paragraph spacing
    bool EndParagraphSpacing();

    /// Begin line spacing
    bool BeginLineSpacing(int lineSpacing);

    /// End line spacing
    bool EndLineSpacing();

    /// Begin numbered bullet
    bool BeginNumberedBullet(int bulletNumber, int leftIndent, int leftSubIndent, int bulletStyle = wxTEXT_ATTR_BULLET_STYLE_ARABIC|wxTEXT_ATTR_BULLET_STYLE_PERIOD);

    /// End numbered bullet
    bool EndNumberedBullet();

    /// Begin symbol bullet
    bool BeginSymbolBullet(const wxString& symbol, int leftIndent, int leftSubIndent, int bulletStyle = wxTEXT_ATTR_BULLET_STYLE_SYMBOL);

    /// End symbol bullet
    bool EndSymbolBullet();

    /// Begin standard bullet
    bool BeginStandardBullet(const wxString& bulletName, int leftIndent, int leftSubIndent, int bulletStyle = wxTEXT_ATTR_BULLET_STYLE_STANDARD);

    /// End standard bullet
    bool EndStandardBullet();

    /// Begin named character style
    bool BeginCharacterStyle(const wxString& characterStyle);

    /// End named character style
    bool EndCharacterStyle();

    /// Begin named paragraph style
    bool BeginParagraphStyle(const wxString& paragraphStyle);

    /// End named character style
    bool EndParagraphStyle();

    /// Begin named list style
    bool BeginListStyle(const wxString& listStyle, int level = 1, int number = 1);

    /// End named character style
    bool EndListStyle();

    /// Begin URL
    bool BeginURL(const wxString& url, const wxString& characterStyle = wxEmptyString);

    /// End URL
    bool EndURL();

// Event handling

    /// Add an event handler
    bool AddEventHandler(wxEvtHandler* handler);

    /// Remove an event handler
    bool RemoveEventHandler(wxEvtHandler* handler, bool deleteHandler = false);

    /// Clear event handlers
    void ClearEventHandlers();

    /// Send event to event handlers. If sendToAll is true, will send to all event handlers,
    /// otherwise will stop at the first successful one.
    bool SendEvent(wxEvent& event, bool sendToAll = true);

// Implementation

    /// Copy
    void Copy(const wxRichTextBuffer& obj);

    /// Clone
    virtual wxRichTextObject* Clone() const;

    /// Submit command to insert paragraphs
    bool InsertParagraphsWithUndo(long pos, const wxRichTextParagraphLayoutBox& paragraphs, wxRichTextCtrl* ctrl, int flags = 0);

    /// Submit command to insert the given text
    bool InsertTextWithUndo(long pos, const wxString& text, wxRichTextCtrl* ctrl, int flags = 0);

    /// Submit command to insert a newline
    bool InsertNewlineWithUndo(long pos, wxRichTextCtrl* ctrl, int flags = 0);

    /// Submit command to insert the given image
    bool InsertImageWithUndo(long pos, const wxRichTextImageBlock& imageBlock, wxRichTextCtrl* ctrl, int flags = 0);

    /// Submit command to delete this range
    bool DeleteRangeWithUndo(const wxRichTextRange& range, wxRichTextCtrl* ctrl);

    /// Mark modified
    void Modify(bool modify = true);
    bool IsModified() const;

    /// Get the style that is appropriate for a new paragraph at this position.
    /// If the previous paragraph has a paragraph style name, look up the next-paragraph
    /// style.
    wxRichTextAttr GetStyleForNewParagraph(wxRichTextBuffer* buffer,
                                           long pos,
                                           bool caretPosition = false,
                                           bool lookUpNewParaStyle=false) const;


    /// Returns the file handlers
    static wxRichTextFileHandlerList_t& GetHandlers();

    %disownarg(wxRichTextFileHandler *handler);
    
    /// Adds a handler to the end
    static void AddHandler(wxRichTextFileHandler *handler);

    /// Inserts a handler at the front
    static void InsertHandler(wxRichTextFileHandler *handler);

    %cleardisown(wxRichTextFileHandler *handler);
    
    
    /// Removes a handler
    static bool RemoveHandler(const wxString& name);

    /// Finds a handler by name
    %Rename(FindHandlerByName,
            static wxRichTextFileHandler* , FindHandler(const wxString& name));

    /// Finds a handler by extension and type
    %Rename(FindHandlerByExtension,
            static wxRichTextFileHandler*, FindHandler(const wxString& extension,
                                                       wxRichTextFileType imageType));

    /// Finds a handler by filename or, if supplied, type
    %Rename(FindHandlerByFilename,
            static wxRichTextFileHandler* , FindHandlerFilenameOrType(const wxString& filename,
                                                                      wxRichTextFileType imageType));

    /// Finds a handler by type
    %Rename(FindHandlerByType,
            static wxRichTextFileHandler* , FindHandler(wxRichTextFileType imageType));


    // TODO: Handle returning the types array?
    
    /// Gets a wildcard incorporating all visible handlers. If 'types' is present,
    /// will be filled with the file type corresponding to each filter. This can be
    /// used to determine the type to pass to LoadFile given a selected filter.
    //static wxString GetExtWildcard(bool combine = false, bool save = false,
    //                               wxArrayInt* types = NULL);
    %extend {
        KeepGIL(GetExtWildcard);
        DocAStr(GetExtWildcard,
                "GetExtWildcard(self, bool combine=False, bool save=False) --> (wildcards, types)",
                "Gets a wildcard string for the file dialog based on all the currently
loaded richtext file handlers, and a list that can be used to map
those filter types to the file handler type.", "");
        static PyObject* GetExtWildcard(bool combine = false, bool save = false) {
            wxString wildcards;
            wxArrayInt types;
            wildcards = wxRichTextBuffer::GetExtWildcard(combine, save, &types);
            PyObject* tup = PyTuple_New(2);
            PyTuple_SET_ITEM(tup, 0, wx2PyString(wildcards));
            PyTuple_SET_ITEM(tup, 1, wxArrayInt2PyList_helper(types));
            return tup;
        }
    }

    /// Clean up handlers
    static void CleanUpHandlers();

    /// Initialise the standard handlers
    static void InitStandardHandlers();

    /// Get renderer
    static wxRichTextRenderer* GetRenderer();

    /// Set renderer, deleting old one
    static void SetRenderer(wxRichTextRenderer* renderer);

    /// Minimum margin between bullet and paragraph in 10ths of a mm
    static int GetBulletRightMargin();
    static void SetBulletRightMargin(int margin);

    /// Factor to multiply by character height to get a reasonable bullet size
    static float GetBulletProportion();
    static void SetBulletProportion(float prop);

    /// Scale factor for calculating dimensions
    double GetScale() const;
    void SetScale(double scale);

    /**
        Returns the floating layout mode. The default is @true, where objects
        are laid out according to their floating status.
    */
    static bool GetFloatingLayoutMode();

    /**
        Sets the floating layout mode. Pass @false to speed up editing by not performing
        floating layout. This setting affects all buffers.

    */
    static void SetFloatingLayoutMode(bool mode);

};






// TODO:  Do we need wrappers for the command processor, undo/redo, etc.?
//
// enum wxRichTextCommandId
// {
//     wxRICHTEXT_INSERT,
//     wxRICHTEXT_DELETE,
//     wxRICHTEXT_CHANGE_STYLE
// };
// class WXDLLIMPEXP_RICHTEXT wxRichTextCommand: public wxCommand
// class WXDLLIMPEXP_RICHTEXT wxRichTextAction: public wxObject




//---------------------------------------------------------------------------
%newgroup


/*!
 * Handler flags
 */

enum {
    // Include style sheet when loading and saving
    wxRICHTEXT_HANDLER_INCLUDE_STYLESHEET,

    // Save images to memory file system in HTML handler
    wxRICHTEXT_HANDLER_SAVE_IMAGES_TO_MEMORY,

    // Save images to files in HTML handler
    wxRICHTEXT_HANDLER_SAVE_IMAGES_TO_FILES,

    // Save images as inline base64 data in HTML handler
    wxRICHTEXT_HANDLER_SAVE_IMAGES_TO_BASE64,

    // Don't write header and footer (or BODY), so we can include the
    // fragment in a larger document
    wxRICHTEXT_HANDLER_NO_HEADER_FOOTER,

    // Convert the more common face names to names that will work on the
    // current platform in a larger document
    wxRICHTEXT_HANDLER_CONVERT_FACENAMES,    
};




DocStr(wxRichTextFileHandler,
       "Base class for file handlers", "");

class wxRichTextFileHandler: public wxObject
{
public:
    //wxRichTextFileHandler(const wxString& name = wxEmptyString,   ****  This is an ABC
    //                      const wxString& ext = wxEmptyString,
    //                      int type = 0);

    ~wxRichTextFileHandler();
    
    %Rename(LoadStream,
            bool, LoadFile(wxRichTextBuffer *buffer, wxInputStream& stream));
    %Rename(SaveStream,
            bool,  SaveFile(wxRichTextBuffer *buffer, wxOutputStream& stream));
    
    bool LoadFile(wxRichTextBuffer *buffer, const wxString& filename);
    bool SaveFile(wxRichTextBuffer *buffer, const wxString& filename);

    /// Can we handle this filename (if using files)? By default, checks the extension.
    virtual bool CanHandle(const wxString& filename) const;

    /// Can we save using this handler?
    virtual bool CanSave() const;

    /// Can we load using this handler?
    virtual bool CanLoad() const;

    /// Should this handler be visible to the user?
    virtual bool IsVisible() const;
    virtual void SetVisible(bool visible);

    /// The name of the nandler
    void SetName(const wxString& name);
    wxString GetName() const;
    %property(Name, GetName, SetName)
    
    /// The default extension to recognise
    void SetExtension(const wxString& ext);
    wxString GetExtension() const;
    %property(Extension, GetExtension, SetExtension)

    /// The handler type
    void SetType(int type);
    int GetType() const;
    %property(Type, GetType, SetType)

    /// Flags controlling how loading and saving is done
    void SetFlags(int flags);
    int GetFlags() const;
    %property(Flags, GetFlags, SetFlags)

    /// Encoding to use when saving a file. If empty, a suitable encoding is chosen
    void SetEncoding(const wxString& encoding);
    const wxString& GetEncoding() const;
    %property(Encoding, GetEncoding, SetEncoding)   
};



MAKE_CONST_WXSTRING2(TextName, wxT("Text"));
MAKE_CONST_WXSTRING2(TextExt,  wxT("txt"));

class wxRichTextPlainTextHandler: public wxRichTextFileHandler
{
public:
    wxRichTextPlainTextHandler(const wxString& name = wxPyTextName,
                               const wxString& ext =  wxPyTextExt,
                               wxRichTextFileType type = wxRICHTEXT_TYPE_TEXT);
};





//---------------------------------------------------------------------------
%newgroup


// TODO: Make a PyRichTextRenderer class


/*!
 * wxRichTextRenderer isolates common drawing functionality
 */

class wxRichTextRenderer: public wxObject
{
public:
    wxRichTextRenderer() {}
    virtual ~wxRichTextRenderer() {}

    /// Draw a standard bullet, as specified by the value of GetBulletName
    virtual bool DrawStandardBullet(wxRichTextParagraph* paragraph,
                                    wxDC& dc,
                                    const wxRichTextAttr& attr,
                                    const wxRect& rect) = 0;

    /// Draw a bullet that can be described by text, such as numbered or symbol bullets
    virtual bool DrawTextBullet(wxRichTextParagraph* paragraph,
                                wxDC& dc, const wxRichTextAttr& attr,
                                const wxRect& rect,
                                const wxString& text) = 0;

    /// Draw a bitmap bullet, where the bullet bitmap is specified by the value of GetBulletName
    virtual bool DrawBitmapBullet(wxRichTextParagraph* paragraph,
                                  wxDC& dc,
                                  const wxRichTextAttr& attr,
                                  const wxRect& rect) = 0;

    /// Enumerate the standard bullet names currently supported
    virtual bool EnumerateStandardBulletNames(wxArrayString& bulletNames) = 0;
};

/*!
 * wxRichTextStdRenderer: standard renderer
 */

class wxRichTextStdRenderer: public wxRichTextRenderer
{
public:
    wxRichTextStdRenderer() {}

    /// Draw a standard bullet, as specified by the value of GetBulletName
    virtual bool DrawStandardBullet(wxRichTextParagraph* paragraph,
                                    wxDC& dc,
                                    const wxRichTextAttr& attr,
                                    const wxRect& rect);

    /// Draw a bullet that can be described by text, such as numbered or symbol bullets
    virtual bool DrawTextBullet(wxRichTextParagraph* paragraph,
                                wxDC& dc,
                                const wxRichTextAttr& attr,
                                const wxRect& rect,
                                const wxString& text);

    /// Draw a bitmap bullet, where the bullet bitmap is specified by the value of GetBulletName
    virtual bool DrawBitmapBullet(wxRichTextParagraph* paragraph,
                                  wxDC& dc,
                                  const wxRichTextAttr& attr,
                                  const wxRect& rect);

    /// Enumerate the standard bullet names currently supported
    virtual bool EnumerateStandardBulletNames(wxArrayString& bulletNames);
};

//---------------------------------------------------------------------------
//---------------------------------------------------------------------------
