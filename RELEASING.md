Releasing a New Version
=======================

 * Update translations
   - `tx pull`
   - `tools/update-translations`
   - `virtaal po/fi.po`
   - `tools/check-translations`
   - `tx push -stf`
   - `git commit -a -m "Update translations for X.Y.Z."`
 * Do final quality checks
   - `python3 -Wd bin/nfoview`
   - `pyflakes3 bin/nfoview nfoview setup.py`
   - `py.test-3 --tb=no nfoview`
 * Bump version numbers
   - `$EDITOR nfoview/__init__.py`
   - `$EDITOR NEWS.md TODO.md`
 * Check that installation works
   - `sudo python3 setup.py clean install --prefix=/usr/local`
   - `sudo python3 setup.py clean`
   - `/usr/local/bin/nfoview`
 * Commit changes
   - `git commit -a -m "RELEASE X.Y.Z"`
   - `git tag -s X.Y.Z`
   - `git push`
   - `git push --tags`
 * Send announcements and update web sites
   - <http://github.com/otsaloma/nfoview/releases>
   - <http://otsaloma.github.io/nfoview>
   - <http://bugzilla.gnome.org/editproducts.cgi?action=edit&product=nfoview>
