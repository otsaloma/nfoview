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

import os
import sys

from pathlib import Path


def get_config_home_directory():
    if sys.platform == "win32":
        return get_config_home_directory_windows()
    return get_config_home_directory_xdg()

def get_config_home_directory_windows():
    directory = os.environ.get("APPDATA", Path.home())
    directory = Path(directory) / "NFO Viewer"
    return directory.resolve()

def get_config_home_directory_xdg():
    directory = os.environ.get("XDG_CONFIG_HOME", Path.home() / ".config")
    directory = Path(directory) / "nfoview"
    return directory.resolve()

def get_data_directory():
    if hasattr(sys, "frozen"):
        return get_data_directory_frozen()
    return get_data_directory_source()

def get_data_directory_frozen():
    directory = Path(sys.argv[0]).parent / "share" / "nfoview"
    return directory.resolve()

def get_data_directory_source():
    directory = Path(__file__).parent.parent / "data"
    return directory.resolve()

def get_locale_directory():
    if hasattr(sys, "frozen"):
        return get_locale_directory_frozen()
    return get_locale_directory_source()

def get_locale_directory_frozen():
    directory = Path(sys.argv[0]).parent / "share" / "locale"
    return directory.resolve()

def get_locale_directory_source():
    directory = Path(__file__).parent.parent / "locale"
    return directory.resolve()

CONFIG_HOME_DIR = get_config_home_directory()
DATA_DIR = get_data_directory()
LOCALE_DIR = get_locale_directory()
