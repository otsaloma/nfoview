# Copyright (C) 2008-2009 Osmo Salomaa
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

"""Reading, writing and storing configurations."""

import nfoview
import os

__all__ = ("Configuration",)


class Configuration(object):

    """Reading, writing and storing configurations."""

    _fields = {
        # name: (default value, decode function, encode function)
        "background_color": ("#ffffff", str, str),
        "color_scheme": ("default", str, str),
        "font": ("Terminus 12", str, str),
        "foreground_color": ("#000000", str, str),
        "link_color": ("#0000ff", str, str),
        "pixels_above_lines": (0, int, str),
        "pixels_below_lines": (0, int, str),
        "text_view_max_lines": (40, int, str),
        "version": ("", str, str),
        "visited_link_color": ("#ff00ff", str, str),}

    path = os.path.join(nfoview.CONFIG_DIR, "nfoview.conf")

    def __init__(self):
        """Initialize a Configuration instance."""

        self.background_color = None
        self.color_scheme = None
        self.font = None
        self.foreground_color = None
        self.link_color = None
        self.pixels_above_lines = None
        self.pixels_below_lines = None
        self.version = None
        self.visited_link_color = None

        self.restore_defaults()

    def read_from_file(self):
        """Read values of configuration fields from file."""

        if not os.path.isfile(self.path): return
        entries = open(self.path, "r").readlines()
        entries = [x.strip() for x in entries]
        entries = [x for x in entries if not x.startswith("#")]
        entries = dict(x.split("=", 1) for x in entries)
        for name in (set(self._fields) & set(entries)):
            decode = self._fields[name][1]
            value = decode(entries[name])
            setattr(self, name, value)
        self.version = nfoview.__version__

    def restore_defaults(self):
        """Set all configuration fields to their default values."""

        for name, (value, x, y) in self._fields.items():
            setattr(self, name, value)
        self.version = nfoview.__version__

    def write_to_file(self):
        """Write values of configuration fields to file."""

        directory = os.path.dirname(self.path)
        if not os.path.isdir(directory):
            try: os.makedirs(directory)
            except OSError: return
        fobj = open(self.path, "w")
        for name in sorted(self._fields.keys()):
            value = getattr(self, name)
            encode = self._fields[name][2]
            text = "%s=%s" % (name, encode(value))
            if value == self._fields[name][0]:
                # Comment out fields with default values.
                text = "# %s" % text
            fobj.write(text)
            fobj.write(os.linesep)
        fobj.close()
