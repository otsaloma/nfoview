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
import contextlib
import copy
import functools
import nfoview
import os
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

def apply_style(widget):
    """Update font and colors to match custom settings."""
    name = nfoview.conf.color_scheme
    scheme = nfoview.schemes.get(name, "default")
    font_desc = Pango.FontDescription(nfoview.conf.font)
    css = """
    .nfoview-text-view,
    .nfoview-text-view text {{
      background-color: {bg};
      color: {fg};
      font-family: {family};
      font-size: {size}px;
      font-weight: {weight};
    }}""".format(bg=scheme.background,
                 fg=scheme.foreground,
                 family=font_desc.get_family().split(",")[0],
                 size=int(round(font_desc.get_size() / Pango.SCALE)),
                 weight=int(font_desc.get_weight()))

    provider = Gtk.CssProvider.get_default()
    provider.load_from_data(bytes(css.encode()))
    style = widget.get_style_context()
    style.add_class("nfoview-text-view")
    priority = Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
    style.add_provider_for_screen(Gdk.Screen.get_default(),
                                  provider,
                                  priority)

def connect(observer, observable, signal, *args):
    """
    Connect `observable`'s signal to `observer`'s callback method.

    If `observable` is a string, it should be an attribute of `observer`.
    If `observable` is not a string it should be the same as `observer`.
    """
    method_name = signal.replace("-", "_").replace("::", "_")
    if observer is not observable:
        method_name = "_".join((observable, method_name))
    method_name = "_on_{}".format(method_name).replace("__", "_")
    if not hasattr(observer, method_name):
        method_name = method_name[1:]
    method = getattr(observer, method_name)
    if observer is not observable:
        observable = getattr(observer, observable)
    return observable.connect(signal, method, *args)

def detect_encoding(path):
    """Detect and return NFO file encoding."""
    with open(path, "rb") as f:
        line = f.readline()
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

def get_max_text_view_size():
    """Return maximum allowed size for text view."""
    max_chars = nfoview.conf.text_view_max_chars
    max_lines = nfoview.conf.text_view_max_lines
    max_text = "\n".join(("x" * max_chars,) * max_lines)
    return get_text_view_size(max_text)

def get_text_view_size(text):
    """Return size for text view required to hold `text`."""
    label = Gtk.Label()
    apply_style(label)
    label.set_text(text)
    label.show()
    return (label.get_preferred_width()[1],
            label.get_preferred_height()[1])

def _hasattr_def(obj, name):
    """Return ``True`` if `obj` has attribute `name` defined."""
    if hasattr(obj, "__dict__"):
        return name in obj.__dict__
    return hasattr(obj, name)

def hex_to_rgba(string):
    """Return a :class:`Gdk.RGBA` for hexadecimal `string`."""
    rgba = Gdk.RGBA()
    success = rgba.parse(string)
    if success:
        return rgba
    raise ValueError("Parsing string {} failed"
                     .format(repr(string)))

def is_valid_encoding(encoding):
    """Return ``True`` if `encoding` is supported."""
    try:
        codecs.lookup(encoding)
        return True
    except LookupError:
        return False

def lookup_color(name, fallback):
    """Return defined color `name` from GTK+ theme."""
    entry = Gtk.Entry()
    entry.show()
    style = entry.get_style_context()
    found, color = style.lookup_color(name)
    if found:
        return rgba_to_hex(color)
    return fallback

def makedirs(directory):
    """Create and return `directory` or raise :exc:`OSError`."""
    directory = os.path.abspath(directory)
    if os.path.isdir(directory):
        return directory
    try:
        os.makedirs(directory)
    except OSError as error:
        print("Failed to create directory {}: {}"
              .format(repr(directory), str(error)),
              file=sys.stderr)
        raise # OSError
    return directory

def monkey_patch(obj, name):
    """
    Decorator for functions that change `obj`'s `name` attribute.

    Any changes done will be reverted after the function is run,
    i.e. `name` attribute is either restored to its original value
    or deleted, if it didn't originally exist.
    """
    def outer_wrapper(function):
        @functools.wraps(function)
        def inner_wrapper(*args, **kwargs):
            exists = _hasattr_def(obj, name)
            value = getattr(obj, name) if exists else None
            setattr(obj, name, copy.deepcopy(value))
            try:
                return function(*args, **kwargs)
            finally:
                setattr(obj, name, value)
                assert getattr(obj, name) == value
                assert getattr(obj, name) is value
                if not exists:
                    delattr(obj, name)
                    assert not _hasattr_def(obj, name)
        return inner_wrapper
    return outer_wrapper

def rgba_to_hex(color):
    """Return hexadecimal string for :class:`Gdk.RGBA` `color`."""
    return "#{:02x}{:02x}{:02x}".format(int(color.red   * 255),
                                        int(color.green * 255),
                                        int(color.blue  * 255))

def show_uri(uri):
    """Open `uri` in default application."""
    try:
        return Gtk.show_uri(None, uri, Gdk.CURRENT_TIME)
    except Exception:
        # Gtk.show_uri fails on Windows and some misconfigured installations.
        # GError: No application is registered as handling this file
        # Gtk.show_uri: Operation not supported
        if uri.startswith(("http://", "https://")):
            return webbrowser.open(uri)
        raise # Exception

@contextlib.contextmanager
def silent(*exceptions):
    """Try to execute body, ignoring `exceptions`."""
    try:
        yield
    except exceptions:
        pass

def uri_to_path(uri):
    """Convert `uri` to local filepath."""
    uri = urllib.parse.unquote(uri)
    if sys.platform == "win32":
        path = urllib.parse.urlsplit(uri)[2]
        while path.startswith("/"):
            path = path[1:]
        return path.replace("/", "\\")
    return urllib.parse.urlsplit(uri)[2]
