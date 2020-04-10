# -*- coding: utf-8 -*-

# Copyright (C) 2008 Osmo Salomaa
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

from gi.repository import GObject
from gi.repository import Gtk
from nfoview.i18n  import _

__all__ = ("AboutDialog",)


class AboutDialog(Gtk.AboutDialog):

    def __init__(self, parent):
        GObject.GObject.__init__(self)
        self.set_title(_("About NFO Viewer"))
        self.set_transient_for(parent)
        self.set_authors(("Osmo Salomaa <otsaloma@iki.fi>",))
        self.set_comments(_("Viewer for NFO files"))
        self.set_copyright("Copyright © 2005–2020 Osmo Salomaa")
        self.set_license_type(Gtk.License.GPL_3_0)
        self.set_logo_icon_name("io.otsaloma.nfoview")
        # TRANSLATORS: The application name "NFO Viewer" has been intentionally
        # marked as translatable. If you manage to translate the name in a
        # fluent manner, without changing the meaning, you may use that
        # translation at your discretion.
        self.set_program_name(_("NFO Viewer"))
        # TRANSLATORS: This is a special message that shouldn't be translated
        # literally. It is used in the about dialog to give credits to the
        # translators. Thus, you should translate it to your name and email
        # address. You can also include other translators who have contributed
        # to this translation; in that case, please write them on separate
        # lines seperated by newlines (\n).
        self.set_translator_credits(_("translator-credits"))
        self.set_version(nfoview.__version__)
        self.set_website("https://otsaloma.io/nfoview/")
        self.set_website_label(_("NFO Viewer Website"))
        self.set_wrap_license(True)
