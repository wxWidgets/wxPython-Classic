/////////////////////////////////////////////////////////////////////////////
// Name:        _headercol.i
// Purpose:     SWIG interface for wxHeaderColumn
//
// Author:      Robin Dunn
//
// Created:     13-April-2009
// RCS-ID:      $Id: $
// Copyright:   (c) 2009 by Total Control Software
// Licence:     wxWindows license
/////////////////////////////////////////////////////////////////////////////

// Not a %module

%{
#include <wx/headercol.h>
%}

//---------------------------------------------------------------------------
%newgroup

enum
{
    // special value for column width meaning unspecified/default
    wxCOL_WIDTH_DEFAULT = -1,

    // size the column automatically to fit all values
    wxCOL_WIDTH_AUTOSIZE = -2
};

// bit masks for the various column attributes
enum
{
    // column can be resized (included in default flags)
    wxCOL_RESIZABLE   = 1,

    // column can be clicked to toggle the sort order by its contents
    wxCOL_SORTABLE    = 2,

    // column can be dragged to change its order (included in default)
    wxCOL_REORDERABLE = 4,

    // column is not shown at all
    wxCOL_HIDDEN      = 8,

    // default flags for wxHeaderColumn ctor
    wxCOL_DEFAULT_FLAGS = wxCOL_RESIZABLE | wxCOL_REORDERABLE
};



// ----------------------------------------------------------------------------
// wxHeaderColumn: interface for a column in a header of controls such as
//                 wxListCtrl, wxDataViewCtrl or wxGrid
// ----------------------------------------------------------------------------

class wxHeaderColumn
{
public:
    // *** ABC, no ctor

    virtual ~wxHeaderColumn();

    // getters for various attributes
    // ------------------------------

    // notice that wxHeaderColumn only provides getters as this is all the
    // wxHeaderCtrl needs, various derived class must also provide some way to
    // change these attributes but this can be done either at the column level
    // (in which case they should inherit from wxSettableHeaderColumn) or via
    // the methods of the main control in which case you don't need setters in
    // the column class at all

    // title is the string shown for this column
    virtual wxString GetTitle() const;

    // bitmap shown (instead of text) in the column header
    virtual wxBitmap GetBitmap() const;                                   

    // width of the column in pixels, can be set to wxCOL_WIDTH_DEFAULT meaning
    // unspecified/default
    virtual int GetWidth() const;

    // minimal width can be set for resizeable columns to forbid resizing them
    // below the specified size (set to 0 to remove)
    virtual int GetMinWidth() const;

    // alignment of the text: wxALIGN_CENTRE, wxALIGN_LEFT or wxALIGN_RIGHT
    virtual wxAlignment GetAlignment() const;


    // flags manipulations:
    // --------------------

    // notice that while we make GetFlags() pure virtual here and implement the
    // individual flags access in terms of it, for some derived classes it is
    // more natural to implement access to each flag individually, in which
    // case they can use our GetFromIndividualFlags() helper below to implement
    // GetFlags()

    // retrieve all column flags at once: combination of wxCOL_XXX values above
    virtual int GetFlags() const;

    bool HasFlag(int flag) const;


    // wxCOL_RESIZABLE
    virtual bool IsResizeable() const;

    // wxCOL_SORTABLE
    virtual bool IsSortable() const;

    // wxCOL_REORDERABLE
    virtual bool IsReorderable() const;

    // wxCOL_HIDDEN
    virtual bool IsHidden() const;
    bool IsShown() const;


    // sorting
    // -------

    // return true if the column is the one currently used for sorting
    virtual bool IsSortKey() const;

    // for sortable columns indicate whether we should sort in ascending or
    // descending order (this should only be taken into account if IsSortKey())
    virtual bool IsSortOrderAscending() const;

    %property(Title, GetTitle);
    %property(Bitmap, GetBitmap);
    %property(Width, GetWidth);
    %property(MinWidth, GetMinWidth);
    %property(Alignment, GetAlignment);
    %property(Flags, GetFlags);

    %property(Resizeable, IsResizeable);
    %property(Sortable, IsSortable);
    %property(Reorderable, IsReorderable);
    %property(Hidden, IsHidden);
    %property(Shown, IsShown);
    %property(SortOrderAscending, IsSortOrderAscending);
    %property(SortKey, IsSortKey);

};

// ----------------------------------------------------------------------------
// wxSettableHeaderColumn: column which allows to change its fields too
// ----------------------------------------------------------------------------

class wxSettableHeaderColumn : public wxHeaderColumn
{
public:
    // *** ABC, no ctor
    
    virtual void SetTitle(const wxString& title);
    virtual void SetBitmap(const wxBitmap& bitmap);
    virtual void SetWidth(int width);
    virtual void SetMinWidth(int minWidth);
    virtual void SetAlignment(wxAlignment align);

    virtual void SetFlags(int flags);
    void ChangeFlag(int flag, bool set);
    void SetFlag(int flag);
    void ClearFlag(int flag);
    void ToggleFlag(int flag);

    virtual void SetResizeable(bool resizeable);
    virtual void SetSortable(bool sortable);
    virtual void SetReorderable(bool reorderable);
    virtual void SetHidden(bool hidden);

    virtual void SetAsSortKey(bool sort = true);
    void UnsetAsSortKey();

    virtual void SetSortOrder(bool ascending);
    void ToggleSortOrder();

    %property(Title, HeaderColumn.GetTitle, SetTitle);
    %property(Bitmap, HeaderColumn.GetBitmap, SetBitmap);
    %property(Width, HeaderColumn.GetWidth, SetWidth);
    %property(MinWidth, HeaderColumn.GetMinWidth, SetMinWidth);
    %property(Alignment, HeaderColumn.GetAlignment, SetAlignment);
    %property(Flags, HeaderColumn.GetFlags, SetFlags);

    %property(Resizeable, HeaderColumn.IsResizeable, SetResizeable);
    %property(Sortable, HeaderColumn.IsSortable, SetSortable);
    %property(Reorderable, HeaderColumn.IsReorderable, SetReorderable);
    %property(Hidden, HeaderColumn.IsHidden, SetHidden);
    %property(SortKey, HeaderColumn.IsSortKey, SetAsSortKey);
};

// ----------------------------------------------------------------------------
// wxHeaderColumnSimple: trivial generic implementation of wxHeaderColumn
// ----------------------------------------------------------------------------

class wxHeaderColumnSimple : public wxSettableHeaderColumn
{
public:
    %extend {
        wxHeaderColumnSimple(PyObject* title_or_bitmap,
                         int width = wxCOL_WIDTH_DEFAULT,
                         wxAlignment align = wxALIGN_NOT,
                         int flags = wxCOL_DEFAULT_FLAGS)
        {
            bool wasString;
            wxString label;
            wxBitmap bitmap;
            if (! wxPyTextOrBitmap_helper(title_or_bitmap, wasString, label, bitmap))
                return NULL;
            return wasString ?
                new wxHeaderColumnSimple(label, width, align, flags)
                :  new wxHeaderColumnSimple(bitmap, width, align, flags);
        }
    }
};



//---------------------------------------------------------------------------
