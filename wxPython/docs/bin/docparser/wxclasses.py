import sys, os, re
import wx
import restconvert
html_heading = "<H3><font color=\"red\">%s</font></H3>"


classes_categories = { \
 "wxTopLevelWindow" : "managedwnd",
 "wxDialog" : "managedwnd",
 "wxFrame" : "managedwnd",
 "wxMDIChildFrame" : "managedwnd",
 "wxMDIParentFrame" : "managedwnd",
 "wxMiniFrame" : "managedwnd",
 "wxPropertySheetDialog" : "managedwnd",
 "wxSplashScreen" : "managedwnd",
 "wxTipWindow" : "managedwnd",
 "wxWizard" : "managedwnd",
 "wxPanel" : "miscwnd",
 "wxScrolledWindow" : "miscwnd",
 "wxGrid" : "miscwnd",
 "wxSplitterWindow" : "miscwnd",
 "wxStatusBar" : "miscwnd",
 "wxToolBar" : "miscwnd",
 "wxNotebook" : "miscwnd",
 "wxListbook" : "miscwnd",
 "wxChoicebook" : "miscwnd",
 "wxTreebook" : "miscwnd",
 "wxSashWindow" : "miscwnd",
 "wxSashLayoutWindow" : "miscwnd",
 "wxVScrolledWindow" : "miscwnd",
 "wxWizardPage" : "miscwnd",
 "wxWizardPageSimple" : "miscwnd",
 "wxDialog" : "cmndlg",
 "wxColourDialog" : "cmndlg",
 "wxDirDialog" : "cmndlg",
 "wxFileDialog" : "cmndlg",
 "wxFindReplaceDialog" : "cmndlg",
 "wxMultiChoiceDialog" : "cmndlg",
 "wxSingleChoiceDialog" : "cmndlg",
 "wxTextEntryDialog" : "cmndlg",
 "wxPasswordEntryDialog" : "cmndlg",
 "wxFontDialog" : "cmndlg",
 "wxPageSetupDialog" : "cmndlg",
 "wxPrintDialog" : "cmndlg",
 "wxProgressDialog" : "cmndlg",
 "wxMessageDialog" : "cmndlg",
 "wxSymbolPickerDialog" : "cmndlg",
 "wxRichTextFormattingDialog" : "cmndlg",
 "wxWizard" : "cmndlg",
 "wxAnimationCtrl" : "ctrl",
 "wxControl" : "ctrl",
 "wxButton" : "ctrl",
 "wxBitmapButton" : "ctrl",
 "wxBitmapComboBox" : "ctrl",
 "wxToggleButton" : "ctrl",
 "wxBitmapToggleButton" : "ctrl",
 "wxCalendarCtrl" : "ctrl",
 "wxCheckBox" : "ctrl",
 "wxCheckListBox" : "ctrl",
 "wxChoice" : "ctrl",
 "wxCollapsiblePane" : "ctrl",
 "wxComboBox" : "ctrl",
 "wxComboCtrl" : "ctrl",
 "wxDataViewCtrl" : "ctrl",
 "wxDataViewTreeCtrl" : "ctrl",
 "wxGauge" : "ctrl",
 "wxGenericDirCtrl" : "ctrl",
 "wxHtmlListBox" : "ctrl",
 "wxSimpleHtmlListBox" : "ctrl",
 "wxStaticBox" : "ctrl",
 "wxListBox" : "ctrl",
 "wxListCtrl" : "ctrl",
 "wxListView" : "ctrl",
 "wxOwnerDrawnComboBox" : "ctrl",
 "wxRichTextCtrl" : "ctrl",
 "wxTextCtrl" : "ctrl",
 "wxTreeCtrl" : "ctrl",
 "wxScrollBar" : "ctrl",
 "wxSpinButton" : "ctrl",
 "wxSpinCtrl" : "ctrl",
 "wxStaticText" : "ctrl",
 "wxHyperlinkCtrl" : "ctrl",
 "wxStaticBitmap" : "ctrl",
 "wxRadioBox" : "ctrl",
 "wxRadioButton" : "ctrl",
 "wxSlider" : "ctrl",
 "wxVListBox" : "ctrl",
 "wxColourPickerCtrl" : "miscpickers",
 "wxDirPickerCtrl" : "miscpickers",
 "wxFilePickerCtrl" : "miscpickers",
 "wxFontPickerCtrl" : "miscpickers",
 "wxDatePickerCtrl" : "miscpickers",
 "wxMenu" : "menus",
 "wxMenuBar" : "menus",
 "wxMenuItem" : "menus",
 "wxAuiManager" : "aui",
 "wxAuiNotebook" : "aui",
 "wxAuiPaneInfo" : "aui",
 "wxAuiDockArt" : "aui",
 "wxAuiTabArt" : "aui",
 "wxSizer" : "winlayout",
 "wxGridSizer" : "winlayout",
 "wxFlexGridSizer" : "winlayout",
 "wxGridBagSizer" : "winlayout",
 "wxBoxSizer" : "winlayout",
 "wxStaticBoxSizer" : "winlayout",
 "wxWrapSizer" : "winlayout",
 "wxIndividualLayoutConstraint" : "winlayout",
 "wxLayoutConstraints" : "winlayout",
 "wxLayoutAlgorithm" : "winlayout",
 "wxAutoBufferedPaintDC" : "dc",
 "wxBufferedDC" : "dc",
 "wxBufferedPaintDC" : "dc",
 "wxClientDC" : "dc",
 "wxPaintDC" : "dc",
 "wxWindowDC" : "dc",
 "wxScreenDC" : "dc",
 "wxDC" : "dc",
 "wxMemoryDC" : "dc",
 "wxMetafileDC" : "dc",
 "wxMirrorDC" : "dc",
 "wxPostScriptDC" : "dc",
 "wxPrinterDC" : "dc",
 "wxColour" : "gdi",
 "wxDCClipper" : "gdi",
 "wxBitmap" : "gdi",
 "wxBrush" : "gdi",
 "wxBrushList" : "gdi",
 "wxCursor" : "gdi",
 "wxFont" : "gdi",
 "wxFontList" : "gdi",
 "wxIcon" : "gdi",
 "wxImage" : "gdi",
 "wxImageList" : "gdi",
 "wxMask" : "gdi",
 "wxPen" : "gdi",
 "wxPenList" : "gdi",
 "wxPalette" : "gdi",
 "wxRegion" : "gdi",
 "wxRendererNative" : "gdi",
 "wxActivateEvent" : "events",
 "wxCalendarEvent" : "events",
 "wxCalculateLayoutEvent" : "events",
 "wxChildFocusEvent" : "events",
 "wxClipboardTextEvent" : "events",
 "wxCloseEvent" : "events",
 "wxCommandEvent" : "events",
 "wxContextMenuEvent" : "events",
 "wxDateEvent" : "events",
 "wxDialUpEvent" : "events",
 "wxDropFilesEvent" : "events",
 "wxEraseEvent" : "events",
 "wxEvent" : "events",
 "wxFindDialogEvent" : "events",
 "wxFocusEvent" : "events",
 "wxKeyEvent" : "events",
 "wxIconizeEvent" : "events",
 "wxIdleEvent" : "events",
 "wxInitDialogEvent" : "events",
 "wxJoystickEvent" : "events",
 "wxListEvent" : "events",
 "wxMaximizeEvent" : "events",
 "wxMenuEvent" : "events",
 "wxMouseCaptureChangedEvent" : "events",
 "wxMouseCaptureLostEvent" : "events",
 "wxMouseEvent" : "events",
 "wxMoveEvent" : "events",
 "wxNavigationKeyEvent" : "events",
 "wxNotebookEvent" : "events",
 "wxNotifyEvent" : "events",
 "wxPaintEvent" : "events",
 "wxProcessEvent" : "events",
 "wxQueryLayoutInfoEvent" : "events",
 "wxRichTextEvent" : "events",
 "wxScrollEvent" : "events",
 "wxScrollWinEvent" : "events",
 "wxSizeEvent" : "events",
 "wxSocketEvent" : "events",
 "wxSpinEvent" : "events",
 "wxSplitterEvent" : "events",
 "wxSysColourChangedEvent" : "events",
 "wxTimerEvent" : "events",
 "wxTreebookEvent" : "events",
 "wxTreeEvent" : "events",
 "wxUpdateUIEvent" : "events",
 "wxWindowCreateEvent" : "events",
 "wxWindowDestroyEvent" : "events",
 "wxWizardEvent" : "events",
 "wxValidator" : "validator",
 "wxTextValidator" : "validator",
 "wxGenericValidator" : "validator",
 "wxCmdLineParser" : "data",
 "wxDateSpan" : "data",
 "wxDateTime" : "data",
 "wxLongLong" : "data",
 "wxObject" : "data",
 "wxPathList" : "data",
 "wxPoint" : "data",
 "wxRect" : "data",
 "wxRegEx" : "data",
 "wxRegion" : "data",
 "wxString" : "data",
 "wxStringTokenizer" : "data",
 "wxRealPoint" : "data",
 "wxSize" : "data",
 "wxTimeSpan" : "data",
 "wxURI" : "data",
 "wxVariant" : "data",
 "wxArray<T>" : "containers",
 "wxArrayString" : "containers",
 "wxHashMap<T>" : "containers",
 "wxHashSet<T>" : "containers",
 "wxHashTable" : "containers",
 "wxList<T>" : "containers",
 "wxVector<T>" : "containers",
 "wxObjectDataPtr<T>" : "smartpointers",
 "wxScopedPtr<T>" : "smartpointers",
 "wxSharedPtr<T>" : "smartpointers",
 "wxWeakRef<T>" : "smartpointers",
 "wxClassInfo" : "rtti",
 "wxObject" : "rtti",
 "RTTI macros" : "rtti",
 "wxLog" : "logging",
 "wxLogStderr" : "logging",
 "wxLogStream" : "logging",
 "wxLogTextCtrl" : "logging",
 "wxLogWindow" : "logging",
 "wxLogGui" : "logging",
 "wxLogNull" : "logging",
 "wxLogChain" : "logging",
 "wxLogInterposer" : "logging",
 "wxLogInterposerTemp" : "logging",
 "wxStreamToTextRedirector" : "logging",
 "Log functions" : "logging",
 "wxDebugContext" : "debugging",
 "Debugging macros" : "debugging",
 "WXDEBUG_NEW" : "debugging",
 "wxDebugReport" : "debugging",
 "wxDebugReportCompress" : "debugging",
 "wxDebugReportUpload" : "debugging",
 "wxDebugReportPreview" : "debugging",
 "wxDebugReportPreviewStd" : "debugging",
 "wxDialUpManager" : "net",
 "wxIPV4address" : "net",
 "wxIPaddress" : "net",
 "wxSocketBase" : "net",
 "wxSocketClient" : "net",
 "wxSocketServer" : "net",
 "wxSocketEvent" : "net",
 "wxFTP" : "net",
 "wxHTTP" : "net",
 "wxURL" : "net",
 "wxClient, wxDDEClient" : "ipc",
 "wxConnection, wxDDEConnection" : "ipc",
 "wxServer, wxDDEServer" : "ipc",
 "wxDocument" : "dvf",
 "wxView" : "dvf",
 "wxDocTemplate" : "dvf",
 "wxDocManager" : "dvf",
 "wxDocChildFrame" : "dvf",
 "wxDocParentFrame" : "dvf",
 "wxPreviewFrame" : "printing",
 "wxPreviewCanvas" : "printing",
 "wxPreviewControlBar" : "printing",
 "wxPrintDialog" : "printing",
 "wxPageSetupDialog" : "printing",
 "wxPrinter" : "printing",
 "wxPrinterDC" : "printing",
 "wxPrintout" : "printing",
 "wxPrintPreview" : "printing",
 "wxPrintData" : "printing",
 "wxPrintDialogData" : "printing",
 "wxPageSetupDialogData" : "printing",
 "wxDataObject" : "dnd",
 "wxDataFormat" : "dnd",
 "wxTextDataObject" : "dnd",
 "wxFileDataObject" : "dnd",
 "wxBitmapDataObject" : "dnd",
 "wxURLDataObject" : "dnd",
 "wxCustomDataObject" : "dnd",
 "wxClipboard" : "dnd",
 "wxDropTarget" : "dnd",
 "wxFileDropTarget" : "dnd",
 "wxTextDropTarget" : "dnd",
 "wxDropSource" : "dnd",
 "wxFileName" : "file",
 "wxDir" : "file",
 "wxDirTraverser" : "file",
 "wxFile" : "file",
 "wxFFile" : "file",
 "wxTempFile" : "file",
 "wxTextFile" : "file",
 "wxStandardPaths" : "file",
 "wxPathList" : "file",
 "wxStreamBase" : "streams",
 "wxStreamBuffer" : "streams",
 "wxInputStream" : "streams",
 "wxOutputStream" : "streams",
 "wxCountingOutputStream" : "streams",
 "wxFilterInputStream" : "streams",
 "wxFilterOutputStream" : "streams",
 "wxBufferedInputStream" : "streams",
 "wxBufferedOutputStream" : "streams",
 "wxMemoryInputStream" : "streams",
 "wxMemoryOutputStream" : "streams",
 "wxDataInputStream" : "streams",
 "wxDataOutputStream" : "streams",
 "wxTextInputStream" : "streams",
 "wxTextOutputStream" : "streams",
 "wxFileInputStream" : "streams",
 "wxFileOutputStream" : "streams",
 "wxFFileInputStream" : "streams",
 "wxFFileOutputStream" : "streams",
 "wxTempFileOutputStream" : "streams",
 "wxStringInputStream" : "streams",
 "wxStringOutputStream" : "streams",
 "wxZlibInputStream" : "streams",
 "wxZlibOutputStream" : "streams",
 "wxZipInputStream" : "streams",
 "wxZipOutputStream" : "streams",
 "wxTarInputStream" : "streams",
 "wxTarOutputStream" : "streams",
 "wxSocketInputStream" : "streams",
 "wxSocketOutputStream" : "streams",
 "wxThread" : "thread",
 "wxThreadHelper" : "thread",
 "wxMutex" : "thread",
 "wxMutexLocker" : "thread",
 "wxCriticalSection" : "thread",
 "wxCriticalSectionLocker" : "thread",
 "wxCondition" : "thread",
 "wxSemaphore" : "thread",
 "wxHtmlHelpController" : "html",
 "wxHtmlWindow" : "html",
 "wxHtmlEasyPrinting" : "html",
 "wxHtmlPrintout" : "html",
 "wxHtmlParser" : "html",
 "wxHtmlTagHandler" : "html",
 "wxHtmlWinParser" : "html",
 "wxHtmlWinTagHandler" : "html",
 "wxTextAttr" : "richtext",
 "wxrichtextTextCtrl" : "richtext",
 "wxrichtextTextBuffer" : "richtext",
 "wxrichtextTextCharacterStyleDefinition" : "richtext",
 "wxrichtextTextParagraphStyleDefinition" : "richtext",
 "wxrichtextTextListStyleDefinition" : "richtext",
 "wxrichtextTextStyleSheet" : "richtext",
 "wxrichtextTextStyleComboCtrl" : "richtext",
 "wxrichtextTextStyleListBox" : "richtext",
 "wxrichtextTextStyleOrganiserDialog" : "richtext",
 "wxrichtextTextEvent" : "richtext",
 "wxrichtextTextRange" : "richtext",
 "wxrichtextTextFileHandler" : "richtext",
 "wxrichtextTextHTMLHandler" : "richtext",
 "wxrichtextTextXMLHandler" : "richtext",
 "wxrichtextTextFormattingDialog" : "richtext",
 "wxrichtextTextPrinting" : "richtext",
 "wxrichtextTextPrintout" : "richtext",
 "wxrichtextTextHeaderFooterData" : "richtext",
 "wxStyledTextCtrl" : "stc",
 "wxFSFile" : "vfs",
 "wxFileSystem" : "vfs",
 "wxFileSystemHandler" : "vfs",
 "wxXmlDocument" : "xml",
 "wxXmlNode" : "xml",
 "wxXmlAttribute" : "xml",
 "wxXmlResource" : "xrc",
 "wxXmlResourceHandler" : "xrc",
 "wxHelpController" : "help",
 "wxHtmlHelpController" : "help",
 "wxContextHelp" : "help",
 "wxContextHelpButton" : "help",
 "wxHelpProvider" : "help",
 "wxSimpleHelpProvider" : "help",
 "wxHelpControllerHelpProvider" : "help",
 "wxToolTip" : "help",
 "wxMediaCtrl" : "media",
 "wxGLCanvas" : "gl",
 "wxGLContext" : "gl",
 "wxApp" : "appmanagement",
 "wxCmdLineParser" : "appmanagement",
 "wxDllLoader" : "appmanagement",
 "wxProcess" : "appmanagement",
 "wxCaret" : "misc",
 "wxConfigBase" : "misc",
 "wxTimer" : "misc",
 "wxStopWatch" : "misc",
 "wxMimeTypesManager" : "misc",
 "wxSystemSettings" : "misc",
 "wxSystemOptions" : "misc",
 "wxAcceleratorTable" : "misc",
 "wxAutomationObject" : "misc",
 "wxFontMapper" : "misc",
 "wxEncodingConverter" : "misc",
 "wxCalendarDateAttr" : "misc",
 "wxQuantize" : "misc",
 "wxSingleInstanceChecker" : "misc"}


def doxifyFormatting(txt):
    txt = txt.replace("true", "@true")
    txt = txt.replace("@@true", "@true")
    txt = txt.replace("@c @true", "@true")
    txt = txt.replace("false", "@false")
    txt = txt.replace("@@false", "@false")
    txt = txt.replace("@c @false", "@false")
    txt = txt.replace("NULL", "@NULL")
    txt = txt.replace("@c @NULL", "@NULL")
    return txt


import HTMLParser
class HTMLStripper(HTMLParser.HTMLParser):
    def __init__(self):
        self.reset()
        self.fed = []
    def handle_data(self, d):
        self.fed.append(d)
    def get_fed_data(self):
        return ''.join(self.fed)
    
    
def stripHTML(txt):
    x = HTMLStripper()
    x.feed(txt)
    return x.get_fed_data()

def stylesAsHtml(styles, extraStyles=False):
    heading = "Window styles"
    if extraStyles:
        heading = "Extra window styles"
        
    html = html_heading % heading
    html += """<table width="95%">"""
    for style in styles:
        html += "<tr><td>%s</td><td>%s</td>" % (style[0], style[1])
        
    html += "</table>"
    
    return html
    
def lastLineLength(str):
    if "\n" not in str:
        return len(str)
    return len(str.split("\n")[-1])
    
def commentizeText(text, indent=4):
    outtext = ""
    midtext = text.strip()
    indentstr = " " * indent
    
    #print "-----------------------------------"
    #print text
    #print "-----------------------------------"
    
    # highly unoptimized system to make justified text
    
    #lst = midtext.replace("\n", " ").split(" ")
    #outtext=indentstr + "*"
    #for word in lst:
        #if lastLineLength(outtext)+len(word)>80:
            #outtext += "\n" + indentstr + "*"
        #else:
            #outtext += " " + word.strip()
    MAX=80
    
    midtext = midtext.replace("\n\n\n", "\n\n")
    midtext = midtext.replace("\n\n\n", "\n\n")
    for line in midtext.split("\n"):
        if len(line)>MAX:
            idx = line[:MAX].rfind(" ")
            firstpart = line[:idx]
            secondpart = line[idx+1:]
            outtext += indentstr + "* " + firstpart + "\n"
            outtext += indentstr + "* " + secondpart + "\n"
        else:
            outtext += indentstr + "* " + line + "\n"
        
    return outtext  # + "\n"
    
def stripExtraNewlines(text):
    outtext = text.strip()
    while len(outtext) > 1 and outtext[0] == "\n":
        outtext = outtext[1:]
        
    while len(outtext) > 1 and outtext[-1] == "\n":
        outtext = outtext[0:-1]

    return outtext 
    
    
def justifyKeepingIndent(MAX, indent, desc, sep=" "):
    while lastLineLength(desc)>MAX:
        lines = desc.split("\n")
        lastline = lines[-1]
        idx = lastline[:MAX].rfind(sep[0])
        if idx<MAX/2:
            if len(sep)>1:
                idx = lastline[:MAX].rfind(sep[1])
            if idx<MAX/2:
                print "ERROR: can't find separator %s in %s for text %s" % (sep, lastline[:MAX], desc)
                sys.exit(1)
        desc = "\n".join(lines[:-1]) + "\n" + lastline[:idx] + "\n" + " "*indent + lastline[idx:]
        #print "desc now is:\n%s" % desc

    if desc.startswith("\n"):
        desc = desc[1:]
    return desc

class wxClass:
    def __init__(self, name, description="", derivedFrom=[], events=[], \
                 styles=[], extrastyles=[], lib="Base", sa=""):
        self.name = name
        self.description = description
        self.derivedFrom = derivedFrom
        self.events = events
        self.styles = styles
        self.extrastyles = extrastyles
        self.methods = {}
        self.propConflicts = []
        self.props = []
        self.inclusionFile = ""
        self.lib = stripHTML(lib).lower()
        self.seeAlso = stripHTML(sa)
        self.objects = ""
        
        if self.lib not in [ "wxcore", "wxbase", "wxaui", "wxnet", "wxrichtext", "wxxml", \
                             "wxadv", "wxmedia", "wxgl", "wxhtml", "wxqa", "wxxrc", "wxstc" ]:
            if self.lib.startswith("none"):
                self.lib = "none"
            else:
                print "ERROR: invalid library %s" % self.lib
                sys.exit(1)
        
        
    def asHtml(self):
        html = "<H1>%s</H1>" % self.name
        html += self.description
        if len(self.derivedFrom) > 0:
            html += html_heading % "Derived from"
            for der in self.derivedFrom:
                derurl = der.replace("wx.", "wx").lower()
                html += "<a href=\"wx_%s.html\">%s</a></br>" % (derurl, der)
                
        if len(self.styles) > 0:
            html += stylesAsHtml(self.styles)
            
        if len(self.extrastyles) > 0:
            html += stylesAsHtml(self.extrastyles, extraStyles=True)
            
        return html
        
    def asReST(self):
        restText = "DocStr(%s,\n" % (self.name)
        
        restText += ");"
        return restText
        
    def asDoxygen(self, indent=0):
        
        incfilename = self.name.lower() + ".h"
        if incfilename.startswith("wx"):
            incfilename = incfilename[2:]
        
        fname = self.inclusionFile
        
        doxytext = "\n"
        doxytext += "@class " + self.name + "\n"
        if '/' in fname:
            fname = fname[fname.find("/")+1:]
            doxytext += "@headerfile " + fname + " wx/" + self.inclusionFile + "\n\n"
        else:
            doxytext += "@wxheader{" + fname + "}\n"
        
        doxytext += self.description.strip() + "\n\n"
        doxytext = doxytext.replace("<P>", "\n")

        def genStyleList(styles):
            text = ""
            for style in styles:
                desc = "       " + style[1].strip().replace("\n", " ")
                desc = stripHTML(desc)
                desc = justifyKeepingIndent(75, 6, desc)
                text += "@style{%s}:\n%s\n" % (style[0].strip().replace(",", "\,"), desc)
            return text
        
        def genEventList(styles):
            text = ""
            for style in styles:
                desc = "       " + style[1].strip().replace("\n", " ")
                desc = stripHTML(desc)
                desc = justifyKeepingIndent(75, 6, desc)
                
                #style[0] = style[0].replace(",", "\,")
                # we don't need this, thanks to the @event overloading hack
                
                text += "@event{%s}:\n%s\n" % (style[0].strip(), desc)
            return text

        if len(self.styles)>0:
            doxytext += "\n@beginStyleTable\n"
            doxytext += genStyleList(self.styles)
            doxytext += "@endStyleTable\n"
        if len(self.extrastyles)>0:
            doxytext += "\n@beginExtraStyleTable\n"
            doxytext += genStyleList(self.extrastyles)
            doxytext += "@endExtraStyleTable\n"

        if len(self.events)>0:
            doxytext += "\n@beginEventTable\n"
            doxytext += genEventList(self.events)
            doxytext += "@endEventTable\n"

        if self.lib == "none":
            doxytext += "\n@nolibrary\n"
        else:
            doxytext += "\n@library{%s}\n" % self.lib
        
        if self.name in classes_categories:
            cat = classes_categories[self.name]
            doxytext += "@category{%s}\n" % cat
            if cat=="ctrl" or cat=="miscpickers":
                fname = self.name[2:] + ".png"
                doxytext += "@appearance{%s}\n\n" % fname.lower()
            else:
                doxytext += "\n"
        else:
            doxytext += "@category{FIXME}\n\n"
        
        if len(self.objects.strip())>0:
            doxytext += "\n@stdobjects\n%s\n\n" % self.objects.strip()
                        #justifyKeepingIndent(75, 8, self.objects.strip())
        
        if len(self.seeAlso.strip())>0:
            doxytext += "\n@seealso\n%s\n\n" % self.seeAlso.strip()
                        #justifyKeepingIndent(75, 8, self.seeAlso.strip())

        doxytext = "/**\n%s*/\n\n" % commentizeText(stripHTML(doxytext), indent).replace("\n* ", "\n    ")
        doxytext = doxifyFormatting(doxytext)
        return doxytext.replace("/**\n* ", "/**\n    ")
        
    def createProps(self):
        propsText = ""
        propList = self.props
        for conflict in self.propConflicts:
            if conflict in propList:
                propList.remove(conflict)
        
        basename = self.name.replace("wx", "")
        for prop in propList:
            if prop != "":
                propname = prop
                if propname[0] == "3":
                    propname = "Three" + propname[1:]
                
                getter = "wx.%s.Get%s" % (basename, prop)
                setter = "wx.%s.Set%s" % (basename, prop)
                propsText += "wx.%s.%s = property(%s" % (basename, propname, getter) 
                hasSetter = eval("(\"%s\" in dir(wx.%s))" % ("Set" + prop, basename))
                if hasSetter:
                    propsText += ", %s" % setter
                propsText += ")\n"
        
        if propsText != "":
            propsText += "\n\n"
        
        return propsText

class wxMethod:
    def __init__(self, name, parent, prototypes=[], params={}, description="", isCtor=False, isDtor=False, remarks="", retDesc="", sa=""):
        self.name = name
        self.parent = parent
        self.prototypes = prototypes
        self.params = params
        self.description = description
        self.isCtor = isCtor
        self.isDtor = isDtor
        self.remarks = stripHTML(remarks).replace("\n", " ")
        self.pythonNote = ""
        self.pythonOverrides = []
        self.returnDesc = stripHTML(retDesc).replace("\n", " ")
        self.seeAlso = stripHTML(sa).replace("\n", " ")
        self.inclusionFile = ""
        
        count=0
        for c in self.name:
            if c.upper()==c:
                count+=1
        #print self.name  + " has %d uppercase chars" % count
        #if len(self.prototypes)==0:
            #print "no protos", self.name
            #sys.exit(1)
        
        #self.isDefine = (len(self.prototypes)>1 and \
                         ##str(self.prototypes[0]).strip() == "" and \
                         #abs(count-len(self.name))<3)
        self.isDefine = abs(count-len(self.name))<3 and len(self.name) > 6
        if self.isDefine:
            print "FOUND A MACRO", self.name
            
        if "@b const" in description:
            self.isconst = True
            self.description = self.description.replace("@b const", "")
        else:
            self.isconst = False
        
    def asReST(self):
        restText = ""
        
        # The below code converts prototypes into ReST, but currently isn't 
        # needed. Left here in case we change approach later.
        
        #for proto in self.prototypes:
        #    restText += proto[1] + "("
        #    counter = 1
        #    for arg in proto[2]:
        #        restText += "%s %s" % (arg[0].replace("wx.", ""), arg[1])
        #        if counter < len(proto[2]):
        #            restText += ", "
        #        counter += 1
        #    if proto[0] != "":
        #        restText += "-> " + proto[0]
        #    restText += "\n"
        #restText += "\n"
        
        if len(self.params) > 0:
            
            for param in self.params:
                restText += "\n:param %s: %s" % (param[0], restconvert.htmlToReST(param[1]))
            restText += "\n\n"
        
        restText += restconvert.htmlToReST(self.description.strip())
        return restText
        
    def asHtml(self):
        anchorname = self.getAnchorName()
        retval = "<A name=\"%s\"></A>" % (anchorname)
        retval += "<H3>%s</H3>" % self.name
        if len(self.pythonOverrides) > 0:
            for myfunc in self.pythonOverrides:
                retval += "<p><b>%s</b></br>%s</p>" % (myfunc[0], myfunc[1])
        else:
            for proto in self.prototypes:
                retval += "<P><B>"
                if proto[0] != "":
                    retval += proto[0] + " "
                retval += proto[1] + "("
                counter = 1
                for arg in proto[2]:
                    retval += "%s <i>%s</i>" % (arg[0], arg[1])
                    if counter < len(proto[2]):
                        retval += ", "
                    counter += 1
                retval += ")</B></P>"
            
        if len(self.params) > 0:
            retval += "<table width=\"90%%\" cellspacing=\"10\">"
            for param in self.params:
                retval += "<tr><td align=\"right\"><i>%s</i></td><td bgcolor=\"#E3E3E3\">%s</td></tr>" % (param[0], param[1])
            retval += "</table>"
            
        retval += "<p>%s</p>" % self.description
        
        if self.remarks != "":
            retval += "<font color=\"red\">Remarks</font><h4>%s</h4></font>" % self.remarks
        
        return retval
        
    def asDoxygen(self, indent=4):
        doxytext = ""
        
        doxytext += self.description.strip() + "\n\n"
        
        # TODO convert supported HTML tags before doing this
        doxytext = stripHTML(doxytext)
        
        paramtext =""
        for param in self.params:
            txt = stripHTML(param[1])
            paramtext += "\n@param " + param[0] + " \n    " + \
                        txt.strip().replace("\n", "\n    ")
                        
        #print paramtext
        doxytext += "\n" + paramtext + "\n"
        
        #if len(self.prototypes) > 0:
        #    proto = self.prototypes[0]
        #    type = proto[0]
        #    type = type.replace("virtual ", "")
        #    if type.strip() == "void":
        #        type = ""
        #    if type != "":
        #        doxytext += "\n\\return " + proto[0]
        
        #doxytext += ""
        #    counter = 1
        #    for arg in proto[2]:
        #        doxytext += "%s %s" % (arg[0], arg[1])
        #        if counter < len(proto[2]):
        #            doxytext += ", "
        #        counter += 1
        #    doxytext += ");\n\n\n"
        
        doxytext = doxytext.replace("<P>", "\n")
        doxytext = doxytext.replace("\n\n\n", "\n")
        
        if len(self.returnDesc.strip())>0:
            doxytext += "\n@returns %s\n\n" % justifyKeepingIndent(65, 8, self.returnDesc.strip())
        
        if len(self.remarks.strip())>0:
            doxytext += "\n@remarks %s\n\n" % justifyKeepingIndent(65, 8, self.remarks.strip())
        
        # NOTE: we won't use @seealso which generates a section and is good only for wxClass!
        if len(self.seeAlso.strip())>0:
            doxytext += "\n@see %s\n\n" % justifyKeepingIndent(75, 4, self.seeAlso.strip())
        
        # TODO convert supported HTML tags before doing this
        doxytext = stripHTML(doxytext)
        
        # inside class X references to members of the same class can be
        # done simply using # prefix or () suffix
        if self.parent!="":
            prefix = self.parent.name + "::"
            doxylink_re = prefix + "([a-zA-Z]*)([\s\.,:;])"
            #print "searching", doxylink_re
            doxylink_regex = re.compile(doxylink_re)
            
            def replace_explicit_link(match):
                funcname = match.group(1)
                #print "found", funcname
                if funcname.endswith("()"):
                    return funcname + match.group(2)
                return funcname + "()" + match.group(2)
            
            doxytext = doxylink_regex.sub(replace_explicit_link, doxytext)
            
            
        
        # to remove HTML:
        def replace_empty(match):
            return ""
        html_re = re.compile("""<[^>]*>""", re.MULTILINE | re.DOTALL)

            
            
        # replace @e followed by argument names with @a
        paramnames = []
        for proto in self.prototypes:
            if len(proto) == 3:
                for a in proto[2]:
                    if len(a) == 2:
                        name = str(a[1]).strip()
                        name = html_re.sub(replace_empty, name)
                        if "=" in name:
                            name=name[:name.find("=")].strip()
                        paramnames.append(name)
        
        for n in paramnames:
            doxytext = doxytext.replace("@e " + n + " ", "@a " + n + " ")
        
        indentstr = " " * indent
        doxytext = "%s/**\n%s%s*/" % (indentstr, commentizeText(doxytext, indent=indent), indentstr)
        doxytext = doxytext.replace("\n" + indentstr + "* ", "\n" + 2*indentstr) #.replace(" *   ", "   ")
        
        doxytext = doxifyFormatting(doxytext)
        
        # call doxifyFormatting before getPrototype()!!
        doxytext += "\n" + self.getPrototype() + "\n"
        
        if len(self.prototypes)>1:
            doxytext = indentstr + "//@{\n" + doxytext + indentstr + "//@}\n"
        
        return doxytext
        
    def getAnchorName(self):
        anchorname = self.parent.name.lower() + self.name.lower()
        if self.parent.name == self.name:
            anchorname = self.name.lower()
            
        return anchorname
    
    def asString(self):
        retval = "method: " + self.name
        retval += "\n\nprototypes: "
        for proto in self.prototypes:
            retval += "\t%s" % `proto`
        retval += "\n\nparams: "
        for param in self.params:
            retval += "%s: %s" % (param, self.params[param])
            
        retval += "\n\ndescription: \n" + self.description
        
        retval += "remarks: \n" + self.remarks
        
        return retval
        
    def getPrototype(self):
        
        # to remove HTML:
        def replace_empty(match):
            return ""
        html_re = re.compile("""<[^>]*>""", re.MULTILINE | re.DOTALL)
                
        retval=""
        for proto in self.prototypes:
            if len(proto) == 3:
                #print "function %s has prototype: %s" % (self.name, str(proto))
                retval += "    "
                
                rettype = html_re.sub(replace_empty, str(proto[0])).strip() + " "
                rettype = rettype.replace("*", "* ").replace("& ", "& ").replace("=", " = ")
                rettype = rettype.replace("  ", " ")
                rettype = rettype.replace(" *", "*").replace(" &", "&")
                
                if not self.isCtor and not self.isDtor:
                    retval += rettype
                retval += str(proto[1]).strip()
                
                offset = lastLineLength(retval)+1
                args = ""
                for a in proto[2]:
                    if len(a) == 2:
                        type = str(a[0])
                        type = html_re.sub(replace_empty, type)
                        
                        name = str(a[1])
                        name = html_re.sub(replace_empty, name)
                        
                        param = str(type).strip() + " " + str(name).strip() + ", "
                        
                        if offset+lastLineLength(args)+len(param)>70:
                            args = args[:-1]
                            args += "\n" + " " * offset + param
                        else:
                            args += param
                        
                        
                # final touches on args string
                # attach * and & qualifier to the argument type
                args = args.replace("*", "* ").replace("& ", "& ").replace("=", " = ")
                args = args.replace("  ", " ")
                args = args.replace(" *", "*").replace(" &", "&")

                args = args.strip()
                if args.endswith(","): args = args[:-1]
                
                retval += "(" + args
                 
                if self.isconst: 
                    retval += ") const;\n    "
                else:
                    retval += ");\n    "

            else:
                print "WARNING: prototype has not 3 elements..."
                sys.exit(1)
                
        retval = retval.replace("&amp;", "&").rstrip();
        
        if len(self.prototypes)==1 and self.isDefine:
            if retval.endswith(";"):
                retval = retval[:-1]
                retval += "     /* implementation is private */"
            return "#define " + retval.strip()
                
        return retval

