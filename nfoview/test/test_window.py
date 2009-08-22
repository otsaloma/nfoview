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

import gtk
import nfoview


class TestWindow(nfoview.TestCase):

    def setup_method(self, method):

        self.window = nfoview.Window(self.get_nfo_file())

    def test___init__(self):

        nfoview.Window()
        nfoview.Window(self.get_nfo_file())

    def test__init_signal_handlers(self):

        text_buffer = self.window.view.get_buffer()
        bounds = text_buffer.get_bounds()
        text_buffer.select_range(*bounds)

    def test__on_close_document_activate(self):

        path = "/ui/menubar/file/close"
        self.window._uim.get_action(path).activate()

    def test__on_edit_preferences_activate(self):

        path = "/ui/menubar/edit/preferences"
        self.window._uim.get_action(path).activate()
        self.window._uim.get_action(path).activate()
        self.window._preferences_dialog.response(gtk.RESPONSE_CLOSE)

    def test__on_copy_text_activate(self):

        path = "/ui/menubar/edit/select_all"
        self.window._uim.get_action(path).activate()
        path = "/ui/menubar/edit/copy"
        self.window._uim.get_action(path).activate()

    def test__on_select_all_text_activate(self):

        path = "/ui/menubar/edit/select_all"
        self.window._uim.get_action(path).activate()

    def test__on_show_about_dialog_activate(self):

        path = "/ui/menubar/help/about"
        self.window._uim.get_action(path).activate()
        self.window._uim.get_action(path).activate()
        self.window._about_dialog.response(gtk.RESPONSE_CLOSE)

    def test_open_file(self):

        self.window.open_file(self.get_nfo_file())

    def test_open_file__blank_lines(self):

        path = self.get_nfo_file()
        fobj = open(path, "a")
        fobj.write("\n\n\n")
        fobj.close()
        self.window.open_file(path)

    def test_open_file__even_lines(self):

        path = self.get_nfo_file()
        fobj = open(path, "w")
        fobj.write("\na\n\na\n\n")
        fobj.close()
        self.window.open_file(path)

    def test_open_file__odd_lines(self):

        path = self.get_nfo_file()
        fobj = open(path, "w")
        fobj.write("a\n\na\n\n")
        fobj.close()
        self.window.open_file(path)

    def test_resize_to_text(self):

        self.window.resize_to_text()

    def test_resize_to_text__long_lines(self):

        path = self.get_nfo_file()
        fobj = open(path, "w")
        fobj.write("aaa " * 100)
        fobj.close()
        self.window.open_file(path)
        self.window.resize_to_text()
