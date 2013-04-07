# -*- coding: utf-8 -*-

# Copyright (C) 2005-2009,2011,2013 Osmo Salomaa
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

"""Miscellaneous functions."""

import codecs
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

def get_color_scheme(name):
    """
    Return the color scheme with given name.

    Raise :exc:`ValueError` if color scheme not found.
    """
    schemes = [getattr(nfoview.schemes, x)
               for x in nfoview.schemes.__all__]

    names = [x.name for x in schemes]
    if not name in names:
        raise ValueError("No color scheme named {}"
                         .format(repr(name)))

    return schemes[names.index(name)]

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

def hex_to_rgba(string):
    """
    Return a :class:`Gdk.RGBA` for hexadecimal `string`.

    Raise :exc:`ValueError` if parsing `string` fails.
    """
    rgba = Gdk.RGBA()
    success = rgba.parse(string)
    if not success:
        raise ValueError("Parsing string {} failed"
                         .format(repr(string)))

    return rgba

def is_valid_encoding(encoding):
    """Return ``True`` if `encoding` is a supported encoding."""
    try:
        codecs.lookup(encoding)
        return True
    except LookupError:
        return False

def lookup_color(name, fallback=None):
    """
    Return color from GTK+ theme.

    `fallback` can be either a :class:`Gdk.RGBA` object or
    a string that can be parsed by :func:`Gdk.RGBA.parse`.
    Raise :exc:`TypeError` if `fallback` is of bad type.
    Raise :exc:`ValueError` if parsing fallback fails.
    """
    text_view = Gtk.TextView()
    text_view.show()
    style = text_view.get_style_context()
    # At some point a 'theme_' prefix was added,
    # e.g. 'base_color' became 'theme_base_color'.
    names = set((name,
                 "theme_{}".format(name),
                 name.replace("theme_", "")))

    for name in names:
        found, rgba = style.lookup_color(name)
        if found: return rgba
    if isinstance(fallback, Gdk.RGBA):
        return fallback
    if isinstance(fallback, str):
        return hex_to_rgba(fallback)
    raise TypeError("Unexpected type for fallback: {}"
                    .format(repr(type(fallback))))

def rgba_to_color(rgba):
    """Return :class:`Gdk.Color` for :class:`Gdk.RGBA` `rgba`."""
    return Gdk.color_parse(rgba_to_hex(rgba))

def rgba_to_hex(color):
    """Return hexadecimal string for :class:`Gdk.RGBA` `color`."""
    return "#{:02x}{:02x}{:02x}".format(int(color.red   * 255),
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
