# Name:         wxlib.py
# Purpose:      XML handlers for wx.lib classes
# Author:       Roman Rolinsky <rolinsky@femagsoft.com>
# Created:      05.09.2007
# RCS-ID:       $Id$

import wx
import wx.xrc as xrc
import wx.lib.foldpanelbar as fpb
from globals import TRACE

class FoldPanelBarXmlHandler(xrc.XmlResourceHandler):
    def __init__(self):
        xrc.XmlResourceHandler.__init__(self)
        # Standard styles
        self.AddWindowStyles()
        # Custom styles
        self.AddStyle('FPB_DEFAULT_STYLE', fpb.FPB_DEFAULT_STYLE)
        self.AddStyle('FPB_SINGLE_FOLD', fpb.FPB_SINGLE_FOLD)
        self.AddStyle('FPB_COLLAPSE_TO_BOTTOM', fpb.FPB_COLLAPSE_TO_BOTTOM)
        self.AddStyle('FPB_EXCLUSIVE_FOLD', fpb.FPB_EXCLUSIVE_FOLD)
        self.AddStyle('FPB_HORIZONTAL', fpb.FPB_HORIZONTAL)
        self.AddStyle('FPB_VERTICAL', fpb.FPB_VERTICAL)
        self.isInside = False
        
    def CanHandle(self,node):
        return not self.isInside and self.IsOfClass(node, 'FoldPanelBar') or \
               self.isInside and self.IsOfClass(node, 'foldpanel')

    # Process XML parameters and create the object
    def DoCreateResource(self):
        TRACE('DoCreateResource: %s', self.GetClass())
        if self.GetClass() == 'foldpanel':
            # !!! Never reached
            import pdb;pdb.set_trace()
            return
        w = fpb.FoldPanelBar(self.GetParentAsWindow(),
                             self.GetID(),
                             self.GetPosition(),
                             self.GetSize(),
                             self.GetStyle(),
                             self.GetStyle('exstyle'))
        self.SetupWindow(w)
        self.isInside = True
        self.CreateChildren(w, True)
        self.isInside = False
        return w

