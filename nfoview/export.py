# -*- coding: utf-8 -*-

# Copyright (C) 2013 Osmo Salomaa
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

"""Dialog for selecting an image file to export to."""

import nfoview
_ = nfoview.i18n._

from gi.repository import GObject
from gi.repository import Gtk

__all__ = ("ExportImageDialog",)


class ExportImageDialog(Gtk.FileChooserDialog):

    """Dialog for selecting an image file to export to."""

    def __init__(self, parent):
        """Initialize an :class:`ExportImageDialog` instance."""
        GObject.GObject.__init__(self)
        self.set_title(_("Export Image"))
        self.set_transient_for(parent)
        self.set_action(Gtk.FileChooserAction.SAVE)
        self.add_button(_("_Cancel"), Gtk.ResponseType.CANCEL)
        self.add_button(_("_Save"), Gtk.ResponseType.OK)
        self.set_do_overwrite_confirmation(True)
        self.set_select_multiple(False)
        self.set_default_response(Gtk.ResponseType.OK)
