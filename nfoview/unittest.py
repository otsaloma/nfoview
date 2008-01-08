# Copyright (C) 2005-2007 Osmo Salomaa
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

"""Base class for unit test cases."""

import atexit
import os
import tempfile

__all__ = ("TestCase",)


class TestCase(object):

    """Base class for unit test cases."""

    def get_nfo_file(self):
        """Return path to a temporary NFO file."""

        handle, path = tempfile.mkstemp()
        fobj = os.fdopen(handle, "w")
        fobj.write("qwertyuiop asdfghjkl zxcvbnm\n")
        fobj.write("http://home.gna.org/nfoview\n")
        fobj.close()
        atexit.register(os.remove, path)
        return path

    def raises(self, exception, function, *args, **kwargs):
        """Assert that calling function raises exception."""

        try:
            function(*args, **kwargs)
        except exception:
            return
        raise AssertionError

    def setUp(self):
        """Compatibility alias for 'setup_method'."""

        self.setup_method(None)

    def setup_method(self, method):
        """Set proper state for executing tests in method."""

        pass

    def tearDown(self):
        """Compatibility alias for 'teardown_method'."""

        self.teardown_method(None)

    def teardown_method(self, method):
        """Remove state set for executing tests in method."""

        pass
