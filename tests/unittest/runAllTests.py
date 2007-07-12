import os, sys
import unittest
import time
import wx
from optparse import OptionParser

# TODO: separate option-logic from test-running from output-reporting

# ------------------- Helper Methods ------------------------

def start_figleaf():
    if options.figleaf:
        globals()['figleaf'] = __import__('figleaf')
        globals()['figfile'] = os.path.join(rootdir, options.figleaf_filename)
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
    print "%d tests passed in total!" % (total_successes)
    if total_failures > 0:
        if wiki:
            print " * ",
        print "%d tests failed in total!" % (total_failures)
    if total_errors > 0:
        if wiki:
            print " * ",
        print "%d tests erred in total!" % (total_errors)

def output_failure_data(failure, wiki):
    if wiki:
        print "\n * " + str(failure[0]).replace('.','.!')
        print " {{{" + str(failure[1]) + "}}}"
    else:
        print "\n------ " + str(failure[0]) + " ------"
        print failure[1],

def wiki_header():
    if options.wiki:
        print "=== %s - %s ===" % (time.asctime(),wx.GetOsDescription())

def wiki_platform_info():
    if options.wiki:
        print "==== Platform Information ===="
        print " * '''Platform [sys.platform]''': %s" % (sys.platform)
        print " * '''Python Version [sys.version]''': %s" % (sys.version)
        print " * '''wx Version [wx.version()]''': %s" % (wx.version())
        print " * '''OS [wx.!GetOsDescription()]''': %s" % (wx.GetOsDescription())
        
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
                    help="don't use figleaf (code coverage tool)")
# TODO: make module parsing case-insensitive?
parser.add_option("-m", "--modules",
                    action="store", dest="module_list", default="",
                    help="run only the comma-separated list of modules given. use either " +
                            "wx class names or the name of the desired test module. " + 
                            "don't use spaces in the list")
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

start_figleaf()

module_names = [ n[:-3] for n in os.listdir(rootdir)
                    if n.startswith('test') and n.endswith('.py') ]
if options.module_list != "":
    module_name_list = options.module_list.split(',')
    tmp = []
    for s in module_name_list:
        if s.endswith('.py'):
            s = s[:-3]
        if s.startswith('wx.'):
            s = 'test' + s[3:]
        if not s.startswith('test'):
            s = 'test' + s
        if s in module_names:
            tmp.append(s)
        else:
            parser.error('asdf')
    module_names = tmp
    
modules = [ __import__(mod) for mod in module_names ]

wiki_header()
wiki_platform_info()
# TODO: add a preliminary "here's what I was told to run" output,
#   and include command-line switches. wiki-only?
                
total_successes = 0
total_failures  = 0
total_errors    = 0
start_time = time.time()
if options.wiki:
    print "==== Failure Data ===="
for module in modules:
    # run suite
    suite = module.suite()
    results = unittest.TestResult()
    suite.run(results)
    # report on it
    failures  = len(results.failures)
    errors    = len(results.errors)
    successes = results.testsRun - failures - errors
    total_failures  += failures
    total_errors    += errors
    total_successes += successes
    if options.verbose:
        print "%s:\t%d tests passed" % (module.__name__, successes)
    if failures > 0:
        if options.verbose:
            print "%s:\t%d tests failed!" % (module.__name__, failures)
        if options.failure_details:
            for failure in results.failures:
                output_failure_data(failure, options.wiki)
    if errors > 0:
        if options.verbose:
            print "%s:\t%d tests in error!" % (module.__name__, errors)
        if options.failure_details:
            for error in results.errors:
                output_failure_data(error, options.wiki)
stop_time = time.time()
if options.verbose or options.failure_details and not options.wiki:
    print "\n----------------------\n"

# -----------------------------------------------------------

# ------------------- Output Reporting --------------------------

output_summary(options.wiki)
if origstdout != None:
    sys.stdout = origstdout
    output_summary()

stop_figleaf()

# this is broken for some reason
#os.system("figleaf2html -d ./tests_code_coverage %s" % figfile)
