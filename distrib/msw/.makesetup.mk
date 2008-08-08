

HYB_SEDCMD=sed "s!wxUSE_MEMORY_TRACING 1!wxUSE_MEMORY_TRACING 0!g;s!wxUSE_DEBUG_CONTEXT 1!wxUSE_DEBUG_CONTEXT 0!g"
!if "$(CPU)" == "AMD64"
UNI_SEDCMD=sed "s!wxUSE_UNICODE 0!wxUSE_UNICODE 1!g"
DLLDIR=vc_amd64_dll
!else
UNI_SEDCMD=sed "s!wxUSE_UNICODE 0!wxUSE_UNICODE 1!g;s!wxUSE_UNICODE_MSLU 0!wxUSE_UNICODE_MSLU 1!g"
DLLDIR=vc_dll
!endif


SRC=$(WXWIN)\include\wx\msw\setup.h
DIR=$(WXWIN)\lib
FILES=	$(DIR)\$(DLLDIR)\mswd\wx\setup.h \
        $(DIR)\$(DLLDIR)\mswh\wx\setup.h \
        $(DIR)\$(DLLDIR)\mswud\wx\setup.h \
        $(DIR)\$(DLLDIR)\mswuh\wx\setup.h \
        $(DIR)\$(DLLDIR)\msw\wx\setup.h \
        $(DIR)\$(DLLDIR)\mswu\wx\setup.h \
	\
        $(DIR)\vc_lib\msw\wx\setup.h \



all : $(FILES)

test :
	echo $(DIR)\vc_lib\msw\wx\setup.h

# debug
$(DIR)\$(DLLDIR)\mswd\wx\setup.h : $(SRC) .makesetup.mk
	-if not exist  $(DIR)\$(DLLDIR)\mswd\wx mkdir $(DIR)\$(DLLDIR)\mswd\wx
	cat $(SRC) > $@

# hybrid
$(DIR)\$(DLLDIR)\mswh\wx\setup.h : $(SRC) .makesetup.mk
	-if not exist  $(DIR)\$(DLLDIR)\mswh\wx mkdir $(DIR)\$(DLLDIR)\mswh\wx
	cat $(SRC) | $(HYB_SEDCMD) > $@

# release
$(DIR)\$(DLLDIR)\msw\wx\setup.h : $(SRC) .makesetup.mk
	-if not exist  $(DIR)\$(DLLDIR)\msw\wx mkdir $(DIR)\$(DLLDIR)\msw\wx
	cat $(SRC) > $@

$(DIR)\vc_lib\msw\wx\setup.h : $(SRC) .makesetup.mk
	-if not exist  $(DIR)\vc_lib\msw\wx mkdir $(DIR)\vc_lib\msw\wx
	cat $(SRC) > $@

# debug-uni
$(DIR)\$(DLLDIR)\mswud\wx\setup.h : $(SRC) .makesetup.mk
	-if not exist  $(DIR)\$(DLLDIR)\mswud\wx mkdir $(DIR)\$(DLLDIR)\mswud\wx
	cat $(SRC) | $(UNI_SEDCMD) > $@

# hybrid-uni
$(DIR)\$(DLLDIR)\mswuh\wx\setup.h : $(SRC) .makesetup.mk
	-if not exist  $(DIR)\$(DLLDIR)\mswuh\wx mkdir $(DIR)\$(DLLDIR)\mswuh\wx
	cat $(SRC) | $(UNI_SEDCMD) | $(HYB_SEDCMD) > $@

# release-uni
$(DIR)\$(DLLDIR)\mswu\wx\setup.h : $(SRC) .makesetup.mk
	-if not exist  $(DIR)\$(DLLDIR)\mswu\wx mkdir $(DIR)\$(DLLDIR)\mswu\wx
	cat $(SRC) | $(UNI_SEDCMD) > $@



