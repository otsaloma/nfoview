# -*- coding: utf-8 -*-

# Copyright (C) 2005-2009,2011 Osmo Salomaa
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

import codecs
import nfoview
import sys

from gi.repository import Gdk
from gi.repository import Gtk


class TestModule(nfoview.TestCase):

    def test_affirm__false(self):
        self.assert_raises(nfoview.AffirmationError,
                           nfoview.util.affirm,
                           1 == 0)

    def test_affirm__true(self):
        nfoview.util.affirm(0 == 0)

    def test_connect__private(self):
        self._on_window_delete_event = lambda *args: None
        self.window = Gtk.Window()
        nfoview.util.connect(self, "window", "delete-event")

    def test_connect__public(self):
        self.on_window_delete_event = lambda *args: None
        self.window = Gtk.Window()
        nfoview.util.connect(self, "window", "delete-event")

    def test_detect_encoding__cp437(self):
        path = self.new_nfo_file()
        encoding = nfoview.util.detect_encoding(path)
        assert encoding == "cp437"

    @nfoview.deco.monkey_patch(nfoview.util, "is_valid_encoding")
    def test_detect_encoding__utf_16_be(self):
        nfoview.util.is_valid_encoding = lambda x: True
        path = self.new_nfo_file()
        blob = open(path, "rb").read()
        open(path, "wb").write(codecs.BOM_UTF16_BE + blob)
        encoding = nfoview.util.detect_encoding(path)
        assert encoding == "utf_16_be"

    @nfoview.deco.monkey_patch(nfoview.util, "is_valid_encoding")
    def test_detect_encoding__utf_16_le(self):
        nfoview.util.is_valid_encoding = lambda x: True
        path = self.new_nfo_file()
        blob = open(path, "rb").read()
        open(path, "wb").write(codecs.BOM_UTF16_LE + blob)
        encoding = nfoview.util.detect_encoding(path)
        assert encoding == "utf_16_le"

    @nfoview.deco.monkey_patch(nfoview.util, "is_valid_encoding")
    def test_detect_encoding__utf_32_be(self):
        nfoview.util.is_valid_encoding = lambda x: True
        path = self.new_nfo_file()
        blob = open(path, "rb").read()
        open(path, "wb").write(codecs.BOM_UTF32_BE + blob)
        encoding = nfoview.util.detect_encoding(path)
        assert encoding == "utf_32_be"

    @nfoview.deco.monkey_patch(nfoview.util, "is_valid_encoding")
    def test_detect_encoding__utf_32_le(self):
        nfoview.util.is_valid_encoding = lambda x: True
        path = self.new_nfo_file()
        blob = open(path, "rb").read()
        open(path, "wb").write(codecs.BOM_UTF32_LE + blob)
        encoding = nfoview.util.detect_encoding(path)
        assert encoding == "utf_32_le"

    @nfoview.deco.monkey_patch(nfoview.util, "is_valid_encoding")
    def test_detect_encoding__utf_8_sig(self):
        nfoview.util.is_valid_encoding = lambda x: True
        path = self.new_nfo_file()
        blob = open(path, "rb").read()
        open(path, "wb").write(codecs.BOM_UTF8 + blob)
        encoding = nfoview.util.detect_encoding(path)
        assert encoding == "utf_8_sig"

    def test_get_color_scheme__custom(self):
        scheme = nfoview.util.get_color_scheme("custom")
        assert scheme is nfoview.CustomScheme

    def test_get_color_scheme__default(self):
        scheme = nfoview.util.get_color_scheme("default")
        assert scheme is nfoview.DefaultScheme

    def test_get_color_scheme__value_error(self):
        self.assert_raises(ValueError,
                           nfoview.util.get_color_scheme,
                           "xxx")

    def test_get_color_schemes(self):
        schemes = nfoview.util.get_color_schemes()
        assert schemes[ 0] is nfoview.DefaultScheme
        assert schemes[-1] is nfoview.CustomScheme

    @nfoview.deco.monkey_patch(nfoview.conf, "font")
    def test_get_font_description(self):
        nfoview.conf.font = "Foo"
        font_desc = nfoview.util.get_font_description()
        assert font_desc.get_family() == "Foo,monospace,"

    def test_hex_to_rgba(self):
        color = nfoview.util.hex_to_rgba("#ff0000")
        assert color.equal(Gdk.RGBA(red=1, green=0, blue=0, alpha=1))

    def test_hex_to_rgba__value_error(self):
        self.assert_raises(ValueError,
                           nfoview.util.hex_to_rgba,
                           "xxx")

    def test_is_valid_encoding__false(self):
        assert not nfoview.util.is_valid_encoding("xxx")

    def test_is_valid_encoding__true(self):
        assert nfoview.util.is_valid_encoding("ascii")
        assert nfoview.util.is_valid_encoding("cp437")
        assert nfoview.util.is_valid_encoding("utf_8")

    def test_lookup_color__fallback(self):
        color = nfoview.util.lookup_color("xxx", "#ff0000")
        assert color.equal(Gdk.RGBA(red=1, green=0, blue=0, alpha=1))

    def test_lookup_color__found_base_color(self):
        color = nfoview.util.lookup_color("base_color", "#ffffff")
        assert isinstance(color, Gdk.RGBA)

    def test_lookup_color__found_theme_base_color(self):
        color = nfoview.util.lookup_color("theme_base_color", "#ffffff")
        assert isinstance(color, Gdk.RGBA)

    def test_lookup_color__value_error(self):
        self.assert_raises(ValueError,
                           nfoview.util.lookup_color,
                           "xxx",
                           "xxx")

    def test_rgba_to_color(self):
        rgba = Gdk.RGBA(red=1, green=0, blue=0, alpha=1)
        color = nfoview.util.rgba_to_color(rgba)
        assert color.equal(Gdk.Color(red=65535, green=0, blue=0))

    def test_rgba_to_hex__black(self):
        rgba = Gdk.RGBA(red=0, green=0, blue=0)
        color = nfoview.util.rgba_to_hex(rgba)
        assert color == "#000000"

    def test_rgba_to_hex__violet(self):
        rgba = Gdk.RGBA(red=1, green=0, blue=1)
        color = nfoview.util.rgba_to_hex(rgba)
        assert color == "#ff00ff"

    @nfoview.deco.monkey_patch(sys, "platform")
    def test_show_uri__unix(self):
        sys.platform = "linux2"
        nfoview.util.show_uri("http://home.gna.org/nfoview/")

    @nfoview.deco.monkey_patch(sys, "platform")
    def test_show_uri__windows(self):
        sys.platform = "win32"
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
