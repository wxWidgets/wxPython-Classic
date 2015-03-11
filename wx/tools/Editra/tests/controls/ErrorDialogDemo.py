###############################################################################
# Name: ErrorDialogDemo.py                                                    #
# Purpose: Test and demo file for eclib.ErrorDialog                           #
# Author: Cody Precord <cprecord@editra.org>                                  #
# Copyright: (c) 2009 Cody Precord <staff@editra.org>                         #
# Licence: wxWindows Licence                                                  #
###############################################################################

"""
Test file for testing the File InfoDialog.

"""

__author__ = "Cody Precord <cprecord@editra.org>"
__svnid__ = "$Id$"
__revision__ = "$Revision$"

#-----------------------------------------------------------------------------#
# Imports
import os
import sys
import wx

# Put local package on the path
#sys.path.insert(0, os.path.abspath('../../src'))
import eclib

#-----------------------------------------------------------------------------#

class TestErrorDialog(eclib.ErrorDialog):
    def __init__(self, msg):
        eclib.ErrorDialog.__init__(self, None, title="Error Report", message=msg)

        # Setup
        self.SetDescriptionLabel("Error: An Error has occured read below")

    def Abort(self):
        """Abort the application"""
        wx.MessageBox("Abort Clicked", "Abort Callback")
        TestErrorDialog.ABORT = False # HACK for testing to keep app from being aborted for real

    def GetProgramName(self):
        """Get the program name to display in error report"""
        return "ErrorDialog Demo"

    def Send(self):
        """Send the error report"""
        wx.MessageBox("Send Clicked", "Send Callback")

#-----------------------------------------------------------------------------#

def ExceptionHook(exctype, value, trace):
    """Handler for all unhandled exceptions
    @param exctype: Exception Type
    @param value: Error Value
    @param trace: Trace back info

    """
    # Format the traceback
    ftrace = TestErrorDialog.FormatTrace(exctype, value, trace)

    # Ensure that error gets raised to console as well
    print ftrace

    # If abort has been set and we get here again do a more forcefull shutdown
    if TestErrorDialog.ABORT:
        os._exit(1)

    # Prevent multiple reporter dialogs from opening at once
    if not TestErrorDialog.REPORTER_ACTIVE and not TestErrorDialog.ABORT:
        dlg = TestErrorDialog(ftrace)
        dlg.ShowModal()
        dlg.Destroy()

#-----------------------------------------------------------------------------#

class TestPanel(wx.Panel):
    def __init__(self, parent, log):
        wx.Panel.__init__(self, parent, wx.ID_ANY, size=(500,500))

        # Attributes
        self.exc = wx.Button(self, label="Raise Exception")
        self.log = log

        # Setup
        self._oldhook = sys.excepthook
        sys.excepthook = ExceptionHook

        # Layout
        self.__DoLayout()

        # Event Handers
        self.Bind(wx.EVT_BUTTON, self.OnButton, self.exc)

    def __del__(self):
        sys.excepthook = self._oldhook

    def __DoLayout(self):
        """Layout the panel"""
        vsizer = wx.BoxSizer(wx.VERTICAL)

        hsizer = wx.BoxSizer(wx.HORIZONTAL)
        hsizer.Add(self.exc, 0, wx.ALIGN_CENTER)

        vsizer.AddStretchSpacer()
        vsizer.Add(hsizer, 0, wx.ALIGN_CENTER)
        vsizer.AddStretchSpacer()

        self.SetSizer(vsizer)
        self.SetAutoLayout(True)

    def OnButton(self, evt):
        """Raise an exception to trigger the Error Dialog"""
        raise Exception("An error has occurred")

#----------------------------------------------------------------------

def runTest(frame, nb, log):
    win = TestPanel(nb, log)
    return win

class TestLog:
    def __init__(self):
        pass

    def write(self, msg):
        print msg

#----------------------------------------------------------------------

overview = eclib.errdlg.__doc__
title = "ErrorDialog"

#-----------------------------------------------------------------------------#
if __name__ == '__main__':
    try:
        import run
    except ImportError:
        app = wx.PySimpleApp(False)
        frame = wx.Frame(None, title="File Info Dialog Demo")
        sizer = wx.BoxSizer(wx.HORIZONTAL)
        sizer.Add(TestPanel(frame, TestLog()), 1, wx.EXPAND)
        frame.CreateStatusBar()
        frame.SetSizer(sizer)
        frame.SetInitialSize((300, 300))
        frame.Show()
        app.MainLoop()
    else:
        run.main(['', os.path.basename(sys.argv[0])] + sys.argv[1:])
