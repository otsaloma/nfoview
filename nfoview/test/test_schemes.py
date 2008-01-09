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


class TestModule(nfoview.TestCase):

    def test_get_color_scheme(self):

        nfoview.schemes.get_color_scheme("default")
        nfoview.schemes.get_color_scheme("custom")

    def test_get_color_schemes__attributes(self):

        schemes = nfoview.schemes.get_color_schemes()
        for scheme in schemes:
            assert hasattr(scheme, "name")
            assert hasattr(scheme, "label")
            assert hasattr(scheme, "foreground")
            assert hasattr(scheme, "background")
            assert hasattr(scheme, "link")
            assert hasattr(scheme, "visited_link")

    def test_get_color_schemes__names(self):

        schemes = nfoview.schemes.get_color_schemes()
        assert schemes[0].name == "default"
        assert schemes[-1].name == "custom"
        names = [x.name for x in schemes]
        assert len(names) == len(set(names))
