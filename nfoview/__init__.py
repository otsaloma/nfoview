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

__version__ = "1.25"

import sys
import warnings

if hasattr(sys, "frozen"):
    # Avoid error trying to write to non-existent stderr.
    # http://stackoverflow.com/a/35773092
    warnings.simplefilter("ignore")

import gi
gi.require_version("Gdk", "3.0")
gi.require_version("Gtk", "3.0")

from gi.repository import GLib

from nfoview.paths import CONFIG_HOME_DIR
from nfoview.paths import DATA_DIR
from nfoview.paths import LOCALE_DIR
from nfoview import util
from nfoview import i18n
from nfoview.errors import AffirmationError
from nfoview.config import ConfigurationStore
conf = ConfigurationStore(read=True)
from nfoview import schemes
from nfoview.builder import BuilderDialog
from nfoview.about import AboutDialog
from nfoview.open import OpenDialog
from nfoview.preferences import PreferencesDialog
from nfoview.export import ExportImageDialog
from nfoview.view import TextView
from nfoview.action import Action
from nfoview.action import ToggleAction
from nfoview import actions
from nfoview.window import Window
from nfoview.application import Application
from nfoview.unittest import TestCase

assert AboutDialog
assert Action
assert actions
assert AffirmationError
assert Application
assert BuilderDialog
assert CONFIG_HOME_DIR
assert ConfigurationStore
assert DATA_DIR
assert ExportImageDialog
assert i18n
assert LOCALE_DIR
assert OpenDialog
assert PreferencesDialog
assert schemes
assert TestCase
assert TextView
assert ToggleAction
assert util
assert Window

def main(paths):
    global app
    # Needed to see application icon on Wayland, while we don't yet
    # use the reverse domain application ID with Gtk.Application.
    # https://wiki.gnome.org/Projects/GnomeShell/ApplicationBased
    # https://github.com/otsaloma/gaupol/issues/62
    GLib.set_prgname("nfoview")
    i18n.bind()
    app = Application(paths)
    raise SystemExit(app.run())
