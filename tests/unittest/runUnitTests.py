import os, sys
import unittest
import time
import wx
from optparse import OptionParser

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
                docstr = getattr(_class, testname).__doc__
                if testname.lower().find(t.lower()) != -1 or \
                       docstr != None and docstr.lower().find(t.lower()) != -1:
                    suite.addTest(_class(testname))
                    break
    # filter out tests that shouldn't be run in subclasses
    tests = suite._tests
    for test in tests:
        mname = test._testMethodName
        if mname.find('_wx') != -1:
            # grab the class: everything between '_wx' and 'Only' at the end
            restriction = mname[mname.find('_wx')+3:-4]
            if not _class.__name__.startswith(restriction):
                #print "filtered: %s (class=%s)" % (mname,_class.__name__)
                tests.remove(test)
    return suite

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
    return wiki_bullet() + wiki_bold(title) + ": %s" % (data)
        
def output(level, string):
    if options.verbosity >= level:
        print string

def start_figleaf():
    if options.figleaf != "":
        globals()["figleaf"] = __import__("figleaf")
        globals()["figfile"] = os.path.join(rootdir, options.figleaf_filename)
        if os.path.exists(figfile):
            os.remove(figfile)
        figleaf.start(ignore_python_lib=False)

def stop_figleaf():
    if options.figleaf != "":
        figleaf.stop()
        figleaf.write_coverage(figfile)
        
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
                    help="use figleaf, and write figleaf output to FILE. " +
                            "this slows down the test run")
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
(options, args) = parser.parse_args()

# Options error-checking
if options.module_list != "" and options.module_ex_list != "":
    parser.error("options --exclude-modules and --include-modules are mutually exclusive")
# doesn't really matter, but the help screen says it, so enforce it
if options.verbosity < 0 or options.verbosity > 5:
    parser.error("verbosity must be between 0 and 5")
    
# -----------------------------------------------------------
# ------------------- Test Running --------------------------
rootdir = os.path.abspath(sys.path[0])
if not os.path.isdir(rootdir):
    rootdir = os.path.dirname(rootdir)

# File redirect
if options.outfilename != "":
    origstdout = sys.stdout
    try:
        sys.stdout = open(options.outfilename,'w')
    except IOError:
        print "Error opening output file, defaulting to original stdout"
        sys.stdout = origstdout

# which test modules should be run?
# ASSUME: each module name is unique not solely because of case
module_names = {}
for name in [ n[:-3] for n in os.listdir(rootdir)
                    if n.startswith('test') and n.endswith(".py") ]:
    module_names[ name.lower() ] = name

# process --include-modules option
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
        if module_names.has_key(s.lower()):
            tmp.append(module_names[s.lower()])
        else:
            parser.error("Class %s not found under test" % (s))
    module_names = tmp

# process --exclude-modules option
if options.module_ex_list != "":
    ex_list_raw = options.module_ex_list.split(",")
    ex_list = []
    for s in ex_list_raw:
        if s.endswith(".py"):
            s = s[:-3]
        if s.startswith("wx."):
            s = "test" + s[3:]
        if not s.startswith("test"):
            s = "test" + s
        ex_list.append(s)
    for s in ex_list:
        if module_names.has_key(s.lower()):
            del module_names[s.lower()]
        else:
            parser.error("Class %s not found under test" % (s))

# the logic for -i changes module_names from a dict to a list
# normalize other program paths here.
if type(module_names) == dict:
    module_names = module_names.values()
modules = [ __import__(mod) for mod in module_names ]

tests = options.test_list.split(",")
if options.test_list == "":
    tests = []

# run tests
num_classes = 0
results = {}
start_figleaf()
start_time = time.time()
for module in modules:
    suite = make_suite(module,tests)
    if suite.countTestCases() == 0:
        continue
    else:
        num_classes += 1
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

# which options was this run called with?
opt_string = " ".join(sys.argv[1:])
# replace short opts with long opts (explicit is better than implicit)
for opt in parser.option_list:
    opt_string = opt_string.replace(" " + opt._short_opts[0], " " + opt._long_opts[0])
    opt_string = opt_string.replace(opt._short_opts[0] + " ", opt._long_opts[0] + " ")

# -----------------------------------------------------------
# ------------------- Output Reporting ----------------------
output(1, "") # make things easier to read
wiki(wiki_title(3, "%s - %s" % (time.asctime(),wx.GetOsDescription())), level=2)
output(3, wiki_title(4, "Platform Information"))
output(3, wiki_summary_item("Platform [sys.platform]",sys.platform))
output(3, wiki_summary_item("Python Version [sys.version]",sys.version))
output(3, wiki_summary_item("wx Version [wx.version()]",wx.version()))
output(3, wiki_summary_item("OS [wx.!GetOsDescription()]",wx.GetOsDescription()))
output(3, wiki_summary_item("wx Info [wx.!PlatformInfo]",str(wx.PlatformInfo)))
output(3, wiki_summary_item("runUnitTests.py options",opt_string))
wiki("\n----------------------\n", level=3, reverse=True)

output(1, wiki_title(4, "Summary"))
output(2, wiki_bullet() + "Run completed in %.2f seconds" % (stop_time-start_time))
output(2, wiki_bullet() + "%d classes tested" % (num_classes))
output(1, wiki_bullet() + "%d tests passed in total!" % (totals['successes']))
if totals['failures'] > 0:
    output(1, wiki_bullet() + "%d tests failed in total!" % (totals['failures']))
if totals['errors'] > 0:
    output(1, wiki_bullet() + "%d tests erred in total!" % (totals['errors']))
wiki("\n----------------------\n", level=3, reverse=True)

data_items = data.items()
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