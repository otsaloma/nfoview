# -*- coding: utf-8-unix -*-

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

"""Viewer window and user interface controller for NFO files."""

import atexit
import nfoview
import os
import textwrap

from gi.repository import Gdk
from gi.repository import GObject
from gi.repository import Gtk

__all__ = ("Window",)


class Window(Gtk.Window):

    """
    Viewer window and user interface controller for NFO files.

    :ivar clipboard: Instance of :class:`Gtk.Clipboard` used
    :ivar path: Path to the NFO file being shown
    :ivar view: Instance of :class:`nfoview.TextView` contained
    """

    def __init__(self, path=None):
        """Initialize a :class:`Window` instance and open file at `path`."""
        GObject.GObject.__init__(self)
        self._about_dialog = None
        self._actions = []
        self._preferences_dialog = None
        self._uim = Gtk.UIManager()
        self.path = path
        self.view = nfoview.TextView()
        self._init_uim()
        self._init_properties()
        self._init_keys()
        self._init_contents()
        self._init_text_view()
        if self.path is not None:
            self.open_file(self.path)
        self.resize_to_text()
        self._update_action_sensitivities()

    def _get_action(self, name):
        """Return action from the UI manager by `name`."""
        for action_group in self._uim.get_action_groups():
            action = action_group.get_action(name)
            if action is not None: return action
        raise ValueError("Action group {} not found"
                         .format(repr(name)))

    def _get_max_view_size(self):
        """Return maximum size for view."""
        label = Gtk.Label()
        font_desc = nfoview.util.get_font_description()
        label.override_font(font_desc)
        max_chars = nfoview.conf.text_view_max_chars
        max_lines = nfoview.conf.text_view_max_lines
        max_text = "\n".join(("x" * max_chars,) * max_lines)
        label.set_text(max_text)
        return (label.get_preferred_width()[1],
                label.get_preferred_height()[1])

    def _get_preferred_view_size(self, text):
        """Return preferred size for view to hold `text`."""
        label = Gtk.Label()
        font_desc = nfoview.util.get_font_description()
        label.override_font(font_desc)
        label.set_text(text)
        return (label.get_preferred_width()[1],
                label.get_preferred_height()[1])

    def _init_contents(self):
        """Initialize child containers and pack contents."""
        main_vbox = Gtk.VBox()
        menubar = self._uim.get_widget("/ui/menubar")
        main_vbox.pack_start(menubar, 
                             expand=False, 
                             fill=False, 
                             padding=0)

        scroller = Gtk.ScrolledWindow()
        scroller.set_policy(*((Gtk.PolicyType.AUTOMATIC,) * 2))
        scroller.set_shadow_type(Gtk.ShadowType.ETCHED_IN)
        scroller.add(self.view)
        main_vbox.pack_start(scroller, 
                             expand=True, 
                             fill=True, 
                             padding=0)

        main_vbox.show_all()
        self.add(main_vbox)

    def _init_keys(self):
        """Initialize additional keybindings."""
        accel_group = Gtk.AccelGroup()
        accel_group.connect(Gdk.KEY_Escape,
                            0,
                            Gtk.AccelFlags.MASK,
                            self._on_escape_pressed)

        self.add_accel_group(accel_group)

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

    def _init_text_view(self):
        """Initialize text view and associated buffer."""
        self.view.drag_dest_unset()
        def update(text_buffer, spec, self):
            self._update_action_sensitivities()
        text_buffer = self.view.get_buffer()
        text_buffer.connect("notify::has-selection", update, self)

    def _init_uim(self):
        """Initialize UI manager actions."""
        action_group = Gtk.ActionGroup("main")
        for name in nfoview.actions.__all__:
            action = getattr(nfoview.actions, name)()
            callback = "_on_{}_activate".format(action.get_name())
            if hasattr(self, callback):
                action.connect("activate", getattr(self, callback))
            action_group.add_action_with_accel(action, action.accelerator)
            self._actions.append(action)
        self._uim.insert_action_group(action_group, 0)
        self._uim.add_ui_from_file(os.path.join(nfoview.DATA_DIR, "ui.xml"))
        self.add_accel_group(self._uim.get_accel_group())
        path = os.path.join(nfoview.CONFIG_HOME_DIR, "accels.conf")
        if os.path.isfile(path):
            Gtk.AccelMap.load(path)
        atexit.register(Gtk.AccelMap.save, path)
        self._uim.ensure_update()

    def _on_close_document_activate(self, *args):
        """Delete the window to close document."""
        self.emit("delete-event", Gdk.Event(Gdk.EventType.DELETE))

    def _on_copy_text_activate(self, *args):
        """Copy the selected text to the clipboard."""
        text_buffer = self.view.get_buffer()
        clipboard = Gtk.Clipboard.get(Gdk.atom_intern("CLIPBOARD", False))
        text_buffer.copy_clipboard(clipboard)

    def _on_drag_data_received(self, widget, context, x, y, sdata, info, time):
        """Open files dragged from a file browser."""
        paths = list(map(nfoview.util.uri_to_path, sdata.get_uris()))
        if self.path is None:
            self.open_file(paths.pop(0))
        for path in paths:
            nfoview.main.open_window(path)

    def _on_edit_preferences_activate(self, *args):
        """Show the preferences dialog."""
        if self._preferences_dialog is not None:
            return self._preferences_dialog.present()
        self._preferences_dialog = nfoview.PreferencesDialog(self)
        def destroy(dialog, response, self):
            self._preferences_dialog.destroy()
            self._preferences_dialog = None
        self._preferences_dialog.connect("response", destroy, self)
        self._preferences_dialog.show()

    def _on_escape_pressed(self, *args):
        """Delete the window to close the document."""
        self.emit("delete-event", Gdk.Event(Gdk.EventType.DELETE))

    def _on_open_file_activate(self, *args):
        """Show the open file dialog and open the chosen file."""
        dialog = nfoview.OpenDialog(self)
        if self.path is not None:
            directory = os.path.dirname(self.path)
            dialog.set_current_folder(directory)
        response = dialog.run()
        paths = dialog.get_filenames()
        dialog.destroy()
        if response != Gtk.ResponseType.OK: return
        if not paths: return
        if self.path is None:
            self.open_file(paths.pop(0))
        for path in paths:
            nfoview.main.open_window(path)

    def _on_quit_activate(self, *args):
        """Delete all windows to quit NFO Viewer."""
        for window in list(nfoview.main.windows):
            window.emit("delete-event", Gdk.Event(Gdk.EventType.DELETE))

    def _on_select_all_text_activate(self, *args):
        """Select all text in the document."""
        text_buffer = self.view.get_buffer()
        bounds = text_buffer.get_bounds()
        text_buffer.select_range(*bounds)
        self._update_action_sensitivities()

    def _on_show_about_dialog_activate(self, *args):
        """Show the about dialog."""
        if self._about_dialog is not None:
            return self._about_dialog.present()
        self._about_dialog = nfoview.AboutDialog(self)
        def destroy(dialog, response, self):
            self._about_dialog.destroy()
            self._about_dialog = None
        self._about_dialog.connect("response", destroy, self)
        self._about_dialog.show()

    def _on_wrap_lines_activate(self, action, *args):
        """Break long lines at word borders."""
        if action.props.active:
            return self.view.set_wrap_mode(Gtk.WrapMode.WORD)
        return self.view.set_wrap_mode(Gtk.WrapMode.NONE)

    def _read_file(self, path):
        """
        Read and return the text of the NFO file.

        Discard trailing space, trailing blank lines and all odd or
        even line if they do not contain non-space characters.
        """
        encoding = nfoview.util.detect_encoding(path)
        lines = open(path, "r", encoding=encoding).readlines()
        lines = [x.rstrip() for x in lines]
        while lines and not lines[-1]: lines.pop()
        lines0 = [lines[i] for i in range(0, len(lines), 2)]
        lines1 = [lines[i] for i in range(1, len(lines), 2)]
        if not sum(map(len, lines0)): lines = lines1
        if not sum(map(len, lines1)): lines = lines0
        return "\n".join(lines)

    def _update_action_sensitivities(self):
        """Update the sensitivities of all UI manager actions."""
        for action in self._actions:
            action.update_sensitivity(self)

    def open_file(self, path):
        """Read the file at `path` and show its text in the view."""
        self.path = os.path.abspath(path)
        self.set_title(os.path.basename(path))
        text = self._read_file(path)
        self.view.set_text(text)
        self.view.grab_focus()
        self._update_action_sensitivities()

    def resize_to_text(self):
        """Resize window to fit the text in the view."""
        # Get the pixel size of the text to be displayed. If the width exceeds
        # 'text_view_max_chars', switch to line wrapping and use 80 characters
        # for the window width. Limit the height of the window to
        # 'text_view_max_lines'. Finally limit both the width and height of the
        # window to 80 % of the screen to ensure it fits on the screen.
        text = self.view.get_text()
        text = text or "\n".join(["x" * 80] * 40)
        size = list(self._get_preferred_view_size(text))
        max_size = self._get_max_view_size()
        if size[0] > max_size[0]:
            self._get_action("wrap_lines").activate()
            lines = text.split("\n")
            for i, line in enumerate(lines):
                lines[i] = textwrap.fill(line, 80)
            text = "\n".join(lines)
            size = list(self._get_preferred_view_size(text))
        size[0] = min(size[0], max_size[0])
        size[1] = min(size[1], max_size[1])
        pixels_above = nfoview.conf.pixels_above_lines
        pixels_below = nfoview.conf.pixels_below_lines
        nlines = text.count("\n") + 1
        size[1] = size[1] + ((pixels_above + pixels_below) * nlines)
        # Assume 32 pixels for scrollbars, 24 for menubar height
        # and 12 pixels total for text view left and right margins.
        size[0] = max(400, size[0] + 12 + 32)
        size[1] = max(248, size[1] + 24 + 32)
        size[0] = min(size[0], int(0.8 * Gdk.Screen.width()))
        size[1] = min(size[1], int(0.8 * Gdk.Screen.height()))
        self.resize(*size)
