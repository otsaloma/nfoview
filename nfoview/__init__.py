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

__version__ = "2.1"

import sys
import warnings

if hasattr(sys, "frozen"):
    # Avoid error trying to write to non-existent stderr.
    # https://stackoverflow.com/a/35773092
    warnings.simplefilter("ignore")

import gi
gi.require_version("Gdk", "4.0")
gi.require_version("Gtk", "4.0")

from nfoview.paths import CONFIG_HOME_DIR
from nfoview.paths import DATA_DIR
from nfoview.paths import LOCALE_DIR
from nfoview import util
from nfoview import i18n
from nfoview.errors import AffirmationError
from nfoview.config import ConfigurationStore
conf = ConfigurationStore(read=True)
from nfoview import schemes
from nfoview.about import AboutDialog
from nfoview.export import ExportImageDialog
from nfoview.open import OpenDialog
from nfoview.preferences import PreferencesDialog
from nfoview.view import TextView
from nfoview.action import Action
from nfoview.action import ToggleAction
from nfoview import actions
from nfoview.window import Window
from nfoview.application import Application
from nfoview.unittest import TestCase

def main(paths):
    global app
    i18n.bind()
    app = Application(paths)
    raise SystemExit(app.run())
