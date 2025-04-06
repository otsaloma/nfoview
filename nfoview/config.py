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

import nfoview
import re

from pathlib import Path

DEFAULTS = {
    "background_color": "#ffffff",
    "color_scheme": "default",
    "font": "Cascadia Mono 12",
    "export_scale": 1.0,
    "foreground_color": "#2e3436",
    "link_color": "#2a76c6",
    "pixels_above_lines": 0,
    "pixels_below_lines": 0,
    "text_view_max_chars": 160,
    "text_view_max_lines": 45,
    "version": "",
    "visited_link_color": "#215d9c",
}

class ConfigurationStore:

    path = Path(nfoview.CONFIG_HOME_DIR) / "nfoview.conf"

    def __init__(self, read=False):
        self.restore_defaults()
        if read: self.read()

    def read(self):
        if not self.path.exists(): return
        entries = self.path.read_text().splitlines()
        entries = dict(
            re.split(" *= *", x.strip(), 1)
            for x in entries
            if not x.startswith("#") and "=" in x
        )
        for name in set(DEFAULTS) & set(entries):
            decode = type(DEFAULTS[name])
            setattr(self, name, decode(entries[name]))
        self.version = nfoview.__version__

    def restore_defaults(self):
        for name in DEFAULTS:
            setattr(self, name, DEFAULTS[name])
        self.version = nfoview.__version__

    def write(self):
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with open(self.path, "w") as f:
            for name in sorted(DEFAULTS):
                text = f"{name} = {getattr(self, name)!s}"
                if getattr(self, name) == DEFAULTS[name]:
                    # Comment out options at default value.
                    text = f"# {text}"
                f.write(text + "\n")
