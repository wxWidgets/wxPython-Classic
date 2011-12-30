#
# Configuration file for create_vcw.py
#

import os

# NOTE! You may need to change this to get the script working.
WX_BASE = os.environ['WXWIN']


projname = 'propgrid'

defines = ['wxUSE_PROPGRID 1', 'wxUSE_VALIDATORS 1', 'wxUSE_DATEPICKCTRL 1',
           'wxUSE_SPINCTRL 1', 'wxUSE_DATETIME 1', 'wxUSE_TOOLTIPS 1']

work_dir = '../../src'
output_dir = work_dir

#
# Find classes in these files
files = ['propgriddefs.h', 'property.h', 'propgridpagestate.h',
    'propgridiface.h', 'propgrid.h', 'editors.h', 'props.h', 'advprops.h']

#
# Create virtual-call wrappers only for these clasees
classes = ['wxPGEditor', 'wxPGProperty', 'wxPGEditorDialogAdapter',
           'wxPGEditableState']

default_script_object_member = 'm_clientData'

class_config = {
    'wxPGProperty' :
    { 'script_object_member' : default_script_object_member,
      #'__init__append'       : 'self._setOORInfo(self)',
      'excluded_methods'     : ['ValidateValue', 'StringToValue', 'IntToValue',
                                'DoGetEditorClass'] },

    'wxPGEditor' :
    { 'script_object_member' : default_script_object_member,
      'excluded_methods'     : ['GetValueFromControl'] },
}

includes = ['my_typemaps.i', 'propgrid.i']

# Ignore typemaps for these types from base wxPython typemap files
# (ie. my_typemaps.i).
ignore_typemaps_from_base = ['wxVariant']

include_paths = [WX_BASE+'/include',
                 WX_BASE+'/include/wx/propgrid',
                 #WX_BASE+'/lib/vc_dll/mswh',
                 WX_BASE+'/lib/vc_dll/mswuh',
                 '../../src']

# If no renamer found, a new class name is generated (for callback classes)
# by adding Py in front of them. Note that topmost renamers take precedence.
#
# All use Python regex substitution format.
class_renamers = [
('wx(\w+)Class', r'Py\1'),
('wxPG(\w+)', r'Py\1'),
('wx(\w+)', r'Py\1'),
]

#
# Code from here is adapted to wrappers, as follows:
#
# 1) pyvirtual methods are added as additional virtuals to generate wrapper for.
# 2) Virtual methods, for which function content is given, are implemented in
#    all classes which parent C++ class implements this same method (and also
#    naturally in top most class). pyvirtual functions also count as virtual.
# 3) Other methods are just added to topmost class (NB: Not yet implemented!).
#
# Other remarks:
# - pyvirtual Functions with name like PyFuncName will be have their name
#   exposed in Python as FuncName.
#
add_wrapper_code = """\

class wxPGProperty
{
    pyvirtual wxPGVariantAndBool PyValidateValue( const wxVariant& value, wxPGValidationInfo& validationInfo ) const
    {
        wxPGVariantAndBool vab;
        vab.m_value = value;
        vab.m_valueValid = true;
        vab.m_result = %(class_name)s::ValidateValue(vab.m_value, validationInfo);
        return vab;
    }

    pyvirtual wxPGVariantAndBool PyStringToValue( const wxString& text, int argFlags ) const
    {
        wxPGVariantAndBool vab;
        vab.m_result = %(class_name)s::StringToValue(vab.m_value, text, argFlags);
        if ( vab.m_result )
            vab.m_valueValid = true;
        return vab;
    }

    pyvirtual wxPGVariantAndBool PyIntToValue( int number, int argFlags ) const
    {
        wxPGVariantAndBool vab;
        vab.m_result = %(class_name)s::IntToValue(vab.m_value, number, argFlags);
        if ( vab.m_result )
            vab.m_valueValid = true;
        return vab;
    }

    pyvirtual wxString PyGetEditor() const
    {
        return wxT("TextCtrl");
    }

    virtual const wxPGEditor* DoGetEditorClass() const
    {
        return wxPropertyGridInterface::GetEditorByName(PyGetEditor());
    }

    virtual bool ValidateValue( wxVariant& value, wxPGValidationInfo& validationInfo ) const
    {
        if ( %(script_object_member)s )
        {
            wxPGVariantAndBool vab = PyValidateValue(value, validationInfo);
            if ( vab.m_valueValid )
                value = vab.m_value;
            return vab.m_result;
        }
        return %(class_name)s::ValidateValue(value, validationInfo);
    }

    virtual bool StringToValue( wxVariant& variant, const wxString& text, int argFlags = 0 ) const
    {
        if ( %(script_object_member)s )
        {
            wxPGVariantAndBool vab = PyStringToValue(text, argFlags);
            if ( vab.m_valueValid )
                variant = vab.m_value;
            return vab.m_result;
        }
        return %(class_name)s::StringToValue(variant, text, argFlags);
    }

    virtual bool IntToValue( wxVariant& variant, int number, int argFlags = 0 ) const
    {
        if ( %(script_object_member)s )
        {
            wxPGVariantAndBool vab = PyIntToValue(number, argFlags);
            if ( vab.m_valueValid )
                variant = vab.m_value;
            return vab.m_result;
        }
        return %(class_name)s::IntToValue(variant, number, argFlags);
    }
};

class wxPGEditor
{
    pyvirtual wxPGVariantAndBool PyGetValueFromControl( wxPGProperty* property, wxWindow* ctrl ) const
    {
        wxPGVariantAndBool vab;
        vab.m_result = %(class_name)s::GetValueFromControl(vab.m_value, property, ctrl);
        if ( vab.m_result )
            vab.m_valueValid = true;
        return vab;
    }

    virtual bool GetValueFromControl( wxVariant& value, wxPGProperty* property, wxWindow* ctrl ) const
    {
        if ( %(script_object_member)s )
        {
            wxPGVariantAndBool vab = PyGetValueFromControl(property, ctrl);
            if ( vab.m_valueValid )
                value = vab.m_value;
            return vab.m_result;
        }
        return %(class_name)s::GetValueFromControl(value, property, ctrl);
    }
};
"""

logging = False

