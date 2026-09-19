# -*- coding: utf-8-unix -*-

# Installation directories without DESTDIR.
# Only used by install, build uses no variables at all.
PREFIX    = /usr/local
BINDIR    = $(PREFIX)/bin
DATADIR   = $(PREFIX)/share
LIBDIR    = $(DATADIR)/nfoview
LOCALEDIR = $(DATADIR)/locale
MANDIR    = $(DATADIR)/man

# EDITOR must wait!
EDITOR = nano

# Packagers tend to just run 'make'.
.DEFAULT_GOAL = build

build:
	@echo "BUILDING PYTHON PACKAGE..."
	rm -rf build
	mkdir -p build
	cp -R nfoview build
	find build -type d -name __pycache__ -prune -exec rm -rf {} +
	find build -type d -name test -prune -exec rm -rf {} +
	@echo "BUILDING TRANSLATIONS..."
	rm -f po/LINGUAS
	ls po/*.po | cut -d/ -f2 | cut -d. -f1 > po/LINGUAS
	mkdir -p build/mo
	for LOCALE in `cat po/LINGUAS`; do msgfmt po/$$LOCALE.po -o build/mo/$$LOCALE.mo; done
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
	flake8 nfoview
	flake8 bin/nfoview
	flake8 bin/nfoview.in
	flake8 conftest.py
	for X in data/*.ui; do echo $$X; gtk4-builder-tool validate $$X; done

clean:
	rm -rf build
	rm -rf dist
	rm -rf flatpak/.flatpak-builder
	rm -rf flatpak/build
	rm -f po/LINGUAS
	rm -f po/*~
	find . -type d -name __pycache__ -prune -exec rm -rf {} +
	find . -type d -name .pytest_cache -prune -exec rm -rf {} +

install:
	test -f build/.complete
	@echo "INSTALLING PYTHON PACKAGE..."
	mkdir -p $(DESTDIR)$(LIBDIR)
	cp -R build/nfoview $(DESTDIR)$(LIBDIR)
	sed \
	-e "s|^DATA_DIR = .*$$|DATA_DIR = Path('$(LIBDIR)')|" \
	-e "s|^LOCALE_DIR = .*$$|LOCALE_DIR = Path('$(LOCALEDIR)')|" \
	build/nfoview/paths.py > $(DESTDIR)$(LIBDIR)/nfoview/paths.py
	grep -qF "$(LIBDIR)" $(DESTDIR)$(LIBDIR)/nfoview/paths.py
	grep -qF "$(LOCALEDIR)" $(DESTDIR)$(LIBDIR)/nfoview/paths.py
	@echo "INSTALLING LAUNCHER..."
	mkdir -p $(DESTDIR)$(BINDIR)
	sed "s|%LIBDIR%|$(LIBDIR)|" bin/nfoview.in > $(DESTDIR)$(BINDIR)/nfoview
	grep -qF "$(LIBDIR)" $(DESTDIR)$(BINDIR)/nfoview
	chmod +x $(DESTDIR)$(BINDIR)/nfoview
	@echo "INSTALLING DATA FILES..."
	cp -f data/*.ui $(DESTDIR)$(LIBDIR)
	@echo "INSTALLING ICONS..."
	mkdir -p $(DESTDIR)$(DATADIR)/icons/hicolor/scalable/apps
	mkdir -p $(DESTDIR)$(DATADIR)/icons/hicolor/symbolic/apps
	cp -f data/io.otsaloma.nfoview.svg $(DESTDIR)$(DATADIR)/icons/hicolor/scalable/apps
	cp -f data/io.otsaloma.nfoview-symbolic.svg $(DESTDIR)$(DATADIR)/icons/hicolor/symbolic/apps
	@echo "INSTALLING TRANSLATIONS..."
	for MO in build/mo/*.mo; do \
	LOCALE=`basename $$MO .mo`; \
	mkdir -p $(DESTDIR)$(LOCALEDIR)/$$LOCALE/LC_MESSAGES; \
	cp -f $$MO $(DESTDIR)$(LOCALEDIR)/$$LOCALE/LC_MESSAGES/nfoview.mo; \
	done
	@echo "INSTALLING DESKTOP FILE..."
	mkdir -p $(DESTDIR)$(DATADIR)/applications
	cp -f build/io.otsaloma.nfoview.desktop $(DESTDIR)$(DATADIR)/applications
	@echo "INSTALLING APPDATA FILE..."
	mkdir -p $(DESTDIR)$(DATADIR)/metainfo
	cp -f build/io.otsaloma.nfoview.appdata.xml $(DESTDIR)$(DATADIR)/metainfo
	@echo "INSTALLING MAN PAGE..."
	mkdir -p $(DESTDIR)$(MANDIR)/man1
	cp -f data/nfoview.1 $(DESTDIR)$(MANDIR)/man1
	test -z "$(DESTDIR)" && update-desktop-database "$(DATADIR)/applications" || true

# Interactive!
release:
	$(MAKE) check test clean
	@echo "BUMP VERSION NUMBERS"
	$(EDITOR) nfoview/__init__.py
	@echo "ADD RELEASE NOTES"
	$(EDITOR) NEWS.md
	$(EDITOR) data/io.otsaloma.nfoview.appdata.xml.in
	appstreamcli validate --no-net data/io.otsaloma.nfoview.appdata.xml.in
	sudo $(MAKE) build install clean
	/usr/local/bin/nfoview
	tools/release
	@echo "REMEMBER TO UPDATE FLATPAK"
	@echo "REMEMBER TO UPDATE WEBSITE"

test:
	pytest -xs nfoview

# Interactive!
translations:
	tools/update-translations

warnings:
	G_ENABLE_DIAGNOSTIC=1 python3 -Wd bin/nfoview README.md

.PHONY: build check clean install release test translations warnings
