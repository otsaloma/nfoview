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
import textwrap

from gi.repository import Gdk
from gi.repository import Gio
from gi.repository import GObject
from gi.repository import Gtk
from nfoview.i18n  import _
from pathlib import Path


class Window(Gtk.ApplicationWindow):

    def __init__(self, path=None):
        GObject.GObject.__init__(self)
        self.path = Path(path) if path else None
        self.view = nfoview.TextView()
        self._init_properties()
        self._init_titlebar()
        self._init_contents()
        self._init_actions()
        self.open_file(self.path)
        self.resize_to_text()
        self._update_actions_enabled()

    def _init_actions(self):
        for name in nfoview.actions.__all__:
            action = getattr(nfoview.actions, name)()
            if hasattr(nfoview, "app"):
                nfoview.app.set_accels_for_action(
                    f"win.{action.props.name}", action.accelerators)
            callback = f"_on_{action.props.name}_activate".replace("-", "_")
            action.connect("activate", getattr(self, callback))
            self.add_action(action)

    def _init_contents(self):
        scroller = Gtk.ScrolledWindow()
        scroller.set_policy(*((Gtk.PolicyType.AUTOMATIC,)*2))
        scroller.set_hexpand(True)
        scroller.set_vexpand(True)
        scroller.set_child(self.view)
        self.set_child(scroller)

    def _init_properties(self):
        self.set_title(_("NFO Viewer"))
        self.set_icon_name("io.otsaloma.nfoview")
        Gtk.Window.set_default_icon_name("io.otsaloma.nfoview")
        target = Gtk.DropTarget.new(Gio.File, Gdk.DragAction.COPY)
        target.connect("drop", self._on_drag_drop)
        self.view.add_controller(target)

    def _init_titlebar(self):
        header = Gtk.HeaderBar()
        menu_button = Gtk.MenuButton()
        menu_button.set_direction(Gtk.ArrowType.NONE)
        path = nfoview.DATA_DIR / "menu.ui"
        builder = Gtk.Builder.new_from_file(str(path))
        menu = builder.get_object("menu")
        menu_button.set_menu_model(menu)
        header.pack_start(menu_button)
        self.set_titlebar(header)

    def _on_drag_drop(self, target, value, x, y, user_data=None):
        path = value.get_path()
        if self.path is None:
            return self.open_file(path)
        nfoview.app.open_window(path)

    def _on_about_activate(self, *args):
        nfoview.AboutDialog(self).show()

    def _on_close_activate(self, *args):
        if hasattr(nfoview, "app"):
            nfoview.app.remove_window(self)

    def _on_export_image_activate(self, *args):
        dialog = nfoview.ExportImageDialog(self)
        directory = Gio.File.new_for_path(str(self.path.parent))
        dialog.set_current_folder(directory)
        dialog.set_current_name(f"{self.path.name}.png")
        dialog.connect("response", self._on_export_image_activate_response)
        dialog.show()

    def _on_export_image_activate_response(self, dialog, response):
        path = dialog.get_file().get_path()
        dialog.destroy()
        if response not in (
            Gtk.ResponseType.ACCEPT,
            Gtk.ResponseType.OK,
        ): return
        if not path: return
        # XXX: No more Gtk.OffscreenWindow in GTK 4,
        # is there a new way to take a screenshot?
        raise NotImplementedError

    def _on_open_activate(self, *args):
        dialog = nfoview.OpenDialog(self)
        if self.path is not None:
            directory = Gio.File.new_for_path(str(self.path.parent))
            dialog.set_current_folder(directory)
        dialog.connect("response", self._on_open_activate_response)
        dialog.show()

    def _on_open_activate_response(self, dialog, response):
        paths = [x.get_path() for x in dialog.get_files()]
        dialog.destroy()
        if response not in (
            Gtk.ResponseType.ACCEPT,
            Gtk.ResponseType.OK,
        ): return
        for path in paths:
            if self.path is None:
                self.open_file(path)
            elif hasattr(nfoview, "app"):
                nfoview.app.open_window(path)

    def _on_quit_activate(self, *args):
        if hasattr(nfoview, "app"):
            nfoview.app.quit()

    def _on_preferences_activate(self, *args):
        nfoview.PreferencesDialog(self).show()

    def _on_wrap_lines_activate(self, action, *args):
        action.set_state(not action.get_state())
        if action.get_state():
            return self.view.set_wrap_mode(Gtk.WrapMode.WORD)
        return self.view.set_wrap_mode(Gtk.WrapMode.NONE)

    def open_file(self, path):
        if path is None: return
        self.path = Path(path).resolve()
        self.set_title(self.path.name)
        text = self._read_file(self.path)
        self.view.set_text(text)
        self.view.grab_focus()
        self._update_actions_enabled()

    def _read_file(self, path):
        encoding = nfoview.util.detect_encoding(path)
        lines = Path(path).read_text(encoding).splitlines()
        lines = [x.rstrip() for x in lines]
        while lines and not lines[-1]: lines.pop()
        # Handle erroneous (?) UTF-16 encoded files that use
        # NULL-character filled linebreaks '\x00\r\x00\n', which
        # readlines interprets as two separate linebreaks.
        if not any(lines[i] for i in range(1, len(lines), 2)):
            lines = [lines[i] for i in range(0, len(lines), 2)]
        return "\n".join(lines)

    def resize_to_text(self):
        # If the width of text exceeds 'text_view_max_chars',
        # switch to line wrapping and use 80 characters width.
        # Limit height to 'text_view_max_lines'. Finally limit
        # width and height to 80% of the screen.
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
        # Assume 12 pixels total for text view margins,
        # 24 pixels for scrollbars, 48 pixels for header bar.
        size[0] = max(400, size[0] + 12 + 24)
        size[1] = max(248, size[1] + 12 + 24 + 48)
        screen_size = nfoview.util.get_screen_size()
        size[0] = min(size[0], int(0.8 * screen_size[0]))
        size[1] = min(size[1], int(0.8 * screen_size[1]))
        self.set_default_size(*size)

    def _update_actions_enabled(self):
        for name in self.list_actions():
            action = self.lookup_action(name)
            action.update_enabled(self)
