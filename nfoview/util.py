# Copyright (C) 2005-2009 Osmo Salomaa
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

"""Miscellaneous functions."""

import codecs
import gtk
import nfoview
import pango
import sys
import urllib.request, urllib.parse, urllib.error
import urllib.parse
import webbrowser


def affirm(value):
    """Raise :exc:`AffirmationError` if value evaluates to ``False``."""
    if not value:
        raise nfoview.AffirmationError

def connect(observer, observable, signal, *args):
    """Connect `observable`'s signal to `observer`'s callback method.

    If `observable` is a string, it should be an attribute of `observer`.
    If `observable` is not a string it should be the same as `observer`.
    """
    method_name = signal.replace("-", "_").replace("::", "_")
    if observer is not observable:
        method_name = "%s_%s" % (observable, method_name)
    method_name = ("_on_%s" % method_name).replace("__", "_")
    if not hasattr(observer, method_name):
        method_name = method_name[1:]
    method = getattr(observer, method_name)
    if observer is not observable:
        observable = getattr(observer, observable)
    return observable.connect(signal, method, *args)

def detect_encoding(path):
    """Detect and return NFO file encoding."""
    line = open(path, "r").readline()
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

def gdk_color_to_hex(color):
    """Return 7-character hexadecimal string for GDK `color`.

    >>> color = gtk.gdk.Color(56797, 61166, 65535)
    >>> nfoview.util.gdk_color_to_hex(color)
    '#ddeeff'
    """
    return "#%02x%02x%02x" % (int(color.red   / 256.0),
                              int(color.green / 256.0),
                              int(color.blue  / 256.0))

def get_color_scheme(name):
    """Return the color scheme with given name.

    Raise :exc:`ValueError` if color scheme not found.
    """
    schemes = [getattr(nfoview.schemes, x) for x in nfoview.schemes.__all__]

    names = [x.name for x in schemes]
    if not name in names:
        raise ValueError("No color scheme named %s" % repr(name))
    return schemes[names.index(name)]

def get_color_schemes():
    """Return a list of all color schemes in proper order."""
    schemes = [getattr(nfoview.schemes, x) for x in nfoview.schemes.__all__]

    schemes.remove(nfoview.DefaultScheme)
    schemes.remove(nfoview.CustomScheme)
    schemes.sort(lambda x, y: cmp(x.label, y.label))
    schemes.insert(0, nfoview.DefaultScheme)
    schemes.append(nfoview.CustomScheme)
    return schemes

def get_font_description(fallback="monospace"):
    """Return font description from conf with `fallback` added."""
    font_desc = pango.FontDescription(nfoview.conf.font)
    family = font_desc.get_family()
    font_desc.set_family(",".join((family, fallback)))
    return font_desc

def is_valid_encoding(encoding):
    """Return ``True`` if `encoding` is a valid and supported encoding."""
    try:
        codecs.lookup(encoding)
        return True
    except LookupError:
        return False

def show_uri(uri):
    """Open `uri` in default application."""
    if sys.platform == "win32":
        if uri.startswith(("http://", "https://")):
            # gtk.show_uri (GTK+ 2.20) fails on Windows.
            # GError: No application is registered as handling this file
            return webbrowser.open(uri)
    return gtk.show_uri(None, uri, gtk.gdk.CURRENT_TIME)

def uri_to_path(uri):
    """Convert `uri` to local filepath."""
    uri = urllib.parse.unquote(uri)
    if sys.platform == "win32":
        path = urllib.parse.urlsplit(uri)[2]
        while path.startswith("/"):
            path = path[1:]
        return path.replace("/", "\\")
    return urllib.parse.urlsplit(uri)[2]
