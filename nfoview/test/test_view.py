# Copyright (C) 2005-2007 Osmo Salomaa
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


class TestTextView(nfoview.TestCase):

    def setup_method(self, method):

        self.view = nfoview.TextView()
        self.view.set_text("test www.test.org")

    def test_get_text(self):

        self.view.set_text("test")
        assert self.view.get_text() == "test"

    def test_set_text(self):

        self.view.set_text("test and rest")
        self.view.set_text("test\nwww.test.org")
        self.view.set_text("test\nhttp://www.test.org")

    def test_update_colors(self):

        self.view.update_colors()
        lst = self.view._link_tags
        self.view._link_tags = []
        self.view._visited_link_tags = lst
        self.view.update_colors()
