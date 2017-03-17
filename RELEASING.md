Releasing a New Version
=======================

* Update translations
    - `tools/update-translations`
    - `msgmerge -UN po/fi.po po/nfoview.pot`
    - `emacs po/fi.po`
    - `tx push -s`
    - `tx push -tf -l fi`
    - `tx pull -a --minimum-perc=75`
    - `tools/check-translations`
    - `tools/check-translations | grep %`
    - `git commit -a -m "Update translations for X.Y.Z"`
* Do final quality checks
    - `python3 -Wd bin/nfoview`
    - `pyflakes bin/nfoview nfoview setup.py`
    - `py.test --tb=no nfoview`
* Bump version number
    - `nfoview/__init__.py`
* Update `NEWS.md` and `TODO.md`
* Check that installation works
    - `sudo python3 setup.py install --prefix=/usr/local`
    - `sudo python3 setup.py clean`
    - `/usr/local/bin/nfoview`
* Commit changes
    - `git commit -a -m "RELEASE X.Y.Z"`
    - `git tag -s X.Y.Z`
    - `git push`
    - `git push --tags`
* Build Windows installer (see [`win32/RELEASING.md`](win32/RELEASING.md))
* Add release notes and Windows installer on GitHub
* Update [web site](http://otsaloma.io/nfoview/)
