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
import shutil
import tempfile

from gi.repository import Gdk
from gi.repository import Gtk
from unittest.mock import patch


class TestModule(nfoview.TestCase):

    def test_affirm__false(self):
        """
        Test if the nfov.

        Args:
            self: (todo): write your description
        """
        self.assert_raises(nfoview.AffirmationError,
                           nfoview.util.affirm,
                           False)

    def test_affirm__true(self):
        """
        Test if the number of the number of the nfov.

        Args:
            self: (todo): write your description
        """
        nfoview.util.affirm(True)

    def test_apply_style__label(self):
        """
        Applies the style of the style

        Args:
            self: (todo): write your description
        """
        nfoview.util.apply_style(Gtk.Label())

    def test_apply_style__text_view(self):
        """
        Applies the style to the style

        Args:
            self: (todo): write your description
        """
        nfoview.util.apply_style(Gtk.TextView())

    def test_detect_encoding__cp437(self):
        """
        Check if the encoding of - encoding

        Args:
            self: (todo): write your description
        """
        path = self.new_nfo_file()
        encoding = nfoview.util.detect_encoding(path)
        assert encoding == "cp437"

    @patch("nfoview.util.is_valid_encoding", lambda x: True)
    def test_detect_encoding__utf_16_be(self):
        """
        Check if the encoding of the file.

        Args:
            self: (todo): write your description
        """
        path = self.new_nfo_file()
        blob = open(path, "rb").read()
        open(path, "wb").write(codecs.BOM_UTF16_BE + blob)
        encoding = nfoview.util.detect_encoding(path)
        assert encoding == "utf_16_be"

    @patch("nfoview.util.is_valid_encoding", lambda x: True)
    def test_detect_encoding__utf_16_le(self):
        """
        Test if the encoding of the encoding of the utf - wise.

        Args:
            self: (todo): write your description
        """
        path = self.new_nfo_file()
        blob = open(path, "rb").read()
        open(path, "wb").write(codecs.BOM_UTF16_LE + blob)
        encoding = nfoview.util.detect_encoding(path)
        assert encoding == "utf_16_le"

    @patch("nfoview.util.is_valid_encoding", lambda x: True)
    def test_detect_encoding__utf_32_be(self):
        """
        Test if the encoding of the encoding of the file.

        Args:
            self: (todo): write your description
        """
        path = self.new_nfo_file()
        blob = open(path, "rb").read()
        open(path, "wb").write(codecs.BOM_UTF32_BE + blob)
        encoding = nfoview.util.detect_encoding(path)
        assert encoding == "utf_32_be"

    @patch("nfoview.util.is_valid_encoding", lambda x: True)
    def test_detect_encoding__utf_32_le(self):
        """
        Test if the encoding of the given encoding.

        Args:
            self: (todo): write your description
        """
        path = self.new_nfo_file()
        blob = open(path, "rb").read()
        open(path, "wb").write(codecs.BOM_UTF32_LE + blob)
        encoding = nfoview.util.detect_encoding(path)
        assert encoding == "utf_32_le"

    @patch("nfoview.util.is_valid_encoding", lambda x: True)
    def test_detect_encoding__utf_8_sig(self):
        """
        Test if the encoding of the given.

        Args:
            self: (todo): write your description
        """
        path = self.new_nfo_file()
        blob = open(path, "rb").read()
        open(path, "wb").write(codecs.BOM_UTF8 + blob)
        encoding = nfoview.util.detect_encoding(path)
        assert encoding == "utf_8_sig"

    def test_get_max_text_view_size(self):
        """
        Returns the width of the text in the view

        Args:
            self: (todo): write your description
        """
        width, height = nfoview.util.get_max_text_view_size()
        assert width > 100 and height > 100

    def test_get_text_view_size(self):
        """
        Get the width of the text in the window.

        Args:
            self: (todo): write your description
        """
        text = 25 * "qwertyuiop asdfghjkl zxcvbnm\n"
        width, height = nfoview.util.get_text_view_size(text)
        assert width > 100 and height > 100

    def test_hex_to_rgba(self):
        """
        Convert the rgb color to rgba color.

        Args:
            self: (todo): write your description
        """
        color = nfoview.util.hex_to_rgba("#ff0000")
        assert color.equal(Gdk.RGBA(red=1, green=0, blue=0, alpha=1))

    def test_makedirs__create(self):
        """
        Create a temporary directory.

        Args:
            self: (todo): write your description
        """
        root = tempfile.mkdtemp()
        directory = os.path.join(root, "test")
        assert not os.path.isdir(directory)
        nfoview.util.makedirs(directory)
        assert os.path.isdir(directory)
        shutil.rmtree(root)

    def test_makedirs__exists(self):
        """
        Creates a directory if it does not exist.

        Args:
            self: (todo): write your description
        """
        directory = tempfile.mkdtemp()
        assert os.path.isdir(directory)
        nfoview.util.makedirs(directory)
        assert os.path.isdir(directory)
        shutil.rmtree(directory)

    def test_rgba_to_hex(self):
        """
        Convert a hex color to a hex color.

        Args:
            self: (todo): write your description
        """
        rgba = Gdk.RGBA(red=1, green=0, blue=1)
        color = nfoview.util.rgba_to_hex(rgba)
        assert color == "#ff00ff"

    @patch("sys.platform", "linux2")
    def test_show_uri__unix(self):
        """
        Gets the test uri.

        Args:
            self: (todo): write your description
        """
        nfoview.util.show_uri("https://otsaloma.io/nfoview/")

    @patch("sys.platform", "win32")
    def test_show_uri__windows(self):
        """
        Gets the uri of a given load balancer.

        Args:
            self: (todo): write your description
        """
        nfoview.util.show_uri("https://otsaloma.io/nfoview/")

    @patch("sys.platform", "linux2")
    def test_uri_to_path__unix(self):
        """
        Return the path to the uri of the uri.

        Args:
            self: (todo): write your description
        """
        uri = "file:///home/nfoview/a%20file.nfo"
        path = nfoview.util.uri_to_path(uri)
        assert path == "/home/nfoview/a file.nfo"

    @patch("sys.platform", "win32")
    def test_uri_to_path__windows(self):
        """
        Return the path to the uri.

        Args:
            self: (todo): write your description
        """
        uri = "file:///c:/nfoview/a%20file.nfo"
        path = nfoview.util.uri_to_path(uri)
        assert path == "c:\\nfoview\\a file.nfo"
