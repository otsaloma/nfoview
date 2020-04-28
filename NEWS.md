2020-04-28: NFO Viewer 1.28
===========================

* Switch default font from Terminus to Cascadia Code as Terminus is
  most commonly a bitmap font, which no longer work with Pango 1.44:
  <https://gitlab.gnome.org/GNOME/pango/issues/386>
* Always fall back on the platform default monospace font
* Add Dutch translation (Heimen Stoffels)

2020-04-10: NFO Viewer 1.27.1
=============================

* Fix CSS error with the abnormal weight of the Unscii font

2019-08-09: NFO Viewer 1.27
===========================

* New app icon, as full-color and symbolic SVGs (#16)
* Use the reverse domain name "io.otsaloma.nfoview" for desktop file,
  appdata file and icons

2019-06-08: NFO Viewer 1.26.1
=============================

* Add Greek translation

2018-12-16: NFO Viewer 1.26
===========================

* Use native file dialogs when available

2018-12-12: NFO Viewer 1.25
===========================

* Add support for building a Flatpak
* Add 64x64 and 128x128 icons
* Update AppData XML file
* Fix build reproducibility (#15)
* Update translations

2018-04-22: NFO Viewer 1.24
===========================

* Fix possibly missing icon in GNOME shell on Wayland
* Update translations

2017-11-06: NFO Viewer 1.23
===========================

* Install AppData XML file under /usr/share/metainfo (#12)
* Drop build dependency on intltool (use gettext instead, #3)
* Add Donate button to about dialog
* Update translations

2017-03-18: NFO Viewer 1.22
===========================

* Fix window height calculation if line-spacing non-zero
* Fix color scheme names not translated (#10)
* Add Brazilian Portuguese translation (Ricardo Borges Jr.)
* Add Romanian translation (Nicolae Crefelean)
* Remove severely incomplete Swiss German, Italian and Simplified
  Chinese translations
* Update translations

2016-10-29: NFO Viewer 1.21
===========================

* Fix size of custom font with GTK 3.22 (#7)
* Update AppData file
* Update translations

2016-07-23: NFO Viewer 1.20
===========================

* Only show monospace fonts in the font chooser dialog
* Fix windows not closing when having multiple windows open
* Add support for releasing installers for Windows

2016-05-12: NFO Viewer 1.19
===========================

* Fix mouse cursor and links with GTK 3.20
* Use CSS for setting custom font and colors, fix selection color
  with GTK 3.20 ([#2], [#4])
* Fix default window size calculations to work better with GTK 3.20
* Don't use deprecated `Gdk.Cursor.new`
* Update preferences dialog GtkBuilder file with Glade 3.20
* Remove shadow from around the text view
* Add top and bottom margins to the text view
* Move web pages to <http://otsaloma.io/nfoview/>
* Move bugs from GNOME Bugzilla to [GitHub][1.19a]
* Update AppData file
* Update translations

[#2]: https://github.com/otsaloma/nfoview/issues/2
[#4]: https://github.com/otsaloma/nfoview/issues/4
[1.19a]: https://github.com/otsaloma/nfoview/issues

2016-01-23: NFO Viewer 1.18
===========================

* Work around a drag destination Gtk-WARNING ([#721708])

[#721708]: https://bugzilla.gnome.org/show_bug.cgi?id=721708

2015-10-11: NFO Viewer 1.17
===========================

* Improve URL detection ([#667102])
* Update translations

[#667102]: http://bugzilla.gnome.org/show_bug.cgi?id=667102

2015-05-08: NFO Viewer 1.16
===========================

* Use a header bar and a menu button in application windows
* Use a header bar for the preferences dialog
* Migrate from deprecated `Gtk.UIManager`, `Gtk.Action` etc.
  to `Gtk.Application`, `Gio.Action` etc.
* New application icon
* Use markdown for documentation files (`README` etc.)
* Bump GTK depedency to version 3.12
* Add European Portuguese translation (Pedro Albuquerque)
* Update Polish translation (Piotr Drąg)
* Move web pages from [gna.org][1.16a] to [github.io][1.16b]
* Move releases from [gna.org][1.16c] to [github.com][1.16d]
* Use [Transifex][1.16e] to manage translations
* Close [nfoview-list][1.16f] mailing list, use
  [gitter.im][1.16g] instead to reach developers
* Close [nfoview-announcements][1.16h] mailing list, use
  [RSS][1.16i] instead to be informed about new releases
  (see also e.g. [sibbell.com][1.16j])

[1.16a]: http://home.gna.org/nfoview/
[1.16b]: http://otsaloma.github.io/nfoview/
[1.16c]: http://download.gna.org/nfoview/
[1.16d]: http://github.com/otsaloma/nfoview/releases
[1.16e]: http://www.transifex.com/projects/p/nfoview/
[1.16f]: http://mail.gna.org/listinfo/nfoview-list/
[1.16g]: http://gitter.im/otsaloma/nfoview
[1.16h]: http://mail.gna.org/listinfo/nfoview-announcements/
[1.16i]: http://github.com/otsaloma/nfoview/releases.atom
[1.16j]: http://sibbell.com/

2014-11-30: NFO Viewer 1.15.1
=============================

* Fix detection of theme colors of the default color scheme
* Update French translation
* Update Turkish translation

2014-10-05: NFO Viewer 1.15
===========================

* Fix preferences dialog padding with GTK 3.14
* Fix selection background color with GTK 3.14
* Remove use of deprecated stock items, `GtkAlignment`
  and `gi.types.Boxed.__init__`
* Update French translation
* Update Turkish translation

2014-06-21: NFO Viewer 1.14
===========================

* Fix default response buttons for dialogs
* Make AppData file translatable
* Add GTK to list of dependencies in the `README` file (GTK has
  always been a dependency, its explicit mention was just forgotten
  when migrating from PyGTK to PyGObject)
* Bump GTK dependency to 3.2 or greater

2013-09-22: NFO Viewer 1.13.1
=============================

* Possibly fix default colors with some GTK themes
* Add an AppData XML file
    - <http://people.freedesktop.org/~hughsient/appdata/>
* Update French translation
* Update Turkish translation

2013-07-29: NFO Viewer 1.13
===========================

* Add action to export document as an image file (#622078)
* Apply GNOME Goal: Add keywords to application desktop files
    - <https://wiki.gnome.org/GnomeGoals/DesktopFileKeywords>
* Update Turkish translation

2013-04-15: NFO Viewer 1.12.1
=============================

* Fix error setting colors in the preferences dialog
  `TypeError: get_rgba() takes exactly 2 arguments (1 given)`

2013-04-08: NFO Viewer 1.12
===========================

* Adapt to new GTK theme color names, thus fixing the default color
  scheme that follows the GTK theme
* Fix window size calculations

2012-11-04: NFO Viewer 1.11
===========================

* Fix immediate crash resulting from bad use of `Gtk.StyleContext` on
  newer versions of PyGObject and/or GTK (#687513)
* Remove deprecated `get_data` and `set_data` calls
* Use `Gtk.Grid` for preferences dialog instead of `Gtk.Table`
* Release source tarballs only compressed as `tar.xz` (instead
  of the previous `tar.gz` and `tar.bz2`)

2011-11-13: NFO Viewer 1.10
===========================

* Migrate to Python 3, GTK 3, GNOME 3 and PyGI
* Bump Python dependency to 3.2 or greater
* Replace PyGTK dependency with PyGobject 3.0.0 or greater
* Add 48x48 and 256x256 pixel PNG icons and remove SVG icon
* Speed up text parsing and display when opening files
* Update Bulgarian translation (Svetoslav Stefanov)

2011-05-29: NFO Viewer 1.9.5
============================

* Fix opening files by drag and drop

2011-04-05: NFO Viewer 1.9.4
============================

* Fix broken inheritance of action classes, which caused
  NFO Viewer to fail to start with recent versions of (Py)GTK

2011-03-27: NFO Viewer 1.9.3
============================

* Update author email address
* Move development repository from Gitorious to GitHub
  (<https://github.com/otsaloma/nfoview>)
* Abandon use of Transifex for translations
* Add Turkish translation (Anonymous)
* Add Serbian translation (Goran Velemirov)
* Update French translation (Anonymous)

2010-10-05: NFO Viewer 1.9.2
============================

* Update Polish translation (Piotr Drąg)
* Add Russian translation (Алекс)

2010-06-26: NFO Viewer 1.9.1
============================

* Fix opening blank files (fixes #619289)
* Add Hebrew translation (Yaron Shahrabani)
* Add Hungarian translation (L. Csordas)

2010-04-25: NFO Viewer 1.9
==========================

* Make the 16x16 px icon paper two pixels wider
* Use `gtk.show_uri` to open hyperlinks
* Raise PyGTK Dependency to 2.16
* Update German translation (Christoph Wickert)
* Update Polish translation (Piotr Drąg)

2009-10-17: NFO Viewer 1.8
==========================

* Add application icon (based on logviewer icon from
  gnome-icon-theme)
* Save menu item keybindings to a GtkAccelMap rc-file in the user's
  configuration directory
* Add French translation (elgeneralmidi)
* Add Polish translation (Piotr Drąg)

2009-09-26: NFO Viewer 1.7
==========================

* Add menu item to toggle line-wrapping
* Automatically switch to wrapping lines if a line longer than 160
  characters is found in the file (the threshold is customizable in
  the configuration file)
* Fall back to "monospace" if preferred font is not found
* Fix URL-detection to be less strict
* Add Italian translation (Alessio Treglia)

2009-08-16: NFO Viewer 1.6
==========================

* Add configuration file option `text_view_max_lines` to set the
  maximum window height to an amount of lines and raise its default
  value from 40 to 45 lines
* Fix URL-detection to be more strict
* Update Simplified Chinese translation (Jonathan Ye)

2009-05-11: NFO Viewer 1.5
==========================

* Add a quit menu item to close all windows (#581091)
* Allow windows to be closed by pressing Escape (#581091)
* Update German translation (Christoph Wickert)
* Add Swiss German translation (Fabian Affolter)
* Add Bulgarian translation (Svetoslav Stefanov)

2009-04-19: NFO Viewer 1.4
==========================

* Handle files with UTF8, UTF16 and UTF32 BOMs
* Abort installation if an `intltool-merge` or `msgfmt` call fails

2009-04-05: NFO Viewer 1.3.1
============================

* Fix gettext translation system for GtkBuilder files

2009-03-15: NFO Viewer 1.3
==========================

* Add two grey low-contrast color schemes
* Remove deprecated Encoding field from the desktop file
* Use six-character hexadecimal color codes in the configuration file
* Fix `GtkWarning: GtkSpinButton: setting an adjustment with
  non-zero page size is deprecated`
* Fix open dialog file filter to list files with upper- and mixed
  case extensions as well (Simon Morgan, #572877)
* Migrate from Libglade to GtkBuilder
* Raise Python dependency to 2.5 or greater
* Raise PyGTK dependency to 2.12 or greater

2008-10-05: NFO Viewer 1.2.1
============================

* Remove misuse of assertions that broke menu item sensitivity
  updates when used with Python's optimization (`-O` switch)
* Fix `AssertionError` when installing multiple times (#12388)
* Add Simplified Chinese translation (Jonathan Ye)
* Switch version-control from svn to git

2008-05-18: NFO Viewer 1.2
==========================

* Remove mimetype installation files and use the new "text/x-nfo"
  mimetype added with freedesktop.org's shared-mime-info 0.30

2008-05-10: NFO Viewer 1.1.2
============================

* Fix `setup.py` to allow building and installing outside X
* Fix `setup.py` to run `update-desktop-database` in addition to
  `update-mime-database` if installing and `--root` not given

2008-04-30: NFO Viewer 1.1.1
============================

* Fix unavailable stock icon usage on GTK < 2.10 (#11585)

2008-01-09: NFO Viewer 1.1
==========================

* Add a menubar
* Add open-, preferences- and about dialogs
* Allow files to be opened by drag-and-drop
* Use Terminus font, size 12, by default
* Use text and background colors from GTK theme by default
* Improve detection of the default web browser
* Add an applications menu entry in the desktop file
* Change configuration file style and save the configuration file to
  `$XDG_CONFIG_HOME/nfoview` (usually `$HOME/.config/nfoview`) as per
  freedesktop.org's XDG Base Directory Specification
* Refactor code and reorganize source directory structure
