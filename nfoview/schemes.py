# Copyright (C) 2008-2009 Osmo Salomaa
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

"""Classes for color scheme definitions."""

import gtk
import nfoview
_ = nfoview.i18n._

__all__ = ("BlackOnWhiteScheme",
           "CustomScheme",
           "DarkGreyOnLightGrayScheme",
           "DefaultScheme",
           "GreyOnBlackScheme",
           "LightGreyOnDarkGrayScheme",
           "WhiteOnBlackScheme",)


class ColorScheme(object):

    """Baseclass for color scheme definitions.

    :cvar name: Name used to identify and save color scheme
    :cvar label: User-visible localized name for color scheme
    :cvar foreground: Foreground color as a :class:`gtk.gdk.Color`
    :cvar background: Background color as a :class:`gtk.gdk.Color`
    :cvar link: Link color as a :class:`gtk.gdk.Color`
    :cvar visited_link: Visited link color as a :class:`gtk.gdk.Color`
    """

    name = "custom"
    label = _("Custom")
    foreground = gtk.gdk.color_parse(nfoview.conf.foreground_color)
    background = gtk.gdk.color_parse(nfoview.conf.background_color)
    link = gtk.gdk.color_parse(nfoview.conf.link_color)
    visited_link = gtk.gdk.color_parse(nfoview.conf.visited_link_color)


class BlackOnWhiteScheme(ColorScheme):

    """Color scheme with black text on white background."""

    name = "black-on-white"
    label = _("Black on white")
    foreground = gtk.gdk.color_parse("#000000")
    background = gtk.gdk.color_parse("#ffffff")
    link = gtk.gdk.color_parse("#0000ff")
    visited_link = gtk.gdk.color_parse("#ff00ff")


class CustomScheme(ColorScheme):

    """Color scheme with custom, user-chosen colors."""

    name = "custom"
    label = _("Custom")
    foreground = gtk.gdk.color_parse(nfoview.conf.foreground_color)
    background = gtk.gdk.color_parse(nfoview.conf.background_color)
    link = gtk.gdk.color_parse(nfoview.conf.link_color)
    visited_link = gtk.gdk.color_parse(nfoview.conf.visited_link_color)


class DarkGreyOnLightGrayScheme(ColorScheme):

    """Color scheme with dark grey text on light grey background."""

    name = "dark-grey-on-light-grey"
    label = _("Dark grey on light grey")
    foreground = gtk.gdk.color_parse("#666666")
    background = gtk.gdk.color_parse("#f2f2f2")
    link = gtk.gdk.color_parse("#5555ff")
    visited_link = gtk.gdk.color_parse("#ff55ff")


class DefaultScheme(ColorScheme):

    """Color scheme with default fore- and background colors."""

    name = "default"
    label = _("System theme")
    _style = gtk.TextView().rc_get_style()
    foreground = _style.text[gtk.STATE_NORMAL]
    background = _style.base[gtk.STATE_NORMAL]
    link = gtk.gdk.color_parse("#5555ff")
    visited_link = gtk.gdk.color_parse("#ff55ff")


class GreyOnBlackScheme(ColorScheme):

    """Color scheme with grey text on black background."""

    name = "grey-on-black"
    label = _("Grey on black")
    foreground = gtk.gdk.color_parse("#aaaaaa")
    background = gtk.gdk.color_parse("#000000")
    link = gtk.gdk.color_parse("#aaaaff")
    visited_link = gtk.gdk.color_parse("#ffaaff")


class LightGreyOnDarkGrayScheme(ColorScheme):

    """Color scheme with light grey text on dark grey background."""

    name = "light-grey-on-dark-grey"
    label = _("Light grey on dark grey")
    foreground = gtk.gdk.color_parse("#f2f2f2")
    background = gtk.gdk.color_parse("#666666")
    link = gtk.gdk.color_parse("#aaaaff")
    visited_link = gtk.gdk.color_parse("#ffaaff")


class WhiteOnBlackScheme(ColorScheme):

    """Color scheme with white text on black background."""

    name = "white-on-black"
    label = _("White on black")
    foreground = gtk.gdk.color_parse("#ffffff")
    background = gtk.gdk.color_parse("#000000")
    link = gtk.gdk.color_parse("#aaaaff")
    visited_link = gtk.gdk.color_parse("#ffaaff")
