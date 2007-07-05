# Name:         attribute.py
# Purpose:      Attribute classes
# Author:       Roman Rolinsky <rolinsky@femagsoft.com>
# Created:      25.06.2007
# RCS-ID:       $Id$

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
        '''Get collected element texts.'''
        t = ''
        for data in [n.data for n in node.childNodes if n.nodeType == node.TEXT_NODE]:
            t += data
        return t
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

class FontAttribute:
    '''Font attribute class. Value is a dictionary of font attribtues.'''
    attributes = ['size', 'style', 'weight', 'underlined', 'family', 'face', 'encoding', 
                  'sysfont', 'relativesize']
    def add(parentNode, attribute, value):
        fontElem = Model.dom.createElement('font')
        parentNode.appendChild(fontElem)
        for a in filter(value.has_key, FontAttribute.attributes):
            elem = Model.dom.createElement(a)
            text = Model.dom.createTextNode(value[a])
            elem.appendChild(text)
            fontElem.appendChild(elem)
    add = staticmethod(add)
    def get(node):
        value = {}
        for n in node.childNodes:
            if n.nodeType == node.ELEMENT_NODE:
                value[n.tagName] = Attribute.get(n)
        return value
    get = staticmethod(get)

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
    '''Content attribute class. Value is a list of strings.'''
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
            
