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

"""Classes for color scheme definitions."""

import nfoview

from nfoview.i18n import _

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

    """Baseclass for color scheme definitions."""

    name         = NotImplementedError
    label        = NotImplementedError
    foreground   = NotImplementedError
    background   = NotImplementedError
    link         = NotImplementedError
    visited_link = NotImplementedError


class BlackOnWhite(ColorScheme):

    """Color scheme with black text on white background."""

    name         = "black-on-white"
    label        = _("Black on white")
    foreground   = "#000000"
    background   = "#ffffff"
    link         = "#0000ff"
    visited_link = "#ff00ff"


class Custom(ColorScheme):

    """Color scheme with custom, user-chosen colors."""

    name         = "custom"
    label        = _("Custom")
    foreground   = nfoview.conf.foreground_color
    background   = nfoview.conf.background_color
    link         = nfoview.conf.link_color
    visited_link = nfoview.conf.visited_link_color


class DarkGreyOnLightGray(ColorScheme):

    """Color scheme with dark grey text on light grey background."""

    name         = "dark-grey-on-light-grey"
    label        = _("Dark grey on light grey")
    foreground   = "#666666"
    background   = "#f2f2f2"
    link         = "#5555ff"
    visited_link = "#ff55ff"


class Default(ColorScheme):

    """Color scheme with system default colors."""

    # http://git.gnome.org/browse/gtk+/tree/gtk/theme/Adwaita/_colors-public.scss
    # http://git.gnome.org/browse/gtk+/tree/gtk/theme/Adwaita/gtk-contained.css

    name         = "default"
    label        = _("System theme")
    foreground   = nfoview.util.lookup_color("theme_text_color", "#000000")
    background   = nfoview.util.lookup_color("theme_base_color", "#ffffff")
    link         = "#2a76c6"
    visited_link = "#215d9c"


class GreyOnBlack(ColorScheme):

    """Color scheme with grey text on black background."""

    name         = "grey-on-black"
    label        = _("Grey on black")
    foreground   = "#aaaaaa"
    background   = "#000000"
    link         = "#aaaaff"
    visited_link = "#ffaaff"


class LightGreyOnDarkGray(ColorScheme):

    """Color scheme with light grey text on dark grey background."""

    name         = "light-grey-on-dark-grey"
    label        = _("Light grey on dark grey")
    foreground   = "#f2f2f2"
    background   = "#666666"
    link         = "#aaaaff"
    visited_link = "#ffaaff"


class WhiteOnBlack(ColorScheme):

    """Color scheme with white text on black background."""

    name         = "white-on-black"
    label        = _("White on black")
    foreground   = "#ffffff"
    background   = "#000000"
    link         = "#aaaaff"
    visited_link = "#ffaaff"


def get(name, fallback=None):
    """Return the color scheme with given name."""
    for class_name in __all__:
        scheme = globals()[class_name]
        if scheme.name == name:
            return scheme
    if fallback is not None:
        return get(fallback)
    raise ValueError("No color scheme named {}"
                     .format(repr(name)))

def get_all():
    """Return a list of all color schemes in proper order."""
    schemes = list(map(globals().get, __all__))
    schemes.remove(Default)
    schemes.remove(Custom)
    schemes.sort(key=lambda x: x.label)
    schemes.insert(0, Default)
    schemes.append(Custom)
    return schemes
