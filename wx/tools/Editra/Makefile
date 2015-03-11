# Editra Makefile
#
# Instructions:
# To make source bundle: make sdist
# To make eggs: make egg
# To make plugins: make plugin
#

# Variables
PYVERSION = 2.5
EGGFILTER = *py2.4.egg *py2.6.egg

# Paths
PLUGINS = ./plugins
FILEBROWSER = $(PLUGINS)/filebrowser
PYSHELL = $(PLUGINS)/PyShell
CODEBROWSER = $(PLUGINS)/codebrowser
LAUNCH = $(PLUGINS)/Launch
I18NDIR = ./scripts/i18n

# Generated Paths
OSXAPP = ./dist/Editra.app/
OSXRESOURCES = $(OSXAPP)/Contents/Resources/

# Commands
PYTHON = python$(PYVERSION)
MAKE_PLUGIN24 = python2.4 ./setup.py bdist_egg --dist-dir=../
MAKE_PLUGIN25 = python2.5 ./setup.py bdist_egg --dist-dir=../
MAKE_PLUGIN26 = python2.6 ./setup.py bdist_egg --dist-dir=../
MAKE_EGG24 = python2.4 ./setup.py bdist_egg 
MAKE_EGG25 = python2.5 ./setup.py bdist_egg 
MAKE_EGG26 = python2.6 ./setup.py bdist_egg 

#---- Plugins ----#

filebrowser:
	cd $(FILEBROWSER) && $(MAKE_PLUGIN24)
	cd $(FILEBROWSER) && $(MAKE_PLUGIN25)
	cd $(FILEBROWSER) && $(MAKE_PLUGIN26)

pyshell:
	cd $(PYSHELL) && $(MAKE_PLUGIN24)
	cd $(PYSHELL) && $(MAKE_PLUGIN25)
	cd $(PYSHELL) && $(MAKE_PLUGIN26)

codebrowser:
	cd $(CODEBROWSER) && $(MAKE_PLUGIN24)
	cd $(CODEBROWSER) && $(MAKE_PLUGIN25)
	cd $(CODEBROWSER) && $(MAKE_PLUGIN26)

launch:
	cd $(LAUNCH) && $(MAKE_PLUGIN24)
	cd $(LAUNCH) && $(MAKE_PLUGIN25)
	cd $(LAUNCH) && $(MAKE_PLUGIN26)

plugins: filebrowser codebrowser pyshell launch

docs:
	cd ./scripts/gendocs && ./gen_api_docs.sh

i18n:
	cd $(I18NDIR) && ./gen_lang.sh -all

depfiles: plugins i18n

sdist: depfiles
	$(PYTHON) ./setup.py sdist

osx_applet: depfiles osx_app_nodeps

osx_app_nodeps:
	$(PYTHON) ./setup.py py2app
	cd $(OSXRESOURCES)/plugins && rm -f $(EGGFILTER)
	cd $(OSXRESOURCES)/pixmaps && rm -f *.ico

egg: depfiles
	$(MAKE_EGG24)
	$(MAKE_EGG25)
	$(MAKE_EGG26)

install: depfiles
	python ./setup.py install

clean:
	rm -rf *.pyc build dist src/*.pyc src/*.pyo
