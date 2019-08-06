#!/usr/bin/env python3

"""
There are two relevant customizations to the standard distutils installation
process: (1) writing the nfoview.paths module and (2) handling translations.

(1) NFO Viewer finds non-Python files based on the paths written in module
    nfoview.paths. In nfoview/paths.py the paths default to the ones in the
    source directory. During the 'install_lib' command the file gets rewritten
    to build/nfoview/paths.py with the installation paths and that file will be
    installed. The paths are based on variable 'install_data' with the 'root'
    variable stripped if it is given. If doing distro-packaging, make sure this
    file gets correctly written.

(2) During installation, the .po files are compiled into .mo files and the
    appdata and desktop files are translated. This requires gettext.
"""

import distutils
import glob
import os
import re
import shutil
import sys

from distutils import log
from distutils.command.clean import clean
from distutils.command.install import install
from distutils.command.install_data import install_data
from distutils.command.install_lib import install_lib


def get_version():
    path = os.path.join("nfoview", "__init__.py")
    text = open(path, "r", encoding="utf_8").read()
    return re.search(r"__version__ *= *['\"](.*?)['\"]", text).group(1)

def run_or_exit(cmd):
    if os.system(cmd) == 0: return
    log.error("command {!r} failed".format(cmd))
    raise SystemExit(1)

def run_or_warn(cmd):
    if os.system(cmd) == 0: return
    log.warn("command {!r} failed".format(cmd))


class Clean(clean):

    __glob_targets = [
        "__pycache__",
        "*/__pycache__",
        "*/*/__pycache__",
        ".pytest_cache",
        "*/.pytest_cache",
        "*/*/.pytest_cache",
        "build",
        "data/io.otsaloma.nfoview.appdata.xml",
        "data/io.otsaloma.nfoview.desktop",
        "dist",
        "flatpak/.flatpak-builder",
        "flatpak/build",
        "locale",
        "po/*~",
        "po/LINGUAS",
        "winsetup.log",
    ]

    def run(self):
        clean.run(self)
        for targets in map(glob.glob, self.__glob_targets):
            for target in filter(os.path.isdir, targets):
                log.info("removing {}".format(target))
                if not self.dry_run:
                    shutil.rmtree(target)
            for target in filter(os.path.isfile, targets):
                log.info("removing {}".format(target))
                if not self.dry_run:
                    os.remove(target)


class Install(install):

    def run(self):
        install.run(self)
        get_command_obj = self.distribution.get_command_obj
        root = get_command_obj("install").root
        data_dir = get_command_obj("install_data").install_dir
        # Assume we're actually installing if --root was not given.
        if (root is not None) or (data_dir is None): return
        directory = os.path.join(data_dir, "share", "applications")
        log.info("updating desktop database in {}".format(directory))
        run_or_warn('update-desktop-database "{}"'.format(directory))


class InstallData(install_data):

    def __generate_linguas(self):
        linguas = sorted(glob.glob("po/*.po"))
        linguas = [os.path.basename(x)[:-3] for x in linguas]
        with open("po/LINGUAS", "w") as f:
            f.write("\n".join(linguas) + "\n")

    def __get_appdata_file(self):
        path = os.path.join("data", "io.otsaloma.nfoview.appdata.xml")
        command = "msgfmt --xml -d po --template {}.in -o {}"
        run_or_warn(command.format(path, path))
        if not os.path.isfile(path):
            # The above can fail with an old version of gettext,
            # fall back on copying the file without translations.
            shutil.copy("{}.in".format(path), path)
        return ("share/metainfo", [path])

    def __get_desktop_file(self):
        path = os.path.join("data", "io.otsaloma.nfoview.desktop")
        command = "msgfmt --desktop -d po --template {}.in -o {}"
        run_or_warn(command.format(path, path))
        if not os.path.isfile(path):
            # The above can fail with an old version of gettext,
            # fall back on copying the file without translations.
            shutil.copy("{}.in".format(path), path)
        return ("share/applications", [path])

    def __get_mo_file(self, po_file):
        locale = os.path.basename(po_file[:-3])
        mo_dir = os.path.join("locale", locale, "LC_MESSAGES")
        mo_file = os.path.join(mo_dir, "nfoview.mo")
        log.info("compiling {}".format(mo_file))
        os.makedirs(mo_dir, exist_ok=True)
        run_or_exit("msgfmt {} -o {}".format(po_file, mo_file))
        dest_dir = os.path.join("share", mo_dir)
        return (dest_dir, [mo_file])

    def __get_mo_files(self):
        if sys.platform == "win32": return []
        files = sorted(glob.glob("po/*.po"))
        return [self.__get_mo_file(x) for x in files]

    def run(self):
        self.__generate_linguas()
        self.data_files.extend(self.__get_mo_files())
        self.data_files.append(self.__get_appdata_file())
        self.data_files.append(self.__get_desktop_file())
        install_data.run(self)


class InstallLib(install_lib):

    def install(self):
        get_command_obj = self.distribution.get_command_obj
        root = get_command_obj("install").root
        prefix = get_command_obj("install").install_data
        # Allow --root to be used like DESTDIR.
        if root is not None:
            prefix = os.path.abspath(prefix)
            prefix = prefix.replace(os.path.abspath(root), "")
        data_dir = os.path.join(prefix, "share", "nfoview")
        locale_dir = os.path.join(prefix, "share", "locale")
        # Write changes to the nfoview.paths module.
        path = os.path.join(self.build_dir, "nfoview", "paths.py")
        text = open(path, "r", encoding="utf_8").read()
        patt = r"^DATA_DIR = .*$"
        repl = "DATA_DIR = {!r}".format(data_dir)
        text = re.sub(patt, repl, text, flags=re.MULTILINE)
        assert text.count(repl) == 1
        patt = r"^LOCALE_DIR = .*$"
        repl = "LOCALE_DIR = {!r}".format(locale_dir)
        text = re.sub(patt, repl, text, flags=re.MULTILINE)
        assert text.count(repl) == 1
        open(path, "w", encoding="utf_8").write(text)
        return install_lib.install(self)


setup_kwargs = {
    "name": "nfoview",
    "version": get_version(),
    "author": "Osmo Salomaa",
    "author_email": "otsaloma@iki.fi",
    "url": "https://otsaloma.io/nfoview/",
    "description": "Viewer for NFO files",
    "license": "GPL",
    "packages": ["nfoview"],
    "scripts": ["bin/nfoview"],
    "data_files": [
        ("share/icons/hicolor/scalable/apps", ["data/icons/io.otsaloma.nfoview.svg"]),
        ("share/icons/hicolor/symbolic/apps", ["data/icons/io.otsaloma.nfoview-symbolic.svg"]),
        ("share/man/man1", ["data/nfoview.1"]),
        ("share/nfoview", glob.glob("data/*.ui")),
    ],
    "cmdclass": {
        "clean": Clean,
        "install": Install,
        "install_data": InstallData,
        "install_lib": InstallLib,
    },
}

if __name__ == "__main__":
    os.chdir(os.path.dirname(__file__) or ".")
    distutils.core.setup(**setup_kwargs)
