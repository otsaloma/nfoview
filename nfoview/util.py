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

"""Miscellaneous functions."""

import codecs
import copy
import functools
import nfoview
import sys
import urllib.parse
import webbrowser

from gi.repository import Gdk
from gi.repository import Gtk
from gi.repository import Pango


def affirm(value):
    """Raise :exc:`AffirmationError` if value evaluates to ``False``."""
    if not value:
        raise nfoview.AffirmationError

def connect(observer, observable, signal, *args):
    """
    Connect `observable`'s signal to `observer`'s callback method.

    If `observable` is a string, it should be an attribute of `observer`.
    If `observable` is not a string it should be the same as `observer`.
    """
    method_name = signal.replace("-", "_").replace("::", "_")
    if observer is not observable:
        method_name = "_".join((observable, method_name))
    method_name = ("_on_{}".format(method_name)).replace("__", "_")
    if not hasattr(observer, method_name):
        method_name = method_name[1:]
    method = getattr(observer, method_name)
    if observer is not observable:
        observable = getattr(observer, observable)
    return observable.connect(signal, method, *args)

def detect_encoding(path):
    """Detect and return NFO file encoding."""
    line = open(path, "rb").readline()
    if (line.startswith(codecs.BOM_UTF32_BE) and
        is_valid_encoding("utf_32_be")):
        return "utf_32_be"
    if (line.startswith(codecs.BOM_UTF32_LE) and
        is_valid_encoding("utf_32_le")):
        return "utf_32_le"
    if (line.startswith(codecs.BOM_UTF8) and
        is_valid_encoding("utf_8_sig")):
        return "utf_8_sig"
    if (line.startswith(codecs.BOM_UTF16_BE) and
        is_valid_encoding("utf_16_be")):
        return "utf_16_be"
    if (line.startswith(codecs.BOM_UTF16_LE) and
        is_valid_encoding("utf_16_le")):
        return "utf_16_le"
    # If no encoding was explicitly recognized, as a fallback,
    # return the de facto standard encoding for NFO files, CP437.
    return "cp437"

def get_color_scheme(name, fallback=None):
    """
    Return the color scheme with given name.

    Raise :exc:`ValueError` if color scheme not found.
    """
    for class_name in nfoview.schemes.__all__:
        scheme = getattr(nfoview.schemes, class_name)
        if scheme.name == name:
            return scheme
    if fallback is not None:
        return get_color_scheme(fallback)
    raise ValueError("No color scheme named {}"
                     .format(repr(name)))

def get_color_schemes():
    """Return a list of all color schemes in proper order."""
    schemes = [getattr(nfoview.schemes, x)
               for x in nfoview.schemes.__all__]

    schemes.remove(nfoview.DefaultScheme)
    schemes.remove(nfoview.CustomScheme)
    schemes.sort(key=lambda x: x.label)
    schemes.insert(0, nfoview.DefaultScheme)
    schemes.append(nfoview.CustomScheme)
    return schemes

def get_font_description(fallback="monospace"):
    """Return font description from conf with `fallback` added."""
    font_desc = Pango.FontDescription(nfoview.conf.font)
    family = font_desc.get_family()
    font_desc.set_family(",".join((family, fallback, "")))
    return font_desc

def _hasattr_def(obj, name):
    """Return ``True`` if `obj` has attribute `name` defined."""
    if hasattr(obj, "__dict__"):
        return name in obj.__dict__
    return hasattr(obj, name)

def hex_to_rgba(string):
    """
    Return a :class:`Gdk.RGBA` for hexadecimal `string`.

    Raise :exc:`ValueError` if parsing `string` fails.
    """
    rgba = Gdk.RGBA()
    success = rgba.parse(string)
    if success:
        return rgba
    raise ValueError("Parsing string {} failed"
                     .format(repr(string)))

def is_valid_encoding(encoding):
    """Return ``True`` if `encoding` is a supported encoding."""
    try:
        codecs.lookup(encoding)
        return True
    except LookupError:
        return False

def lookup_color(name, fallback):
    """
    Return defined color `name` from GTK+ theme.

    `fallback` should be a hexadecimal string of form '#RRGGBB'.
    Raise :exc:`ValueError` if parsing `fallback` fails.
    """
    # XXX: It would be nice to get colors from the user's GTK+ theme,
    # but any possible code used here seems destined to break with
    # every new release of GTK+ and/or whichever GTK+ theme.
    return hex_to_rgba(fallback)

def monkey_patch(obj, name):
    """
    Decorator for functions that change `obj`'s `name` attribute.

    Any changes done will be reverted after the function is run, i.e. `name`
    attribute is either restored to its original value or deleted, if it didn't
    originally exist.
    """
    def outer_wrapper(function):
        @functools.wraps(function)
        def inner_wrapper(*args, **kwargs):
            if _hasattr_def(obj, name):
                attr = getattr(obj, name)
                setattr(obj, name, copy.deepcopy(attr))
                try:
                    return function(*args, **kwargs)
                finally:
                    setattr(obj, name, attr)
                    assert getattr(obj, name) == attr
                    assert getattr(obj, name) is attr
            else: # Attribute not defined.
                try:
                    return function(*args, **kwargs)
                finally:
                    delattr(obj, name)
                    assert not _hasattr_def(obj, name)
        return inner_wrapper
    return outer_wrapper

def rgba_to_hex(color):
    """Return hexadecimal string for :class:`Gdk.RGBA` `color`."""
    return "#{:02X}{:02X}{:02X}".format(int(color.red   * 255),
                                        int(color.green * 255),
                                        int(color.blue  * 255))

def show_uri(uri):
    """Open `uri` in default application."""
    if sys.platform == "win32" and uri.startswith(("http://", "https://")):
        # Gtk.show_uri (GTK+ 2.20) fails on Windows.
        # GError: No application is registered as handling this file
        return webbrowser.open(uri)
    return Gtk.show_uri(None, uri, Gdk.CURRENT_TIME)

def uri_to_path(uri):
    """Convert `uri` to local filepath."""
    uri = urllib.parse.unquote(uri)
    if sys.platform == "win32":
        path = urllib.parse.urlsplit(uri)[2]
        while path.startswith("/"):
            path = path[1:]
        return path.replace("/", "\\")
    return urllib.parse.urlsplit(uri)[2]
