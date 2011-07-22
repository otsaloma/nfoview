# Copyright (C) 2008-2009,2011 Osmo Salomaa
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

"""Reading, writing and storing configurations."""

import nfoview
import os
import re

__all__ = ("ConfigurationStore",)


class ConfigurationStore(object):

    """Reading, writing and storing configurations.

    :cvar path: Path to user's local configuration file

    :ivar background_color: Background color as a hexadecimal string
    :ivar color_scheme: Name of the color scheme used
    :ivar font: Font string in :class:`Pango.FontDescription` format
    :ivar foreground_color: Foreground color as a hexadecimal string
    :ivar link_color: Link color as a hexadecimal string
    :ivar pixels_above_lines: Extra line-spacing above each line
    :ivar pixels_below_lines: Extra line-spacing below each line
    :ivar text_view_max_chars: Maximum width for text view in characters
    :ivar text_view_max_lines: Maximum height for text view in lines
    :ivar version: Version number, same as :data:`nfoview.__version__`
    :ivar visited_link_color: Visited link color as a hexadecimal string
    """

    DEFAULT, DECODE, ENCODE = list(range(3))
    _fields = {"background_color"   : (    "#ffffff", str, str),
               "color_scheme"       : (    "default", str, str),
               "font"               : ("Terminus 12", str, str),
               "foreground_color"   : (    "#000000", str, str),
               "link_color"         : (    "#0000ff", str, str),
               "pixels_above_lines" : (            0, int, str),
               "pixels_below_lines" : (            0, int, str),
               "text_view_max_chars": (          160, int, str),
               "text_view_max_lines": (           45, int, str),
               "version"            : (           "", str, str),
               "visited_link_color" : (    "#ff00ff", str, str),
               }

    path = os.path.join(nfoview.CONFIG_HOME_DIR, "nfoview.conf")

    def __init__(self):
        """Initialize a :class:`ConfigurationStore` instance."""
        self.restore_defaults()

    def read_from_file(self):
        """Read values of configuration options from file."""
        if not os.path.isfile(self.path): return
        entries = open(self.path, "r").readlines()
        entries = [x.strip() for x in entries]
        entries = [x for x in entries if not x.startswith("#")]
        entries = dict(re.split(" *= *", x, 1) for x in entries)
        for name in (set(self._fields) & set(entries)):
            decode = self._fields[name][self.DECODE]
            setattr(self, name, decode(entries[name]))
        self.version = nfoview.__version__

    def restore_defaults(self):
        """Set all configuration options to their default values."""
        for name in self._fields:
            setattr(self, name, self._fields[name][self.DEFAULT])
        self.version = nfoview.__version__

    def write_to_file(self):
        """Write values of configuration options to file."""
        directory = os.path.dirname(self.path)
        if not os.path.isdir(directory):
            try: os.makedirs(directory)
            except OSError: return
        fobj = open(self.path, "w")
        for name in sorted(self._fields):
            value = getattr(self, name)
            encode = self._fields[name][self.ENCODE]
            text = " = ".join((name, encode(value)))
            if value == self._fields[name][self.DEFAULT]:
                # Comment out fields with default values.
                text = "# {0}".format(text)
            fobj.write(text)
            fobj.write(os.linesep)
        fobj.close()
