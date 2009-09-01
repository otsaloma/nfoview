# Copyright (C) 2005-2009 Osmo Salomaa
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
        self.window = nfoview.Window(self.new_temp_nfo_file())

    def test___init____no_file(self):
        nfoview.Window()

    def test__on_close_document_activate(self):
        self.window._get_action("close_document").activate()

    def test__on_copy_text_activate(self):
        self.window._get_action("select_all_text").activate()
        self.window._get_action("copy_text").activate()

    def test__on_edit_preferences_activate(self):
        self.window._get_action("edit_preferences").activate()
        self.window._get_action("edit_preferences").activate()
        self.window._preferences_dialog.response(gtk.RESPONSE_CLOSE)
        self.window._get_action("edit_preferences").activate()

    @nfoview.deco.monkey_patch(nfoview, "OpenDialog")
    def test__on_open_file_activate__cancel(self):
        nfoview.OpenDialog.run = lambda *args: gtk.RESPONSE_CANCEL
        self.window._get_action("open_file").activate()

    def test__on_quit_activate(self):
        nfoview.main.windows.append(self.window)
        self.window._get_action("quit").activate()

    def test__on_select_all_text_activate(self):
        self.window._get_action("select_all_text").activate()

    def test__on_show_about_dialog_activate(self):
        self.window._get_action("show_about_dialog").activate()
        self.window._get_action("show_about_dialog").activate()
        self.window._about_dialog.response(gtk.RESPONSE_CLOSE)
        self.window._get_action("show_about_dialog").activate()

    def test__on_wrap_lines_activate(self):
        self.window._get_action("wrap_lines").activate()
        self.window._get_action("wrap_lines").activate()
        self.window._get_action("wrap_lines").activate()

    def test_open_file__blank_lines(self):
        path = self.new_temp_nfo_file()
        fobj = open(path, "a")
        fobj.write("\n\n\n")
        fobj.close()
        self.window.open_file(path)

    def test_open_file__even_lines(self):
        path = self.new_temp_nfo_file()
        fobj = open(path, "a")
        fobj.write("\na\n\na\n\n")
        fobj.close()
        self.window.open_file(path)

    def test_open_file__odd_lines(self):
        path = self.new_temp_nfo_file()
        fobj = open(path, "w")
        fobj.write("a\n\na\n\n")
        fobj.close()
        self.window.open_file(path)

    def test_resize_to_text__blank(self):
        self.window = nfoview.Window()
        self.window.resize_to_text()

    def test_resize_to_text__long_file(self):
        path = self.new_temp_nfo_file()
        fobj = open(path, "w")
        fobj.write("aaa\n" * 100)
        fobj.close()
        self.window.open_file(path)
        self.window.resize_to_text()

    def test_resize_to_text__long_lines(self):
        path = self.new_temp_nfo_file()
        fobj = open(path, "w")
        fobj.write("aaa " * 100)
        fobj.close()
        self.window.open_file(path)
        self.window.resize_to_text()
