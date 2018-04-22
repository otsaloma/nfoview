NFO Viewer
==========

[![Build Status](https://travis-ci.org/otsaloma/nfoview.svg)](https://travis-ci.org/otsaloma/nfoview)
[![Packages](https://repology.org/badge/tiny-repos/nfoview.svg)](https://repology.org/metapackage/nfoview)
[![Gitter](https://badges.gitter.im/Join%20Chat.svg)](https://gitter.im/otsaloma/nfoview)
[![Donate](https://img.shields.io/badge/donate-paypal.me-blue.svg)](https://www.paypal.me/otsaloma)

NFO Viewer is a simple viewer for NFO files, which are "ASCII" art in
the CP437 codepage. The advantages of using NFO Viewer instead of a text
editor are preset font and encoding settings, automatic window size and
clickable hyperlinks.

## Installing

### Linux

NFO Viewer is packaged for most of the popular [distros][packages], so
easiest is to install via your distro's package management. If you need
a newer version than packaged, read on.

NFO Viewer requires Python ≥ 3.2, PyGObject ≥ 3.0.0 and GTK+ ≥ 3.12.
Additionally, during installation you need gettext. On Debian/Ubuntu you
can install these with the following command.

    sudo apt install python3 python3-gi gir1.2-gtk-3.0 gettext

Then, to install NFO Viewer, run command

    python3 setup.py install --prefix=/usr/local

[packages]: https://repology.org/metapackage/nfoview

### Windows

See the [releases page][releases] for installers. Note that Windows
packaging will sometimes be a bit behind and might sometimes skip a
version, so you might need to look further than the latest release.

[releases]: https://github.com/otsaloma/nfoview/releases
