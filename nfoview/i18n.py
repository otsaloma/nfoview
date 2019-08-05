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

import gettext
import locale
import nfoview

_translation = gettext.NullTranslations()


def bind(localedir=nfoview.LOCALE_DIR):
    with nfoview.util.silent(Exception):
        # Set locale to the user's default setting.
        # Might fail on misconfigured systems.
        locale.setlocale(locale.LC_ALL, "")
    # Make translations available to the gettext module.
    gettext.bindtextdomain("nfoview", localedir)
    gettext.textdomain("nfoview")
    with nfoview.util.silent(Exception):
        # Make translations available to GTK as well.
        # Not available on all platforms.
        locale.bindtextdomain("nfoview", localedir)
        locale.textdomain("nfoview")
    globals()["_translation"] = gettext.translation(
        "nfoview", localedir=localedir, fallback=True)

def _(message):
    return _translation.gettext(message)

def d_(domain, message):
    return gettext.dgettext(domain, message)

def n_(singular, plural, n):
    return _translation.ngettext(singular, plural, n)
