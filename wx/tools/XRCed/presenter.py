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
from model import Model
from component import Manager

# Presenter class linking model to view objects
class _Presenter:
    def init(self):
        Model.init()
        self.path = ''
        # Global modified state
        self.setModified(False)
        view.frame.Clear()
        view.tree.Clear()
        view.tree.SetPyData(view.tree.root, Model.mainNode)
        view.panel.Clear()
        view.testWin.Init()
        self.panels = []
        self.comp = Manager.rootComponent # component shown in panel (or the root component)
        self.container = None           # current container (None if root)
        # Insert/append mode flags
        self.createSibling = self.insertBefore = False

    def loadXML(self, path):
        Model.loadXML(path)
        view.tree.Flush()
        view.tree.SetPyData(view.tree.root, Model.mainNode)

    def saveXML(self, path):
        Model.saveXML(path)

    def open(self, path):
        if not os.path.exists(path):
            wx.LogError('File does not exists: %s' % path)
            return False
        try:
            self.path = os.path.abspath(path)
            self.loadXML(self.path)
            # Change dir
            dir = os.path.dirname(self.path)
            if dir: os.chdir(dir)
            self.setModified(False)
            g.conf.localconf = self.createLocalConf(path)
        except:
            inf = sys.exc_info()
            wx.LogError('Error reading file: %s' % path)
            if debug: raise
            return False
        return True
            
    def save(self, path):
        # Apply changes if needed
        if not self.applied:
            self.update(view.tree.GetSelection())
        try:
            tmpFile,tmpName = tempfile.mkstemp(prefix='xrced-')
            os.close(tmpFile)
            self.saveXML(tmpName)
            shutil.move(tmpName, path)
            self.path = path
            self.setModified(False)
        except:
            inf = sys.exc_info()
            wx.LogError('Error writing file: %s' % path)
            if debug: raise
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

    def setData(self, item):
        '''Set data and view for current tree item.'''
        if not item or item == view.tree.root:
            self.container = None
            self.comp = Manager.rootComponent
            self.panels = []
            view.panel.Clear()
        else:
            node = view.tree.GetPyData(item)
            className = node.getAttribute('class')
            self.comp = Manager.components[className]
            parentItem = view.tree.GetItemParent(item)
            parentNode = view.tree.GetPyData(parentItem)
            if parentNode == Model.mainNode:
                self.container = Manager.rootComponent
            else:
                parentClass = parentNode.getAttribute('class')
                self.container = Manager.components[parentClass]
            self.panels = view.panel.SetData(self.container, self.comp, node)

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
        if self.createSibling:
            node = view.tree.GetPyData(item)
            if self.insertBefore:
                self.container.insertBefore(parentNode, child, node)
                item = view.tree.InsertItemBefore(parentItem, item, comp.klass, 
                                                  comp.getTreeImageId(child), data=data)

            else:
                self.container.insertAfter(parentNode, child, node)
                item = view.tree.InsertItem(parentItem, item, comp.klass, 
                                            comp.getTreeImageId(child), data=data)
        else:
            if self.insertBefore and view.tree.ItemHasChildren(item):
                nextNode = view.tree.GetPyData(view.tree.GetFirstChild(item)[0])
                self.comp.insertBefore(parentNode, child, nextNode)
                item = view.tree.PrependItem(item, comp.klass, 
                                             comp.getTreeImageId(child), data=data)
            else:
                self.comp.appendChild(parentNode, child)
                item = view.tree.AppendItem(item, comp.klass, 
                                            comp.getTreeImageId(child), data=data)
        view.tree.EnsureVisible(item)
        view.tree.UnselectAll()
        wx.Yield()
        view.tree.SelectItem(item)
        self.setModified()
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
        item = view.tree.InsertItem(parentItem, item, comp.klass, 
                                    comp.getTreeImageId(node), data=data)
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
                    self.comp.addAttribute(panelNode, a, value)
        view.tree.SetItemImage(item, self.comp.getTreeImageId(node))
        self.setApplied()

    def unselect(self):
        item = view.tree.GetSelection()
        if item and not self.applied:
            self.update(item)
        view.panel.Clear()
        # Reset variables
        self.comp = Manager.rootComponent
        self.container = None
        view.tree.UnselectAll()
        #view.tree.Flush()

    def delete(self):
        '''Delete selected object(s).'''
        item = view.tree.GetSelection()
        parentItem = view.tree.GetItemParent(item)
        parentNode = view.tree.GetPyData(parentItem)
        for item in view.tree.GetSelections():
            node = view.tree.GetPyData(item)
            if parentItem == view.tree.root:
                Model.mainNode.removeChild(node)
            else:
                self.container.removeChild(parentNode, node)
            node.unlink()
            view.tree.Delete(item)
        view.panel.Clear()
        # Reset variables
        self.comp = Manager.rootComponent
        self.container = None
        self.setApplied()
        self.setModified()

    def cut(self):
        self.copy()
        self.delete()

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
        klass = node.getAttribute('class')
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
        if not g.currentEncoding:
            xmlFlags != xrc.XRC_USE_LOCALE
        res = xrc.EmptyXmlResource(xmlFlags)
        res.InitAllHandlers()
        xrc.XmlResource.Set(res)        # set as global
        # Register handlers
#        addHandlers()
        # Same module list
        res.Load('memory:test.xrc')
        object = None
        try:
            try:
                frame, object = self.comp.makeTestWin(res, name)
                view.testWin.SetView(frame, object, item)
                view.testWin.Show()
                view.tree.SetItemBold(item, True)
            except NotImplementedError:
                wx.LogError('Test window not implemented for %s' % node.getAttribute('class'))
            except:
                wx.LogError('Error loading resource: %s' % sys.exc_value)
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
        view.testWin.pos = view.testWin.GetFrame().GetPosition()
        view.testWin.size = view.testWin.GetFrame().GetSize()
        view.testWin.Destroy()

# Singleton class
Presenter = _Presenter()
