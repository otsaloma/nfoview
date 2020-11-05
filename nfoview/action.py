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

import nfoview

from gi.repository import Gio
from gi.repository import GLib
from gi.repository import GObject

__all__ = ("Action", "ToggleAction")


class Action(Gio.SimpleAction):

    def __init__(self, name):
        """
        Initialize a class object.

        Args:
            self: (todo): write your description
            name: (str): write your description
        """
        GObject.GObject.__init__(self, name=name)
        self.accelerators = []

    def _affirm_doable(self, window):
        """
        _affirmirmirm.

        Args:
            self: (todo): write your description
            window: (array): write your description
        """
        pass

    def update_enabled(self, window):
        """
        Updates the current window.

        Args:
            self: (todo): write your description
            window: (int): write your description
        """
        try:
            self._affirm_doable(window)
            self.set_enabled(True)
        except nfoview.AffirmationError:
            self.set_enabled(False)


class ToggleAction(Action):

    # Gio's abstraction makes toggle action instantiation and
    # management of boolean state values look really stupid
    # in Python. For proper instantiation, subclasses need to
    # define __new__, call new and assign to __class__.

    @staticmethod
    def new(name, parameter_type=None):
        """
        Create a new parameter

        Args:
            name: (str): write your description
            parameter_type: (str): write your description
        """
        return Gio.SimpleAction.new_stateful(
            name, parameter_type, GLib.Variant("b", False))

    def get_state(self):
        """
        : return state

        Args:
            self: (todo): write your description
        """
        return Action.get_state(self).get_boolean()

    def set_state(self, value):
        """
        Sets whether or not this widget is on. : param value | <bool >

        Args:
            self: (todo): write your description
            value: (todo): write your description
        """
        Action.set_state(self, GLib.Variant("b", value))
