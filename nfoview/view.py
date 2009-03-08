# Copyright (C) 2005-2009 Osmo Salomaa
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

"""Text view widget for NFO text."""

import gtk
import nfoview
import pango

__all__ = ("TextView",)


class TextView(gtk.TextView):

    """Text view widget for NFO text."""

    def __init__(self):
        """Initialize a TextView instance."""

        gtk.TextView.__init__(self)
        self._init_properties()
        self._link_tags = []
        self._visited_link_tags = []
        self.update_colors()

    def _init_properties(self):
        """Initliaze the text view widget properties."""

        self.set_cursor_visible(False)
        self.set_editable(False)
        self.set_wrap_mode(gtk.WRAP_NONE)
        pixels_above = nfoview.conf.pixels_above_lines
        self.set_pixels_above_lines(pixels_above)
        pixels_below = nfoview.conf.pixels_below_lines
        self.set_pixels_below_lines(pixels_below)
        self.set_left_margin(6)
        self.set_right_margin(6)
        font_desc = pango.FontDescription(nfoview.conf.font)
        self.modify_font(font_desc)
        callback = self._on_motion_notify_event
        self.connect("motion-notify-event", callback)

    def _insert_url(self, url):
        """Insert URL into the text view as a link."""

        text_buffer = self.get_buffer()
        tag = text_buffer.create_tag(None)
        tag.props.underline = pango.UNDERLINE_SINGLE
        tag.connect("event", self._on_link_tag_event)
        tag.set_data("url", url)
        itr = text_buffer.get_end_iter()
        text_buffer.insert_with_tags(itr, url, tag)
        self._link_tags.append(tag)

    def _insert_word(self, word, *tags):
        """Insert word into the text view with tags."""

        text_buffer = self.get_buffer()
        itr = text_buffer.get_end_iter()
        text_buffer.insert_with_tags_by_name(itr, word, *tags)

    def _on_link_tag_event(self, tag, text_view, event, itr):
        """Open clicked link in web browser."""

        if event.type != gtk.gdk.BUTTON_RELEASE: return
        text_buffer = self.get_buffer()
        if text_buffer.get_selection_bounds(): return
        nfoview.util.browse_url(tag.get_data("url"))
        if tag in self._link_tags:
            self._link_tags.remove(tag)
            self._visited_link_tags.append(tag)
            self.update_colors()

    def _on_motion_notify_event(self, text_view, event):
        """Change the mouse pointer when hovering over a link."""

        x = int(event.x)
        y = int(event.y)
        window = gtk.TEXT_WINDOW_WIDGET
        x, y = self.window_to_buffer_coords(window, x, y)
        window = self.get_window(gtk.TEXT_WINDOW_TEXT)
        for tag in self.get_iter_at_location(x, y).get_tags():
            if tag.get_data("url") is not None:
                window.set_cursor(gtk.gdk.Cursor(gtk.gdk.HAND2))
                # pylint: disable-msg=E1101
                return self.window.get_pointer()
        window.set_cursor(gtk.gdk.Cursor(gtk.gdk.XTERM))
        # pylint: disable-msg=E1101
        self.window.get_pointer()

    def get_text(self):
        """Return the text in the text view."""

        text_buffer = self.get_buffer()
        bounds = text_buffer.get_bounds()
        return text_buffer.get_text(*bounds)

    def set_text(self, text):
        """Set the text displayed in the text view."""

        self._link_tags = []
        self._visited_link_tags = []
        text_buffer = self.get_buffer()
        bounds = text_buffer.get_bounds()
        text_buffer.delete(*bounds)
        lines = text.split("\n")
        for i, line in enumerate(lines):
            words = line.split(" ")
            for j, word in enumerate(words):
                if word.count("://"):
                    k = word.index("://")
                    while (k > 0) and word[k - 1].isalnum():
                        k -= 1
                    self._insert_word(word[:k])
                    self._insert_url(word[k:])
                elif word.count("www."):
                    k = word.index("www.")
                    self._insert_word(word[:k])
                    self._insert_url(word[k:])
                else:
                    self._insert_word(word)
                if j < (len(words) - 1):
                    self._insert_word(" ")
            if i < (len(lines) - 1):
                self._insert_word("\n")
        self.update_colors()

    def update_colors(self):
        """Update the colors to match the current color scheme."""

        scheme = nfoview.conf.color_scheme
        try: scheme = nfoview.schemes.get_color_scheme(scheme)
        except ValueError:
            scheme = nfoview.schemes.get_color_scheme("default")
            nfoview.conf.color_scheme = "default"
        self.modify_text(gtk.STATE_NORMAL, scheme.foreground)
        self.modify_base(gtk.STATE_NORMAL, scheme.background)
        for tag in self._link_tags:
            tag.props.foreground_gdk = scheme.link
        for tag in self._visited_link_tags:
            tag.props.foreground_gdk = scheme.visited_link
