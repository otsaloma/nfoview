# -*- coding: utf-8-unix -*-

# Copyright (C) 2008-2009,2011 Osmo Salomaa
#
# This file is part of NFO Viewer.
#
# NFO Viewer is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the
# Free Software Foundation, either version 3 of the License, or (at your
# option) any later version.
#
# NFO Viewer is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with NFO Viewer. If not, see <http://www.gnu.org/licenses/>.

import nfoview

from gi.repository import Gdk
from gi.repository import Gtk


class TestModule(nfoview.TestCase):

    def setup_method(self, method):
        nfoview.main.windows = []

    def test__on_window_delete_event(self):
        nfoview.main.open_window(self.new_nfo_file())
        nfoview.main.open_window(self.new_nfo_file())
        for window in nfoview.main.windows:
            window.emit("delete-event", Gdk.Event(Gdk.EventType.DELETE))

    def test_open_window__empty(self):
        nfoview.main.open_window()

    def test_open_window__file(self):
        nfoview.main.open_window(self.new_nfo_file())

    @nfoview.deco.monkey_patch(Gtk, "main")
    def test_main__empty(self):
        Gtk.main = lambda *args: None
        nfoview.main.main(())
        assert len(nfoview.main.windows) == 1

    @nfoview.deco.monkey_patch(Gtk, "main")
    def test_main__files(self):
        Gtk.main = lambda *args: None
        paths = (self.new_nfo_file(),
                 self.new_nfo_file(),
                 self.new_nfo_file(),)

        nfoview.main.main(paths)
        assert len(nfoview.main.windows) == 3

    @nfoview.deco.monkey_patch(Gtk, "main")
    def test_main__non_files(self):
        Gtk.main = lambda *args: None
        path = "{}.xxx".format(self.new_nfo_file())
        nfoview.main.main((path,))
        assert len(nfoview.main.windows) == 1
