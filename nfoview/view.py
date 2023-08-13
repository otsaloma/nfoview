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
import re

from gi.repository import Gdk
from gi.repository import GObject
from gi.repository import Gtk
from gi.repository import Pango


class TextView(Gtk.TextView):

    def __init__(self):
        GObject.GObject.__init__(self)
        self._link_tags = []
        self._visited_link_tags = []
        self.set_bottom_margin(6)
        self.set_cursor_visible(False)
        self.set_editable(False)
        self.set_left_margin(6)
        self.set_pixels_above_lines(nfoview.conf.pixels_above_lines)
        self.set_pixels_below_lines(nfoview.conf.pixels_below_lines)
        self.set_right_margin(6)
        self.set_top_margin(6)
        self.set_wrap_mode(Gtk.WrapMode.NONE)
        controller = Gtk.EventControllerMotion()
        controller.set_propagation_phase(Gtk.PropagationPhase.CAPTURE)
        self.add_controller(controller)
        controller.connect("motion", self._on_motion)
        gesture = Gtk.GestureClick()
        self.add_controller(gesture)
        gesture.connect("pressed", self._on_pressed)
        self.update_style()

    def get_text(self):
        text_buffer = self.get_buffer()
        start, end = text_buffer.get_bounds()
        return text_buffer.get_text(start, end, False)

    def _insert_text(self, text):
        text_buffer = self.get_buffer()
        itr = text_buffer.get_end_iter()
        text_buffer.insert(itr, text)

    def _insert_url(self, url):
        text_buffer = self.get_buffer()
        tag = text_buffer.create_tag(None)
        tag.props.underline = Pango.Underline.SINGLE
        tag.nfoview_url = url
        itr = text_buffer.get_end_iter()
        text_buffer.insert_with_tags(itr, url, tag)
        self._link_tags.append(tag)

    def _on_motion(self, controller, x, y, user_data=None):
        window = Gtk.TextWindowType.WIDGET
        x, y = self.window_to_buffer_coords(window, x, y)
        if iter := self.get_iter_at_location(x, y):
            for tag in iter.iter.get_tags():
                if hasattr(tag, "nfoview_url"):
                    return self.set_cursor(Gdk.Cursor.new_from_name("pointer"))
        self.set_cursor(Gdk.Cursor.new_from_name("default"))

    def _on_pressed(self, gesture, n_press, x, y, user_data=None):
        text_buffer = self.get_buffer()
        if text_buffer.get_selection_bounds(): return
        window = Gtk.TextWindowType.WIDGET
        x, y = self.window_to_buffer_coords(window, x, y)
        if iter := self.get_iter_at_location(x, y):
            for tag in iter.iter.get_tags():
                if hasattr(tag, "nfoview_url"):
                    nfoview.util.show_uri(tag.nfoview_url)
                    if tag in self._link_tags:
                        self._link_tags.remove(tag)
                        self._visited_link_tags.append(tag)
                        self.update_style()

    def set_text(self, text):
        URL = r"(\w+://(\S+\.)?\S+|www\.\S+)\.[\w\-.~:/?#\[\]@!$&'()*+,;=%]+"
        text_buffer = self.get_buffer()
        bounds = text_buffer.get_bounds()
        text_buffer.delete(*bounds)
        self._link_tags = []
        self._visited_link_tags = []
        for line in text.splitlines():
            i = 0
            for match in re.finditer(URL, line):
                a, z = match.span()
                self._insert_text(line[i:a])
                self._insert_url(line[a:z])
                i = z
            self._insert_text(line[i:])
            self._insert_text("\n")
        self.update_style()

    def update_style(self):
        nfoview.util.apply_style(self)
        name = nfoview.conf.color_scheme
        scheme = nfoview.schemes.get(name, "default")
        for tag in self._link_tags:
            color = nfoview.util.hex_to_rgba(scheme.link)
            tag.props.foreground_rgba = color
        for tag in self._visited_link_tags:
            color = nfoview.util.hex_to_rgba(scheme.visited_link)
            tag.props.foreground_rgba = color
