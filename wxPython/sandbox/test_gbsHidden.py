import wx
from test_gbsSpan import CPanel, TestPanel


class MyTestPanel(TestPanel):
    def MakeContent(self):
        gbs = self.gbs = wx.GridBagSizer(10,10)

        p1 = CPanel(self, 'pink', size=(100,100), name="one")
        p2 = CPanel(self, 'pink', size=(100,100), name="two")
        p3 = CPanel(self, 'pink', size=(100,100), name="three")
        p4 = CPanel(self, 'blue', size=(200,200), name="four")
        self.blue = p4
        btn = wx.Button(self, label="Hide Blue")

        self.Bind(wx.EVT_BUTTON, self.OnButton)
        
        gbs.Add(p1,  pos=(0,0))
        gbs.Add(p2,  pos=(0,2))
        gbs.Add(p3,  pos=(2,0))
        gbs.Add(btn, pos=(2,2))
        gbs.Add(p4,  pos=(1,1))
        

        box = wx.BoxSizer()
        box.Add(gbs, 1, wx.EXPAND|wx.ALL, 10)
        self.SetSizer(box)


    def OnButton(self, evt):
        shown = self.blue.IsShown()
        self.blue.Show(not shown)
        evt.GetEventObject().SetLabel(shown and "Show Blue" or "Hide Blue")
        self.Layout()
        self.Refresh()  # so the grid lines are redrawn



if __name__ == '__main__':
    app = wx.App(False)
    frm = wx.Frame(None, title="GBS hidden item test", size=(500, 500))
    pbl = MyTestPanel(frm, name="main")
    frm.Show()
    # import wx.lib.inspection
    # wx.lib.inspection.InspectionTool().Show()
    app.MainLoop()


