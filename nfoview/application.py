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

import nfoview
import sys
import traceback

from gi.repository import Gio
from gi.repository import GObject
from gi.repository import Gtk

__all__ = ("Application",)


class Application(Gtk.Application):

    def __init__(self, paths):
        GObject.GObject.__init__(self)
        self.set_application_id("io.otsaloma.nfoview")
        self.set_flags(Gio.ApplicationFlags.NON_UNIQUE)
        self.connect("activate", self._on_activate, paths)
        self.connect("shutdown", self._on_shutdown)

    def _on_activate(self, app, paths):
        for path in sorted(paths):
            self.open_window(path)
        if not self.get_windows():
            # If no arguments were given, or none of them exist,
            # open one blank window.
            self.open_window()

    def _on_shutdown(self, app):
        nfoview.conf.write()

    def open_window(self, path=None):
        try:
            window = nfoview.Window(path)
            self.add_window(window)
            window.present()
        except Exception as error:
            print("Failed to open {!r}: {!s}"
                  .format(path, error),
                  file=sys.stderr)
            traceback.print_exc()
