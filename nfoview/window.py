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

"""Viewer window and user interface controller for NFO files."""

import nfoview
import os
import textwrap
_ = nfoview.i18n.gettext

from gi.repository import Gdk
from gi.repository import Gio
from gi.repository import GObject
from gi.repository import Gtk

__all__ = ("Window",)


class Window(Gtk.ApplicationWindow):

    """Viewer window and user interface controller for NFO files."""

    def __init__(self, path=None):
        """Initialize a :class:`Window` instance and open file at `path`."""
        GObject.GObject.__init__(self)
        self.path = path
        self.view = nfoview.TextView()
        self._init_properties()
        self._init_titlebar()
        self._init_contents()
        self._init_view()
        self._init_actions()
        if self.path is not None:
            self.open_file(self.path)
        self.resize_to_text()
        self._update_actions_enabled()

    def _init_actions(self):
        """Initialize user-activatable actions."""
        for name in nfoview.actions.__all__:
            action = getattr(nfoview.actions, name)()
            if hasattr(nfoview, "app"):
                name = "win.{}".format(action.props.name)
                nfoview.app.set_accels_for_action(
                    name, action.accelerators)
            # TODO: Connect signal handlers
            self.add_action(action)

    def _init_contents(self):
        """Initialize child containers and pack contents."""
        scroller = Gtk.ScrolledWindow()
        scroller.set_policy(*((Gtk.PolicyType.AUTOMATIC,)*2))
        scroller.set_shadow_type(Gtk.ShadowType.ETCHED_IN)
        scroller.add(self.view)
        main_vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        main_vbox.pack_start(scroller, expand=True, fill=True, padding=0)
        main_vbox.show_all()
        self.add(main_vbox)

    def _init_properties(self):
        """Initialize window properties."""
        self.set_position(Gtk.WindowPosition.CENTER)
        self.set_icon_name("nfoview")
        Gtk.Window.set_default_icon_name("nfoview")
        self.drag_dest_set(flags=Gtk.DestDefaults.ALL,
                           targets=None,
                           actions=Gdk.DragAction.COPY)

        self.drag_dest_add_uri_targets()
        self.connect("drag-data-received",
                     self._on_drag_data_received)

    def _init_titlebar(self):
        """Initialize window titlebar."""
        header = Gtk.HeaderBar()
        header.set_title(_("NFO Viewer"))
        header.set_show_close_button(True)
        menu_button = Gtk.MenuButton()
        menu_button.set_direction(Gtk.ArrowType.NONE)
        menu_button.set_use_popover(False)
        path = os.path.join(nfoview.DATA_DIR, "menu.ui")
        builder = Gtk.Builder.new_from_file(path)
        menu = builder.get_object("menu")
        menu_button.set_menu_model(menu)
        header.pack_start(menu_button)
        header.show_all()
        self.set_titlebar(header)

    def _init_view(self):
        """Initialize text view and associated buffer."""
        self.view.drag_dest_unset()
        def update(text_buffer, spec, self):
            self._update_actions_enabled()
        text_buffer = self.view.get_buffer()
        text_buffer.connect("notify::has-selection", update, self)

    def _on_drag_data_received(self, widget, context, x, y, data, info, time):
        """Open files dragged from a file browser."""
        paths = list(map(nfoview.util.uri_to_path, data.get_uris()))
        if self.path is None:
            self.open_file(paths.pop(0))
        if hasattr(nfoview, "app"):
            list(map(nfoview.app.open_window, paths))

    def open_file(self, path):
        """Read the file at `path` and show its text in the view."""
        self.path = os.path.abspath(path)
        self.set_title(os.path.basename(path))
        text = self._read_file(path)
        self.view.set_text(text)
        self.view.grab_focus()
        self._update_actions_enabled()

    def _read_file(self, path):
        """Read and return the text of NFO file at `path`."""
        encoding = nfoview.util.detect_encoding(path)
        with open(path, "r", encoding=encoding) as f:
            lines = f.readlines()
        lines = [x.rstrip() for x in lines]
        while lines and not lines[-1]: lines.pop()
        # Handle erroneous (?) UTF-16 encoded files that use
        # NULL-character filled linebreaks '\x00\r\x00\n', which
        # readlines interprets as two separate linebreaks.
        if not any(lines[i] for i in range(1, len(lines), 2)):
            lines = [lines[i] for i in range(0, len(lines), 2)]
        return "\n".join(lines)

    def resize_to_text(self):
        """Resize window to fit the text in the view."""
        # If the width of text exceeds 'text_view_max_chars',
        # switch to line wrapping and use 80 characters width.
        # Limit height to 'text_view_max_lines'. Finally width
        # and height to to 80 % of the screen.
        text = self.view.get_text()
        text = text or "\n".join(["x" * 80] * 40)
        size = list(nfoview.util.get_text_view_size(text))
        max_size = nfoview.util.get_max_text_view_size()
        if size[0] > max_size[0]:
            self.activate_action("wrap-lines", None)
            text = "\n".join(map(
                lambda x: textwrap.fill(x, 80),
                text.split("\n")))
            size = list(nfoview.util.get_text_view_size(text))
        size[0] = min(size[0], max_size[0])
        size[1] = min(size[1], max_size[1])
        p1 = nfoview.conf.pixels_above_lines
        p2 = nfoview.conf.pixels_below_lines
        size[1] = size[1] + ((p1 + p2) * (text.count("\n")+1))
        # Assume 12 pixels total for text view margins,
        # 14 pixels for scrollbars, 48 pixels for header bar.
        # XXX: Why is that not even close to enough?
        size[0] = max(400, size[0] + 12 + 14 + 100)
        size[1] = max(248, size[1] + 48 + 14 + 100)
        size[0] = min(size[0], int(0.8 * Gdk.Screen.width()))
        size[1] = min(size[1], int(0.8 * Gdk.Screen.height()))
        self.resize(*size)

    def _update_actions_enabled(self):
        """Update the enabled state of all actions."""
        for name in self.list_actions():
            action = self.lookup_action(name)
            action.update_enabled(self)
