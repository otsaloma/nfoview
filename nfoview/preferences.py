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

"""Dialog for editing preferences."""

import gtk
import nfoview
import os
import pango

__all__ = ("PreferencesDialog",)


class PreferencesDialog(nfoview.BuilderDialog):

    """Dialog for editing preferences."""

    widgets = ("bg_color_button",
               "bg_color_label",
               "fg_color_button",
               "fg_color_label",
               "font_button",
               "line_spacing_spin",
               "link_color_button",
               "link_color_label",
               "scheme_combo",
               "vlink_color_button",
               "vlink_color_label",)

    def __init__(self, parent):
        """Initialize a PreferencesDialog instance."""
        path = os.path.join(nfoview.DATA_DIR, "preferences-dialog.ui")
        nfoview.BuilderDialog.__init__(self, path)
        self._init_scheme_combo()
        self._init_values()
        self._init_sizes()
        self.set_transient_for(parent)

    def _init_scheme_combo(self):
        """Initialize a model and populate the scheme combo box."""
        self._scheme_combo.clear()
        store = gtk.ListStore(object, str)
        self._scheme_combo.set_model(store)
        renderer = gtk.CellRendererText()
        self._scheme_combo.pack_start(renderer, True)
        self._scheme_combo.add_attribute(renderer, "text", 1)
        for scheme in nfoview.util.get_color_schemes():
            store.append((scheme, scheme.label))

    def _init_sizes(self):
        """Set a reasonable default size for dialog."""
        label = gtk.Label("Some Long Name Font Family  12")
        width = label.size_request()[0]
        self._font_button.set_size_request(width, -1)

    def _init_values(self):
        """Set saved default values for widgets."""
        self._font_button.set_font_name(nfoview.conf.font)
        pixels = nfoview.conf.pixels_above_lines
        self._line_spacing_spin.set_value(pixels)
        store = self._scheme_combo.get_model()
        for i, (scheme, label) in enumerate(store):
            if scheme.name == nfoview.conf.color_scheme:
                self._scheme_combo.set_active(i)
                self._update_color_buttons(scheme)
        self._update_sensitivities()

    def _on_bg_color_button_color_set(self, color_button):
        """Save the new color and update window and its view."""
        color = color_button.get_color()
        string = nfoview.util.gdk_color_to_hex(color)
        nfoview.conf.background_color = string
        scheme = nfoview.util.get_color_scheme("custom")
        scheme.background = color
        for window in nfoview.main.windows:
            window.view.update_colors()

    def _on_fg_color_button_color_set(self, color_button):
        """Save the new color and update window and its view."""
        color = color_button.get_color()
        string = nfoview.util.gdk_color_to_hex(color)
        nfoview.conf.foreground_color = string
        scheme = nfoview.util.get_color_scheme("custom")
        scheme.foreground = color
        for window in nfoview.main.windows:
            window.view.update_colors()

    def _on_font_button_font_set(self, font_button):
        """Save the new font and update window and its view."""
        nfoview.conf.font = font_button.get_font_name()
        font_desc = pango.FontDescription(nfoview.conf.font)
        for window in nfoview.main.windows:
            window.view.modify_font(font_desc)

    def _on_line_spacing_spin_value_changed(self, spin_button):
        """Save the new line-spacing and update window and its view."""
        pixels = spin_button.get_value_as_int()
        nfoview.conf.pixels_above_lines = pixels
        for window in nfoview.main.windows:
            window.view.set_pixels_above_lines(pixels)

    def _on_link_color_button_color_set(self, color_button):
        """Save the new color and update window and its view."""
        color = color_button.get_color()
        string = nfoview.util.gdk_color_to_hex(color)
        nfoview.conf.link_color = string
        scheme = nfoview.util.get_color_scheme("custom")
        scheme.link = color
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
        self._update_sensitivities()

    def _on_vlink_color_button_color_set(self, color_button):
        """Save the new color and update window and its view."""
        color = color_button.get_color()
        string = nfoview.util.gdk_color_to_hex(color)
        nfoview.conf.visited_link_color = string
        scheme = nfoview.util.get_color_scheme("custom")
        scheme.vlink = color
        for window in nfoview.main.windows:
            window.view.update_colors()

    def _update_color_buttons(self, scheme):
        """Set color button colors to match those of scheme."""
        self._bg_color_button.set_color(scheme.background)
        self._fg_color_button.set_color(scheme.foreground)
        self._link_color_button.set_color(scheme.link)
        self._vlink_color_button.set_color(scheme.visited_link)

    def _update_sensitivities(self):
        """Set the sensitivities of color buttons and labels."""
        sensitive = (nfoview.conf.color_scheme == "custom")
        self._bg_color_button.set_sensitive(sensitive)
        self._bg_color_label.set_sensitive(sensitive)
        self._fg_color_button.set_sensitive(sensitive)
        self._fg_color_label.set_sensitive(sensitive)
        self._link_color_button.set_sensitive(sensitive)
        self._link_color_label.set_sensitive(sensitive)
        self._vlink_color_button.set_sensitive(sensitive)
        self._vlink_color_label.set_sensitive(sensitive)
