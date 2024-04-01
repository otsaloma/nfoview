# -*- coding: utf-8-unix -*-

DESTDIR   =
PREFIX    = /usr/local
BINDIR    = $(DESTDIR)$(PREFIX)/bin
DATADIR   = $(DESTDIR)$(PREFIX)/share
LOCALEDIR = $(DESTDIR)$(PREFIX)/share/locale

# EDITOR must wait!
EDITOR = nano

build:
	@echo "BUILDING PYTHON PACKAGE..."
	mkdir -p build/nfoview
	cp nfoview/*.py build/nfoview
	sed -i "s|^DATA_DIR = .*$$|DATA_DIR = Path('$(DATADIR)/nfoview')|" build/nfoview/paths.py
	sed -i "s|^LOCALE_DIR = .*$$|LOCALE_DIR = Path('$(LOCALEDIR)')|" build/nfoview/paths.py
	fgrep -q "$(DATADIR)/nfoview" build/nfoview/paths.py
	fgrep -q "$(LOCALEDIR)" build/nfoview/paths.py
	flake8 build/nfoview/*.py
	@echo "BUILDING SCRIPT..."
	mkdir -p build/bin
	cp bin/nfoview.in build/bin/nfoview
	sed -i "s|%LIBDIR%|$(DATADIR)/nfoview|" build/bin/nfoview
	fgrep -q "$(DATADIR)/nfoview" build/bin/nfoview
	flake8 build/bin/nfoview
	chmod +x build/bin/nfoview
	@echo "BUILDING TRANSLATIONS..."
	mkdir -p build/mo
	for LANG in `cat po/LINGUAS`; do msgfmt po/$$LANG.po -o build/mo/$$LANG.mo; done
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
	mkdir -p $(DATADIR)/nfoview/nfoview
	cp -f build/nfoview/*.py $(DATADIR)/nfoview/nfoview
	@echo "INSTALLING SCRIPT..."
	mkdir -p $(BINDIR)
	cp -f build/bin/nfoview $(BINDIR)
	@echo "INSTALLING DATA FILES..."
	mkdir -p $(DATADIR)/nfoview
	cp -f data/*.ui $(DATADIR)/nfoview
	@echo "INSTALLING ICONS..."
	mkdir -p $(DATADIR)/icons/hicolor/scalable/apps
	mkdir -p $(DATADIR)/icons/hicolor/symbolic/apps
	cp -f data/io.otsaloma.nfoview.svg $(DATADIR)/icons/hicolor/scalable/apps
	cp -f data/io.otsaloma.nfoview-symbolic.svg $(DATADIR)/icons/hicolor/symbolic/apps
	@echo "INSTALLING TRANSLATIONS..."
	for LANG in `cat po/LINGUAS`; do mkdir -p $(LOCALEDIR)/$$LANG/LC_MESSAGES; done
	for LANG in `cat po/LINGUAS`; do cp -f build/mo/$$LANG.mo $(LOCALEDIR)/$$LANG/LC_MESSAGES/nfoview.mo; done
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
