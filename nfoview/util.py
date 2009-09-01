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
import nfoview
import os
import subprocess
import sys
import urllib
import urlparse
import webbrowser


def affirm(value):
    """Raise AffirmationError if value evaluates to False."""
    if not value:
        raise nfoview.AffirmationError

def browse_url(url, browser=None):
    """Open URL in web browser."""
    if browser and isinstance(browser, basestring):
        return subprocess.Popen((browser, url))
    if "GNOME_DESKTOP_SESSION_ID" in os.environ:
        return subprocess.Popen(("gnome-open", url))
    if "KDE_FULL_SESSION" in os.environ:
        return subprocess.Popen(("kfmclient", "exec", url))
    if sys.platform == "darwin":
        return subprocess.Popen(("open", url))
    if is_command("xdg-open"):
        return subprocess.Popen(("xdg-open", url))
    if is_command("exo-open"):
        return subprocess.Popen(("exo-open", url))
    return webbrowser.open(url)

def connect(observer, observable, signal, *args):
    """Connect observable's signal to observer's callback method.

    If observable is a string, it should be an attribute of observer. If
    observable is not a string it should be the same as observer.
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
    """Return 7-character hexadecimal string for GDK color."""
    return "#%02x%02x%02x" % (int(color.red   / 256.0),
                              int(color.green / 256.0),
                              int(color.blue  / 256.0))

def get_color_scheme(name):
    """Get the color scheme with given name.

    Raise ValueError if color scheme not found.
    """
    schemes = map(lambda x: getattr(nfoview.schemes, x),
                  nfoview.schemes.__all__)

    names = [x.name for x in schemes]
    if not name in names:
        raise ValueError("No color scheme named %s" % repr(name))
    return schemes[names.index(name)]

def get_color_schemes():
    """Get a list of all color schemes in proper order."""
    schemes = map(lambda x: getattr(nfoview.schemes, x),
                  nfoview.schemes.__all__)

    schemes.remove(nfoview.DefaultScheme)
    schemes.remove(nfoview.CustomScheme)
    schemes.sort(lambda x, y: cmp(x.label, y.label))
    schemes.insert(0, nfoview.DefaultScheme)
    schemes.append(nfoview.CustomScheme)
    return schemes

def is_command(command):
    """Return True if command exists as a file in $PATH."""
    dirs = os.environ.get("PATH", "").split(os.pathsep)
    paths = [os.path.join(x, command) for x in dirs]
    return any(map(os.path.isfile, paths))

def is_valid_encoding(encoding):
    """Return True if encoding is a valid and supported encoding."""
    try:
        codecs.lookup(encoding)
        return True
    except LookupError:
        return False

def uri_to_path(uri):
    """Convert URI to local filepath."""
    uri = urllib.unquote(uri)
    if sys.platform == "win32":
        path = urlparse.urlsplit(uri)[2]
        while path.startswith("/"):
            path = path[1:]
        return path.replace("/", "\\")
    return urlparse.urlsplit(uri)[2]
