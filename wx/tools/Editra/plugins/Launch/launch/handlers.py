# -*- coding: utf-8 -*-
###############################################################################
# Name: handlers.py                                                           #
# Purpose: File Type Handlers                                                 #
# Author: Cody Precord <cprecord@editra.org>                                  #
# Copyright: (c) 2008 Cody Precord <staff@editra.org>                         #
# License: wxWindows License                                                  #
###############################################################################

"""File Type Handlers
The file type handlers are used to handle the execution of and output of the
different file types that they represent. Each handler manages its own settings
and configuration.

It is easy to extend the filetypes supported by the Launch plugin through this
interface. To add support for a new filetype simply derive a new class from the
base L{FileTypeHandler} and override any of the following methods to provide
custom functionality.

Required Overrides:
__init__ : define default command mapping and default command
__name__ : set the name of the handler, this should be the file type

Other Overrides:
GetEnvironment : Return a dictionary of environmental variables to run the
                 process within
HandleHotSpot : Action to perform when a hotspot is clicked on in the output
                buffer.
StyleText : Perform custom styling on the text as its added, line by line

"""

__author__ = "Cody Precord <cprecord@editra.org>"
__svnid__ = "$Id$"
__revision__ = "$Revision$"

__all__ = ['GetHandlerById', 'GetHandlerByName', 'GetState', 'DEFAULT_HANDLER']

#-----------------------------------------------------------------------------#
# Imports
import os
import sys
import re
import copy

# Editra Libraries
import util
import ebmlib
import eclib
import syntax.synglob as synglob
from profiler import Profile_Get, Profile_Set

# Local Imports
import launchxml

#-----------------------------------------------------------------------------#
# Globals
DEFAULT_HANDLER = 'handler'
CONFIG_KEY = 'Launch.Config2'

# Ansi escape sequence color table
# For coloring shell script output
RE_ANSI_START = re.compile(r'\[[34][0-9];01m')
RE_ANSI_FORE = re.compile('\[3[0-9]m')
RE_ANSI_BLOCK = re.compile('\[[34][0-9]m*.*?\[m')
RE_ANSI_END = re.compile(r'\[[0]{0,1}m')
RE_ANSI_ESC = re.compile('\[[0-9]+m')
ANSI = {
        ## Foreground colours ##
        '[30m' : (1, '#000000'),  # Black
        '[31m' : (2, '#FF0000'),  # Red
        '[32m' : (3, '#00FF00'),  # Green
        '[33m' : (4, '#FFFF00'),  # Yellow
        '[34m' : (5, '#0000FF'),  # Blue
        '[35m' : (6, '#FF00FF'),  # Magenta
        '[36m' : (7, '#00FFFF'),  # Cyan
        '[37m' : (8, '#FFFFFF'),  # White
        #'[39m' : default

        ## Background colour ##
        '[40m' : (011, '#000000'),  # Black
        '[41m' : (012, '#FF0000'),  # Red
        '[42m' : (013, '#00FF00'),  # Green
        '[43m' : (014, '#FFFF00'),  # Yellow
        '[44m' : (015, '#0000FF'),  # Blue
        '[45m' : (016, '#FF00FF'),  # Magenta
        '[46m' : (017, '#00FFFF'),  # Cyan
        '[47m' : (020, '#FFFFFF'),  # White
        #'[49m' : default
        }

# Style Types
STYLE_NORMAL = 0
STYLE_INFO   = 1
STYLE_ERROR  = 2

# Process Start/Exit Regular Expression
RE_PROC_SE = re.compile('>{3,3}.*' + os.linesep)

#-----------------------------------------------------------------------------#
# Public Handler Api for use outside this module
def GetHandlerById(lang_id):
    """Get a handler for the specified language id"""
    return FileTypeHandler.FactoryCreate(lang_id)

def GetHandlerByName(name):
    """Get an output handler by name"""
    lang_id = synglob.GetIdFromDescription(name)
    return GetHandlerById(lang_id)

def GetUserSettings(name):
    """Get the user settings for a given file type
    @param name: file type name

    """
    data = Profile_Get(CONFIG_KEY, default=dict())
    val = data.get(name, tuple())
    return val

def InitCustomHandlers(path):
    """Init the custom handlers defined in the launch.xml file
    @param path: path to directory to find the launch xml in
    @return: bool

    """
    loaded = False
    path = os.path.join(path, u'launch.xml')
    if os.path.exists(path):
        lxml = None
        try:
            lxml = launchxml.LaunchXml.Load(path)
        except Exception, msg:
            # XML Parsing error
            util.Log("[Launch][err] Failed to load custom Handlers")
            util.Log("[Launch][err] XML Parsing Error: %s" % msg)

        if lxml:
            for hndlr in lxml.GetHandlers():
                try:
                    FileTypeHandler.RegisterClass(XmlHandlerDelegate(hndlr))
                except Exception, msg:
                    util.Log("[Launch][err] Unexpected error in creating xml delegate")
                    util.Log("[Launch][err] %s" % msg)
    return loaded

def LoadCustomHandler(xml_str):
    """Load a custom Launch handler an xml string
    @param xml_str: Launch Xml String
    @return: bool

    """
    try:
        lxml = launchxml.LaunchXml()
        lxml.Xml = xml_str
        for hndlr in lxml.GetHandlers():
            FileTypeHandler.RegisterClass(XmlHandlerDelegate(hndlr))
    except:
        return False
    else:
        return True

#-----------------------------------------------------------------------------#
# Handler Base Class and Handler implementations
#

class Meta:
    """Metadata namespace, acts as a container object for all FileTypeHandler
    meta attributes.
    @see: HandlerMeta

    """
    _defaults = {"typeid" : -1,            # Editra Language ID
                 "name" : DEFAULT_HANDLER, # Language Display Name (derived from ID)
                 "commands" : dict(),      # Commands alias -> commandline
                 "default" : u"",          # Default command alias
                 "error" : None,           # Error regular expression
                 "hotspot" : None,         # Hotspot expression (line, filename)
                 "transient" : False}      # Transient configuration (bool)
    def __init__(self, meta_attrs):
        for (attr,default) in self._defaults.items():
            attr_val = meta_attrs.get(attr, default)
            try:
                if attr in ('error', 'hotspot'):
                    setattr(self, attr, attr_val)
                else:
                    setattr(self, attr, copy.copy(attr_val))
            except Exception, msg:
                util.Log("[Launch][err] Metadata copy error")

class HandlerMeta(type):
    """Metaclass for manipulating a handler classes metadata converts
    all user defined 'meta' classes to a Meta class with all unset attributes
    initialized to the default setting.

    """
    def __new__(mcls,name,bases,attrs):
        cls = super(HandlerMeta,mcls).__new__(mcls,name,bases,attrs)
        meta_attrs = {}
        if hasattr(cls, 'meta'):
            for attr in dir(cls.meta):
                if not attr.startswith("_"):
                    meta_attrs[attr] = getattr(cls.meta,attr)
        cls.meta = Meta(meta_attrs)
        return cls

#-----------------------------------------------------------------------------#

class FileTypeHandler(object):
    """Base default Output handler all output handlers should derive from
    this class. This base class is used when an output handler is request
    but no special one exists.

    """
    __metaclass__ = HandlerMeta
    handler_cache = dict()

    def __init__(self):
        super(FileTypeHandler, self).__init__()

        if self.meta.typeid != -1:
            self.meta.name = synglob.GetDescriptionFromId(self.meta.typeid)

    @staticmethod
    def __ClassFactory(ftype):
        """Generate a new class for ones that don't have a
        specialized implementation.
        @return: new FileTypeHandler class

        """
        class DynamicHandler(FileTypeHandler):
            class meta:
                langid = ftype
                name = synglob.GetDescriptionFromId(ftype)
        return DynamicHandler

    @classmethod
    def FactoryCreate(cls, ftype):
        """Create an instance of a FileTypeHandler for the given
        file type. One of the two arguments must be provided. If
        both are provided the ftype argument will take preference.
        @param cls: Class object
        @param ftype: Editra file type ID

        """
        obj = cls.handler_cache.get(ftype, None)
        if obj is None:
            # Check existing custom subclasses for a proper implementation
            for handler in cls.__subclasses__():
                if ftype != -1 and handler.meta.typeid == ftype:
                    obj = handler
                    break
            else:
                # Dynamically create a new class
                obj = cls.__ClassFactory(ftype)
            cls.RegisterClass(obj)
        obj = obj()

        # Load custom settings for non-transient filetypes
        if not obj.meta.transient:
            data = GetUserSettings(obj.GetName())
            if len(data):
                obj.SetCommands(data[1])
                obj.SetDefault(data)
        return obj

    @classmethod
    def AppendCommand(cls, cmd):
        """Add a command to the list of commands known to this handler
        @param cls: Class object
        @param cmd: Tuple of (Command alias, executable path or name)

        """
        if isinstance(cmd, tuple):
            cls.meta.commands[cmd[0]] = cmd[1]

    @classmethod
    def RegisterClass(cls, handler):
        """Register a filetype handler in the handler
        chain cache.
        @param cls: Class object
        @param handler: FileTypeHandler

        """
        cls.handler_cache[handler.meta.typeid] = handler

    @classmethod
    def GetAliases(cls):
        """Get the list of command aliases
        @param cls: Class object

        """
        return sorted(cls.meta.commands.keys())

    @classmethod
    def GetCommand(cls, alias):
        """Get the command for a given alias
        @param cls: Class object
        @param alias: Command Alias (Unicode)

        """
        return cls.meta.commands.get(alias, alias)

    @classmethod
    def GetCommands(cls):
        """Get the set of commands available for this file type
        @param cls: Class object

        """
        return sorted(cls.meta.commands.items())

    @classmethod
    def GetDefault(cls):
        """Get the preferred default command
        @param cls: Class object
        @return: string

        """
        return cls.meta.default

    def GetEnvironment(self):
        """Get the dictionary of environmental variables to run the
        command under.
        @return: dict

        """
        return dict(os.environ)

    @classmethod
    def GetName(cls):
        """Get the name of this handler
        @param cls: Class object
        @return: Unicode

        """
        return cls.meta.name

    @classmethod
    def HandleHotSpot(cls, mainw, outbuffer, line, fname):
        """Handle hotspot clicks. Called when a hotspot is clicked
        in an output buffer of this file type.
        @param cls: Class object
        @param mainw: MainWindow instance that created the launch instance
        @param outbuffer: Buffer the click took place in
        @param line: line number of the hotspot region in the buffer
        @param fname: path of the script that was run to produce the output that
                      contains the hotspot.

        """
        if cls.meta.hotspot is not None:
            ifile, line = _FindFileLine(outbuffer, line, fname,
                                        cls.meta.hotspot)
            _OpenToLine(ifile, line, mainw)

    def FilterInput(self, text):
        """Filter incoming text return the text to be displayed
        @param text: The incoming text to filter before putting in buffer

        """
        return text

    @classmethod
    def SetCommands(cls, cmds):
        """Set the list of commands known by the handler
        @param cls: Class object
        @param cmds: list of command tuples

        """
        if not isinstance(cmds, list):
            raise TypeError("SetCommands expects a list of tuples: %s" % repr(cmds))
        else:
            sdict = dict()
            for cmd in cmds:
                if len(cmd) == 2:
                    sdict[cmd[0]] = cmd[1]
            cls.meta.commands.clear()
            cls.meta.commands.update(sdict)

            # Reset default if it has been removed
            if cls.meta.default not in cls.meta.commands:
                keys = cls.meta.commands.keys()
                if len(keys):
                    cls.meta.default = keys[0]
                else:
                    cls.meta.default = u""

    @classmethod
    def SetDefault(cls, cmd):
        """Set the preferred default command
        @param cls: Class object
        @param cmd: Command alias/path tuple to set as the preferred one
        @postcondition: if cmd is not in the saved command list it will be
                        added to that list.

        """
        cmd = [ cmd[0].strip(), cmd[1] ]
        if cmd[0] not in cls.GetAliases():
            cls.AppendCommand(cmd)
        cls.meta.default = cmd[0]

    @classmethod
    def StoreState(cls):
        """Store the state of this handler
        @param cls: Class object

        """
        if cls.meta.transient:
            util.Log("[Launch][info] Transient XML handler: settings will not persist")
            # TODO: update XML configuration file?
            return
        data = Profile_Get(CONFIG_KEY, default=dict())
        cdata = data.get(cls.GetName(), None)
        if data != cdata:
            util.Log("[Launch][info] Store config: %s" % cls.GetName())
            data[cls.GetName()] = (cls.meta.default, cls.meta.commands.items())
            Profile_Set(CONFIG_KEY, data)

    @classmethod
    def StyleText(cls, stc, start, txt):
        """Style Information and Error messages from script output.
        @param cls: Class object
        @param stc: EditraStc instance
        @param start: Start position (int)
        @param txt: Text to style (Unicode)

        """
        if cls.meta.error is not None:
            sty = STYLE_NORMAL
            err, more = _StyleError(stc, start, txt, cls.meta.error)
            if err:
                err = STYLE_ERROR
            if more:
                sty = cls._StyleText(stc, start, txt)[0]
            sty = max(err, sty)
        else:
            sty, more = cls._StyleText(stc, start, txt)
        return sty, more

    @classmethod
    def _StyleText(cls, stc, start, txt):
        """Style the text in the given buffer
        @param cls: Class object
        @param stc: stc based buffer to apply styling to
        @param start: start of text that was just added to buffer
        @param txt: text that was just added at start point

        """
        # Highlight Start and End lines in info style
        finfo = False
        for info in RE_PROC_SE.finditer(txt):
            sty_s = start + info.start()
            sty_e = start + info.end()
            stc.StartStyling(sty_s, 0xff)
            stc.SetStyling(sty_e - sty_s, eclib.OPB_STYLE_INFO)
            finfo = True

        if finfo:
            return STYLE_INFO, False
        else:
            return STYLE_NORMAL, False

#-----------------------------------------------------------------------------#

class AdaHandler(FileTypeHandler):
    """FileTypeHandler for Ada"""
    class meta:
        typeid = synglob.ID_LANG_ADA
        commands = {'gcc -c' : 'gcc -c'}
        default = 'gcc -c'

#-----------------------------------------------------------------------------#

class BashHandler(FileTypeHandler):
    """FileTypeHandler for Bash scripts"""
    class meta:
        typeid = synglob.ID_LANG_BASH
        commands = dict(bash='bash')
        error = re.compile('(.+): line ([0-9]+): .*' + os.linesep)
        hotspot = re.compile('(.+): line ([0-9]+): .*' + os.linesep)

    def FilterInput(self, txt):
        """Filter out ansi escape sequences from input
        @param txt: Text to apply filter to
        @return: Filtered Text

        """
        txt = RE_ANSI_START.sub('', txt)
        return RE_ANSI_END.sub('', txt)

    @classmethod
    def HandleHotSpot(cls, mainw, outbuffer, line, fname):
        """Hotspots are error messages, find the file/line of the
        error in question and open the file to that point in the buffer.

        """
        txt = outbuffer.GetLine(line)
        match = cls.meta.hotspot.findall(txt)
        ifile = None
        if len(match):
            ifile = match[0][0].split()[-1]
            try:
                line = max(int(match[0][1]) - 1, 0)
            except IndexError:
                line = 0

        # If not an absolute path then the error is in the current script
        if not os.path.isabs(ifile):
            dname = os.path.split(fname)[0]
            ifile = os.path.join(dname, ifile)

        _OpenToLine(ifile, line, mainw)

#-----------------------------------------------------------------------------#

class BatchHandler(FileTypeHandler):
    """FileTypeHandler for Dos batch files"""
    class meta:
        typeid = synglob.ID_LANG_BATCH
        commands = dict(cmd='cmd /c')
        default = 'cmd'

#-----------------------------------------------------------------------------#

class BooHandler(FileTypeHandler):
    """FileTypeHandler for Boo"""
    class meta:
        typeid = synglob.ID_LANG_BOO
        commands = dict(booi='booi')
        default = 'booi'

#-----------------------------------------------------------------------------#

class CHandler(FileTypeHandler):
    """FileTypeHandler for C Files"""
    class meta:
        typeid = synglob.ID_LANG_C
        commands = {'gcc -c' : 'gcc -c'}
        default = 'gcc -c'
        error = re.compile  ('(.+):([0-9]+): error:.+')
        hotspot = re.compile('(.+):([0-9]+): error:.+')

class CPPHandler(FileTypeHandler):
    """FileTypeHandler for C++ Files"""
    class meta:
        typeid = synglob.ID_LANG_CPP
        commands = {'g++ -c' : 'g++ -c'}
        default = 'g++ -c'
        error = re.compile  ('(.+):([0-9]+): error:.+')
        hotspot = re.compile('(.+):([0-9]+): error:.+')

#-----------------------------------------------------------------------------#

class CamlHandler(FileTypeHandler):
    """FileTypeHandler for Caml"""
    class meta:
        typeid = synglob.ID_LANG_CAML
        commands = dict(ocaml='ocaml')
        error = re.compile(r'File "(.+)", line (.+), characters .+:')
        hotspot = re.compile(r'File "(.+)", line (.+), characters .+:')

#-----------------------------------------------------------------------------#

class CSHHandler(FileTypeHandler):
    """FileTypeHandler for C-Shell"""
    class meta:
        typeid = synglob.ID_LANG_CSH
        commands = dict(csh='csh')
        default = 'csh'

#-----------------------------------------------------------------------------#

class DHandler(FileTypeHandler):
    """FileTypeHandler for D"""
    class meta:
        typeid = synglob.ID_LANG_D
        commands = dict(dmd='dmd -run')
        default = 'dmd'

#-----------------------------------------------------------------------------#

class FeriteHandler(FileTypeHandler):
    """FileTypeHandler for Ferite"""
    class meta:
        typeid = synglob.ID_LANG_FERITE
        commands = dict(ferite='ferite')
        default = 'ferite'

#-----------------------------------------------------------------------------#

class HaskellHandler(FileTypeHandler):
    """FileTypeHandler for Haskell"""
    class meta:
        typeid = synglob.ID_LANG_HASKELL
        commands = {'ghc --make' : 'ghc --make'}
        default = 'ghc --make'
        error = re.compile('(.+):(.+):[0-9]+:.+ error .+')
        hotspot = re.compile('(.+):(.+):[0-9]+:.+ error .+')

#-----------------------------------------------------------------------------#

class HaxeHandler(FileTypeHandler):
    """FileTypeHandler for haXe"""
    class meta:
        typeid = synglob.ID_LANG_HAXE
        commands = dict(neko='neko', nekoc='nekoc')
        default = 'nekoc'
        error = re.compile('([a-zA-Z_.]+)\(([0-9]+)\):.*')
        hotspot = re.compile('([a-zA-Z_.]+)\(([0-9]+)\):.*')

#-----------------------------------------------------------------------------#

class HTMLHandler(FileTypeHandler):
    """FileTypeHandler for HTML"""
    class meta:
        typeid = synglob.ID_LANG_HTML
        if u'darwin' in sys.platform:
            commands = dict(Safari='open -a Safari.app',
                            Camino='open -a Camino.app',
                            Firefox='open -a Firefox.app',
                            Opera='open -a Opera.app')
            default = 'Safari'
        elif sys.platform.startswith('win'):
            commands = dict(ie='iexplorer.exe',
                             firefox='firefox.exe',
                             opera='opera.exe')
            default = 'ie'
        else:
            commands = dict(firefox='firefox', opera='opera')
            default = 'firefox'

#-----------------------------------------------------------------------------#

class InnoSetupHandler(FileTypeHandler):
    """FileTypeHandler for Inno Setup Scripts"""
    class meta:
        typeid = synglob.ID_LANG_INNO
        commands = dict(iscc='iscc.exe', Compil32='Compil32.exe /cc')
        default = 'iscc'

#-----------------------------------------------------------------------------#

class KornHandler(FileTypeHandler):
    """FileTypeHandler for Korn Shell scripts"""
    class meta:
        typeid = synglob.ID_LANG_KSH
        commands = dict(ksh='ksh')
        default = 'ksh'

#-----------------------------------------------------------------------------#

class STATAHandler(FileTypeHandler):
    """FileTypeHandler for Stata"""
    class meta:
        typeid = synglob.ID_LANG_STATA
        commands = dict(stata='stata', xstata='xstata')
        default = 'stata'

#-----------------------------------------------------------------------------#

class LatexHandler(FileTypeHandler):
    """FileTypeHandler for LaTex"""
    class meta:
        typeid = synglob.ID_LANG_LATEX
        commands = dict(latex='latex', dvips='dvips',
                        pdflatex='pdflatex', ps2pdf='ps2pdf',
                        dvipng='dvipng', latex2html='latex2html')
        default = 'latex'

#-----------------------------------------------------------------------------#

class LuaHandler(FileTypeHandler):
    """FileTypeHandler for Lua"""
    class meta:
        typeid = synglob.ID_LANG_LUA
        commands = dict(lua='lua', luac='luac')
        default = 'lua'
        error = re.compile('.*: (.+):([0-9]+):.*')
        hotspot = re.compile('.*: (.+):([0-9]+):.*')

#-----------------------------------------------------------------------------#

class NewLispHandler(FileTypeHandler):
    """FileTypeHandler for newLisp"""
    class meta:
        typeid = synglob.ID_LANG_NEWLISP
        commands = dict(newlisp='newlisp')
        default = 'newlisp'

#-----------------------------------------------------------------------------#

class NSISHandler(FileTypeHandler):
    """FileTypeHandler for NSIS scripts"""
    class meta:
        typeid = synglob.ID_LANG_NSIS
        commands = dict(makensis='makensis')
        default = 'makensis'
        error = re.compile(r'Error .* "(.+)" on line ([0-9]+) ')
        hotspot = re.compile(r'Error .* "(.+)" on line ([0-9]+) ')

#-----------------------------------------------------------------------------#

class PhpHandler(FileTypeHandler):
    """FileTypeHandler for Php"""
    class meta:
        typeid = synglob.ID_LANG_PHP
        commands = dict(php='php -f')
        default = 'php'
        error = re.compile(r'[a-zA-Z]+ error: .* in (.+) on line ([0-9]+).*')
        hotspot = re.compile(r'[a-zA-Z]+ error: .* in (.+) on line ([0-9]+).*')

#-----------------------------------------------------------------------------#

class PikeHandler(FileTypeHandler):
    """FileTypeHandler for Pike"""
    class meta:
        typeid = synglob.ID_LANG_PIKE
        commands = dict(pike='pike')
        default = 'pike'

#-----------------------------------------------------------------------------#

class PerlHandler(FileTypeHandler):
    """FileTypeHandler for Perl scripts"""
    class meta:
        typeid = synglob.ID_LANG_PERL
        commands = dict(perl='perl')
        default = 'perl'
        hotspot = re.compile(r'.+ at (.+) line ([0-9]+)[,\.].*')

#-----------------------------------------------------------------------------#

class PostScriptHandler(FileTypeHandler):
    """FileTypeHandler for Post/GhostScript"""
    class meta:
        typeid = synglob.ID_LANG_PS
        if sys.platform.startswith('win'):
            commands = dict(gswin32c='gswin32c')
            default = 'gs2in32c'
        elif 'darwin' in sys.platform:
            commands = dict(pstopdf='pstopdf')
            default = 'pstopdf'
        else:
            commands = dict(gs='gs')
            default = 'gs'

#-----------------------------------------------------------------------------#

class PythonHandler(FileTypeHandler):
    """FileTypeHandler for Python"""
    RE_PL_ERR = re.compile(r'\s*([REWCF]):\s*([0-9]+):.*') # Pylint Output

    class meta:
        typeid = synglob.ID_LANG_PYTHON
        commands = dict(python='python -u', pylint='pylint',
                             pylinterr='pylint -e')
        default = 'python'
        error = re.compile('File "(.+)", line ([0-9]+)')
        hotspot = re.compile('File "(.+)", line ([0-9]+)')

    def GetEnvironment(self):
        """Get the environment to run the python script in"""
        if not hasattr(sys, 'frozen') or sys.platform.startswith('win'):
            proc_env = super(PythonHandler, self).GetEnvironment()
        else:
            proc_env = dict()

        proc_env['PYTHONUNBUFFERED'] = '1'
        return proc_env

    @classmethod
    def HandleHotSpot(cls, mainw, outbuffer, line, fname):
        """Hotspots are error messages, find the file/line of the
        error in question and open the file to that point in the buffer.

        """
        match = PythonHandler.RE_PL_ERR.match(outbuffer.GetLine(line))
        if match:
            eline = max(0, int(match.group(2)) - 1)
            _OpenToLine(fname, eline, mainw)
        else:
            super(PythonHandler, cls).HandleHotSpot(mainw, outbuffer, line, fname)

#-----------------------------------------------------------------------------#

class RHandler(FileTypeHandler):
    """FileTypeHandler for R"""
    class meta:
        typeid = synglob.ID_LANG_R
        commands = {'r' : 'R', 'Rterm' : 'Rterm', 
                    'Rgui' : 'Rgui', 'Rscript' : 'Rscript'}
        default = 'Rscript'

#-----------------------------------------------------------------------------#

class RubyHandler(FileTypeHandler):
    """FileTypeHandler for Ruby scripts"""
    class meta:
        typeid = synglob.ID_LANG_RUBY
        commands = dict(ruby='ruby')
        default = 'ruby'
        error = re.compile('(.+):([0-9]+)[:]{0,1}.*')
        hotspot = re.compile('(.+):([0-9]+)[:]{0,1}.*')

#-----------------------------------------------------------------------------#

class TCLHandler(FileTypeHandler):
    """FileTypeHandler for TCL/TK"""
    class meta:
        typeid = synglob.ID_LANG_TCL
        commands = dict(wish='wish')
        default = 'wish'
        error = re.compile('\(file "(.+)" line ([0-9]+)\)')
        hotspot = re.compile('\(file "(.+)" line ([0-9]+)\)')

    @classmethod
    def HandleHotSpot(cls, mainw, outbuffer, line, fname):
        """Hotspots are error messages, find the file/line of the
        error in question and open the file to that point in the buffer.

        """
        txt = outbuffer.GetLine(line)
        match = cls.meta.hotspot.findall(txt)
        ifile = None
        if len(match):
            ifile = match[0][0]
            try:
                line = max(int(match[0][1]) - 1, 0)
            except IndexError:
                line = 0

        # If not an absolute path then the error is in the current script
        if not os.path.isabs(ifile):
            dname = os.path.split(fname)[0]
            ifile = os.path.join(dname, ifile)

        _OpenToLine(ifile, line, mainw)

#-----------------------------------------------------------------------------#

class VBScriptHandler(FileTypeHandler):
    """FileTypeHandler for VBScript"""
    class meta:
        typeid = synglob.ID_LANG_VBSCRIPT
        commands = dict(cscript='CSCRIPT.exe', wscript='WSCRIPT.exe')
        default = 'cscript'
        error = re.compile('(.+)\(([0-9]+).*' + os.linesep)
        hotspot = re.compile('(.+)\(([0-9]+).*' + os.linesep)

#-----------------------------------------------------------------------------#

def XmlHandlerDelegate(xmlobj):
    """Create delegate class for creating new filetype handlers from a Launch
    Xml object.
    @param xmlobj: launchxml.Handler

    """
    class XmlDelegateClass(FileTypeHandler):
        class meta:
            typeid = getattr(synglob, xmlobj.id, -1)
            name = xmlobj.name
            commands = xmlobj.GetCommands()
            default = xmlobj.GetDefaultCommand()
            error = xmlobj.GetErrorPattern()
            hotspot = xmlobj.GetHotspotPattern()
            transient = True
    return XmlDelegateClass

#-----------------------------------------------------------------------------#
# Local utility functions

def _FindFileLine(outbuffer, line, fname, regex):
    """Find and return the filename and line number found by applying
    the given regular expression to the text found in the line of the
    given buffer.
    @param outbuffer: OutputBuffer instance
    @param line: in the buffer
    @param fname: Filname that generated the error message
    @param regex: a regular expression with two groups the first group needs to
                  match the filename. The second group needs to match the line
                  number that the error is reporting

    """
    match = regex.findall(outbuffer.GetLine(line))
    ifile = None
    if len(match):
        ifile = match[0][0]
        try:
            line = max(int(match[0][1]) - 1, 0)
        except (IndexError, TypeError):
            line = 0

    # If not an absolute path then the error is relative to the
    # script that produced this error message.
    if ifile is not None and not os.path.isabs(ifile):
        dname = os.path.split(fname)[0]
        ifile = os.path.join(dname, ifile)

    return (ifile, line)

def _OpenToLine(fname, line, mainw):
    """Open the given filename to the given line number
    @param fname: File name to open, relative paths will be converted to abs
                  paths.
    @param line: Line number to set the cursor to after opening the file
    @param mainw: MainWindow instance to open the file in

    """
    fname = os.path.abspath(fname) # Normalize path
    nbook = mainw.GetNotebook()
    buffers = [ page.GetFileName() for page in nbook.GetTextControls() ]
    for page, name in enumerate(buffers):
        if ebmlib.ComparePaths(fname, name):
            nbook.ChangePage(page)
            nbook.GetPage(page).GotoLine(line)
            break
    else:
        nbook.OnDrop([fname])
        nbook.GetPage(nbook.GetSelection()).GotoLine(line)

def _StyleError(stc, start, txt, regex):
    """Style Error message groups
    @param stc: OutputBuffer reference
    @param start: start of text just added to buffer
    @param txt: text that was just added
    @param regex: regular expression object for matching the errors
    @return: (bool errfound, bool more)

    """
    found_err = False
    more = False
    sty_e = start
    for group in regex.finditer(txt):
        sty_s = start + group.start()
        sty_e = start + group.end()
        stc.StartStyling(sty_s, 0xff)
        stc.SetStyling(sty_e - sty_s, eclib.OPB_STYLE_ERROR)
        found_err = True

    if sty_e != start + len(txt):
        more = True

    return found_err, more
