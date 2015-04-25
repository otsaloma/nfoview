# -*- coding: utf-8 -*-

# Copyright (C) 2005 Osmo Salomaa
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

from gi.repository import Gtk


class TestWindow(nfoview.TestCase):

    def run_window(self):
        self.window.show()
        self.window.connect("delete-event", Gtk.main_quit)
        Gtk.main()

    def setup_method(self, method):
        self.window = nfoview.Window(self.new_nfo_file())

    def test_open_file__blank_lines(self):
        path = self.new_nfo_file()
        with open(path, "a") as f:
            f.write("\n\n\n")
        self.window.open_file(path)

    def test_open_file__odd_lines(self):
        path = self.new_nfo_file()
        with open(path, "w") as f:
            f.write("a\n\na\n\n")
        self.window.open_file(path)

    def test_resize_to_text__blank(self):
        self.window = nfoview.Window()
        self.window.resize_to_text()

    def test_resize_to_text__long_file(self):
        path = self.new_nfo_file()
        with open(path, "w") as f:
            f.write("aaa\n" * 100)
        self.window.open_file(path)
        self.window.resize_to_text()

    def test_resize_to_text__long_lines(self):
        path = self.new_nfo_file()
        with open(path, "w") as f:
            f.write("aaa " * 100)
        self.window.open_file(path)
        self.window.resize_to_text()
