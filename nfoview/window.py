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

"""Viewer window and user interface controller for NFO files."""

import codecs
import gtk
import nfoview
import os
import pango
import textwrap

__all__ = ("Window",)


class Window(gtk.Window):

    """Viewer window and user interface controller for NFO files.

    :ivar clipboard: Instance of :class:`gtk.Clipboard` used
    :ivar path: Path to the NFO file being shown
    :ivar view: Instance of :class:`nfoview.TextView` contained
    """

    def __init__(self, path=None):
        """Initialize a :class:`Window` instance and open file at `path`."""
        gtk.Window.__init__(self)
        self._about_dialog = None
        self._actions = []
        self._preferences_dialog = None
        self._uim = gtk.UIManager()
        self.clipboard = gtk.Clipboard()
        self.path = path
        self.view = nfoview.TextView()
        self._init_window()

    def _get_action(self, name):
        """Return action from the UI manager by `name`."""
        for action_group in self._uim.get_action_groups():
            action = action_group.get_action(name)
            if action is not None: return action
        raise ValueError("Action group %s not found" % repr(name))

    def _get_size_test_label(self):
        """Return a label to use for text size calculations."""
        label = gtk.Label()
        attrs = pango.AttrList()
        font_desc = nfoview.util.get_font_description()
        attrs.insert(pango.AttrFontDesc(font_desc, 0, -1))
        label.set_attributes(attrs)
        return label

    def _init_action_groups_and_uim(self):
        """Initialize action groups and UI manager actions."""
        action_group = gtk.ActionGroup("main")
        for name in nfoview.actions.__all__:
            action = getattr(nfoview.actions, name)()
            callback = "_on_%s_activate" % action.get_name()
            if hasattr(self, callback):
                action.connect("activate", getattr(self, callback))
            action_group.add_action_with_accel(action, action.accelerator)
            self._actions.append(action)
        self._uim.insert_action_group(action_group, 0)
        self._uim.add_ui_from_file(os.path.join(nfoview.DATA_DIR, "ui.xml"))
        self.add_accel_group(self._uim.get_accel_group())
        self._uim.ensure_update()

    def _init_contents(self):
        """Initialize child containers and pack contents."""
        main_vbox = gtk.VBox()
        menubar = self._uim.get_widget("/ui/menubar")
        main_vbox.pack_start(menubar, False, False, 0)
        scroller = gtk.ScrolledWindow()
        scroller.set_policy(*((gtk.POLICY_AUTOMATIC,) * 2))
        scroller.set_shadow_type(gtk.SHADOW_ETCHED_IN)
        scroller.add(self.view)
        main_vbox.pack_start(scroller, True, True, 0)
        main_vbox.show_all()
        self.add(main_vbox)

    def _init_keys(self):
        """Set keybindings not handled by UI manager."""
        accel_group = gtk.AccelGroup()
        key = gtk.keysyms.Escape
        callback = self._on_escape_pressed
        accel_group.connect_group(key, 0, gtk.ACCEL_MASK, callback)
        self.add_accel_group(accel_group)

    def _init_properties(self):
        """Set window properties."""
        self.set_position(gtk.WIN_POS_CENTER)
        self.set_icon_name("gtk-dialog-info")
        gtk.window_set_default_icon_name("gtk-dialog-info")
        self.drag_dest_set(gtk.DEST_DEFAULT_ALL,
                           [("text/uri-list", 0, 0)],
                           gtk.gdk.ACTION_COPY)

        self.connect("drag-data-received",
                     self._on_drag_data_received)

    def _init_text_view_and_buffer(self):
        """Set text view and text buffer properties."""
        self.view.set_sensitive(False)
        self.view.drag_dest_unset()
        def update(text_buffer, spec, self):
            self._update_action_sensitivities()
        text_buffer = self.view.get_buffer()
        text_buffer.connect("notify::has-selection", update, self)

    def _init_window(self):
        """Initialize widgets and set initial properties."""
        self._init_action_groups_and_uim()
        self._init_properties()
        self._init_keys()
        self._init_contents()
        self._init_text_view_and_buffer()
        if self.path is not None:
            self.open_file(self.path)
        self.resize_to_text()
        self._update_action_sensitivities()

    def _on_close_document_activate(self, *args):
        """Delete the window to close the document."""
        self.emit("delete-event", gtk.gdk.Event(gtk.gdk.DELETE))

    def _on_copy_text_activate(self, *args):
        """Copy the selected text to the clipboard."""
        text_buffer = self.view.get_buffer()
        text_buffer.copy_clipboard(self.clipboard)

    def _on_drag_data_received(self, widget, context, x, y, sdata, info, time):
        """Open files dragged from a file browser."""
        paths = map(nfoview.util.uri_to_path, sdata.get_uris())
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
        self.emit("delete-event", gtk.gdk.Event(gtk.gdk.DELETE))

    def _on_open_file_activate(self, *args):
        """Show the open file dialog and open the chosen file."""
        dialog = nfoview.OpenDialog(self)
        if self.path is not None:
            directory = os.path.dirname(self.path)
            dialog.set_current_folder(directory)
        response = dialog.run()
        paths = dialog.get_filenames()
        dialog.destroy()
        if response != gtk.RESPONSE_OK: return
        if not paths: return
        if self.path is None:
            self.open_file(paths.pop(0))
        for path in paths:
            nfoview.main.open_window(path)

    def _on_quit_activate(self, *args):
        """Delete all windows to quit NFO Viewer."""
        for window in nfoview.main.windows[:]:
            window.emit("delete-event", gtk.gdk.Event(gtk.gdk.DELETE))

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
            self.view.set_wrap_mode(gtk.WRAP_WORD)
        else: # not action.props.active
            self.view.set_wrap_mode(gtk.WRAP_NONE)

    def _read_file(self, path, encoding=None):
        """Read and return the text of the NFO file.

        Discard trailing space, trailing blank lines and all odd or even lines
        if they do not contain non-space characters.
        """
        if encoding is None:
            encoding = nfoview.util.detect_encoding(path)
            return self._read_file(path, encoding)
        lines = codecs.open(path, "r", encoding).readlines()
        lines = [x.rstrip() for x in lines]
        while not lines[-1]:
            lines.pop()
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
        self.view.set_sensitive(True)
        self.view.grab_focus()
        self._update_action_sensitivities()

    def resize_to_text(self):
        """Resize window to fit the text in the view."""
        # Get the pixel size of the text to be displayed. If the width exceeds
        # 'text_view_max_chars', switch to line wrapping and use 80 characters
        # for the window width. Limit the height of the window to
        # 'text_view_max_lines'. Finally limit both the width and height of the
        # window to 80 % of the screen to ensure it fits on the screen.
        label = self._get_size_test_label()
        req_text = self.view.get_text()
        blank_text = "\n".join(["x" * 80] * 40)
        label.set_text(req_text or blank_text)
        req_size = list(label.size_request())
        max_chars = nfoview.conf.text_view_max_chars
        max_lines = nfoview.conf.text_view_max_lines
        max_text = "\n".join(("x" * max_chars,) * max_lines)
        label.set_text(max_text)
        max_size = list(label.size_request())
        size = list(req_size)
        if req_size[0] > max_size[0]:
            self._get_action("wrap_lines").activate()
            lines = req_text.split("\n")
            for i, line in enumerate(lines):
                lines[i] = textwrap.fill(line, 80)
            req_text = "\n".join(lines)
            label.set_text(req_text)
            req_size = list(label.size_request())
            size[0] = min(req_size[0], max_size[0])
        size[1] = min(req_size[1], max_size[1])
        pixels_above = nfoview.conf.pixels_above_lines
        pixels_below = nfoview.conf.pixels_below_lines
        lines = self.view.get_text().split("\n")
        size[1] += ((pixels_above + pixels_below) * len(lines))
        # Assume 32 pixels for scrollbars, 24 for menubar height
        # and 12 pixels total for text view left and right margins.
        size[0] = max(200, size[0] + 12 + 32)
        size[1] = max(100, size[1] + 24 + 32)
        size[0] = min(size[0], int(0.8 * gtk.gdk.screen_width()))
        size[1] = min(size[1], int(0.8 * gtk.gdk.screen_height()))
        self.resize(size[0], size[1])
