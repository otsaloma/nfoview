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

import codecs
import gtk
import nfoview
import sys


class TestModule(nfoview.TestCase):

    def test_affirm__false(self):
        self.raises(nfoview.AffirmationError,
                    nfoview.util.affirm,
                    1 == 0)

    def test_affirm__true(self):
        nfoview.util.affirm(0 == 0)

    def test_connect__private(self):
        # pylint: disable=W0201
        self._on_window_delete_event = lambda *args: None
        self.window = gtk.Window()
        nfoview.util.connect(self, "window", "delete-event")

    def test_connect__public(self):
        # pylint: disable=W0201
        self.on_window_delete_event = lambda *args: None
        self.window = gtk.Window()
        nfoview.util.connect(self, "window", "delete-event")

    def test_detect_encoding__cp437(self):
        path = self.new_temp_nfo_file()
        encoding = nfoview.util.detect_encoding(path)
        assert encoding == "cp437"

    @nfoview.deco.monkey_patch(nfoview.util, "is_valid_encoding")
    def test_detect_encoding__utf_16_be(self):
        nfoview.util.is_valid_encoding = lambda x: True
        path = self.new_temp_nfo_file()
        text = open(path, "r").read()
        open(path, "w").write(codecs.BOM_UTF16_BE + text)
        encoding = nfoview.util.detect_encoding(path)
        assert encoding == "utf_16_be"

    @nfoview.deco.monkey_patch(nfoview.util, "is_valid_encoding")
    def test_detect_encoding__utf_16_le(self):
        nfoview.util.is_valid_encoding = lambda x: True
        path = self.new_temp_nfo_file()
        text = open(path, "r").read()
        open(path, "w").write(codecs.BOM_UTF16_LE + text)
        encoding = nfoview.util.detect_encoding(path)
        assert encoding == "utf_16_le"

    @nfoview.deco.monkey_patch(nfoview.util, "is_valid_encoding")
    def test_detect_encoding__utf_32_be(self):
        nfoview.util.is_valid_encoding = lambda x: True
        path = self.new_temp_nfo_file()
        text = open(path, "r").read()
        open(path, "w").write(codecs.BOM_UTF32_BE + text)
        encoding = nfoview.util.detect_encoding(path)
        assert encoding == "utf_32_be"

    @nfoview.deco.monkey_patch(nfoview.util, "is_valid_encoding")
    def test_detect_encoding__utf_32_le(self):
        nfoview.util.is_valid_encoding = lambda x: True
        path = self.new_temp_nfo_file()
        text = open(path, "r").read()
        open(path, "w").write(codecs.BOM_UTF32_LE + text)
        encoding = nfoview.util.detect_encoding(path)
        assert encoding == "utf_32_le"

    @nfoview.deco.monkey_patch(nfoview.util, "is_valid_encoding")
    def test_detect_encoding__utf_8_sig(self):
        nfoview.util.is_valid_encoding = lambda x: True
        path = self.new_temp_nfo_file()
        text = open(path, "r").read()
        open(path, "w").write(codecs.BOM_UTF8 + text)
        encoding = nfoview.util.detect_encoding(path)
        assert encoding == "utf_8_sig"

    def test_gdk_color_to_hex__black(self):
        color = gtk.gdk.Color(0, 0, 0)
        color = nfoview.util.gdk_color_to_hex(color)
        assert color == "#000000"

    def test_gdk_color_to_hex__violet(self):
        color = gtk.gdk.Color(65535, 0, 65535)
        color = nfoview.util.gdk_color_to_hex(color)
        assert color == "#ff00ff"

    def test_gdk_color_to_hex__white(self):
        color = gtk.gdk.Color(65535, 65535, 65535)
        color = nfoview.util.gdk_color_to_hex(color)
        assert color == "#ffffff"

    def test_gdk_color_to_hex__yellow(self):
        color = gtk.gdk.Color(65535, 65535, 0)
        color = nfoview.util.gdk_color_to_hex(color)
        assert color == "#ffff00"

    def test_get_color_scheme(self):
        scheme = nfoview.util.get_color_scheme("custom")
        assert scheme is nfoview.CustomScheme
        scheme = nfoview.util.get_color_scheme("default")
        assert scheme is nfoview.DefaultScheme

    def test_get_color_scheme__value_error(self):
        self.raises(ValueError, nfoview.util.get_color_scheme, "xxx")

    @nfoview.deco.monkey_patch(nfoview.conf, "font")
    def test_get_font_description(self):
        nfoview.conf.font = "Foo"
        font_desc = nfoview.util.get_font_description()
        assert font_desc.get_family() == "Foo,monospace"

    def test_color_schemes(self):
        schemes = nfoview.util.get_color_schemes()
        assert schemes[0] is nfoview.DefaultScheme
        assert schemes[-1] is nfoview.CustomScheme

    def test_is_valid_encoding__false(self):
        assert not nfoview.util.is_valid_encoding("xxx")

    def test_is_valid_encoding__true(self):
        assert nfoview.util.is_valid_encoding("ascii")
        assert nfoview.util.is_valid_encoding("cp437")
        assert nfoview.util.is_valid_encoding("utf_8")

    def test_show_uri(self):
        nfoview.util.show_uri("http://home.gna.org/nfoview/")

    @nfoview.deco.monkey_patch(sys, "platform")
    def test_uri_to_path__unix(self):
        sys.platform = "linux2"
        uri = "file:///home/nfoview/a%20file.nfo"
        path = nfoview.util.uri_to_path(uri)
        assert path == "/home/nfoview/a file.nfo"

    @nfoview.deco.monkey_patch(sys, "platform")
    def test_uri_to_path__windows(self):
        sys.platform = "win32"
        uri = "file:///c:/nfoview/a%20file.nfo"
        path = nfoview.util.uri_to_path(uri)
        assert path == "c:\\nfoview\\a file.nfo"
