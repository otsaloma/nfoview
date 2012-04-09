# -*- coding: utf-8-unix -*-

# Copyright (C) 2009 Osmo Salomaa
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

"""Miscellaneous decorators for functions and methods."""

import copy
import functools


def _hasattr_def(obj, name):
    """Return ``True`` if `obj` has attribute `name` defined."""
    if hasattr(obj, "__dict__"):
        return name in obj.__dict__
    return hasattr(obj, name)

def monkey_patch(obj, name):
    """
    Decorator for functions that change `obj`'s `name` attribute.

    Any changes done will be reverted after the function is run, i.e. `name`
    attribute is either restored to its original value or deleted, if it didn't
    originally exist. The attribute in question must be able to correctly
    handle a :func:`copy.deepcopy` operation.

    Typical use would be unit testing code under legitimately unachievable
    conditions, e.g. pseudo-testing behaviour on Windows, while not actually
    using Windows::

        @nfoview.deco.monkey_patch(sys, "platform")
        def test_do_something():
            sys.platform = "win32"
            do_something()

    """
    def outer_wrapper(function):
        @functools.wraps(function)
        def inner_wrapper(*args, **kwargs):
            if _hasattr_def(obj, name):
                attr = getattr(obj, name)
                setattr(obj, name, copy.deepcopy(attr))
                try: return function(*args, **kwargs)
                finally:
                    setattr(obj, name, attr)
                    assert getattr(obj, name) == attr
                    assert getattr(obj, name) is attr
            else: # Attribute not defined.
                try: return function(*args, **kwargs)
                finally:
                    delattr(obj, name)
                    assert not _hasattr_def(obj, name)
        return inner_wrapper
    return outer_wrapper
