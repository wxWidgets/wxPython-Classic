# Name:         component.py
# Purpose:      base component classes
# Author:       Roman Rolinsky <rolinsky@femagsoft.com>
# Created:      31.05.2007
# RCS-ID:       $Id$

import os,sys,bisect
import wx
from sets import Set
from globals import *
from model import Model
from attribute import *
import params
import view
import images

# Group compatibility specifications. 
# Key is the parent group, value is the list of child groups.
# !value means named main group is excluded from possible children.
# "root" is a special group for the tree root
parentChildGroups = {
    'root': ['top_level', 'component'],      # top-level objects
    'frame': ['toolbar', 'menubar', 'statusbar'],
    'window': ['control', 'window', 'sizer', '!frame'],
    'sizer': ['control', 'sizer', 'spacer'],
    'menubar': ['menu'],
    'toolbar': ['tool', 'separator'],
    'menu': ['menu', 'menu_item', 'separator']
}

class Component(object):
    '''Base component class.'''
    # Common window attributes
    windowAttributes = ['fg', 'bg', 'font', 'tooltip', 'help', 
                        'enabled', 'focused', 'hidden']
    genericStyles = [
        'wxSIMPLE_BORDER', 'wxSUNKEN_BORDER', 'wxDOUBLE_BORDER',
        'wxRAISED_BORDER', 'wxSTATIC_BORDER', 'wxNO_BORDER',
        'wxCLIP_CHILDREN', 'wxTRANSPARENT_WINDOW', 'wxWANTS_CHARS',
        'wxNO_FULL_REPAINT_ON_RESIZE', 'wxFULL_REPAINT_ON_RESIZE'
        ]
    genericExStyles = [
        'wxWS_EX_VALIDATE_RECURSIVELY',
        'wxWS_EX_BLOCK_EVENTS',
        'wxWS_EX_TRANSIENT',
        'wxFRAME_EX_CONTEXTHELP',
        'wxWS_EX_PROCESS_IDLE',
        'wxWS_EX_PROCESS_UI_UPDATES'
        ]
    hasName = True                      # most elements have XRC IDs
    isTopLevel = False                  # if can be created as top level window
    renameDict = {}
    def __init__(self, klass, groups, attributes, **kargs):
        self.klass = klass
        self.groups = groups
        self.attributes = attributes
        self.styles = []
        self.exStyles = []
        self.defaults = kargs.get('defaults', {})
        # Special Attribute classes if required
        self.specials = kargs.get('specials', {'font': FontAttribute})
        # Special Param classes if required
        self.params = kargs.get('params', {})
        # Tree image
        if 'images' in kargs:
            self.images = kargs['images']
        elif 'image' in kargs:
            self.images = [kargs['image']]
        elif not 'image' in self.__dict__:
            self.images = []

    def addStyles(self, *styles):
        self.styles.extend(styles)

    def addExStyles(self, *styles):
        self.exStyles.extend(styles)

    def setSpecial(self, attrName, attrClass):
        '''Set special Attribute class.'''
        self.specials[attrName] = attrClass

    def setParamClass(self, attrName, paramClass):
        '''Set special Param class.'''
        self.params[attrName] = paramClass

    def getTreeImageId(self, node):
        try:
            return self.images[0].Id
        except IndexError:
            return 0

    def getTreeText(self, node):
        label = node.getAttribute('class')
        if self.hasName:
            name = node.getAttribute('name')
            if name: label += ' "%s"' % name
        return label

    # Order components having same index by group and klass
    def __cmp__(self, other):
        if self.groups < other.groups: return -1
        elif self.groups == other.groups: 
            if self.klass < other.klass: return -1
            elif self.klass == other.klass: return 0
            else: return 1
        else: return 1

    def __repr__(self):
        return "Component('%s', %s)" % (self.klass, self.attributes)

    def canHaveChild(self, component):
        '''True if the current component can have child of given type.

        This function is redefined by container classes.'''
        return False

    def canBeReplaced(self, component):
        '''True if the current component can be replaced by component.

        This function can be redefined by derived classes.'''
        return component.groups == groups

    def isContainer(self):
        return isinstance(self, Container)

    def getAttribute(self, node, attribute):
        attrClass = self.specials.get(attribute, Attribute)
        if attribute == 'object':    # object means element node
            return attrClass.get(node)
        for n in node.childNodes:
            if n.nodeType == node.ELEMENT_NODE and n.tagName == attribute:
                return attrClass.get(n)
        return ''

    def addAttribute(self, node, attribute, value):
        '''Add attribute element.'''
        attrClass = self.specials.get(attribute, Attribute)
        attrClass.add(node, attribute, value)

    def makeTestWin(self, res, name):
        '''Method can be overrided by derived classes to create test view.'''
        if not self.hasName: raise NotImplementedError

        if self.isTopLevel:
            # Top-level window creates frame itself
            frame = None
            object = res.LoadObject(None, STD_NAME, self.klass)
        else:
            frame = view.testWin.frame
            if not frame:
                frame = wx.MiniFrame(None, -1, '%s: %s' % (self.klass, name), name=STD_NAME,
                                     style=wx.CAPTION|wx.CLOSE_BOX|wx.RESIZE_BORDER)
                frame.panel = wx.Panel(frame)
            else:                       # reuse present frame
                view.testWin.object.Destroy()
            object = res.LoadObject(frame.panel, STD_NAME, self.klass)
            object.SetPosition((10,10))
            object.Fit()
            if not isinstance(object, wx.Window): raise NotImplementedError
            if not view.testWin.frame:
                frame.SetClientSize(object.GetSize()+(20,20))
        return frame, object

    def copyAttributes(self, srcNode, dstNode):
        '''Copy relevant attribute nodes from oldNode to newNode.'''
        dstComp = Manager.getNodeComp(dstNode)
        for n in srcNode.childNodes:
            if n.nodeType == n.ELEMENT_NODE:
                a = n.tagName
                # Check if attributes are compatible
                srcAttrClass = self.specials.get(a, Attribute)
                dstAttrClass = dstComp.specials.get(a, Attribute)
                if srcAttrClass is not dstAttrClass: continue
                srcParamClass = self.params.get(a, params.paramDict.get(a, params.ParamText))
                dstParamClass = dstComp.params.get(a, params.paramDict.get(a, params.ParamText))
                if srcParamClass is not dstParamClass: continue
                # Style and exstyle are not in attributes and can be treated specially
                if a == 'style':
                    styles = self.getAttribute(srcNode, a).split('|')
                    allStyles = dstComp.styles + params.genericStyles
                    dstStyles = [s for s in styles if s.strip() in allStyles]
                    if dstStyles:
                        dstComp.addAttribute(dstNode, a, '|'.join(dstStyles))
                elif a == 'exstyle':
                    styles = self.getAttribute(srcNode, a).split('|')
                    allStyles = dstComp.exStyles + params.genericExStyles
                    dstStyles = [s for s in styles if s.strip() in allStyles]
                    if dstStyles:
                        dstComp.addAttribute(dstNode, a, '|'.join(dstStyles))
                elif a in dstComp.attributes:
                    value = self.getAttribute(srcNode, a)
                    dstComp.addAttribute(dstNode, a, value)


class SimpleComponent(Component):
    '''Component without window attributes and styles.'''
    windowAttributes = []
    genericStyles = genericExStyles = []


class Container(Component):
    '''Base class for containers.'''
    def canHaveChild(self, component):
        # Test exclusion first
        for g in self.groups:
            if '!'+component.groups[0] in parentChildGroups.get(g, []): return False
        # Test for any possible parent-child
        groups = Set(component.groups)
        for g in self.groups:
            if groups.intersection(parentChildGroups.get(g, [])):
                return True
        return False

    def requireImplicit(self, node):
        '''If there are implicit nodes for this particular node.'''
        return False

    def getTreeNode(self, node):
        '''Some containers may hide some internal elements.'''
        return node

    def getTreeOrImplicitNode(self, node):
        '''Return topmost child (implicit if exists).'''
        return node

    def appendChild(self, parentNode, node):
        '''Append child node. Can be overriden to create implicit nodes.'''
        parentNode.appendChild(node)

    def insertBefore(self, parentNode, node, nextNode):
        '''Insert node before nextNode. Can be overriden to create implicit nodes.'''
        parentNode.insertBefore(node, nextNode)

    def insertAfter(self, parentNode, node, prevNode):
        '''Insert node after prevNode. Can be overriden to create implicit nodes.'''
        parentNode.insertBefore(node, prevNode.nextSibling)

    def removeChild(self, parentNode, node):
        '''
        Remove node and the implicit node (if present). Return
        top-level removed child.
        '''
        return parentNode.removeChild(node)

    def copyObjects(self, srcNode, dstNode):
        # Copy child objects only for the same group
        dstComp = Manager.getNodeComp(dstNode)
        if self.groups[0] != dstComp.groups[0]: return
        children = []
        for n in filter(is_object, srcNode.childNodes):
            n = self.getTreeNode(n)
            if dstComp.canHaveChild(Manager.getNodeComp(n)):
                dstComp.appendChild(dstNode, n)

    def replaceChild(self, parentNode, newNode, oldNode):
        # Keep compatible children
        oldComp = Manager.getNodeComp(oldNode)
        oldComp.copyAttributes(oldNode, newNode)
        if oldComp.isContainer():
            oldComp.copyObjects(oldNode, newNode)
        parentNode.replaceChild(newNode, oldNode)


class SimpleContainer(Container):
    '''Container without window attributes and styles.'''
    windowAttributes = []
    genericStyles = genericExStyles = []


class RootComponent(Container):    
    '''Special root component.'''
    windowAttributes = []
    hasName = False


class SmartContainer(Container):
    implicitRenameDict = {}
    def __init__(self, klass, groups, attributes, **kargs):
        Container.__init__(self, klass, groups, attributes, **kargs)
        self.implicitKlass = kargs['implicit_klass']
        self.implicitPageName = kargs['implicit_page']
        self.implicitAttributes = kargs['implicit_attributes']
        # This is optional
        self.implicitParams = kargs.get('implicit_params', {})

    '''Base class for containers with implicit nodes.'''
    def getTreeNode(self, node):
        if node.getAttribute('class') == self.implicitKlass:
            for n in node.childNodes: # find first object
                if is_object(n): return n
        # Maybe some children are not implicit
        return node

    def getTreeOrImplicitNode(self, node):
        '''Return topmost child (implicit if exists).'''
        if node.parentNode.getAttribute('class') == self.implicitKlass:
            return node.parentNode
        else:
            return node

    def appendChild(self, parentNode, node):
        if self.requireImplicit(node):
            elem = Model.createObjectNode(self.implicitKlass)
            elem.appendChild(node)
            parentNode.appendChild(elem)
        else:
            parentNode.appendChild(node)

    def insertBefore(self, parentNode, node, nextNode):
        if self.requireImplicit(nextNode):
            nextNode = nextNode.parentNode
        if self.requireImplicit(node):
            elem = Model.createObjectNode(self.implicitKlass)
            elem.appendChild(node)
            parentNode.insertBefore(elem, nextNode)
        else:
            parentNode.insertBefore(node, nextNode)

    def insertAfter(self, parentNode, node, prevNode):
        if self.requireImplicit(prevNode):
            nextNode = prevNode.parentNode.nextSibling
        else:
            nextNode = prevNode.nextSibling
        if self.requireImplicit(node):
            elem = Model.createObjectNode(self.implicitKlass)
            elem.appendChild(node)
            parentNode.insertBefore(elem, nextNode)
        else:
            parentNode.insertBefore(node, nextNode)

    def removeChild(self, parentNode, node):
        if self.requireImplicit(node):
            implicitNode = node.parentNode
            #implicitNode.removeChild(node)
            return parentNode.removeChild(implicitNode)
        else:
            return parentNode.removeChild(node)

    def replaceChild(self, parentNode, newNode, oldNode):
        # Do similarly to Container for object child nodes
        oldComp = Manager.getNodeComp(oldNode)
        oldComp.copyAttributes(oldNode, newNode)
        if oldComp.isContainer():
            oldComp.copyObjects(oldNode, newNode)
        # Special treatment for implicit nodes
        if self.requireImplicit(oldNode):
            implicitNode = oldNode.parentNode
            if self.requireImplicit(newNode):
                implicitNode.replaceChild(newNode, oldNode)
            else:
                parentNode.replaceChild(newNode, implicitNode)
        else:
            if self.requireImplicit(newNode):
                elem = Model.createObjectNode(self.implicitKlass)
                elem.appendChild(newNode)
                parentNode.replaceChild(elem, oldNode)
            else:
                parentNode.replaceChild(newNode, oldNode)            

    def requireImplicit(self, node):
        # SmartContainer by default requires implicit
        return True

    def setImplicitParamClass(self, attrName, paramClass):
        '''Set special Param class.'''
        self.implicitParams[attrName] = paramClass


class Sizer(SmartContainer):
    '''Sizers are not windows and have common implicit node.'''
    windowAttributes = []
    hasName = False
    genericStyles = []
    genericExStyles = []    
    renameDict = {'orient':'orientation'}
    implicitRenameDict = {'option':'proportion'}
    def __init__(self, klass, groups, attributes, **kargs):
        kargs.setdefault('implicit_klass', 'sizeritem')
        kargs.setdefault('implicit_page', 'SizeItem')
        kargs.setdefault('implicit_attributes', ['option', 'flag', 'border', 'minsize', 'ratio'])
        kargs.setdefault('implicit_params', {'option': params.ParamInt, 
                                             'minsize': params.ParamPosSize, 
                                             'ratio': params.ParamPosSize})
        SmartContainer.__init__(self, klass, groups, attributes, **kargs)

    def requireImplicit(self, node):
        '''if there are implicit nodes for this particular component'''
        return node.getAttribute('class') != 'spacer'


class BoxSizer(Sizer):
    '''Sizers are not windows and have common implicit node.'''

    def __init__(self, klass, groups, attributes, **kargs):
        self.images = kargs.get('images', None)
        Sizer.__init__(self, klass, groups, attributes, **kargs)

    def getTreeImageId(self, node):
        if self.getAttribute(node, 'orient') == 'wxVERTICAL':
            return self.images[0].Id
        else:
            return self.images[1].Id


################################################################################
    
class _ComponentManager:
    '''Manager instance collects information from component plugins.'''
    def __init__(self):
        self.rootComponent = RootComponent('root', ['root'], ['encoding'])
        self.components = {}
        self.ids = {}
        self.firstId = self.lastId = -1
        self.menus = {}
        self.panels = {}
        self.menuNames = ['TOP_LEVEL', 'ROOT', 'bar', 'control', 'button', 'box', 
                          'container', 'sizer', 'custom']
        self.panelNames = ['Windows', 'Panels', 'Controls', 'Sizers',  'Menus', 'Custom']
        self.panelImages = {}

    def init(self):
        self.firstId = self.lastId = wx.NewId()

    def register(self, component):
        '''Register component object.'''
        TRACE('register %s' % component.klass)
        self.components[component.klass] = component
        # unique wx ID for event handling
        component.id = self.lastId = wx.NewId()
        self.ids[component.id] = component

    def forget(self, klass):
        '''Remove registered component.'''
        del self.components[klass]
        for menu,iclh in self.menus.items():
            if iclh[1].klass == klass:
                self.menus[menu].remove(iclh)
        for panel,icb in self.panels.items():
            if icb[1].klass == klass:
                self.panels[panel].remove(icb)

    def getNodeComp(self, node):
        return self.components[node.getAttribute('class')]

    def getMenuData(self, menu):
        return self.menus.get(menu, None)

    def setMenu(self, component, menu, label, help, index=1000):
        '''Set pulldown menu data.'''
        if menu not in self.menuNames: self.menuNames.append(menu)
        if menu not in self.menus: self.menus[menu] = []
        bisect.insort_left(self.menus[menu], (index, component, label, help))

    def getPanelData(self, panel):
        return self.panels.get(panel, None)

    def setTool(self, component, panel, bitmap=None, 
                pos=(1000,1000), span=(1,1)):
        '''Set toolpanel data.'''
        if panel not in self.panelNames: self.panelNames.append(panel)
        if panel not in self.panels: self.panels[panel] = []
        # Auto-select bitmap if not provided
        if not bitmap:
            bmpPath = os.path.join('bitmaps', component.klass + '.png')
            if os.path.exists(bmpPath):
                bitmap = wx.Bitmap(bmpPath)
            else:
                bitmap = images.getToolDefaultBitmap()
        bisect.insort_left(self.panels[panel], (pos, span, component, bitmap))
        
    def findById(self, id):
        return self.ids[id]

# Singleton object
Manager = _ComponentManager()
