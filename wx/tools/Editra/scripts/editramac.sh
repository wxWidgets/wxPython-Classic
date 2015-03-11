#!/bin/bash
# ----------------------------------------------------------------------
# Start up the Editra application bundle, passing along any
# command-line args.  (Mac OS X only)
# ----------------------------------------------------------------------

#set -o xtrace

if [ "$1" = "-c" ]; then
   # Use AppleScript to load the file(s) into a currently running Editra
   shift
   for f in "$@"; do 
	ABSPATH=`readlink -f $f`
	osascript -e "tell app \"Editra\" to open (POSIX file \"$ABSPATH\")"
   done
   exit 0
fi


# Otherwise, start a new instance of Editra, passing the files on the command
# line. First find the app bundle.
if [ -z "$EDITRA_APP_DIR" ]; then
   myDir=`dirname "$0"`
   for i in ~/Applications $myDir $myDir/dist /Applications /Applications/MyApps/Editors; do
	if [ -x "$i/Editra.app" ]; then
	    EDITRA_APP_DIR="$i"
	    break
	fi
   done
fi
if [ -z "$EDITRA_APP_DIR" ];then
   echo "Sorry, cannot find Edita.app.  Try setting the EDITRA_APP_DIR"
   echo "environment variable to the folder containing Editra.app."
	exit 1
fi
binary="$EDITRA_APP_DIR/Editra.app/Contents/MacOS/Editra"

# Use readlink to ensure that we have absolute pathnames for each arg,
# adding each result to an array
declare -a A
for f in ${1:+"$@"}; do 
   A=( "${A[@]}" "`readlink -f "$f"`" )
done

# Execute the binary, expanding the array on the command line.
exec "$binary" "${A[@]}"


# ----------------------------------------------------------------------