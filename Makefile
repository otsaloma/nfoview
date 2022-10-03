# -*- coding: utf-8-unix -*-

DESTDIR   =
PREFIX    = /usr/local
DATADIR   = $(DESTDIR)$(PREFIX)/share
LOCALEDIR = $(DESTDIR)$(PREFIX)/share/locale

# Allow overriding setup.py paths. Note that we can't set
# SETUP_PREFIX=PREFIX as many distros are automatically adding
# 'local', causing '/usr/local/local' and a broken install.
SETUP_ROOT   = $(DESTDIR)
SETUP_PREFIX =

# EDITOR must wait!
EDITOR = nano

# TODO: Use either 'pip3 install' or 'python3 -m build' + 'python3 -m
# installer' once either supports a sensible installation both from
# source (--prefix=/usr/local, whether implicit or explicit) and
# building a distro package (--destdir=pkg --prefix=/usr). As of 9/2022
# it seems setup.py is deprecated, but there is no replacement.

build:
	@echo "BUILDING PYTHON PACKAGE..."
	NFOVIEW_PREFIX=$(PREFIX) ./setup-partial.py build
	@echo "BUILDING TRANSLATIONS..."
	mkdir -p build/mo
	for LANG in `cat po/LINGUAS`; do \
	echo $$LANG; \
	msgfmt po/$$LANG.po -o build/mo/$$LANG.mo; \
	done
	@echo "BUILDING DESKTOP FILE..."
	msgfmt --desktop -d po \
	--template data/io.otsaloma.nfoview.desktop.in \
	-o build/io.otsaloma.nfoview.desktop
	@echo "BUILDING APPDATA FILE..."
	msgfmt --xml -d po \
	--template data/io.otsaloma.nfoview.appdata.xml.in \
	-o build/io.otsaloma.nfoview.appdata.xml
	touch build/.complete

check:
	flake8 .
	flake8 bin/*

clean:
	rm -rf build
	rm -rf nfoview.egg-info
	rm -rf dist
	rm -rf __pycache__
	rm -rf */__pycache__
	rm -rf */*/__pycache__
	rm -rf */*/*/__pycache__

install:
	test -f build/.complete
	@echo "INSTALLING PYTHON PACKAGE..."
	NFOVIEW_PREFIX=$(PREFIX) ./setup-partial.py install \
	$(if $(SETUP_ROOT),--root=$(SETUP_ROOT),) \
	$(if $(SETUP_PREFIX),--prefix=$(SETUP_PREFIX),)
	@echo "INSTALLING DATA FILES..."
	mkdir -p $(DATADIR)/nfoview
	cp -f data/*.ui $(DATADIR)/nfoview
	@echo "INSTALLING ICONS..."
	mkdir -p $(DATADIR)/icons/hicolor/scalable/apps
	mkdir -p $(DATADIR)/icons/hicolor/symbolic/apps
	cp -f data/io.otsaloma.nfoview.svg $(DATADIR)/icons/hicolor/scalable/apps
	cp -f data/io.otsaloma.nfoview-symbolic.svg $(DATADIR)/icons/hicolor/symbolic/apps
	@echo "INSTALLING TRANSLATIONS..."
	for LANG in `cat po/LINGUAS`; do \
	echo $$LANG; \
	mkdir -p $(LOCALEDIR)/$$LANG/LC_MESSAGES; \
	cp -f build/mo/$$LANG.mo $(LOCALEDIR)/$$LANG/LC_MESSAGES/nfoview.mo; \
	done
	@echo "INSTALLING DESKTOP FILE..."
	mkdir -p $(DATADIR)/applications
	cp -f build/io.otsaloma.nfoview.desktop $(DATADIR)/applications
	@echo "INSTALLING APPDATA FILE..."
	mkdir -p $(DATADIR)/metainfo
	cp -f build/io.otsaloma.nfoview.appdata.xml $(DATADIR)/metainfo
	@echo "INSTALLING MAN PAGE..."
	mkdir -p $(DATADIR)/man/man1
	cp -f data/nfoview.1 $(DATADIR)/man/man1

# Interactive!
release:
	$(MAKE) check test clean
	@echo "BUMP VERSION NUMBERS"
	$(EDITOR) nfoview/__init__.py
	@echo "ADD RELEASE NOTES"
	$(EDITOR) NEWS.md
	$(EDITOR) data/io.otsaloma.nfoview.appdata.xml.in
	sudo $(MAKE) PREFIX=/usr/local build install clean
	/usr/local/bin/nfoview
	tools/release
	@echo "REMEMBER TO UPDATE FLATPAK"
	@echo "REMEMBER TO UPDATE WEBSITE"

test:
	py.test -xs .

# Interactive!
translations:
	tools/update-translations

.PHONY: build check clean install release test translations
