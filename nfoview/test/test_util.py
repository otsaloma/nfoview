# -*- coding: utf-8 -*-

# Copyright (C) 2005 Osmo Salomaa
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

import codecs
import nfoview
import os
import sys

from gi.repository import Gdk


class TestModule(nfoview.TestCase):

    def test_affirm__false(self):
        self.assert_raises(nfoview.AffirmationError,
                           nfoview.util.affirm,
                           False)

    def test_affirm__true(self):
        nfoview.util.affirm(True)

    def test_detect_encoding__cp437(self):
        path = self.new_nfo_file()
        encoding = nfoview.util.detect_encoding(path)
        assert encoding == "cp437"

    @nfoview.util.monkey_patch(nfoview.util, "is_valid_encoding")
    def test_detect_encoding__utf_16_be(self):
        nfoview.util.is_valid_encoding = lambda x: True
        path = self.new_nfo_file()
        blob = open(path, "rb").read()
        open(path, "wb").write(codecs.BOM_UTF16_BE + blob)
        encoding = nfoview.util.detect_encoding(path)
        assert encoding == "utf_16_be"

    @nfoview.util.monkey_patch(nfoview.util, "is_valid_encoding")
    def test_detect_encoding__utf_16_le(self):
        nfoview.util.is_valid_encoding = lambda x: True
        path = self.new_nfo_file()
        blob = open(path, "rb").read()
        open(path, "wb").write(codecs.BOM_UTF16_LE + blob)
        encoding = nfoview.util.detect_encoding(path)
        assert encoding == "utf_16_le"

    @nfoview.util.monkey_patch(nfoview.util, "is_valid_encoding")
    def test_detect_encoding__utf_32_be(self):
        nfoview.util.is_valid_encoding = lambda x: True
        path = self.new_nfo_file()
        blob = open(path, "rb").read()
        open(path, "wb").write(codecs.BOM_UTF32_BE + blob)
        encoding = nfoview.util.detect_encoding(path)
        assert encoding == "utf_32_be"

    @nfoview.util.monkey_patch(nfoview.util, "is_valid_encoding")
    def test_detect_encoding__utf_32_le(self):
        nfoview.util.is_valid_encoding = lambda x: True
        path = self.new_nfo_file()
        blob = open(path, "rb").read()
        open(path, "wb").write(codecs.BOM_UTF32_LE + blob)
        encoding = nfoview.util.detect_encoding(path)
        assert encoding == "utf_32_le"

    @nfoview.util.monkey_patch(nfoview.util, "is_valid_encoding")
    def test_detect_encoding__utf_8_sig(self):
        nfoview.util.is_valid_encoding = lambda x: True
        path = self.new_nfo_file()
        blob = open(path, "rb").read()
        open(path, "wb").write(codecs.BOM_UTF8 + blob)
        encoding = nfoview.util.detect_encoding(path)
        assert encoding == "utf_8_sig"

    @nfoview.util.monkey_patch(nfoview.conf, "font")
    def test_get_font_description(self):
        nfoview.conf.font = "Foo"
        font_desc = nfoview.util.get_font_description()
        assert font_desc.get_family() == "Foo,monospace,"

    def test_hex_to_rgba(self):
        color = nfoview.util.hex_to_rgba("#ff0000")
        assert color.equal(Gdk.RGBA(red=1, green=0, blue=0, alpha=1))

    def test_lookup_color(self):
        color = nfoview.util.lookup_color("theme_fg_color", "#ff0000")
        assert not color.equal(Gdk.RGBA(red=1, green=0, blue=0, alpha=1))

    def test_lookup_color_fallback(self):
        color = nfoview.util.lookup_color("xxx", "#ff0000")
        assert color.equal(Gdk.RGBA(red=1, green=0, blue=0, alpha=1))

    def test_monkey_patch__no_attribute(self):
        @nfoview.util.monkey_patch(sys, "nfoview")
        def modify_nfoview():
            sys.nfoview = True
        modify_nfoview()
        assert not hasattr(sys, "nfoview")

    def test_monkey_patch__os_environ(self):
        @nfoview.util.monkey_patch(os, "environ")
        def modify_environment():
            os.environ["NFOVIEW_TEST"] = "1"
        modify_environment()
        assert not "NFOVIEW_TEST" in os.environ

    def test_monkey_patch__sys_platform(self):
        platform = sys.platform
        @nfoview.util.monkey_patch(sys, "platform")
        def modify_platform():
            sys.platform = "commodore_64"
        modify_platform()
        assert sys.platform == platform

    def test_rgba_to_hex(self):
        rgba = Gdk.RGBA(red=1, green=0, blue=1)
        color = nfoview.util.rgba_to_hex(rgba)
        assert color == "#ff00ff"

    @nfoview.util.monkey_patch(sys, "platform")
    def test_show_uri__unix(self):
        sys.platform = "linux2"
        nfoview.util.show_uri("http://github.com/otsaloma/nfoview")

    @nfoview.util.monkey_patch(sys, "platform")
    def test_show_uri__windows(self):
        sys.platform = "win32"
        nfoview.util.show_uri("http://github.com/otsaloma/nfoview")

    @nfoview.util.monkey_patch(sys, "platform")
    def test_uri_to_path__unix(self):
        sys.platform = "linux2"
        uri = "file:///home/nfoview/a%20file.nfo"
        path = nfoview.util.uri_to_path(uri)
        assert path == "/home/nfoview/a file.nfo"

    @nfoview.util.monkey_patch(sys, "platform")
    def test_uri_to_path__windows(self):
        sys.platform = "win32"
        uri = "file:///c:/nfoview/a%20file.nfo"
        path = nfoview.util.uri_to_path(uri)
        assert path == "c:\\nfoview\\a file.nfo"
