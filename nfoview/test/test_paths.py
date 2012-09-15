# -*- coding: utf-8 -*-

# Copyright (C) 2008-2009 Osmo Salomaa
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

import imp
import nfoview
import os
import sys


class TestModule(nfoview.TestCase):

    @nfoview.deco.monkey_patch(sys, "platform")
    def test_config_home_dir__win32(self):
        sys.platform = "win32"
        imp.reload(nfoview.paths)
        assert hasattr(nfoview, "CONFIG_HOME_DIR")

    @nfoview.deco.monkey_patch(os, "environ")
    def test_config_home_dir__xdg_default(self):
        os.environ.clear()
        imp.reload(nfoview.paths)
        assert hasattr(nfoview, "CONFIG_HOME_DIR")

    @nfoview.deco.monkey_patch(os, "environ")
    def test_config_home_dir__xdg_environment(self):
        os.environ["XDG_CONFIG_HOME"] = "xdg"
        imp.reload(nfoview.paths)
        assert hasattr(nfoview, "CONFIG_HOME_DIR")

    def test_data_dir__source(self):
        assert os.path.isdir(nfoview.DATA_DIR)

    def test_locale_dir__source(self):
        assert hasattr(nfoview, "LOCALE_DIR")
