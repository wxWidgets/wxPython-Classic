# Name:         attribute.py
# Purpose:      Attribute classes
# Author:       Roman Rolinsky <rolinsky@femagsoft.com>
# Created:      25.06.2007
# RCS-ID:       $Id$

import cPickle
from model import Model

class Attribute:
    '''Base class for defining attributes.'''
    def add(parentNode, attribute, value):
        if attribute == '':
            elem = parentNode
        else:
            elem = Model.dom.createElement(attribute)
            parentNode.appendChild(elem)
        text = Model.dom.createTextNode(value)
        elem.appendChild(text)
    add = staticmethod(add)
    def get(node):
        '''Get text.'''
        try:
            n = node.childNodes[0]
            return n.wholeText
        except IndexError:
            return ''
    get = staticmethod(get)

class ContentAttribute:
    '''Content attribute class. Value is a list of strings.'''
    def add(parentNode, attribute, value):
        contentElem = Model.dom.createElement(attribute)
        parentNode.appendChild(contentElem)
        for item in value:
            elem = Model.dom.createElement('item')
            text = Model.dom.createTextNode(item)
            elem.appendChild(text)
            contentElem.appendChild(elem)
    add = staticmethod(add)
    def get(node):
        value = []
        for n in node.childNodes:
            if n.nodeType == node.ELEMENT_NODE and n.tagName == 'item':
                value.append(Attribute.get(n))
        return value
    get = staticmethod(get)

class CheckContentAttribute:
    '''CheckList content. Value is a list of tuples (checked, string).'''
    def add(parentNode, attribute, value):
        contentElem = Model.dom.createElement(attribute)
        parentNode.appendChild(contentElem)
        for checked,item in value:
            elem = Model.dom.createElement('item')
            if checked:
                elem.setAttribute('checked', '1')
            text = Model.dom.createTextNode(item)
            elem.appendChild(text)
            contentElem.appendChild(elem)
    add = staticmethod(add)
    def get(node):
        value = []
        for n in node.childNodes:
            if n.nodeType == node.ELEMENT_NODE and n.tagName == 'item':
                checked = bool(n.getAttribute('checked'))
                value.append((checked, Attribute.get(n)))
        return value
    get = staticmethod(get)

class DictAttribute:
    '''Font attribute class. Value is a dictionary of font attribtues.'''
    attributes = []
    @classmethod
    def add(cls, parentNode, attribute, value):
        fontElem = Model.dom.createElement(attribute)
        parentNode.appendChild(fontElem)
        for a in filter(value.has_key, cls.attributes):
            elem = Model.dom.createElement(a)
            text = Model.dom.createTextNode(value[a])
            elem.appendChild(text)
            fontElem.appendChild(elem)
    @staticmethod
    def get(node):
        value = {}
        for n in node.childNodes:
            if n.nodeType == node.ELEMENT_NODE:
                value[n.tagName] = Attribute.get(n)
        return value

class FontAttribute(DictAttribute):
    attributes = ['size', 'style', 'weight', 'underlined', 'family', 'face', 'encoding', 
                  'sysfont', 'relativesize']

class CodeAttribute(DictAttribute):
    attributes = ['events', 'assign_var']

class MultiAttribute:
    '''Repeated attribute like growablecols.'''
    def add(parentNode, attribute, value):
        for v in value:
            elem = Model.dom.createElement(attribute)
            parentNode.appendChild(elem)
            text = Model.dom.createTextNode(v)
            elem.appendChild(text)
    add = staticmethod(add)
    def get(node):
        tag = node.tagName  # remember tag name
        value = []
        # Look for multiple tags
        while node:
            if node.nodeType == node.ELEMENT_NODE and node.tagName == tag:
                value.append(Attribute.get(node))
            node = node.nextSibling
        return value
    get = staticmethod(get)

class BitmapAttribute:
    '''Bitmap attribute.'''
    def add(parentNode, attribute, value):
        if attribute == 'object':
            elem = parentNode
        else:
            elem = Model.dom.createElement(attribute)
            parentNode.appendChild(elem)
        if value[0]:
            elem.setAttribute('stock_id', value[0])
        else:
            if elem.hasAttribute('stock_id'): elem.removeAttribute('stock_id')
            text = Model.dom.createTextNode(value[1])
            elem.appendChild(text)
    add = staticmethod(add)
    def get(node):
        return [node.getAttribute('stock_id'), Attribute.get(node)]
    get = staticmethod(get)
            
class AttributeAttribute:
    '''Attribute as an XML attribute of the element node.'''
    def add(elem, attribute, value):
        if value:
            elem.setAttribute(attribute, value)
        else:
            if elem.hasAttribute(attribute): elem.removeAttribute(attribute)
    add = staticmethod(add)
    def getAA(elem, attribute):
        return elem.getAttribute(attribute)
    getAA = staticmethod(getAA)

class EncodingAttribute(AttributeAttribute):
    '''Encoding is a special attribute stored in dom object.'''
    def add(elem, attribute, value):
        Model.dom.encoding = value
    add = staticmethod(add)
    def getAA(elem, attribute):
        return Model.dom.encoding
    getAA = staticmethod(getAA)
            
class CDATAAttribute(Attribute):
    def add(parentNode, attribute, value):
        '''value is a dictionary.'''
        if value:
            elem = Model.dom.createElement(attribute)
            parentNode.appendChild(elem)
            data = Model.dom.createCDATASection(cPickle.dumps(value))
            elem.appendChild(data)
    add = staticmethod(add)
    def get(node):
        '''Get XRCED data from a CDATA text node.'''
        try:
            n = node.childNodes[0]
            if n.nodeType == n.CDATA_SECTION_NODE:
                return cPickle.loads(n.wholeText.encode())
        except IndexError:
            pass
    get = staticmethod(get)
    
