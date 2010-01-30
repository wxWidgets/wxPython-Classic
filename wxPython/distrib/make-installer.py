#!/usr/bin/env python

import optparse
import os
import shutil
import string
import sys
import tempfile

script_dir = os.path.abspath(sys.path[0])
wxpy_dir = os.path.abspath(os.path.join(script_dir, ".."))

wx_version = "2.9.0"
py_version = "2.5"

tempdir = "/tmp/wxpy-%s-py%s" % (wx_version, py_version)
installroot = os.path.join(tempdir, "install-root")
installapps = os.path.join(tempdir, "install-apps")

prefix = ""
sitepackages = ""

platform = "gtk"
if sys.platform.startswith("win"):
    platform = "msw"
elif sys.platform.startswith("darwin"):
    platform = "osx"
    
pkgname = "wxPython%s-%s-py%s" % (wx_version[:3], platform, py_version)

if platform == "msw":
    print "Please define these values for your platform."
    assert False
elif platform == "osx":
    prefix = "/usr/local/lib/" + pkgname
    sitepackages = "/Library/Python/" + py_version
elif platform == "gtk":
    prefix = "/usr/local/lib/" + pkgname
    sitepackages = "/lib/python%s/site-packages" % py_version
else:
    print "Please define these values for your platform."
    assert False


def exitIfError(cmd):
    retval = os.system(cmd)
    if retval != 0:
        if os.path.exists(tempdir):
            shutil.rmtree(tempdir)
        sys.exit(1)

wxroot = installroot + prefix
wxpythonroot = installroot + sitepackages

os.makedirs(wxroot)
os.makedirs(wxpythonroot)

build_options = ["--unicode"]

if not sys.platform.startswith("win"):
    build_options.extend(["--install", "--install_dir=%s" % wxroot,
                    "--wxpy_install_dir=%s" % wxpythonroot])

if sys.platform.startswith("darwin"):
    build_options.append("--osx_cocoa")

exitIfError(sys.executable + " %s/build-wxpython.py %s" % (wxpy_dir, string.join(build_options, " ")))
    
if sys.platform.startswith("darwin"):
    if os.path.exists(pkgname + ".pkg"):
        shutil.rmtree(pkgname + ".pkg")

    pkg_args = ['--Title=' + pkgname,
                '--Version=' + wx_version,
                '--Description="wxPython runtime %s for the Universal version of MacPython %s"' % (wx_version, py_version),
                '--NeedsAuthorization="YES"',
                '--Relocatable="NO"',
                '--InstallOnly="YES"',
                installroot,
                "mac/resources"
                ]

    exitIfError(sys.executable + " %s/mac/buildpkg.py %s" % (script_dir, string.join(pkg_args, " ")))

if os.path.exists(tempdir):
    shutil.rmtree(tempdir)
