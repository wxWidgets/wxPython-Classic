#!/bin/bash

unicode=yes
debug=no
reswig=no
clean=no

for flag in $*; do
    case ${flag} in
      debug)       debug=yes              ;;
      ansi)        unicode=no             ;;
      unicode)     unicode=yes            ;;
      reswig)      reswig=yes             ;;
      clean)       clean=yes              ;;
    esac
done

scriptDir="$(cd $(dirname $0);pwd)"
scriptName="$(basename $0)"

if [ "$WXWIN" = "" ]; then
  export WXWIN=$scriptDir/..
fi
  
# clean the wxPython build files, this part is platform-agnostic
# we do the platform-specific clean below.
if [ $clean = yes ]; then
  rm -rf $scriptDir/build $scriptDir/build.unicode
  rm -rf $scriptDir/wx/*.pyd
  rm -rf $scriptDir/wx/*.so
fi

echo "wxWidgets directory is: $WXWIN"

if [ "$OSTYPE" = "cygwin" ]; then
  export WXWIN=`cygpath -d $WXWIN`

  if [ $clean = yes ]; then
    rm -rf $WXWIN/build/msw/vc_msw*
    
    # TODO: test using .make with a clean argument
    if [ $ansi = yes ]; then
      rm -rf $WXWIN/lib/vc_dll/wxmsw28h*
      rm -rf $WXWIN/lib/vc_dll/vc_mswhdll
    fi
    
    if [ $unicode = yes ]; then
      rm -rf $WXWIN/lib/vc_dll/wxmsw28uh*
      rm -rf $WXWIN/lib/vc_dll/vc_mswuhdll
    fi
    rm -rf $WXWIN/lib/*h.lib
  fi

  # do setup of build environment vars
  if [ "$TOOLS" = "" ]; then
    export TOOLS=`cygpath C:\\`
  fi

  if [ "$SWIGDIR" = "" ]; then
    export SWIGDIR=$TOOLS/SWIG-1.3.24
  fi

  DEBUG_FLAG=
  UNICODE_FLAG=
  if [ $debug = yes ]; then
    DEBUG_FLAG=--debug
  fi
  if [ $unicode = yes ]; then
    UNICODE_FLAG="UNICODE=1"
  fi

  # change the setup.h defines for wxPython
  update_setup_h $WXWIN_CYGPATH/include/wx/msw

  # copy wxPython build scripts
  cp $WXWIN_CYGPATH/wxPython/distrib/msw/.m* $WXWIN/build/msw
  
  cd $WXWIN_CYGPATH/build/msw
  # remove old build files
  UNI=
  if [ $unicode = yes ]; then
      UNI=-uni
  fi
  
  ./.make hybrid$UNI
  
  if [ $? != 0 ]; then
    exit $?
  fi
  
  cd $WXWIN_CYGPATH/wxPython

  # update the language files
  $TOOLS/Python$PY_VERSION/python `cygpath -d $WXWIN/wxPython/distrib/makemo.py`
  
  # re-generate SWIG files
  if [ $reswig = yes ]; then
    $WXWIN_CYGPATH/wxPython/b $PY_VERSION t
  fi
  
  # build the hybrid extension
  # NOTE: Win Python needs Windows-style pathnames, so we 
  # need to convert
  export SWIGDIR=`cygpath -w $SWIGDIR`
  
  # TODO: Currently the b script used here doesn't exit with
  # non-zero even if there's an error. Once it's been updated to do
  # so, make sure build-wxpython.sh exits with that same error code.
  
  $WXWIN_CYGPATH/wxPython/b $PY_VERSION h $DEBUG_FLAG $UNICODE_FLAG

  cp $WXWIN_CYGPATH/lib/vc_dll/*.dll $WXWIN_CYGPATH/wxPython/wx
  
else
  if [ "$WXPY_BUILD_DIR" = "" ]; then
    WXPY_BUILD_DIR=$PWD/wxpy-bld
  fi
  
  if [ "$WXPY_INSTALL_DIR" = "" ]; then
    WXPY_INSTALL_DIR=$HOME/wxpython-2.8.4
  fi
  
  if [ $clean = yes ]; then
    rm -rf $WXPY_BUILD_DIR
    rm -rf $WXPY_INSTALLDIR
    exit 0
  fi

  UNICODE_OPT=
  UNICODE_WXPY_OPT=0
  if [ $unicode = yes ]; then
    UNICODE_OPT=unicode
    UNICODE_WXPY_OPT=1
  fi 
  
  DEBUG_OPT=
  if [ $debug = yes ]; then
    DEBUG_OPT=debug
  fi

  mkdir -p $WXPY_BUILD_DIR
  cd $WXPY_BUILD_DIR
  export INSTALLDIR=$WXPY_INSTALL_DIR
  
  if [ "${OSTYPE:0:6}" = "darwin" ]; then
    $WXWIN/distrib/scripts/mac/macbuild-lipo wxpython $UNICODE_OPT $DEBUG_OPT
  else
    $WXWIN/distrib/scripts/unix/unixbuild wxpython $UNICODE_OPT $DEBUG_OPT
  fi
  
  if [ $? != 0 ]; then
    exit $?
  fi

  cd $scriptDir
  python ./setup.py build_ext --inplace WX_CONFIG=$WXPY_INSTALL_DIR/bin/wx-config USE_SWIG=1 SWIG=/opt/swig/bin/swig UNICODE=$UNICODE_WXPY_OPT
  if [ $? != 0 ]; then
    exit $?
  fi
fi

# return to original dir
cd $WXWIN/wxPython

echo "------------ BUILD FINISHED ------------"
echo ""
echo "To run the wxPython demo:"
echo ""
echo "1) set your PYTHONPATH variable to $WXWIN."
echo "2) run python demo/demo.py"
echo ""

