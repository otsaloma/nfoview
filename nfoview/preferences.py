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

def attach_row(grid, row, text, widget):
    label = Gtk.Label.new(text)
    label.add_css_class("dim-label")
    label.set_xalign(1)
    grid.attach(label, 0, row, 1, 1)
    # Keep the widget at its natural size instead of filling the cell.
    widget.set_halign(Gtk.Align.START)
    grid.attach(widget, 1, row, 1, 1)

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
        self._font_button = Gtk.FontButton()
        def monospace(family, *args, **kwargs):
            return family.is_monospace()
        self._font_button.set_filter_func(monospace, None)
        self._font_button.set_font(nfoview.conf.font)
        self._font_button.connect("font-set", self._on_font_button_font_set)
        attach_row(grid, 0, _("Font"), self._font_button)

        # Line-spacing
        self._line_spacing_spin = Gtk.SpinButton.new_with_range(-99, 99, 1)
        self._line_spacing_spin.set_value(nfoview.conf.pixels_above_lines)
        self._line_spacing_spin.connect("value-changed", self._on_line_spacing_spin_value_changed)
        attach_row(grid, 1, _("Line-spacing"), self._line_spacing_spin)

        # Color scheme
        self._scheme_combo = Gtk.ComboBoxText.new()
        for i, scheme in enumerate(nfoview.schemes.get_all()):
            self._scheme_combo.append_text(scheme.label)
            if scheme.name == nfoview.conf.color_scheme:
                self._scheme_combo.set_active(i)
        self._scheme_combo.connect("changed", self._on_scheme_combo_changed)
        attach_row(grid, 2, _("Color scheme"), self._scheme_combo)

        # Colors of the custom color scheme
        self._color_buttons = {}
        for row, (text, option, attribute) in enumerate((
            (_("Foreground"),   "foreground_color",   "foreground"),
            (_("Background"),   "background_color",   "background"),
            (_("Link"),         "link_color",         "link"),
            (_("Visited link"), "visited_link_color", "visited_link"),
        ), start=3):
            button = Gtk.ColorButton()
            color = getattr(nfoview.conf, option)
            button.set_rgba(nfoview.util.hex_to_rgba(color))
            button.connect("color-set", self._on_color_button_color_set, option, attribute)
            attach_row(grid, row, text, button)
            self._color_buttons[attribute] = button

        # Export Scaling
        self._export_scale_spin = Gtk.SpinButton.new_with_range(1, 5, 0.5)
        self._export_scale_spin.set_value(nfoview.conf.export_scale)
        self._export_scale_spin.connect("value-changed", self._on_export_scale_spin_value_changed)
        attach_row(grid, 7, _("Export to PNG scaling"), self._export_scale_spin)

        self._update_sensitivities()
        self.set_child(grid)
        self.show()

    def _get_windows(self):
        return nfoview.app.get_windows() if nfoview.app else []

    def _on_color_button_color_set(self, color_button, option, attribute):
        color = nfoview.util.rgba_to_hex(color_button.get_rgba())
        setattr(nfoview.conf, option, color)
        setattr(nfoview.schemes.Custom, attribute, color)
        self._update_views()

    def _on_export_scale_spin_value_changed(self, spin_button):
        nfoview.conf.export_scale = spin_button.get_value()

    def _on_font_button_font_set(self, font_button):
        nfoview.conf.font = font_button.get_font()
        self._update_views()

    def _on_line_spacing_spin_value_changed(self, spin_button):
        pixels = spin_button.get_value_as_int()
        nfoview.conf.pixels_above_lines = pixels
        for window in self._get_windows():
            window.view.set_pixels_above_lines(pixels)

    def _on_scheme_combo_changed(self, combo_box):
        index = combo_box.get_active()
        scheme = nfoview.schemes.get_all()[index]
        nfoview.conf.color_scheme = scheme.name
        self._update_color_buttons(scheme)
        self._update_views()
        self._update_sensitivities()

    def _update_color_buttons(self, scheme):
        for attribute, button in self._color_buttons.items():
            color = getattr(scheme, attribute)
            button.set_rgba(nfoview.util.hex_to_rgba(color))

    def _update_sensitivities(self):
        sensitive = (nfoview.conf.color_scheme == "custom")
        for button in self._color_buttons.values():
            button.set_sensitive(sensitive)

    def _update_views(self):
        for window in self._get_windows():
            window.view.update_style()
