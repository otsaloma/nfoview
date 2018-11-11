# -*- coding: utf-8 -*-

# Copyright (C) 2006 Osmo Salomaa
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

from gi.repository import Gtk

__all__ = ("BuilderDialog",)


class BuilderDialog:

    """
    Baseclass and wrapper for :class:`Gtk.Builder` constructed dialogs.

    All widgets defined in :attr:`_widgets` are assigned as instance variables
    with names preceded by a single underscore. All signals defined in the UI
    definition file are connected to ``self``. All :func:`getattr` calls not
    found in ``self`` are delegated to :attr:`self._dialog` allowing ``self``
    to look and act like a :class:`Gtk.Dialog`.
    """

    _widgets = []

    def __init__(self, ui_file_path):
        if not os.path.isabs(ui_file_path):
            ui_file_path = os.path.join(nfoview.DATA_DIR, ui_file_path)
        self._builder = Gtk.Builder()
        self._builder.set_translation_domain("nfoview")
        self._builder.add_from_file(ui_file_path)
        self._dialog = self._builder.get_object("dialog")
        self._builder.connect_signals(self)
        for name in self._widgets:
            widget = self._builder.get_object(name)
            setattr(self, "_{}".format(name), widget)

    def __getattr__(self, name):
        return getattr(self._dialog, name)

    def run(self):
        self._dialog.show()
        return self._dialog.run()
