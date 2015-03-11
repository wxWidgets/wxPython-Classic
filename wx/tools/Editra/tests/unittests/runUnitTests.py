################################################################################
## Name: runUnitTests.py                                                       #
## Purpose: Run the Unit Test Suite                                            #
## Author: Cody Precord <cprecord@editra.org>                                  #
## Copyright: (c) 2008 Cody Precord <staff@editra.org>                         #
## License: wxWindows License                                                  #
################################################################################

"""
Run Editra's Unittest Suite.

This module is mostly copied from the wxPython Unittest Suite.

@summary: Unittest Suite Main Module

"""

__author__ = "Cody Precord <cprecord@editra.org>"
__svnid__ = "$Id$"
__revision__ = "$Revision$"

#-----------------------------------------------------------------------------#
# Imports
import os
import sys
import unittest
import time
import wx
from optparse import OptionParser

# Put Editra/src on the path
sys.path.append(os.path.abspath("../../src"))
sys.path.append(os.path.abspath("../../src/extern"))

# Local Utilities
import common

# ----------------- Helper Functions / Classes ---------------------

# TODO: maybe change some variable names?
# TODO: maybe put this function as a method somewhere else?
def _make_clean_opt_string():
    # which options was this run called with?
    # replace short opts with long opts (explicit is better than implicit)
    opt_string = ""
    args = sys.argv[1:]
    for arg in args:
        if arg.startswith("-") and not arg.startswith("--"):
            # handle the case where opt and arg are conjoined
            arg2 = None
            if len(arg) > 2:
                arg2 = arg[2:]
                arg  = arg[:2]
            # it's a short opt, now find it
            for opt in parser.option_list:
                if arg in opt._short_opts:
                    opt_string += opt._long_opts[0]
                    if opt.action == "store":
                        opt_string += "="
                        if arg2 != None:
                            opt_string += arg2
                    else:
                        opt_string += " "
        else:
            opt_string += arg
            opt_string += " "
    if opt_string == "":
        opt_string = "NONE"
    return opt_string

def output(string):
    print string

#-----------------------------------------------------------------------------#

class UnitTestSuite:
    def __init__(self, include="", exclude="", tests=""):
        # error checking
        if include != "" and exclude != "":
            raise ValueError("include and exclude arguments are mutually exclusive")
        # TODO: could this become a simple os.listdir(".")?
        _rootdir = os.path.abspath(sys.path[0])
        if not os.path.isdir(_rootdir):
            _rootdir = os.path.dirname(_rootdir)
        self.rootdir = _rootdir # to come in handy later
        # a dict of all possible test modules that could be run
        # ASSUME: each module name is unique not solely because of case
        _module_names = {}
        for _name in [ n[:-3] for n in os.listdir(self.rootdir)
                    if n.startswith("test") and n.endswith(".py") ]:
            _module_names[ _name.lower() ] = _name
        # make the include/exclude/tests lists
        _module_specs = None
        _spec_type    = None
        _test_specs   = None
        if include != "":
            _module_specs = self._clean_listify(include)
            _spec_type    = "include"
        elif exclude != "":
            _module_specs = self._clean_listify(exclude)
            _spec_type    = "exclude"

        if tests != "":
            _test_specs = self._clean_listify(tests, False)

        # make sure they all exist
        if _module_specs != None: # TODO: got to be a better place to put this
            for _mod in _module_specs:
                if not _module_names.has_key(_mod.lower()):
                    parser.error("Module %s not found under test" % (_mod))

        # now import the modules
        if _module_specs == None:
            self.modules = [ __import__(name) for name in _module_names.values() ]
        elif _spec_type == "include":
            self.modules = [ __import__(name) for name in _module_specs ]
        elif _spec_type == "exclude":
            self.modules = [ __import__(name) for name in _module_names.values()
                                            if name not in _module_specs ]
        # convert modules into suites
        self.suites = []
        for module in self.modules:
            _classname = module.__name__[4:] + "Test"
            _class = module.__getattribute__(_classname)
            # build test suite (whether or not --tests are specified)
            if _test_specs == None:
                _suite = unittest.makeSuite(_class)
            else:
                _suite = unittest.TestSuite()
                for _test_name in unittest.getTestCaseNames(_class,"test"):
                    for _test in _test_specs:
                        _docstr = getattr(_class, _test_name).__doc__
                        if _test_name.lower().find(_test.lower()) != -1 or \
                               _docstr != None and _docstr.lower().find(_test.lower()) != -1:
                            _suite.addTest(_class(_test_name))
                        break

            # filter out tests that shouldn't be run in subclasses
            _tests = _suite._tests
            for _t in _tests:
                # TODO: pull logic into wxtest
                # or use the version of unittest instead
                if sys.version_info[0:2] >= (2,5):
                    _mname = _t._testMethodName
                else:
                    _mname = _t._TestCase__testMethodName
                
                if _mname.find('_wx') != -1:
                    # grab the class: everything between '_wx' and 'Only' at the end
                    restriction = _mname[_mname.find('_wx')+3:-4]
                    if not _class.__name__.startswith(restriction):
                        #print "filtered: %s (class=%s)" % (mname,_class.__name__)
                        _tests.remove(_t)

            # if suite is non-empty...
            if _suite.countTestCases() > 0:
                # add it to the list of suites :-)
                self.suites.append(_suite)
    
    def _clean_listify(self, string, include_or_exclude=True):
        _clean_list = []
        _list = string.split(",")
        for s in _list:
            if include_or_exclude:
                if s.endswith(".py"):
                    s = s[:-3]
                if s.startswith("wx."):
                    s = "test" + s[3:]
                if not s.startswith("test"):
                    s = "test" + s
            _clean_list.append(s)
        # maintains capitalization
        return _clean_list
    
    def _start_figleaf(self):
        if options.figleaf != "":
            globals()["figleaf"] = __import__("figleaf")
            # TODO: perhaps make this class-specific rather than global?
            globals()["figfile"] = os.path.join(self.rootdir, options.figleaf_filename)
            if os.path.exists(figfile):
                os.remove(figfile)
            figleaf.start(ignore_python_lib=False)

    def _stop_figleaf(self):
        if options.figleaf != "":
            figleaf.stop()
            figleaf.write_coverage(figfile)
        
    def run(self):
        test_run_data = UnitTestRunData()
        self._start_figleaf()
        self.start_time = time.time()
        # run tests
        for _suite in self.suites:
            _result = unittest.TestResult()
            _suite.run(_result)
            _module_name = _suite._tests[0].__module__
            test_run_data.addResult(_module_name, _result)
        self.stop_time = time.time()
        self._stop_figleaf()
        # process results
        test_run_data.setTime(self.start_time, self.stop_time)
        test_run_data.process()
        # return results
        return test_run_data

#-----------------------------------------------------------------------------#

class UnitTestRunData:
    def __init__(self):
        self.results = {}
    
    def addResult(self, module_name, result):
        self.results[module_name] = result
    
    def setTime(self, start, stop):
        self.startTime = start
        self.stopTime  = stop
    
    def process(self):
        # process data
        self.elapsedTime = self.stopTime - self.startTime
        self.countSuites = len(self.results)
        self.countSuccesses = 0
        self.countFailures  = 0
        self.countErrors    = 0
        self.rawData = {}
        for _module_name, _result in self.results.iteritems():
            # TODO: revisit all this processing, is everything necessary?
            tmp = {}
            # parse results individually
            tmp["failures"]  = len(_result.failures)
            tmp["errors"]    = len(_result.errors)
            tmp["successes"] = _result.testsRun - tmp["failures"] - tmp["errors"]
            # total results
            self.countSuccesses += tmp["successes"]
            self.countFailures  += tmp["failures"]
            self.countErrors    += tmp["errors"]
            # TODO: add processing here
            tmp["failure_data"] = _result.failures
            tmp["error_data"]   = _result.errors
            self.rawData[_module_name] = tmp
        
# -----------------------------------------------------------
# -------------------- Option Logic -------------------------

# Options
usage = "usage: python %prog [options]"
parser = OptionParser(usage=usage)
parser.add_option("-o", "--output-filename", default="",
                    action="store", dest="outfilename",
                    metavar="FILE",
                    help="redirect output from console to FILE")
parser.add_option("-f", "--figleaf", default="",
                    action="store", dest="figleaf", metavar="FILE",
                    help="use the figleaf code-coverage tool, and write figleaf output to " +
                    "FILE. you must have figleaf installed to use this option. " +
                    "using this option will result in a slower test run")
parser.add_option("-i", "--include-modules", default="",
                    action="store", dest="module_list",
                    help="run only the comma-separated list of modules given. use either " +
                         "wx class names or the name of the desired test module. " + 
                         "don't use spaces in the list")
parser.add_option("-e", "--exclude-modules", default="",
                    action="store", dest="module_ex_list",
                    help="run all modules excluding those given in the comma-separated " + 
                    "list given. use either wx class names or the name of the desired " +
                    "test module.")
parser.add_option("-t", "--tests", default="",
                    action="store", dest="test_list",
                    help="run only a targeted list of tests. give a comma-separated list " +
                            "of strings, and each test whose name or docstring contains " +
                            "one of those given will be run.")

def runUnitTestsAndOutputResults():   
    unit_test_suite = UnitTestSuite(include=options.module_list,
                                    exclude=options.module_ex_list,
                                    tests=options.test_list)
    
    result_data = unit_test_suite.run()
    
    # see refactored method above
    opt_string = _make_clean_opt_string()
    
    # -----------------------------------------------------------
    # ------------------- Output Reporting ----------------------
    output("") # make things easier to read
    output("%s - %s\n" % (time.asctime(), wx.GetOsDescription()))
    output("Platform Information")
    output("Platform [sys.platform]: %s" % sys.platform)
    output("Python Version [sys.version]: %s" % sys.version)
    output("wx Version [wx.version()]: %s" % wx.version())
    output("OS [wx.GetOsDescription()]: %s" % wx.GetOsDescription())
    output("wx Info [wx.PlatformInfo]: %s" % str(wx.PlatformInfo))
    output("runUnitTests.py options: %s" % opt_string)
    output("\n----------------------\n")
    
    output("Summary")
    output("Run completed in %.2f seconds" % (result_data.elapsedTime))
    output("%d classes tested" % (result_data.countSuites))
    output("%d tests passed in total!" % (result_data.countSuccesses))
    if result_data.countFailures > 0:
        output("%d tests failed in total!" % (result_data.countFailures))
    if result_data.countErrors > 0:
        output("%d tests erred in total!" % (result_data.countErrors))
    output("\n----------------------\n")
    
    data_items = result_data.rawData.items()
    data_items.sort()
    
    output("Module Data")
    for mod_name, results in data_items:
        messages = ["%d passed" % (results["successes"])]
        if results["failures"] > 0:
            messages.append("%d failed" % (results["failures"]))
        if results["errors"] > 0:
            messages.append("%d erred"  % (results["errors"]))
        output("%s:  %s" % (mod_name, ", ".join(messages)))
    output("\n----------------------\n")
    
    if result_data.countFailures + result_data.countErrors > 0:
        output("Failure Data")
    for mod_name, results in data_items:
        # report on it
        for failure in results["failure_data"] + results["error_data"]:
            type = None
            if failure in results["failure_data"]:
                type = "Fail: "
            elif failure in results["error_data"]:
                type = "Error: "
            output("   " + type + str(failure[0]))
            output("      " + str(failure[1]).replace("\n","\n      "))

#-----------------------------------------------------------------------------#
if __name__ == '__main__':
    (options, args) = parser.parse_args()

    # Options error-checking
    if options.module_list != "" and options.module_ex_list != "":
        parser.error("options --exclude-modules and --include-modules are mutually exclusive")
        
    # File redirect
    if options.outfilename != "":
        origstdout = sys.stdout
        try:
            sys.stdout = open(options.outfilename,'w')
        except IOError:
            print "Error opening output file, defaulting to original stdout"
            sys.stdout = origstdout

    app = common.EdApp(False)
    runUnitTestsAndOutputResults()
#    app.MainLoop()

