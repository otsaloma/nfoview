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

"""Text view widget for NFO text with support for clickable hyperlinks."""

import nfoview
import re

from gi.repository import Gdk
from gi.repository import GObject
from gi.repository import Gtk
from gi.repository import Pango

__all__ = ("TextView",)


class TextView(Gtk.TextView):

    """Text view widget for NFO text with support for clickable hyperlinks."""

    def __init__(self):
        """Initialize a :class:`TextView` instance."""
        GObject.GObject.__init__(self)
        self._init_properties()
        self._link_tags = []
        self._visited_link_tags = []
        self.update_colors()

    def _init_properties(self):
        """Initliaze text view widget properties."""
        pixels_above = nfoview.conf.pixels_above_lines
        pixels_below = nfoview.conf.pixels_below_lines
        font_desc = nfoview.util.get_font_description()
        self.set_cursor_visible(False)
        self.set_editable(False)
        self.set_wrap_mode(Gtk.WrapMode.NONE)
        self.set_pixels_above_lines(pixels_above)
        self.set_pixels_below_lines(pixels_below)
        self.set_left_margin(6)
        self.set_right_margin(6)
        self.modify_font(font_desc)
        nfoview.util.connect(self, self, "motion-notify-event")

    def _insert_url(self, url):
        """Insert `url` into the text view as a hyperlink."""
        text_buffer = self.get_buffer()
        tag = text_buffer.create_tag(None)
        tag.props.underline = Pango.Underline.SINGLE
        tag.connect("event", self._on_link_tag_event)
        tag.set_data("url", url)
        itr = text_buffer.get_end_iter()
        text_buffer.insert_with_tags(itr, url, tag)
        self._link_tags.append(tag)

    def _insert_word(self, word):
        """Insert `word` into the text view."""
        text_buffer = self.get_buffer()
        itr = text_buffer.get_end_iter()
        # XXX: assertion `g_utf8_validate (text, len, NULL)' failed
        text_buffer.insert(itr, word)

    def _on_link_tag_event(self, tag, text_view, event, itr):
        """Open clicked hyperlink in web browser."""
        if event.type != Gdk.EventType.BUTTON_RELEASE: return
        text_buffer = self.get_buffer()
        if text_buffer.get_selection_bounds(): return
        nfoview.util.show_uri(tag.get_data("url"))
        if tag in self._link_tags:
            self._link_tags.remove(tag)
            self._visited_link_tags.append(tag)
            self.update_colors()

    def _on_motion_notify_event(self, text_view, event):
        """Change the mouse pointer when hovering over a hyperlink."""
        x = int(event.x)
        y = int(event.y)
        window = Gtk.TextWindowType.WIDGET
        x, y = self.window_to_buffer_coords(window, x, y)
        window = self.get_window(Gtk.TextWindowType.TEXT)
        for tag in self.get_iter_at_location(x, y).get_tags():
            if tag.get_data("url") is not None:
                window.set_cursor(Gdk.Cursor.new(Gdk.CursorType.HAND2))
                return True
        window.set_cursor(Gdk.Cursor.new(Gdk.CursorType.XTERM))
        return False

    def get_text(self):
        """Return the text in the text view."""
        text_buffer = self.get_buffer()
        start, end = text_buffer.get_bounds()
        return text_buffer.get_text(start, end, False)

    def set_text(self, text):
        """Set the text displayed in the text view."""
        re_url = re.compile(r"(([0-9a-zA-Z]+://\S+?\.\S+)|(www\.\S+?\.\S+))")
        self._link_tags = []
        self._visited_link_tags = []
        text_buffer = self.get_buffer()
        bounds = text_buffer.get_bounds()
        text_buffer.delete(*bounds)
        lines = text.split("\n")
        for i, line in enumerate(lines):
            words = line.split(" ")
            for j, word in enumerate(words):
                match = re_url.search(word)
                if match is not None:
                    a, z = match.span()
                    self._insert_word(word[:a])
                    self._insert_url(word[a:z])
                    self._insert_word(word[z:])
                else: # Normal text.
                    self._insert_word(word)
                self._insert_word(" ")
            itr = text_buffer.get_end_iter()
            text_buffer.backspace(itr, False, True)
            self._insert_word("\n")
        itr = text_buffer.get_end_iter()
        text_buffer.backspace(itr, False, True)
        self.update_colors()

    def update_colors(self):
        """Update colors to match the current color scheme."""
        name = nfoview.conf.color_scheme
        try: scheme = nfoview.util.get_color_scheme(name)
        except ValueError:
            scheme = nfoview.util.get_color_scheme("default")
            nfoview.conf.color_scheme = "default"
        for state in (Gtk.StateFlags.NORMAL,):
            self.override_color(state, scheme.foreground)
            self.override_background_color(state, scheme.background)
        for state in (Gtk.StateFlags.SELECTED,):
            context = Gtk.TextView().get_style_context()
            foreground = context.get_color(state)
            background = context.get_background_color(state)
            self.override_color(state, foreground)
            self.override_background_color(state, background)
        for tag in self._link_tags:
            color = nfoview.util.rgba_to_color(scheme.link)
            tag.set_property("foreground_gdk", color)
        for tag in self._visited_link_tags:
            color = nfoview.util.rgba_to_color(scheme.visited_link)
            tag.set_property("foreground_gdk", color)
