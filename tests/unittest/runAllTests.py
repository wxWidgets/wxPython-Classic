import os, sys
import unittest
import time
import wx
from optparse import OptionParser

# TODO: separate option-logic from test-running from output-reporting

# ------------------- Helper Methods ------------------------

def make_suite(mod, tests=[]):
    suite = unittest.TestSuite()
    _classname = mod.__name__[4:] + "Test"
    _class = mod.__getattribute__(_classname)
    if len(tests) == 0:
        suite = unittest.makeSuite(_class)
    else:
        # go through and make it yourself
        for testname in unittest.getTestCaseNames(_class,"test"):
            for t in tests:
                if testname.find(t) != -1:
                    suite.addTest(_class(testname))
                    break
                # TODO: also check docstring
    return suite

def wiki(string):
    if options.wiki:
        print string

def start_figleaf():
    if options.figleaf:
        globals()["figleaf"] = __import__("figleaf")
        globals()["figfile"] = os.path.join(rootdir, options.figleaf_filename)
        if os.path.exists(figfile):
            os.remove(figfile)
        figleaf.start(ignore_python_lib=False)

def stop_figleaf():
    if options.figleaf:
        figleaf.stop()
        figleaf.write_coverage(figfile)

def output_summary(wiki=False):
    if wiki:
        print "==== Summary ===="
    if wiki:
        print " * ",
    print "Run completed in %.2f seconds" % (stop_time-start_time)
    if wiki:
        print " * ",
    print "%d classes tested" % (len(modules))
    if wiki:
        print " * ",
    print "%d tests passed in total!" % (totals['successes'])
    if totals['failures'] > 0:
        if wiki:
            print " * ",
        print "%d tests failed in total!" % (totals['failures'])
    if totals['errors'] > 0:
        if wiki:
            print " * ",
        print "%d tests erred in total!" % (totals['errors'])

def output_failure_data(failure, wiki):
    if wiki:
        print "\n * " + str(failure[0]).replace('.','.!')
        print " {{{" + str(failure[1]) + "}}}"
    else:
        print "\n------ " + str(failure[0]) + " ------"
        print failure[1],
        
# -----------------------------------------------------------
# -------------------- Option Logic -------------------------

# Options
# TODO: would log4py be better than custom flags?
usage = "usage: python %prog [options]"
parser = OptionParser(usage=usage)
parser.set_defaults(verbose=True, failure_details=False,
                    wiki=False, figleaf=True)
parser.add_option("-v","--verbose",
                    action="store_true", dest="verbose",
                    help="report on each module individually [default]")
parser.add_option("-q","--quiet",
                    action="store_false", dest="verbose",
                    help="only print pass/fail/error totals")
parser.add_option("-d","--failure-details",
                    action="store_true", dest="failure_details",
                    help="print information on each failure")
parser.add_option("-o", "--output-filename",
                    action="store", dest="outfilename",
                    metavar="FILE", default="",
                    help="redirect output from console to FILE")
parser.add_option("-f", "--figleaf-filename",
                    action="store", dest="figleaf_filename",
                    metavar="FILE", default="tests.figleaf",
                    help="write figleaf output to FILE [default: %default]")
parser.add_option("-w", "--wiki",
                    action="store_true", dest="wiki",
                    help="write data in wiki-markup format (MoinMoin / wxPyWiki)")
parser.add_option("-x", "--no-figleaf",
                    action="store_false", dest="figleaf",
                    help="don't use figleaf (code coverage tool). makes runs quicker.")
# TODO: make module parsing case-insensitive?
parser.add_option("-m", "--modules",
                    action="store", dest="module_list", default="",
                    help="run only the comma-separated list of modules given. use either " +
                            "wx class names or the name of the desired test module. " + 
                            "don't use spaces in the list")
# TODO: make other test specification case-insensitive?
parser.add_option("-t", "--tests",
                    action="store", dest="test_list", default="",
                    help="run only a targeted list of tests. give a comma-separated list " +
                            "of strings, and each test whose name or docstring contains " +
                            "one of those given will be run.")
(options, args) = parser.parse_args()

# Options error-checking
if not options.figleaf and options.figleaf_filename != 'tests.figleaf':
    # not strictly necessary, but -f is useless with -x
    parser.error("options -f and -x are mutually exclusive")
# may need error-checking, might be a bad idea, but i'm making -w override others
if options.wiki:
    options.failure_details = True
    options.verbose = False
    
# -----------------------------------------------------------
# ------------------- Test Running --------------------------
rootdir = os.path.abspath(sys.path[0])
if not os.path.isdir(rootdir):
    rootdir = os.path.dirname(rootdir)
    
# File redirect
origstdout = None
if options.outfilename != "":
    origstdout = sys.stdout
    try:
        sys.stdout = open(options.outfilename,'w')
    except IOError:
        print "Error opening output file, defaulting to original stdout"
        sys.stdout = origstdout

# which test modules should be run?
module_names = [ n[:-3] for n in os.listdir(rootdir)
                    if n.startswith('test') and n.endswith(".py") ]
if options.module_list != "":
    module_name_list = options.module_list.split(",")
    tmp = []
    for s in module_name_list:
        if s.endswith(".py"):
            s = s[:-3]
        if s.startswith("wx."):
            s = "test" + s[3:]
        if not s.startswith("test"):
            s = "test" + s
        if s in module_names:
            tmp.append(s)
        else:
            parser.error("Class not found under test")
    module_names = tmp
    
modules = [ __import__(mod) for mod in module_names ]

tests = options.test_list.split(",")
if options.test_list == "":
    tests = []

# run tests
results = {}
start_figleaf()
start_time = time.time()
for module in modules:
    suite = make_suite(module,tests)
    if suite.countTestCases() == 0:
        continue
    result = unittest.TestResult()
    suite.run(result)
    results[module.__name__] = result
stop_time = time.time()
stop_figleaf()

# process data
totals = {}
data   = {}
totals["successes"] = 0
totals["failures"]  = 0
totals["errors"]    = 0
for mod_name, result in results.iteritems():
    tmp = {}
    tmp["failures"]  = len(result.failures)
    tmp["errors"]    = len(result.errors)
    tmp["successes"] = result.testsRun - tmp["failures"] - tmp["errors"]
    for s in ("failures","errors","successes"):
        totals[s] += tmp[s]
    # TODO: add processing here...
    tmp["failure_data"] = result.failures
    tmp["error_data"]   = result.errors
    data[mod_name] = tmp

# -----------------------------------------------------------
# ------------------- Output Reporting ----------------------
wiki("=== %s - %s ===" % (time.asctime(),wx.GetOsDescription()))
wiki("==== Platform Information ====")
wiki(" * '''Platform [sys.platform]''': %s" % (sys.platform))
wiki(" * '''Python Version [sys.version]''': %s" % (sys.version))
wiki(" * '''wx Version [wx.version()]''': %s" % (wx.version()))
wiki(" * '''OS [wx.!GetOsDescription()]''': %s" % (wx.GetOsDescription()))

# TODO: add a preliminary "here's what I was told to run" output,
#   and include command-line switches. wiki-only?

output_summary(options.wiki)
if options.verbose or options.failure_details and not options.wiki:
    print "\n----------------------\n"

wiki("==== Failure Data ====")
for mod_name, results in data.iteritems():
    # report on it
    if options.verbose:
        print "%s:\t%d tests passed" % (mod_name, results["successes"])
    if results["failures"] > 0:
        if options.verbose:
            print "%s:\t%d tests failed!" % (mod_name, results["failures"])
        if options.failure_details:
            for failure in results["failure_data"]:
                output_failure_data(failure, options.wiki)
    if results["errors"] > 0:
        if options.verbose:
            print "%s:\t%d tests in error!" % (mod_name, results["errors"])
        if options.failure_details:
            for error in results["error_data"]:
                output_failure_data(error, options.wiki)
    
if origstdout != None:
    sys.stdout = origstdout
    output_summary()

# this is broken for some reason
#os.system("figleaf2html -d ./tests_code_coverage %s" % figfile)
