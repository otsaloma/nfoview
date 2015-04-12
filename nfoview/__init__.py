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

"""Viewer for NFO files."""

__version__ = "1.15.99"

from nfoview.paths import *
from nfoview import i18n
from nfoview import util
from nfoview.errors import *
from nfoview.config import *
conf = ConfigurationStore()
from nfoview import schemes
from nfoview.builder import *
from nfoview.about import *
from nfoview.open import *
from nfoview.preferences import *
from nfoview.export import *
from nfoview.view import *
from nfoview import actions
from nfoview.window import *
from nfoview import main
from nfoview.unittest import *
