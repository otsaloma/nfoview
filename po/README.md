Translating NFO Viewer
======================

Translations are available at [Transifex][1]. Please use that to add and
update translations.

To try your translation, get the nfoview source code from [GitHub][2],
download the translation from Transifex, place it in the `po` directory
and compile that translation to the `locale` directory (which does not
exist by default).

```sh
mkdir -p locale/xx/LC_MESSAGES
msgfmt -cv po/xx.po -o locale/xx/LC_MESSAGES/nfoview.mo
LANG=xx bin/nfoview
```

[1]: http://www.transifex.com/projects/p/nfoview/
[2]: http://github.com/otsaloma/nfoview
