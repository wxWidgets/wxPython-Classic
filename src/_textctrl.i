/////////////////////////////////////////////////////////////////////////////
// Name:        _textctrl.i
// Purpose:     SWIG interface defs for wxTextCtrl and related classes
//
// Author:      Robin Dunn
//
// Created:     10-June-1998
// RCS-ID:      $Id$
// Copyright:   (c) 2003 by Total Control Software
// Licence:     wxWindows license
/////////////////////////////////////////////////////////////////////////////

// Not a %module


//---------------------------------------------------------------------------

MAKE_CONST_WXSTRING(TextCtrlNameStr);

//---------------------------------------------------------------------------
%newgroup

enum {
    // Style flags
    wxTE_NO_VSCROLL,
    wxTE_AUTO_SCROLL,

    wxTE_READONLY,
    wxTE_MULTILINE,
    wxTE_PROCESS_TAB,

    // alignment flags
    wxTE_LEFT,
    wxTE_CENTER,
    wxTE_RIGHT,
    wxTE_CENTRE,

    // this style means to use RICHEDIT control and does something only under
    // wxMSW and Win32 and is silently ignored under all other platforms
    wxTE_RICH,

    wxTE_PROCESS_ENTER,
    wxTE_PASSWORD,

    // automatically detect the URLs and generate the events when mouse is
    // moved/clicked over an URL
    //
    // this is for Win32 richedit controls only so far
    wxTE_AUTO_URL,

    // by default, the Windows text control doesn't show the selection when it
    // doesn't have focus - use this style to force it to always show it
    wxTE_NOHIDESEL,

    // use wxHSCROLL (wxTE_DONTWRAP) to not wrap text at all, wxTE_CHARWRAP to
    // wrap it at any position and wxTE_WORDWRAP to wrap at words boundary
    //
    // if no wrapping style is given at all, the control wraps at word boundary
    wxTE_DONTWRAP,
    wxTE_CHARWRAP,
    wxTE_WORDWRAP,
    wxTE_BESTWRAP,

    // force using RichEdit version 2.0 or 3.0 instead of 1.0 (default) for
    // wxTE_RICH controls - can be used together with or instead of wxTE_RICH
    wxTE_RICH2,

    wxTE_CAPITALIZE,
};

%pythoncode { TE_LINEWRAP = TE_CHARWRAP }

// deprecated synonymns
%pythoncode {
PROCESS_ENTER = TE_PROCESS_ENTER
PASSWORD = TE_PASSWORD
}



enum wxTextAttrAlignment
{
    wxTEXT_ALIGNMENT_DEFAULT,
    wxTEXT_ALIGNMENT_LEFT,
    wxTEXT_ALIGNMENT_CENTRE,
    wxTEXT_ALIGNMENT_CENTER = wxTEXT_ALIGNMENT_CENTRE,
    wxTEXT_ALIGNMENT_RIGHT,
    wxTEXT_ALIGNMENT_JUSTIFIED
};

enum wxTextAttrFlags {
    // Flags to indicate which attributes are being applied
    wxTEXT_ATTR_TEXT_COLOUR,
    wxTEXT_ATTR_BACKGROUND_COLOUR,
    wxTEXT_ATTR_FONT_FACE,
    wxTEXT_ATTR_FONT_SIZE,
    wxTEXT_ATTR_FONT_WEIGHT,
    wxTEXT_ATTR_FONT_ITALIC,
    wxTEXT_ATTR_FONT_UNDERLINE,
    wxTEXT_ATTR_FONT_STRIKETHROUGH,
    wxTEXT_ATTR_FONT_ENCODING,
    wxTEXT_ATTR_FONT_FAMILY,

    wxTEXT_ATTR_FONT,
    wxTEXT_ATTR_ALIGNMENT,
    wxTEXT_ATTR_LEFT_INDENT,
    wxTEXT_ATTR_RIGHT_INDENT,
    wxTEXT_ATTR_TABS,

    wxTEXT_ATTR_PARA_SPACING_AFTER,
    wxTEXT_ATTR_LINE_SPACING,
    wxTEXT_ATTR_CHARACTER_STYLE_NAME,
    wxTEXT_ATTR_PARAGRAPH_STYLE_NAME,
    wxTEXT_ATTR_LIST_STYLE_NAME,
    wxTEXT_ATTR_BULLET_STYLE,
    wxTEXT_ATTR_BULLET_NUMBER,
    wxTEXT_ATTR_BULLET_TEXT,
    wxTEXT_ATTR_BULLET_NAME,
    wxTEXT_ATTR_BULLET,
    
    wxTEXT_ATTR_URL,
    wxTEXT_ATTR_PAGE_BREAK,
    wxTEXT_ATTR_EFFECTS,
    wxTEXT_ATTR_OUTLINE_LEVEL,

    wxTEXT_ATTR_CHARACTER,
    wxTEXT_ATTR_PARAGRAPH,
    wxTEXT_ATTR_ALL,
};


/*!
 * Styles for wxTextAttr::SetBulletStyle
 */
enum wxTextAttrBulletStyle {
    wxTEXT_ATTR_BULLET_STYLE_NONE,
    wxTEXT_ATTR_BULLET_STYLE_ARABIC,
    wxTEXT_ATTR_BULLET_STYLE_LETTERS_UPPER,
    wxTEXT_ATTR_BULLET_STYLE_LETTERS_LOWER,
    wxTEXT_ATTR_BULLET_STYLE_ROMAN_UPPER,
    wxTEXT_ATTR_BULLET_STYLE_ROMAN_LOWER,
    wxTEXT_ATTR_BULLET_STYLE_SYMBOL,
    wxTEXT_ATTR_BULLET_STYLE_BITMAP,
    wxTEXT_ATTR_BULLET_STYLE_PARENTHESES,
    wxTEXT_ATTR_BULLET_STYLE_PERIOD,
    wxTEXT_ATTR_BULLET_STYLE_STANDARD,
    wxTEXT_ATTR_BULLET_STYLE_RIGHT_PARENTHESIS,
    wxTEXT_ATTR_BULLET_STYLE_OUTLINE,

    wxTEXT_ATTR_BULLET_STYLE_ALIGN_LEFT,
    wxTEXT_ATTR_BULLET_STYLE_ALIGN_RIGHT,
    wxTEXT_ATTR_BULLET_STYLE_ALIGN_CENTRE,
};



/*!
 * Styles for wxTextAttr::SetTextEffects
 */
enum wxTextAttrEffects {
    wxTEXT_ATTR_EFFECT_NONE,
    wxTEXT_ATTR_EFFECT_CAPITALS,
    wxTEXT_ATTR_EFFECT_SMALL_CAPITALS,
    wxTEXT_ATTR_EFFECT_STRIKETHROUGH,
    wxTEXT_ATTR_EFFECT_DOUBLE_STRIKETHROUGH,
    wxTEXT_ATTR_EFFECT_SHADOW,
    wxTEXT_ATTR_EFFECT_EMBOSS,
    wxTEXT_ATTR_EFFECT_OUTLINE,
    wxTEXT_ATTR_EFFECT_ENGRAVE,
    wxTEXT_ATTR_EFFECT_SUPERSCRIPT,
    wxTEXT_ATTR_EFFECT_SUBSCRIPT,
};



/*!
 * Line spacing values
 */
enum wxTextAttrLineSpacing {
    wxTEXT_ATTR_LINE_SPACING_NORMAL,
    wxTEXT_ATTR_LINE_SPACING_HALF,
    wxTEXT_ATTR_LINE_SPACING_TWICE,
};


enum {
    wxOutOfRangeTextCoord,
    wxInvalidTextCoord,

    wxTEXT_TYPE_ANY
};

enum wxFontStyle;
enum wxFontWeight;
enum wxFontEncoding;
enum wxFontFamily;

//---------------------------------------------------------------------------

// wxTextAttr: a structure containing the visual attributes of a text
class wxTextAttr
{
public:
    wxTextAttr(const wxColour& colText = wxNullColour,
               const wxColour& colBack = wxNullColour,
               const wxFont& font = wxNullFont,
               wxTextAttrAlignment alignment = wxTEXT_ALIGNMENT_DEFAULT);
    ~wxTextAttr();

    // operations
    void Init();

    void Copy(const wxTextAttr& attr);

    // Partial equality test
    bool EqPartial(const wxTextAttr& attr) const;

    // Get attributes from font.
    bool GetFontAttributes(const wxFont& font, int flags = wxTEXT_ATTR_FONT);

    
    // setters
    void SetTextColour(const wxColour& colText);
    void SetBackgroundColour(const wxColour& colBack);
    void SetAlignment(wxTextAttrAlignment alignment);
    void SetTabs(const wxArrayInt& tabs);
    void SetLeftIndent(int indent, int subIndent=0);
    void SetRightIndent(int indent);

    void SetFontSize(int pointSize);
    void SetFontStyle(wxFontStyle fontStyle);
    void SetFontWeight(wxFontWeight fontWeight);
    void SetFontFaceName(const wxString& faceName);
    void SetFontUnderlined(bool underlined);
    void SetFontStrikethrough(bool strikethrough);
    void SetFontEncoding(wxFontEncoding encoding);
    void SetFontFamily(wxFontFamily family);
    void SetFont(const wxFont& font, int flags = wxTEXT_ATTR_FONT);
    
    void SetFlags(long flags);

    void SetCharacterStyleName(const wxString& name);
    void SetParagraphStyleName(const wxString& name);
    void SetListStyleName(const wxString& name);
    void SetParagraphSpacingAfter(int spacing);
    void SetParagraphSpacingBefore(int spacing);
    void SetLineSpacing(int spacing);
    void SetBulletStyle(int style);
    void SetBulletNumber(int n);
    void SetBulletText(const wxString& text);
    void SetBulletFont(const wxString& bulletFont);
    void SetBulletName(const wxString& name);
    void SetURL(const wxString& url);
    void SetPageBreak(bool pageBreak = true);
    void SetTextEffects(int effects);
    void SetTextEffectFlags(int effects);
    void SetOutlineLevel(int level);


    
//     // accessors
//     bool HasTextColour() const;
//     bool HasBackgroundColour() const;
//     bool HasFont() const;
//     bool HasAlignment() const;
//     bool HasTabs() const;
//     bool HasLeftIndent() const;
//     bool HasRightIndent() const;
//     bool HasFlag(long flag) const;

    
    const wxColour& GetTextColour() const;
    const wxColour& GetBackgroundColour() const;
    wxTextAttrAlignment GetAlignment() const;
    const wxArrayInt& GetTabs() const;
    long GetLeftIndent() const;
    long GetLeftSubIndent() const;
    long GetRightIndent() const;
    long GetFlags() const;

    int GetFontSize() const;
    int GetFontStyle() const;
    int GetFontWeight() const;
    bool GetFontUnderlined() const;
    bool GetFontStrikethrough() const;
    const wxString& GetFontFaceName() const;
    wxFontEncoding GetFontEncoding() const;
    wxFontFamily GetFontFamily() const;
    
    wxFont GetFont() const;
    %pythoncode { CreateFont = GetFont }
    
    const wxString& GetCharacterStyleName() const;
    const wxString& GetParagraphStyleName() const;
    const wxString& GetListStyleName() const;
    int GetParagraphSpacingAfter() const;
    int GetParagraphSpacingBefore() const;
    int GetLineSpacing() const;
    int GetBulletStyle() const;
    int GetBulletNumber() const;
    const wxString& GetBulletText() const;
    const wxString& GetBulletFont() const;
    const wxString& GetBulletName() const;
    const wxString& GetURL() const;
    int GetTextEffects() const;
    int GetTextEffectFlags() const;
    int GetOutlineLevel() const;

    // accessors
    bool HasTextColour() const;
    bool HasBackgroundColour() const;
    bool HasAlignment() const;
    bool HasTabs() const;
    bool HasLeftIndent() const;
    bool HasRightIndent() const;
    bool HasFontWeight() const;
    bool HasFontSize() const;
    bool HasFontItalic() const;
    bool HasFontUnderlined() const;
    bool HasFontStrikethrough() const;
    bool HasFontFaceName() const;
    bool HasFontEncoding() const;
    bool HasFontFamily() const;
    bool HasFont() const;

    bool HasParagraphSpacingAfter() const;
    bool HasParagraphSpacingBefore() const;
    bool HasLineSpacing() const;
    bool HasCharacterStyleName() const;
    bool HasParagraphStyleName() const;
    bool HasListStyleName() const;
    bool HasBulletStyle() const;
    bool HasBulletNumber() const;
    bool HasBulletText() const;
    bool HasBulletName() const;
    bool HasURL() const;
    bool HasPageBreak() const;
    bool HasTextEffects() const;
    bool HasTextEffect(int effect) const;
    bool HasOutlineLevel() const;

    bool HasFlag(long flag) const;
    void RemoveFlag(long flag);
    void AddFlag(long flag);

    // Is this a character style?
    bool IsCharacterStyle() const;
    bool IsParagraphStyle() const;

    
    // returns False if we have any attributes set, True otherwise
    bool IsDefault() const;

    // Merges the given attributes. Does not affect 'this'. If compareWith
    // is non-NULL, then it will be used to mask out those attributes that are the same in style
    // and compareWith, for situations where we don't want to explicitly set inherited attributes.
    bool Apply(const wxTextAttr& style, const wxTextAttr* compareWith = NULL);

//     // merges the attributes of the base and the overlay objects and returns
//     // the result; the parameter attributes take precedence
//     //
//     // WARNING: the order of arguments is the opposite of Combine()
//     static wxTextAttr Merge(const wxTextAttr& base, const wxTextAttr& overlay);

    // merges the attributes of this object and overlay
    void Merge(const wxTextAttr& overlay);
    
    // return the attribute having the valid font and colours: it uses the
    // attributes set in attr and falls back first to attrDefault and then to
    // the text control font/colours for those attributes which are not set
    static wxTextAttr Combine(const wxTextAttr& attr,
                              const wxTextAttr& attrDef,
                              const wxTextCtrl *text);

    // Compare tabs
    static bool TabsEq(const wxArrayInt& tabs1, const wxArrayInt& tabs2);

    // Remove attributes
    static bool RemoveStyle(wxTextAttr& destStyle, const wxTextAttr& style);

    // Combine two bitlists, specifying the bits of interest with separate flags.
    static bool CombineBitlists(int& valueA, int valueB, int& flagsA, int flagsB);

    // Compare two bitlists
    static bool BitlistsEqPartial(int valueA, int valueB, int flags);

    // Split into paragraph and character styles
    static bool SplitParaCharStyles(const wxTextAttr& style, wxTextAttr& parStyle, wxTextAttr& charStyle);
    
    
    %property(Alignment, GetAlignment, SetAlignment);
    %property(BackgroundColour, GetBackgroundColour, SetBackgroundColour);
    %property(Flags, GetFlags, SetFlags);
    %property(Font, GetFont, SetFont);
    %property(LeftIndent, GetLeftIndent, SetLeftIndent);
    %property(LeftSubIndent, GetLeftSubIndent);
    %property(RightIndent, GetRightIndent, SetRightIndent);
    %property(Tabs, GetTabs, SetTabs);
    %property(TextColour, GetTextColour, SetTextColour);
    %property(FontSize, GetFontSize, SetFontSize);
    %property(FontStyle, GetFontStyle, SetFontStyle);
    %property(FontWeight, GetFontWeight, SetFontWeight);
    %property(FontUnderlined, GetFontUnderlined, SetFontUnderlined);
    %property(FontFaceName, GetFontFaceName, SetFontFaceName);
    %property(FontEncoding, GetFontEncoding, SetFontEncoding);
    %property(FontFamily, GetFontFamily, SetFontFamily);
    %property(CharacterStyleName, GetCharacterStyleName, SetCharacterStyleName);
    %property(ParagraphStyleName, GetParagraphStyleName, SetParagraphStyleName);
    %property(ListStyleName, GetListStyleName, SetListStyleName);
    %property(ParagraphSpacingAfter, GetParagraphSpacingAfter, SetParagraphSpacingAfter);
    %property(ParagraphSpacingBefore, GetParagraphSpacingBefore, SetParagraphSpacingBefore);
    %property(LineSpacing, GetLineSpacing, SetLineSpacing);
    %property(BulletStyle, GetBulletStyle, SetBulletStyle);
    %property(BulletNumber, GetBulletNumber, SetBulletNumber);
    %property(BulletText, GetBulletText, SetBulletText);
    %property(BulletFont, GetBulletFont, SetBulletFont);
    %property(BulletName, GetBulletName, SetBulletName);
    %property(URL, GetURL, SetURL);
    %property(TextEffects, GetTextEffects, SetTextEffects);
    %property(TextEffectFlags, GetTextEffectFlags, SetTextEffectFlags);
    %property(OutlineLevel, GetOutlineLevel, SetOutlineLevel);
};

//---------------------------------------------------------------------------

// wxTextCtrl: a single or multiple line text zone where user can enter and
// edit text
MustHaveApp(wxTextCtrl);
class wxTextCtrl : public wxTextCtrlBase
{
public:
    %pythonAppend wxTextCtrl         "self._setOORInfo(self)"
    %pythonAppend wxTextCtrl()       ""
    %typemap(out) wxTextCtrl*;    // turn off this typemap

    wxTextCtrl(wxWindow* parent, wxWindowID id=-1,
               const wxString& value = wxPyEmptyString,
               const wxPoint& pos = wxDefaultPosition,
               const wxSize& size = wxDefaultSize,
               long style = 0,
               const wxValidator& validator = wxDefaultValidator,
               const wxString& name = wxPyTextCtrlNameStr);
    %RenameCtor(PreTextCtrl, wxTextCtrl());

    // Turn it back on again
    %typemap(out) wxTextCtrl* { $result = wxPyMake_wxObject($1, $owner); }

    bool Create(wxWindow* parent, wxWindowID id=-1,
               const wxString& value = wxPyEmptyString,
               const wxPoint& pos = wxDefaultPosition,
               const wxSize& size = wxDefaultSize,
               long style = 0,
               const wxValidator& validator = wxDefaultValidator,
               const wxString& name = wxPyTextCtrlNameStr);


    // more readable flag testing methods
    bool IsSingleLine() const;
    bool IsMultiLine() const;


    // insert the character which would have resulted from this key event,
    // return True if anything has been inserted
    virtual bool EmulateKeyPress(const wxKeyEvent& event);


#ifdef __WXMAC__
    virtual void MacCheckSpelling(bool check);
#else
    %extend {
        void MacCheckSpelling(bool check) {}
    }
#endif

    // generate the wxEVT_COMMAND_TEXT_UPDATED event, like SetValue() does
    void SendTextUpdatedEvent();

#ifdef __WXMSW__
    // Caret handling (Windows only)
    bool ShowNativeCaret(bool show = true);
    bool HideNativeCaret();
#endif

    %extend {
        // TODO: Add more file-like methods
        void write(const wxString& text) {
            self->AppendText(text);
        }
    }


    static wxVisualAttributes
    GetClassDefaultAttributes(wxWindowVariant variant = wxWINDOW_VARIANT_NORMAL);

};

//---------------------------------------------------------------------------


%constant wxEventType wxEVT_COMMAND_TEXT_UPDATED;
%constant wxEventType wxEVT_COMMAND_TEXT_ENTER;
%constant wxEventType wxEVT_COMMAND_TEXT_URL;
%constant wxEventType wxEVT_COMMAND_TEXT_MAXLEN;


class wxTextUrlEvent : public wxCommandEvent
{
public:
    wxTextUrlEvent(int winid, const wxMouseEvent& evtMouse,
                   long start, long end);

    // get the mouse event which happend over the URL
    const wxMouseEvent& GetMouseEvent();

    // get the start of the URL
    long GetURLStart() const;

    // get the end of the URL
    long GetURLEnd() const;

    %property(MouseEvent, GetMouseEvent, doc="See `GetMouseEvent`");
    %property(URLEnd, GetURLEnd, doc="See `GetURLEnd`");
    %property(URLStart, GetURLStart, doc="See `GetURLStart`");
};


%pythoncode {
EVT_TEXT        = wx.PyEventBinder( wxEVT_COMMAND_TEXT_UPDATED, 1)
EVT_TEXT_ENTER  = wx.PyEventBinder( wxEVT_COMMAND_TEXT_ENTER, 1)
EVT_TEXT_URL    = wx.PyEventBinder( wxEVT_COMMAND_TEXT_URL, 1)
EVT_TEXT_MAXLEN = wx.PyEventBinder( wxEVT_COMMAND_TEXT_MAXLEN, 1)
}




//---------------------------------------------------------------------------

