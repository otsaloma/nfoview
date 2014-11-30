Installation
============

The installation process requires that you have Python, gettext and
intltool installed. Depending on your distro's Python packaging you may
also need a package called python-dev or python-devel. For dependencies
required to run NFO Viewer, see the file README.md.

To install, run command

    python3 setup.py clean install [--prefix=...]

Uninstallation
==============

To uninstall, remove files and directories

    .../bin/nfoview
    .../lib/python3.*/dist-packages/nfoview*
    .../lib/python3.*/site-packages/nfoview*
    .../share/appdata/nfoview.appdata.xml
    .../share/applications/nfoview.desktop
    .../share/icons/hicolor/*/apps/nfoview.*
    .../share/locale/*/LC_MESSAGES/nfoview.mo
    .../share/nfoview/
    .../share/man/man1/nfoview.1
