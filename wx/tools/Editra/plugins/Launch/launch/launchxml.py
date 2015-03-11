# -*- coding: utf-8 -*-
###############################################################################
# Name: launchxml.py                                                          #
# Purpose: Launch Xml Interface                                               #
# Author: Cody Precord <cprecord@editra.org>                                  #
# Copyright: (c) 2009 Cody Precord <staff@editra.org>                         #
# License: wxWindows License                                                  #
###############################################################################

"""Launch Xml Interface
Interface to add new filetype support to launch or to override existing support.

"""

xml_spec = """
<launch version="1">

   <handler name="Python" id="ID_LANG_PYTHON">

      <commandlist default="python">
         <command name="python" execute="python2.5 -u"/>
         <command name="pylint" execute="/usr/local/bin/pylint"/>
      </commandlist>

      <error pattern="File &quot;(.+)&quot;, line ([0-9]+)"/>  

   </handler>

</launch>
"""

__author__ = "Cody Precord <cprecord@editra.org>"
__svnid__ = "$Id$"
__revision__ = "$Revision$"

#-----------------------------------------------------------------------------#
# Imports
import re
import sys
#sys.path.insert(0, '../../../src/')

# Editra Imports
import ed_xml

#-----------------------------------------------------------------------------#
# Globals

#-----------------------------------------------------------------------------#

class ErrorPattern(ed_xml.EdXml):
    class meta:
        tagname = "error"
    pattern = ed_xml.String(required=True)

class HotspotPattern(ed_xml.EdXml):
    class meta:
        tagname = "hotspot"
    pattern = ed_xml.String(required=True)

class Command(ed_xml.EdXml):
    class meta:
        tagname = "command"
    name = ed_xml.String(required=True)
    execute = ed_xml.String(required=True)

class CommandList(ed_xml.EdXml):
    class meta:
        tagname = "commandlist"
    default = ed_xml.String(required=True)
    commands = ed_xml.List(Command)

class Handler(ed_xml.EdXml):
    class meta:
        tagname = "handler"
    name = ed_xml.String(required=True)
    id = ed_xml.String(required=True)
    # Sub elements
    commandlist = ed_xml.Model(CommandList, required=False)
    error = ed_xml.Model(ErrorPattern, required=False)
    hotspot = ed_xml.Model(HotspotPattern, required=False)

    def GetDefaultCommand(self):
        """Get the default command"""
        default = u""
        if self.commandlist:
            default = self.commandlist.default
        return default

    def GetCommands(self):
        """Get the list of commands"""
        clist = dict()
        if self.commandlist:
            for cmd in self.commandlist.commands:
                clist[cmd.name] = cmd.execute
        return clist

    def GetErrorPattern(self):
        """Get the handlers error pattern"""
        if self.error and self.error.pattern:
            return re.compile(self.error.pattern)
        return None

    def GetHotspotPattern(self):
        """Get the handlers hotspot pattern"""
        if self.hotspot and self.hotspot.pattern:
            return re.compile(self.hotspot.pattern)
        return None

class LaunchXml(ed_xml.EdXml):
    class meta:
        tagname = "launch"
    handlers = ed_xml.List(Handler, required=False)

    def GetHandler(self, name):
        """Get a handler by name
        @return: Handler instance or None

        """
        rval = None
        for handler in self.handlers:
            if handler.name == name:
                rval = handler
                break
        return handler

    def GetHandlers(self):
        """Get the whole dictionary of handlers
        @return: dict(name=Handler)

        """
        return self.handlers

    def HasHandler(self, name):
        """Is there a handler for the given file type
        @return: bool

        """
        for handler in self.handlers:
            if handler.name == name:
                return True
        return False

#-----------------------------------------------------------------------------#
# Test
#if __name__ == '__main__':
#    h = LaunchXml.Load("launch.xml")
#    print "CHECK Python Handler"
#    hndlr = h.GetHandler('Python')
#    print hndlr.GetCommands()
#    print hndlr.error.pattern
#    print hndlr.hotspot.pattern
#    print hndlr.commandlist.default

#    print h.GetHandlers()

#    print "Check C Handler"
#    hndlr = h.GetHandler('C')
#    print hndlr.GetCommands()
#    print hndlr.GetHotspotPattern()
#    print hndlr.GetErrorPattern()
#    print hndlr.GetDefaultCommand()

