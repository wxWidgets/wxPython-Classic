/////////////////////////////////////////////////////////////////////////////
// Name:        core.i
// Purpose:     SWIG interface file for the CORE wxPython classes and stuff.
//
// Author:      Robin Dunn
//
// Created:     22-May-1998
// RCS-ID:      $Id$
// Copyright:   (c) 1998 by Total Control Software
// Licence:     wxWindows license
/////////////////////////////////////////////////////////////////////////////

%module(package="wx") _core

%{
#include "wx/wxPython/wxPython_int.h"
#include "wx/wxPython/pyclasses.h"
#include "wx/wxPython/twoitem.h"
%}


//---------------------------------------------------------------------------

#ifndef SWIGXML
%include typemaps.i
%include my_typemaps.i

%include _core_api.i

%native(_wxPySetDictionary)   __wxPySetDictionary;


%pythoncode {
%#//----------------------------------------------------------------------------
%#// These will be reset when the _wxPySetDictionary is called.  Dummy
%#// values are set here for tools that do static source analysis.
Platform = ""
PlatformInfo = ()

%#// Give a reference to the dictionary of this module to the C++ extension
%#// code.
_core_._wxPySetDictionary(vars())

%#// A little trick to make 'wx' be a reference to this module so wx.Names can
%#// be used here.
import sys as _sys
wx = _sys.modules[__name__]

}
#endif


%pythoncode {
%#----------------------------------------------------------------------------
            
import warnings
class wxPyDeprecationWarning(DeprecationWarning):
    pass
warnings.simplefilter('default', wxPyDeprecationWarning)
del warnings

def deprecated(item, msg=''):
    """
    Create a delegating wrapper that raises a deprecation warning.  Can be
    used with callable objects (functions, methods, classes) or with
    properties.
    """
    import warnings
    if isinstance(item, type):
        %# It is a class.  Make a subclass that raises a warning.
        class DeprecatedClassProxy(item):
            def __init__(*args, **kw):
                warnings.warn("Using deprecated class %s. %s" % (item.__name__, msg),
                          wxPyDeprecationWarning, stacklevel=2)
                item.__init__(*args, **kw)
        DeprecatedClassProxy.__name__ = item.__name__
        return DeprecatedClassProxy
    
    elif callable(item):
        %# wrap a new function around the callable
        def deprecated_func(*args, **kw):
            warnings.warn("Call to deprecated item. %s" %  msg,
                          wxPyDeprecationWarning, stacklevel=2)
            return item(*args, **kw)
        deprecated_func.__name__ = item.__name__
        deprecated_func.__doc__ = item.__doc__
        if hasattr(item, '__dict__'):
            deprecated_func.__dict__.update(item.__dict__)
        return deprecated_func
        
    elif hasattr(item, '__get__'):
        %# it should be a property if there is a getter
        class DepGetProp(object):
            def __init__(self,item, msg):
                self.item = item
                self.msg = msg
            def __get__(self, inst, klass):
                warnings.warn("Accessing deprecated property. %s" % msg,
                              wxPyDeprecationWarning, stacklevel=2)
                return self.item.__get__(inst, klass)
        class DepGetSetProp(DepGetProp):
            def __set__(self, inst, val):
                warnings.warn("Accessing deprecated property. %s" % msg,
                              wxPyDeprecationWarning, stacklevel=2)
                return self.item.__set__(inst, val)
        class DepGetSetDelProp(DepGetSetProp):
            def __delete__(self, inst):
                warnings.warn("Accessing deprecated property. %s" % msg,
                              wxPyDeprecationWarning, stacklevel=2)
                return self.item.__delete__(inst)
        
        if hasattr(item, '__set__') and hasattr(item, '__delete__'):
            return DepGetSetDelProp(item, msg)
        elif hasattr(item, '__set__'):
            return DepGetSetProp(item, msg)
        else:
            return DepGetProp(item, msg)
    else:
        raise TypeError, "unsupported type %s" % type(item)
                   
         
                   
%#----------------------------------------------------------------------------
}


//---------------------------------------------------------------------------
// Include all the files that make up the core module

// wxObject, functions and other base stuff
%include _defs.i

MAKE_CONST_WXSTRING(EmptyString);

%include _swigtype.i

%include _obj.i
%include _gdicmn.i
%include _streams.i
%include _filesys.i
%include _image.i


// Events, event handlers, base Windows and such
%include _evthandler.i
%include _keyboardstate.i
%include _mousestate.i
%include _event.i
%include _app.i
%include _evtloop.i
%include _accel.i
%include _window.i
%include _validator.i
%include _menu.i
%include _control.i
%include _withimages.i
%include _bookctrl.i

// Layout
%include _sizers.i
%include _gbsizer.i
%include _constraints.i

// other
%include _headercol.i
%include _versioninfo.i


%pythoncode "_core_ex.py"

//---------------------------------------------------------------------------
// This code gets added to the module initialization function

%init %{
    // Initialize threading, some globals and such
    __wxPyPreStart(d);
    

    // Although these are defined in __version__ they need to be here too so
    // that an assert can be done to ensure that the wxPython and the wxWindows
    // versions match.
    PyDict_SetItemString(d,"MAJOR_VERSION", PyInt_FromLong((long)wxMAJOR_VERSION ));
    PyDict_SetItemString(d,"MINOR_VERSION", PyInt_FromLong((long)wxMINOR_VERSION ));
    PyDict_SetItemString(d,"RELEASE_VERSION", PyInt_FromLong((long)wxRELEASE_NUMBER ));
%}
 
//---------------------------------------------------------------------------
