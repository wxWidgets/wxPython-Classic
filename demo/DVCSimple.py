
import wx
import wx.dataview as dv

#----------------------------------------------------------------------

class TestModel(dv.PyDataViewIndexListModel):
    def __init__(self):
        dv.PyDataViewIndexListModel.__init__(self, 5)
        
    def GetValue(self, row, col):
        #print 'GetValue:', row, col
        return "%d, %d" % (row, col)

    def SetValue(self, value, row, col):
        print 'SetValue:', value, row, col

    def GetColumnCount(self):
        print 'GetColumnCount'
        return 5

    def GetColumnType(self, col):
        print 'GetColumnType:', col
        return "string"

    

class TestPanel(wx.Panel):
    def __init__(self, parent, log):
        self.log = log
        wx.Panel.__init__(self, parent, -1)

        self.dv = dv.DataViewCtrl(self)#, style=wx.BORDER_THEME)
        self.model = TestModel()
        self.dv.AssociateModel(self.model)
        self.dv.AppendTextColumn("zero", 0)
        #self.dv.AppendTextColumn("one", 1)
        self.dv.AppendTextColumn("two", 2, mode=dv.DATAVIEW_CELL_EDITABLE)
        #self.dv.AppendTextColumn("three", 3, mode=dv.DATAVIEW_CELL_EDITABLE)
        self.dv.AppendTextColumn("four", 4, mode=dv.DATAVIEW_CELL_EDITABLE)
        
        self.Sizer = wx.BoxSizer()  # use the Sizer property (same as SetSizer)
        self.Sizer.Add(self.dv, 1, wx.EXPAND)
        


#----------------------------------------------------------------------

def runTest(frame, nb, log):
    win = TestPanel(nb, log)
    return win

#----------------------------------------------------------------------



overview = """<html><body>
<h2><center>DataViewCtrl</center></h2>

</body></html>
"""



if __name__ == '__main__':
    import sys,os
    import run
    run.main(['', os.path.basename(sys.argv[0])] + sys.argv[1:])

