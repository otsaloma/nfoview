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


class TestTextView(nfoview.TestCase):

    def run_window(self):
        """
        Run the gtk window.

        Args:
            self: (todo): write your description
        """
        window = Gtk.Window()
        window.connect("delete-event", Gtk.main_quit)
        window.set_position(Gtk.WindowPosition.CENTER)
        window.set_default_size(500, 500)
        window.add(self.view)
        window.show_all()
        Gtk.main()

    def setup_method(self, method):
        """
        Setup the view to the given view

        Args:
            self: (todo): write your description
            method: (str): write your description
        """
        self.view = nfoview.TextView()
        text = "testing...\nhttps://otsaloma.io/nfoview/"
        self.view.set_text(text)

    def test_get_text(self):
        """
        The test text

        Args:
            self: (todo): write your description
        """
        self.view.set_text("test\ntest")
        text = self.view.get_text()
        # set_text adds a final newline.
        assert text == "test\ntest\n"

    def test_set_text(self):
        """
        Sets the text to the test text

        Args:
            self: (todo): write your description
        """
        self.view.set_text("test\ntest")
        text = self.view.get_text()
        # set_text adds a final newline.
        assert text == "test\ntest\n"

    def test_update_style(self):
        """
        Update the style of the view

        Args:
            self: (todo): write your description
        """
        self.view.update_style()
        tags = self.view._link_tags
        self.view._link_tags = []
        self.view._visited_link_tags = tags
        self.view.update_style()
