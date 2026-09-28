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

import codecs
import nfoview
import sys
import urllib.parse
import webbrowser

from gi.repository import Gdk
from gi.repository import Gtk
from gi.repository import Pango

_css_provider = None

def affirm(value):
    if not value:
        raise nfoview.AffirmationError(f"Not True: {value!r}")

def apply_style(widget):
    name = nfoview.conf.color_scheme
    scheme = nfoview.schemes.get(name, "default")
    font_desc = Pango.FontDescription(nfoview.conf.font)
    css = """
    .nfoview-text-view, .nfoview-text-view text {{
        background-color: {bg};
        color: {fg};
        font-family: "{family}", monospace;
        font-size: {size}px;
        font-weight: {weight};
    }}""".format(
        bg=scheme.background,
        fg=scheme.foreground,
        family=font_desc.get_family().split(",")[0].strip('"'),
        size=int(round(font_desc.get_size() / Pango.SCALE)),
        # Round weight to hundreds to work around CSS errors
        # with weird weights such as Unscii's 101.
        weight=round(font_desc.get_weight(), -2),
    )
    css = css.replace("font-size: 0px;", "")
    css = css.replace("font-weight: 0;", "")
    css = "\n".join(filter(lambda x: x.strip(), css.splitlines()))
    global _css_provider
    if _css_provider is None:
        _css_provider = Gtk.CssProvider()
        Gtk.StyleContext.add_provider_for_display(
            Gdk.Display.get_default(),
            _css_provider,
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)
    _css_provider.load_from_string(css)
    widget.add_css_class("nfoview-text-view")

def detect_encoding(path, default="cp437"):
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
    return default

def get_max_text_view_size():
    max_chars = nfoview.conf.text_view_max_chars
    max_lines = nfoview.conf.text_view_max_lines
    max_text = "\n".join(("x" * max_chars,) * max_lines)
    return get_text_view_size(max_text)

def get_monitor():
    display = Gdk.Display.get_default()
    for monitor in display.get_monitors():
        if monitor is not None:
            return monitor

def get_screen_size(monitor=None):
    monitor = monitor or get_monitor()
    rect = monitor.get_geometry()
    return rect.width, rect.height

def get_text_view_size(text):
    label = Gtk.Label()
    apply_style(label)
    label.set_text(text)
    width = label.measure(Gtk.Orientation.HORIZONTAL, -1)
    height = label.measure(Gtk.Orientation.VERTICAL, -1)
    return width.natural, height.natural

def hex_to_rgba(string):
    rgba = Gdk.RGBA()
    success = rgba.parse(string)
    if success: return rgba
    raise ValueError(f"Parsing {string!r} failed")

def is_valid_encoding(encoding):
    try:
        return codecs.lookup(encoding)
    except LookupError:
        return False

def rgba_to_hex(color):
    return "#{:02x}{:02x}{:02x}".format(
        int(color.red   * 255),
        int(color.green * 255),
        int(color.blue  * 255),
    )

def show_uri(uri, parent=None):
    def on_finish(launcher, result):
        try:
            launcher.launch_finish(result)
        except Exception:
            # Launching fails on Windows and some misconfigured installations.
            # GError: No application is registered as handling this file
            # GError: Operation not supported
            if uri.startswith(("http://", "https://")):
                return webbrowser.open(uri)
            raise # Exception
    Gtk.UriLauncher.new(uri).launch(parent, None, on_finish)

def uri_to_path(uri):
    uri = urllib.parse.unquote(uri)
    if sys.platform == "win32":
        path = urllib.parse.urlsplit(uri)[2]
        while path.startswith("/"):
            path = path[1:]
        return path.replace("/", "\\")
    return urllib.parse.urlsplit(uri)[2]
