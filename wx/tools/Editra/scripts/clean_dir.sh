#!/bin/bash
# Cleans up all the junk files from the project directories

CWD=$(pwd)
EXPATH=$(dirname $0)
SCRIPT=$(basename $0)
IGNORE=".svn .cvs"

BLUE="[34;01m"
CYAN="[36;01m"
GREEN="[32;01m"
RED="[31;01m"
YELLOW="[33;01m"
OFF="[0m"

DELETED=0

echo "${YELLOW}**${OFF} Cleaning Project Directories ${YELLOW}**${OFF}"
sleep 2

# Go to the script directory
cd $EXPATH

# Go to project
cd ..
PROJDIR=$(pwd)

echo "${YELLOW}**${OFF} Starting from project root $PROJDIR"
ls *~ 2>/dev/null
if [ $? -eq 0 ]; then
   for f in $(ls *~); do
	echo "${RED}Deleting${OFF} $f";
	rm -f "$f";
	let "DELETED = $DELETED + 1"
   done
fi

for item in $(ls -R); do
	if [ "$(echo $item | grep \: )" != "" ]; then
	       dest=$(echo $item | tr -d ":");
       	   echo "${GREEN}Cleaning${OFF} $dest";
	       cd "$dest";
	       ls *~ 2>/dev/null;
	       if [ $? -eq 0 ]; then
              for f in $(ls *~); do
		           echo "${RED}Deleting${OFF} $f";
	               rm -f $f;
	               let "DELETED = $DELETED + 1"
	          done
	       fi
	       ls *.pyc 2>/dev/null
	       if [ $? -eq 0 ]; then
              for f in $(ls *.pyc); do
		           echo "${RED}Deleting${OFF} $f";
	               rm -f $f;
	               let "DELETED = $DELETED + 1"
	          done
	       fi
	       ls *.pyo 2>/dev/null
	       if [ $? -eq 0 ]; then
             for f in $(ls *.pyo); do
		           echo "${RED}Deleting${OFF} $f";
	               rm -f $f;
	               let "DELETED = $DELETED + 1"
	          done
	       fi
	       cd "$PROJDIR"
	fi	       
done
echo
echo "${CYAN}Finished Cleaning Project Directories!!${OFF}"
echo "A total of ${RED}$DELETED${OFF} files were cleaned from the project directories"
echo
