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

import gtk
import nfoview


class TestAboutDialog(nfoview.TestCase):

    def setup_method(self, method):

        self.dialog = nfoview.AboutDialog(gtk.Window())

    def test__on_url_clicked(self):

        # pylint: disable-msg=E1101
        vbox = self.dialog.vbox.get_children()[0]
        hbox = vbox.get_children()[-1]
        link_button = hbox.get_children()[0]
        link_button.clicked()
