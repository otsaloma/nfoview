Releasing a New Version
=======================

```bash
# Update translations.
tools/update-translations
tx push -s
tx pull -a --minimum-perc=50
sed -i "s/charset=CHARSET/charset=UTF-8/" po/*.po
emacs po/fi.po
tx push -tf --no-interactive -l fi
tools/check-translations
tools/check-translations | grep %
git add po/*.po po/*.pot; git status
git commit -m "Update translations"

# Check, test, do final edits and release.
python3 -Wd bin/nfoview
flake8 bin/nfoview nfoview setup.py
py.test --tb=no nfoview
emacs nfoview/__init__.py win32/nfoview.iss
emacs NEWS.md TODO.md data/io.otsaloma.nfoview.appdata.xml.in
sudo ./setup.py install --prefix=/usr/local clean
/usr/local/bin/nfoview
tools/release

# Update Flatpak, website.
# https://github.com/flathub/io.otsaloma.nfoview
# https://github.com/otsaloma/nfoview-www
```
