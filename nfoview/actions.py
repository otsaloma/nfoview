# Copyright (C) 2005-2008 Osmo Salomaa
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

"""UI manager actions."""

import gtk
import nfoview
_ = nfoview.i18n._

__all__ = (
    "CloseDocumentAction",
    "CopyTextAction",
    "EditPreferencesAction",
    "OpenFileAction",
    "SelectAllTextAction",
    "ShowAboutDialogAction",
    "ShowEditMenuAction",
    "ShowFileMenuAction",
    "ShowHelpMenuAction",)


class Action(gtk.Action):

    """Base class for UI manager actions.

    Instance variable 'accelerator' defines a string string in the format
    understood by the gtk.accelerator_parse(), None to use the stock
    accelerator or leave undefined to use a blank string as a fallback.
    """

    accelerator = ""

    def __init__(self, name):
        """Initialize an Action instance."""

        gtk.Action.__init__(self, name, None, None, None)

    def _affirm_doable(self, window):
        """Raise AffirmationError if action cannot be done."""

        pass

    def update_sensitivity(self, window):
        """Update the sensitivity of action."""

        try:
            self._affirm_doable(window)
        except nfoview.AffirmationError:
            return self.set_sensitive(False)
        return self.set_sensitive(True)


class CloseDocumentAction(Action):

    """Close document."""

    def __init__(self):
        """Initialize a CloseDocumentAction instance."""

        Action.__init__(self, "close_document")
        self.props.label = _("_Close")
        self.props.stock_id = gtk.STOCK_CLOSE
        self.props.tooltip = _("Close document")
        self.accelerator = "<Control>W"


class CopyTextAction(Action):

    """Copy the selected text to the clipboard."""

    def __init__(self):
        """Initialize a CopyTextAction instance."""

        Action.__init__(self, "copy_text")
        self.props.is_important = True
        self.props.label = _("_Copy")
        self.props.short_label = _("Copy")
        self.props.stock_id = gtk.STOCK_COPY
        self.props.tooltip = _("Copy the selected text to the clipboard")
        self.accelerator = "<Control>C"

    def _affirm_doable(self, window):
        """Raise AffirmationError if action cannot be done."""

        nfoview.util.affirm(window.view is not None)
        nfoview.util.affirm(window.view.props.sensitive)
        text_buffer = window.view.get_buffer()
        nfoview.util.affirm(text_buffer.get_has_selection())


class EditPreferencesAction(Action):

    """Edit NFO Viewer preferences."""

    def __init__(self):
        """Initialize an EditPreferencesAction instance."""

        Action.__init__(self, "edit_preferences")
        self.props.label = _("_Preferences")
        self.props.stock_id = gtk.STOCK_PREFERENCES
        self.props.tooltip = _("Edit NFO Viewer preferences")


class OpenFileAction(Action):

    """Open file."""

    def __init__(self):
        """Initialize an OpenFileAction instance."""

        Action.__init__(self, "open_file")
        self.props.is_important = True
        self.props.label = _("_Open...")
        self.props.short_label = _("Open")
        self.props.stock_id = gtk.STOCK_OPEN
        self.props.tooltip = _("Open file")
        self.accelerator = "<Control>O"


class ShowAboutDialogAction(Action):

    """Show information about NFO Viewer."""

    def __init__(self):
        """Initialize a ShowAboutDialogAction instance."""

        Action.__init__(self, "show_about_dialog")
        self.props.label = _("_About")
        self.props.stock_id = gtk.STOCK_ABOUT
        self.props.tooltip = _("Show information about NFO Viewer")


class SelectAllTextAction(Action):

    """Select all text in the document."""

    def __init__(self):
        """Initialize a SelectAllTextAction instance."""

        Action.__init__(self, "select_all_text")
        self.props.label = _("_Select All")
        if hasattr(gtk, "STOCK_SELECT_ALL"):
            self.props.stock_id = gtk.STOCK_SELECT_ALL
        self.props.tooltip = _("Select all text in the document")
        self.accelerator = "<Control>A"

    def _affirm_doable(self, window):
        """Raise AffirmationError if action cannot be done."""

        nfoview.util.affirm(window.view is not None)
        nfoview.util.affirm(window.view.props.sensitive)


class ShowEditMenuAction(Action):

    """Show the edit menu."""

    def __init__(self):
        """Initialize a ShowEditMenuAction instance."""

        Action.__init__(self, "show_edit_menu")
        self.props.label = _("_Edit")


class ShowFileMenuAction(Action):

    """Show the file menu."""

    def __init__(self):
        """Initialize a ShowFileMenuAction instance."""

        Action.__init__(self, "show_file_menu")
        self.props.label = _("_File")


class ShowHelpMenuAction(Action):

    """Show the help menu."""

    def __init__(self):
        """Initialize a ShowHelpMenuAction instance."""

        Action.__init__(self, "show_help_menu")
        self.props.label = _("_Help")
