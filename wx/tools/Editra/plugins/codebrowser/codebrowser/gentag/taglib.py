###############################################################################
# Name: taglib.py                                                             #
# Purpose: Common api for tag generators                                      #
# Author: Cody Precord <cprecord@editra.org>                                  #
# Copyright: (c) 2008 Cody Precord <staff@editra.org>                         #
# License: wxWindows License                                                  #
###############################################################################

"""
FILE: taglib.py
AUTHOR: Cody Precord
LANGUAGE: Python
SUMMARY:
    Basic api for creating tag generator module. Tag generator modules have two
requirements to fit into the api expected by the Editra's CodeBrowser.

  1. The method `GenerateTags` must be defined
  2. GenerateTags must return a L{DocStruct} that contains the code structure

Most common code elements have convinience classes defined in this module. If a
new generator module needs some type of element that is not available in this
module the generator module can derive a type to describe the element. The
derived class should inherit from L{Code} if it is a non container type code
element. If the code element can contain other elements it should instead
derive from L{Scope}. In either case it is important to set the type identifier
attribute that describes the type.

@see: L{Class} and L{Method} for examples


"""

__author__ = "Cody Precord <cprecord@editra.org>"
__svnid__ = "$Id$"
__revision__ = "$Revision$"

#-----------------------------------------------------------------------------#
# Code Object Base Classes

class Code(object):
    """Code representation objects base class all code elements should
    inherit from this class.

    """
    def __init__(self, name, line, obj="code", scope=None):
        """Create the Code Object
        @param name: Items Name
        @param line: Line in buffer item is found on
        @keyword obj: Object type identifier string
        @keyword scope: The name of the scope the object belongs to or None
                        for top level.

        """
        object.__init__(self)

        # Attributes
        self.name = name
        self.line = line
        self.type = obj
        self.doc = name
        self.scope = scope

    def __eq__(self, other):
        if type(other) != type(self):
            return self.name == other
        else:
            return self.name == other.name

    def __gt__(self, other):
        return self.name > other.name

    def __lt__(self, other):
        return self.name < other.name

    def __str__(self):
        if self.scope is not None:
            return u"%s.%s" % (self.scope, self.name)
        else:
            return self.name

    def GetDocumentation(self):
        """Get any documentation associated with this object
        @return: documentation string

        """
        return self.doc

    def SetDocumentation(self, doc):
        """Set the documentation string for this object
        @param doc: documenation string

        """
        self.doc = doc

    def GetLine(self):
        """Returns the line of the code object
        @return: int

        """
        return self.line

    def SetLine(self, line):
        """Set this items line number
        @param line: int

        """
        self.line = line

    def GetName(self):
        """Get the name of this code object
        @return: string

        """
        return self.name

    def SetName(self, objname):
       """Set the name of this code object
       @param objname: string

       """
       self.name = objname

    def GetScope(self):
        """Get the scope this object belongs to, if it returns None
        the scope of the object is at the global/top level.
        @return: string

        """
        return self.scope

    def GetType(self):
        """Get the objects type identifier
        @return: string

        """
        return self.type

    def SetType(self, objtype):
        """Set the object type id string
        @param objtype: string

        """
        self.type = objtype

#-----------------------------------------------------------------------------#

class Scope(Code):
    """Scope object base class used for creating container code types"""
    def __init__(self, name, line, obj="scope", scope=None):
        Code.__init__(self, name, line, obj, scope)
        self.elements = dict()
        self.descript = dict()
        self.prio = dict()
        self._lscope = self

    #---- Properties ----#
    LastScope = property(lambda self: self._lscope)
    #---- End Properties ----#

    def AddElement(self, obj, element):
        """Add an element to this scope
        @param obj: object identifier string
        @param element: L{Code} object to add to this scope

        """
        if isinstance(element, Scope):
            self._lscope = element
        else:
            self._lscope = self
        if obj not in self.elements:
            self.elements[obj] = list()
        self.elements[obj].append(element)
        if obj not in self.prio:
            self.prio[obj] = 0

    def GetElement(self, etype, ename):
        """Get the named element
        @param etype: string element type
        @param ename: name of the object
        @return: string or None

        """
        elist = self.GetElementType(etype)
        for element in elist:
            if element.GetName() == ename:
                return element
        else:
            return None

    def GetElementDescription(self, obj):
        """Get the description of a given element
        @param obj: object identifier string

        """
        return self.descript.get(obj, obj)

    def GetElements(self):
        """Return the dictionary of elements contained in this scope as an
        ordered list of single key dictionaries 
        @return: list of dict

        """
        sorder = [ key for key, val in sorted(self.prio.items(),
                                              key=lambda x: x[1],
                                              reverse=True) ]
        rlist = list()
        for key in sorder:
            if key in self.elements:
                rlist.append({key:sorted(self.elements[key])})
        return rlist

    def GetElementType(self, obj):
        """Get the list of element types in this object that match the
        given identifier string.
        @param obj: object identifier string
        @return: list

        """
        return self.elements.get(obj, list())

    def SetElementDescription(self, obj, desc):
        """Set the description string for a type of element
        @param obj: object identifier string
        @param desc: description string

        """
        self.descript[obj] = desc

    def SetElementPriority(self, obj, prio):
        """Set the priority of of an object in the document. The priority
        is used to decide the order of the list returned by L{GetElements}.
        A higher number means higher priorty (i.e listed earlier).
        @param obj: element identifier string
        @param prio: priority value (int)

        """
        self.prio[obj] = prio

#-----------------------------------------------------------------------------#
# Common Code Object Types for use in Tag Generator Modules
#-----------------------------------------------------------------------------#

class Class(Scope):
    """Class Object Representation"""
    def __init__(self, name, line, scope=None):
        Scope.__init__(self, name, line, "class", scope)

    def AddMethod(self, method):
        """Convenience method for adding a L{Method} to the class object
        @param method: L{Method} object

        """
        self.AddElement('method', method)

    def AddVariable(self, var):
        """Convenience method for adding a L{Variable} to the class object
        @param var: L{Variable} object

        """
        self.AddElement('variable', var)

#---- Scopes ----#
class Namespace(Scope):
    """Namespace Representation"""
    def __init__(self, name, line, scope=None):
        Scope.__init__(self, name, line, "namespace", scope)

class Package(Scope):
    """Package Method object"""
    def __init__(self, name, line, scope=None):
        Scope.__init__(self, name, line, "package", scope)

class Section(Scope):
    """Section Representation"""
    def __init__(self, name, line, scope=None):
        Scope.__init__(self, name, line, "section", scope)

class Method(Scope):
    """Method Object"""
    def __init__(self, name, line, scope=None):
        Scope.__init__(self, name, line, "method", scope)

class Module(Scope):
    """Module Object"""
    def __init__(self, name, line, scope=None):
        Scope.__init__(self, name, line, "module", scope)

class Function(Scope):
    """General Function Object, to create a function like object with
    a differen't type identifier, change the obj parameter to set the
    element type property.

    """
    def __init__(self, name, line, obj="function", scope=None):
        Scope.__init__(self, name, line, obj, scope)

#---- Code Objects ----#

class Macro(Code):
    """Macro Object"""
    def __init__(self, name, line, scope=None):
        Code.__init__(self, name, line, "macro", scope)

class Procedure(Code):
    """Procedure object"""
    def __init__(self, name, line, scope=None):
        Code.__init__(self, name, line, "procedure", scope)

class Variable(Code):
    """Variable object"""
    def __init__(self, name, line, scope=None):
        Code.__init__(self, name, line, "variable", scope)

class Struct(Code):
    """Struct object"""
    def __init__(self, name, line, scope=None):
        Code.__init__(self, name, line, "struct", scope)

#-----------------------------------------------------------------------------#
# Top level code representation object. All tag generators should return an
# instance of this object that contains the structure of the document they
# parsed.

class DocStruct(Scope):
    """Code Document Representation Object
    Captures the structure of the code in a document, this structure can
    then be easily used to represent the document in a number of differen't
    formats.

    """
    def __init__(self):
        Scope.__init__(self, 'docstruct', None)
        self.lastclass = None

    def AddClass(self, cobj):
        """Convenience method for adding a L{Class} to the document
        @param cobj: L{Class} object

        """
        self.lastclass = cobj
        self.AddElement('class', cobj)

    def AddFunction(self, fobj):
        """Convenience method for adding a L{Function} to the document
        @param fobj: L{Function} object

        """
        self.AddElement('function', fobj)

    def AddVariable(self, vobj):
        """Convenience for adding a (global) variable to the document
        @param vobj: L{Variable} object

        """
        self.AddElement('variable', vobj)

    def GetClasses(self):
        """Get all classes in the document and return them as
        a sorted list.

        """
        return sorted(self.GetElementType('class'))

    def GetFunctions(self):
        """Get all top level functions defined in a document and 
        return them as a sorted list.

        """
        return sorted(self.GetElementType('function'))

    def GetScopes(self):
        """Get all Scope type elements in this document object."""
        relem = list()
        for elem in self.GetElements():
            for obj in elem.values():
                if len(obj) and isinstance(obj[0], Scope):
                    relem.extend(obj)
        return relem

    def GetVariables(self):
        """Get all global variables defined in a document and 
        return them as a sorted list.

        """
        return sorted(self.GetElementType('variable'))

    def GetLastClass(self):
        """Gets the last L{Class} that was added to the document
        @return: L{Class}

        """
        return self.lastclass
