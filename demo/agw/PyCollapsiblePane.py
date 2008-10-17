import wx
import wx.lib.buttons as buttons
import cStringIO

import os
import sys

try:
    dirName = os.path.dirname(os.path.abspath(__file__))
except:
    dirName = os.path.dirname(os.path.abspath(sys.argv[0]))

sys.path.append(os.path.split(dirName)[0])

try:
    from agw import pycollapsiblepane as PCP
except ImportError: # if it's not there locally, try the wxPython lib.
    import wx.lib.agw.pycollapsiblepane as PCP

import images

btnlbl1 = "call Expand(True)"
btnlbl2 = "call Expand(False)"

choices = ["wx.Button", "GenButton", "GenBitmapButton", "GenBitmapTextButton", "GTK Expander"]
gtkChoices = ["3, 6", "4, 8", "5, 10"]


class PyCollapsiblePaneDemo(wx.Panel):

    def __init__(self, parent, log):

        wx.Panel.__init__(self, parent)

        self.log = log
        
        self.label1 = "Click here to show pane"
        self.label2 = "Click here to hide pane"

        title = wx.StaticText(self, label="PyCollapsiblePane")
        title.SetFont(wx.Font(18, wx.SWISS, wx.NORMAL, wx.BOLD))
        title.SetForegroundColour("blue")

        self.cp = cp = PCP.PyCollapsiblePane(self, label=self.label1,
                                             style=wx.CP_DEFAULT_STYLE|wx.CP_NO_TLW_RESIZE)
        self.Bind(wx.EVT_COLLAPSIBLEPANE_CHANGED, self.OnPaneChanged, cp)
        self.MakePaneContent(cp.GetPane())

        radioBox = wx.RadioBox(self, -1, "Button Types", choices=choices, style=wx.RA_SPECIFY_ROWS)
        self.static1 = wx.StaticText(self, -1, "Collapsed Button Text:")
        self.static2 = wx.StaticText(self, -1, "Expanded Button Text:")

        self.buttonText1 = wx.TextCtrl(self, -1, self.label1)
        self.buttonText2 = wx.TextCtrl(self, -1, self.label2)
        self.updateButton = wx.Button(self, -1, "Update!")

        self.gtkText = wx.StaticText(self, -1, "Expander Size")
        self.gtkChoice = wx.ComboBox(self, -1, choices=gtkChoices)
        self.gtkChoice.SetSelection(0)
        
        self.gtkText.Enable(False)
        self.gtkChoice.Enable(False)
        
        sizer = wx.BoxSizer(wx.VERTICAL)
        radioSizer = wx.BoxSizer(wx.HORIZONTAL)
        dummySizer = wx.BoxSizer(wx.VERTICAL)

        dummySizer.Add(self.gtkText, 0, wx.EXPAND|wx.BOTTOM, 2)
        dummySizer.Add(self.gtkChoice, 0, wx.EXPAND)

        radioSizer.Add(radioBox, 0, wx.EXPAND)
        radioSizer.Add(dummySizer, 0, wx.ALIGN_BOTTOM|wx.LEFT, 10)

        self.SetSizer(sizer)
        sizer.Add((0, 10))
        sizer.Add(title, 0, wx.LEFT|wx.RIGHT, 25)
        sizer.Add((0, 10))
        sizer.Add(radioSizer, 0, wx.LEFT, 25)

        sizer.Add((0, 10))
        subSizer = wx.FlexGridSizer(2, 3, 5, 5)
        subSizer.Add(self.static1, 0, wx.LEFT|wx.ALIGN_CENTER_VERTICAL, 5)
        subSizer.Add(self.buttonText1, 0, wx.EXPAND)
        subSizer.Add((0, 0))
        subSizer.Add(self.static2, 0, wx.LEFT|wx.ALIGN_CENTER_VERTICAL, 5)
        subSizer.Add(self.buttonText2, 0, wx.EXPAND)
        subSizer.Add(self.updateButton, 0, wx.LEFT|wx.RIGHT, 10)
        
        subSizer.AddGrowableCol(1)
        
        sizer.Add(subSizer, 0, wx.EXPAND|wx.LEFT, 20)
        sizer.Add((0, 15))
        sizer.Add(cp, 0, wx.RIGHT|wx.LEFT|wx.EXPAND, 20)

        self.btn = wx.Button(self, label=btnlbl1)
        sizer.Add(self.btn, 0, wx.ALL, 25)

        self.Bind(wx.EVT_BUTTON, self.OnToggle, self.btn)
        self.Bind(wx.EVT_BUTTON, self.OnUpdate, self.updateButton)
        self.Bind(wx.EVT_RADIOBOX, self.OnButtonChoice)
        self.Bind(wx.EVT_COMBOBOX, self.OnUserChoice, self.gtkChoice)
        
        
    def OnToggle(self, event):
        
        self.cp.Collapse(self.cp.IsExpanded())
        self.OnPaneChanged()


    def OnUpdate(self, event):

        self.label1 = self.buttonText1.GetValue()
        self.label2 = self.buttonText2.GetValue()

        self.OnPaneChanged(None)
        

    def OnButtonChoice(self, event):

        selection = event.GetSelection()
        
        if self.cp.IsExpanded():
            label = self.label1
        else:
            label = self.label2

        style = self.cp.GetWindowStyleFlag()
        if selection < 4:
            style &= ~PCP.CP_GTK_EXPANDER
        else:
            style |= PCP.CP_GTK_EXPANDER
            
        self.gtkText.Enable(selection == 4)
        self.gtkChoice.Enable(selection == 4)
        
        self.Freeze()
        cp = PCP.PyCollapsiblePane(self, label=self.label1, style=style)
        self.Bind(wx.EVT_COLLAPSIBLEPANE_CHANGED, self.OnPaneChanged, cp)
        self.MakePaneContent(cp.GetPane())
        self.GetSizer().Replace(self.cp, cp)
        
        self.cp.Destroy()
        self.cp = cp
        self.Thaw()
        
        if selection == 0:     # standard wx.Button
            btn = wx.Button(self.cp, -1, label)
        elif selection == 1:   # buttons.GenButton
            btn = buttons.GenButton(self.cp, -1, label)
        elif selection == 2:   # buttons.GenBitmapButton
            bmp = images.Smiles.GetBitmap()
            btn = buttons.GenBitmapButton(self.cp, -1, bmp)
        elif selection == 3:   # buttons.GenBitmapTextButton
            bmp = images.Mondrian.GetBitmap()
            btn = buttons.GenBitmapTextButton(self.cp, -1, bmp, label)

        if selection < 4:
            self.cp.SetButton(btn)
            btn.Bind(wx.EVT_BUTTON, self.OnToggle)
        else:
            self.cp.SetExpanderDimensions(*self.GetUserSize())

        self.OnPaneChanged(None)
        self.Layout()
        

    def OnPaneChanged(self, event=None):

        if event:
            self.log.write('wx.EVT_COLLAPSIBLEPANE_CHANGED: %s\n' % event.Collapsed)

        # redo the layout
        self.Layout()
        
        # and also change the labels
        if self.cp.IsExpanded():
            self.cp.SetLabel(self.label2)
            self.btn.SetLabel(btnlbl2)
        else:
            self.cp.SetLabel(self.label1)
            self.btn.SetLabel(btnlbl1)
            
        self.btn.SetInitialSize()


    def OnUserChoice(self, event):

        self.cp.SetExpanderDimensions(*self.GetUserSize(event.GetSelection()))


    def GetUserSize(self, selection=None):

        if selection is None:
            selection = self.gtkChoice.GetSelection()

        choice = gtkChoices[selection]
        width, height = choice.split(",")

        return int(width), int(height)
            

    def MakePaneContent(self, pane):
        '''Just make a few controls to put on the collapsible pane'''

        nameLbl = wx.StaticText(pane, -1, "Name:")
        name = wx.TextCtrl(pane, -1, "");

        addrLbl = wx.StaticText(pane, -1, "Address:")
        addr1 = wx.TextCtrl(pane, -1, "");
        addr2 = wx.TextCtrl(pane, -1, "");

        cstLbl = wx.StaticText(pane, -1, "City, State, Zip:")
        city  = wx.TextCtrl(pane, -1, "", size=(150,-1));
        state = wx.TextCtrl(pane, -1, "", size=(50,-1));
        zip   = wx.TextCtrl(pane, -1, "", size=(70,-1));
        
        addrSizer = wx.FlexGridSizer(cols=2, hgap=5, vgap=5)
        addrSizer.AddGrowableCol(1)
        addrSizer.Add(nameLbl, 0, 
                wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL)
        addrSizer.Add(name, 0, wx.EXPAND)
        addrSizer.Add(addrLbl, 0,
                wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL)
        addrSizer.Add(addr1, 0, wx.EXPAND)
        addrSizer.Add((5,5)) 
        addrSizer.Add(addr2, 0, wx.EXPAND)

        addrSizer.Add(cstLbl, 0,
                wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL)

        cstSizer = wx.BoxSizer(wx.HORIZONTAL)
        cstSizer.Add(city, 1)
        cstSizer.Add(state, 0, wx.LEFT|wx.RIGHT, 5)
        cstSizer.Add(zip)
        addrSizer.Add(cstSizer, 0, wx.EXPAND)

        border = wx.BoxSizer()
        border.Add(addrSizer, 1, wx.EXPAND|wx.ALL, 5)
        pane.SetSizer(border)


#----------------------------------------------------------------------

def runTest(frame, nb, log):
    win = PyCollapsiblePaneDemo(nb, log)
    return win

#----------------------------------------------------------------------

overview = PCP.__doc__

if __name__ == '__main__':
    import sys,os
    import run
    run.main(['', os.path.basename(sys.argv[0])] + sys.argv[1:])


