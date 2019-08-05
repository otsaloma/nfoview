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

from gi.repository import GObject
from gi.repository import Gtk
from nfoview.i18n  import _

__all__ = ("ExportImageDialog",)

try:
    # Available since GTK 3.20.
    Base = Gtk.FileChooserNative
except AttributeError:
    Base = Gtk.FileChooserDialog


class ExportImageDialog(Base):

    def __init__(self, parent):
        GObject.GObject.__init__(self)
        self.set_title(_("Export Image"))
        self.set_transient_for(parent)
        self.set_action(Gtk.FileChooserAction.SAVE)
        if Base is Gtk.FileChooserNative:
            self.set_cancel_label(_("_Cancel"))
            self.set_accept_label(_("_Save"))
        if Base is Gtk.FileChooserDialog:
            self.add_button(_("_Cancel"), Gtk.ResponseType.CANCEL)
            self.add_button(_("_Save"), Gtk.ResponseType.OK)
            self.set_default_response(Gtk.ResponseType.OK)
        self.set_do_overwrite_confirmation(True)
        self.set_select_multiple(False)
