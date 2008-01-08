# Copyright (C) 2007 Osmo Salomaa
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

"""Classes and functions for defining and accessing color schemes."""

import gtk
import nfoview
_ = nfoview.i18n._


class BlackOnWhiteScheme(object):

    """Color scheme with black text on white background."""

    name = "black-on-white"
    label = _("Black on white")
    foreground = gtk.gdk.color_parse("#000000")
    background = gtk.gdk.color_parse("#ffffff")
    link = gtk.gdk.color_parse("#0000ff")
    visited_link = gtk.gdk.color_parse("#ff00ff")


class CustomScheme(object):

    """Color scheme with custom, user-chosen colors."""

    name = "custom"
    label = _("Custom")
    foreground = gtk.gdk.color_parse(nfoview.conf.foreground_color)
    background = gtk.gdk.color_parse(nfoview.conf.background_color)
    link = gtk.gdk.color_parse(nfoview.conf.link_color)
    visited_link = gtk.gdk.color_parse(nfoview.conf.visited_link_color)


class DefaultScheme(object):

    """Color scheme with default fore- and background colors."""

    name = "default"
    label = _("System theme")
    _style = gtk.TextView().rc_get_style()
    foreground = _style.text[gtk.STATE_NORMAL]
    background = _style.base[gtk.STATE_NORMAL]
    link = gtk.gdk.color_parse("#5455ff")
    visited_link = gtk.gdk.color_parse("#ff54ff")


class GreyOnBlackScheme(object):

    """Color scheme with grey text on black background."""

    name = "grey-on-black"
    label = _("Grey on black")
    foreground = gtk.gdk.color_parse("#aaaaaa")
    background = gtk.gdk.color_parse("#000000")
    link = gtk.gdk.color_parse("#abacff")
    visited_link = gtk.gdk.color_parse("#ffabff")


class WhiteOnBlackScheme(object):

    """Color scheme with white text on black background."""

    name = "white-on-black"
    label = _("White on black")
    foreground = gtk.gdk.color_parse("#ffffff")
    background = gtk.gdk.color_parse("#000000")
    link = gtk.gdk.color_parse("#abacff")
    visited_link = gtk.gdk.color_parse("#ffabff")


def _get_color_scheme_classes():
    """Get a list of all color scheme classes."""

    return [eval(x) for x in globals() if x.endswith("Scheme")]

def get_color_scheme(name):
    """Get the color scheme class with given name."""

    schemes = _get_color_scheme_classes()
    names = [x.name for x in schemes]
    return schemes[names.index(name)]

def get_color_schemes():
    """Get a list of all color scheme classes in proper order."""

    schemes = _get_color_scheme_classes()
    schemes.remove(DefaultScheme)
    schemes.remove(CustomScheme)
    schemes.sort(lambda x, y: cmp(x.label, y.label))
    schemes.insert(0, DefaultScheme)
    schemes.append(CustomScheme)
    return schemes
