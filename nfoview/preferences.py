# Copyright (C) 2008-2009 Osmo Salomaa
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

import gtk.glade
import nfoview
import os
import pango

__all__ = ("PreferencesDialog",)


class PreferencesDialog(object):

    def __getattr__(self, name):

        # Allow others to think this class is a dialog.
        return getattr(self._dialog, name)

    def __init__(self, parent):

        path = os.path.join(nfoview.DATA_DIR, "preferences-dialog.ui")
        builder = gtk.Builder()
        builder.add_from_file(path)
        get_object = builder.get_object
        self._bg_color_button = get_object("bg_color_button")
        self._bg_color_label = get_object("bg_color_label")
        self._dialog = get_object("dialog")
        self._fg_color_button = get_object("fg_color_button")
        self._fg_color_label = get_object("fg_color_label")
        self._font_button = get_object("font_button")
        self._line_spacing_spin = get_object("line_spacing_spin")
        self._link_color_button = get_object("link_color_button")
        self._link_color_label = get_object("link_color_label")
        self._scheme_combo = get_object("scheme_combo")
        self._vlink_color_button = get_object("vlink_color_button")
        self._vlink_color_label = get_object("vlink_color_label")

        self._init_scheme_combo()
        self._init_values()
        self._init_signal_handlers()
        self._init_sizes()
        self.set_transient_for(parent)

    def _init_scheme_combo(self):
        """Initialize the color scheme combo box."""

        self._scheme_combo.clear()
        store = gtk.ListStore(object)
        self._scheme_combo.set_model(store)
        renderer = gtk.CellRendererText()
        self._scheme_combo.pack_start(renderer, True)
        store = self._scheme_combo.get_model()
        for scheme in nfoview.schemes.get_color_schemes():
            store.append([scheme])
        def set_label(layout, renderer, store, itr):
            renderer.props.text = store.get_value(itr, 0).label
        self._scheme_combo.set_cell_data_func(renderer, set_label)

    def _init_signal_handlers(self):
        """Initialize signal handlers."""

        callback = self._on_font_button_font_set
        self._font_button.connect("font-set", callback)
        callback = self._on_line_spacing_spin_value_changed
        self._line_spacing_spin.connect("value-changed", callback)
        callback = self._on_scheme_combo_changed
        self._scheme_combo.connect("changed", callback)
        callback = self._on_fg_color_button_color_set
        self._fg_color_button.connect("color-set", callback)
        callback = self._on_bg_color_button_color_set
        self._bg_color_button.connect("color-set", callback)
        callback = self._on_link_color_button_color_set
        self._link_color_button.connect("color-set", callback)
        callback = self._on_vlink_color_button_color_set
        self._vlink_color_button.connect("color-set", callback)

    def _init_sizes(self):
        """Initialize widget sizes."""

        label = gtk.Label("Some Long Name Font Family  12")
        self._font_button.set_size_request(label.size_request()[0], -1)

    def _init_values(self):
        """Initialize default values for widgets."""

        self._font_button.set_font_name(nfoview.conf.font)
        self._line_spacing_spin.set_value(nfoview.conf.pixels_above_lines)
        store = self._scheme_combo.get_model()
        for i, (scheme,) in enumerate(store):
            if scheme.name == nfoview.conf.color_scheme:
                self._scheme_combo.set_active(i)
        index = self._scheme_combo.get_active()
        scheme = store[index][0]
        self._update_color_buttons(scheme)
        self._set_sensitivities()

    def _on_bg_color_button_color_set(self, color_button):
        """Save the new color and update window and its view."""

        color = color_button.get_color()
        string = nfoview.util.gdk_color_to_hex(color)
        nfoview.conf.background_color = string
        nfoview.schemes.CustomScheme.background = color
        for window in nfoview.main.windows:
            window.view.update_colors()

    def _on_fg_color_button_color_set(self, color_button):
        """Save the new color and update window and its view."""

        color = color_button.get_color()
        string = nfoview.util.gdk_color_to_hex(color)
        nfoview.conf.foreground_color = string
        nfoview.schemes.CustomScheme.foreground = color
        for window in nfoview.main.windows:
            window.view.update_colors()

    def _on_font_button_font_set(self, font_button):
        """Save the new font and update window and its view."""

        nfoview.conf.font = font_button.get_font_name()
        font_desc = pango.FontDescription(nfoview.conf.font)
        for window in nfoview.main.windows:
            window.view.modify_font(font_desc)

    def _on_link_color_button_color_set(self, color_button):
        """Save the new color and update window and its view."""

        color = color_button.get_color()
        string = nfoview.util.gdk_color_to_hex(color)
        nfoview.conf.link_color = string
        nfoview.schemes.CustomScheme.link = color
        for window in nfoview.main.windows:
            window.view.update_colors()

    def _on_scheme_combo_changed(self, combo_box):
        """Save the new color scheme and update window and its view."""

        store = combo_box.get_model()
        index = combo_box.get_active()
        scheme = store[index][0]
        nfoview.conf.color_scheme = scheme.name
        self._update_color_buttons(scheme)
        for window in nfoview.main.windows:
            window.view.update_colors()
        self._set_sensitivities()

    def _on_line_spacing_spin_value_changed(self, spin_button):
        """Save the new line-spacing and update window and its view."""

        pixels = spin_button.get_value_as_int()
        nfoview.conf.pixels_above_lines = pixels
        for window in nfoview.main.windows:
            window.view.set_pixels_above_lines(pixels)

    def _on_vlink_color_button_color_set(self, color_button):
        """Save the new color and update window and its view."""

        color = color_button.get_color()
        string = nfoview.util.gdk_color_to_hex(color)
        nfoview.conf.visited_link_color = string
        nfoview.schemes.CustomScheme.visited_link = color
        for window in nfoview.main.windows:
            window.view.update_colors()

    def _set_sensitivities(self):
        """Set the sensitivities of widgets."""

        sensitive = (nfoview.conf.color_scheme == "custom")
        self._fg_color_button.set_sensitive(sensitive)
        self._fg_color_label.set_sensitive(sensitive)
        self._bg_color_button.set_sensitive(sensitive)
        self._bg_color_label.set_sensitive(sensitive)
        self._link_color_button.set_sensitive(sensitive)
        self._link_color_label.set_sensitive(sensitive)
        self._vlink_color_button.set_sensitive(sensitive)
        self._vlink_color_label.set_sensitive(sensitive)

    def _update_color_buttons(self, scheme):
        """Set color button colors to match those of scheme."""

        self._fg_color_button.set_color(scheme.foreground)
        self._bg_color_button.set_color(scheme.background)
        self._link_color_button.set_color(scheme.link)
        self._vlink_color_button.set_color(scheme.visited_link)
