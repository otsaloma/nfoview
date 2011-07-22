# Copyright (C) 2008-2009,2011 Osmo Salomaa
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

"""Classes for color scheme definitions."""

import nfoview
_ = nfoview.i18n._

__all__ = ("BlackOnWhiteScheme",
           "CustomScheme",
           "DarkGreyOnLightGrayScheme",
           "DefaultScheme",
           "GreyOnBlackScheme",
           "LightGreyOnDarkGrayScheme",
           "WhiteOnBlackScheme",
           )


class ColorScheme(object):

    """Baseclass for color scheme definitions.

    :cvar name: Name used to identify and save color scheme
    :cvar label: User-visible localized name for color scheme
    :cvar foreground: Foreground color as a :class:`Gdk.Color`
    :cvar background: Background color as a :class:`Gdk.Color`
    :cvar link: Link color as a :class:`Gdk.Color`
    :cvar visited_link: Visited link color as a :class:`Gdk.Color`
    """

    name         = NotImplementedError
    label        = NotImplementedError
    foreground   = NotImplementedError
    background   = NotImplementedError
    link         = NotImplementedError
    visited_link = NotImplementedError


class BlackOnWhiteScheme(ColorScheme):

    """Color scheme with black text on white background."""

    name         = "black-on-white"
    label        = _("Black on white")
    foreground   = nfoview.util.hex_to_rgba("#000000")
    background   = nfoview.util.hex_to_rgba("#ffffff")
    link         = nfoview.util.hex_to_rgba("#0000ff")
    visited_link = nfoview.util.hex_to_rgba("#ff00ff")


class CustomScheme(ColorScheme):

    """Color scheme with custom, user-chosen colors."""

    name         = "custom"
    label        = _("Custom")
    foreground   = nfoview.util.hex_to_rgba(nfoview.conf.foreground_color)
    background   = nfoview.util.hex_to_rgba(nfoview.conf.background_color)
    link         = nfoview.util.hex_to_rgba(nfoview.conf.link_color)
    visited_link = nfoview.util.hex_to_rgba(nfoview.conf.visited_link_color)


class DarkGreyOnLightGrayScheme(ColorScheme):

    """Color scheme with dark grey text on light grey background."""

    name         = "dark-grey-on-light-grey"
    label        = _("Dark grey on light grey")
    foreground   = nfoview.util.hex_to_rgba("#666666")
    background   = nfoview.util.hex_to_rgba("#f2f2f2")
    link         = nfoview.util.hex_to_rgba("#5555ff")
    visited_link = nfoview.util.hex_to_rgba("#ff55ff")


class DefaultScheme(ColorScheme):

    """Color scheme with default fore- and background colors."""

    name         = "default"
    label        = _("System theme")
    foreground   = nfoview.util.lookup_color("text_color", "#000000")
    background   = nfoview.util.lookup_color("base_color", "#ffffff")
    link         = nfoview.util.lookup_color("link_color", "#0000ff")
    visited_link = nfoview.util.lookup_color("link_color", "#ff00ff")


class GreyOnBlackScheme(ColorScheme):

    """Color scheme with grey text on black background."""

    name         = "grey-on-black"
    label        = _("Grey on black")
    foreground   = nfoview.util.hex_to_rgba("#aaaaaa")
    background   = nfoview.util.hex_to_rgba("#000000")
    link         = nfoview.util.hex_to_rgba("#aaaaff")
    visited_link = nfoview.util.hex_to_rgba("#ffaaff")


class LightGreyOnDarkGrayScheme(ColorScheme):

    """Color scheme with light grey text on dark grey background."""

    name         = "light-grey-on-dark-grey"
    label        = _("Light grey on dark grey")
    foreground   = nfoview.util.hex_to_rgba("#f2f2f2")
    background   = nfoview.util.hex_to_rgba("#666666")
    link         = nfoview.util.hex_to_rgba("#aaaaff")
    visited_link = nfoview.util.hex_to_rgba("#ffaaff")


class WhiteOnBlackScheme(ColorScheme):

    """Color scheme with white text on black background."""

    name         = "white-on-black"
    label        = _("White on black")
    foreground   = nfoview.util.hex_to_rgba("#ffffff")
    background   = nfoview.util.hex_to_rgba("#000000")
    link         = nfoview.util.hex_to_rgba("#aaaaff")
    visited_link = nfoview.util.hex_to_rgba("#ffaaff")
