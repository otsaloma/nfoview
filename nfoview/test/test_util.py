# Copyright (C) 2005-2008 Osmo Salomaa
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
import sys


class TestModule(nfoview.TestCase):

    url = "http://home.gna.org/nfoview"

    def test__command_exists(self):

        if os.path.isfile("/bin/sh"):
            assert nfoview.util._command_exists("sh")
        assert not nfoview.util._command_exists("+?")

    def test_browse_url(self):

        nfoview.util.browse_url(self.url)
        nfoview.util.browse_url(self.url, "echo")
        environment = os.environ.copy()
        os.environ.clear()
        nfoview.util.browse_url(self.url)
        os.environ = environment

    def test_uri_to_path__unix(self):

        platform = sys.platform
        sys.platform = "linux2"
        uri = "file:///home/tester/a%20file.ext"
        path = nfoview.util.uri_to_path(uri)
        assert path == "/home/tester/a file.ext"
        sys.platform = platform

    def test_uri_to_path__windows(self):

        platform = sys.platform
        sys.platform = "win32"
        uri = "file:///c:/tester/a%20file.ext"
        path = nfoview.util.uri_to_path(uri)
        assert path == "c:\\tester\\a file.ext"
        sys.platform = platform
