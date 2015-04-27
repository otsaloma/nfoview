# -*- coding: utf-8 -*-

# Copyright (C) 2015 Osmo Salomaa
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

"""Baseclasses for user-activatable actions."""

import nfoview

from gi.repository import Gio
from gi.repository import GObject

__all__ = ("Action",)


class Action(Gio.SimpleAction):

    """Baseclass for user-activatable actions."""

    def __init__(self, name):
        """Initialize an :class:`Action` instance."""
        GObject.GObject.__init__(self, name=name)
        self.accelerators = []

    def _affirm_doable(self, window):
        """Raise :exc:`nfoview.AffirmationError` if action cannot be done."""
        pass

    def update_enabled(self, window):
        """Update the "enabled" property to match `window`."""
        try:
            self._affirm_doable(window)
            self.set_enabled(True)
        except nfoview.AffirmationError:
            self.set_enabled(False)
