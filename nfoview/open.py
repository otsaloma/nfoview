# -*- coding: utf-8-unix -*-

# Copyright (C) 2008 Osmo Salomaa
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

"""Dialog for selecting NFO files to open."""

import nfoview
_ = nfoview.i18n._

from gi.repository import GObject
from gi.repository import Gtk

__all__ = ("OpenDialog",)


class OpenDialog(Gtk.FileChooserDialog):

    """Dialog for selecting NFO files to open."""

    def __init__(self, parent):
        """Initialize an OpenDialog instance."""
        GObject.GObject.__init__(self)
        self.set_title(_("Open"))
        self.set_transient_for(parent)
        self.set_action(Gtk.FileChooserAction.OPEN)
        self.add_button(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL)
        self.add_button(Gtk.STOCK_OPEN, Gtk.ResponseType.OK)
        self.set_select_multiple(True)
        file_filter = Gtk.FileFilter()
        file_filter.set_name(_("All files"))
        file_filter.add_pattern("*")
        self.add_filter(file_filter)
        file_filter = Gtk.FileFilter()
        file_filter.set_name(_("NFO files (*.nfo)"))
        file_filter.add_pattern("*.[Nn][Ff][Oo]")
        self.add_filter(file_filter)
        self.set_filter(file_filter)
