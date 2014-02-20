# -*- coding: utf-8 -*-

# Copyright (C) 2005-2009,2011,2013 Osmo Salomaa
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

"""UI manager actions."""

import nfoview
_ = nfoview.i18n._

from gi.repository import GObject
from gi.repository import Gtk

__all__ = ("CloseDocumentAction",
           "CopyTextAction",
           "EditPreferencesAction",
           "ExportAsImageFileAction",
           "OpenFileAction",
           "QuitAction",
           "SelectAllTextAction",
           "ShowAboutDialogAction",
           "ShowEditMenuAction",
           "ShowFileMenuAction",
           "ShowHelpMenuAction",
           "WrapLinesAction",
           )


class Action(Gtk.Action):

    """
    Base class for UI manager actions.

    :ivar accelerator: Accelerator string for :func:`Gtk.accelerator_parse`

    Instance variable :attr:`accelerator` defines a string in the format
    understood by :func:`Gtk.accelerator_parse`, ``None`` to use the stock
    accelerator or leave undefined to use blank string as a fallback.
    """

    def __init__(self, name):
        """Initialize an :class:`Action` instance."""
        GObject.GObject.__init__(self, name=name)
        self.accelerator = ""

    def _affirm_doable(self, window):
        """Raise :exc:`AffirmationError` if action cannot be done."""
        pass

    def update_sensitivity(self, window):
        """Update the sensitivity of action."""
        try:
            self._affirm_doable(window)
        except nfoview.AffirmationError:
            return self.set_sensitive(False)
        return self.set_sensitive(True)


class ToggleAction(Gtk.ToggleAction, Action):

    """Base class for UI manager toggle actions."""

    def __init__(self, name):
        """Initialize an :class:`ToggleAction` instance."""
        GObject.GObject.__init__(self, name=name)


class CloseDocumentAction(Action):

    """Close document."""

    def __init__(self):
        """Initialize a :class:`CloseDocumentAction` instance."""
        Action.__init__(self, "close_document")
        self.props.label = _("_Close")
        self.props.stock_id = Gtk.STOCK_CLOSE
        self.props.tooltip = _("Close document")
        self.accelerator = "<Control>W"


class CopyTextAction(Action):

    """Copy the selected text to the clipboard."""

    def __init__(self):
        """Initialize a :class:`CopyTextAction` instance."""
        Action.__init__(self, "copy_text")
        self.props.is_important = True
        self.props.label = _("_Copy")
        self.props.short_label = _("Copy")
        self.props.stock_id = Gtk.STOCK_COPY
        self.props.tooltip = _("Copy the selected text to the clipboard")
        self.accelerator = "<Control>C"

    def _affirm_doable(self, window):
        """Raise :exc:`AffirmationError` if action cannot be done."""
        nfoview.util.affirm(window.view is not None)
        nfoview.util.affirm(window.view.props.sensitive)
        text_buffer = window.view.get_buffer()
        nfoview.util.affirm(text_buffer.get_has_selection())


class EditPreferencesAction(Action):

    """Edit NFO Viewer preferences."""

    def __init__(self):
        """Initialize an :class:`EditPreferencesAction` instance."""
        Action.__init__(self, "edit_preferences")
        self.props.label = _("_Preferences")
        self.props.stock_id = Gtk.STOCK_PREFERENCES
        self.props.tooltip = _("Edit NFO Viewer preferences")


class ExportAsImageFileAction(Action):

    """Export document as an image file."""

    def __init__(self):
        """Initialize an :class:`ExportAsImageFileAction` instance."""
        Action.__init__(self, "export_as_image")
        self.props.label = _("_Export Image…")
        self.props.tooltip = _("Export document as an image file")
        self.accelerator = "<Control>E"

    def _affirm_doable(self, window):
        """Raise :exc:`AffirmationError` if action cannot be done."""
        nfoview.util.affirm(window.path is not None)
        nfoview.util.affirm(window.view is not None)
        nfoview.util.affirm(window.view.props.sensitive)


class OpenFileAction(Action):

    """Open file."""

    def __init__(self):
        """Initialize an :class:`OpenFileAction` instance."""
        Action.__init__(self, "open_file")
        self.props.is_important = True
        self.props.label = _("_Open…")
        self.props.short_label = _("Open")
        self.props.stock_id = Gtk.STOCK_OPEN
        self.props.tooltip = _("Open file")
        self.accelerator = "<Control>O"


class QuitAction(Action):

    """Close all documents and quit NFO Viewer."""

    def __init__(self):
        """Initialize a :class:`QuitAction` instance."""
        Action.__init__(self, "quit")
        self.props.label = _("_Quit")
        self.props.stock_id = Gtk.STOCK_QUIT
        self.props.tooltip = _("Quit NFO Viewer")
        self.accelerator = "<Control>Q"


class SelectAllTextAction(Action):

    """Select all text in the document."""

    def __init__(self):
        """Initialize a :class:`SelectAllTextAction` instance."""
        Action.__init__(self, "select_all_text")
        self.props.label = _("_Select All")
        self.props.stock_id = Gtk.STOCK_SELECT_ALL
        self.props.tooltip = _("Select all text in the document")
        self.accelerator = "<Control>A"

    def _affirm_doable(self, window):
        """Raise :exc:`AffirmationError` if action cannot be done."""
        nfoview.util.affirm(window.view is not None)
        nfoview.util.affirm(window.view.props.sensitive)


class ShowAboutDialogAction(Action):

    """Show information about NFO Viewer."""

    def __init__(self):
        """Initialize a :class:`ShowAboutDialogAction` instance."""
        Action.__init__(self, "show_about_dialog")
        self.props.label = _("_About")
        self.props.stock_id = Gtk.STOCK_ABOUT
        self.props.tooltip = _("Show information about NFO Viewer")


class ShowEditMenuAction(Action):

    """Show the edit menu."""

    def __init__(self):
        """Initialize a :class:`ShowEditMenuAction` instance."""
        Action.__init__(self, "show_edit_menu")
        self.props.label = _("_Edit")


class ShowFileMenuAction(Action):

    """Show the file menu."""

    def __init__(self):
        """Initialize a :class:`ShowFileMenuAction` instance."""
        Action.__init__(self, "show_file_menu")
        self.props.label = _("_File")


class ShowHelpMenuAction(Action):

    """Show the help menu."""

    def __init__(self):
        """Initialize a :class:`ShowHelpMenuAction` instance."""
        Action.__init__(self, "show_help_menu")
        self.props.label = _("_Help")


class WrapLinesAction(ToggleAction):

    """Break long lines at word borders."""

    def __init__(self):
        """Initialize a :class:`WrapLinesAction` instance."""
        ToggleAction.__init__(self, "wrap_lines")
        self.props.active = False
        self.props.label = _("_Wrap Lines")
        self.props.tooltip = _("Break long lines at word borders")
        self.accelerator = "<Control>R"

    def _affirm_doable(self, window):
        """Raise :exc:`AffirmationError` if action cannot be done."""
        nfoview.util.affirm(window.view is not None)
        nfoview.util.affirm(window.view.props.sensitive)
