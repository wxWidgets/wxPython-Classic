#########################################################################
""" wingdbstub.py    -- Debug stub for debuggifying Python programs

Copyright (c) 1999-2001, Archaeopteryx Software, Inc.  All rights reserved.

Written by Stephan R.A. Deibel and John P. Ehresman

Usage:
-----

This is the file that Wing DB users copy into their python project 
directory if they want to be able to debug programs that are launched
outside of the IDE (e.g., CGI scripts, in response to a browser page
load).

To use this, edit the configuration values below to match your 
Wing IDE installation and requirements of your project.

Then, add the following line to your code:

  import wingdbstub

Debugging will start immediately after this import statements.

Next make sure that your IDE is running and that it's configured to accept
connections from the host the debug program will be running on.

Now, invoking your python file should run the code within the debugger.
Note, however, that Wing will not stop in the code unless a breakpoint
is set.

If the debug process is started before the IDE, or is not listening
at the time this module is imported then the program will run with
debugging until an attach request is seen.  Attaching only works 
if the .wingdebugpw file is present; see the manual for details.

One win32, you either need to edit WINGHOME in this script or
pass in an environment variable called WINGHOME that points to
the Wing IDE installation directory.

"""
#########################################################################

import sys
import os
import imp


#------------------------------------------------------------------------
# Default configuration values:  Note that the named environment 
# variables, if set, will override these settings.

# Set this to 1 to disable all debugging; 0 to enable debugging
# (WINGDB_DISABLED environment variable)
kWingDebugDisabled = 0

# Host:port of the IDE within which to debug: As configured in the IDE
# with the Server Port preference
# (WINGDB_HOSTPORT environment variable)
kWingHostPort = 'localhost:50005'

# Port on which to listen for connection requests, so that the
# IDE can (re)attach to the debug process after it has started
# This is only used when the debug process is not attached to
# an IDE or the IDE has dropped its connection. The configured
# port can optionally be added to the IDE's Common Attach Hosts
# preference. Note that a random port is used instead if this 
# port is already in use!
# (WINGDB_ATTACHPORT environment variable)
kAttachPort = '50015'

# Set this to a filename to log verbose information about the debugger
# internals to a file.  If the file does not exist, it will be created
# as long as its enclosing directory exists and is writeable.  Use 
# "<stderr>" or "<stdout>".  Note that "<stderr>" may cause problems 
# on win32 if the debug process is not running in a console.
# (WINGDB_LOGFILE environment variable)
kLogFile = None

# Set to get a tremendous amount of logging from the debugger internals
# (WINGDB_LOGVERYVERBOSE)
kLogVeryVerbose = 0

# Set this to 1 when debugging embedded scripts in an environment that
# creates and reuses a Python instance across multiple script invocations:  
# It turns off automatic detection of program quit so that the debug session
# can span multiple script invocations.  When this is turned on, you may
# need to call ProgramQuit() on the debugger object to shut down the
# debugger cleanly when your application exits or discards the Python
# instance.  If multiple Python instances are created in the same run,
# only the first one will be able to debug unless it terminates debug
# and the environment variable WINGDB_ACTIVE is unset before importing
# this module in the second or later Python instance.  See the Wing
# IDE manual for details.
kEmbedded = 0

# Path to search for the debug password file and the name of the file
# to use.  The password file contains the encryption type and connect 
# password for all connections to the IDE and must match the wingdebugpw
# file in the profile dir used by the IDE.  Any entry of '$<winguserprofile>' 
# is replaced by the wing user profile directory for the user that the 
# current process is running as
# (WINGDB_PWFILEPATH environment variable)
kPWFilePath = [os.path.dirname(__file__), '$<winguserprofile>']
kPWFileName = 'wingdebugpw'

# Whether to exit if the debugger fails to run or to connect with an IDE
# for whatever reason
kExitOnFailure = 0

#------------------------------------------------------------------------
# Find Wing debugger installation location

# Edit this to point to your Wing installation or set to None to use env WINGHOME
# On OS X this must be set to name of the Wing IDE application bundle
# (for example, /Applications/WingIDE.app)
WINGHOME="/usr/lib/wingide5"

if sys.hexversion >= 0x03000000:
  def has_key(o, key):
    return key in o
else:
  def has_key(o, key):
    return o.has_key(key)
    
# Check environment:  Must have WINGHOME defined if still == None
if WINGHOME == None:
  if has_key(os.environ, 'WINGHOME'):
    WINGHOME=os.environ['WINGHOME']
  else:
    sys.stdout.write("*******************************************************************\n")
    sys.stdout.write("Error: Could not find Wing installation!  You must set WINGHOME or edit\n")
    sys.stdout.write("wingdbstub.py where indicated to point it to the location where\n")
    sys.stdout.write("Wing IDE is installed.\n")
    sys.exit(1)

# The user settings dir where per-user settings & patches are located.  Will be
# set from environment if left as None
kUserSettingsDir = None
if kUserSettingsDir is None:
  kUserSettingsDir = os.environ.get('WINGDB_USERSETTINGS')
  
def _FindActualWingHome(winghome):
  """ Find the actual directory to use for winghome.  Needed on OS X
  where the .app directory is the preferred dir to use for WINGHOME and
  .app/Contents/MacOS is accepted for backward compatibility. """
  
  if sys.platform != 'darwin':
    return winghome
  
  app_dir = None
  if os.path.isdir(winghome):
    if winghome.endswith('/'):
      wo_slash = winghome[:-1]
    else:
      wo_slash = winghome
      
    if wo_slash.endswith('.app'):
      app_dir = wo_slash
    elif wo_slash.endswith('.app/Contents/MacOS'):
      app_dir = wo_slash[:-len('/Contents/MacOS')]
    
  if app_dir and os.path.isdir(os.path.join(app_dir, 'Contents', 'Resources')):
    return os.path.join(app_dir, 'Contents', 'Resources')
  
  return winghome
  
def _ImportWingdb(winghome, user_settings=None):
  """ Find & import wingdb module. """
  
  try:
    exec_dict = {}
    execfile(os.path.join(winghome, 'bin', '_patchsupport.py'), exec_dict)
    find_matching = exec_dict['FindMatching']
    dir_list = find_matching('bin', winghome, user_settings)
  except Exception:
    dir_list = []
  dir_list.extend([os.path.join(winghome, 'bin'), os.path.join(winghome, 'src')])
  for path in dir_list:
    try:
      f, p, d = imp.find_module('wingdb', [path])
      try:
        return imp.load_module('wingdb', f, p, d)
      finally:
        if f is not None:
          f.close()
      break
    except ImportError:
      pass

#------------------------------------------------------------------------
# Set debugger if it hasn't been set -- this is to handle module reloading
# In the reload case, the debugger variable will be set to something
try:
  debugger
except NameError:
  debugger = None

# Start debugging if not disabled and this module has never been imported
# before
if (not kWingDebugDisabled and debugger is None
    and not has_key(os.environ, 'WINGDB_DISABLED') and 
    not has_key(os.environ, 'WINGDB_ACTIVE')):

  exit_on_fail = 0
  
  try:
    # Obtain exit if fails value
    exit_on_fail = os.environ.get('WINGDB_EXITONFAILURE', kExitOnFailure)
    
    # Obtain configuration for log file to use, if any
    logfile = os.environ.get('WINGDB_LOGFILE', kLogFile)
    if logfile == '-' or logfile == None or len(logfile.strip()) == 0:
      logfile = None

    very_verbose_log = os.environ.get('WINGDB_LOGVERYVERBOSE', kLogVeryVerbose)
    if type(very_verbose_log) == type('') and very_verbose_log.strip() == '':
      very_verbose_log = 0
      
    # Determine remote host/port where the IDE is running
    hostport = os.environ.get('WINGDB_HOSTPORT', kWingHostPort)
    colonpos = hostport.find(':')
    host = hostport[:colonpos]
    port = int(hostport[colonpos+1:])
  
    # Determine port to listen on locally for attach requests
    attachport = int(os.environ.get('WINGDB_ATTACHPORT', kAttachPort))
  
    # Check if running embedded script
    embedded = int(os.environ.get('WINGDB_EMBEDDED', kEmbedded))
  
    # Obtain debug password file search path
    if has_key(os.environ, 'WINGDB_PWFILEPATH'):
      pwfile_path = os.environ['WINGDB_PWFILEPATH'].split(os.pathsep)
    else:
      pwfile_path = kPWFilePath
    
    # Obtain debug password file name
    if has_key(os.environ, 'WINGDB_PWFILENAME'):
      pwfile_name = os.environ['WINGDB_PWFILENAME']
    else:
      pwfile_name = kPWFileName
    
    # Load wingdb.py
    actual_winghome = _FindActualWingHome(WINGHOME)
    wingdb = _ImportWingdb(actual_winghome, kUserSettingsDir)
    if wingdb == None:
      sys.stdout.write("*******************************************************************\n")
      sys.stdout.write("Error: Cannot find wingdb.py in $(WINGHOME)/bin or $(WINGHOME)/src\n")
      sys.stdout.write("Error: Please check the WINGHOME definition in wingdbstub.py\n")
      sys.exit(2)
    
    # Find the netserver module and create an error stream
    netserver = wingdb.FindNetServerModule(actual_winghome, kUserSettingsDir)
    err = wingdb.CreateErrStream(netserver, logfile, very_verbose_log)
    
    # Start debugging
    debugger = netserver.CNetworkServer(host, port, attachport, err, 
                                        pwfile_path=pwfile_path,
                                        pwfile_name=pwfile_name,
                                        autoquit=not embedded)
    debugger.StartDebug(stophere=0)
    os.environ['WINGDB_ACTIVE'] = "1"
    if debugger.ChannelClosed():
      raise ValueError('Not connected')
    
  except:
    if exit_on_fail:
      raise
    else:
      pass

def Ensure(require_connection=1, require_debugger=1):
  """ Ensure the debugger is started and attempt to connect to the IDE if
  not already connected.  Will raise a ValueError if:
  
  * the require_connection arg is true and the debugger is unable to connect
  * the require_debugger arg is true and the debugger cannot be loaded
  
  If SuspendDebug() has been called through the low-level API, calling
  Ensure() resets the suspend count to zero and additional calls to
  ResumeDebug() will be ignored until SuspendDebug() is called again.
  
  """
  
  if debugger is None:
    if require_debugger:
      raise ValueError("No debugger")
    return
  
  resumed = debugger.ResumeDebug()
  while resumed > 0:
    resumed = debugger.ResumeDebug()
  
  if not debugger.DebugActive():
    debugger.StartDebug()
  elif debugger.ChannelClosed():
    debugger.ConnectToClient()
    
  if require_connection and debugger.ChannelClosed():
    raise ValueError('Not connected')
    