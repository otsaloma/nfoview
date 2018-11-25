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

from gi.repository import Gtk

__all__ = ("PreferencesDialog",)


class PreferencesDialog(nfoview.BuilderDialog):

    _widgets = [
        "bg_color_button",
        "bg_color_label",
        "fg_color_button",
        "fg_color_label",
        "font_button",
        "line_spacing_spin",
        "link_color_button",
        "link_color_label",
        "scheme_combo",
        "vlink_color_button",
        "vlink_color_label",
    ]

    def __init__(self, parent):
        nfoview.BuilderDialog.__init__(self, "preferences-dialog.ui")
        self._init_font_button()
        self._init_scheme_combo()
        self._init_values()
        self.set_transient_for(parent)
        self.set_default_response(Gtk.ResponseType.CLOSE)

    def _get_windows(self):
        return nfoview.app.get_windows() if hasattr(nfoview, "app") else []

    def _init_font_button(self):
        def monospace(family, *args, **kwargs):
            return family.is_monospace()
        self._font_button.set_filter_func(monospace, None)

    def _init_scheme_combo(self):
        self._scheme_combo.clear()
        store = Gtk.ListStore(object, str)
        self._scheme_combo.set_model(store)
        renderer = Gtk.CellRendererText()
        self._scheme_combo.pack_start(renderer, expand=True)
        self._scheme_combo.add_attribute(renderer, "text", 1)
        for scheme in nfoview.schemes.get_all():
            store.append((scheme, scheme.label))

    def _init_values(self):
        self._font_button.set_font(nfoview.conf.font)
        pixels = nfoview.conf.pixels_above_lines
        self._line_spacing_spin.set_value(pixels)
        store = self._scheme_combo.get_model()
        for i, (scheme, label) in enumerate(store):
            if scheme.name == nfoview.conf.color_scheme:
                self._scheme_combo.set_active(i)
                self._update_color_buttons(scheme)
        self._update_sensitivities()

    def _on_bg_color_button_color_set(self, color_button):
        color = color_button.get_rgba()
        color = nfoview.util.rgba_to_hex(color)
        nfoview.conf.background_color = color
        scheme = nfoview.schemes.get("custom")
        scheme.background = color
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

    def _on_font_button_font_set(self, font_button):
        nfoview.conf.font = font_button.get_font()
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
        store = combo_box.get_model()
        index = combo_box.get_active()
        scheme = store[index][0]
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
        self._bg_color_label.set_sensitive(sensitive)
        self._fg_color_button.set_sensitive(sensitive)
        self._fg_color_label.set_sensitive(sensitive)
        self._link_color_button.set_sensitive(sensitive)
        self._link_color_label.set_sensitive(sensitive)
        self._vlink_color_button.set_sensitive(sensitive)
        self._vlink_color_label.set_sensitive(sensitive)
