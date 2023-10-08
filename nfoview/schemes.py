# -*- coding: utf-8 -*-

# Copyright (C) 2008 Osmo Salomaa
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

import nfoview

from nfoview.i18n import _
from nfoview.i18n import __

__all__ = (
    "BlackOnWhite",
    "Custom",
    "DarkGreyOnLightGray",
    "Default",
    "GreyOnBlack",
    "LightGreyOnDarkGray",
    "WhiteOnBlack",
)

class ColorScheme:

    name         = NotImplementedError
    label        = NotImplementedError
    foreground   = NotImplementedError
    background   = NotImplementedError
    link         = NotImplementedError
    visited_link = NotImplementedError

class BlackOnWhite(ColorScheme):

    name         = "black-on-white"
    label        = __("Black on white")
    foreground   = "#000000"
    background   = "#ffffff"
    link         = "#0000ff"
    visited_link = "#ff00ff"

class Custom(ColorScheme):

    name         = "custom"
    label        = __("Custom")
    foreground   = nfoview.conf.foreground_color
    background   = nfoview.conf.background_color
    link         = nfoview.conf.link_color
    visited_link = nfoview.conf.visited_link_color

class DarkGreyOnLightGray(ColorScheme):

    name         = "dark-grey-on-light-grey"
    label        = __("Dark grey on light grey")
    foreground   = "#666666"
    background   = "#f2f2f2"
    link         = "#5555ff"
    visited_link = "#ff55ff"

class Default(ColorScheme):

    # https://github.com/GNOME/gtk/blob/main/gtk/theme/Default/_colors.scss
    # https://github.com/GNOME/gtk/blob/main/gtk/theme/Default/_colors-public.scss

    name         = "default"
    label        = __("System theme")
    foreground   = nfoview.util.lookup_color("theme_text_color", "#000000")
    background   = nfoview.util.lookup_color("theme_base_color", "#ffffff")
    link         = "#2a76c6"
    visited_link = "#215d9c"

class GreyOnBlack(ColorScheme):

    name         = "grey-on-black"
    label        = __("Grey on black")
    foreground   = "#aaaaaa"
    background   = "#000000"
    link         = "#aaaaff"
    visited_link = "#ffaaff"

class LightGreyOnDarkGray(ColorScheme):

    name         = "light-grey-on-dark-grey"
    label        = __("Light grey on dark grey")
    foreground   = "#f2f2f2"
    background   = "#666666"
    link         = "#aaaaff"
    visited_link = "#ffaaff"

class WhiteOnBlack(ColorScheme):

    name         = "white-on-black"
    label        = __("White on black")
    foreground   = "#ffffff"
    background   = "#000000"
    link         = "#aaaaff"
    visited_link = "#ffaaff"

def _ensure_translated():
    for class_name in __all__:
        scheme = globals()[class_name]
        if isinstance(scheme.label, __):
            scheme.label = _(scheme.label)

def get(name, fallback=None):
    _ensure_translated()
    for class_name in __all__:
        scheme = globals()[class_name]
        if scheme.name == name:
            return scheme
    if fallback is not None:
        return get(fallback)
    raise ValueError(f"No color scheme named {name!r}")

def get_all():
    _ensure_translated()
    schemes = list(map(globals().get, __all__))
    schemes.remove(Default)
    schemes.remove(Custom)
    schemes.sort(key=lambda x: x.label)
    schemes.insert(0, Default)
    schemes.append(Custom)
    return schemes
