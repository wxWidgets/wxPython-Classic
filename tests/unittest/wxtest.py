import wx

"""
The wxtest module is used for common code across the wx Test Suite.

Its major use is to provide a standard means of determining the current
platform, for platform-specific testing.  There are currently three choices
of platform: Windows, GTK, and Mac.  These may increase in the future.

The two use case types are as follows (the second is preferred):
    
    # Method 1:
    if wxtest.CURRENT_PLATFORM == wxtest.MAC:
        # mac-specific test
    if wxtest.CURRENT_PLATFORM != wxtest.WINDOWS:
        # test not to be run on windows
    
    # Method 2 (for convenience)
    if wxtest.PlatformIsMac():
        # mac-specific test
    if wxtest.PlatformIsNotWindows():
        # test not to be run on windows
"""

# A poor attempt at enums
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
