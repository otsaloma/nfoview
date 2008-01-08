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


class TestModule(nfoview.TestCase):

    def test_attributes(self):

        function = nfoview.i18n._
        function("message")
        function = nfoview.i18n.dgettext
        function("domain", "message")
        function = nfoview.i18n.ngettext
        function("singular", "plural", 1)
