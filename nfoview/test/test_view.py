# -*- coding: utf-8 -*-

# Copyright (C) 2005-2009,2011 Osmo Salomaa
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

from gi.repository import Gtk


class TestTextView(nfoview.TestCase):

    def run_window(self):
        window = Gtk.Window()
        window.connect("delete-event", Gtk.main_quit)
        window.set_position(Gtk.WindowPosition.CENTER)
        window.set_default_size(500, 500)
        window.add(self.view)
        window.show_all()
        Gtk.main()

    def setup_method(self, method):
        self.view = nfoview.TextView()
        text = "testing...\nhttp://home.gna.org/nfoview"
        self.view.set_text(text)

    def test_get_text(self):
        self.view.set_text("test\ntest")
        text = self.view.get_text()
        # set_text adds a final newline.
        assert text == "test\ntest\n"

    def test_set_text(self):
        self.view.set_text("test\ntest")
        text = self.view.get_text()
        # set_text adds a final newline.
        assert text == "test\ntest\n"

    def test_update_colors(self):
        self.view.update_colors()
        tags = self.view._link_tags
        self.view._link_tags = []
        self.view._visited_link_tags = tags
        self.view.update_colors()

    def test_update_colors__value_error(self):
        nfoview.conf.color_scheme = "xxx"
        self.view.update_colors()
