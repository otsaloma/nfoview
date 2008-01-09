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

"""Dialog for selecting NFO files to open."""

import gtk
import nfoview
_ = nfoview.i18n._

__all__ = ("OpenDialog",)


class OpenDialog(gtk.FileChooserDialog):

    """Dialog for selecting NFO files to open."""

    def __init__(self, parent):

        gtk.FileChooserDialog.__init__(self, parent=parent)
        self.set_title(_("Open"))
        self.set_transient_for(parent)
        self.set_action(gtk.FILE_CHOOSER_ACTION_OPEN)
        self.add_button(gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL)
        self.add_button(gtk.STOCK_OPEN, gtk.RESPONSE_OK)
        self.set_select_multiple(True)

        file_filter = gtk.FileFilter()
        file_filter.set_name(_("All files"))
        file_filter.add_pattern("*")
        self.add_filter(file_filter)

        file_filter = gtk.FileFilter()
        file_filter.set_name(_("NFO files (*.nfo)"))
        file_filter.add_pattern("*.nfo")
        self.add_filter(file_filter)
        self.set_filter(file_filter)
