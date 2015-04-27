# -*- coding: utf-8 -*-

# Copyright (C) 2015 Osmo Salomaa
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

"""Initializing and managing NFO Viewer windows."""

import gettext
import locale
import nfoview
import sys
import traceback

from gi.repository import Gio
from gi.repository import GObject
from gi.repository import Gtk

__all__ = ("Application",)


class Application(Gtk.Application):

    """Initializing and managing NFO Viewer windows."""

    def __init__(self, paths):
        """Initialize an :class:`Application` instance."""
        GObject.GObject.__init__(self)
        self.set_flags(Gio.ApplicationFlags.NON_UNIQUE)
        self.connect("activate", self._on_activate, paths)
        self.connect("shutdown", self._on_shutdown)
        self._init_gettext()

    def _init_gettext(self):
        """Initialize translation settings."""
        with nfoview.util.silent(Exception):
            # Might fail with misconfigured locales.
            locale.setlocale(locale.LC_ALL, "")
        d = nfoview.LOCALE_DIR
        with nfoview.util.silent(Exception):
            # Not available on all platforms.
            locale.bindtextdomain("nfoview", d)
            locale.textdomain("nfoview")
        gettext.bindtextdomain("nfoview", d)
        gettext.textdomain("nfoview")

    def _on_activate(self, app, paths):
        """Open windows for files given as arguments."""
        for path in sorted(paths):
            self.open_window(path)
        if not self.get_windows():
            # If no arguments were given, or none of them exist,
            # open one blank window.
            self.open_window()

    def _on_shutdown(self, app):
        """Terminate application."""
        nfoview.conf.write()

    def open_window(self, path=None):
        """Open `path` in a new window and present that window."""
        try:
            window = nfoview.Window(path)
            self.add_window(window)
            window.present()
        except Exception as error:
            print("Failed to open {}: {}"
                  .format(repr(path), str(error)),
                  file=sys.stderr)
            traceback.print_exc()
