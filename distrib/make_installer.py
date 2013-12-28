# -*- coding: iso-8859-1 -*-
#----------------------------------------------------------------------
# Name:        make_installer.py
# Purpose:     A script to create the wxPython windows installer
#
# Author:      Robin Dunn
#
# Created:     30-April-2001
# RCS-ID:      $Id$
# Copyright:   (c) 2003 by Total Control Software
# Licence:     wxWindows license
#----------------------------------------------------------------------

"""
This script will generate a setup script for InnoSetup and then run it
to make the installer executable.  If all goes right the proper versions
of Python and wxWindows (including hybrid/final settings) will all be
calculated based on what _core_.pyd imports and an appropriate installer
will be created.
"""


import sys, os, time, glob

KEEP_TEMPS = False

# default InnoSetup installer location
ISCC = r"%s\InnoSetup5\ISCC.exe %s"

if os.environ.has_key("INNO5"):
    ISCC = os.environ["INNO5"]


#----------------------------------------------------------------------

ISS_Template = r'''

[Setup]
AppName = wxPython%(SHORTVER)s-%(PYVER)s
AppVerName = wxPython %(VERSION)s for Python %(PYTHONVER)s
OutputBaseFilename = wxPython%(SHORTVER)s-win%(BITS)s-%(VERSION)s-%(PYVER)s
AppCopyright = Copyright 2011 Total Control Software
DefaultDirName = {code:GetInstallDir|c:\DoNotInstallHere}
DefaultGroupName = wxPython %(VERSION)s for Python %(PYTHONVER)s
PrivilegesRequired = %(PRIV)s
OutputDir = dist
DisableStartupPrompt = true
Compression = bzip
SolidCompression = yes
DirExistsWarning = no
DisableReadyMemo = true
DisableReadyPage = true
;;DisableDirPage = true
DisableProgramGroupPage = true
UsePreviousAppDir = no
UsePreviousGroup = no

%(ARCH)s

AppPublisher = Total Control Software
AppPublisherURL = http://wxPython.org/
AppSupportURL = http://wxPython.org/maillist.php
AppUpdatesURL = http://wxPython.org/download.php
AppVersion = %(VERSION)s

UninstallFilesDir = {app}\%(PKGDIR)s
LicenseFile = licence\licence.txt


;;------------------------------------------------------------

[Components]
Name: core;     Description: "wxPython modules and library";              Types: full custom;  Flags: fixed
Name: cairo;    Description: "Cairo runtime DLLs";                        Types: full
Name: pthfile;  Description: "Make this install be the default wxPython"; Types: full

;;------------------------------------------------------------

[Files]
%(RTDLL)s
Source: "%(WXDIR)s\lib\%(VCDLLDIR)s\wx*%(WXDLLVER)s_*.dll";  DestDir: "{app}\%(PKGDIR)s\wx"; Components: core; Flags: replacesameversion
%(GDIPLUS)s
%(CPPDLL)s
%(MSLU)s
Source: "%(CAIRO_ROOT)s\bin\*.dll";            DestDir: "{app}\%(PKGDIR)s\wx"; Components: cairo; Flags: replacesameversion


Source: "wx\_activex.pyd";                     DestDir: "{app}\%(PKGDIR)s\wx"; Components: core; Flags: comparetimestamp
Source: "wx\_calendar.pyd";                    DestDir: "{app}\%(PKGDIR)s\wx"; Components: core; Flags: comparetimestamp
Source: "wx\_combo.pyd";                       DestDir: "{app}\%(PKGDIR)s\wx"; Components: core; Flags: comparetimestamp
Source: "wx\_controls_.pyd";                   DestDir: "{app}\%(PKGDIR)s\wx"; Components: core; Flags: comparetimestamp
Source: "wx\_core_.pyd";                       DestDir: "{app}\%(PKGDIR)s\wx"; Components: core; Flags: comparetimestamp
Source: "wx\_gdi_.pyd";                        DestDir: "{app}\%(PKGDIR)s\wx"; Components: core; Flags: comparetimestamp
Source: "wx\_animate.pyd";                     DestDir: "{app}\%(PKGDIR)s\wx"; Components: core; Flags: comparetimestamp
Source: "wx\_gizmos.pyd";                      DestDir: "{app}\%(PKGDIR)s\wx"; Components: core; Flags: comparetimestamp
Source: "wx\_glcanvas.pyd";                    DestDir: "{app}\%(PKGDIR)s\wx"; Components: core; Flags: comparetimestamp
Source: "wx\_grid.pyd";                        DestDir: "{app}\%(PKGDIR)s\wx"; Components: core; Flags: comparetimestamp
Source: "wx\_html.pyd";                        DestDir: "{app}\%(PKGDIR)s\wx"; Components: core; Flags: comparetimestamp
Source: "wx\_html2.pyd";                       DestDir: "{app}\%(PKGDIR)s\wx"; Components: core; Flags: comparetimestamp
Source: "wx\_media.pyd";                       DestDir: "{app}\%(PKGDIR)s\wx"; Components: core; Flags: comparetimestamp
Source: "wx\_misc_.pyd";                       DestDir: "{app}\%(PKGDIR)s\wx"; Components: core; Flags: comparetimestamp
Source: "wx\_stc.pyd";                         DestDir: "{app}\%(PKGDIR)s\wx"; Components: core; Flags: comparetimestamp
Source: "wx\_webkit.pyd";                      DestDir: "{app}\%(PKGDIR)s\wx"; Components: core; Flags: comparetimestamp
Source: "wx\_windows_.pyd";                    DestDir: "{app}\%(PKGDIR)s\wx"; Components: core; Flags: comparetimestamp
Source: "wx\_wizard.pyd";                      DestDir: "{app}\%(PKGDIR)s\wx"; Components: core; Flags: comparetimestamp
Source: "wx\_xrc.pyd";                         DestDir: "{app}\%(PKGDIR)s\wx"; Components: core; Flags: comparetimestamp
Source: "wx\_aui.pyd";                         DestDir: "{app}\%(PKGDIR)s\wx"; Components: core; Flags: comparetimestamp
Source: "wx\_richtext.pyd";                    DestDir: "{app}\%(PKGDIR)s\wx"; Components: core; Flags: comparetimestamp
Source: "wx\_dataview.pyd";                    DestDir: "{app}\%(PKGDIR)s\wx"; Components: core; Flags: comparetimestamp
Source: "wx\_propgrid.pyd";                    DestDir: "{app}\%(PKGDIR)s\wx"; Components: core; Flags: comparetimestamp

Source: "wx\*.py";                              DestDir: "{app}\%(PKGDIR)s\wx"; Components: core
Source: "wx\build\*.py";                        DestDir: "{app}\%(PKGDIR)s\wx\build"; Components: core
Source: "wx\lib\*.py";                          DestDir: "{app}\%(PKGDIR)s\wx\lib"; Components: core
Source: "wx\lib\*.idl";                         DestDir: "{app}\%(PKGDIR)s\wx\lib"; Components: core
Source: "wx\lib\*.tlb";                         DestDir: "{app}\%(PKGDIR)s\wx\lib"; Components: core
Source: "wx\lib\agw\*.py";                      DestDir: "{app}\%(PKGDIR)s\wx\lib\agw"; Components: core
Source: "wx\lib\agw\aui\*.py";                  DestDir: "{app}\%(PKGDIR)s\wx\lib\agw\aui"; Components: core
Source: "wx\lib\agw\persist\*.py";              DestDir: "{app}\%(PKGDIR)s\wx\lib\agw\persist"; Components: core
Source: "wx\lib\agw\ribbon\*.py";               DestDir: "{app}\%(PKGDIR)s\wx\lib\agw\ribbon"; Components: core
Source: "wx\lib\agw\data\*.png";                DestDir: "{app}\%(PKGDIR)s\wx\lib\agw\data"; Components: core
Source: "wx\lib\agw\data\*.html";               DestDir: "{app}\%(PKGDIR)s\wx\lib\agw\data"; Components: core
Source: "wx\lib\analogclock\*.py";              DestDir: "{app}\%(PKGDIR)s\wx\lib\analogclock"; Components: core
Source: "wx\lib\analogclock\lib_setup\*.py";    DestDir: "{app}\%(PKGDIR)s\wx\lib\analogclock\lib_setup"; Components: core
Source: "wx\lib\art\*.py";                      DestDir: "{app}\%(PKGDIR)s\wx\lib\art"; Components: core
Source: "wx\lib\colourchooser\*.py";            DestDir: "{app}\%(PKGDIR)s\wx\lib\colourchooser"; Components: core
Source: "wx\lib\editor\*.py";                   DestDir: "{app}\%(PKGDIR)s\wx\lib\editor"; Components: core
Source: "wx\lib\editor\*.txt";                  DestDir: "{app}\%(PKGDIR)s\wx\lib\editor"; Components: core
Source: "wx\lib\mixins\*.py";                   DestDir: "{app}\%(PKGDIR)s\wx\lib\mixins"; Components: core
Source: "wx\lib\masked\*.py";                   DestDir: "{app}\%(PKGDIR)s\wx\lib\masked"; Components: core
Source: "wx\lib\ogl\*.py";                      DestDir: "{app}\%(PKGDIR)s\wx\lib\ogl"; Components: core
Source: "wx\lib\pdfviewer\*.py";                DestDir: "{app}\%(PKGDIR)s\wx\lib\pdfviewer"; Components: core
Source: "wx\lib\floatcanvas\*.py";              DestDir: "{app}\%(PKGDIR)s\wx\lib\floatcanvas"; Components: core
Source: "wx\lib\floatcanvas\Utilities\*.py";    DestDir: "{app}\%(PKGDIR)s\wx\lib\floatcanvas\Utilities"; Components: core
Source: "wx\lib\pubsub\*.py";                   DestDir: "{app}\%(PKGDIR)s\wx\lib\pubsub"; Components: core
Source: "wx\lib\pubsub\core\*.py";              DestDir: "{app}\%(PKGDIR)s\wx\lib\pubsub\core"; Components: core
Source: "wx\lib\pubsub\core\arg1\*.py";         DestDir: "{app}\%(PKGDIR)s\wx\lib\pubsub\core\arg1"; Components: core
Source: "wx\lib\pubsub\core\kwargs\*.py";       DestDir: "{app}\%(PKGDIR)s\wx\lib\pubsub\core\kwargs"; Components: core
Source: "wx\lib\pubsub\utils\*.py";             DestDir: "{app}\%(PKGDIR)s\wx\lib\pubsub\utils"; Components: core
Source: "wx\py\*.py";                           DestDir: "{app}\%(PKGDIR)s\wx\py"; Components: core
Source: "wx\py\*.txt";                          DestDir: "{app}\%(PKGDIR)s\wx\py"; Components: core
Source: "wx\py\*.ico";                          DestDir: "{app}\%(PKGDIR)s\wx\py"; Components: core
Source: "wx\py\*.png";                          DestDir: "{app}\%(PKGDIR)s\wx\py"; Components: core
Source: "wx\py\tests\*.py";                     DestDir: "{app}\%(PKGDIR)s\wx\py\tests"; Components: core
Source: "wx\tools\*.py";                        DestDir: "{app}\%(PKGDIR)s\wx\tools"; Components: core
Source: "wx\tools\XRCed\*.txt";                 DestDir: "{app}\%(PKGDIR)s\wx\tools\XRCed"; Components: core
Source: "wx\tools\XRCed\sawfishrc";             DestDir: "{app}\%(PKGDIR)s\wx\tools\XRCed"; Components: core
Source: "wx\tools\XRCed\*.py";                  DestDir: "{app}\%(PKGDIR)s\wx\tools\XRCed"; Components: core
Source: "wx\tools\XRCed\*.xrc";                 DestDir: "{app}\%(PKGDIR)s\wx\tools\XRCed"; Components: core
Source: "wx\tools\XRCed\*.ico";                 DestDir: "{app}\%(PKGDIR)s\wx\tools\XRCed"; Components: core
Source: "wx\tools\XRCed\*.png";                 DestDir: "{app}\%(PKGDIR)s\wx\tools\XRCed"; Components: core
Source: "wx\tools\XRCed\*.sh";                  DestDir: "{app}\%(PKGDIR)s\wx\tools\XRCed"; Components: core
Source: "wx\tools\XRCed\*.htb";                 DestDir: "{app}\%(PKGDIR)s\wx\tools\XRCed"; Components: core
Source: "wx\tools\XRCed\plugins\*.py";          DestDir: "{app}\%(PKGDIR)s\wx\tools\XRCed\plugins"; Components: core
Source: "wx\tools\XRCed\plugins\*.crx";         DestDir: "{app}\%(PKGDIR)s\wx\tools\XRCed\plugins"; Components: core
Source: "wx\tools\XRCed\plugins\bitmaps\*.png"; DestDir: "{app}\%(PKGDIR)s\wx\tools\XRCed\plugins\bitmaps"; Components: core

Source: "wx\tools\Editra\docs\*.txt";                        DestDir: "{app}\%(PKGDIR)s\wx\tools\Editra\docs"; Components: core

%(EDITRA_LOCALE)s

Source: "wx\tools\Editra\pixmaps\*.png";                     DestDir: "{app}\%(PKGDIR)s\wx\tools\Editra\pixmaps"; Components: core
Source: "wx\tools\Editra\pixmaps\*.ico";                     DestDir: "{app}\%(PKGDIR)s\wx\tools\Editra\pixmaps"; Components: core
Source: "wx\tools\Editra\pixmaps\*.icns";                    DestDir: "{app}\%(PKGDIR)s\wx\tools\Editra\pixmaps"; Components: core
Source: "wx\tools\Editra\pixmaps\theme\Default\README";      DestDir: "{app}\%(PKGDIR)s\wx\tools\Editra\pixmaps\theme\Default"; Components: core
Source: "wx\tools\Editra\pixmaps\theme\Tango\AUTHORS";       DestDir: "{app}\%(PKGDIR)s\wx\tools\Editra\pixmaps\theme\Tango"; Components: core
Source: "wx\tools\Editra\pixmaps\theme\Tango\COPYING";       DestDir: "{app}\%(PKGDIR)s\wx\tools\Editra\pixmaps\theme\Tango"; Components: core
Source: "wx\tools\Editra\pixmaps\theme\Tango\menu\*.png";    DestDir: "{app}\%(PKGDIR)s\wx\tools\Editra\pixmaps\theme\Tango\menu"; Components: core
Source: "wx\tools\Editra\pixmaps\theme\Tango\mime\*.png";    DestDir: "{app}\%(PKGDIR)s\wx\tools\Editra\pixmaps\theme\Tango\mime"; Components: core
Source: "wx\tools\Editra\pixmaps\theme\Tango\other\*.png";   DestDir: "{app}\%(PKGDIR)s\wx\tools\Editra\pixmaps\theme\Tango\other"; Components: core
Source: "wx\tools\Editra\pixmaps\theme\Tango\toolbar\*.png"; DestDir: "{app}\%(PKGDIR)s\wx\tools\Editra\pixmaps\theme\Tango\toolbar"; Components: core
Source: "wx\tools\Editra\plugins\*.egg";                     DestDir: "{app}\%(PKGDIR)s\wx\tools\Editra\plugins"; Components: core
Source: "wx\tools\Editra\src\*.py";                          DestDir: "{app}\%(PKGDIR)s\wx\tools\Editra\src"; Components: core
Source: "wx\tools\Editra\src\autocomp\*.py";                 DestDir: "{app}\%(PKGDIR)s\wx\tools\Editra\src\autocomp"; Components: core
Source: "wx\tools\Editra\src\ebmlib\*.py";                   DestDir: "{app}\%(PKGDIR)s\wx\tools\Editra\src\ebmlib"; Components: core
Source: "wx\tools\Editra\src\eclib\*.py";                    DestDir: "{app}\%(PKGDIR)s\wx\tools\Editra\src\eclib"; Components: core
Source: "wx\tools\Editra\src\extern\*.py";                   DestDir: "{app}\%(PKGDIR)s\wx\tools\Editra\src\extern"; Components: core
Source: "wx\tools\Editra\src\extern\README";                 DestDir: "{app}\%(PKGDIR)s\wx\tools\Editra\src\extern"; Components: core
Source: "wx\tools\Editra\src\extern\aui\*.py";               DestDir: "{app}\%(PKGDIR)s\wx\tools\Editra\src\extern\aui"; Components: core
Source: "wx\tools\Editra\src\extern\pygments\*.py";          DestDir: "{app}\%(PKGDIR)s\wx\tools\Editra\src\extern\pygments"; Components: core
Source: "wx\tools\Editra\src\extern\pygments\filters\*.py";    DestDir: "{app}\%(PKGDIR)s\wx\tools\Editra\src\extern\pygments\filters"; Components: core
Source: "wx\tools\Editra\src\extern\pygments\formatters\*.py"; DestDir: "{app}\%(PKGDIR)s\wx\tools\Editra\src\extern\pygments\formatters"; Components: core
Source: "wx\tools\Editra\src\extern\pygments\lexers\*.py";     DestDir: "{app}\%(PKGDIR)s\wx\tools\Editra\src\extern\pygments\lexers"; Components: core
Source: "wx\tools\Editra\src\extern\pygments\styles\*.py";     DestDir: "{app}\%(PKGDIR)s\wx\tools\Editra\src\extern\pygments\styles"; Components: core
Source: "wx\tools\Editra\src\syntax\*.py";                   DestDir: "{app}\%(PKGDIR)s\wx\tools\Editra\src\syntax"; Components: core
Source: "wx\tools\Editra\src\syntax\README";                 DestDir: "{app}\%(PKGDIR)s\wx\tools\Editra\src\syntax"; Components: core
Source: "wx\tools\Editra\styles\*.ess";                      DestDir: "{app}\%(PKGDIR)s\wx\tools\Editra\styles"; Components: core
Source: "wx\tools\Editra\tests\syntax\*.*";                  DestDir: "{app}\%(PKGDIR)s\wx\tools\Editra\tests\syntax"; Components: core
Source: "wx\tools\Editra\AUTHORS";                           DestDir: "{app}\%(PKGDIR)s\wx\tools\Editra"; Components: core
Source: "wx\tools\Editra\CHANGELOG";                         DestDir: "{app}\%(PKGDIR)s\wx\tools\Editra"; Components: core
Source: "wx\tools\Editra\COPYING";                           DestDir: "{app}\%(PKGDIR)s\wx\tools\Editra"; Components: core
Source: "wx\tools\Editra\NEWS";                              DestDir: "{app}\%(PKGDIR)s\wx\tools\Editra"; Components: core
Source: "wx\tools\Editra\README";                            DestDir: "{app}\%(PKGDIR)s\wx\tools\Editra"; Components: core
Source: "wx\tools\Editra\THANKS";                            DestDir: "{app}\%(PKGDIR)s\wx\tools\Editra"; Components: core
Source: "wx\tools\Editra\FAQ";                               DestDir: "{app}\%(PKGDIR)s\wx\tools\Editra"; Components: core
Source: "wx\tools\Editra\TODO";                              DestDir: "{app}\%(PKGDIR)s\wx\tools\Editra"; Components: core
Source: "wx\tools\Editra\__init__.py";                       DestDir: "{app}\%(PKGDIR)s\wx\tools\Editra"; Components: core
Source: "wx\tools\Editra\launcher.py";                       DestDir: "{app}\%(PKGDIR)s\wx\tools\Editra"; Components: core
Source: "wx\tools\Editra\Editra";                            DestDir: "{app}\%(PKGDIR)s\wx\tools\Editra"; Components: core

Source: "wxversion\wxversion.py";           DestDir: "{app}";  Flags: sharedfile;  Components: core
Source: "src\wx.pth";                       DestDir: "{app}";  Flags: sharedfile;  Components: pthfile

%(LOCALE)s


Source: "scripts\*.py";                     DestDir: "{code:GetPythonDir}\Scripts"; Flags: sharedfile;  Components: core
Source: "scripts\helpviewer";               DestDir: "{code:GetPythonDir}\Scripts"; Flags: sharedfile;  Components: core
Source: "scripts\img2png";                  DestDir: "{code:GetPythonDir}\Scripts"; Flags: sharedfile;  Components: core
Source: "scripts\img2py";                   DestDir: "{code:GetPythonDir}\Scripts"; Flags: sharedfile;  Components: core
Source: "scripts\img2xpm";                  DestDir: "{code:GetPythonDir}\Scripts"; Flags: sharedfile;  Components: core
Source: "scripts\pyalacarte";               DestDir: "{code:GetPythonDir}\Scripts"; Flags: sharedfile;  Components: core
Source: "scripts\pyalamode";                DestDir: "{code:GetPythonDir}\Scripts"; Flags: sharedfile;  Components: core
Source: "scripts\pyshell";                  DestDir: "{code:GetPythonDir}\Scripts"; Flags: sharedfile;  Components: core
Source: "scripts\pysliceshell";             DestDir: "{code:GetPythonDir}\Scripts"; Flags: sharedfile;  Components: core
Source: "scripts\pycrust";                  DestDir: "{code:GetPythonDir}\Scripts"; Flags: sharedfile;  Components: core
Source: "scripts\pyslices";                 DestDir: "{code:GetPythonDir}\Scripts"; Flags: sharedfile;  Components: core
Source: "scripts\pywrap";                   DestDir: "{code:GetPythonDir}\Scripts"; Flags: sharedfile;  Components: core
Source: "scripts\pywxrc";                   DestDir: "{code:GetPythonDir}\Scripts"; Flags: sharedfile;  Components: core
Source: "scripts\xrced";                    DestDir: "{code:GetPythonDir}\Scripts"; Flags: sharedfile;  Components: core
Source: "scripts\editra";                   DestDir: "{code:GetPythonDir}\Scripts"; Flags: sharedfile;  Components: core

Source: "distrib\README.win32.txt";         DestDir: "{app}\%(PKGDIR)s\docs";  Flags: isreadme; Components: core
Source: "licence\*.txt";                    DestDir: "{app}\%(PKGDIR)s\docs\licence"; Components: core
Source: "docs\CHANGES.*";                   DestDir: "{app}\%(PKGDIR)s\docs"; Components: core
Source: "docs\MigrationGuide.*";            DestDir: "{app}\%(PKGDIR)s\docs"; Components: core
Source: "docs\default.css";                 DestDir: "{app}\%(PKGDIR)s\docs"; Components: core



;;------------------------------------------------------------

[Run]
;; Compile the .py files
Filename: "{code:GetPythonDir}\python.exe";  Parameters: "{code:GetPythonDir}\Lib\compileall.py {app}\%(PKGDIR)s"; Description: "Compile Python .py files to .pyc"; Flags: postinstall; Components: core

;; Recreate the tool scripts to use the paths on the users machine
Filename: "{code:GetPythonDir}\python.exe";  Parameters: "CreateBatchFiles.py";  WorkingDir: "{code:GetPythonDir}\Scripts";  Description: "Create batch files for tool scripts"; Flags: postinstall; Components: core




;;------------------------------------------------------------

[UninstallDelete]
Type: files; Name: "{app}\%(PKGDIR)s\wx\*.pyc";
Type: files; Name: "{app}\%(PKGDIR)s\wx\*.pyo";
Type: files; Name: "{app}\%(PKGDIR)s\wx\*.pyd";
Type: files; Name: "{app}\%(PKGDIR)s\wx\build\*.pyc";
Type: files; Name: "{app}\%(PKGDIR)s\wx\build\*.pyo";
Type: files; Name: "{app}\%(PKGDIR)s\wx\lib\*.pyc";
Type: files; Name: "{app}\%(PKGDIR)s\wx\lib\*.pyo";
Type: files; Name: "{app}\%(PKGDIR)s\wx\lib\agw\*.pyc";
Type: files; Name: "{app}\%(PKGDIR)s\wx\lib\agw\*.pyo";
Type: files; Name: "{app}\%(PKGDIR)s\wx\lib\agw\aui\*.pyc";
Type: files; Name: "{app}\%(PKGDIR)s\wx\lib\agw\aui\*.pyo";
Type: files; Name: "{app}\%(PKGDIR)s\wx\lib\agw\persist\*.pyc";
Type: files; Name: "{app}\%(PKGDIR)s\wx\lib\agw\persist\*.pyo";
Type: files; Name: "{app}\%(PKGDIR)s\wx\lib\agw\ribbon\*.pyc";
Type: files; Name: "{app}\%(PKGDIR)s\wx\lib\agw\ribbon\*.pyo";
Type: files; Name: "{app}\%(PKGDIR)s\wx\lib\analogclock\*.pyc";
Type: files; Name: "{app}\%(PKGDIR)s\wx\lib\analogclock\*.pyo";
Type: files; Name: "{app}\%(PKGDIR)s\wx\lib\analogclock\lib_setup\*.pyc";
Type: files; Name: "{app}\%(PKGDIR)s\wx\lib\analogclock\lib_setup\*.pyo";
Type: files; Name: "{app}\%(PKGDIR)s\wx\lib\art\*.pyc";
Type: files; Name: "{app}\%(PKGDIR)s\wx\lib\art\*.pyo";
Type: files; Name: "{app}\%(PKGDIR)s\wx\lib\colourchooser\*.pyc";
Type: files; Name: "{app}\%(PKGDIR)s\wx\lib\colourchooser\*.pyo";
Type: files; Name: "{app}\%(PKGDIR)s\wx\lib\editor\*.pyc";
Type: files; Name: "{app}\%(PKGDIR)s\wx\lib\editor\*.pyo";
Type: files; Name: "{app}\%(PKGDIR)s\wx\lib\mixins\*.pyc";
Type: files; Name: "{app}\%(PKGDIR)s\wx\lib\mixins\*.pyo";
Type: files; Name: "{app}\%(PKGDIR)s\wx\lib\masked\*.pyc";
Type: files; Name: "{app}\%(PKGDIR)s\wx\lib\masked\*.pyo";
Type: files; Name: "{app}\%(PKGDIR)s\wx\lib\ogl\*.pyc";
Type: files; Name: "{app}\%(PKGDIR)s\wx\lib\ogl\*.pyo";
Type: files; Name: "{app}\%(PKGDIR)s\wx\lib\pdfviewer\*.pyc";
Type: files; Name: "{app}\%(PKGDIR)s\wx\lib\pdfviewer\*.pyo";

Type: files; Name: "{app}\%(PKGDIR)s\wx\lib\pubsub\*.pyc";
Type: files; Name: "{app}\%(PKGDIR)s\wx\lib\pubsub\*.pyo";
Type: files; Name: "{app}\%(PKGDIR)s\wx\lib\pubsub\core\*.pyc";
Type: files; Name: "{app}\%(PKGDIR)s\wx\lib\pubsub\core\*.pyo";
Type: files; Name: "{app}\%(PKGDIR)s\wx\lib\pubsub\core\arg1\*.pyc"
Type: files; Name: "{app}\%(PKGDIR)s\wx\lib\pubsub\core\arg1\*.pyo"
Type: files; Name: "{app}\%(PKGDIR)s\wx\lib\pubsub\core\kwargs\*.pyc";
Type: files; Name: "{app}\%(PKGDIR)s\wx\lib\pubsub\core\kwargs\*.pyo";
Type: files; Name: "{app}\%(PKGDIR)s\wx\lib\pubsub\utils\*.pyc";
Type: files; Name: "{app}\%(PKGDIR)s\wx\lib\pubsub\utils\*.pyo";

Type: files; Name: "{app}\%(PKGDIR)s\wx\lib\floatcanvas\*.pyc";
Type: files; Name: "{app}\%(PKGDIR)s\wx\lib\floatcanvas\*.pyo";
Type: files; Name: "{app}\%(PKGDIR)s\wx\lib\floatcanvas\Utilities\*.pyc";
Type: files; Name: "{app}\%(PKGDIR)s\wx\lib\floatcanvas\Utilities\*.pyo";

Type: files; Name: "{app}\%(PKGDIR)s\wx\py\*.pyc";
Type: files; Name: "{app}\%(PKGDIR)s\wx\py\*.pyo";
Type: files; Name: "{app}\%(PKGDIR)s\wx\py\tests\*.pyc";
Type: files; Name: "{app}\%(PKGDIR)s\wx\py\tests\*.pyo";
Type: files; Name: "{app}\%(PKGDIR)s\wx\tools\*.pyc";
Type: files; Name: "{app}\%(PKGDIR)s\wx\tools\*.pyo";
Type: files; Name: "{app}\%(PKGDIR)s\wx\tools\XRCed\*.pyc";
Type: files; Name: "{app}\%(PKGDIR)s\wx\tools\XRCed\*.pyo";
Type: files; Name: "{app}\%(PKGDIR)s\wx\tools\XRCed\plugins\*.pyc";
Type: files; Name: "{app}\%(PKGDIR)s\wx\tools\XRCed\plugins\*.pyo";

Type: files; Name: "{app}\%(PKGDIR)s\wx\tools\Editra\*.pyc";
Type: files; Name: "{app}\%(PKGDIR)s\wx\tools\Editra\*.pyo";
Type: files; Name: "{app}\%(PKGDIR)s\wx\tools\Editra\src\syntax\*.pyc";
Type: files; Name: "{app}\%(PKGDIR)s\wx\tools\Editra\src\syntax\*.pyo";
Type: files; Name: "{app}\%(PKGDIR)s\wx\tools\Editra\src\extern\*.pyc";
Type: files; Name: "{app}\%(PKGDIR)s\wx\tools\Editra\src\extern\*.pyo";
Type: files; Name: "{app}\%(PKGDIR)s\wx\tools\Editra\src\extern\aui\*.pyc";
Type: files; Name: "{app}\%(PKGDIR)s\wx\tools\Editra\src\extern\aui\*.pyo";
Type: files; Name: "{app}\%(PKGDIR)s\wx\tools\Editra\src\extern\pygments\*.pyc";      
Type: files; Name: "{app}\%(PKGDIR)s\wx\tools\Editra\src\extern\pygments\*.pyo";      
Type: files; Name: "{app}\%(PKGDIR)s\wx\tools\Editra\src\extern\pygments\filters\*.pyc"; 
Type: files; Name: "{app}\%(PKGDIR)s\wx\tools\Editra\src\extern\pygments\filters\*.pyo"; 
Type: files; Name: "{app}\%(PKGDIR)s\wx\tools\Editra\src\extern\pygments\formatters\*.pyc";
Type: files; Name: "{app}\%(PKGDIR)s\wx\tools\Editra\src\extern\pygments\formatters\*.pyo";
Type: files; Name: "{app}\%(PKGDIR)s\wx\tools\Editra\src\extern\pygments\lexers\*.pyc";    
Type: files; Name: "{app}\%(PKGDIR)s\wx\tools\Editra\src\extern\pygments\lexers\*.pyo";    
Type: files; Name: "{app}\%(PKGDIR)s\wx\tools\Editra\src\extern\pygments\styles\*.pyc";    
Type: files; Name: "{app}\%(PKGDIR)s\wx\tools\Editra\src\extern\pygments\styles\*.pyo";    

Type: files; Name: "{app}\%(PKGDIR)s\wx\tools\Editra\src\autocomp\*.pyc";
Type: files; Name: "{app}\%(PKGDIR)s\wx\tools\Editra\src\autocomp\*.pyo";
Type: files; Name: "{app}\%(PKGDIR)s\wx\tools\Editra\src\ebmlib\*.pyc";
Type: files; Name: "{app}\%(PKGDIR)s\wx\tools\Editra\src\ebmlib\*.pyo";
Type: files; Name: "{app}\%(PKGDIR)s\wx\tools\Editra\src\eclib\*.pyc";
Type: files; Name: "{app}\%(PKGDIR)s\wx\tools\Editra\src\eclib\*.pyo";
Type: files; Name: "{app}\%(PKGDIR)s\wx\tools\Editra\src\*.pyc";
Type: files; Name: "{app}\%(PKGDIR)s\wx\tools\Editra\src\*.pyo";

Type: files; Name: "{app}\wxversion.pyc";
Type: files; Name: "{app}\wxversion.pyo";


%(UNINSTALL_BATCH)s

''' + """
;----------------------------------------------------------------------

[Code]

program Setup;
var
    PythonDir  : String;
    InstallDir : String;


function InitializeSetup(): Boolean;
begin

    (* -------------------------------------------------------------- *)
    (* Figure out what to use as a default installation dir           *)

    if not RegQueryStringValue(HKEY_CURRENT_USER,
                               'Software\Python\PythonCore\%(PYTHONVER)s\InstallPath',
                               '', PythonDir) then begin

        if not RegQueryStringValue(HKEY_LOCAL_MACHINE,
                                   'Software\Python\PythonCore\%(PYTHONVER)s\InstallPath',
                                   '', PythonDir) then begin

            if not RegQueryStringValue(HKEY_CURRENT_USER,
                                       'Software\Wow6432Node\Python\PythonCore\%(PYTHONVER)s\InstallPath',
                                       '', PythonDir) then begin

                if not RegQueryStringValue(HKEY_LOCAL_MACHINE,
                                           'Software\Wow6432Node\Python\PythonCore\%(PYTHONVER)s\InstallPath',
                                           '', PythonDir) then begin

                    MsgBox('No installation of Python %(PYTHONVER)s found in registry.' + #13 +
                           'Be sure to enter a pathname that places wxPython on the PYTHONPATH',
                           mbConfirmation, MB_OK);
                    PythonDir := 'C:\Put a directory on PYTHONPATH here\';
                end;
            end;
        end;
    end;
    InstallDir := PythonDir;
    %(IF22)s

    Result := True;
end;



function GetPythonDir(Default: String): String;
begin
    Result := PythonDir;
end;



function GetInstallDir(Default: String): String;
begin
    Result := InstallDir;
end;



function UninstallOld(FileName: String): Boolean;
var
    ResultCode: Integer;
begin
    Result := False;
    if FileExists(FileName) then begin
        Result := True;
        ResultCode := MsgBox('A prior wxPython installation was found in this directory.  It' + #13 +
                             'is recommended that it be uninstalled first.' + #13#13 +
                             'Should I do it?',
                             mbConfirmation, MB_YESNO);
        if ResultCode = IDYES then begin
            Exec(FileName, '/SILENT', WizardDirValue(), SW_SHOWNORMAL, ewWaitUntilTerminated, ResultCode);

        end;
    end;
end;



function NextButtonClick(CurPage: Integer): Boolean;
begin
    Result := True;
    if CurPage <> wpSelectDir then Exit;
    if not UninstallOld(WizardDirValue() + '\wxPython\unins000.exe') then
        if not UninstallOld(WizardDirValue() + '\wx\unins000.exe') then
            UninstallOld(WizardDirValue() + '\%(PKGDIR)s\unins000.exe')
end;



function OnlyBeforeXP(): Boolean;
var
    Version: TWindowsVersion;
begin
    GetWindowsVersionEx(Version);
    Result := True;
    if (Version.Major > 5) or ((Version.Major = 5) and (Version.Minor >= 1)) then begin
        Result := False;
    end;
end;


begin
end.

"""

#----------------------------------------------------------------------

ISS_DocDemo_Template = r'''

[Setup]
AppName = wxPython%(SHORTVER)s-docs-demos
AppVerName = wxPython Docs and Demos %(VERSION)s
OutputBaseFilename = wxPython%(SHORTVER)s-win32-docs-demos-%(VERSION)s
AppCopyright = Copyright 2011 Total Control Software
DefaultDirName = {pf}\wxPython%(SHORTVER)s Docs and Demos
DefaultGroupName = wxPython%(SHORTVER)s Docs Demos and Tools
PrivilegesRequired = none
OutputDir = dist
WizardStyle = modern
DisableStartupPrompt = true
Compression = bzip
DirExistsWarning = no
DisableReadyMemo = true
DisableReadyPage = true
;;DisableDirPage = true
DisableProgramGroupPage = no
UsePreviousAppDir = no
UsePreviousGroup = no

AppPublisher = Total Control Software
AppPublisherURL = http://wxPython.org/
AppSupportURL = http://wxPython.org/maillist.php
AppUpdatesURL = http://wxPython.org/download.php
AppVersion = %(VERSION)s

UninstallDisplayIcon = {app}\demo\wxpdemo.ico
UninstallFilesDir = {app}
LicenseFile = licence\licence.txt

;; WizardDebug = yes


;;------------------------------------------------------------


[Files]
Source: "demo\demo.py";                     DestDir: "{app}\demo"; DestName: "demo.pyw";
Source: "demo\*.py";                        DestDir: "{app}\demo";
Source: "demo\*.xml";                       DestDir: "{app}\demo";
Source: "demo\*.txt";                       DestDir: "{app}\demo";
Source: "demo\*.ico";                       DestDir: "{app}\demo";

Source: "demo\agw\*.py";                    DestDir: "{app}\demo\agw";
Source: "demo\agw\bitmaps\*.png";           DestDir: "{app}\demo\agw\bitmaps";
Source: "demo\agw\bitmaps\*.ico";           DestDir: "{app}\demo\agw\bitmaps";
Source: "demo\agw\bitmaps\*.gif";           DestDir: "{app}\demo\agw\bitmaps";
Source: "demo\agw\data\*.xls";              DestDir: "{app}\demo\agw\data";

Source: "demo\bitmaps\*.bmp";               DestDir: "{app}\demo\bitmaps";
Source: "demo\bitmaps\*.gif";               DestDir: "{app}\demo\bitmaps";
Source: "demo\bitmaps\*.jpg";               DestDir: "{app}\demo\bitmaps";
Source: "demo\bitmaps\*.png";               DestDir: "{app}\demo\bitmaps";
Source: "demo\bitmaps\*.ico";               DestDir: "{app}\demo\bitmaps";

Source: "demo\bmp_source\*.gif";               DestDir: "{app}\demo\bmp_source";
Source: "demo\bmp_source\*.bmp";               DestDir: "{app}\demo\bmp_source";
Source: "demo\bmp_source\*.jpg";               DestDir: "{app}\demo\bmp_source";
Source: "demo\bmp_source\*.png";               DestDir: "{app}\demo\bmp_source";
Source: "demo\bmp_source\*.ico";               DestDir: "{app}\demo\bmp_source";

Source: "demo\data\*.htm";                  DestDir: "{app}\demo\data";
Source: "demo\data\*.html";                 DestDir: "{app}\demo\data";
Source: "demo\data\*.py";                   DestDir: "{app}\demo\data";
Source: "demo\data\*.png";                  DestDir: "{app}\demo\data";
Source: "demo\data\*.bmp";                  DestDir: "{app}\demo\data";
Source: "demo\data\*.dat";                  DestDir: "{app}\demo\data";
Source: "demo\data\*.txt";                  DestDir: "{app}\demo\data";
Source: "demo\data\*.wav";                  DestDir: "{app}\demo\data";
Source: "demo\data\*.wdr";                  DestDir: "{app}\demo\data";
Source: "demo\data\*.xrc";                  DestDir: "{app}\demo\data";
Source: "demo\data\*.swf";                  DestDir: "{app}\demo\data";
Source: "demo\data\*.mpg";                  DestDir: "{app}\demo\data";

Source: "demo\data\locale-src\*.po";            DestDir: "{app}\demo\data\locale-src";
Source: "demo\data\locale-src\install";         DestDir: "{app}\demo\data\locale-src";
Source: "demo\data\locale\af\LC_MESSAGES\*.mo"; DestDir: "{app}\demo\data\locale\af\LC_MESSAGES";
Source: "demo\data\locale\de\LC_MESSAGES\*.mo"; DestDir: "{app}\demo\data\locale\de\LC_MESSAGES";
Source: "demo\data\locale\es\LC_MESSAGES\*.mo"; DestDir: "{app}\demo\data\locale\es\LC_MESSAGES";
Source: "demo\data\locale\fr\LC_MESSAGES\*.mo"; DestDir: "{app}\demo\data\locale\fr\LC_MESSAGES";
Source: "demo\data\locale\it\LC_MESSAGES\*.mo"; DestDir: "{app}\demo\data\locale\it\LC_MESSAGES";

Source: "demo\snippets\*.py";                   DestDir: "{app}\demo\snippets";

;;Source: "demo\dllwidget\*.cpp";             DestDir: "{app}\demo\dllwidget";
;;Source: "demo\dllwidget\*.py";              DestDir: "{app}\demo\dllwidget";
;;Source: "demo\dllwidget\Makefile";          DestDir: "{app}\demo\dllwidget";
;;Source: "demo\dllwidget\makefile.*";        DestDir: "{app}\demo\dllwidget";

Source: "licence\*.txt";                    DestDir: "{app}\docs\licence";
Source: "%(WXDIR)s\docs\htmlhelp\wx.chm";   DestDir: "{app}\docs";
;;Source: "%(WXDIR)s\docs\htmlhelp\ogl.chm";  DestDir: "{app}\docs";
Source: "docs\README.txt";                  DestDir: "{app}\docs";  Flags: isreadme;
Source: "docs\*.txt";                       DestDir: "{app}\docs";
Source: "docs\*.css";                       DestDir: "{app}\docs";
Source: "docs\*.html";                      DestDir: "{app}\docs";
Source: "docs\*.conf";                      DestDir: "{app}\docs";
Source: "docs\screenshots\*.png";           DestDir: "{app}\docs\screenshots";


Source: "samples\doodle\*.py";              DestDir: "{app}\samples\doodle";
Source: "samples\doodle\*.txt";             DestDir: "{app}\samples\doodle";
Source: "samples\doodle\*.ico";             DestDir: "{app}\samples\doodle";
Source: "samples\doodle\*.icns";            DestDir: "{app}\samples\doodle";
Source: "samples\doodle\sample.ddl";        DestDir: "{app}\samples\doodle";

Source: "samples\docview\*.py";                DestDir: "{app}\samples\docview";
Source: "samples\pydocview\*.py";              DestDir: "{app}\samples\pydocview";
Source: "samples\pydocview\*.png";             DestDir: "{app}\samples\pydocview";
Source: "samples\pydocview\*.txt";             DestDir: "{app}\samples\pydocview";

Source: "samples\ide\*.py";                       DestDir: "{app}\samples\ide";
Source: "samples\ide\activegrid\*.py";            DestDir: "{app}\samples\ide\activegrid";
Source: "samples\ide\activegrid\tool\*.py";       DestDir: "{app}\samples\ide\activegrid\tool";
Source: "samples\ide\activegrid\tool\data\*.txt"; DestDir: "{app}\samples\ide\activegrid\tool\data";
Source: "samples\ide\activegrid\util\*.py";       DestDir: "{app}\samples\ide\activegrid\util";
Source: "samples\ide\activegrid\model\*.py";      DestDir: "{app}\samples\ide\activegrid\model";

Source: "samples\embedded\*.py";            DestDir: "{app}\samples\embedded";
Source: "samples\embedded\*.cpp";           DestDir: "{app}\samples\embedded";
Source: "samples\embedded\*.txt";           DestDir: "{app}\samples\embedded";
Source: "samples\embedded\*.vc";            DestDir: "{app}\samples\embedded";
Source: "samples\embedded\*.unx";           DestDir: "{app}\samples\embedded";
Source: "samples\embedded\*.ico";           DestDir: "{app}\samples\embedded";
Source: "samples\embedded\*.xpm";           DestDir: "{app}\samples\embedded";
Source: "samples\embedded\*.rc";            DestDir: "{app}\samples\embedded";

Source: "samples\frogedit\*.py";            DestDir: "{app}\samples\frogedit";

Source: "samples\hangman\*.py";             DestDir: "{app}\samples\hangman";

Source: "samples\mainloop\*.py";            DestDir: "{app}\samples\mainloop";

Source: "samples\pubsub\*.bat";            DestDir: "{app}\samples\pubsub";
Source: "samples\pubsub\*.py";            DestDir: "{app}\samples\pubsub";
Source: "samples\pubsub\advanced\*.txt";   DestDir: "{app}\samples\advanced";
Source: "samples\pubsub\advanced\*.py";    DestDir: "{app}\samples\advanced";
Source: "samples\pubsub\basic_arg1\*.txt";   DestDir: "{app}\samples\basic_arg1";
Source: "samples\pubsub\basic_arg1\*.py";    DestDir: "{app}\samples\basic_arg1";
Source: "samples\pubsub\basic_kwargs\*.txt";   DestDir: "{app}\samples\basic_kwargs";
Source: "samples\pubsub\basic_kwargs\*.py";    DestDir: "{app}\samples\basic_kwargs";

Source: "samples\pySketch\*.py";            DestDir: "{app}\samples\pySketch";
Source: "samples\pySketch\images\*.bmp";    DestDir: "{app}\samples\pySketch\images";

Source: "samples\simple\*.py";              DestDir: "{app}\samples\simple";

Source: "samples\StyleEditor\*.txt";        DestDir: "{app}\samples\StyleEditor";
Source: "samples\StyleEditor\*.py";         DestDir: "{app}\samples\StyleEditor";
Source: "samples\StyleEditor\*.cfg";        DestDir: "{app}\samples\StyleEditor";

Source: "samples\wxProject\*.txt";          DestDir: "{app}\samples\wxProject";
Source: "samples\wxProject\*.py";           DestDir: "{app}\samples\wxProject";

Source: "samples\wxPIA_book\*";                       DestDir: "{app}\wxPython\samples\wxPIA_book";
Source: "samples\wxPIA_book\Chapter-01\*";            DestDir: "{app}\wxPython\samples\wxPIA_book\Chapter-01";
Source: "samples\wxPIA_book\Chapter-02\*";            DestDir: "{app}\wxPython\samples\wxPIA_book\Chapter-02";
Source: "samples\wxPIA_book\Chapter-03\*";            DestDir: "{app}\wxPython\samples\wxPIA_book\Chapter-03";
Source: "samples\wxPIA_book\Chapter-04\*";            DestDir: "{app}\wxPython\samples\wxPIA_book\Chapter-04";
Source: "samples\wxPIA_book\Chapter-05\*";            DestDir: "{app}\wxPython\samples\wxPIA_book\Chapter-05";
Source: "samples\wxPIA_book\Chapter-06\*";            DestDir: "{app}\wxPython\samples\wxPIA_book\Chapter-06";
Source: "samples\wxPIA_book\Chapter-07\*";            DestDir: "{app}\wxPython\samples\wxPIA_book\Chapter-07";
Source: "samples\wxPIA_book\Chapter-08\*";            DestDir: "{app}\wxPython\samples\wxPIA_book\Chapter-08";
Source: "samples\wxPIA_book\Chapter-09\*";            DestDir: "{app}\wxPython\samples\wxPIA_book\Chapter-09";
Source: "samples\wxPIA_book\Chapter-10\*";            DestDir: "{app}\wxPython\samples\wxPIA_book\Chapter-10";
Source: "samples\wxPIA_book\Chapter-11\*";            DestDir: "{app}\wxPython\samples\wxPIA_book\Chapter-11";
Source: "samples\wxPIA_book\Chapter-12\*";            DestDir: "{app}\wxPython\samples\wxPIA_book\Chapter-12";
Source: "samples\wxPIA_book\Chapter-13\*";            DestDir: "{app}\wxPython\samples\wxPIA_book\Chapter-13";
Source: "samples\wxPIA_book\Chapter-14\*";            DestDir: "{app}\wxPython\samples\wxPIA_book\Chapter-14";
Source: "samples\wxPIA_book\Chapter-15\*";            DestDir: "{app}\wxPython\samples\wxPIA_book\Chapter-15";
Source: "samples\wxPIA_book\Chapter-16\*";            DestDir: "{app}\wxPython\samples\wxPIA_book\Chapter-16";
Source: "samples\wxPIA_book\Chapter-16\helpfiles\*";  DestDir: "{app}\wxPython\samples\wxPIA_book\Chapter-16\helpfiles";
Source: "samples\wxPIA_book\Chapter-17\*";            DestDir: "{app}\wxPython\samples\wxPIA_book\Chapter-17";
Source: "samples\wxPIA_book\Chapter-18\*";            DestDir: "{app}\wxPython\samples\wxPIA_book\Chapter-18";


Source: "scripts\pyshell";                      DestDir: "{app}\scripts"; DestName: "pyshell.pyw";
Source: "scripts\pysliceshell";                 DestDir: "{app}\scripts"; DestName: "pysliceshell.pyw";
Source: "scripts\pycrust";                      DestDir: "{app}\scripts"; DestName: "pycrust.pyw";
Source: "scripts\pyslices";                     DestDir: "{app}\scripts"; DestName: "pyslices.pyw";
Source: "scripts\xrced";                        DestDir: "{app}\scripts"; DestName: "xrced.pyw";
Source: "scripts\editra";                       DestDir: "{app}\scripts"; DestName: "editra.pyw";
Source: "scripts\pyalamode";                    DestDir: "{app}\scripts"; DestName: "pyalamode.pyw";
Source: "scripts\pyalacarte";                   DestDir: "{app}\scripts"; DestName: "pyalacarte.pyw";

Source: "wx\py\PyCrust.ico";                    DestDir: "{app}\scripts";
Source: "wx\py\PySlices.ico";                    DestDir: "{app}\scripts";
Source: "wx\tools\XRCed\xrced.ico";             DestDir: "{app}\scripts";
Source: "wx\tools\Editra\pixmaps\editra.ico";   DestDir: "{app}\scripts";



;;------------------------------------------------------------

[Icons]
Name: "{group}\Run the wxPython DEMO"; Filename: "{app}\demo\demo.pyw";           WorkingDir: "{app}\demo";   IconFilename: "{app}\demo\wxpdemo.ico";
Name: "{group}\PyCrust";               Filename: "{app}\scripts\pycrust.pyw";     WorkingDir: "c:\";          IconFilename: "{app}\scripts\PyCrust.ico";
Name: "{group}\PySlices";              Filename: "{app}\scripts\pyslices.pyw";    WorkingDir: "c:\";          IconFilename: "{app}\scripts\PySlices.ico";
Name: "{group}\PyShell";               Filename: "{app}\scripts\pyshell.pyw";     WorkingDir: "c:\";          IconFilename: "{app}\scripts\PyCrust.ico";
Name: "{group}\PySlicesShell";         Filename: "{app}\scripts\pysliceshell.pyw";WorkingDir: "c:\";          IconFilename: "{app}\scripts\PySlices.ico";
Name: "{group}\XRC Resource Editor";   Filename: "{app}\scripts\xrced.pyw";       WorkingDir: "c:\";          IconFilename: "{app}\scripts\xrced.ico";
Name: "{group}\Editra";                Filename: "{app}\scripts\editra.pyw";      WorkingDir: "c:\";          IconFilename: "{app}\scripts\editra.ico";

;;Name: "{group}\PyAlaMode";             Filename: "{app}\scripts\pyalamode.pyw";   WorkingDir: "c:\";          IconFilename: "{app}\scripts\PyCrust.ico";
;;Name: "{group}\PyAlaCarte";            Filename: "{app}\scripts\pyalacarte.pyw";  WorkingDir: "c:\";          IconFilename: "{app}\scripts\PyCrust.ico";

Name: "{group}\Sample Apps";           Filename: "{app}\samples";

Name: "{group}\wxWidgets Reference";   Filename: "{app}\docs\wx.chm";
Name: "{group}\Migration Guide";       Filename: "{app}\docs\MigrationGuide.html";
Name: "{group}\Recent Changes";        Filename: "{app}\docs\CHANGES.html";
Name: "{group}\Other Docs";            Filename: "{app}\docs";

Name: "{group}\Uninstall wxPython Docs and Demos";  Filename: "{uninstallexe}";




;;------------------------------------------------------------

[UninstallDelete]
Type: files; Name: "{app}\demo\*.pyc";
Type: files; Name: "{app}\demo\*.pyo";
Type: files; Name: "{app}\demo\data\showTips";
Type: files; Name: "{app}\demo\data\*.pyc";
Type: files; Name: "{app}\demo\data\*.pyo";
Type: files; Name: "{app}\demo\dllwidget\*.pyc";
Type: files; Name: "{app}\demo\dllwidget\*.pyo";

Type: files; Name: "{app}\samples\doodle\*.pyc";
Type: files; Name: "{app}\samples\doodle\*.pyo";
Type: files; Name: "{app}\samples\embedded\*.pyc";
Type: files; Name: "{app}\samples\embedded\*.pyo";
Type: files; Name: "{app}\samples\frogedit\*.pyc";
Type: files; Name: "{app}\samples\frogedit\*.pyo";
Type: files; Name: "{app}\samples\hangman\*.pyc";
Type: files; Name: "{app}\samples\hangman\*.pyo";
Type: files; Name: "{app}\samples\hangman\*.txt";
Type: files; Name: "{app}\samples\mainloop\*.pyc";
Type: files; Name: "{app}\samples\mainloop\*.pyo";
Type: files; Name: "{app}\samples\pubsub\advanced\*.pyc";
Type: files; Name: "{app}\samples\pubsub\advanced\*.pyo"; 
Type: files; Name: "{app}\samples\pubsub\basic_arg1\*.pyc";
Type: files; Name: "{app}\samples\pubsub\basic_arg1\*.pyo"; 
Type: files; Name: "{app}\samples\pubsub\basic_kwargs\*.pyc";
Type: files; Name: "{app}\samples\pubsub\basic_kwargs\*.pyo"; 
Type: files; Name: "{app}\samples\pubsub\*.pyc";   
Type: files; Name: "{app}\samples\pubsub\*.pyo";    
Type: files; Name: "{app}\samples\pySketch\*.pyc";
Type: files; Name: "{app}\samples\pySketch\*.pyo";
Type: files; Name: "{app}\samples\simple\*.pyc";
Type: files; Name: "{app}\samples\simple\*.pyo";
Type: files; Name: "{app}\samples\StyleEditor\*.pyc";
Type: files; Name: "{app}\samples\StyleEditor\*.pyo";
Type: files; Name: "{app}\samples\wx_examples\basic\*.pyc";
Type: files; Name: "{app}\samples\wx_examples\basic\*.pyo";
Type: files; Name: "{app}\samples\wx_examples\hello\*.pyc";
Type: files; Name: "{app}\samples\wx_examples\hello\*.pyo";
Type: files; Name: "{app}\samples\wxProject\*.pyc";
Type: files; Name: "{app}\samples\wxProject\*.pyo";

Type: files; Name: "{app}\samples\ide\*.pyc";
Type: files; Name: "{app}\samples\ide\activegrid\*.pyc";
Type: files; Name: "{app}\samples\ide\activegrid\tool\*.pyc";
Type: files; Name: "{app}\samples\ide\activegrid\util\*.pyc";
Type: files; Name: "{app}\samples\ide\activegrid\model\*.pyc";
Type: files; Name: "{app}\samples\ide\*.pyo";
Type: files; Name: "{app}\samples\ide\activegrid\*.pyo";
Type: files; Name: "{app}\samples\ide\activegrid\tool\*.pyo";
Type: files; Name: "{app}\samples\ide\activegrid\util\*.pyo";
Type: files; Name: "{app}\samples\ide\activegrid\model\*.pyo";

Type: files; Name: "{app}\samples\docview\*.pyc";
Type: files; Name: "{app}\samples\pydocview\*.pyc";
Type: files; Name: "{app}\samples\docview\*.pyo";
Type: files; Name: "{app}\samples\pydocview\*.pyo";

Type: files; Name: "{app}\samples\wxPIA_book\*";
Type: files; Name: "{app}\samples\wxPIA_book\Chapter-01\*";
Type: files; Name: "{app}\samples\wxPIA_book\Chapter-02\*";
Type: files; Name: "{app}\samples\wxPIA_book\Chapter-03\*";
Type: files; Name: "{app}\samples\wxPIA_book\Chapter-04\*";
Type: files; Name: "{app}\samples\wxPIA_book\Chapter-05\*";
Type: files; Name: "{app}\samples\wxPIA_book\Chapter-06\*";
Type: files; Name: "{app}\samples\wxPIA_book\Chapter-07\*";
Type: files; Name: "{app}\samples\wxPIA_book\Chapter-08\*";
Type: files; Name: "{app}\samples\wxPIA_book\Chapter-09\*";
Type: files; Name: "{app}\samples\wxPIA_book\Chapter-10\*";
Type: files; Name: "{app}\samples\wxPIA_book\Chapter-11\*";
Type: files; Name: "{app}\samples\wxPIA_book\Chapter-12\*";
Type: files; Name: "{app}\samples\wxPIA_book\Chapter-13\*";
Type: files; Name: "{app}\samples\wxPIA_book\Chapter-14\*";
Type: files; Name: "{app}\samples\wxPIA_book\Chapter-15\*";
Type: files; Name: "{app}\samples\wxPIA_book\Chapter-16\*";
Type: files; Name: "{app}\samples\wxPIA_book\Chapter-16\helpfiles\*";
Type: files; Name: "{app}\samples\wxPIA_book\Chapter-17\*";
Type: files; Name: "{app}\samples\wxPIA_book\Chapter-18\*";


'''

#----------------------------------------------------------------------

def find_DLLs():

    if os.environ.get('CPU', '') in ['AMD64', 'X64']:
        # Just hard-code it for now until a good solution for finding
        # the right dumpbin can be found...
        return '30u', sys.version[:3]
        
    WXDLLVER = PYTHONVER = None

    proc = os.popen(r"dumpbin /imports wx\_core_.pyd", "r")
    lines = proc.readlines()
    proc.close()
    for line in lines:
        if line.startswith("    wxmsw"):
            WXDLLVER = line[9:14].split('_')[0]

        if line.startswith("    python"):
            PYTHONVER = line[10] + '.' + line[11]

    return WXDLLVER, PYTHONVER


#----------------------------------------------------------------------

locale_template = 'Source: "%s";  DestDir: "{app}\%s\%s"; Components: core'

def build_locale_string(pkgdir):
    stringlst = []

    def walk_helper(lst, dirname, files):
        for f in files:
            filename = os.path.join(dirname, f)
            if not os.path.isdir(filename):
                lst.append( locale_template % (filename, pkgdir, dirname) )

    os.path.walk('wx\\locale', walk_helper, stringlst)
    return '\n'.join(stringlst)


def build_editra_locale(pkgdir):
    template = r'Source: "%(lang)s\LC_MESSAGES\Editra.mo";  DestDir: "{app}\%(PKGDIR)s\%(lang)s\LC_MESSAGES"; Components: core'

    stringlist = list()
    for lang in glob.glob(r'wx\tools\Editra\locale\*'):
        stringlist.append(template % dict(lang=lang, PKGDIR=pkgdir))

    return '\n'.join(stringlist)
 

def get_system_dir():
    for p in [r"C:\WINNT\SYSTEM32",
              r"C:\WINDOWS\SYSTEM32",
              ]:
        if os.path.exists(p):
            return p
    raise IOError, "System dir not found"


def get_batch_files():
    globs = {}
    execfile("scripts/CreateBatchFiles.py", globs)
    scripts = globs["scripts"]
    scripts = ['Type: files; Name: "{code:GetPythonDir}\Scripts\%s.bat";' % i[0] for i in scripts]
    return '\n'.join(scripts)



runtime_template1 = 'Source: "%(name)s"; DestDir: "{code:GetPythonDir}"; Flags: uninsneveruninstall; Components: core'
runtime_template2 = 'Source: "%(name)s"; DestDir: "{app}\%(PKGDIR)s\wx"; Components: core; Flags: replacesameversion'

def get_runtime_dlls(PYVER, PKGDIR):
    if PYVER >= 'py26':
        # Since Python 2.6+ uses MSVC 9 then the SxS assemblies
        # for the CRT will already be installed, so we can not
        # bother with installing it ourselves.
        return ('', '')
        
    if os.environ.get('CPU', '') in ['AMD64', 'X64']:
        if PYVER == 'py25':
            # For now just pull the DLLs from the system dir, and install
            # them there.  We may eventually want to get more customized
            # like on win32.
            return (
                r'Source: "{sys}\MSVCRT.DLL"; DestDir: "{sys}"; Flags: 64bit uninsneveruninstall external; Components: core',
                r'Source: "{sys}\MSVCP60.DLL"; DestDir: "{sys}"; Flags: 64bit uninsneveruninstall external; Components: core',
                )
    else:
        if PYVER >= "py24":
            return ( runtime_template1 % dict(name=r"distrib\msw\msvcr71.dll", PKGDIR=PKGDIR),
                     runtime_template2 % dict(name=r"distrib\msw\msvcp71.dll", PKGDIR=PKGDIR) )
        else:
            return (  runtime_template1 % dict(name=r"distrib\msw\MSVCRT.dll", PKGDIR=PKGDIR),
                      runtime_template2 % dict(name=r"distrib\msw\MSVCIRT.dll", PKGDIR=PKGDIR) + "\n" +
                      runtime_template2 % dict(name=r"distrib\msw\MSVCP60.dll", PKGDIR=PKGDIR) )


#----------------------------------------------------------------------

def main():

    verglob = {}
    execfile("wx/__version__.py", verglob)

    VERSION    = verglob["VERSION_STRING"]
    SHORTVER   = VERSION[:3]

    WXDLLVER, PYTHONVER = find_DLLs()

    PYVER           = "py" + PYTHONVER[0] + PYTHONVER[2]
    WXDIR           = os.environ["WXWIN"]
    WXPYDIR         = os.path.join(WXDIR, "wxPython")
    SYSDIR          = get_system_dir()
    ISSFILE         = "__wxPython.iss"
    ISSDEMOFILE     = "__wxPythonDemo.iss"
    UNINSTALL_BATCH = get_batch_files()
    PKGDIR          = open('src/wx.pth').read().strip()
    LOCALE          = build_locale_string(PKGDIR)
    EDITRA_LOCALE   = build_editra_locale(PKGDIR)
    RTDLL,CPPDLL    = get_runtime_dlls(PYVER, PKGDIR)
    CAIRO_ROOT      = os.environ["CAIRO_ROOT"]

    if os.environ.get('CPU', '') in ['AMD64', 'X64']:
        BITS        = '64'
        VCDLLDIR    = 'vc90_x64_dll'
        GDIPLUS     = ''
        ARCH        = 'ArchitecturesInstallIn64BitMode = x64\nArchitecturesAllowed = x64'
        PRIV        = 'admin'

    else:
        BITS        = '32'
        VCDLLDIR    = 'vc90_dll'
        GDIPLUS     = 'Source: "distrib\msw\gdiplus.dll"; DestDir: "{app}\%(PKGDIR)s\wx"; Components: core; Flags: replacesameversion' % vars()
        ARCH        = ''
        PRIV        = 'none'

        
    print """
Building Win32 installer for wxPython:
    VERSION    = %(VERSION)s
    SHORTVER   = %(SHORTVER)s
    WXDLLVER   = %(WXDLLVER)s
    PYTHONVER  = %(PYTHONVER)s
    PYVER      = %(PYVER)s
    PKGDIR     = %(PKGDIR)s
    WXDIR      = %(WXDIR)s
    WXPYDIR    = %(WXPYDIR)s
    SYSDIR     = %(SYSDIR)s
    CAIRO_ROOT = %(CAIRO_ROOT)s
    """ % vars()

    if PYTHONVER >= "2.2":
        IF22 = r"InstallDir := InstallDir + '\Lib\site-packages';"
    else:
        IF22 = ""

    MSLU=''

    f = open(ISSFILE, "w")
    f.write(ISS_Template % vars())
    f.close()

    f = open(ISSDEMOFILE, "w")
    f.write(ISS_DocDemo_Template % vars())
    f.close()

    TOOLS = os.environ['TOOLS']
    if TOOLS.startswith('/cygdrive'):
        TOOLS = r"c:\TOOLS"  # temporary hack until I convert everything over to bash

    os.system(ISCC % (TOOLS, ISSFILE))
    time.sleep(1)
    os.system(ISCC % (TOOLS, ISSDEMOFILE))

    if not KEEP_TEMPS:
        time.sleep(1)
        os.remove(ISSFILE)
        os.remove(ISSDEMOFILE)


#----------------------------------------------------------------------

if __name__ == "__main__":
    main()



#----------------------------------------------------------------------


