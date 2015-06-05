NFO Viewer
==========

NFO Viewer is a simple viewer for NFO files, which are "ASCII" art in
the CP437 codepage. The advantages of using NFO Viewer instead of a text
editor are preset font and encoding settings, automatic window size and
clickable hyperlinks.

NFO Viewer is free software released under the GNU General Public
License (GPL), see the file `COPYING` for details.

Dependencies
============

NFO Viewer requires [Python][1] 3.2 or greater, [PyGObject][2] 3.0.0 or
greater and [GTK+][3] 3.12 or greater. [Terminus font][4] is recommended
and used by default.

[1]: http://www.python.org/
[2]: http://wiki.gnome.org/Projects/PyGObject
[3]: http://www.gtk.org/
[4]: http://terminus-font.sourceforge.net/

Terminus font is used by default because it renders drawing characters
taller than text characters. You can use any other fixed width font that
has support for the necessary CP437 drawing characters (e.g. DejaVu Sans
Mono), but with them you need to decrease the line-spacing (to a
negative value that depends on the font and font size) in order to
remove blank space between adjacent lines of drawing characters.

Running
=======

To try NFO Viewer from the source directory without installation, use
command `bin/nfoview`. For installing NFO Viewer, see the file
`INSTALL.md`.

<br>[![Gitter](https://badges.gitter.im/Join%20Chat.svg)](https://gitter.im/otsaloma/nfoview)
