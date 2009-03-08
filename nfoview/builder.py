# Copyright (C) 2006-2009 Osmo Salomaa
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

"""Wrapper for gtk.Builder constructed dialogs."""

import gtk
import nfoview
_ = nfoview.i18n._

__all__ = ("BuilderDialog",)


class BuilderDialog(object):

    """Wrapper for gtk.Builder constructed dialogs.

    The gtk.Builder instance is saved as instance variable '_builder' and from
    the widget tree the widget name 'dialog' as '_dialog'.
    """

    def __getattr__(self, name):
        """Return attribute from either self or self._dialog."""

        # Allow others to think this class is a dialog.
        return getattr(self._dialog, name)

    def __init__(self, ui_file_path):
        """Initialize a BuilderDialog object from ui_file_path."""

        self._builder = gtk.Builder()
        self._builder.set_translation_domain("nfoview")
        self._builder.add_from_file(ui_file_path)
        self._dialog = self._builder.get_object("dialog")
        # Work around a deeply mysterious bug that prevents strings in the
        # GtkBuilder file from being translated even though calling
        # gettext.gettext manually gives a translation.
        # TODO: Remove this shit once GtkBuilder works properly.
        self.__translate_labels()
        self.__translate_titles()

    def __translate_labels(self):
        """Call nfoview.i18n._ on texts of all labels in self._builder."""

        for obj in self._builder.get_objects():
            if not isinstance(obj, gtk.Label): continue
            if not obj.get_text(): continue
            use_underline = obj.get_use_underline()
            if obj.get_use_markup():
                obj.set_markup(_(obj.props.label))
            else: # Not using markup.
                obj.set_text(_(obj.props.label))
            obj.set_use_underline(use_underline)

    def __translate_titles(self):
        """Call nfoview.i18n._ on titles of all widgets in self._builder."""

        for obj in self._builder.get_objects():
            if not hasattr(obj, "get_title"): continue
            if not hasattr(obj, "set_title"): continue
            if not obj.get_title(): continue
            obj.set_title(_(obj.get_title()))

    def run(self):
        """Show the dialog, run it and return response."""

        self._dialog.show()
        return self._dialog.run()
