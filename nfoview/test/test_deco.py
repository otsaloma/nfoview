# Copyright (C) 2009 Osmo Salomaa
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

import nfoview
import os
import sys


class TestModule(nfoview.TestCase):

    def test_monkey_patch__no_attribute(self):
        @nfoview.deco.monkey_patch(sys, "nfoview")
        def modify_nfoview():
            sys.nfoview = True
        modify_nfoview()
        assert not hasattr(sys, "nfoview")

    def test_monkey_patch__os_environ(self):
        @nfoview.deco.monkey_patch(os, "environ")
        def modify_environment():
            os.environ["NFOVIEW_TEST"] = "1"
        modify_environment()
        assert not "NFOVIEW_TEST" in os.environ

    def test_monkey_patch__sys_platform(self):
        platform = sys.platform
        @nfoview.deco.monkey_patch(sys, "platform")
        def modify_platform():
            sys.platform = "commodore_64"
        modify_platform()
        assert sys.platform == platform
