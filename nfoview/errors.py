# Copyright (C) 2008-2009 Osmo Salomaa
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

"""All :mod:`nfoview` error classes."""

__all__ = ("Error", "AffirmationError",)


class Error(Exception):

    """Base class for all :mod:`nfoview` errors."""

    pass


class AffirmationError(Error):

    """Something expected to be ``True`` was ``False``.

    :exc:`AffirmationError` is by nature similar to the built-in
    :exc:`AssertionError`, but without the special reliance on
    :const:`__debug__` and given optimization options. :exc:`AffirmationError`
    is used to provide essential checks of boolean values instead of optional
    debug checks.
    """

    pass
