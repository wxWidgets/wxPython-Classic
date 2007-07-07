import os, sys
import unittest
from optparse import OptionParser

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

def output_summary():
    # TODO: add time and duration of test run to output
    print "%d tests passed in total!" % (total_successes)
    if total_failures > 0:
        print "%d tests failed in total!" % (total_failures)
    if total_errors > 0:
        print "%d tests erred in total!" % (total_errors)
        
# -----------------------------------------------------------

# Options
# TODO: would log4py be better than custom flags?
# TODO: ability to turn off figleaf
# TODO: store textual output in a file
# TODO: configure which modules run via command line
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
parser.add_option("-x", "--no-figleaf",
                    action="store_false", dest="figleaf",
                    help="don't use figleaf (code coverage tool)")
(options, args) = parser.parse_args()

# Options error-checking
if not options.figleaf and options.figleaf_filename != 'tests.figleaf':
    # not strictly necessary, but -f is useless with -x
    parser.error("options -f and -x are mutually exclusive")


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

modules = [__import__(f[:-3]) for f in os.listdir(rootdir) 
                if f.startswith('test') and f.endswith('.py')]
                
total_successes = 0
total_failures  = 0
total_errors    = 0
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
                print "\n------ " + str(failure[0]) + " ------"
                print failure[1],
    if errors > 0:
        if options.verbose:
            print "%s:\t%d tests in error!" % (module.__name__, errors)
        if options.failure_details:
            for error in results.errors:
                print "\n------ " + str(error[0]) + " ------"
                print error[1],
if options.verbose or options.failure_details:
    print "\n----------------------\n"

output_summary()
if origstdout != None:
    sys.stdout = origstdout
    output_summary()

stop_figleaf()

# this is broken for some reason
#os.system("figleaf2html -d ./tests_code_coverage %s" % figfile)
