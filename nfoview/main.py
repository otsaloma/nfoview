# Copyright (C) 2008 Osmo Salomaa
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

import gtk
import nfoview
import os

windows = []

def _on_window_delete_event(window, event):
    """Exit the GTK main loop if the last window was closed."""

    window.destroy()
    ids = map(id, windows)
    index = ids.index(id(window))
    windows.pop(index)
    if windows: return
    nfoview.conf.write_to_file()
    try:
        gtk.main_quit()
    except RuntimeError:
        raise SystemExit(1)

def open_window(path=None):
    """Open file in a new window and present that window."""

    window = nfoview.Window(path)
    callback = _on_window_delete_event
    window.connect("delete-event", callback)
    windows.append(window)
    window.present()

def main(args):
    """Start viewer windows for given arguments."""

    for path in args:
        if os.path.isfile(path):
            open_window(path)
    if not windows:
        # If no arguments were given,
        # or none of them exist,
        # open one blank window.
        open_window()
    gtk.main()
