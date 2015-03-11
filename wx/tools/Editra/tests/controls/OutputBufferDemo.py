###############################################################################
# Name: OutputBufferDemo.py                                                   #
# Purpose: OutputBuffer Test and Demo File                                    #
# Author: Cody Precord <cprecord@editra.org>                                  #
# Copyright: (c) 2008 Cody Precord <staff@editra.org>                         #
# License: wxWindows License                                                  #
###############################################################################

"""
Test file for testing the OutputBuffer (eclib.eclib) module and controls. This
demo/test contains a small application for running 'ping' and other command line
commands and then displaying their output. Special text styling is provided for
ping to highlight and create hotspot regions on IP and website addresses.

Clicking the start button multiple times will spawn multiple processes and
threads to interact with the buffer.


"""

__author__ = "Cody Precord <cprecord@editra.org>"
__svnid__ = "$Id$"
__revision__ = "$Revision$"

#-----------------------------------------------------------------------------#
# Imports
import os
import sys
import re
import wx

#sys.path.insert(0, os.path.abspath('../../src'))
import eclib

#-----------------------------------------------------------------------------#
# Globals

ID_COMMAND = wx.NewId()
ID_START = wx.NewId()
ID_STOP = wx.NewId()
ID_PROC_LIST = wx.NewId()
ID_THREAD_STATUS = wx.NewId()
#-----------------------------------------------------------------------------#

class TestPanel(wx.Panel):
    def __init__(self, parent, log):
        self.log = log
        wx.Panel.__init__(self, parent)

        # Attributes
        self.ssizer = wx.BoxSizer(wx.HORIZONTAL)
        self._buff = ProcessOutputBuffer(self, self.log)

        # Layout
        self.__DoLayout()

        # Event Handlers
        self.Bind(wx.EVT_BUTTON, self.OnButton)

    def __DoLayout(self):
        """Layout the panel"""

        # Status Display Layout (Top Section)
        self.ssizer.AddMany([((5, 5),),
                             (wx.StaticText(self, label="Running:"),
                              0, wx.ALIGN_CENTER_VERTICAL),
                             (wx.Choice(self, ID_PROC_LIST), 0),
                             ((-1, 5), 1, wx.EXPAND),
                             (wx.StaticText(self, ID_THREAD_STATUS, "Threads: 0"),
                              0, wx.ALIGN_CENTER_VERTICAL),
                             ((5, 5),)])

        default = ["ping localhost", "ping editra.org", "ping wxpython.org"]
        combo = wx.ComboBox(self, ID_COMMAND, value='ping localhost', choices=default)
        combo.SetToolTipString("Enter a command to run here")
        hsizer = wx.BoxSizer(wx.HORIZONTAL)
        stopb = wx.Button(self, ID_STOP, "Stop")
        stopb.SetToolTipString("Stop all running processes")
        startb = wx.Button(self, ID_START, "Start")
        startb.SetToolTipString("Run the command in the combo box\n"
                                "Press multiple times to start multiple threads")
        hsizer.AddMany([((5, 5),), (wx.StaticText(self, label="Cmd: "), 0,
                                    wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_LEFT),
                        (combo, 1, wx.EXPAND), ((20, 20),),
                        (stopb, 0, wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL),
                        ((5, 5),),
                        (startb, 0, wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL),
                        ((5, 5),)])

        # Main Sizer Layout
        msizer = wx.BoxSizer(wx.VERTICAL)
        msizer.AddMany([((3, 3),),
                        (self.ssizer, 0, wx.EXPAND),
                        (self._buff, 1, wx.EXPAND),
                        (hsizer, 0, wx.EXPAND)])
        self.SetSizer(msizer)

    def OnButton(self, evt):
        """Start/Stop ProcessThread(s)"""
        e_id = evt.GetId()
        if e_id == ID_STOP:
            self._buff.Abort()
            self.UpdateProcs()
        elif e_id == ID_START:
            # Spawn a new ProcessThread
            combo = self.FindWindowById(ID_COMMAND)
            self._buff.StartProcess(u'%s' % combo.GetValue())
            self.UpdateProcs()
        else:
            evt.Skip()

    def UpdateProcs(self):
        """Update the controls to show the current processes/threads"""
        procs = self.FindWindowById(ID_PROC_LIST)
        status = self.FindWindowById(ID_THREAD_STATUS)

        running = self._buff.GetProcesses()
        procs.SetItems(running)
        if len(running):
            procs.SetStringSelection(running[-1])
        status.SetLabel("Threads: %d" % len(running))
        self.ssizer.Layout()

#-----------------------------------------------------------------------------#
STARTED_STR = 'ProcessThread Started'
FINISHED_STR = 'ProcessThread Finished'

class ProcessOutputBuffer(eclib.OutputBuffer, eclib.ProcessBufferMixin):
    """Custom output buffer for processing output from running ping"""
    RE_ADDR = re.compile(r' ([a-z0-9]+\.[a-z0-9]+\.{0,1})+')
    ADDRESS_STYLE = eclib.OPB_STYLE_MAX + 1

    def __init__(self, parent, log):
        eclib.OutputBuffer.__init__(self, parent)
        eclib.ProcessBufferMixin.__init__(self, update=125)

        # Attributes
        self.log = log
        self._threads = list()

        # Setup a custom style for highlighting IP addresses
        font = self.GetFont()
        style = (font.GetFaceName(), font.GetPointSize(), "#FFFFFF")
        self.StyleSetSpec(ProcessOutputBuffer.ADDRESS_STYLE, 
                          "face:%s,size:%d,fore:#3030FF,back:%s" % style)
        self.StyleSetHotSpot(ProcessOutputBuffer.ADDRESS_STYLE, True)

    def Abort(self):
        """Kill off all running threads and procesess"""
        for proc in self._threads:
            proc[0].Abort()

    def ApplyStyles(self, ind, txt):
        """Highlight the begining and process exit text in the buffer
        Tests overriding of the ApplyStyles method from L{eclib.OutputBuffer}
        This is called every time text is added to the output buffer.
        @param ind: Index of text insertion point in buffer
        @param txt: the text that was just inserted at ind

        """
        # Highlight ip addresses
        for group in ProcessOutputBuffer.RE_ADDR.finditer(txt):
            sty_s = ind + group.start() + 1 # start past whitespace
            sty_e = ind + group.end()
            self.StartStyling(sty_s, 0xff)
            self.SetStyling(sty_e - sty_s, ProcessOutputBuffer.ADDRESS_STYLE)

        # Check for first/last messages
        start = txt.find(STARTED_STR)
        end = txt.find(FINISHED_STR)
        if start >= 0:
            sty_s = ind + start
            slen = len(STARTED_STR)
            style = eclib.OPB_STYLE_INFO
        elif end >= 0:
            sty_s = ind + end
            slen = len(FINISHED_STR)
            style = eclib.OPB_STYLE_WARN
        else:
            return

        # Do the styling if one of the patterns was found
        self.StartStyling(sty_s, 0xff)
        self.SetStyling(slen, style)

    def DoHotSpotClicked(self, pos, line):
        """Overridden method from base L{eclib.OutputBuffer} class.
        This method is called whenever a hotspot in the output buffer is
        clicked on.
        @param pos: Click postion in buffer
        @param line: Line click occurred on

        """
        self.log.write("Hotspot Clicked: Pos %d, Line %d" % (pos, line))
        if self.GetStyleAt(pos) == ProcessOutputBuffer.ADDRESS_STYLE:
            ipaddr = ProcessOutputBuffer.RE_ADDR.search(self.GetLine(line))
            if ipaddr is not None:
                ipaddr = ipaddr.group(0)
                self.log.write("Address Clicked: %s" % ipaddr)

    def DoProcessStart(self, cmd=''):
        """Do any necessary preprocessing before a process is started.
        This method is called directly before the process in the
        L{eclib.ProcessThread} is started. This method is an overridden 
        method of the L{eclib.ProcessBufferMixin} super class.
        @keyword cmd: Command string used to start the process

        """
        self.AppendUpdate("%s: %s%s" % (STARTED_STR, cmd, os.linesep))

    def DoProcessExit(self, code=0):
        """Do all that is needed to be done after a process has exited
        This method is called when a L{eclib.ProcessThread} has exited and
        is an overridden method from the L{eclib.ProcessBufferMixin} super
        class.
        @keyword code: Exit code of the process

        """
        self.AppendUpdate("%s: %d%s" % (FINISHED_STR, code, os.linesep))
        dead = list()

        # Remove all Dead Threads
        for idx, proc in enumerate(self._threads):
            if not proc[0].isAlive():
                dead.append(idx)

        for zombie in reversed(dead):
            del self._threads[zombie]

        self.GetParent().UpdateProcs()

        # If there are no more running threads stop the buffers timer
        if not len(self._threads):
            self.Stop()

    def GetActiveCount(self):
        """Get the count of active threaded processes that are running
        @return: int

        """
        return len(self._threads)

    def GetProcesses(self):
        """Return the list of running process commands
        @return: list of strings

        """
        return [ proc[1] for proc in self._threads ]

    def StartProcess(self, cmd):
        """Start a new process thread, the process will be created by
        executing the given command.
        @param cmd: Command string (i.e 'ping localhost')

        """
        proc = eclib.ProcessThread(self, cmd, env=os.environ)
        self._threads.append((proc, cmd))
        self._threads[-1][0].start()
        
#-----------------------------------------------------------------------------#

def runTest(frame, nb, log):
    return TestPanel(nb, log)

class TestLog:
    def __init__(self):
        pass

    def write(self, msg):
        print msg

#----------------------------------------------------------------------

overview = eclib.outbuff.__doc__
title = "OutputBuffer"

#-----------------------------------------------------------------------------#
# Run the Test
if __name__ == '__main__':
    try:
        import run
    except ImportError:
        app = wx.PySimpleApp(False)
        frame = wx.Frame(None, title="OutputBuffer Test 'Ping-O-Matic'")
        sizer = wx.BoxSizer(wx.HORIZONTAL)
        sizer.Add(TestPanel(frame, TestLog()), 1, wx.EXPAND)
        frame.CreateStatusBar()
        frame.SetSizer(sizer)
        frame.SetInitialSize((500, 500))
        frame.SetStatusText("OutputBufferDemo: wxPython %s, Python %s" % \
                            (wx.__version__, u".".join(str(x) for x in sys.version_info)))
        frame.CenterOnParent()
        frame.Show()
        app.MainLoop()
    else:
        run.main(['', os.path.basename(sys.argv[0])] + sys.argv[1:])
