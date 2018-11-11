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

__all__ = (
    "AboutAction",
    "CloseAction",
    "CopyAction",
    "ExportImageAction",
    "OpenAction",
    "PreferencesAction",
    "QuitAction",
    "SelectAllAction",
    "WrapLinesAction",
)

class AboutAction(nfoview.Action):
    def __init__(self):
        nfoview.Action.__init__(self, "about")

class CloseAction(nfoview.Action):
    def __init__(self):
        nfoview.Action.__init__(self, "close")
        self.accelerators = ["<Control>W", "Escape"]

class CopyAction(nfoview.Action):
    def __init__(self):
        nfoview.Action.__init__(self, "copy")
        self.accelerators = ["<Control>C"]
    def _affirm_doable(self, window):
        nfoview.util.affirm(window.view is not None)
        nfoview.util.affirm(window.view.get_sensitive())
        text_buffer = window.view.get_buffer()
        nfoview.util.affirm(text_buffer.get_has_selection())

class ExportImageAction(nfoview.Action):
    def __init__(self):
        nfoview.Action.__init__(self, "export-image")
        self.accelerators = ["<Control>E"]
    def _affirm_doable(self, window):
        nfoview.util.affirm(window.path is not None)
        nfoview.util.affirm(window.view is not None)
        nfoview.util.affirm(window.view.get_sensitive())

class OpenAction(nfoview.Action):
    def __init__(self):
        nfoview.Action.__init__(self, "open")
        self.accelerators = ["<Control>O"]

class PreferencesAction(nfoview.Action):
    def __init__(self):
        nfoview.Action.__init__(self, "preferences")

class QuitAction(nfoview.Action):
    def __init__(self):
        nfoview.Action.__init__(self, "quit")
        self.accelerators = ["<Control>Q"]

class SelectAllAction(nfoview.Action):
    def __init__(self):
        nfoview.Action.__init__(self, "select-all")
        self.accelerators = ["<Control>A"]
    def _affirm_doable(self, window):
        nfoview.util.affirm(window.view is not None)
        nfoview.util.affirm(window.view.get_sensitive())
        nfoview.util.affirm(window.view.get_text())

class WrapLinesAction(nfoview.ToggleAction):
    def __new__(cls):
        action = nfoview.ToggleAction.new("wrap-lines")
        action.__class__ = cls
        return action
    def __init__(self):
        nfoview.Action.__init__(self, "wrap-lines")
        self.accelerators = ["<Control>R"]
    def _affirm_doable(self, window):
        nfoview.util.affirm(window.view is not None)
        nfoview.util.affirm(window.view.get_sensitive())
        nfoview.util.affirm(window.view.get_text())
