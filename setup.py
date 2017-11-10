#!/usr/bin/env python3
# -*- coding: utf-8 -*-

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

import distutils.command.clean
import distutils.command.install
import distutils.command.install_data
import distutils.command.install_lib
import glob
import os
import re
import shutil

freezing = "NFOVIEW_FREEZING" in os.environ

clean = distutils.command.clean.clean
install = distutils.command.install.install
install_data = distutils.command.install_data.install_data
install_lib = distutils.command.install_lib.install_lib
log = distutils.log


def get_version():
    """Return version number from nfoview/__init__.py."""
    path = os.path.join("nfoview", "__init__.py")
    text = open(path, "r", encoding="utf_8").read()
    return re.search(r"__version__ *= *['\"](.*?)['\"]", text).group(1)

def run_or_exit(cmd):
    """Run command in shell and raise SystemExit if it fails."""
    if os.system(cmd) != 0:
        log.error("command {} failed".format(repr(cmd)))
        raise SystemExit(1)

def run_or_warn(cmd):
    """Run command in shell and warn if it fails."""
    if os.system(cmd) != 0:
        log.warn("command {} failed".format(repr(cmd)))


class Clean(clean):

    """Command to remove files and directories created."""

    __glob_targets = (
        ".cache",
        "*/.cache",
        "*/*/.cache",
        "*/*/*/.cache",
        "__pycache__",
        "*/__pycache__",
        "*/*/__pycache__",
        "*/*/*/__pycache__",
        "build",
        "data/nfoview.appdata.xml",
        "data/nfoview.desktop",
        "dist",
        "locale",
        "po/*~",
        "po/LINGUAS",
        "winsetup.log",
    )

    def run(self):
        """Remove files and directories listed in self.__glob_targets."""
        clean.run(self)
        for targets in map(glob.glob, self.__glob_targets):
            for target in filter(os.path.isdir, targets):
                log.info("removing '{}'".format(target))
                if not self.dry_run:
                    shutil.rmtree(target)
            for target in filter(os.path.isfile, targets):
                log.info("removing '{}'".format(target))
                if not self.dry_run:
                    os.remove(target)


class Install(install):

    """Command to install everything."""

    def run(self):
        """Install everything and update the desktop file database."""
        install.run(self)
        get_command_obj = self.distribution.get_command_obj
        root = get_command_obj("install").root
        data_dir = get_command_obj("install_data").install_dir
        # Assume we're actually installing if --root was not given.
        if (root is not None) or (data_dir is None): return
        directory = os.path.join(data_dir, "share", "applications")
        log.info("updating desktop database in '{}'".format(directory))
        run_or_warn('update-desktop-database "{}"'.format(directory))


class InstallData(install_data):

    """Command to install data files."""

    def __generate_linguas(self):
        """Generate LINGUAS file needed by msgfmt."""
        linguas = glob.glob("po/*.po")
        linguas = [x.split(os.sep)[1] for x in linguas]
        linguas = [x.split(".")[0] for x in linguas]
        with open("po/LINGUAS", "w") as f:
            f.write("\n".join(linguas) + "\n")

    def __get_appdata_file(self):
        """Return a tuple for the translated appdata file."""
        path = os.path.join("data", "nfoview.appdata.xml")
        command = "msgfmt --xml -d po --template {}.in -o {}"
        run_or_warn(command.format(path, path))
        if not os.path.isfile(path):
            # The above can fail with an old version of gettext,
            # fall back on copying the file without translations.
            shutil.copy("{}.in".format(path), path)
        return ("share/metainfo", (path,))

    def __get_desktop_file(self):
        """Return a tuple for the translated desktop file."""
        path = os.path.join("data", "nfoview.desktop")
        command = "msgfmt --desktop -d po --template {}.in -o {}"
        run_or_warn(command.format(path, path))
        if not os.path.isfile(path):
            # The above can fail with an old version of gettext,
            # fall back on copying the file without translations.
            shutil.copy("{}.in".format(path), path)
        return ("share/applications", (path,))

    def __get_mo_file(self, po_file):
        """Return a tuple for the compiled .mo file."""
        locale = os.path.basename(po_file[:-3])
        mo_dir = os.path.join("locale", locale, "LC_MESSAGES")
        if not os.path.isdir(mo_dir):
            log.info("creating {}".format(mo_dir))
            os.makedirs(mo_dir)
        mo_file = os.path.join(mo_dir, "nfoview.mo")
        dest_dir = os.path.join("share", mo_dir)
        log.info("compiling '{}'".format(mo_file))
        run_or_exit("msgfmt {} -o {}".format(po_file, mo_file))
        return (dest_dir, (mo_file,))

    def run(self):
        """Install data files after translating them."""
        self.__generate_linguas()
        for po_file in glob.glob("po/*.po"):
            if freezing: continue
            self.data_files.append(self.__get_mo_file(po_file))
        self.data_files.append(self.__get_appdata_file())
        self.data_files.append(self.__get_desktop_file())
        install_data.run(self)


class InstallLib(install_lib):

    """Command to install library files."""

    def install(self):
        """Install library files after writing changes."""
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
        repl = "DATA_DIR = {}".format(repr(data_dir))
        text = re.sub(patt, repl, text, flags=re.MULTILINE)
        assert text.count(repl) == 1
        patt = r"^LOCALE_DIR = .*$"
        repl = "LOCALE_DIR = {}".format(repr(locale_dir))
        text = re.sub(patt, repl, text, flags=re.MULTILINE)
        assert text.count(repl) == 1
        open(path, "w", encoding="utf_8").write(text)
        return install_lib.install(self)


setup_kwargs = dict(
    name="nfoview",
    version=get_version(),
    platforms=("Platform Independent",),
    author="Osmo Salomaa",
    author_email="otsaloma@iki.fi",
    url="https://otsaloma.io/nfoview/",
    description="Viewer for NFO files",
    license="GPL",
    packages=("nfoview",),
    scripts=("bin/nfoview",),
    data_files=[
        ("share/icons/hicolor/16x16/apps", ("data/icons/16x16/nfoview.png",)),
        ("share/icons/hicolor/22x22/apps", ("data/icons/22x22/nfoview.png",)),
        ("share/icons/hicolor/24x24/apps", ("data/icons/24x24/nfoview.png",)),
        ("share/icons/hicolor/32x32/apps", ("data/icons/32x32/nfoview.png",)),
        ("share/icons/hicolor/48x48/apps", ("data/icons/48x48/nfoview.png",)),
        ("share/icons/hicolor/256x256/apps", ("data/icons/256x256/nfoview.png",)),
        ("share/man/man1", ("data/nfoview.1",)),
        ("share/nfoview", glob.glob("data/*.ui")),
    ],
    cmdclass=dict(
        clean=Clean,
        install=Install,
        install_data=InstallData,
        install_lib=InstallLib,
    ))

if __name__ == "__main__":
    os.chdir(os.path.dirname(__file__) or ".")
    distutils.core.setup(**setup_kwargs)
