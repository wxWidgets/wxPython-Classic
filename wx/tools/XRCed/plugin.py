# Name:         plugin.py
# Purpose:      Pluggable component support
# Author:       Roman Rolinsky <rolinsky@femagsoft.com>
# Created:      31.05.2007
# RCS-ID:       $Id$

import os, sys, glob
from xml.dom import minidom
from globals import *
from presenter import Manager
import component

def load_all_plugins():
    pluginPath = os.getenv('XRCEDPATH')
    if pluginPath:
        for dir in plugins.split(':'):
            if os.path.isdir(dir):
                import_plugins(dir)

def load_plugins(dir):
    sys_path = sys.path
    cwd = os.getcwd()
    dir = os.path.abspath(os.path.normpath(dir))
    TRACE('* load_plugins %s' % dir)
    os.chdir(dir)
    sys.path = sys_path + [dir]
    try:
        ff_py = glob.glob('*.py')
        for f in ff_py:
            name = os.path.splitext(f)[0]
            TRACE('* __import__ %s' % name)
            try:
                __import__(name, globals(), locals(), ['*'])
            except:
                print 'Error:', sys.exc_value
        ff_crx = glob.glob('*.crx')
        for crx in ff_crx:
            try:
                load_crx(crx)
            except:
                print 'Error:', sys.exc_value
        dirs = glob.glob('*/')
        for dir in dirs:
            if os.path.isfile(os.path.join(dir, '__init__.py')):
                TRACE('* __import__ %s/__init__.py' % f)
                try:
                    __import__(dir, globals(), locals(), ['*'])
                except:
                    print 'Error:', sys.exc_value
    finally:
        sys.path = sys_path
        os.chdir(cwd)

def load_crx(filename):
    dom = minidom.parse(filename)
    for node in dom.documentElement.childNodes:
        if node.nodeType == node.ELEMENT_NODE and node.tagName == 'component':
            create_component(node)

def create_component(node):
    klass = node.getAttribute('class')
    name = node.getAttribute('name')
    TRACE('create_component %s', name)
    comp = Manager.getNodeComp(node)
    # !!! getattr is better?
    meta = component.__dict__[comp.klass] # get component class
    attributes = comp.getAttribute(node, 'attributes')
    groups = comp.getAttribute(node, 'groups')
    styles = comp.getAttribute(node, 'styles')
    menu = comp.getAttribute(node, 'menu')
    label = comp.getAttribute(node, 'item')
    if not label: label = name.tolower()
    help = comp.getAttribute(node, 'help')
    panel = comp.getAttribute(node, 'panel')
    bitmap = comp.getAttribute(node, 'bitmap')
    c = meta(name, groups, attributes)
    c.addStyles(*styles)
    Manager.register(c)
    if menu:
        Manager.setMenu(c, menu, label, help)
    if panel:
        Manager.setTool(c, panel, bitmap[1])
