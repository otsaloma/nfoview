# -*- coding: utf-8 -*-

# Copyright (C) 2008 Osmo Salomaa
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

"""
Spawning, managing and killing viewer windows.

:var windows: List of existing :class:`nfoview.Window` instances
"""

import gettext
import locale
import nfoview
import sys

from gi.repository import Gtk

windows = []


def _init_gettext():
    """Initialize translation settings."""
    try:
        # Might fail with misconfigured locales.
        locale.setlocale(locale.LC_ALL, "")
    except Exception:
        print("Failed to set default locale.", file=sys.stderr)
        print("Please check your locale settings.", file=sys.stderr)
        print("Falling back to the 'C' locale.", file=sys.stderr)
        locale.setlocale(locale.LC_ALL, "C")
    try:
        # Not available on all platforms.
        locale.bindtextdomain("nfoview", nfoview.LOCALE_DIR)
        locale.textdomain("nfoview")
    except AttributeError:
        pass
    gettext.bindtextdomain("nfoview", nfoview.LOCALE_DIR)
    gettext.textdomain("nfoview")

def main(args):
    """Start viewer windows for files given as arguments."""
    _init_gettext()
    for path in sorted(args):
        try:
            open_window(path)
        except Exception as error:
            print("Failed to open '{}': {}"
                  .format(path, str(error)),
                  file=sys.stderr)

    if not windows:
        # If no arguments were given, or none of them exist,
        # open one blank window.
        open_window()
    Gtk.main()

def _on_window_delete_event(window, event):
    """Exit the ``Gtk`` main loop if the last window was closed."""
    window.destroy()
    windows.remove(window)
    if windows: return
    nfoview.conf.write_to_file()
    try:
        Gtk.main_quit()
    except RuntimeError:
        raise SystemExit(1)

def open_window(path=None):
    """Open file in a new window and present that window."""
    window = nfoview.Window(path)
    window.connect("delete-event",
                   _on_window_delete_event)

    windows.append(window)
    window.present()
