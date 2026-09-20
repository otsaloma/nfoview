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

import cairo
import nfoview
import textwrap

from gi.repository import Gdk
from gi.repository import Gio
from gi.repository import GObject
from gi.repository import Gtk
from gi.repository import Pango
from gi.repository import PangoCairo
from nfoview.i18n import _
from pathlib import Path

class Window(Gtk.ApplicationWindow):

    def __init__(self, path=None):
        GObject.GObject.__init__(self)
        self.path = Path(path) if path else None
        self.view = nfoview.TextView()
        self._about_dialog = None
        self._prefs_dialog = None
        self._init_properties()
        self._init_titlebar()
        self._init_contents()
        self._init_actions()
        self.open_file(self.path)
        self.resize_to_text()
        self._update_actions_enabled()

    def _hide_on_close(self, dialog):
        # Keep the dialog around so that it can be presented again.
        def on_close_request(dialog, *args):
            dialog.hide()
            return True
        dialog.connect("close-request", on_close_request)
        return dialog

    def _init_actions(self):
        for name in nfoview.actions.__all__:
            action = getattr(nfoview.actions, name)()
            if nfoview.app:
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
        self.connect("close-request", self._on_close_activate)
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
        if self._about_dialog is None:
            self._about_dialog = self._hide_on_close(nfoview.AboutDialog(self))
        self._about_dialog.present()

    def _on_close_activate(self, *args):
        self.destroy()
        if nfoview.app:
            nfoview.app.remove_window(self)

    def _on_export_image_activate(self, *args):
        dialog = nfoview.ExportImageDialog(self)
        directory = Gio.File.new_for_path(str(self.path.parent))
        dialog.set_current_folder(directory)
        dialog.set_current_name(f"{self.path.name}.png")
        dialog.connect("response", self._on_export_image_activate_response)
        dialog.show()

    def _on_export_image_activate_response(self, dialog, response):
        file = dialog.get_file()
        dialog.destroy()
        if response != Gtk.ResponseType.ACCEPT: return
        if file is None: return
        self._write_png(file.get_path())

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
        if response != Gtk.ResponseType.ACCEPT: return
        for path in paths:
            if self.path is None:
                self.open_file(path)
            elif nfoview.app:
                nfoview.app.open_window(path)

    def _on_preferences_activate(self, *args):
        if self._prefs_dialog is None:
            self._prefs_dialog = self._hide_on_close(nfoview.PreferencesDialog(self))
        self._prefs_dialog.present()

    def _on_quit_activate(self, *args):
        if nfoview.app:
            nfoview.app.quit()

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
        text = self.view.get_text() or "\n".join(["x" * 80] * 40)
        width, height = nfoview.util.get_text_view_size(text)
        max_width, max_height = nfoview.util.get_max_text_view_size()
        if width > max_width:
            self.activate_action("wrap-lines", None)
            text = "\n".join(textwrap.fill(x, 80) for x in text.split("\n"))
            width, height = nfoview.util.get_text_view_size(text)
        width = min(width, max_width)
        height = min(height, max_height)
        # Assume 12 pixels total for text view margins,
        # 24 pixels for scrollbars, 48 pixels for header bar.
        width = max(400, width + 12 + 24)
        height = max(248, height + 12 + 24 + 48)
        screen_width, screen_height = nfoview.util.get_screen_size()
        width = min(width, int(0.8 * screen_width))
        height = min(height, int(0.8 * screen_height))
        self.set_default_size(width, height)

    def _update_actions_enabled(self):
        for name in self.list_actions():
            action = self.lookup_action(name)
            action.update_enabled(self)

    def _write_png(self, path):
        # Lay the text out on a dummy surface to measure the size needed.
        dummy = cairo.Context(cairo.ImageSurface(cairo.FORMAT_ARGB32, 1, 1))
        layout = PangoCairo.create_layout(dummy)
        layout.set_font_description(Pango.FontDescription(nfoview.conf.font))
        layout.set_text(self.view.get_text(), -1)
        width, height = layout.get_pixel_size()
        scale = nfoview.conf.export_scale
        surface = cairo.ImageSurface(cairo.FORMAT_ARGB32,
                                     int(scale * width),
                                     int(scale * height))
        surface.set_device_scale(scale, scale)
        context = cairo.Context(surface)
        # Always export black on white regardless of the color scheme.
        context.set_source_rgb(1, 1, 1)
        context.paint()
        PangoCairo.update_layout(context, layout)
        context.set_source_rgb(0, 0, 0)
        PangoCairo.show_layout(context, layout)
        surface.write_to_png(path)
