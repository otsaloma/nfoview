Translating NFO Viewer
======================

Translations are available at [Transifex][]. Please use that to add and
update translations.

To try your translation, get the nfoview source code from [GitHub][],
download the translation from Transifex, place it in the `po` directory
and compile that translation to the `locale` directory (which does not
exist by default).

```bash
mkdir -p locale/xx/LC_MESSAGES
msgfmt -cv po/xx.po -o locale/xx/LC_MESSAGES/nfoview.mo
LANG=xx bin/nfoview
```

[GitHub]: http://github.com/otsaloma/nfoview
[Transifex]: http://www.transifex.com/otsaloma/nfoview/
