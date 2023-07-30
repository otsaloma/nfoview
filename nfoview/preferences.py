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

from gi.repository import GObject
from gi.repository import Gtk
from nfoview.i18n import _


def boxwrap(widget):
    # Needed to get widget natural-size left-aligned in grid.
    box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
    box.append(widget)
    return box

def build_label(text):
    label = Gtk.Label.new(text)
    label.add_css_class("dim-label")
    label.set_xalign(1)
    return label


class PreferencesDialog(Gtk.Dialog):

    def __init__(self, parent):
        GObject.GObject.__init__(self, use_header_bar=True)
        self.set_resizable(False)
        self.set_title(_("Preferences"))
        self.set_transient_for(parent)
        grid = Gtk.Grid()
        grid.set_column_spacing(18)
        grid.set_margin_bottom(18)
        grid.set_margin_end(18)
        grid.set_margin_start(18)
        grid.set_margin_top(18)
        grid.set_row_homogeneous(True)
        grid.set_row_spacing(12)

        # Font
        self._font_label = build_label(_("Font"))
        self._font_button = Gtk.FontButton()
        def monospace(family, *args, **kwargs):
            return family.is_monospace()
        self._font_button.set_filter_func(monospace, None)
        self._font_button.set_font(nfoview.conf.font)
        self._font_button.connect("font-set", self._on_font_button_font_set)
        grid.attach(self._font_label, 0, 0, 1, 1)
        grid.attach(boxwrap(self._font_button), 1, 0, 1, 1)

        # Line-spacing
        self._line_spacing_label = build_label(_("Line-spacing"))
        self._line_spacing_spin = Gtk.SpinButton.new_with_range(-99, 99, 1)
        self._line_spacing_spin.set_value(nfoview.conf.pixels_above_lines)
        self._line_spacing_spin.connect("value-changed", self._on_line_spacing_spin_value_changed)
        grid.attach(self._line_spacing_label, 0, 1, 1, 1)
        grid.attach(boxwrap(self._line_spacing_spin), 1, 1, 1, 1)

        # Color scheme
        self._scheme_label = build_label(_("Color scheme"))
        self._scheme_combo = Gtk.ComboBoxText.new()
        for i, scheme in enumerate(nfoview.schemes.get_all()):
            self._scheme_combo.append_text(scheme.label)
            if scheme.name == nfoview.conf.color_scheme:
                self._scheme_combo.set_active(i)
        self._scheme_combo.connect("changed", self._on_scheme_combo_changed)
        grid.attach(self._scheme_label, 0, 2, 1, 1)
        grid.attach(boxwrap(self._scheme_combo), 1, 2, 1, 1)

        # Foreground
        self._fg_color_label = build_label(_("Foreground"))
        self._fg_color_button = Gtk.ColorButton()
        color = nfoview.util.hex_to_rgba(nfoview.conf.foreground_color)
        self._fg_color_button.set_rgba(color)
        self._fg_color_button.connect("color-set", self._on_fg_color_button_color_set)
        grid.attach(self._fg_color_label, 0, 3, 1, 1)
        grid.attach(boxwrap(self._fg_color_button), 1, 3, 1, 1)

        # Background
        self._bg_color_label = build_label(_("Background"))
        self._bg_color_button = Gtk.ColorButton()
        color = nfoview.util.hex_to_rgba(nfoview.conf.background_color)
        self._bg_color_button.set_rgba(color)
        self._bg_color_button.connect("color-set", self._on_bg_color_button_color_set)
        grid.attach(self._bg_color_label, 0, 4, 1, 1)
        grid.attach(boxwrap(self._bg_color_button), 1, 4, 1, 1)

        # Link
        self._link_color_label = build_label(_("Link"))
        self._link_color_button = Gtk.ColorButton()
        color = nfoview.util.hex_to_rgba(nfoview.conf.link_color)
        self._link_color_button.set_rgba(color)
        self._link_color_button.connect("color-set", self._on_link_color_button_color_set)
        grid.attach(self._link_color_label, 0, 5, 1, 1)
        grid.attach(boxwrap(self._link_color_button), 1, 5, 1, 1)

        # Visited link
        self._vlink_color_label = build_label(_("Visited link"))
        self._vlink_color_button = Gtk.ColorButton()
        color = nfoview.util.hex_to_rgba(nfoview.conf.visited_link_color)
        self._vlink_color_button.set_rgba(color)
        self._vlink_color_button.connect("color-set", self._on_vlink_color_button_color_set)
        grid.attach(self._vlink_color_label, 0, 6, 1, 1)
        grid.attach(boxwrap(self._vlink_color_button), 1, 6, 1, 1)

        self._update_sensitivities()
        self.set_child(grid)
        self.show()

    def _get_windows(self):
        return nfoview.app.get_windows() if hasattr(nfoview, "app") else []

    def _on_bg_color_button_color_set(self, color_button):
        color = color_button.get_rgba()
        color = nfoview.util.rgba_to_hex(color)
        nfoview.conf.background_color = color
        scheme = nfoview.schemes.get("custom")
        scheme.background = color
        for window in self._get_windows():
            window.view.update_style()

    def _on_font_button_font_set(self, font_button):
        nfoview.conf.font = font_button.get_font()
        for window in self._get_windows():
            window.view.update_style()

    def _on_fg_color_button_color_set(self, color_button):
        color = color_button.get_rgba()
        color = nfoview.util.rgba_to_hex(color)
        nfoview.conf.foreground_color = color
        scheme = nfoview.schemes.get("custom")
        scheme.foreground = color
        for window in self._get_windows():
            window.view.update_style()

    def _on_line_spacing_spin_value_changed(self, spin_button):
        pixels = spin_button.get_value_as_int()
        nfoview.conf.pixels_above_lines = pixels
        for window in self._get_windows():
            window.view.set_pixels_above_lines(pixels)

    def _on_link_color_button_color_set(self, color_button):
        color = color_button.get_rgba()
        color = nfoview.util.rgba_to_hex(color)
        nfoview.conf.link_color = color
        scheme = nfoview.schemes.get("custom")
        scheme.link = color
        for window in self._get_windows():
            window.view.update_style()

    def _on_scheme_combo_changed(self, combo_box):
        index = combo_box.get_active()
        scheme = nfoview.schemes.get_all()[index]
        nfoview.conf.color_scheme = scheme.name
        self._update_color_buttons(scheme)
        for window in self._get_windows():
            window.view.update_style()
        self._update_sensitivities()

    def _on_vlink_color_button_color_set(self, color_button):
        color = color_button.get_rgba()
        color = nfoview.util.rgba_to_hex(color)
        nfoview.conf.visited_link_color = color
        scheme = nfoview.schemes.get("custom")
        scheme.vlink = color
        for window in self._get_windows():
            window.view.update_style()

    def _update_color_buttons(self, scheme):
        rgba = nfoview.util.hex_to_rgba
        self._bg_color_button.set_rgba(rgba(scheme.background))
        self._fg_color_button.set_rgba(rgba(scheme.foreground))
        self._link_color_button.set_rgba(rgba(scheme.link))
        self._vlink_color_button.set_rgba(rgba(scheme.visited_link))

    def _update_sensitivities(self):
        sensitive = (nfoview.conf.color_scheme == "custom")
        self._bg_color_button.set_sensitive(sensitive)
        self._fg_color_button.set_sensitive(sensitive)
        self._link_color_button.set_sensitive(sensitive)
        self._vlink_color_button.set_sensitive(sensitive)
