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
import os
import random
import sys


class TestModule(nfoview.TestCase):

    url = "http://home.gna.org/nfoview"

    def browse_url_silent(self, url):

        try: return nfoview.util.browse_url(url)
        except OSError: return None

    def test_affirm(self):

        nfoview.util.affirm(0 == 0)
        error = nfoview.AffirmationError
        self.raises(error, nfoview.util.affirm, 1 == 0)

    def test_browse_url(self):

        nfoview.util.browse_url(self.url)
        nfoview.util.browse_url(self.url, "echo")

    def test_browse_url__command(self):

        environment = os.environ.copy()
        os.environ.clear()
        platform = sys.platform
        sys.platform = "linux2"
        is_command = nfoview.util.is_command
        nfoview.util.is_command = lambda x: (x == "xdg-open")
        self.browse_url_silent(self.url)
        nfoview.util.is_command = lambda x: (x == "exo-open")
        self.browse_url_silent(self.url)
        os.environ = environment
        sys.platform = platform
        nfoview.util.is_command = is_command

    def test_browse_url__environment(self):

        environment = os.environ.copy()
        platform = sys.platform
        sys.platform = "linux2"
        os.environ["GNOME_DESKTOP_SESSION_ID"] = "1"
        self.browse_url_silent(self.url)
        del os.environ["GNOME_DESKTOP_SESSION_ID"]
        os.environ["KDE_FULL_SESSION"] = "1"
        self.browse_url_silent(self.url)
        del os.environ["KDE_FULL_SESSION"]
        print os.environ
        self.browse_url_silent(self.url)
        os.environ = environment
        sys.platform = platform

    def test_browse_url__platform(self):

        environment = os.environ.copy()
        os.environ.clear()
        platform = sys.platform
        sys.platform = "darwin"
        self.browse_url_silent(self.url)
        sys.platform = "win32"
        self.browse_url_silent(self.url)
        os.environ = environment
        sys.platform = platform

    def test_browse_url__webbrowser(self):

        environment = os.environ.copy()
        os.environ.clear()
        platform = sys.platform
        sys.platform = "linux2"
        nfoview.util.browse_url(self.url)
        os.environ = environment
        sys.platform = platform

    def test_detect_encoding_cp437(self):

        path = self.get_nfo_file()
        encoding = nfoview.util.detect_encoding(path)
        assert encoding == "cp437"

    def test_detect_encoding_utf_8(self):

        path = self.get_nfo_file()
        text = open(path, "r").read()
        open(path, "w").write(codecs.BOM_UTF8 + text)
        encoding = nfoview.util.detect_encoding(path)
        assert encoding == "utf_8"

    def test_detect_encoding_utf_16_be(self):

        path = self.get_nfo_file()
        text = open(path, "r").read()
        open(path, "w").write(codecs.BOM_UTF16_BE + text)
        encoding = nfoview.util.detect_encoding(path)
        assert encoding == "utf_16_be"

    def test_detect_encoding_utf_16_le(self):

        path = self.get_nfo_file()
        text = open(path, "r").read()
        open(path, "w").write(codecs.BOM_UTF16_LE + text)
        encoding = nfoview.util.detect_encoding(path)
        assert encoding == "utf_16_le"

    def test_detect_encoding_utf_32_be(self):

        path = self.get_nfo_file()
        text = open(path, "r").read()
        open(path, "w").write(codecs.BOM_UTF32_BE + text)
        encoding = nfoview.util.detect_encoding(path)
        assert encoding == "utf_32_be"

    def test_detect_encoding_utf_32_le(self):

        path = self.get_nfo_file()
        text = open(path, "r").read()
        open(path, "w").write(codecs.BOM_UTF32_LE + text)
        encoding = nfoview.util.detect_encoding(path)
        assert encoding == "utf_32_le"

    def test_gdk_color_to_hex(self):

        gdk_color_to_hex = nfoview.util.gdk_color_to_hex
        for i in range(100):
            r = random.randint(0, 16)
            g = random.randint(0, 16)
            b = random.randint(0, 16)
            string = "#%02x%02x%02x" % (r, g, b)
            color = gtk.gdk.color_parse(string)
            assert gdk_color_to_hex(color) == string

    def test_is_command(self):

        if os.path.isfile("/bin/echo"):
            assert nfoview.util.is_command("echo")
        if os.path.isfile("/usr/bin/python"):
            nfoview.util.is_command("python")
        assert not nfoview.util.is_command("+?")

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
