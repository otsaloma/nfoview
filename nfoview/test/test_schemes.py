# -*- coding: utf-8 -*-

# Copyright (C) 2008-2009,2011 Osmo Salomaa
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

import nfoview

from gi.repository import Gdk


class  _TestScheme(nfoview.TestCase):

    def test_name(self):
        assert isinstance(self.scheme.name, str)

    def test_label(self):
        assert isinstance(self.scheme.label, str)

    def test_foreground(self):
        assert isinstance(self.scheme.foreground, Gdk.RGBA)

    def test_background(self):
        assert isinstance(self.scheme.background, Gdk.RGBA)

    def test_link(self):
        assert isinstance(self.scheme.link, Gdk.RGBA)

    def test_visited_link(self):
        assert isinstance(self.scheme.visited_link, Gdk.RGBA)


class TestBlackOnWhiteScheme(_TestScheme):

    def setup_method(self, method):
        self.scheme = nfoview.BlackOnWhiteScheme


class TestCustomScheme(_TestScheme):

    def setup_method(self, method):
        self.scheme = nfoview.CustomScheme


class TestDarkGreyOnLightGrayScheme(_TestScheme):

    def setup_method(self, method):
        self.scheme = nfoview.DarkGreyOnLightGrayScheme


class TestDefaultScheme(_TestScheme):

    def setup_method(self, method):
        self.scheme = nfoview.DefaultScheme


class TestGreyOnBlackScheme(_TestScheme):

    def setup_method(self, method):
        self.scheme = nfoview.GreyOnBlackScheme


class TestLightGreyOnDarkGrayScheme(_TestScheme):

    def setup_method(self, method):
        self.scheme = nfoview.LightGreyOnDarkGrayScheme


class TestWhiteOnBlackScheme(_TestScheme):

    def setup_method(self, method):
        self.scheme = nfoview.WhiteOnBlackScheme
