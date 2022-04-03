# -*- coding: utf-8-unix -*-

# EDITOR must wait!
EDITOR = nano

check:
	flake8 bin/nfoview
	flake8 nfoview
	flake8 *.py

clean:
	./setup.py clean

install:
	./setup.py install

# Interactive!
release:
	$(MAKE) check test clean
	@echo "BUMP VERSION NUMBERS"
	$(EDITOR) nfoview/__init__.py
	@echo "ADD RELEASE NOTES"
	$(EDITOR) NEWS.md
	$(EDITOR) data/io.otsaloma.nfoview.appdata.xml.in
	sudo ./setup.py install --prefix=/usr/local clean
	/usr/local/bin/nfoview
	tools/release
	@echo "REMEMBER TO UPDATE FLATPAK"
	@echo "REMEMBER TO UPDATE WEBSITE"

test:
	py.test -xs nfoview

# Interactive!
translations:
	tools/update-translations

warnings:
	python3 -Wd bin/nfoview

.PHONY: check clean install release test translations warnings
