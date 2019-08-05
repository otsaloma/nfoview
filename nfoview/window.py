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
import os
import textwrap

from gi.repository import Gdk
from gi.repository import GObject
from gi.repository import Gtk
from nfoview.i18n  import _

__all__ = ("Window",)


class Window(Gtk.ApplicationWindow):

    def __init__(self, path=None):
        GObject.GObject.__init__(self)
        self._about_dialog = None
        self.path = path
        self._preferences_dialog = None
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
        for name in nfoview.actions.__all__:
            action = getattr(nfoview.actions, name)()
            if hasattr(nfoview, "app"):
                name = "win.{}".format(action.props.name)
                nfoview.app.set_accels_for_action(name, action.accelerators)
            callback = "_on_{}_activate".format(action.props.name.replace("-", "_"))
            action.connect("activate", getattr(self, callback))
            self.add_action(action)

    def _init_contents(self):
        scroller = Gtk.ScrolledWindow()
        scroller.set_policy(*((Gtk.PolicyType.AUTOMATIC,)*2))
        scroller.set_shadow_type(Gtk.ShadowType.NONE)
        scroller.add(self.view)
        main_vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        main_vbox.pack_start(scroller, expand=True, fill=True, padding=0)
        main_vbox.show_all()
        self.add(main_vbox)

    def _init_properties(self):
        self.set_position(Gtk.WindowPosition.CENTER)
        self.set_icon_name("io.otsaloma.nfoview")
        Gtk.Window.set_default_icon_name("io.otsaloma.nfoview")
        self.drag_dest_set(flags=Gtk.DestDefaults.ALL,
                           targets=None,
                           actions=Gdk.DragAction.COPY)

        self.drag_dest_add_uri_targets()
        self.connect("drag-data-received", self._on_drag_data_received)
        self.connect("delete-event", self._on_delete_event)

    def _init_titlebar(self):
        header = Gtk.HeaderBar()
        header.set_title(_("NFO Viewer"))
        header.set_show_close_button(True)
        menu_button = Gtk.MenuButton()
        menu_button.set_direction(Gtk.ArrowType.NONE)
        # Popover doesn't show keyboard shortcuts.
        menu_button.set_use_popover(False)
        path = os.path.join(nfoview.DATA_DIR, "menu.ui")
        builder = Gtk.Builder.new_from_file(path)
        menu = builder.get_object("menu")
        menu_button.set_menu_model(menu)
        header.pack_start(menu_button)
        header.show_all()
        self.set_titlebar(header)

    def _init_view(self):
        self.view.drag_dest_unset()
        def update(text_buffer, spec, self):
            self._update_actions_enabled()
        text_buffer = self.view.get_buffer()
        text_buffer.connect("notify::has-selection", update, self)

    def _on_about_activate(self, *args):
        if self._about_dialog is not None:
            return self._about_dialog.present()
        self._about_dialog = nfoview.AboutDialog(self)
        def destroy(dialog, response, self):
            self._about_dialog.destroy()
            self._about_dialog = None
        self._about_dialog.connect("response", destroy, self)
        self._about_dialog.show()

    def _on_close_activate(self, *args):
        if hasattr(nfoview, "app"):
            nfoview.app.remove_window(self)

    def _on_copy_activate(self, *args):
        text_buffer = self.view.get_buffer()
        clipboard = Gtk.Clipboard.get(Gdk.atom_intern("CLIPBOARD", False))
        text_buffer.copy_clipboard(clipboard)

    def _on_delete_event(self, *args):
        # Work around a harmless Gtk-WARNING about drag destination
        # by removing the window and hiding it instead of destroying.
        # https://bugzilla.gnome.org/show_bug.cgi?id=721708
        if hasattr(nfoview, "app"):
            self.hide()
            nfoview.app.remove_window(self)
            return True

    def _on_drag_data_received(self, widget, context, x, y, data, info, time):
        paths = list(map(nfoview.util.uri_to_path, data.get_uris()))
        if self.path is None:
            self.open_file(paths.pop(0))
        if hasattr(nfoview, "app"):
            list(map(nfoview.app.open_window, paths))

    def _on_export_image_activate(self, *args):
        dialog = nfoview.ExportImageDialog(self)
        directory = os.path.dirname(self.path)
        dialog.set_current_folder(directory)
        basename = os.path.basename(self.path)
        dialog.set_current_name("{}.png".format(basename))
        response = dialog.run()
        path = dialog.get_filename()
        dialog.destroy()
        if response not in (
            Gtk.ResponseType.ACCEPT,
            Gtk.ResponseType.OK,
        ): return
        if not path: return
        view = nfoview.TextView()
        view.set_text(self.view.get_text())
        window = Gtk.OffscreenWindow()
        window.nfoview_path = path
        window.add(view)
        def on_damage_event(window, *args):
            pixbuf = window.get_pixbuf()
            pixbuf.savev(window.nfoview_path, "png", [], [])
        window.connect("damage-event", on_damage_event)
        window.show_all()
        while Gtk.events_pending():
            Gtk.main_iteration()

    def _on_open_activate(self, *args):
        dialog = nfoview.OpenDialog(self)
        if self.path is not None:
            directory = os.path.dirname(self.path)
            dialog.set_current_folder(directory)
        response = dialog.run()
        paths = dialog.get_filenames()
        dialog.destroy()
        if response not in (
            Gtk.ResponseType.ACCEPT,
            Gtk.ResponseType.OK,
        ): return
        if not paths: return
        if self.path is None:
            self.open_file(paths.pop(0))
        if hasattr(nfoview, "app"):
            list(map(nfoview.app.open_window, paths))

    def _on_preferences_activate(self, *args):
        if self._preferences_dialog is not None:
            return self._preferences_dialog.present()
        self._preferences_dialog = nfoview.PreferencesDialog(self)
        def destroy(dialog, response, self):
            self._preferences_dialog.destroy()
            self._preferences_dialog = None
        self._preferences_dialog.connect("response", destroy, self)
        self._preferences_dialog.show()

    def _on_quit_activate(self, *args):
        if hasattr(nfoview, "app"):
            nfoview.app.quit()

    def _on_select_all_activate(self, *args):
        text_buffer = self.view.get_buffer()
        bounds = text_buffer.get_bounds()
        text_buffer.select_range(*bounds)
        self._update_actions_enabled()

    def _on_wrap_lines_activate(self, action, *args):
        action.set_state(not action.get_state())
        if action.get_state():
            return self.view.set_wrap_mode(Gtk.WrapMode.WORD)
        return self.view.set_wrap_mode(Gtk.WrapMode.NONE)

    def open_file(self, path):
        self.path = os.path.abspath(path)
        self.set_title(os.path.basename(path))
        text = self._read_file(path)
        self.view.set_text(text)
        self.view.grab_focus()
        self._update_actions_enabled()

    def _read_file(self, path):
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
        # If the width of text exceeds 'text_view_max_chars',
        # switch to line wrapping and use 80 characters width.
        # Limit height to 'text_view_max_lines'. Finally limit
        # width and height to to 80 % of the screen.
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
        # TODO: Use per-monitor geometry, requires GTK >= 3.22.
        size[0] = min(size[0], int(0.8 * Gdk.Screen.width()))
        size[1] = min(size[1], int(0.8 * Gdk.Screen.height()))
        self.resize(*size)

    def _update_actions_enabled(self):
        for name in self.list_actions():
            action = self.lookup_action(name)
            action.update_enabled(self)
