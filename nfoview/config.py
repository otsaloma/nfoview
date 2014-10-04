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

"""Reading, writing and storing configurations."""

import nfoview
import os
import re
import sys
import traceback

__all__ = ("ConfigurationStore",)

_DEFAULTS = dict(
    background_color="#ffffff",
    color_scheme="default",
    font="Terminus 12",
    foreground_color="#2e3436",
    link_color="#4a90d9",
    pixels_above_lines=0,
    pixels_below_lines=0,
    text_view_max_chars=160,
    text_view_max_lines=45,
    version="",
    visited_link_color="#ac4ad9",
)


class ConfigurationStore:

    """
    Reading, writing and storing configurations.

    :ivar background_color: Custom background color
    :ivar color_scheme: Name of the color scheme used
    :ivar font: Font string in :class:`Pango.FontDescription` format
    :ivar foreground_color: Custom foreground color
    :ivar link_color: Custom link color
    :ivar path: Path to user's local configuration file
    :ivar pixels_above_lines: Extra line-spacing above each line
    :ivar pixels_below_lines: Extra line-spacing below each line
    :ivar text_view_max_chars: Maximum width for text view in characters
    :ivar text_view_max_lines: Maximum height for text view in lines
    :ivar version: Version number, same as :data:`nfoview.__version__`
    :ivar visited_link_color: Custom visited link color
    """

    path = os.path.join(nfoview.CONFIG_HOME_DIR, "nfoview.conf")

    def __init__(self):
        """Initialize a :class:`ConfigurationStore` instance."""
        self.restore_defaults()

    def read_from_file(self):
        """Read values of configuration options from file."""
        if not os.path.isfile(self.path): return
        entries = open(self.path, "r").readlines()
        entries = dict(re.split(" *= *", x.strip(), 1)
                       for x in entries if
                       not x.startswith("#") and "=" in x)

        for name in set(_DEFAULTS) & set(entries):
            decode = type(_DEFAULTS[name])
            setattr(self, name, decode(entries[name]))
        self.version = nfoview.__version__

    def restore_defaults(self):
        """Set all configuration options to their default values."""
        for name in _DEFAULTS:
            setattr(self, name, _DEFAULTS[name])
        self.version = nfoview.__version__

    def write_to_file(self):
        """Write values of configuration options to file."""
        directory = os.path.dirname(self.path)
        if not os.path.isdir(directory):
            try:
                os.makedirs(directory)
            except OSError:
                print("Failed to create directory:", file=sys.stderr)
                traceback.print_exc()
                return
        fobj = open(self.path, "w")
        for name in sorted(_DEFAULTS):
            value = getattr(self, name)
            text = "{} = {}".format(name, str(value))
            if value == _DEFAULTS[name]:
                # Comment out options at default value.
                text = "# {}".format(text)
            fobj.write(text + "\n")
        fobj.close()
