# Copyright (C) 2009 Osmo Salomaa
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

"""Miscellaneous decorators for functions and methods."""

import copy
import functools


def monkey_patch(obj, name):
    """Save obj's attribute and restore it after function returns.

    Attribute in question must be able to handle copy.deepcopy.
    """
    def outer_wrapper(function):
        @functools.wraps(function)
        def inner_wrapper(*args, **kwargs):
            has_attr = hasattr(obj, name)
            attr = getattr(obj, name, None)
            setattr(obj, name, copy.deepcopy(attr))
            try: return function(*args, **kwargs)
            finally:
                if has_attr:
                    setattr(obj, name, attr)
                    assert getattr(obj, name) == attr
                    assert getattr(obj, name) is attr
                else: # Remove attribute.
                    delattr(obj, name)
                    assert not hasattr(obj, name)
        return inner_wrapper
    return outer_wrapper
