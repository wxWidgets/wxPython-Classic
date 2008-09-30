"""Test-runner for wxPython's unit test suite.

TODO: document all functionality"""

import os, sys
import unittest
import time
import wx
from optparse import OptionParser

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

def wiki(string, level=3, reverse=False):
    if options.wiki and not reverse or not options.wiki and reverse:
        output(level, string)
    
def wiki_title(number, string):
    if options.wiki:
        title = "=" * number
        return title + " " + string + " " + title
    else:
        return string

def wiki_bullet():
    if options.wiki:
        return " * "
    else:
        return ""

def wiki_bold(string):
    if options.wiki:
        return "'''" + string + "'''"
    else:
        return string

def wiki_summary_item(title, data):
    # TODO: possible more elegant way with regexes?
    if options.wiki:
        # escape the CamelCase for wiki only
        # ASSUME: max one CamelCase, right after a period
        i = title.find(".")
        if i != -1 and title[i+1].isupper():
            title = title.replace(".", ".!")
    return wiki_bullet() + wiki_bold(title) + ": %s" % (data)
        
def output(level, string):
    if options.verbosity >= level:
        print string

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
parser.add_option("-v","--verbosity", default=3,
                    action="store", type="int", dest="verbosity",
                    help="An integer [from 0 to 5, default=3] determining " +
                            "how much test result data will be output.")
parser.add_option("-o", "--output-filename", default="",
                    action="store", dest="outfilename",
                    metavar="FILE",
                    help="redirect output from console to FILE")
parser.add_option("-f", "--figleaf", default="",
                    action="store", dest="figleaf", metavar="FILE",
                    help="use the figleaf code-coverage tool, and write figleaf output to " +
                    "FILE. you must have figleaf installed to use this option. " +
                    "using this option will result in a slower test run")
parser.add_option("-w", "--wiki", default=False,
                    action="store_true", dest="wiki",
                    help="write data in wiki-markup format (MoinMoin / wxPyWiki)")
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
# TODO: add "--include-methods" and "--exclude-methods" functionality
(options, args) = parser.parse_args()

# Options error-checking
if options.module_list != "" and options.module_ex_list != "":
    parser.error("options --exclude-modules and --include-modules are mutually exclusive")
# doesn't really matter, but the help screen says it, so enforce it
if options.verbosity < 0 or options.verbosity > 5:
    parser.error("verbosity must be between 0 and 5")
    
# -----------------------------------------------------------
# ------------------- Test Running --------------------------

# File redirect
if options.outfilename != "":
    origstdout = sys.stdout
    try:
        sys.stdout = open(options.outfilename,'w')
    except IOError:
        print "Error opening output file, defaulting to original stdout"
        sys.stdout = origstdout

def runUnitTestsAndOutputResults():   
    unit_test_suite = UnitTestSuite(include=options.module_list,
                                    exclude=options.module_ex_list,
                                    tests=options.test_list)
    
    result_data = unit_test_suite.run()
    
    # see refactored method above
    opt_string = _make_clean_opt_string()
    
    # -----------------------------------------------------------
    # ------------------- Output Reporting ----------------------
    output(1, "") # make things easier to read
    wiki(wiki_title(3, "%s - %s" % (time.asctime(),wx.GetOsDescription())), level=2)
    output(2, wiki_title(4, "Platform Information"))
    output(2, wiki_summary_item("Platform [sys.platform]",sys.platform))
    output(2, wiki_summary_item("Python Version [sys.version]",sys.version))
    output(2, wiki_summary_item("wx Version [wx.version()]",wx.version()))
    output(2, wiki_summary_item("OS [wx.GetOsDescription()]",wx.GetOsDescription()))
    output(2, wiki_summary_item("wx Info [wx.PlatformInfo]",str(wx.PlatformInfo)))
    output(2, wiki_summary_item("runUnitTests.py options",opt_string))
    wiki("\n----------------------\n", level=3, reverse=True)
    
    output(1, wiki_title(4, "Summary"))
    output(2, wiki_bullet() + "Run completed in %.2f seconds" % (result_data.elapsedTime))
    output(2, wiki_bullet() + "%d classes tested" % (result_data.countSuites))
    output(1, wiki_bullet() + "%d tests passed in total!" % (result_data.countSuccesses))
    if result_data.countFailures > 0:
        output(1, wiki_bullet() + "%d tests failed in total!" % (result_data.countFailures))
    if result_data.countErrors > 0:
        output(1, wiki_bullet() + "%d tests erred in total!" % (result_data.countErrors))
    wiki("\n----------------------\n", level=3, reverse=True)
    
    data_items = result_data.rawData.items()
    data_items.sort()
    
    output(3, wiki_title(4, "Module Data"))
    for mod_name, results in data_items:
        messages = ["%d passed" % (results["successes"])]
        if results["failures"] > 0:
            messages.append("%d failed" % (results["failures"]))
        if results["errors"] > 0:
            messages.append("%d erred"  % (results["errors"]))
        output(3, wiki_bullet() + "%s:  %s" % (mod_name, ", ".join(messages)))
    wiki("\n----------------------\n", level=4, reverse=True)
    
    if result_data.countFailures + result_data.countErrors > 0:
        output(4, wiki_title(4,"Failure Data"))
    for mod_name, results in data_items:
        # report on it
        for failure in results["failure_data"] + results["error_data"]:
            type = None
            if failure in results["failure_data"]:
                type = "Fail: "
            elif failure in results["error_data"]:
                type = "Error: "
            if options.wiki:
                output(4, wiki_bullet() + type + str(failure[0]).replace('.','.!'))
                output(5," {{{" + str(failure[1]) + "}}}")
            else:
                output(4, "   " + type + str(failure[0]))
                output(5, "      " + str(failure[1]).replace("\n","\n      "))
                
class MyApp(wx.App):
    def __init__(self):
        wx.App.__init__(self, redirect=False)
        
    def OnInit(self):
        runUnitTestsAndOutputResults()
        wx.CallAfter(self.ExitMainLoop)
        return True
        
app = MyApp()
app.MainLoop()
