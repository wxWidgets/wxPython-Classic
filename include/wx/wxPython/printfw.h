/////////////////////////////////////////////////////////////////////////////
// Name:        printfw.h
// Purpose:     Exposing the class definition of wxPyPrintout so it can also 
//              be used by wxHtmlPrintout.  Must be included after wxPython.h
//
// Author:      Robin Dunn
//
// Created:     29-Oct-1999
// RCS-ID:      $Id$
// Copyright:   (c) 1999 by Total Control Software
// Licence:     wxWindows license
/////////////////////////////////////////////////////////////////////////////

#ifndef __wxpy_printfw_h
#define __wxpy_printfw_h

#if !wxUSE_PRINTING_ARCHITECTURE
#error wxPython requires the wx printing architecture to be enabled
#endif

class wxPyPrintout : public wxPrintout {
public:
    wxPyPrintout(const wxString& title) : wxPrintout(title) {}

    bool OnBeginDocument(int a, int b);
    void OnEndDocument(); 
    void OnBeginPrinting();
    void OnEndPrinting();
    void OnPreparePrinting();
    bool OnPrintPage(int a);
    bool HasPage(int a);
    void GetPageInfo(int *minPage, int *maxPage, int *pageFrom, int *pageTo);

    PYPRIVATE;
    DECLARE_ABSTRACT_CLASS(wxPyPrintout)
};

#endif
