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

DEFAULTS = dict(
    background_color="#ffffff",
    color_scheme="default",
    font="Terminus 12",
    foreground_color="#2e3436",
    link_color="#2a76c6",
    pixels_above_lines=0,
    pixels_below_lines=0,
    text_view_max_chars=160,
    text_view_max_lines=45,
    version="",
    visited_link_color="#215d9c",
)


class ConfigurationStore:

    """Reading, writing and storing configurations."""

    path = os.path.join(nfoview.CONFIG_HOME_DIR, "nfoview.conf")

    def __init__(self, read=False):
        """Initialize a :class:`ConfigurationStore` instance."""
        self.restore_defaults()
        if read: self.read()

    def read(self):
        """Read values of configuration options from file."""
        if not os.path.isfile(self.path): return
        with open(self.path, "r") as f:
            entries = f.readlines()
        entries = dict(re.split(" *= *", x.strip(), 1)
                       for x in entries if
                       not x.startswith("#") and "=" in x)

        for name in set(DEFAULTS) & set(entries):
            decode = type(DEFAULTS[name])
            setattr(self, name, decode(entries[name]))
        self.version = nfoview.__version__

    def restore_defaults(self):
        """Set all configuration options to their default values."""
        for name in DEFAULTS:
            setattr(self, name, DEFAULTS[name])
        self.version = nfoview.__version__

    def write(self):
        """Write values of configuration options to file."""
        directory = os.path.dirname(self.path)
        try:
            if not os.path.isdir(directory):
                os.makedirs(directory)
        except OSError:
            print("Failed to create directory:", file=sys.stderr)
            traceback.print_exc()
            return
        f = open(self.path, "w")
        for name in sorted(DEFAULTS):
            text = "{} = {}".format(name, str(getattr(self, name)))
            if getattr(self, name) == DEFAULTS[name]:
                # Comment out options at default value.
                text = "# {}".format(text)
            f.write(text + "\n")
        f.close()
