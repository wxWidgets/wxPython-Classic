
import sys, time, math, os, os.path

import wx
_ = wx.GetTranslation
import wx.propgrid as wxpg


############################################################################
#
# TEST RELATED CODE AND VARIABLES
#
############################################################################

default_object_content2 = """\
object.title = "Object Title"
object.index = 1
object.PI = %f
object.wxpython_rules = True
"""%(math.pi)

default_object_content1 = """\

#
# Note that the results of autofill will appear on the second page.

#
# Set number of iterations appropriately to test performance
iterations = 100

#
# Test result for 100,000 iterations on Athlon XP 2000+:
#
# Time spent per property: 0.054ms
# Memory allocated per property: ~350 bytes (includes Python object)
#

for i in range(0,iterations):
    setattr(object,'title%i'%i,"Object Title")
    setattr(object,'index%i'%i,1)
    setattr(object,'PI%i'%i,3.14)
    setattr(object,'wxpython_rules%i'%i,True)
"""


############################################################################
#
# CUSTOM PROPERTY SAMPLES
#
############################################################################


class ValueObject:
    def __init__(self):
        pass


class IntProperty2(wxpg.PyProperty):
    """\
    This is a simple re-implementation of wxIntProperty.
    """
    def __init__(self, label, name = wxpg.LABEL_AS_NAME, value=0):
        wxpg.PyProperty.__init__(self, label, name)
        self.SetValue(value)

    def GetClassName(self):
        """\
        This is not 100% necessary and in future is probably going to be
        automated to return class name.
        """
        return "IntProperty2"

    def GetEditor(self):
        return "TextCtrl"

    def ValueToString(self, value, flags):
        return str(value)

    def StringToValue(self, s, flags):
        try:
            v = int(s)
            if self.GetValue() != v:
                return v
        except TypeError:
            if flags & wxpg.PG_REPORT_ERROR:
                wx.MessageBox("Cannot convert '%s' into a number."%s, "Error")
        return False

    def IntToValue(self, v, flags):
        if (self.GetValue() != v):
            return v


class SizeProperty(wxpg.PyProperty):
    """ Demonstrates a property with few children.
    """
    def __init__(self, label, name = wxpg.LABEL_AS_NAME, value=wx.Size(0, 0)):
        wxpg.PyProperty.__init__(self, label, name)

        value = self._ConvertValue(value)

        self.AddPrivateChild( wxpg.IntProperty("X", value=value.x) )
        self.AddPrivateChild( wxpg.IntProperty("Y", value=value.y) )

        self.m_value = value

    def GetClassName(self):
        return self.__class__.__name__

    def GetEditor(self):
        return "TextCtrl"

    def RefreshChildren(self):
        size = self.m_value
        self.Item(0).SetValue( size.x )
        self.Item(1).SetValue( size.y )

    def _ConvertValue(self, value):
        """ Utility convert arbitrary value to a real wx.Size.
        """
        from operator import isSequenceType
        if isinstance(value, wx.Point):
            value = wx.Size(value.x, value.y)
        elif isSequenceType(value):
            value = wx.Size(*value)
        return value

    def ChildChanged(self, thisValue, childIndex, childValue):
        # FIXME: This does not work yet. ChildChanged needs be fixed "for"
        #        wxPython in wxWidgets SVN trunk, and that has to wait for
        #        2.9.1, as wxPython 2.9.0 uses WX_2_9_0_BRANCH.
        size = self._ConvertValue(self.m_value)
        if childIndex == 0:
            size.x = childValue
        elif childIndex == 1:
            size.y = childValue
        else:
            raise AssertionError

        return size


class DirsProperty(wxpg.PyArrayStringProperty):
    """ Sample of a custom custom ArrayStringProperty.

        Because currently some of the C++ helpers from wxArrayStringProperty
        and wxProperytGrid are not available, our implementation has to quite
        a bit 'manually'. Which is not too bad since Python has excellent
        string and list manipulation facilities.
    """
    def __init__(self, label, name = wxpg.LABEL_AS_NAME, value=[]):
        wxpg.PyArrayStringProperty.__init__(self, label, name, value)

        # Set default delimiter
        self.SetAttribute("Delimiter", ',')

    def GetEditor(self):
        return "TextCtrlAndButton"

    def ValueToString(self, value, flags):
        return self.m_display

    def OnSetValue(self):
        self.GenerateValueAsString()

    def DoSetAttribute(self, name, value):
        # Proper way to call same method from super class
        retval = self.CallSuperMethod("DoSetAttribute", name, value)

        #
        # Must re-generate cached string when delimiter changes
        if name == "Delimiter":
            self.GenerateValueAsString(delim=value)

        return retval

    def GenerateValueAsString(self, delim=None):
        """ This function creates a cached version of displayed text
            (self.m_display).
        """
        if not delim:
            delim = self.GetAttribute("Delimiter")
            if not delim:
                delim = ','

        ls = self.GetValue()
        if delim == '"' or delim == "'":
            text = ' '.join(['%s%s%s'%(delim,a,delim) for a in ls])
        else:
            text = ', '.join(ls)
        self.m_display = text

    def StringToValue(self, text, argFlags):
        delim = self.GetAttribute("Delimiter")
        if delim == '"' or delim == "'":
            # Proper way to call same method from super class
            return self.CallSuperMethod("StringToValue", text, 0)
        return [a.strip() for a in text.split(delim)]

    def OnEvent(self, propgrid, primaryEditor, event):
        if event.GetEventType() == wx.wxEVT_COMMAND_BUTTON_CLICKED:
            dlg = wx.DirDialog(propgrid,
                               _("Select a directory to be added to "
                                 "the list:"))

            if dlg.ShowModal() == wx.ID_OK:
                new_path = dlg.GetPath();
                old_value = self.m_value
                if old_value:
                    new_value = list(old_value)
                    new_value.append(new_path)
                else:
                    new_value = [new_path]
                self.SetValueInEvent(new_value)
                retval = True
            else:
                retval = False

            dlg.Destroy()
            return retval

        return False


class PyObjectPropertyValue:
    """\
    Value type of our sample PyObjectProperty. We keep a simple dash-delimited
    list of string given as argument to constructor.
    """
    def __init__(self, s=None):
        try:
            self.ls = [a.strip() for a in s.split('-')]
        except:
            self.ls = []

    def __repr__(self):
        return ' - '.join(self.ls)


class PyObjectProperty(wxpg.PyProperty):
    """\
    Another simple example. This time our value is a PyObject.

    NOTE: We can't return an arbitrary python object in DoGetValue. It cannot
          be a simple type such as int, bool, double, or string, nor an array
          or wxObject based. Dictionary, None, or any user-specified Python
          class is allowed.
    """
    def __init__(self, label, name = wxpg.LABEL_AS_NAME, value=None):
        wxpg.PyProperty.__init__(self, label, name)
        self.SetValue(value)

    def GetClassName(self):
        return self.__class__.__name__

    def GetEditor(self):
        return "TextCtrl"

    def ValueToString(self, value, flags):
        return repr(value)

    def StringToValue(self, s, flags):
        return PyObjectPropertyValue(s)


############################################################################
#
# MAIN PROPERTY GRID TEST PANEL
#
############################################################################

class TestPanel( wx.Panel ):
    def __init__( self, parent, log ):
        wx.Panel.__init__(self, parent, wx.ID_ANY)
        self.log = log

        self.panel = panel = wx.Panel(self, wx.ID_ANY)
        topsizer = wx.BoxSizer(wx.VERTICAL)

        # Difference between using PropertyGridManager vs PropertyGrid is that
        # the manager supports multiple pages and a description box.
        self.pg = pg = wxpg.PropertyGridManager(panel,
                        style=wxpg.PG_SPLITTER_AUTO_CENTER |
                              wxpg.PG_AUTO_SORT |
                              wxpg.PG_TOOLBAR)

        # Show help as tooltips
        pg.SetExtraStyle(wxpg.PG_EX_HELP_AS_TOOLTIPS)

        pg.Bind( wxpg.EVT_PG_CHANGED, self.OnPropGridChange )
        pg.Bind( wxpg.EVT_PG_PAGE_CHANGED, self.OnPropGridPageChange )
        pg.Bind( wxpg.EVT_PG_SELECTED, self.OnPropGridSelect )
        pg.Bind( wxpg.EVT_PG_RIGHT_CLICK, self.OnPropGridRightClick )

        # Needed by custom image editor
        wx.InitAllImageHandlers()

        #
        # Let's create a simple custome editor
        #
        # NOTE: Editor must be registered *before* adding a property that
        #       uses it.
        try:
            pg.RegisterEditor(LargeImageEditor)
        except:
            # Editor may have already been registered (demo related issue)
            pass

        #
        # Add properties
        #

        pg.AddPage( "Page 1 - Testing All" )

        pg.Append( wxpg.PropertyCategory("1 - Basic Properties") )
        pg.Append( wxpg.StringProperty("String",value="Some Text") )
        pg.Append( wxpg.IntProperty("Int",value=100) )
        pg.Append( wxpg.FloatProperty("Float",value=100.0) )
        pg.Append( wxpg.BoolProperty("Bool",value=True) )
        pg.Append( wxpg.BoolProperty("Bool_with_Checkbox",value=True) )
        pg.SetPropertyAttribute("Bool_with_Checkbox", "UseCheckbox", True)

        pg.Append( wxpg.PropertyCategory("2 - More Properties") )
        pg.Append( wxpg.LongStringProperty("LongString",
            value="This is a\\nmulti-line string\\nwith\\ttabs\\nmixed\\tin."))
        pg.Append( wxpg.DirProperty("Dir",value="C:\\Windows") )
        pg.Append( wxpg.FileProperty("File",value="C:\\Windows\\system.ini") )
        pg.Append( wxpg.ArrayStringProperty("ArrayString",value=['A','B','C']) )

        pg.Append( wxpg.EnumProperty("Enum","Enum",
                                     ['wxPython Rules',
                                      'wxPython Rocks',
                                      'wxPython Is The Best'],
                                     [10,11,12],
                                     0) )
        pg.Append( wxpg.EditEnumProperty("EditEnum","EditEnumProperty",
                                         ['A','B','C'],
                                         [0,1,2],
                                         "Text Not in List") )

        pg.Append( wxpg.PropertyCategory("3 - Advanced Properties") )
        pg.Append( wxpg.DateProperty("Date",value=wx.DateTime_Now()) )
        pg.Append( wxpg.FontProperty("Font",value=panel.GetFont()) )
        pg.Append( wxpg.ColourProperty("Colour",
                                       value=panel.GetBackgroundColour()) )
        pg.Append( wxpg.SystemColourProperty("SystemColour") )
        pg.Append( wxpg.ImageFileProperty("ImageFile") )
        pg.Append( wxpg.MultiChoiceProperty("MultiChoice",
                    choices=['wxWidgets','QT','GTK+']) )

        pg.Append( wxpg.PropertyCategory("4 - Additional Properties") )
        #pg.Append( wxpg.PointProperty("Point",value=panel.GetPosition()) )
        #pg.Append( SizeProperty("Size",value=panel.GetSize()) )
        #pg.Append( wxpg.FontDataProperty("FontData") )
        pg.Append( wxpg.IntProperty("IntWithSpin",value=256) )
        pg.SetPropertyEditor("IntWithSpin","SpinCtrl")
        pg.Append( DirsProperty("Dirs1",value=['C:/Lib','C:/Bin']) )
        pg.Append( DirsProperty("Dirs2",value=['/lib','/bin']) )

        # Test another type of delimiter
        pg.SetPropertyAttribute("Dirs2", "Delimiter", '"')

        pg.SetPropertyAttribute( "File", wxpg.PG_FILE_SHOW_FULL_PATH, 0 )
        pg.SetPropertyAttribute( "File", wxpg.PG_FILE_INITIAL_PATH,
                                 "C:\\Program Files\\Internet Explorer" )
        pg.SetPropertyAttribute( "Date", wxpg.PG_DATE_PICKER_STYLE,
                                 wx.DP_DROPDOWN|wx.DP_SHOWCENTURY )

        pg.Append( wxpg.PropertyCategory("5 - Custom Properties") )
        pg.Append( IntProperty2("IntProperty2", value=1024) )

        pg.Append( PyObjectProperty("PyObjectProperty") )

        # When page is added, it will become the target page for AutoFill
        # calls (and for other property insertion methods as well)
        pg.AddPage( "Page 2 - Results of AutoFill will appear here" )

        pg.SetPropertyClientData( "Bool", 1234 )
        if pg.GetPropertyClientData( "Bool" ) != 1234:
            raise ValueError("Set/GetPropertyClientData() failed")

        # Test setting unicode string
        pg.GetPropertyByName("String").SetValue(u"Some Unicode Text")

        #
        # Test some code that *should* fail (but not crash)
        try:
            if wx.GetApp().GetAssertionMode() == wx.PYAPP_ASSERT_EXCEPTION:
                a_ = pg.GetPropertyValue( "NotARealProperty" )
                pg.EnableProperty( "NotAtAllRealProperty", False )
                pg.SetPropertyHelpString( "AgaintNotARealProperty", "Dummy Help String" )
        except:
            pass
            #raise
        topsizer.Add(pg, 1, wx.EXPAND)

        rowsizer = wx.BoxSizer(wx.HORIZONTAL)
        but = wx.Button(panel,-1,"SetPropertyValues")
        but.Bind( wx.EVT_BUTTON, self.OnSetPropertyValues )
        rowsizer.Add(but,1)
        but = wx.Button(panel,-1,"GetPropertyValues")
        but.Bind( wx.EVT_BUTTON, self.OnGetPropertyValues )
        rowsizer.Add(but,1)
        topsizer.Add(rowsizer,0,wx.EXPAND)
        rowsizer = wx.BoxSizer(wx.HORIZONTAL)
        but = wx.Button(panel,-1,"GetPropertyValues(as_strings=True)")
        but.Bind( wx.EVT_BUTTON, self.OnGetPropertyValues2 )
        rowsizer.Add(but,1)
        but = wx.Button(panel,-1,"AutoFill")
        but.Bind( wx.EVT_BUTTON, self.OnAutoFill )
        rowsizer.Add(but,1)
        topsizer.Add(rowsizer,0,wx.EXPAND)
        rowsizer = wx.BoxSizer(wx.HORIZONTAL)
        but = wx.Button(panel,-1,"Delete")
        but.Bind( wx.EVT_BUTTON, self.OnDeleteProperty )
        rowsizer.Add(but,1)
        but = wx.Button(panel,-1,"Run Tests")
        but.Bind( wx.EVT_BUTTON, self.RunTests )
        rowsizer.Add(but,1)
        topsizer.Add(rowsizer,0,wx.EXPAND)

        panel.SetSizer(topsizer)
        topsizer.SetSizeHints(panel)

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(panel, 1, wx.EXPAND)
        self.SetSizer(sizer)
        self.SetAutoLayout(True)

    def OnPropGridChange(self, event):
        p = event.GetProperty()
        if p:
            self.log.write('%s changed to "%s"\n' % (p.GetName(),p.GetValueAsString()))

    def OnPropGridSelect(self, event):
        p = event.GetProperty()
        if p:
            self.log.write('%s selected\n' % (event.GetProperty().GetName()))
        else:
            self.log.write('Nothing selected\n')

    def OnDeleteProperty(self, event):
        p = self.pg.GetSelectedProperty()
        if p:
            self.pg.DeleteProperty(p)
        else:
            wx.MessageBox("First select a property to delete")

    def OnReserved(self, event):
        pass

    def OnSetPropertyValues(self,event):
        try:
            d = self.pg.GetPropertyValues(inc_attributes=True)

            ss = []
            for k,v in d.iteritems():
                v = repr(v)
                if not v or v[0] != '<':
                    if k.startswith('@'):
                        ss.append('setattr(obj, "%s", %s)'%(k,v))
                    else:
                        ss.append('obj.%s = %s'%(k,v))

            dlg = MemoDialog(self,
                    "Enter Content for Object Used in SetPropertyValues",
                    '\n'.join(ss))  # default_object_content1

            if dlg.ShowModal() == wx.ID_OK:
                import datetime
                sandbox = {'obj':ValueObject(),
                           'wx':wx,
                           'datetime':datetime}
                exec dlg.tc.GetValue() in sandbox
                t_start = time.time()
                #print(sandbox['obj'].__dict__)
                self.pg.SetPropertyValues(sandbox['obj'])
                t_end = time.time()
                self.log.write('SetPropertyValues finished in %.0fms\n' %
                               ((t_end-t_start)*1000.0))
        except:
            import traceback
            traceback.print_exc()

    def OnGetPropertyValues(self,event):
        try:
            t_start = time.time()
            d = self.pg.GetPropertyValues(inc_attributes=True)
            t_end = time.time()
            self.log.write('GetPropertyValues finished in %.0fms\n' %
                           ((t_end-t_start)*1000.0))
            ss = ['%s: %s'%(k,repr(v)) for k,v in d.iteritems()]
            dlg = MemoDialog(self,"GetPropertyValues Result",
                             'Contents of resulting dictionary:\n\n'+'\n'.join(ss))
            dlg.ShowModal()
        except:
            import traceback
            traceback.print_exc()

    def OnGetPropertyValues2(self,event):
        try:
            t_start = time.time()
            d = self.pg.GetPropertyValues(as_strings=True)
            t_end = time.time()
            self.log.write('GetPropertyValues(as_strings=True) finished in %.0fms\n' %
                           ((t_end-t_start)*1000.0))
            ss = ['%s: %s'%(k,repr(v)) for k,v in d.iteritems()]
            dlg = MemoDialog(self,"GetPropertyValues Result",
                             'Contents of resulting dictionary:\n\n'+'\n'.join(ss))
            dlg.ShowModal()
        except:
            import traceback
            traceback.print_exc()

    def OnAutoFill(self,event):
        try:
            dlg = MemoDialog(self,"Enter Content for Object Used for AutoFill",default_object_content1)
            if dlg.ShowModal() == wx.ID_OK:
                sandbox = {'object':ValueObject(),'wx':wx}
                exec dlg.tc.GetValue() in sandbox
                t_start = time.time()
                self.pg.AutoFill(sandbox['object'])
                t_end = time.time()
                self.log.write('AutoFill finished in %.0fms\n' %
                               ((t_end-t_start)*1000.0))
        except:
            import traceback
            traceback.print_exc()

    def OnPropGridRightClick(self, event):
        p = event.GetProperty()
        if p:
            self.log.write('%s right clicked\n' % (event.GetProperty().GetName()))
        else:
            self.log.write('Nothing right clicked\n')

    def OnPropGridPageChange(self, event):
        index = self.pg.GetSelectedPage()
        self.log.write('Page Changed to \'%s\'\n' % (self.pg.GetPageName(index)))

    def RunTests(self, event):
        pg = self.pg

        # Iterator

        it = pg.GetPage(0).GetIterator(wxpg.PG_ITERATE_ALL)
        while not it.AtEnd():
            self.log.write('Iterating \'%s\'\n' % (it.GetProperty().GetName()))
            it.Next()

        # VIterator

        it = pg.GetVIterator(wxpg.PG_ITERATE_ALL)
        while not it.AtEnd():
            self.log.write('Iterating \'%s\'\n' % (it.GetProperty().GetName()))
            it.Next()


#---------------------------------------------------------------------------


class MemoDialog(wx.Dialog):
    """\
    Dialog for multi-line text editing.
    """
    def __init__(self,parent=None,title="",text="",pos=None,size=(500,500)):
        wx.Dialog.__init__(self,parent,-1,title,style=wx.DEFAULT_DIALOG_STYLE|wx.RESIZE_BORDER)

        topsizer = wx.BoxSizer( wx.VERTICAL )

        tc = wx.TextCtrl(self,11,text,style=wx.TE_MULTILINE)
        self.tc = tc
        topsizer.Add(tc,1,wx.EXPAND|wx.ALL,8)

        rowsizer = wx.BoxSizer( wx.HORIZONTAL )
        rowsizer.Add(wx.Button(self,wx.ID_OK,'Ok'),0,wx.ALIGN_RIGHT|wx.ALIGN_CENTRE_VERTICAL,8)
        rowsizer.Add((0,0),1,wx.ALIGN_RIGHT|wx.ALIGN_CENTRE_VERTICAL,8)
        rowsizer.Add(wx.Button(self,wx.ID_CANCEL,'Cancel'),0,wx.ALIGN_RIGHT|wx.ALIGN_CENTRE_VERTICAL,8)
        topsizer.Add(rowsizer,0,wx.EXPAND|wx.ALL,8)

        self.SetSizer( topsizer )
        topsizer.Layout()

        self.SetSize( size )
        if not pos:
            self.CenterOnScreen()
        else:
            self.Move(pos)

#----------------------------------------------------------------------

def runTest( frame, nb, log ):
    win = TestPanel( nb, log )
    return win

#----------------------------------------------------------------------


overview = """\
<html><body>
<P>
This demo shows all basic wxPropertyGrid properties, in addition to
some custom property classes.
</body></html>
"""



if __name__ == '__main__':
    import sys,os
    import run
    run.main(['', os.path.basename(sys.argv[0])] + sys.argv[1:])

