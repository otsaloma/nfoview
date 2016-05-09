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
        self._link_tags = []
        self._visited_link_tags = []
        self._init_properties()
        self.update_colors()

    def get_text(self):
        """Return the text in the text view."""
        text_buffer = self.get_buffer()
        start, end = text_buffer.get_bounds()
        return text_buffer.get_text(start, end, False)

    def _init_properties(self):
        """Initialize text view widget properties."""
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
        with nfoview.util.silent(AttributeError):
            # Available since GTK+ 3.18.
            self.set_top_margin(6)
            self.set_bottom_margin(6)
        self.override_font(font_desc)
        nfoview.util.connect(self, self, "motion-notify-event")

    def _insert_url(self, url):
        """Insert `url` into the text view as a hyperlink."""
        text_buffer = self.get_buffer()
        tag = text_buffer.create_tag(None)
        tag.props.underline = Pango.Underline.SINGLE
        tag.connect("event", self._on_link_tag_event)
        tag.nfoview_url = url
        itr = text_buffer.get_end_iter()
        text_buffer.insert_with_tags(itr, url, tag)
        self._link_tags.append(tag)

    def _insert_word(self, word):
        """Insert `word` into the text view."""
        text_buffer = self.get_buffer()
        itr = text_buffer.get_end_iter()
        text_buffer.insert(itr, word)

    def _on_link_tag_event(self, tag, text_view, event, itr):
        """Open clicked hyperlink in web browser."""
        if event.type != Gdk.EventType.BUTTON_RELEASE: return
        text_buffer = self.get_buffer()
        if text_buffer.get_selection_bounds(): return
        nfoview.util.show_uri(tag.nfoview_url)
        if tag in self._link_tags:
            self._link_tags.remove(tag)
            self._visited_link_tags.append(tag)
            self.update_colors()

    def _on_motion_notify_event(self, text_view, event):
        """Change the mouse pointer when hovering over a hyperlink."""
        window = Gtk.TextWindowType.WIDGET
        x, y = self.window_to_buffer_coords(window, int(event.x), int(event.y))
        window = self.get_window(Gtk.TextWindowType.TEXT)
        tags = []
        # XXX: Return value changed since GTK+ 3.20!?
        iter = self.get_iter_at_location(x, y)
        if (isinstance(iter, tuple) and
            hasattr(iter, "iter")):
            iter = iter.iter
        with nfoview.util.silent(AttributeError):
            tags = iter.get_tags()
        if any(hasattr(x, "nfoview_url") for x in tags):
            window.set_cursor(Gdk.Cursor.new_for_display(
                Gdk.Display.get_default(), Gdk.CursorType.HAND2))
            return True # to not call the default handler.
        window.set_cursor(Gdk.Cursor.new_for_display(
            Gdk.Display.get_default(), Gdk.CursorType.XTERM))

    def set_text(self, text):
        """Set the text displayed in the text view."""
        re_url = re.compile(r"(\w+://(\S+\.)?\S+|www\.\S+)\.[\w\-.~:/?#\[\]@!$&'()*+,;=%]+")
        self._link_tags = []
        self._visited_link_tags = []
        text_buffer = self.get_buffer()
        bounds = text_buffer.get_bounds()
        text_buffer.delete(*bounds)
        lines = text.split("\n")
        # Scan text word-by-word for possible URLs,
        # but insert words in larger chunks to avoid
        # doing too many slow text view updates.
        word_queue = []
        for i, line in enumerate(lines):
            words = line.split(" ")
            for j, word in enumerate(words):
                match = re_url.search(word)
                if match is not None:
                    a, z = match.span()
                    word_queue.append(word[:a])
                    self._insert_word("".join(word_queue))
                    word_queue = []
                    self._insert_url(word[a:z])
                    word_queue.append(word[z:])
                else: # Normal text.
                    word_queue.append(word)
                word_queue.append(" ")
            word_queue.pop(-1)
            word_queue.append("\n")
            if len(word_queue) > 1000:
                self._insert_word("".join(word_queue))
                word_queue = []
        self._insert_word("".join(word_queue))
        self.update_colors()

    def update_colors(self):
        """Update colors to match the current color scheme."""
        name = nfoview.conf.color_scheme
        scheme = nfoview.schemes.get(name, "default")
        state = Gtk.StateFlags.NORMAL
        self.override_color(state, scheme.foreground)
        self.override_background_color(state, scheme.background)
        entry = Gtk.Entry()
        entry.show()
        style = entry.get_style_context()
        state = Gtk.StateFlags.SELECTED
        foreground = style.get_color(state)
        background = style.get_background_color(state)
        self.override_color(state, foreground)
        self.override_background_color(state, background)
        for tag in self._link_tags:
            tag.props.foreground_rgba = scheme.link
        for tag in self._visited_link_tags:
            tag.props.foreground_rgba = scheme.visited_link
