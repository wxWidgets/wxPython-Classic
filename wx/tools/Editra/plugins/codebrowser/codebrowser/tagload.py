###############################################################################
# Name: tagload.py                                                            #
# Purpose: Dynamic tag generator loader                                       #
# Author: Cody Precord <cprecord@editra.org>                                  #
# Copyright: (c) 2008 Cody Precord <staff@editra.org>                         #
# License: wxWindows License                                                  #
###############################################################################

"""
FILE: tagload.py
AUTHOR: Cody Precord
LANGUAGE: Python
SUMMARY:
    Dynamically load and provide tag generator methods based on the unique
file type identifiers defined in Editra.src.syntax.synglob.

"""

__author__ = "Cody Precord <cprecord@editra.org>"
__svnid__ = "$Id$"
__revision__ = "$Revision$"

#--------------------------------------------------------------------------#
# Imports
import sys

# Editra Libraries
import syntax.synglob as synglob

#--------------------------------------------------------------------------#
# Globals
TAGLIB = 'gentag.'

LOAD_MAP = { synglob.ID_LANG_ADA : TAGLIB + 'adatags',
             synglob.ID_LANG_BASH : TAGLIB + 'shtags',
             synglob.ID_LANG_BATCH : TAGLIB + 'batchtags',
             synglob.ID_LANG_C : TAGLIB + 'ctags',
             synglob.ID_LANG_CPP : TAGLIB + 'ctags',
             synglob.ID_LANG_CSH : TAGLIB + 'shtags',
             synglob.ID_LANG_CSS : TAGLIB + 'csstags',
             synglob.ID_LANG_D : TAGLIB + 'dtags',
             synglob.ID_LANG_DIFF : TAGLIB + 'difftags',
             synglob.ID_LANG_ESS : TAGLIB + 'esstags',
             synglob.ID_LANG_F77 : TAGLIB + 'fortrantags',
             synglob.ID_LANG_F95 : TAGLIB + 'fortrantags',
             synglob.ID_LANG_FERITE : TAGLIB + 'feritetags',
             synglob.ID_LANG_HAXE : TAGLIB + 'haxetags',
             synglob.ID_LANG_HTML : TAGLIB + 'xmltags',
             synglob.ID_LANG_INNO : TAGLIB + 'innotags',
             synglob.ID_LANG_JAVA : TAGLIB + 'javatags',
             synglob.ID_LANG_KSH : TAGLIB + 'shtags',
             synglob.ID_LANG_LISP : TAGLIB + 'lisptags',
             synglob.ID_LANG_LUA : TAGLIB + 'luatags',
             synglob.ID_LANG_MATLAB : TAGLIB + 'matlabtags',
             synglob.ID_LANG_NSIS : TAGLIB + 'nsistags',
             synglob.ID_LANG_OCTAVE : TAGLIB + 'matlabtags',
             synglob.ID_LANG_PERL : TAGLIB + 'perltags',
             synglob.ID_LANG_PHP : TAGLIB + 'phptags',
             synglob.ID_LANG_PLSQL : TAGLIB + 'sqltags',
             synglob.ID_LANG_PROPS : TAGLIB + 'conftags',
             synglob.ID_LANG_PYTHON : TAGLIB + 'pytags',
             synglob.ID_LANG_RUBY : TAGLIB + 'rubytags',
             synglob.ID_LANG_SCHEME : TAGLIB + 'schemetags',
             synglob.ID_LANG_SQL : TAGLIB + 'sqltags',
             synglob.ID_LANG_TCL : TAGLIB + 'tcltags',
             synglob.ID_LANG_VALA : TAGLIB + 'valatags',
             synglob.ID_LANG_VBSCRIPT : TAGLIB + 'vbstags',
             synglob.ID_LANG_VERILOG : TAGLIB + 'verilogtags',
             synglob.ID_LANG_XML : TAGLIB + 'xmltags',
             synglob.ID_LANG_XTEXT: TAGLIB + 'xtexttags' }

# Compatibility for older versions of Editra
if hasattr(synglob, 'ID_LANG_SYSVERILOG'):
    LOAD_MAP[synglob.ID_LANG_SYSVERILOG] = TAGLIB + 'verilogtags'

#--------------------------------------------------------------------------#

class _TagLoader(object):
    """Tag generator loader and manager class"""
    _loaded = dict()
    def __init__(self):
        object.__init__(self)

    def GetGenerator(self, lang_id):
        """Get the tag generator method for the given language id
        @param lang_id: Editra language identifier id
        @return: Generator Method or None

        """
        if lang_id in LOAD_MAP:
            modname = LOAD_MAP[lang_id]
            self.LoadModule(modname)
            if modname in _TagLoader._loaded:
                return TagLoader._loaded[modname].GenerateTags
        return None

    def IsModLoaded(self, modname):
        """Checks if a module has already been loaded
        @param modname: name of module to lookup

        """
        if modname in sys.modules or modname in _TagLoader._loaded:
            return True
        else:
            return False

    def LoadModule(self, modname):
        """Dynamically loads a module by name. The loading is only
        done if the modules data set is not already being managed
        @param modname: name of DocStruct generator to load

        """
        if modname == None:
            return False

        if not self.IsModLoaded(modname):
            try:
                _TagLoader._loaded[modname] = __import__(modname, globals(), 
                                                         locals(), [''])
            except ImportError:
                return False
        return True

#--------------------------------------------------------------------------#
# Public Api

TagLoader = _TagLoader()
