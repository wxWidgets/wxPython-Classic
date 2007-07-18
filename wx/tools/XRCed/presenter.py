# Name:         presenter.py
# Purpose:      Presenter part
# Author:       Roman Rolinsky <rolinsky@femagsoft.com>
# Created:      07.06.2007
# RCS-ID:       $Id$

import os,tempfile,shutil
from xml.parsers import expat
import cPickle
from globals import *
import view
from model import Model, MyDocument
from component import Manager
import undo

# Presenter class linking model to view objects
class _Presenter:
    def init(self):
        Model.init()
        self.path = ''
        # Global modified state
        self.setModified(False) # sets applied
        self.undoSaved = True   # set to false when some pending undo data
        view.frame.Clear()
        view.tree.Clear()
        view.tree.SetPyData(view.tree.root, Model.mainNode)
        view.testWin.Init()
        g.undoMan.Clear()
        # Insert/append mode flags
        self.createSibling = self.insertBefore = False
        # Select main node attributes
        self.setData(view.tree.root)

    def loadXML(self, path):
        Model.loadXML(path)
        view.tree.Flush()
        view.tree.ExpandAll()
        view.tree.SetPyData(view.tree.root, Model.mainNode)
        self.setData(view.tree.root)

    def saveXML(self, path):
        Model.saveXML(path)

    def open(self, path):
        if not os.path.exists(path):
            wx.LogError('File does not exists: %s' % path)
            raise IOError
        try:
            self.path = os.path.abspath(path)
            TRACE('Loading XML file: %s', self.path)
            self.loadXML(self.path)
            # Change dir
            dir = os.path.dirname(self.path)
            if dir: os.chdir(dir)
            self.setModified(False)
            g.conf.localconf = self.createLocalConf(path)
        except:
            logger.exception('error loading XML file')
            wx.LogError('Error loading XML file: %s' % path)
            raise
            
    def save(self, path):
        # Apply changes if needed
        if not self.applied:
            self.update(view.tree.GetSelection())
        try:
            tmpFile,tmpName = tempfile.mkstemp(prefix='xrced-')
            os.close(tmpFile)
            TRACE('Saving temporaty file: %s', tmpName)
            self.saveXML(tmpName)
            TRACE('moving to main: %s', path)
            shutil.move(tmpName, path)
            self.path = path
            self.setModified(False)
        except:
            logger.exception('error saving XML file')
            wx.LogError('Error saving XML file: %s' % path)
            raise

    def setModified(self, state=True):
        '''Set global modified state.'''
        self.modified = state
        # Set applied flag
        if not state: self.applied = True
        name = os.path.basename(self.path)
        if not name: name = 'UNTITLED'
        # Update GUI
        if state:
            view.frame.SetTitle(progname + ': ' + name + ' *')
        else:
            view.frame.SetTitle(progname + ': ' + name)

    def setApplied(self, state=True):
        '''Set panel state.'''
        self.applied = state
        if not state and not self.modified: 
            self.setModified()  # toggle global state

    def createUndoEdit(self, item=None, page=None):
        # Create initial undo object
        if item is None: item = view.tree.GetSelection()
        if page is None: page = view.panel.nb.GetSelection()
        view.panel.undo = undo.UndoEdit(item, page)

    def registerUndoEdit(self):
        g.undoMan.RegisterUndo(view.panel.undo)
        view.panel.undo = None

    def panelIsDirty(self):
        '''Check if the panel was changed since last undo.'''
        # Register undo
        if view.panel.undo:
            panel = view.panel.GetActivePanel()
            if view.panel.undo.values != panel.GetValues():
                return True
        return False

    def setData(self, item):
        '''Set data and view for current tree item.'''

        if not item or item == view.tree.root:
            TRACE('setData: root node')
            self.container = None
            self.comp = Manager.rootComponent
#            self.panels = []
#            view.panel.Clear()
            self.panels = view.panel.SetData(self.container, self.comp, Model.mainNode)
            # Create new pending undo
            self.createUndoEdit(view.tree.root)
        else:
            node = view.tree.GetPyData(item)
            className = node.getAttribute('class')
            TRACE('setData: %s', className)
            self.comp = Manager.components[className]
            parentItem = view.tree.GetItemParent(item)
            parentNode = view.tree.GetPyData(parentItem)
            if parentNode == Model.mainNode:
                self.container = Manager.rootComponent
            else:
                parentClass = parentNode.getAttribute('class')
                self.container = Manager.components[parentClass]
            self.panels = view.panel.SetData(self.container, self.comp, node)
            # Create new pending undo
            self.createUndoEdit(item)

        if view.testWin.object:
            self.highlight(item)        

    def highlight(self, item):
        try:
            obj = view.testWin.FindObject(item)
            if obj:
                rect = self.comp.getRect(obj)
                print rect
                if rect is not None:
                    # If framed object use external frame
                    #if obj == view.testWin.object and view.testWin.frame:
                    #    rect.x = rect.y = 10
                    view.testWin.Highlight(rect)
                # Special highlighting for sizers
                if isinstance(obj, wx.Sizer):
                    for sizerItem in obj.GetChildren():
                        rect = sizerItem.GetRect()
                        view.testWin.HighlightSizerItem(rect)
                    
        except:
            logger.exception('highlighting failed')

    def popupMenu(self, forceSibling, forceInsert, pos):
        '''Show popup menu and set sibling/insert flags.'''
        if self.container:
            if self.comp.isContainer():
                self.createSibling = forceSibling
            else:
                self.createSibling = True
        else:
            self.createSibling = False
        self.insertBefore = forceInsert
        menu = view.XMLTreeMenu(self.container, self.comp, view.tree,
                                self.createSibling, self.insertBefore)
        view.tree.PopupMenu(menu, pos)
        menu.Destroy()        

    def create(self, comp, child=None):
        '''
        Add DOM node as child or sibling depending on flags. Return new item.

        If child is passed replace by existing data.
        '''
        if child is None:
            child = Model.createObjectNode(comp.klass)
        data = wx.TreeItemData(child)
        item = view.tree.GetSelection()
        if not item: 
            item = view.tree.root
        elif not self.applied:
            self.update(item)
        if item == view.tree.root:
            self.createSibling = False # can't create sibling of root
        if self.createSibling:
            parentItem = view.tree.GetItemParent(item)
            parentNode = view.tree.GetPyData(parentItem)
        else:
            parentNode = view.tree.GetPyData(item)
        label = comp.getTreeText(child)
        imageId = comp.getTreeImageId(child)
        if self.createSibling:
            node = view.tree.GetPyData(item)
            if self.insertBefore:
                self.container.insertBefore(parentNode, child, node)
                item = view.tree.InsertItemBefore(
                    parentItem, item, label, imageId, data=data)

            else:
                self.container.insertAfter(parentNode, child, node)
                item = view.tree.InsertItem(
                    parentItem, item, label, imageId, data=data)
        else:
            if self.insertBefore and view.tree.ItemHasChildren(item):
                nextNode = view.tree.GetPyData(view.tree.GetFirstChild(item)[0])
                self.comp.insertBefore(parentNode, child, nextNode)
                item = view.tree.PrependItem(item, label, imageId, data=data)
            else:
                self.comp.appendChild(parentNode, child)
                item = view.tree.AppendItem(item, label, imageId, data=data)
        view.tree.EnsureVisible(item)
        view.tree.UnselectAll()
#        wx.Yield()
        view.tree.SelectItem(item)
        self.setModified()
        # Refresh test window after finishing
        if g.conf.autoRefresh and view.testWin.IsShown():
            self.refreshTestWin()
        return item

    def replace(self, comp, node=None):
        '''Replace DOM node by new or passed node. Return new item.'''
        if node is None:
            node = Model.createObjectNode(comp.klass)
        if not self.applied:
            self.update(item)
        data = wx.TreeItemData(node)
        item = view.tree.GetSelection()
        parentItem = view.tree.GetItemParent(item)
        parentNode = view.tree.GetPyData(parentItem)
        oldNode = view.tree.GetPyData(item)
        self.container.replaceChild(parentNode, node, oldNode)
        # Replace tree item: insert new, remove old
        label = comp.getTreeText(node)
        imageId = comp.getTreeImageId(node)
        item = view.tree.InsertItem(parentItem, item, label, imageId, data=data)
        view.tree.Delete(view.tree.GetPrevSibling(item))
        # Add children
        for n in filter(is_object, node.childNodes):
            view.tree.AddNode(item, comp.getTreeNode(n))
        view.tree.EnsureVisible(item)
        # Update panel
        view.tree.SelectItem(item)
        self.setModified()
        return item

    def update(self, item):
        '''Update DOM with new attribute values. Update tree if necessary.'''
        if not item: item = view.tree.root
        node = view.tree.GetPyData(item)
        if self.comp and self.comp.hasName:
            name = view.panel.controlName.GetValue()
            if name:
                node.setAttribute('name', view.panel.controlName.GetValue())
            elif node.hasAttribute('name'): # clean up empty names
                node.removeAttribute('name')
        for panel in self.panels:
            if not panel.node: continue
            # Replace node contents except object children
            for n in panel.node.childNodes[:]:
                if not is_object(n):
                    panel.node.removeChild(n)
                    n.unlink()
        for panel in self.panels:
            if panel.node:
                panelNode = panel.node
            else:
                panelNode = node
            for a,value in panel.GetValues():
                if value: 
                    try:
                        self.comp.addAttribute(panelNode, a, value)
                    except:
                        logging.exception('addAttribute error: %s %s', a, value)
        if item != view.tree.root:
            view.tree.SetItemImage(item, self.comp.getTreeImageId(node))
            view.tree.SetItemText(item, self.comp.getTreeText(node))
        self.setApplied()
        self.undoSaved = False
        # Set dirty flag
        if view.testWin.IsShown():
            view.testWin.isDirty = True

    def unselect(self):
        if not self.applied:
            item = view.tree.GetSelection()
            if not item: item = view.tree.root
            self.update(item)
        view.tree.UnselectAll()
        self.setData(view.tree.root)

    def delete(self, item):
        '''Delete selected object(s).'''
        parentItem = view.tree.GetItemParent(item)
        parentNode = view.tree.GetPyData(parentItem)
        node = view.tree.GetPyData(item)
        node = self.container.removeChild(parentNode, node)
        view.tree.Delete(item)
        self.unselect()
        self.setApplied()
        self.setModified()
        return node

    def deleteMany(self, items):
        '''Delete selected object(s).'''
        for item in items:
            if not item: continue # child already deleted
            parentItem = view.tree.GetItemParent(item)
            parentNode = view.tree.GetPyData(parentItem)
            node = view.tree.GetPyData(item)
            node = self.container.removeChild(parentNode, node)
            node.unlink()       # delete completely
            view.tree.Delete(item)
        self.unselect()
        self.setApplied()
        self.setModified()

    def cut(self):
        self.copy()
        self.delete(view.tree.GetSelection())

    def copy(self):
        # Update values from panel first
        item = view.tree.GetSelection()
        if not self.applied:
            self.update(item)
        node = view.tree.GetPyData(item)
        if wx.TheClipboard.Open():
            if node.nodeType == node.ELEMENT_NODE:
                data = wx.CustomDataObject('XRCED_elem')
                s = node.toxml(encoding=expat.native_encoding)
            else:
                data = wx.CustomDataObject('XRCED_node')
                s = node.data
            data.SetData(cPickle.dumps(s))
            wx.TheClipboard.SetData(data)
            wx.TheClipboard.Close()
        else:
            wx.MessageBox("Unable to open the clipboard", "Error")        

    def paste(self):
        success = success_node = False
        if wx.TheClipboard.IsOpened() or wx.TheClipboard.Open():
            try:
                data = wx.CustomDataObject('XRCED_elem')
                if wx.TheClipboard.IsSupported(data.GetFormat()):
                    try:
                        success = wx.TheClipboard.GetData(data)
                    except:
                        # there is a problem if XRCED_node is in clipboard
                        # but previous SetData was for XRCED
                        pass
                if not success:             # try other format
                    data = wx.CustomDataObject('XRCED_node')
                    if wx.TheClipboard.IsSupported(data.GetFormat()):
                        success_node = wx.TheClipboard.GetData(data)
            finally:
                wx.TheClipboard.Close()

        if not success and not success_node:
            wx.MessageBox(
                "There is no data in the clipboard in the required format",
                "Error")
            return

        # XML representation of element or node value string
        data = cPickle.loads(data.GetData()) 
        if success:
            node = Model.parseString(data)
            comp = Manager.components[node.getAttribute('class')]
        else:
            node = Model.dom.createComment(data)
            raise NotImplementedError

        # Check compatibility
        if self.createSibling: container = self.container
        else: container = self.comp
        if not container.canHaveChild(comp):
            wx.LogError('Incompatible parent/child: parent is %s, child is %s!' %
                        (container.klass, comp.klass))
            node.unlink()
            return

        item = view.tree.GetSelection()
        if item and not self.applied:
            self.update(item)
        
        item = self.create(comp, node)
        # Add children
        for n in filter(is_object, node.childNodes):
            view.tree.AddNode(item, comp.getTreeNode(n))
        self.setModified()
        
    def createLocalConf(self, path):
        name = os.path.splitext(path)[0]
        name += '.xcfg'
        return wx.FileConfig(localFilename=name)

    def createTestWin(self, item):
        # Create a window with this resource
        node = view.tree.GetPyData(item)
        # Close old window, remember where it was
        highLight = None
        comp = Manager.getNodeComp(node)
        # Create memory XML file
        elem = node.cloneNode(True)
        if not node.hasAttribute('name'):
            name = 'noname'
        else:
            name = node.getAttribute('name')
        elem.setAttribute('name', STD_NAME)
        Model.setTestElem(elem)
        Model.saveTestMemoryFile()
        xmlFlags = xrc.XRC_NO_SUBCLASSING
        # Use translations if encoding is not specified
        if not Model.dom.encoding:
            xmlFlags != xrc.XRC_USE_LOCALE
        res = xrc.EmptyXmlResource(xmlFlags)
        xrc.XmlResource.Set(res)        # set as global
        # Init other handlers
        Manager.addXmlHandlers(res)
        # Same module list
        res.Load('memory:test.xrc')
        object = None
        try:
            try:
                frame, object = comp.makeTestWin(res, name)
                # Reset tree item and locate tool
                if view.testWin.item:
                    view.tree.SetItemBold(view.testWin.item, False)
                    view.frame.tb.ToggleTool(view.frame.ID_TOOL_LOCATE, False)
                    view.frame.miniFrame.tb.ToggleTool(view.frame.ID_TOOL_LOCATE, False)
                view.testWin.SetView(frame, object, item)
                view.testWin.Show()
                view.testWin.isDirty = False
                view.tree.SetItemBold(item, True)
            except NotImplementedError:
                wx.LogError('Test window not implemented for %s' % node.getAttribute('class'))
            except:
                logger.exception('error creating test view')
                wx.LogError('Error creating test view')
                if debug: raise
        finally:
            # Cleanup
            res.Unload(TEST_FILE)
            xrc.XmlResource.Set(None)
            wx.MemoryFSHandler.RemoveFile(TEST_FILE)
        return object

    def closeTestWin(self):
        if not view.testWin.object: return
        view.tree.SetItemBold(view.testWin.item, False)
        view.frame.tb.ToggleTool(view.frame.ID_TOOL_LOCATE, False)
        view.frame.miniFrame.tb.ToggleTool(view.frame.ID_TOOL_LOCATE, False)
        # Remember dimensions
        view.testWin.pos = view.testWin.GetFrame().GetPosition()
        view.testWin.size = view.testWin.GetFrame().GetSize()
        view.testWin.Destroy()

    def refreshTestWin(self):
        '''Refresh test window after some change.'''
        if not view.testWin.object: return
        TRACE('refreshTestWin')
        # Dumb refresh
        self.createTestWin(view.testWin.item)

    def showXML(self):
        '''Show some source.'''
        item = view.tree.GetSelection()
        if not item: item = view.tree.root
        node = view.tree.GetPyData(item)
        dom = MyDocument()
        node = dom.appendChild(node.cloneNode(True))
        Model.indent(dom, node)
        text = node.toxml()#Model.dom.encoding)
        dom.unlink()
        lines = text.split('\n')
        maxLen = max(map(len, lines))
        w = max(40, min(80, maxLen))
        h = max(20, min(40, len(lines)))
        dlg = view.ScrolledMessageDialog(view.frame, text, 'XML Source',
                                         textSize=(w,h), centered=False)
        dlg.Bind(wx.EVT_CLOSE, lambda evt: dlg.Destroy())
        dlg.Bind(wx.EVT_BUTTON, lambda evt: dlg.Destroy(), id=wx.ID_OK)
        dlg.Show()

# Singleton class
Presenter = _Presenter()

undo.Presenter = Presenter
