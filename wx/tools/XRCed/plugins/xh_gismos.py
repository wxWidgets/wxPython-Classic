# Name:         gizmos.py
# Purpose:      XML handlers for wx.gismos
# Author:       Roman Rolinsky <rolinsky@femagsoft.com>
# Created:      09.07.2007
# RCS-ID:       $Id$

import wx
import wx.xrc as xrc
import wx.gizmos as gizmos

# Resource handler class
class LEDNumberCtrlXmlHandler(xrc.XmlResourceHandler):
    def __init__(self):
        xrc.XmlResourceHandler.__init__(self)
        # Standard styles
        self.AddWindowStyles()
        # Custom styles
        self.AddStyle('wxLED_ALIGN_LEFT', gizmos.LED_ALIGN_LEFT)
        self.AddStyle('wxLED_ALIGN_RIGHT', gizmos.LED_ALIGN_RIGHT)
        self.AddStyle('wxLED_ALIGN_CENTER', gizmos.LED_ALIGN_CENTER)
        self.AddStyle('wxLED_DRAW_FADED', gizmos.LED_DRAW_FADED)
        
    def CanHandle(self,node):
        return self.IsOfClass(node, 'LEDNumberCtrl')

    # Process XML parameters and create the object
    def DoCreateResource(self):
        assert self.GetInstance() is None
        w = gizmos.LEDNumberCtrl(self.GetParentAsWindow(),
                                 self.GetID(),
                                 self.GetPosition(),
                                 self.GetSize(),
                                 self.GetStyle())
        # wxLED_ALIGN_MASK was incorrect
        align = self.GetStyle() & 7
        if align: w.SetAlignment(self.GetStyle() & 7)
        w.SetValue(self.GetText('value'))
        self.SetupWindow(w)
        return w
