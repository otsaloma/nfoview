# Copyright (C) 2005-2008 Osmo Salomaa
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

import os
import subprocess
import sys
import urllib
import urlparse
import webbrowser


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

def is_command(command):
    """Return True if command exists as a file in $PATH."""

    for directory in os.environ.get("PATH", "").split(os.pathsep):
        path = os.path.join(directory, command)
        if os.path.isfile(path): return True
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
