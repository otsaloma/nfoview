# Copyright (C) 2008 Osmo Salomaa
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

"""Paths to files and directories used."""

import os

__all__ = ("CONFIG_DIR", "DATA_DIR", "LOCALE_DIR")


def get_config_directory():
    directory = os.path.join(os.path.expanduser("~"), ".config")
    directory = os.environ.get("XDG_CONFIG_HOME", directory)
    directory = os.path.abspath(directory)
    return os.path.join(directory, "nfoview")

def get_source_directory(child):
    parent = os.path.dirname(os.path.abspath(__file__))
    source = os.path.abspath(os.path.join(parent, ".."))
    return os.path.abspath(os.path.join(source, child))

CONFIG_DIR = get_config_directory()
DATA_DIR = get_source_directory("data")
LOCALE_DIR = get_source_directory("locale")
