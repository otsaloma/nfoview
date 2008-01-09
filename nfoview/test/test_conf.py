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

import nfoview
import os
import tempfile


class TestConfiguration(nfoview.TestCase):

    fields = {
        "background_color": "#ff0000",
        "browser": "echo",
        "color_scheme": "default",
        "font": "monospace 12",
        "foreground_color": "#00ff00",
        "link_color": "#0000ff",
        "pixels_above_lines": 1,
        "pixels_below_lines": 0,
        "visited_link_color": "#ffff00",}

    def setup_method(self, method):

        self.temp_dir = tempfile.mkdtemp()
        conf_dir = os.path.join(self.temp_dir, "test")
        nfoview.conf.restore_defaults()
        nfoview.conf.path = os.path.join(conf_dir, "conf")
        for name, value in self.fields.items():
            setattr(nfoview.conf, name, value)

    def teardown_method(self, method):

        from distutils import dir_util
        dir_util.remove_tree(self.temp_dir)

    def test_read_and_write(self):

        nfoview.conf.write_to_file()
        nfoview.conf.restore_defaults()
        nfoview.conf.read_from_file()
        for name, value in self.fields.items():
            assert getattr(nfoview.conf, name) == value

    def test_restore_defaults(self):

        nfoview.conf.restore_defaults()
        for name, attrs in nfoview.conf._fields.items():
            if name == "version": continue
            assert getattr(nfoview.conf, name) == attrs[0]
        assert nfoview.conf.version == nfoview.__version__

    def test_write__os_error(self):

        directory = os.path.dirname(nfoview.conf.path)
        directory = os.path.abspath(os.path.join(directory, ".."))
        os.chmod(directory, 0000)
        nfoview.conf.write_to_file()
        os.chmod(directory, 0777)
