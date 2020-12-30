NFO Viewer
==========

[![Test](https://github.com/otsaloma/nfoview/workflows/Test/badge.svg)](https://github.com/otsaloma/nfoview/actions)
[![Packages](https://repology.org/badge/tiny-repos/nfoview.svg)](https://repology.org/metapackage/nfoview)
[![Flathub](https://img.shields.io/badge/download-flathub-blue.svg)](https://flathub.org/apps/details/io.otsaloma.nfoview)
[![Gitter](https://badges.gitter.im/Join%20Chat.svg)](https://gitter.im/otsaloma/nfoview)

NFO Viewer is a simple viewer for NFO files, which are "ASCII" art in
the CP437 codepage. The advantages of using NFO Viewer instead of a text
editor are preset font and encoding settings, automatic window size and
clickable hyperlinks.

## Installing

### Linux

#### Packages

NFO Viewer is packaged for most of the popular [distros][], so easiest
is to install via your distro's package management. If not packaged for
your distro or you need a newer version than packaged, read below on how
to install from Flatpak or the source code.

[distros]: https://repology.org/metapackage/nfoview

#### Flatpak

Stable releases are available via [Flathub][].

The development version can be installed by running command `make
install` under the `flatpak` directory. You need make, flatpak-builder
and gettext to build the Flatpak.

[Flathub]: https://flathub.org/apps/details/io.otsaloma.nfoview

#### Source

NFO Viewer requires Python ≥ 3.2, PyGObject ≥ 3.0.0 and GTK ≥ 3.12. You
also need a font that supports the kinds of glyphs commonly used in NFO
files: Cascadia Code is a good choice and used by NFO Viewer by default,
if available. During installation you will also need gettext. On
Debian/Ubuntu you can install these with the following command.

    sudo apt install fonts-cascadia-code \
                     gettext \
                     gir1.2-gtk-3.0 \
                     python3 \
                     python3-gi

Then, to install NFO Viewer, run command

    sudo python3 setup.py install --prefix=/usr/local

### Windows

Windows installers are built irregularly, see [releases][].

[releases]: https://github.com/otsaloma/nfoview/releases
