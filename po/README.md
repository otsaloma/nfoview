Translating NFO Viewer
======================

To avoid doing redundant work, first check the latest list of existing
translations at the [head of the master branch][1].

 [1]: http://github.com/otsaloma/nfoview/tree/master/po

To try your translation in the source directory, you can compile it to
the `locale` directory (which does not exist by default).

    mkdir -p locale/XX/LC_MESSAGES
    msgfmt -cv po/XX.po -o locale/XX/LC_MESSAGES/nfoview.mo
    python3 bin/nfoview

A script has been written to check translation files for some common
potential errors. You can use it to check your translation using the
following command.

    python3 tools/check-translations [XX...]

When done, send your translation by email to <otsaloma@iki.fi>, or,
if you find it more convenient, fork the repository on GitHub and send
a pull request.
