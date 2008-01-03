#----------------------------------------------------------------------
# Name:        wx.lib.embeddedimage
# Purpose:     Defines a class used for embedding PNG images in Python
#              code. The primary method of using this module is via
#              the code generator in wx.tools.img2py.
#
# Author:      Anthony Tuininga
#
# Created:     26-Nov-2007
# RCS-ID:      $Id$
# Copyright:   (c) 2007 by Anthony Tuininga
# Licence:     wxWindows license
#----------------------------------------------------------------------

import base64
import cStringIO
import wx

class PyEmbeddedImage(object):
    """
    Class for PNG images embedded in Python source files as base64 encoded
    text.
    """

    def __init__(self, data):
        self.data = data

    def GetBitmap(self):
        return wx.BitmapFromImage(self.GetImage())

    def GetData(self):
        return self.data

    def GetIcon(self):
        icon = wx.EmptyIcon()
        icon.CopyFromBitmap(self.GetBitmap())
        return icon

    def GetImage(self):
        data = base64.b64decode(self.data)
        stream = cStringIO.StringIO(data)
        return wx.ImageFromStream(stream)

    # added for backwards compatibility
    getBitmap = GetBitmap
    getData = GetData
    getIcon = GetIcon
    getImage = GetImage

    # define properties, for convenience
    Bitmap = property(GetBitmap)
    Icon = property(GetIcon)
    Image = property(GetImage)

