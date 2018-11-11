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
import os
import shutil
import tempfile

FIELDS = {
    "background_color": "#ff0000",
    "color_scheme": "default",
    "font": "monospace 12",
    "foreground_color": "#00ff00",
    "link_color": "#0000ff",
    "pixels_above_lines": 1,
    "pixels_below_lines": 0,
    "text_view_max_chars": 160,
    "text_view_max_lines": 45,
    "visited_link_color": "#ffff00",
}


class TestConfigurationStore(nfoview.TestCase):

    def setup_method(self, method):
        self.temp_dir = tempfile.mkdtemp()
        nfoview.conf.path = os.path.join(
            self.temp_dir, "nfoview", "nfoview.conf")
        nfoview.conf.restore_defaults()
        for name, value in list(FIELDS.items()):
            setattr(nfoview.conf, name, value)

    def teardown_method(self, method):
        shutil.rmtree(self.temp_dir)

    def test_read(self):
        nfoview.conf.write()
        nfoview.conf.restore_defaults()
        nfoview.conf.read()
        for name, value in FIELDS.items():
            assert getattr(nfoview.conf, name) == value

    def test_restore_defaults(self):
        nfoview.conf.restore_defaults()
        defaults = dict(nfoview.config.DEFAULTS)
        defaults["version"] = nfoview.__version__
        for name, value in defaults.items():
            assert getattr(nfoview.conf, name) == value

    def test_write(self):
        nfoview.conf.write()
        nfoview.conf.restore_defaults()
        nfoview.conf.read()
        for name, value in FIELDS.items():
            assert getattr(nfoview.conf, name) == value
