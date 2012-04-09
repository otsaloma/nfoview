# -*- coding: utf-8-unix -*-

# Copyright (C) 2008-2009 Osmo Salomaa
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

"""
Internationalization functions.

Functions defined in this module are convenience aliases for functions of the
:mod:`gettext` module. More important than the aliases is that importing this
module will set proper locale and domain values.
"""

import gettext
import locale
import nfoview

__all__ = ("_", "dgettext", "ngettext")

locale.setlocale(locale.LC_ALL, "")
locale.bindtextdomain("nfoview", nfoview.LOCALE_DIR)
locale.textdomain("nfoview")
gettext.bindtextdomain("nfoview", nfoview.LOCALE_DIR)
gettext.textdomain("nfoview")


def _(message):
    """Return the localized translation of `message`."""
    return gettext.gettext(message)

def dgettext(domain, message):
    """Return the localized translation of `message` from `domain`."""
    return gettext.dgettext(domain, message)

def ngettext(singular, plural, n):
    """Return the localized translation of `singular` or `plural`."""
    return gettext.ngettext(singular, plural, n)
