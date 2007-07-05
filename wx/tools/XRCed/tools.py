# Name:         tools.py
# Purpose:      XRC editor, toolbar
# Author:       Roman Rolinsky <rolinsky@mema.ucl.ac.be>
# Created:      19.03.2003
# RCS-ID:       $Id$

from globals import *
from component import Manager
import view
import images

class ToolPanel(wx.Panel):
    '''Manages a Listbook with tool bitmap buttons.'''
    def __init__(self, parent):
        if wx.Platform == '__WXGTK__':
            wx.Panel.__init__(self, parent, -1,
                             style=wx.RAISED_BORDER|wx.WANTS_CHARS)
        else:
            wx.Panel.__init__(self, parent, -1, style=wx.WANTS_CHARS)
        # Top sizer
        sizer = wx.BoxSizer(wx.VERTICAL)
        # Listbook
        self.lb = wx.Toolbook(self, -1, style=wx.BK_TOP)
        sizer.Add(self.lb, 1, wx.EXPAND)
        self.panels = []
        # Image list
        il = wx.ImageList(48, 48, True)
        # Default Id 0
        il.Add(images.getToolPanel_DefaultImage().ConvertToBitmap())
        self.il = il
        self.lb.AssignImageList(il)
#        self.ctrl = self.shift = False
        # Current state (what to enable/disable)
#        self.state = None
        for name in Manager.panelNames:
            panelData = Manager.getPanelData(name)
            if not panelData: continue
            try:
                im = Manager.panelImages[name]
                imageId = il.Add(im.Scale(48, 48).ConvertToBitmap())
            except:
                imageId = 0
            panel = self.AddPanel(name, imageId)
            for index,comp,image in panelData:
                self.AddButton(panel, comp.id, image, comp.klass)
            panel.Layout()
        self.SetSizerAndFit(sizer)
        # Allow to be resized in horizontal direction only
        self.SetSizeHints(-1, self.GetSize()[1])
        # Events
#        wx.EVT_COMMAND_RANGE(self, ID_NEW.PANEL, ID_NEW.LAST,
#                             wx.wxEVT_COMMAND_BUTTON_CLICKED, g.frame.OnCreate)
#        wx.EVT_KEY_DOWN(self, self.OnKeyDown)
#        wx.EVT_KEY_UP(self, self.OnKeyUp)
        # wxMSW does not generate click events for StaticBox
 #       if wx.Platform == '__WXMSW__':
 #           self.Bind(wx.EVT_LEFT_DOWN, self.OnClickBox)
        self.drag = None

    def AddButton(self, panel, id, bmp, text):
        button = wx.BitmapButton(panel, id, bmp, 
                                 style=wx.NO_BORDER|wx.WANTS_CHARS)
#        button = buttons.GenBitmapButton(self, id, image, size=self.TOOL_SIZE,
#                                         style=wx.NO_BORDER|wx.WANTS_CHARS)
#        button.SetBezelWidth(0)
#        wx.EVT_KEY_DOWN(button, self.OnKeyDown)
#        wx.EVT_KEY_UP(button, self.OnKeyUp)
#        button.Bind(wx.EVT_BUTTON, self.OnButton)
#        wx.EVT_MOTION(button, self.OnMotionOnButton)
        button.SetToolTipString(text)
        panel.sizer.Add(button, 0, wx.ALIGN_CENTRE)
        panel.controls[id] = button

    def AddPanel(self, name, imageId):
        # Each group is inside box
        panel = wx.Panel(self.lb)
        panel.SetBackgroundColour(wx.Colour(115, 180, 215))
        panel.name = name
        panel.gnum = len(self.panels)
        panel.controls = {}
        panel.sizer = wx.FlexGridSizer(0, 3, 5, 5)
        panel.SetSizer(panel.sizer)
        self.lb.AddPage(panel, '', imageId=imageId)
        self.panels.append(panel)
        return panel

    # DnD
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

