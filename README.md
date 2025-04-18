NFO Viewer
==========

[![Packages](https://repology.org/badge/tiny-repos/nfoview.svg)](https://repology.org/project/nfoview/versions)
[![Flathub](https://img.shields.io/badge/download-flathub-blue.svg)](https://flathub.org/apps/io.otsaloma.nfoview)

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

NFO Viewer requires Python ≥ 3.8, PyGObject ≥ 3.0.0 and GTK ≥ 4.0. You
also need a font that supports the kinds of glyphs commonly used in NFO
files: Cascadia Mono is a good choice and used by NFO Viewer by default,
if available. During installation you will also need gettext. On
Debian/Ubuntu you can install these with the following command.

    sudo apt install fonts-cascadia-code \
                     gettext \
                     gir1.2-gtk-4.0 \
                     gir1.2-pango-1.0 \
                     python3 \
                     python3-cairo \
                     python3-dev \
                     python3-gi

Then, to install NFO Viewer, run commands

    make PREFIX=/usr/local build
    sudo make PREFIX=/usr/local install

### Windows

Windows installers are no longer built due to bad tooling, bad results,
lack of time and lack of motivation. The latest version available for
Windows is [1.23][].

[1.23]: https://github.com/otsaloma/nfoview/releases/tag/1.23
