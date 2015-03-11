#!/bin/bash
##############################################################################
# Generates po and mo files from the project source code
# Author: Cody Precord
# Copyright: Cody Precord <cprecord@editra.org>
# License: wxWindows
##############################################################################

##############################################################################
# Variables
##############################################################################
ARG=$1
IMPORT_DIR=$2

##############################################################################
# Function: print_help
# Purpose: Print the scripts usage help to the console
##############################################################################
print_help () {
	echo
	echo "Usage: $0 [-h|-mo|-po|-all|-app]"
	echo "    -h    Print this help message"
	echo "    -mo   Generate mo files and install them in the locale directory"
	echo "    -po   Generate new po files from the project source"
    echo "    -all  Regenerate everything"
    echo "    -app  Only regenerate the file list"
    echo "    -lp <path> Import translations from Launchpad export"
	echo
}

##############################################################################
# Function: get_appfile
# Purpose: Generate the app file
##############################################################################
gen_appfile () {
    OUTPUT="$(pwd)/app.fil"
    BASE="../.."
    PLUGINS="$BASE/plugins"

    # Remove current file
    rm app.fil

    # Start searching for files
    DIRS=("$BASE/" "$BASE/src/" "$BASE/src/eclib/" "$BASE/src/syntax/" 
          "$PLUGINS/" "$PLUGINS/codebrowser/codebrowser/"
          "$PLUGINS/filebrowser/filebrowser/" "$PLUGINS/Launch/launch/"
          "$PLUGINS/PyShell/PyShell/" )

    # TODO: why does this not give the right number?
    #DIRNUM=${#DIRS}

    for ((i=0; i < 9; i++)); do
        DIR=${DIRS[${i}]}
        for FNAME in $(ls $DIR); do
            if ! [ -z `echo $FNAME | grep "^.*\.py$"` ]; then
                if [ -a "$DIR$FNAME" ]; then
                    echo "Found: $DIR$FNAME"
                    echo "$DIR$FNAME" >> $OUTPUT
                fi
            fi
        done
    done
}

##############################################################################
# Function: import_lp_files
# Purpose: Copy exported launchpad files to here and rename
##############################################################################
import_lp_files() {
    python getlpfiles.py $IMPORT_DIR
}

##############################################################################
# Function: gen_flist
# Purpose: Generate the list of files to create the po files from
##############################################################################
gen_flist() {
    python mkflist.py
}

##############################################################################
# Function: gen_po
# Purpose: Generate new po files from the source
##############################################################################
gen_po () {
    python mki18n.py -pv --domain=Editra
    # Copy all .new files to override the originals
    for fname in $(ls); do
        if ! [ -z $(echo $fname | grep '.*\.new') ]; then
            name=$(echo $fname | sed 's/.new//')
            mv $fname $name
        fi
    done
}

##############################################################################
# Function: make_mo
# Purpose: Make mo files and place them in the appropriate locale directory
##############################################################################
make_mo () {
    python mki18n.py -mv --domain=Editra --moTarget=../../locale
}


##############################################################################
# Main
##############################################################################

if [ "$ARG" = "-po" ]
then
    gen_appfile
    gen_po
    exit 0
elif [ "$ARG" = "-mo" ]
then
    make_mo
    exit 0
elif [ "$ARG" = "-all" ]
then
    gen_appfile
    gen_po
    make_mo
    exit 0
elif [ "$ARG" = "-app" ]
then
    gen_appfile
    exit 0
elif [ "$ARG" = "-lp" ]
then
    import_lp_files
    exit 0
else
    print_help
fi    
