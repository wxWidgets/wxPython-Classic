/////////////////////////////////////////////////////////////////////////////
// Name:        stc.i
// Purpose:     Wrappers for the wxStyledTextCtrl.
//
// Author:      Robin Dunn
//
// Created:     12-Oct-1999
// RCS-ID:      $Id$
// Copyright:   (c) 2000 by Total Control Software
// Licence:     wxWindows license
/////////////////////////////////////////////////////////////////////////////

%define DOCSTRING
"The `StyledTextCtrl` provides a text editor that can used as a syntax
highlighting source code editor, or similar.  Lexers for several programming
languages are built-in."
%enddef

%module(package="wx", docstring=DOCSTRING) stc


%{
#include "wx/wxPython/wxPython.h"
#include "wx/wxPython/pyclasses.h"
#include <wx/stc/stc.h>
%}

//---------------------------------------------------------------------------

%import core.i
%import misc.i  // for DnD
//%import gdi.i   // for wxFontEncoding

%pythoncode { wx = _core }
%pythoncode { __docfilter__ = wx.__DocFilter(globals()) }

MAKE_CONST_WXSTRING(STCNameStr);


%include _stc_docstrings.i

enum wxFontEncoding;  // forward declare

MustHaveApp(wxStyledTextCtrl);

%ignore wxStyledTextCtrl::HitTest;
%ignore wxStyledTextCtrl::GetCharacterPointer;

//---------------------------------------------------------------------------
// Get all our defs from the REAL header file.

#define wxUSE_STC 1
#define wxUSE_TEXTCTRL 1
#define WXDLLIMPEXP_STC
#define WXDLLIMPEXP_FWD_STC
#define WXDLLIMPEXP_CORE
#define WXDLLIMPEXP_FWD_CORE
%include stc.h


%extend wxStyledTextCtrl {
    %extend {
        PyObject* GetCharacterPointer() {
            const char* ptr = self->GetCharacterPointer();
            int len = self->GetLength();
            PyObject* rv;
            wxPyBLOCK_THREADS( rv = PyBuffer_FromMemory((void*)ptr, len) );
            return rv;
        }
    }
    
    %pythoncode {
        GetCaretLineBack = GetCaretLineBackground
        SetCaretLineBack = SetCaretLineBackground
    }

    
    %property(Anchor, GetAnchor, SetAnchor);
    %property(BackSpaceUnIndents, GetBackSpaceUnIndents, SetBackSpaceUnIndents);
    %property(BufferedDraw, GetBufferedDraw, SetBufferedDraw);
    %property(CaretForeground, GetCaretForeground, SetCaretForeground);
    %property(CaretLineBack, GetCaretLineBack, SetCaretLineBack);
    %property(CaretLineBackAlpha, GetCaretLineBackAlpha, SetCaretLineBackAlpha);
    %property(CaretLineBackground, GetCaretLineBackground, SetCaretLineBackground);
    %property(CaretLineVisible, GetCaretLineVisible, SetCaretLineVisible);
    %property(CaretPeriod, GetCaretPeriod, SetCaretPeriod);
    %property(CaretSticky, GetCaretSticky, SetCaretSticky);
    %property(CaretWidth, GetCaretWidth, SetCaretWidth);
    %property(CodePage, GetCodePage, SetCodePage);
    %property(ControlCharSymbol, GetControlCharSymbol, SetControlCharSymbol);
    %property(CurLine, GetCurLine);
    %property(CurLineRaw, GetCurLineRaw);
    %property(CurLineUTF8, GetCurLineUTF8);
    %property(CurrentLine, GetCurrentLine);
    %property(CurrentPos, GetCurrentPos, SetCurrentPos);
    %property(DocPointer, GetDocPointer, SetDocPointer);
    %property(EOLMode, GetEOLMode, SetEOLMode);
    %property(EdgeColour, GetEdgeColour, SetEdgeColour);
    %property(EdgeColumn, GetEdgeColumn, SetEdgeColumn);
    %property(EdgeMode, GetEdgeMode, SetEdgeMode);
    %property(EndAtLastLine, GetEndAtLastLine, SetEndAtLastLine);
    %property(EndStyled, GetEndStyled);
    %property(FirstVisibleLine, GetFirstVisibleLine);
    %property(HighlightGuide, GetHighlightGuide, SetHighlightGuide);
    %property(Indent, GetIndent, SetIndent);
    %property(IndentationGuides, GetIndentationGuides, SetIndentationGuides);
    %property(LastKeydownProcessed, GetLastKeydownProcessed, SetLastKeydownProcessed);
    %property(LayoutCache, GetLayoutCache, SetLayoutCache);
    %property(Length, GetLength);
    %property(Lexer, GetLexer, SetLexer);
    %property(LineCount, GetLineCount);
    %property(MarginLeft, GetMarginLeft, SetMarginLeft);
    %property(MarginRight, GetMarginRight, SetMarginRight);
    %property(MaxLineState, GetMaxLineState);
    %property(ModEventMask, GetModEventMask, SetModEventMask);
    %property(Modify, GetModify);
    %property(MouseDownCaptures, GetMouseDownCaptures, SetMouseDownCaptures);
    %property(MouseDwellTime, GetMouseDwellTime, SetMouseDwellTime);
    %property(Overtype, GetOvertype, SetOvertype);
    %property(PasteConvertEndings, GetPasteConvertEndings, SetPasteConvertEndings);
    %property(PrintColourMode, GetPrintColourMode, SetPrintColourMode);
    %property(PrintMagnification, GetPrintMagnification, SetPrintMagnification);
    %property(PrintWrapMode, GetPrintWrapMode, SetPrintWrapMode);
    %property(ReadOnly, GetReadOnly, SetReadOnly);
    %property(STCCursor, GetSTCCursor, SetSTCCursor);
    %property(STCFocus, GetSTCFocus, SetSTCFocus);
    %property(ScrollWidth, GetScrollWidth, SetScrollWidth);
    %property(SearchFlags, GetSearchFlags, SetSearchFlags);
    %property(SelAlpha, GetSelAlpha, SetSelAlpha);
    %property(SelectedText, GetSelectedText);
    %property(SelectedTextRaw, GetSelectedTextRaw);
    %property(SelectedTextUTF8, GetSelectedTextUTF8);

    //%property(Selection, GetSelection, SetSelection);
    //%property(Selection, GetSelection);
    
    %property(SelectionEnd, GetSelectionEnd, SetSelectionEnd);
    %property(SelectionMode, GetSelectionMode, SetSelectionMode);
    %property(SelectionStart, GetSelectionStart, SetSelectionStart);
    %property(Status, GetStatus, SetStatus);
    %property(StyleBits, GetStyleBits, SetStyleBits);
    %property(StyleBitsNeeded, GetStyleBitsNeeded);
    %property(TabIndents, GetTabIndents, SetTabIndents);
    %property(TabWidth, GetTabWidth, SetTabWidth);
    %property(TargetEnd, GetTargetEnd, SetTargetEnd);
    %property(TargetStart, GetTargetStart, SetTargetStart);
    %property(Text, GetText, SetText);
    %property(TextLength, GetTextLength);
    %property(TextRaw, GetTextRaw, SetTextRaw);
    %property(TextUTF8, GetTextUTF8, SetTextUTF8);
    %property(TwoPhaseDraw, GetTwoPhaseDraw, SetTwoPhaseDraw);
    %property(UndoCollection, GetUndoCollection, SetUndoCollection);
    %property(UseAntiAliasing, GetUseAntiAliasing, SetUseAntiAliasing);
    %property(UseHorizontalScrollBar, GetUseHorizontalScrollBar, SetUseHorizontalScrollBar);
    %property(UseTabs, GetUseTabs, SetUseTabs);
    %property(UseVerticalScrollBar, GetUseVerticalScrollBar, SetUseVerticalScrollBar);
    %property(ViewEOL, GetViewEOL, SetViewEOL);
    %property(ViewWhiteSpace, GetViewWhiteSpace, SetViewWhiteSpace);
    %property(WrapMode, GetWrapMode, SetWrapMode);
    %property(WrapStartIndent, GetWrapStartIndent, SetWrapStartIndent);
    %property(WrapVisualFlags, GetWrapVisualFlags, SetWrapVisualFlags);
    %property(WrapVisualFlagsLocation, GetWrapVisualFlagsLocation, SetWrapVisualFlagsLocation);
    %property(XOffset, GetXOffset, SetXOffset);
    %property(Zoom, GetZoom, SetZoom);

    %property(SelEOLFilled, GetSelEOLFilled, SetSelEOLFilled);
    %property(ScrollWidthTracking, GetScrollWidthTracking, SetScrollWidthTracking);
    %property(HotspotActiveForeground, GetHotspotActiveForeground, SetHotspotActiveForeground);
    %property(HotspotActiveBackground, GetHotspotActiveBackground, SetHotspotActiveBackground);
    %property(HotspotActiveUnderline, GetHotspotActiveUnderline, SetHotspotActiveUnderline);
    %property(HotspotSingleLine, GetHotspotSingleLine, SetHotspotSingleLine);
    %property(CaretStyle, GetCaretStyle, SetCaretStyle);
    %property(IndicatorCurrent, GetIndicatorCurrent, SetIndicatorCurrent);
    %property(IndicatorValue, GetIndicatorValue, SetIndicatorValue);
    %property(PositionCacheSize, GetPositionCacheSize, SetPositionCacheSize);
    
}


%extend wxStyledTextEvent {
    %property(Alt, GetAlt);
    %property(Control, GetControl);
    %property(DragAllowMove, GetDragAllowMove, SetDragAllowMove);
    %property(DragResult, GetDragResult, SetDragResult);
    %property(DragText, GetDragText, SetDragText);
    %property(FoldLevelNow, GetFoldLevelNow, SetFoldLevelNow);
    %property(FoldLevelPrev, GetFoldLevelPrev, SetFoldLevelPrev);
    %property(Key, GetKey, SetKey);
    %property(LParam, GetLParam, SetLParam);
    %property(Length, GetLength, SetLength);
    %property(Line, GetLine, SetLine);
    %property(LinesAdded, GetLinesAdded, SetLinesAdded);
    %property(ListType, GetListType, SetListType);
    %property(Margin, GetMargin, SetMargin);
    %property(Message, GetMessage, SetMessage);
    %property(ModificationType, GetModificationType, SetModificationType);
    %property(Modifiers, GetModifiers, SetModifiers);
    %property(Position, GetPosition, SetPosition);
    %property(Shift, GetShift);
    %property(Text, GetText, SetText);
    %property(WParam, GetWParam, SetWParam);
    %property(X, GetX, SetX);
    %property(Y, GetY, SetY);
}

//---------------------------------------------------------------------------
// STC Events

%pythoncode {
EVT_STC_CHANGE = wx.PyEventBinder( wxEVT_STC_CHANGE, 1 )
EVT_STC_STYLENEEDED = wx.PyEventBinder( wxEVT_STC_STYLENEEDED, 1 )
EVT_STC_CHARADDED = wx.PyEventBinder( wxEVT_STC_CHARADDED, 1 )
EVT_STC_SAVEPOINTREACHED = wx.PyEventBinder( wxEVT_STC_SAVEPOINTREACHED, 1 )
EVT_STC_SAVEPOINTLEFT = wx.PyEventBinder( wxEVT_STC_SAVEPOINTLEFT, 1 )
EVT_STC_ROMODIFYATTEMPT = wx.PyEventBinder( wxEVT_STC_ROMODIFYATTEMPT, 1 )
EVT_STC_KEY = wx.PyEventBinder( wxEVT_STC_KEY, 1 )
EVT_STC_DOUBLECLICK = wx.PyEventBinder( wxEVT_STC_DOUBLECLICK, 1 )
EVT_STC_UPDATEUI = wx.PyEventBinder( wxEVT_STC_UPDATEUI, 1 )
EVT_STC_MODIFIED = wx.PyEventBinder( wxEVT_STC_MODIFIED, 1 )
EVT_STC_MACRORECORD = wx.PyEventBinder( wxEVT_STC_MACRORECORD, 1 )
EVT_STC_MARGINCLICK = wx.PyEventBinder( wxEVT_STC_MARGINCLICK, 1 )
EVT_STC_NEEDSHOWN = wx.PyEventBinder( wxEVT_STC_NEEDSHOWN, 1 )
EVT_STC_PAINTED = wx.PyEventBinder( wxEVT_STC_PAINTED, 1 )
EVT_STC_USERLISTSELECTION = wx.PyEventBinder( wxEVT_STC_USERLISTSELECTION, 1 )
EVT_STC_URIDROPPED = wx.PyEventBinder( wxEVT_STC_URIDROPPED, 1 )
EVT_STC_DWELLSTART = wx.PyEventBinder( wxEVT_STC_DWELLSTART, 1 )
EVT_STC_DWELLEND = wx.PyEventBinder( wxEVT_STC_DWELLEND, 1 )
EVT_STC_START_DRAG = wx.PyEventBinder( wxEVT_STC_START_DRAG, 1 )
EVT_STC_DRAG_OVER = wx.PyEventBinder( wxEVT_STC_DRAG_OVER, 1 )
EVT_STC_DO_DROP = wx.PyEventBinder( wxEVT_STC_DO_DROP, 1 )
EVT_STC_ZOOM = wx.PyEventBinder( wxEVT_STC_ZOOM, 1 )
EVT_STC_HOTSPOT_CLICK = wx.PyEventBinder( wxEVT_STC_HOTSPOT_CLICK, 1 )
EVT_STC_HOTSPOT_DCLICK = wx.PyEventBinder( wxEVT_STC_HOTSPOT_DCLICK, 1 )
EVT_STC_CALLTIP_CLICK = wx.PyEventBinder( wxEVT_STC_CALLTIP_CLICK, 1 )
EVT_STC_AUTOCOMP_SELECTION = wx.PyEventBinder( wxEVT_STC_AUTOCOMP_SELECTION, 1 )
EVT_STC_INDICATOR_CLICK = wx.PyEventBinder( wxEVT_STC_INDICATOR_CLICK, 1 )
EVT_STC_INDICATOR_RELEASE = wx.PyEventBinder( wxEVT_STC_INDICATOR_RELEASE, 1 )
EVT_STC_AUTOCOMP_CANCELLED = wx.PyEventBinder( wxEVT_STC_AUTOCOMP_CANCELLED, 1 )
EVT_STC_AUTOCOMP_CHAR_DELETED = wx.PyEventBinder( wxEVT_STC_AUTOCOMP_CHAR_DELETED, 1 )    
}

//---------------------------------------------------------------------------

%init %{
%}


//---------------------------------------------------------------------------

