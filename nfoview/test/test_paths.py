# Copyright (C) 2007 Osmo Salomaa
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


class TestModule(nfoview.TestCase):

    def test_attributes__no_environment(self):

        environment = os.environ.copy()
        os.environ.clear()
        assert hasattr(nfoview, "CONFIG_DIR")
        assert os.path.isdir(nfoview.DATA_DIR)
        assert hasattr(nfoview, "LOCALE_DIR")
        os.environ = environment

    def test_attributes__xdg_environment(self):

        environment = os.environ.copy()
        os.environ.clear()
        os.environ["XDG_CONFIG_HOME"] = "xdg"
        reload(nfoview.paths)
        assert hasattr(nfoview, "CONFIG_DIR")
        os.environ = environment
