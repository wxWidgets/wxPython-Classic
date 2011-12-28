/////////////////////////////////////////////////////////////////////////////
// Name:        withimages.i
// Purpose:     SWIG interface for wxWithImages
//
// Author:      Robin Dunn
//
// Created:     7-Sept-2011
// RCS-ID:      $Id: $
// Copyright:   (c) 2011 by Total Control Software
// Licence:     wxWindows license
/////////////////////////////////////////////////////////////////////////////

// Not a %module


//---------------------------------------------------------------------------
%newgroup

%{
    #include "wx/withimages.h"
%}    

// ----------------------------------------------------------------------------
// wxWithImages: mix-in class providing access to wxImageList.
// ----------------------------------------------------------------------------

class wxWithImages
{
public:
    enum
    {
        NO_IMAGE = -1
    };

    wxWithImages();

    virtual ~wxWithImages();

    // Sets the image list to use, it is *not* deleted by the control.
    virtual void SetImageList(wxImageList* imageList);

    // As SetImageList() but we will delete the image list ourselves.
    %disownarg( wxImageList *imageList );
    void AssignImageList(wxImageList* imageList);
    %cleardisown( wxImageList *imageList );

    // Get pointer (may be NULL) to the associated image list.
    wxImageList* GetImageList() const;

    %property(ImageList, GetImageList, SetImageList, doc="See `GetImageList` and `SetImageList`");

};


//---------------------------------------------------------------------------
