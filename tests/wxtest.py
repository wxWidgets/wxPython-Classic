"""Common code for wxPython's unit test suite.

wxtest's major use is to provide a standard means of determining information
about the current platform, for platform-specific testing.  For example,
to determine whether wx-assertions are on or off.

There are currently three choices of platform: Windows, GTK, and Mac.
These may increase in the future.

The following are two use cases.
The second is preferred; may be deprecated.
    
    # Method 1:
    if wxtest.CURRENT_PLATFORM == wxtest.MAC:
        # mac-specific test
    if wxtest.CURRENT_PLATFORM != wxtest.WINDOWS:
        # test not to be run on windows
    
    # Method 2 (for convenience)
    if wxtest.PlatformIsMac():
        # mac-specific test
    if wxtest.PlatformIsNotWindows():
        # test not to be run on windows"""
        
import wx

# A poor attempt at enums
# TODO: how are enums implemented in Python?
WINDOWS = 100
GTK     = 200
MAC     = 300

# Determine current platform
CURRENT_PLATFORM = None
if 'wxMSW' in wx.PlatformInfo: # or '__WXMSW__'
    CURRENT_PLATFORM = WINDOWS
elif 'wxGTK' in wx.PlatformInfo: # or '__WXGTK__'
    CURRENT_PLATFORM = GTK
elif 'wxMac' in wx.PlatformInfo: # or '__WXMAC__'
    CURRENT_PLATFORM = MAC
else:
    raise EnvironmentError("Unknown platform!")


# Convenience methods

def PlatformIsWindows():
    return CURRENT_PLATFORM == WINDOWS

def PlatformIsGtk():
    return CURRENT_PLATFORM == GTK

def PlatformIsMac():
    return CURRENT_PLATFORM == MAC

def PlatformIsNotWindows():
    return CURRENT_PLATFORM != WINDOWS

def PlatformIsNotGtk():
    return CURRENT_PLATFORM != GTK

def PlatformIsNotMac():
    return CURRENT_PLATFORM != MAC

# -----------------------------------------------------------

SIZE         = 34
VIRTUAL_SIZE = 56
CLIENT_SIZE  = 78

# -----------------------------------------------------------

ASSERTIONS_ON  = None
ASSERTIONS_OFF = None

if 'wx-assertions-on' in wx.PlatformInfo:
    ASSERTIONS_ON  = True
    ASSERTIONS_OFF = False
elif 'wx-assertions-off' in wx.PlatformInfo:
    ASSERTIONS_ON  = False
    ASSERTIONS_OFF = True
else:
    raise EnvironmentError("Cannot determine wx-assertion status!")
