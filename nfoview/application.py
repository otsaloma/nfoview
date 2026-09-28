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
import traceback

from gi.repository import Gio
from gi.repository import Gtk

class Application(Gtk.Application):

    def __init__(self):
        super().__init__(application_id="io.otsaloma.nfoview",
                         flags=Gio.ApplicationFlags.HANDLES_OPEN)
        self.connect("activate", self._on_activate)
        self.connect("open", self._on_open)
        self.connect("shutdown", self._on_shutdown)
        self.connect("startup", self._on_startup)

    def _init_theme(self):
        theme = nfoview.conf.theme
        if theme == "system": return
        settings = Gtk.Settings.get_default()
        if settings.find_property("gtk-interface-color-scheme") is None: return
        settings.set_property("gtk-interface-color-scheme",
                              Gtk.InterfaceColorScheme.DARK
                              if theme == "dark"
                              else Gtk.InterfaceColorScheme.LIGHT)

        # Themes with separate dark stylesheets
        # are only reloaded when the theme name changes.
        settings.notify("gtk-theme-name")

    def _on_activate(self, app):
        self.open_window()

    def _on_open(self, app, files, n_files, hint):
        paths = sorted(filter(None, (x.get_path() for x in files)))
        windows = [self.open_window(x) for x in paths]
        if not any(windows):
            # If none of the files could be opened,
            # open one blank window.
            self.open_window()

    def _on_shutdown(self, app):
        nfoview.conf.write()

    def _on_startup(self, app):
        try:
            self._init_theme()
        except Exception:
            traceback.print_exc()

    def open_window(self, path=None):
        try:
            window = nfoview.Window(path)
            self.add_window(window)
            window.present()
            return window
        except Exception as error:
            print(f"Failed to open {path!r}: {error!s}")
            traceback.print_exc()
