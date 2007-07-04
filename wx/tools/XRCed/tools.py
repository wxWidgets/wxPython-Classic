# Name:         tools.py
# Purpose:      XRC editor, toolbar
# Author:       Roman Rolinsky <rolinsky@mema.ucl.ac.be>
# Created:      19.03.2003
# RCS-ID:       $Id$

#from wx.lib import buttons
from globals import *
from component import Manager
import images

# Tool panel
class ToolPanel(wx.Panel):
    TOOL_SIZE = (30, 30)
    def __init__(self, parent):
        if wx.Platform == '__WXGTK__':
            wx.Panel.__init__(self, parent, -1,
                             style=wx.RAISED_BORDER|wx.WANTS_CHARS)
        else:
            wx.Panel.__init__(self, parent, -1, style=wx.WANTS_CHARS)
        # Create sizer for groups
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        # Data to create buttons
        self.groups = []
#        self.ctrl = self.shift = False
        # Current state (what to enable/disable)
#        self.state = None
        self.boxes = {}
        for panel in Manager.panelNames:
            panelData = Manager.panels.get(panel, None)
            if not panelData: continue
            self.AddGroup(panel)
            for index,comp,image in panelData:
                self.AddButton(comp.id, image, comp.klass)
        self.SetSizerAndFit(self.sizer)
        # Allow to be resized in vertical direction only
        self.SetSizeHints(self.GetSize()[0], -1)
        # Events
#        wx.EVT_COMMAND_RANGE(self, ID_NEW.PANEL, ID_NEW.LAST,
#                             wx.wxEVT_COMMAND_BUTTON_CLICKED, g.frame.OnCreate)
#        wx.EVT_KEY_DOWN(self, self.OnKeyDown)
#        wx.EVT_KEY_UP(self, self.OnKeyUp)
        # wxMSW does not generate click events for StaticBox
 #       if wx.Platform == '__WXMSW__':
 #           self.Bind(wx.EVT_LEFT_DOWN, self.OnClickBox)
        self.drag = None

    def AddButton(self, id, bmp, text):
        button = wx.BitmapButton(self, id, bmp, 
                                 style=wx.NO_BORDER|wx.WANTS_CHARS)
#        button = buttons.GenBitmapButton(self, id, image, size=self.TOOL_SIZE,
#                                         style=wx.NO_BORDER|wx.WANTS_CHARS)
#        button.SetBezelWidth(0)
#        wx.EVT_KEY_DOWN(button, self.OnKeyDown)
#        wx.EVT_KEY_UP(button, self.OnKeyUp)
#        wx.EVT_LEFT_DOWN(button, self.OnLeftDownOnButton)
#        wx.EVT_MOTION(button, self.OnMotionOnButton)
        button.SetToolTipString(text)
        self.curSizer.Add(button)
        self.groups[-1][1][id] = button

    def AddGroup(self, name):
        # Each group is inside box
        id = wx.NewId()
        box = wx.StaticBox(self, id, '[+] '+name, style=wx.WANTS_CHARS)
        box.SetForegroundColour(wx.Colour(64, 64, 64))
#        box.SetFont(g.smallerFont())
        box.show = True
        box.name = name
        box.gnum = len(self.groups)
        box.Bind(wx.EVT_LEFT_DOWN, self.OnClickBox)
        boxSizer = wx.StaticBoxSizer(box, wx.VERTICAL)
        boxSizer.Add((0, 0))
        self.boxes[id] = box
        self.curSizer = wx.GridSizer(0, 3, 3, 3)
        boxSizer.Add(self.curSizer)
        self.sizer.Add(boxSizer, 0, wx.TOP | wx.LEFT | wx.RIGHT | wx.EXPAND, 4)
        self.groups.append((box,{}))

    # Enable/disable group
    def EnableGroup(self, gnum, enable = True):
        grp = self.groups[gnum]
        for b in grp[1].values(): b.Enable(enable)

    # Show/hide group
    def ShowGroup(self, gnum, show = True):
        grp = self.groups[gnum]
        grp[0].show = show
        for b in grp[1].values(): b.Show(show)

    # Enable/disable group item
    def EnableGroupItem(self, gnum, id, enable = True):
        grp = self.groups[gnum]
        grp[1][id].Enable(enable)

    # Enable/disable group items
    def EnableGroupItems(self, gnum, ids, enable = True):
        grp = self.groups[gnum]
        for id in ids:
            grp[1][id].Enable(enable)

    def OnClickBox(self, evt):
        if wx.Platform == '__WXMSW__':
            box = None
            for id,b in self.boxes.items():
                # How to detect a click on a label?
                if b.GetRect().Inside(evt.GetPosition()):
                    box = b
                    break
            if not box: 
                evt.Skip()
                return
        else:
            box = self.boxes[evt.GetId()]
        # Collapse/restore static box, change label
        self.ShowGroup(box.gnum, not box.show)
        if box.show: box.SetLabel('[+] ' + box.name)
        else: box.SetLabel('[-] ' + box.name)
        self.Layout()
        self.Refresh()
        #for b in self.boxes.items():

    # DaD
    def OnLeftDownOnButton(self, evt):
        self.posDown = evt.GetPosition()
        self.idDown = evt.GetId()
        self.btnDown = evt.GetEventObject()
        evt.Skip()

    def OnMotionOnButton(self, evt):
        # Detect dragging
        if evt.Dragging() and evt.LeftIsDown():
            d = evt.GetPosition() - self.posDown
            if max(abs(d[0]), abs(d[1])) >= 5:
                if self.btnDown.HasCapture(): 
                    # Generate up event to release mouse
                    evt = wx.MouseEvent(wx.EVT_LEFT_UP.typeId)
                    evt.SetId(self.idDown)
                    # Set flag to prevent normal button operation this time
                    self.drag = True
                    self.btnDown.ProcessEvent(evt)
                self.StartDrag()
        evt.Skip()

    def StartDrag(self):
        do = MyDataObject()
        do.SetData(str(self.idDown))
        bm = self.btnDown.GetBitmapLabel()
        # wxGTK requires wxIcon cursor, wxWIN and wxMAC require wxCursor
        if wx.Platform == '__WXGTK__':
            icon = wx.EmptyIcon()
            icon.CopyFromBitmap(bm)
            dragSource = wx.DropSource(self, icon)
        else:
            curs = wx.CursorFromImage(wx.ImageFromBitmap(bm))
            dragSource = wx.DropSource(self, curs)
        dragSource.SetData(do)
        g.frame.SetStatusText('Release the mouse button over the test window')
        dragSource.DoDragDrop()

    # Process key events
    def OnKeyDown(self, evt):
        if evt.GetKeyCode() == wx.WXK_CONTROL:
            g.tree.ctrl = True
        elif evt.GetKeyCode() == wx.WXK_SHIFT:
            g.tree.shift = True
        self.UpdateIfNeeded()
        evt.Skip()

    def OnKeyUp(self, evt):
        if evt.GetKeyCode() == wx.WXK_CONTROL:
            g.tree.ctrl = False
        elif evt.GetKeyCode() == wx.WXK_SHIFT:
            g.tree.shift = False
        self.UpdateIfNeeded()
        evt.Skip()

    def OnMouse(self, evt):
        # Update control and shift states
        g.tree.ctrl = evt.ControlDown()
        g.tree.shift = evt.ShiftDown()
        self.UpdateIfNeeded()
        evt.Skip()

    # Update UI after key presses, if necessary
    def UpdateIfNeeded(self):
        tree = g.tree
        if self.ctrl != tree.ctrl or self.shift != tree.shift:
            # Enabling is needed only for ctrl
            if self.ctrl != tree.ctrl: self.UpdateUI()
            self.ctrl = tree.ctrl
            self.shift = tree.shift
            if tree.ctrl:
                status = 'SBL'
            elif tree.shift:
                status = 'INS'
            else:
                status = ''
            g.frame.SetStatusText(status, 1)

