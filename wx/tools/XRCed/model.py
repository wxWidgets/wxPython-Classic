# Name:         model.py
# Purpose:      Model class and related
# Author:       Roman Rolinsky <rolinsky@femagsoft.com>
# Created:      07.06.2007
# RCS-ID:       $Id$

import os,sys
from xml.dom import minidom
from globals import *

# Redefine writing to include encoding
class MyDocument(minidom.Document):
    def __init__(self):
        minidom.Document.__init__(self)
        self.encoding = ''
    def writexml(self, writer, indent="", addindent="", newl="", encoding=""):
        if encoding: encdstr = 'encoding="%s"' % encoding
        else: encdstr = ''
        writer.write('<?xml version="1.0" %s?>\n' % encdstr)
        for node in self.childNodes:
            node.writexml(writer, indent, addindent, newl)

# Model object is used for data manipulation
class _Model:
    def __init__(self):
        self.dom = None

    def init(self, dom=None):
        if self.dom: self.dom.unlink()
        if not dom:
            self.dom = MyDocument()
            self.mainNode = self.dom.createElement('resource')
            self.dom.appendChild(self.mainNode)
            # Dummy node to be replaced by the node being tested
            self.testElem = self.dom.createElement('dummy')
        else:
            self.dom = dom
            self.testElem = self.dom.createElement('dummy')
            self.mainNode = dom.documentElement
        # Test element node is always first
        self.mainNode.insertBefore(self.testElem, self.mainNode.firstChild)

    def loadXML(self, path):
        f = open(path)
        dom = minidom.parse(f)
        f.close()
        self.init(dom)

        # Set encoding global variable and default encoding
        if dom.encoding:
            g.currentEncoding = dom.encoding
            wx.SetDefaultPyEncoding(g.currentEncoding.encode())
        else:
            g.currentEncoding = ''
        
    def saveXML(self, path):
        if g.currentEncoding:
            import codecs
            f = codecs.open(path, 'wt', g.currentEncoding)
        else:
            f = open(path, 'wt')
        # Make temporary copy for formatting it
        domCopy = MyDocument()
        mainNode = domCopy.appendChild(self.mainNode.cloneNode(True))
        # Remove first child (testElem)
        mainNode.removeChild(mainNode.firstChild).unlink()
        self.indent(domCopy, mainNode)
        domCopy.writexml(f, encoding = g.currentEncoding)
        f.close()
        domCopy.unlink()

    def saveTestMemoryFile(self):
        # Save in memory FS
        memFile = MemoryFile(TEST_FILE)
        encd = self.dom.encoding
        if not encd: encd = None
        try:
            self.dom.writexml(memFile, encoding=encd)
        except:
            inf = sys.exc_info()
            wx.LogError(traceback.format_exception(inf[0], inf[1], None)[-1])
            wx.LogError('Error writing temporary file')
        memFile.close()                 # write to wxMemoryFS        

    def indent(self, domCopy, node, indent = 0):
        '''Indent node which must be a comment or an element node and children.'''
        if indent != 0:
            prevNode = node.previousSibling
            if prevNode and prevNode.nodeType == prevNode.TEXT_NODE:
                prevNode.data = '\n' + ' ' * indent
            else:
                text = domCopy.createTextNode('\n' + ' ' * indent)
                node.parentNode.insertBefore(text, node)
        # Indent element/comment children recurcively
        if node.hasChildNodes():
            lastIndented = None
            for n in node.childNodes[:]:
                if n.nodeType in [n.ELEMENT_NODE, n.COMMENT_NODE]:
                    self.indent(domCopy, n, indent + 2)
                    lastIndented = n

            # Insert newline after last element/comment child
            if lastIndented:
                n = lastIndented.nextSibling
                if n and n.nodeType == n.TEXT_NODE:
                    n.data = '\n' + ' ' * indent
                else:
                    text = domCopy.createTextNode('\n' + ' ' * indent)
                    node.appendChild(text)

    def createObjectNode(self, className):
        node = self.dom.createElement('object')
        node.setAttribute('class', className)
        return node

    def parseString(self, data):
        return minidom.parseString(data).childNodes[0]

    def setTestElem(self, elem):
        oldTestElem = Model.testElem
        self.testElem = elem
        self.mainNode.replaceChild(elem, oldTestElem)
        oldTestElem.unlink()

Model = _Model()

class MemoryFile:
    '''Memory file proxy for python-like file object.'''
    def __init__(self, name):
        self.name = name
        self.buffer = ''
    def write(self, data):
        if g.currentEncoding:
            encoding = g.currentEncoding
        else:
            encoding = wx.GetDefaultPyEncoding()
        try:
            self.buffer += data.encode(encoding)
        except UnicodeEncodeError:
            self.buffer += data.encode(encoding, 'xmlcharrefreplace')
            
    def close(self):
        wx.MemoryFSHandler.AddFile(self.name, self.buffer)
