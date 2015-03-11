###############################################################################
# Name: testThreadpool.py                                                     #
# Purpose: Unit tests for the Icon Theme provider                             #
# Author: Cody Precord <cprecord@editra.org>                                  #
# Copyright: (c) 2011 Cody Precord <staff@editra.org>                         #
# License: wxWindows License                                                  #
###############################################################################

"""Unittest cases for testing the icon theme provider interface"""

__author__ = "Cody Precord <cprecord@editra.org>"
__svnid__ = "$Id:  $"
__revision__ = "$Revision:  $"

#-----------------------------------------------------------------------------#
# Imports
import wx
import os
import time
import threading
import unittest

# Module to test
import ebmlib

#-----------------------------------------------------------------------------#
# Test Class

def doWork(seconds, id_, callback):
    """Worker job for threadpool test"""
    time.sleep(seconds)
    callback(id_) # notify done

class ThreadpoolTest(unittest.TestCase):
    """Tests the ThreadPool class"""
    def setUp(self):
        self._threads = 3
        self.pool = ebmlib.ThreadPool(self._threads)
        self._completed = list()
        self._lock = threading.Lock()

    def tearDown(self):
        self.pool.Shutdown()
        self._completed = list()

    def notifyDone(self, id_):
        with self._lock:
            self._completed.append(id_)

    #---- Test Cases ----#

    def testThreadCount(self):
        """Check that thread pool spawned off requested number of threads"""
        self.assertEquals(self.pool.ThreadCount, self._threads)

    def testQueueJob(self):
        jobs = [ (1.5, 1), (2, 2), (0.5, 3), (1, 4) ]
        for job in jobs:
            self.pool.QueueJob(doWork, job[0], job[1], self.notifyDone)
        maxwait = sum([j[0] for j in jobs])
        time.sleep(maxwait) # wait for the jobs to finish
        self.assertTrue(len(jobs) == len(self._completed), repr(self._completed))
