# Copyright (C) 2007 Osmo Salomaa
#
# This file is part of NFO Viewer.
#
# NFO Viewer is free software: you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free Software
# Foundation, either version 3 of the License, or (at your option) any later
# version.
#
# NFO Viewer is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR
# A PARTICULAR PURPOSE. See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with
# NFO Viewer. If not, see <http://www.gnu.org/licenses/>.

import gtk
import nfoview


class TestModule(nfoview.TestCase):

    delete_event = gtk.gdk.Event(gtk.gdk.DELETE)

    def setup_method(self, method):

        self.gtk_main = gtk.main
        self.gtk_main_quit = gtk.main_quit
        gtk.main = lambda *args: None
        gtk.main_quit = lambda *args: None
        nfoview.main.windows = []

    def teardown_method(self, method):

        for window in nfoview.main.windows:
            window.emit("delete-event", self.delete_event)
        gtk.main = self.gtk_main
        gtk.main_quit = self.gtk_main_quit

    def test__on_window_delete_event(self):

        nfoview.main.open_window(self.get_nfo_file())
        nfoview.main.open_window(self.get_nfo_file())
        for window in nfoview.main.windows:
            window.emit("delete-event", self.delete_event)

    def test_open_window(self):

        nfoview.main.open_window()
        nfoview.main.open_window(self.get_nfo_file())
        assert len(nfoview.main.windows) == 2

    def test_main(self):

        nfoview.main.main(())
        paths = (
            self.get_nfo_file(),
            self.get_nfo_file(),
            self.get_nfo_file() + "x",)
        nfoview.main.main(paths)
        assert len(nfoview.main.windows) == 3
