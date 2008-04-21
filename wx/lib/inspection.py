#----------------------------------------------------------------------------
# Name:        wx.lib.inspection
# Purpose:     A widget inspection tool that allows easy introspection of
#              all the live widgets and sizers in an application.
#
# Author:      Robin Dunn
#
# Created:     26-Jan-2007
# RCS-ID:      $Id$
# Copyright:   (c) 2007 by Total Control Software
# Licence:     wxWindows license
#----------------------------------------------------------------------------

# NOTE: This class was originally based on ideas sent to the
# wxPython-users mail list by Dan Eloff.  See also
# wx.lib.mixins.inspect for a class that can be mixed-in with wx.App
# to provide Hot-Key access to the inspection tool.

import wx
import wx.py
import wx.stc
import wx.aui
import sys
import inspect

#----------------------------------------------------------------------------

class InspectionTool:
    """
    The InspectionTool is a singleton that manages creating and
    showing an InspectionFrame.
    """

    # Note: This is the Borg design pattern which ensures that all
    # instances of this class are actually using the same set of
    # instance data.  See
    # http://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/66531
    __shared_state = {}
    def __init__(self):
        self.__dict__ = self.__shared_state
        if not hasattr(self, 'initialized'):
            self.initialized = False

    def Init(self, pos=wx.DefaultPosition, size=wx.Size(850,700),
             config=None, locals=None, app=None):
        """
        Init is used to set some parameters that will be used later
        when the inspection tool is shown.  Suitable defaults will be
        used for all of these parameters if they are not provided.

        :param pos:   The default position to show the frame at
        :param size:  The default size of the frame
        :param config: A wx.Config object to be used to store layout
            and other info to when the inspection frame is closed.
            This info will be restored the next time the inspection
            frame is used.
        :param locals: A dictionary of names to be added to the PyCrust
            namespace.
        :param app:  A reference to the wx.App object.
        """
        self._frame = None
        self._pos = pos
        self._size = size
        self._config = config
        self._locals = locals
        self._app = app
        if not self._app:
            self._app = wx.GetApp()
        self.initialized = True
            
        
    def Show(self, selectObj=None, refreshTree=False):
        """
        Creates the inspection frame if it hasn't been already, and
        raises it if neccessary.  Pass a widget or sizer in selectObj
        to have that object be preselected in widget tree.  If
        refreshTree is True then the widget tree will be rebuilt,
        otherwise if the tree has already been built it will be left
        alone.
        """
        if not self.initialized:
            self.Init()

        parent = self._app.GetTopWindow()
        if not selectObj:
            selectObj = parent
        if not self._frame:
            self._frame = InspectionFrame( parent=parent,
                                           pos=self._pos,
                                           size=self._size,
                                           config=self._config,
                                           locals=self._locals,
                                           app=self._app)
        if selectObj:
            self._frame.SetObj(selectObj)
        if refreshTree:
            self._frame.RefreshTree()
        self._frame.Show()
        if self._frame.IsIconized():
            self._frame.Iconize(False)
        self._frame.Raise()

        
#----------------------------------------------------------------------------


class InspectionFrame(wx.Frame):
    """
    This class is the frame that holds the wxPython inspection tools.
    The toolbar and AUI splitters/floating panes are also managed
    here.  The contents of the tool windows are handled by other
    classes.
    """
    def __init__(self, wnd=None, locals=None, config=None,
                 app=None, title="wxPython Widget Inspection Tool",
                 *args, **kw):
        kw['title'] = title
        wx.Frame.__init__(self, *args, **kw)

        self.includeSizers = False
        self.started = False

        self.SetIcon(Icon.GetIcon())
        self.MakeToolBar()
        panel = wx.Panel(self, size=self.GetClientSize())
        
        # tell FrameManager to manage this frame        
        self.mgr = wx.aui.AuiManager(panel,
                                     wx.aui.AUI_MGR_DEFAULT
                                     | wx.aui.AUI_MGR_TRANSPARENT_DRAG
                                     | wx.aui.AUI_MGR_ALLOW_ACTIVE_PANE)

        # make the child tools        
        self.tree = InspectionTree(panel, size=(100,300))
        self.info = InspectionInfoPanel(panel,
                                        style=wx.NO_BORDER,
                                        )

        if not locals:
            locals = {}
        myIntroText = (
            "Python %s on %s, wxPython %s\n"
            "NOTE: The 'obj' variable refers to the object selected in the tree."
            % (sys.version.split()[0], sys.platform, wx.version()))
        self.crust = wx.py.crust.Crust(panel, locals=locals,
                                       intro=myIntroText,
                                       showInterpIntro=False,
                                       style=wx.NO_BORDER,
                                       )
        self.locals = self.crust.shell.interp.locals
        self.crust.shell.interp.introText = ''
        self.locals['obj'] = self.obj = wnd
        self.locals['app'] = app
        self.locals['wx'] = wx
        wx.CallAfter(self._postStartup)

        # put the chlid tools in AUI panes
        self.mgr.AddPane(self.info,
                         wx.aui.AuiPaneInfo().Name("info").Caption("Object Info").
                         CenterPane().CaptionVisible(True).
                         CloseButton(False).MaximizeButton(True)
                         )
        self.mgr.AddPane(self.tree,
                         wx.aui.AuiPaneInfo().Name("tree").Caption("Widget Tree").
                         CaptionVisible(True).Left().Dockable(True).Floatable(True).
                         BestSize((280,200)).CloseButton(False).MaximizeButton(True)
                         )
        self.mgr.AddPane(self.crust,
                         wx.aui.AuiPaneInfo().Name("crust").Caption("PyCrust").
                         CaptionVisible(True).Bottom().Dockable(True).Floatable(True).
                         BestSize((400,200)).CloseButton(False).MaximizeButton(True)
                         )

        self.mgr.Update()

        if config is None:
            config = wx.Config('wxpyinspector')
        self.config = config
        self.Bind(wx.EVT_CLOSE, self.OnClose)
        self.LoadSettings(self.config)
        self.crust.shell.lineNumbers = False
        self.crust.shell.setDisplayLineNumbers(False)
        self.crust.shell.SetMarginWidth(1, 0)
        

    def MakeToolBar(self):
        tbar = self.CreateToolBar(wx.TB_HORIZONTAL | wx.TB_FLAT | wx.TB_TEXT | wx.NO_BORDER )
        tbar.SetToolBitmapSize((24,24))

        refreshBmp = Refresh.GetBitmap()
        findWidgetBmp = Find.GetBitmap()
        showSizersBmp = ShowSizers.GetBitmap() 
        toggleFillingBmp = ShowFilling.GetBitmap()

        refreshTool = tbar.AddLabelTool(-1, 'Refresh', refreshBmp,
                                        shortHelp = 'Refresh widget tree')
        findWidgetTool = tbar.AddLabelTool(-1, 'Find', findWidgetBmp,
                                           shortHelp='Find new target widget.  Click here and\nthen on another widget in the app.')
        showSizersTool = tbar.AddLabelTool(-1, 'Sizers', showSizersBmp,
                                           shortHelp='Include sizers in widget tree',
                                           kind=wx.ITEM_CHECK)
        toggleFillingTool = tbar.AddLabelTool(-1, 'Filling', toggleFillingBmp,
                                              shortHelp='Show PyCrust \'filling\'',
                                              kind=wx.ITEM_CHECK)
        tbar.Realize()

        self.Bind(wx.EVT_TOOL,      self.OnRefreshTree,     refreshTool)
        self.Bind(wx.EVT_TOOL,      self.OnFindWidget,      findWidgetTool)
        self.Bind(wx.EVT_TOOL,      self.OnShowSizers,      showSizersTool)
        self.Bind(wx.EVT_TOOL,      self.OnToggleFilling,   toggleFillingTool)
        self.Bind(wx.EVT_UPDATE_UI, self.OnShowSizersUI,    showSizersTool)
        self.Bind(wx.EVT_UPDATE_UI, self.OnToggleFillingUI, toggleFillingTool)



    def _postStartup(self):
        if self.crust.ToolsShown():
            self.crust.ToggleTools()
        self.UpdateInfo()
        self.started = True


    def OnClose(self, evt):
        self.SaveSettings(self.config)
        self.mgr.UnInit()
        del self.mgr
        evt.Skip()
        

    def UpdateInfo(self):
        self.info.Update(self.obj)


    def SetObj(self, obj):
        if self.obj is obj:
            return
        self.locals['obj'] = self.obj = obj
        self.UpdateInfo()
        if not self.tree.built:
            self.tree.BuildTree(obj, includeSizers=self.includeSizers)
        else:
            self.tree.SelectObj(obj)


    def RefreshTree(self):
        self.tree.BuildTree(self.obj, includeSizers=self.includeSizers)


    def OnRefreshTree(self, evt):
        self.RefreshTree()
        self.UpdateInfo()
        

    def OnFindWidget(self, evt):
        self.Bind(wx.EVT_LEFT_DOWN, self.OnLeftDown)
        self.Bind(wx.EVT_MOUSE_CAPTURE_LOST, self.OnCaptureLost)
        self.CaptureMouse()
        self.finding = wx.BusyInfo("Click on any widget in the app...")


    def OnCaptureLost(self, evt):
        self.Unbind(wx.EVT_LEFT_DOWN)
        self.Unbind(wx.EVT_MOUSE_CAPTURE_LOST)
        del self.finding

    def OnLeftDown(self, evt):
        self.ReleaseMouse()
        wnd = wx.FindWindowAtPointer()
        if wnd is not None:
            self.SetObj(wnd)
        else:
            wx.Bell()
        self.OnCaptureLost(evt)


    def OnShowSizers(self, evt):
        self.includeSizers = not self.includeSizers
        self.RefreshTree()


    def OnToggleFilling(self, evt):
        self.crust.ToggleTools()


    def OnShowSizersUI(self, evt):
        evt.Check(self.includeSizers)


    def OnToggleFillingUI(self, evt):
        if self.started:
            evt.Check(self.crust.ToolsShown())


    def LoadSettings(self, config):
        self.crust.LoadSettings(config)
        self.info.LoadSettings(config)

        pos  = wx.Point(config.ReadInt('Window/PosX', -1),
                        config.ReadInt('Window/PosY', -1))
                        
        size = wx.Size(config.ReadInt('Window/Width', -1),
                       config.ReadInt('Window/Height', -1))
        self.SetSize(size)
        self.Move(pos)

        perspective = config.Read('perspective', '')
        if perspective:
            self.mgr.LoadPerspective(perspective)
        self.includeSizers = config.ReadBool('includeSizers', False)
            

    def SaveSettings(self, config):
        self.crust.SaveSettings(config)
        self.info.SaveSettings(config)

        if not self.IsIconized() and not self.IsMaximized():
            w, h = self.GetSize()
            config.WriteInt('Window/Width', w)
            config.WriteInt('Window/Height', h)
            
            px, py = self.GetPosition()
            config.WriteInt('Window/PosX', px)
            config.WriteInt('Window/PosY', py)

        perspective = self.mgr.SavePerspective()
        config.Write('perspective', perspective)
        config.WriteBool('includeSizers', self.includeSizers)
        
#---------------------------------------------------------------------------

# should inspection frame (and children) be includeed in the tree?
INCLUDE_INSPECTOR = True

USE_CUSTOMTREECTRL = False
if USE_CUSTOMTREECTRL:
    import wx.lib.customtreectrl as CT
    TreeBaseClass = CT.CustomTreeCtrl
else:
    TreeBaseClass = wx.TreeCtrl

class InspectionTree(TreeBaseClass):
    """
    All of the widgets in the app, and optionally their sizers, are
    loaded into this tree.
    """
    def __init__(self, *args, **kw):
        #s = kw.get('style', 0)
        #kw['style'] = s | wx.TR_DEFAULT_STYLE | wx.TR_HIDE_ROOT
        TreeBaseClass.__init__(self, *args, **kw)
        self.roots = []
        self.built = False
        self.Bind(wx.EVT_TREE_SEL_CHANGED, self.OnSelectionChanged)
        self.toolFrame = wx.GetTopLevelParent(self)
        if 'wxMac' in wx.PlatformInfo:
            self.SetWindowVariant(wx.WINDOW_VARIANT_SMALL)
        

    def BuildTree(self, startWidget, includeSizers=False):
        if self.GetCount():
            self.DeleteAllItems()
            self.roots = []
            self.built = False

        realRoot = self.AddRoot('Top-level Windows')

        for w in wx.GetTopLevelWindows():
            if w is wx.GetTopLevelParent(self) and not INCLUDE_INSPECTOR:
                continue
            root  = self._AddWidget(realRoot, w, includeSizers)
            self.roots.append(root)

        # Expand the subtree containing the startWidget, and select it.
        if not startWidget or not isinstance(startWidget, wx.Window):
            startWidget = wx.GetApp().GetTopWindow()
        top = wx.GetTopLevelParent(startWidget)
        topItem = self.FindWidgetItem(top)
        if topItem:
            self.ExpandAllChildren(topItem)
        self.SelectObj(startWidget)
        self.built = True


    def _AddWidget(self, parentItem, widget, includeSizers):
        text = self.GetTextForWidget(widget)
        item = self.AppendItem(parentItem, text)
        self.SetItemPyData(item, widget)

        # Add the sizer and widgets in the sizer, if we're showing them
        widgetsInSizer = []
        if includeSizers and widget.GetSizer() is not None:
            widgetsInSizer = self._AddSizer(item, widget.GetSizer())

        # Add any children not in the sizer, or all children if we're
        # not showing the sizers
        for child in widget.GetChildren():
            if not child in widgetsInSizer and not child.IsTopLevel():
                self._AddWidget(item, child, includeSizers)

        return item


    def _AddSizer(self, parentItem, sizer):
        widgets = []
        text = self.GetTextForSizer(sizer)
        item = self.AppendItem(parentItem, text)
        self.SetItemPyData(item, sizer)
        self.SetItemTextColour(item, "blue")

        for si in sizer.GetChildren():
            if si.IsWindow():
                w = si.GetWindow()
                self._AddWidget(item, w, True)
                widgets.append(w)
            elif si.IsSizer():
                widgets += self._AddSizer(item, si.GetSizer())
            else:
                i = self.AppendItem(item, "Spacer")
                self.SetItemPyData(i, si)
                self.SetItemTextColour(i, "blue")
        return widgets
    

    def FindWidgetItem(self, widget):
        """
        Find the tree item for a widget.
        """
        for item in self.roots:
            found = self._FindWidgetItem(widget, item)
            if found:
                return found
        return None

    def _FindWidgetItem(self, widget, item):
        if self.GetItemPyData(item) is widget:
            return item
        child, cookie = self.GetFirstChild(item)
        while child:
            found = self._FindWidgetItem(widget, child)
            if found:
                return found
            child, cookie = self.GetNextChild(item, cookie)
        return None


    def GetTextForWidget(self, widget):
        """
        Returns the string to be used in the tree for a widget
        """
        return "%s (\"%s\")" % (widget.__class__.__name__, widget.GetName())

    def GetTextForSizer(self, sizer):
        """
        Returns the string to be used in the tree for a sizer
        """
        return "%s" % sizer.__class__.__name__


    def SelectObj(self, obj):
        item = self.FindWidgetItem(obj)
        if item:
            self.EnsureVisible(item)
            self.SelectItem(item)


    def OnSelectionChanged(self, evt):
        obj = self.GetItemPyData(evt.GetItem())
        self.toolFrame.SetObj(obj)


#---------------------------------------------------------------------------

class InspectionInfoPanel(wx.stc.StyledTextCtrl):
    """
    Used to display information about the currently selected items.
    Currently just a read-only wx.stc.StyledTextCtrl with some plain
    text.  Should probably add some styles to make things easier to
    read.
    """
    def __init__(self, *args, **kw):
        wx.stc.StyledTextCtrl.__init__(self, *args, **kw)

        from wx.py.editwindow import FACES
        self.StyleSetSpec(wx.stc.STC_STYLE_DEFAULT,
                          "face:%(mono)s,size:%(size)d,back:%(backcol)s" % FACES)
        self.StyleClearAll()
        self.SetReadOnly(True)
        self.SetMarginType(1, 0)
        self.SetMarginWidth(1, 0)
        self.SetSelForeground(True, wx.SystemSettings.GetColour(wx.SYS_COLOUR_HIGHLIGHTTEXT))
        self.SetSelBackground(True, wx.SystemSettings.GetColour(wx.SYS_COLOUR_HIGHLIGHT))


    def LoadSettings(self, config):
        zoom = config.ReadInt('View/Zoom/Info', 0)
        self.SetZoom(zoom)

    def SaveSettings(self, config):
        config.WriteInt('View/Zoom/Info', self.GetZoom())
        

    def Update(self, obj):
        st = []
        if not obj:
            st.append("Item is None or has been destroyed.")

        elif isinstance(obj, wx.Window):
            st += self.FmtWidget(obj)
            
        elif isinstance(obj, wx.Sizer):
            st += self.FmtSizer(obj)

        elif isinstance(obj, wx.SizerItem):
            st += self.FmtSizerItem(obj)

        self.SetReadOnly(False)
        self.SetText('\n'.join(st))
        self.SetReadOnly(True)


    def Fmt(self, name, value):
        if isinstance(value, (str, unicode)):
            return "    %s = '%s'" % (name, value)
        else:
            return "    %s = %s" % (name, value)


    def FmtWidget(self, obj):
        st = ["Widget:"]
        st.append(self.Fmt('name',       obj.GetName()))
        st.append(self.Fmt('class',      obj.__class__))
        st.append(self.Fmt('bases',      obj.__class__.__bases__))
        st.append(self.Fmt('module',     inspect.getmodule(obj)))
        if hasattr(obj, 'this'):
            st.append(self.Fmt('this',      repr(obj.this)))
        st.append(self.Fmt('id',         obj.GetId()))
        st.append(self.Fmt('style',      obj.GetWindowStyle()))
        st.append(self.Fmt('pos',        obj.GetPosition()))
        st.append(self.Fmt('size',       obj.GetSize()))
        st.append(self.Fmt('minsize',    obj.GetMinSize()))
        st.append(self.Fmt('bestsize',   obj.GetBestSize()))
        st.append(self.Fmt('client size',obj.GetClientSize()))
        st.append(self.Fmt('IsEnabled',  obj.IsEnabled()))
        st.append(self.Fmt('IsShown',    obj.IsShown()))
        st.append(self.Fmt('fg color',   obj.GetForegroundColour()))
        st.append(self.Fmt('bg color',   obj.GetBackgroundColour()))
        st.append(self.Fmt('label',      obj.GetLabel()))
        if hasattr(obj, 'GetTitle'):
            st.append(self.Fmt('title',      obj.GetTitle()))
        if hasattr(obj, 'GetValue'):
            st.append(self.Fmt('value',      obj.GetValue()))
        if obj.GetContainingSizer() is not None:
            st.append('')
            sizer = obj.GetContainingSizer()
            st += self.FmtSizerItem(sizer.GetItem(obj))
        return st


    def FmtSizerItem(self, obj):
        if obj is None:
            return ['SizerItem: None']
        
        st = ['SizerItem:']
        st.append(self.Fmt('proportion', obj.GetProportion()))
        st.append(self.Fmt('flag',
                           FlagsFormatter(itemFlags, obj.GetFlag())))
        st.append(self.Fmt('border',     obj.GetBorder()))
        st.append(self.Fmt('pos',        obj.GetPosition()))
        st.append(self.Fmt('size',       obj.GetSize()))
        st.append(self.Fmt('minsize',    obj.GetMinSize()))
        st.append(self.Fmt('ratio',      obj.GetRatio()))
        st.append(self.Fmt('IsWindow',   obj.IsWindow()))
        st.append(self.Fmt('IsSizer',    obj.IsSizer()))
        st.append(self.Fmt('IsSpacer',   obj.IsSpacer()))
        st.append(self.Fmt('IsShown',    obj.IsShown()))
        if isinstance(obj, wx.GBSizerItem):
            st.append(self.Fmt('cellpos',    obj.GetPos()))
            st.append(self.Fmt('cellspan',   obj.GetSpan()))
            st.append(self.Fmt('endpos',     obj.GetEndPos()))
        return st


    def FmtSizer(self, obj):
        st = ['Sizer:']
        st.append(self.Fmt('class',      obj.__class__))
        if hasattr(obj, 'this'):
            st.append(self.Fmt('this',      repr(obj.this)))
        st.append(self.Fmt('pos',        obj.GetPosition()))
        st.append(self.Fmt('size',       obj.GetSize()))
        st.append(self.Fmt('minsize',    obj.GetMinSize()))
        if isinstance(obj, wx.BoxSizer):
            st.append(self.Fmt('orientation',
                               FlagsFormatter(orientFlags, obj.GetOrientation())))
        if isinstance(obj, wx.GridSizer):
            st.append(self.Fmt('cols', obj.GetCols()))
            st.append(self.Fmt('rows', obj.GetRows()))
            st.append(self.Fmt('vgap', obj.GetVGap()))
            st.append(self.Fmt('hgap', obj.GetHGap()))
        if isinstance(obj, wx.FlexGridSizer):
            st.append(self.Fmt('rowheights', obj.GetRowHeights()))
            st.append(self.Fmt('colwidths', obj.GetColWidths()))
            st.append(self.Fmt('flexdir',
                               FlagsFormatter(orientFlags, obj.GetFlexibleDirection())))
            st.append(self.Fmt('nonflexmode',
                               FlagsFormatter(flexmodeFlags, obj.GetNonFlexibleGrowMode())))
        if isinstance(obj, wx.GridBagSizer):
            st.append(self.Fmt('emptycell', obj.GetEmptyCellSize()))
            
        if obj.GetContainingWindow():
            si = obj.GetContainingWindow().GetSizer().GetItem(obj)
            if si:
                st.append('')
                st += self.FmtSizerItem(si)
        return st


class FlagsFormatter(object):
    def __init__(self, d, val):
        self.d = d
        self.val = val
        
    def __str__(self):
        st = []
        for k in self.d.keys():
            if self.val & k:
                st.append(self.d[k])
        if st:
            return '|'.join(st)
        else:
            return '0'

orientFlags = {
    wx.HORIZONTAL : 'wx.HORIZONTAL',
    wx.VERTICAL : 'wx.VERTICAL',
    }

itemFlags = {
    wx.TOP : 'wx.TOP',
    wx.BOTTOM : 'wx.BOTTOM',
    wx.LEFT : 'wx.LEFT',
    wx.RIGHT : 'wx.RIGHT',
#    wx.ALL : 'wx.ALL',
    wx.EXPAND : 'wx.EXPAND',
#    wx.GROW : 'wx.GROW',
    wx.SHAPED : 'wx.SHAPED',
    wx.STRETCH_NOT : 'wx.STRETCH_NOT',
    wx.ALIGN_CENTER : 'wx.ALIGN_CENTER',
    wx.ALIGN_LEFT : 'wx.ALIGN_LEFT',
    wx.ALIGN_RIGHT : 'wx.ALIGN_RIGHT',
    wx.ALIGN_TOP : 'wx.ALIGN_TOP',
    wx.ALIGN_BOTTOM : 'wx.ALIGN_BOTTOM',
    wx.ALIGN_CENTER_VERTICAL : 'wx.ALIGN_CENTER_VERTICAL',
    wx.ALIGN_CENTER_HORIZONTAL : 'wx.ALIGN_CENTER_HORIZONTAL',
    wx.ADJUST_MINSIZE : 'wx.ADJUST_MINSIZE',
    wx.FIXED_MINSIZE : 'wx.FIXED_MINSIZE',
    }

flexmodeFlags = {
    wx.FLEX_GROWMODE_NONE : 'wx.FLEX_GROWMODE_NONE',
    wx.FLEX_GROWMODE_SPECIFIED : 'wx.FLEX_GROWMODE_SPECIFIED',
    wx.FLEX_GROWMODE_ALL : 'wx.FLEX_GROWMODE_ALL',
    }

#---------------------------------------------------------------------------
from wx.lib.embeddedimage import PyEmbeddedImage

Refresh = PyEmbeddedImage(
    "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"
    "GXlKb/xX4wAAAABJRU5ErkJggg==")

Find = PyEmbeddedImage(
    "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")

ShowSizers = PyEmbeddedImage(
    "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAABHNCSVQICAgIfAhkiAAABChJ"
    "REFUSIm1lU1oXFUUx3/33nn3zbx5mcm0M5OZxGlNAn6XUqlRKIIWKrXqRlCLOwvitrooqKDg"
    "RhcirkSpigSECl0WBa104UKoSIoLS8TWlja1NTOTyUzz5s37uNdFWpumJSktHriry//8zj38"
    "z7nwP4dY5/7BUqn0quu62621i9cJhSjGcTzTarUOAr/dFn1sbGy/N+SdksgoQ2bh2mFBQpTz"
    "vdP1ev3AWjkya10qpe4yPbPZ3GeUecEMswQoYK4I3w+wzWiz3qgbtw0AQoHoswWfNxyYLYE2"
    "8GcVfr8IzU5gjOnfCWA5YuCvHPw0CRkLhGDjW5LeGiAFWjGcaYKyUHLAwvoeWQcgpczZjM3z"
    "A3CiD5fPAlikFXRicNy8lNJbK4das/A0VdKVJd/4oWqJZhSGVcJUeH3n5JA/NGe1OhEG/W+i"
    "KJq9LUAURe1KuVJQrrqnn4YVrXXkOE5gFCpf8NteLvdts9k8AgRXJDf0bC1ArlgsTiVJsqfX"
    "6+1K03RQLpenfd//tdvtbh0MBvdaaxe01pcGg8FFlq1wU8jNoqiUeq5Wqx3SWlutdWvTpk3v"
    "ANuBbY1G423Xdecdx7EjIyOHlVLPA6X1kl4lK6XU7rGxsU+UUkue54XlcvlL4LEVL36kUql8"
    "ns/nl6SUwejo6EGl1DNcM81/r7ihRfl8fmehUHil2Wzu1Vr3Xdc9lCTJZ4PB4DhXzAlcAOa0"
    "1koIMdntdqdKpZInhGjHcXx6ZT4FjDQajR21Wm2L7/sPJ0nyYr/ff1ZKOV8ul2eTJDnS6XSO"
    "sjwN4mp1cRw3s9lssVQq1cIwVEmSbNVa+9VqNTsyMjLh+/744uJiT3ied8BxnJcx6QMS0wkH"
    "UaEfJe6w4mc8v5AINWOS+KMgCGZWVuZ53taMlPtRaqovTRAv9LaTdQIn5y0oYzZkkaejOJ6m"
    "Xq8fk0IkCGVxci2UnsfNz1MatSDtUN7rT0xMvLa6lePj4/v8wlAfsCVUuJFMZxh1eQMqyIFF"
    "irRerx/LGGMCYa3ioV1f8el30/w4k8V178bNfMjHL3mcPREA0U1MES3ZNK2R6Z9katpgkpBU"
    "jFLovcnJRz8QF54wxgTXVoUQl9iBzz/bniQlT39JIdecQywICfEwQwFkd4KqdAmDS8gKEMLK"
    "XZTaOVImsbyOpM1QXiPkmgBAZBApeOEsS5OSjD8gJYsG6AFkhBA5C3D6+G72vudTGYXg8gYQ"
    "0J6DDB4sK67LLISjhXQ6xLm3+OXxU6RuBGxEM0sPLFkhRC5jjDmntD5D2N4jDr8LsMCV+bCQ"
    "t8Xhs0mStFYD4jhu55B/LEpx//vi/A5gieWdJLBoV+m2MeacAJ6uVqt7pZQNa+11v5MQohAE"
    "wdFut/sFcH4VY9T3/X2+7z9lre2t0mXTNP17fn7+6/V6fMfxL1klnkaQRVDaAAAAAElFTkSu"
    "QmCC")

ShowFilling = PyEmbeddedImage(
    "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAABHNCSVQICAgIfAhkiAAAAZ5J"
    "REFUSIntlc9KAkEcxz+tu7OxLRSuGUXtIfUpukW9QJcO3nqELoLXLr2Bt47dRBAqgxJ6BqMw"
    "PJe0FEliaLNrFxV1zXatY9/TMDPf72eG3/yBf/2guaH2DrALrADtGfME8AKUgCsAdWhwX1XV"
    "bSnlMtCZEaApivrqeXJxEmBDSrl+dHQoNjf3OD9/xjSDJ5vmMre3Z1xeHi8AG/3+YcAH8GEY"
    "SbG6uoVtP2IYwQFLS2s8PT0MciYBALi5uUfTrrEsB88LDtB1C027A+h+N6cAvBUK+e6surg4"
    "6wLvvSwAlHFKu/0ZfNkBvD6AEGJmwCSvrwaNRgOAZrMZKtw0zYF3KiCXy1Eul2m1WqEAhmFQ"
    "q9VgrMg+QKVSoVqt4oU5QoCiKHQ6/vvpA2QyGdLpNPV6PRQgHo+Tz+fJZrPTAYlEgmQyiW3b"
    "oQBCCFKpFIy+b36ArusDQ1j1vCM18B3TaDQaOrgvy7Jgyg7mgflisQiA4zihwmOxGKVSCUDv"
    "ZTFOO/mL5zoSiby6rnsFHMDoDk6llA6//HBc1+1/OP8Kpi8497f1tG0HzQAAAABJRU5ErkJg"
    "gg==")

Icon = PyEmbeddedImage(
    "iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAYAAABzenr0AAAABHNCSVQICAgIfAhkiAAAALhJ"
    "REFUWIXtl80SgyAMhHeR99Y+eJseLAdHbJM0TjiwN2dI+MgfQpYFmSqpu0+AEQDqrwXyeorH"
    "McvCEIBdm3F7/fr0FKgBRFaIrHkAdykdQFmEGm2HL233BAIAYmxYEqjePo9SBYBvBKppclDz"
    "prMcqAhbAtknJx+3AKRHgGhnv4iApQY+jtSWpOY27BnifNt5uyk9BekAoZNwl21yDBSBi/63"
    "yOMiLAXaf8AuwP9n94vzaTYBsgHeht4lXXmb7yQAAAAASUVORK5CYII=")

