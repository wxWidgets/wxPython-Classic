/////////////////////////////////////////////////////////////////////////////
// Name:        _combobox.i
// Purpose:     SWIG interface defs for wxComboBox
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

MAKE_CONST_WXSTRING(ComboBoxNameStr);

//---------------------------------------------------------------------------
%newgroup;


DocStr(wxComboBox,
"A combobox is like a combination of an edit control and a
listbox. It can be displayed as static list with editable or
read-only text field; or a drop-down list with text field.

A combobox permits a single selection only. Combobox items are
numbered from zero.", "

Styles
------
    ================    ===============================================
    wx.CB_SIMPLE        Creates a combobox with a permanently
                        displayed list.  Windows only.

    wx.CB_DROPDOWN      Creates a combobox with a drop-down list.

    wx.CB_READONLY      Same as wxCB_DROPDOWN but only the strings
                        specified as the combobox choices can be
                        selected, it is impossible to select
                        (even from a program) a string which is
                        not in the choices list.

    wx.CB_SORT          Sorts the entries in the list alphabetically.
    ================    ===============================================

Events
-------
    ================    ===============================================
    EVT_COMBOBOX        Sent when an item on the list is selected.
                        Note that calling `GetValue` in this handler 
                        will return the newly selected value.
    EVT_TEXT            Sent when the combobox text changes.
    EVT_TEXT_ENTER      Sent when the RETURN/ENTER key is pressed in
                        the combobox.
    ================    ===============================================
");



MustHaveApp(wxComboBox);

#ifdef __WXMSW__
class wxComboBox : public wxChoice, public wxTextEntry
#else
class wxComboBox : public wxControl, public wxItemContainer, public wxTextEntry
#endif
{
public:
    %pythonAppend wxComboBox         "self._setOORInfo(self)"
    %pythonAppend wxComboBox()       ""

    DocCtorAStr(
        wxComboBox(wxWindow* parent, wxWindowID id=-1,
                   const wxString& value = wxPyEmptyString,
                   const wxPoint& pos = wxDefaultPosition,
                   const wxSize& size = wxDefaultSize,
                   const wxArrayString& choices = wxPyEmptyStringArray,
                   long style = 0,
                   const wxValidator& validator = wxDefaultValidator,
                   const wxString& name = wxPyComboBoxNameStr),
        "__init__(Window parent, int id=-1, String value=EmptyString,
    Point pos=DefaultPosition, Size size=DefaultSize,
    List choices=EmptyList, long style=0, Validator validator=DefaultValidator,
    String name=ComboBoxNameStr) -> ComboBox",
        "Constructor, creates and shows a ComboBox control.", "");

    DocCtorStrName(
        wxComboBox(),
        "Precreate a ComboBox control for 2-phase creation.", "",
        PreComboBox);


    DocDeclAStr(
        bool, Create(wxWindow *parent, wxWindowID id=-1,
                     const wxString& value = wxPyEmptyString,
                     const wxPoint& pos = wxDefaultPosition,
                     const wxSize& size = wxDefaultSize,
                     const wxArrayString& choices = wxPyEmptyStringArray,
                     long style = 0,
                     const wxValidator& validator = wxDefaultValidator,
                     const wxString& name = wxPyChoiceNameStr),
        "Create(Window parent, int id=-1, String value=EmptyString,
    Point pos=DefaultPosition, Size size=DefaultSize,
    List choices=EmptyList, long style=0, Validator validator=DefaultValidator,
    String name=ChoiceNameStr) -> bool",
        "Actually create the GUI wxComboBox control for 2-phase creation", "");
    

    
    DocDeclStr(
        void , SetSelection(int n),
        "Sets the item at index 'n' to be the selected item.", "");
    
    DocStr(SetMark,
           "Selects the text between the two positions in the combobox text field.", "");
    %extend {
        void SetMark(long from, long to)
        {
            self->SetSelection(from, to);
        }
    }

    DocDeclAStrName(
        virtual void , GetSelection(long* OUTPUT, long* OUTPUT),
        "GetMark(self) -> (from, to)",
        "Gets the positions of the begining and ending of the selection mark in
the combobox text field.", "",
        GetMark);


    %extend {
        bool IsEmpty() {
            return self->wxItemContainer::IsEmpty();
        }
    }

    bool IsListEmpty() const;
    bool IsTextEmpty() const;

    virtual void Popup();
    virtual void Dismiss();


    DocDeclStr(
        int , GetCurrentSelection() const,
        "Unlike `GetSelection` which only returns the accepted selection value,
i.e. the selection in the control once the user closes the dropdown
list, this function returns the current selection.  That is, while the
dropdown list is shown, it returns the currently selected item in
it. When it is not shown, its result is the same as for the other
function.", "");
    
    DocDeclStr(
        bool , SetStringSelection(const wxString& string),
        "Select the item with the specifed string", "");
    
    DocDeclStr(
        void , SetString(int n, const wxString& string),
        "Set the label for the n'th item (zero based) in the list.", "");
    


    
    static wxVisualAttributes
    GetClassDefaultAttributes(wxWindowVariant variant = wxWINDOW_VARIANT_NORMAL);

    %property(CurrentSelection, GetCurrentSelection);
    %property(Mark, GetMark, SetMark);

};

//---------------------------------------------------------------------------
