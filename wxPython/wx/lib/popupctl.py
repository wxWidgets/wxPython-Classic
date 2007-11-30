#----------------------------------------------------------------------
# Name:         popup
# Purpose:      Generic popup control
#
# Author:       Gerrit van Dyk
#
# Created:      2002/11/20
# Version:      0.1
# RCS-ID:       $Id$
# License:      wxWindows license
#----------------------------------------------------------------------
# 11/24/2007 - Cody Precord
#
# o Use RendererNative to draw button
#
# 12/09/2003 - Jeff Grimmett (grimmtooth@softhome.net)
#
# o 2.5 compatability update.
#
# 12/20/2003 - Jeff Grimmett (grimmtooth@softhome.net)
#
# o wxPopupDialog -> PopupDialog
# o wxPopupControl -> PopupControl
#

import  wx
from wx.lib.buttons import GenButtonEvent


class PopButton(wx.PyControl):
    def __init__(self,*_args,**_kwargs):
        apply(wx.PyControl.__init__,(self,) + _args,_kwargs)

        self.up = True
        self.didDown = False

        self.Bind(wx.EVT_LEFT_DOWN, self.OnLeftDown)
        self.Bind(wx.EVT_LEFT_UP, self.OnLeftUp)
        self.Bind(wx.EVT_MOTION, self.OnMotion)
        self.Bind(wx.EVT_PAINT, self.OnPaint)

    def Notify(self):
        evt = GenButtonEvent(wx.wxEVT_COMMAND_BUTTON_CLICKED, self.GetId())
        evt.SetIsDown(not self.up)
        evt.SetButtonObj(self)
        evt.SetEventObject(self)
        self.GetEventHandler().ProcessEvent(evt)

    def OnEraseBackground(self, event):
        pass

    def OnLeftDown(self, event):
        if not self.IsEnabled():
            return
        self.didDown = True
        self.up = False
        self.CaptureMouse()
        self.GetParent().textCtrl.SetFocus()
        self.Refresh()
        event.Skip()

    def OnLeftUp(self, event):
        if not self.IsEnabled():
            return
        if self.didDown:
            self.ReleaseMouse()
            if not self.up:
                self.Notify()
            self.up = True
            self.Refresh()
            self.didDown = False
        event.Skip()

    def OnMotion(self, event):
        if not self.IsEnabled():
            return
        if event.LeftIsDown():
            if self.didDown:
                x,y = event.GetPosition()
                w,h = self.GetClientSize()
                if self.up and x<w and x>=0 and y<h and y>=0:
                    self.up = False
                    self.Refresh()
                    return
                if not self.up and (x<0 or y<0 or x>=w or y>=h):
                    self.up = True
                    self.Refresh()
                    return
        event.Skip()

    def OnPaint(self, event):
        dc = wx.BufferedPaintDC(self)
        if self.up:
            flag = wx.CONTROL_CURRENT
        else:
            flag = wx.CONTROL_PRESSED
        wx.RendererNative.Get().DrawComboBoxDropButton(self, dc, self.GetClientRect(), flag)

#---------------------------------------------------------------------------


# Tried to use wxPopupWindow but the control misbehaves on MSW
class PopupDialog(wx.Dialog):
    def __init__(self,parent,content = None):
        wx.Dialog.__init__(self,parent,-1,'', style = wx.BORDER_SIMPLE|wx.STAY_ON_TOP)

        self.ctrl = parent
        self.win = wx.Window(self,-1,pos = (0,0),style = 0)

        if content:
            self.SetContent(content)

    def SetContent(self,content):
        self.content = content
        self.content.Reparent(self.win)
        self.content.Show(True)
        self.win.SetClientSize(self.content.GetSize())
        self.SetSize(self.win.GetSize())

    def Display(self):
        pos = self.ctrl.ClientToScreen( (0,0) )
        dSize = wx.GetDisplaySize()
        selfSize = self.GetSize()
        tcSize = self.ctrl.GetSize()

        pos.x -= (selfSize.width - tcSize.width) / 2
        if pos.x + selfSize.width > dSize.width:
            pos.x = dSize.width - selfSize.width
        if pos.x < 0:
            pos.x = 0

        pos.y += tcSize.height
        if pos.y + selfSize.height > dSize.height:
            pos.y = dSize.height - selfSize.height
        if pos.y < 0:
            pos.y = 0

        self.Move(pos)

        self.ctrl.FormatContent()

        self.ShowModal()


#---------------------------------------------------------------------------


class PopupControl(wx.PyControl):
    def __init__(self,*_args,**_kwargs):
        if _kwargs.has_key('value'):
            del _kwargs['value']
        apply(wx.PyControl.__init__,(self,) + _args,_kwargs)

        self.textCtrl = wx.TextCtrl(self, wx.ID_ANY, '', pos = (0,0))
        self.bCtrl = PopButton(self, wx.ID_ANY)
        self.pop = None
        self.content = None
        self.OnSize(None)

        self.Bind(wx.EVT_SIZE, self.OnSize)
        self.bCtrl.Bind(wx.EVT_BUTTON, self.OnButton, self.bCtrl)
        # embedded control should get focus on TAB keypress
        self.Bind(wx.EVT_SET_FOCUS, self.OnFocus)

    def OnFocus(self,evt):
        self.textCtrl.SetFocus()
        evt.Skip()

    def OnSize(self,evt):
        w,h = self.GetClientSize()
        self.textCtrl.SetDimensions(0,0,w-24,h)
        self.bCtrl.SetDimensions(w-20, 0, 20, h)

    def OnButton(self,evt):
        if not self.pop:
            if self.content:
                self.pop = PopupDialog(self,self.content)
                del self.content
            else:
                print 'No Content to pop'
        if self.pop:
            self.pop.Display()

    def Enable(self,flag):
        wx.PyControl.Enable(self,flag)
        self.textCtrl.Enable(flag)
        self.bCtrl.Enable(flag)

    def SetPopupContent(self,content):
        if not self.pop:
            self.content = content
            self.content.Show(False)
        else:
            self.pop.SetContent(content)

    def FormatContent(self):
        pass

    def PopDown(self):
        if self.pop:
            self.pop.EndModal(1)

    def SetValue(self,value):
        self.textCtrl.SetValue(value)

    def GetValue(self):
        return self.textCtrl.GetValue()


# an alias
PopupCtrl = PopupControl
