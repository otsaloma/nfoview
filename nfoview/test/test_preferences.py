# -*- coding: utf-8 -*-

# Copyright (C) 2008 Osmo Salomaa
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

from gi.repository import Gdk
from gi.repository import Gtk


class TestPreferencesDialog(nfoview.TestCase):

    def run_dialog(self):
        """
        Run the dialog.

        Args:
            self: (todo): write your description
        """
        self.dialog.run()

    def setup_method(self, method):
        """
        Setup the method

        Args:
            self: (todo): write your description
            method: (str): write your description
        """
        self.dialog = nfoview.PreferencesDialog(Gtk.Window())
        self.rgba = Gdk.RGBA(red=1, green=0, blue=1)

    def test__on_bg_color_button_color_set(self):
        """
        Set the color_set

        Args:
            self: (todo): write your description
        """
        store = self.dialog._scheme_combo.get_model()
        self.dialog._scheme_combo.set_active(len(store)-1)
        self.dialog._bg_color_button.set_rgba(self.rgba)
        self.dialog._bg_color_button.emit("color-set")

    def test__on_fg_color_button_color_set(self):
        """
        Set the color_set.

        Args:
            self: (todo): write your description
        """
        store = self.dialog._scheme_combo.get_model()
        self.dialog._scheme_combo.set_active(len(store)-1)
        self.dialog._fg_color_button.set_rgba(self.rgba)
        self.dialog._fg_color_button.emit("color-set")

    def test__on_font_button_font_set(self):
        """
        Set the font font button changed.

        Args:
            self: (todo): write your description
        """
        self.dialog._font_button.set_font("monospace 8")
        self.dialog._font_button.emit("font-set")

    def test__on_line_spacing_spin_value_changed(self):
        """
        Changes the value of the value has changed value

        Args:
            self: (todo): write your description
        """
        self.dialog._line_spacing_spin.set_value(-3)
        self.dialog._line_spacing_spin.set_value(+3)

    def test__on_link_color_button_color_set(self):
        """
        Set the color_set_button

        Args:
            self: (todo): write your description
        """
        store = self.dialog._scheme_combo.get_model()
        self.dialog._scheme_combo.set_active(len(store)-1)
        self.dialog._link_color_button.set_rgba(self.rgba)
        self.dialog._link_color_button.emit("color-set")

    def test__on_scheme_combo_changed(self):
        """
        Update the scheme scheme

        Args:
            self: (todo): write your description
        """
        store = self.dialog._scheme_combo.get_model()
        for i in range(len(store)):
            self.dialog._scheme_combo.set_active(i)

    def test__on_vlink_color_button_color_set(self):
        """
        Update the color_color_button_set_color

        Args:
            self: (todo): write your description
        """
        store = self.dialog._scheme_combo.get_model()
        self.dialog._scheme_combo.set_active(len(store)-1)
        self.dialog._vlink_color_button.set_rgba(self.rgba)
        self.dialog._vlink_color_button.emit("color-set")
