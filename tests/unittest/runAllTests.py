import os, sys
from optparse import OptionParser

# Options
# TODO: would log4py be better than custom flags?
# TODO: ability to turn off figleaf
# TODO: store textual output in a file
# TODO: configure which modules run via command line
usage = "usage: python %prog [options]"
parser = OptionParser(usage=usage)
parser.set_defaults(verbose=True, failure_details=False)
parser.add_option("-v","--verbose",
                    action="store_true", dest="verbose",
                    help="report on each module individually")
parser.add_option("-q","--quiet",
                    action="store_false", dest="verbose",
                    help="only print pass/fail/error totals")
parser.add_option("-d","--failure-details",
                    action="store_true", dest="failure_details",
                    help="print information on each failure"
                    )
parser.add_option("-f", "--filename",
                    action="store", dest="filename",
                    metavar="FILE", default="tests.figleaf",
                    help="write figleaf output to FILE [default: %default]"),
(options, args) = parser.parse_args()

# Figleaf
rootdir = os.path.abspath(sys.path[0])
if not os.path.isdir(rootdir):
    rootdir = os.path.dirname(rootdir)
figfile = os.path.join(rootdir, options.filename)

if os.path.exists(figfile):
    os.remove(figfile)

# note figleaf dependency
# may want to revisit this issue in the future
import figleaf
figleaf.start(ignore_python_lib=False)

import unittest

modules = [__import__(f[:-3]) for f in os.listdir(rootdir) 
                if f.startswith('test') and f.endswith('.py')]

alltests = unittest.TestSuite([mod.suite() for mod in modules])

results = unittest.TestResult()
alltests.run(results)

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
    print "----------------------"

print "%d tests passed in total!" % (total_successes)
if total_failures > 0:
    print "%d tests failed in total!" % (total_failures)
if total_errors > 0:
    print "%d tests erred in total!" % (total_errors)

figleaf.stop()
figleaf.write_coverage(figfile)

# this is broken for some reason
#os.system("figleaf2html -d ./tests_code_coverage %s" % figfile)
