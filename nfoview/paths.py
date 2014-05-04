# -*- coding: utf-8 -*-

# Copyright (C) 2008 Osmo Salomaa
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
Paths to files and directories used.

:var CONFIG_HOME_DIR: Path to user's local configuration directory
:var DATA_DIR: Path to the global data directory
:var LOCALE_DIR: Path to the global locale directory
"""

import os
import sys

__all__ = ("CONFIG_HOME_DIR", "DATA_DIR", "LOCALE_DIR")


def get_config_home_directory():
    """Return path to the user's configuration directory."""
    if sys.platform == "win32":
        return get_config_home_directory_windows()
    return get_config_home_directory_xdg()

def get_config_home_directory_windows():
    """Return path to the user's configuration directory on Windows."""
    directory = os.path.expanduser("~")
    directory = os.environ.get("APPDATA", directory)
    directory = os.path.join(directory, "nfoview")
    return os.path.abspath(directory)

def get_config_home_directory_xdg():
    """Return path to the user's XDG configuration directory."""
    directory = os.path.join(os.path.expanduser("~"), ".config")
    directory = os.environ.get("XDG_CONFIG_HOME", directory)
    directory = os.path.join(directory, "nfoview")
    return os.path.abspath(directory)

def get_data_directory_source():
    """Return path to the global data directory when running from source."""
    directory = os.path.dirname(os.path.abspath(__file__))
    directory = os.path.abspath(os.path.join(directory, ".."))
    directory = os.path.join(directory, "data")
    return os.path.abspath(directory)

def get_locale_directory_source():
    """Return path to the locale directory when running from source."""
    directory = os.path.dirname(os.path.abspath(__file__))
    directory = os.path.abspath(os.path.join(directory, ".."))
    directory = os.path.join(directory, "locale")
    return os.path.abspath(directory)

CONFIG_HOME_DIR = get_config_home_directory()
DATA_DIR = get_data_directory_source()
LOCALE_DIR = get_locale_directory_source()
