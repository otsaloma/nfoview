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

import atexit
import os
import tempfile

__all__ = ("TestCase",)


class TestCase:

    def assert_raises(self, exception, function, *args, **kwargs):
        try:
            function(*args, **kwargs)
        except exception:
            return
        raise AssertionError(
            "{!r} failed to raise {!r}"
            .format(function, exception))

    def new_nfo_file(self):
        handle, path = tempfile.mkstemp()
        f = os.fdopen(handle, "w")
        f.write("qwertyuiop asdfghjkl zxcvbnm\n")
        f.write("https://otsaloma.io/nfoview/\n")
        f.close()
        atexit.register(os.remove, path)
        return path

    def setUp(self):
        self.setup_method(None)

    def setup_method(self, method):
        pass

    def tearDown(self):
        self.teardown_method(None)

    def teardown_method(self, method):
        pass

    def test___init__(self):
        # Make sure that setup_method is always run.
        pass
