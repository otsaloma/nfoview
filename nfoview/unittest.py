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
        """
        Asserts that the given function was raised.

        Args:
            self: (todo): write your description
            exception: (todo): write your description
            function: (todo): write your description
        """
        try:
            function(*args, **kwargs)
        except exception:
            return
        raise AssertionError(
            "{!r} failed to raise {!r}"
            .format(function, exception))

    def new_nfo_file(self):
        """
        Create a new nfo file

        Args:
            self: (todo): write your description
        """
        handle, path = tempfile.mkstemp()
        f = os.fdopen(handle, "w")
        f.write("qwertyuiop asdfghjkl zxcvbnm\n")
        f.write("https://otsaloma.io/nfoview/\n")
        f.close()
        atexit.register(os.remove, path)
        return path

    def setUp(self):
        """
        Sets the setup.

        Args:
            self: (todo): write your description
        """
        self.setup_method(None)

    def setup_method(self, method):
        """
        Setup a method.

        Args:
            self: (todo): write your description
            method: (str): write your description
        """
        pass

    def tearDown(self):
        """
        Tear down the teardown.

        Args:
            self: (todo): write your description
        """
        self.teardown_method(None)

    def teardown_method(self, method):
        """
        Teardown a method.

        Args:
            self: (todo): write your description
            method: (str): write your description
        """
        pass

    def test___init__(self):
        """
        Initialize the test___

        Args:
            self: (todo): write your description
        """
        # Make sure that setup_method is always run.
        pass
