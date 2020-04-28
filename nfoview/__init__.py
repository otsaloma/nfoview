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

__version__ = "1.28"

import sys
import warnings

if hasattr(sys, "frozen"):
    # Avoid error trying to write to non-existent stderr.
    # https://stackoverflow.com/a/35773092
    warnings.simplefilter("ignore")

import gi
gi.require_version("Gdk", "3.0")
gi.require_version("Gtk", "3.0")

from nfoview.paths import CONFIG_HOME_DIR # noqa
from nfoview.paths import DATA_DIR # noqa
from nfoview.paths import LOCALE_DIR # noqa
from nfoview import util # noqa
from nfoview import i18n # noqa
from nfoview.errors import AffirmationError # noqa
from nfoview.config import ConfigurationStore # noqa
conf = ConfigurationStore(read=True) # noqa
from nfoview import schemes # noqa
from nfoview.builder import BuilderDialog # noqa
from nfoview.about import AboutDialog # noqa
from nfoview.open import OpenDialog # noqa
from nfoview.preferences import PreferencesDialog # noqa
from nfoview.export import ExportImageDialog # noqa
from nfoview.view import TextView # noqa
from nfoview.action import Action # noqa
from nfoview.action import ToggleAction # noqa
from nfoview import actions # noqa
from nfoview.window import Window # noqa
from nfoview.application import Application # noqa
from nfoview.unittest import TestCase # noqa

def main(paths):
    global app
    i18n.bind()
    app = Application(paths)
    raise SystemExit(app.run())
