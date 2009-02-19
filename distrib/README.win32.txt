wxPython win32 README
---------------------

The self-installer package you have just installed contains the Python
extension modules, python modules and packages needed to run wxPython
applications.  If you selected the "Make this install be the default
wxPython" option in the installer then this version will be the one
that is imported when apps do "import wx".  See the following wiki
page for more information about managing multiple installs:

      http://wiki.wxpython.org/index.cgi/MultiVersionInstalls

In addition to the wxPython modules, several tools scripts (such as
XRCed and PyShell) and batch file launchers have been installed to
Python's Scripts directory.  (For example, c:\Python23\Scripts.)  If
you have multiple versions of wxPython installed these tool scripts
will use whichever is the default install.  If you would like to
control which version is used then follow the directions at the wiki
page for using wxversion.

This installer does *not* include the wxPython documentation, the
wxPython demo and other sample applications that are provided as part
of wxPython.  Those are available in a separate installer named
wxPython2.6-win32-docs-demos-*.exe which should also be located from
wherever you downloaded this package from.  The Docs and Demos
installer will also create Start Menu shortcuts for the tool scripts
mentioned above.


PYTHON 2.6 NOTE 
----------------

If you are using Python 2.6 you may notice that your wxPython
applications on XP or Vista are not using the newer themed controls.
This happens because Windows is loading the old version of the common
controls DLL instead of the new version.  In order to change this we
need to change the menifest resource embedded in the executable file.
To help you do this we've installed a script next to your python.exe
called update_manifest.py which you can run to replace the manifest
resource in both python.exe and pythonw.exe, however it may not be
able to update a python executable that is un use running some script
(including update_manifest) so you may need to create a copy of
python.exe and use the copy to run the script in order for it to be
successful.
