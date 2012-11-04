#!/usr/bin/env python
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
    desktop file is translated. This requires gettext and intltool, more
    specifically, executables 'msgfmt' and 'intltool-merge' in $PATH.
"""

import distutils.command.clean
import distutils.command.install
import distutils.command.install_data
import distutils.command.install_lib
import distutils.command.sdist
import glob
import os
import re
import shutil
import sys
import tarfile
import tempfile

clean = distutils.command.clean.clean
command = distutils.cmd.Command
install = distutils.command.install.install
install_data = distutils.command.install_data.install_data
install_lib = distutils.command.install_lib.install_lib
log = distutils.log
sdist = distutils.command.sdist.sdist


def get_version():
    """Return version number from nfoview/__init__.py."""
    path = os.path.join("nfoview", "__init__.py")
    text = open(path, "r", encoding="utf_8").read()
    return re.search(r"__version__ *= *['\"](.*?)['\"]", text).group(1)

def run_command_or_exit(cmd):
    """Run command in shell and raise SystemExit if it fails."""
    if os.system(cmd) != 0:
        log.error("command {} failed".format(repr(cmd)))
        raise SystemExit(1)

def run_command_or_warn(cmd):
    """Run command in shell and warn if it fails."""
    if os.system(cmd) != 0:
        log.warn("command {} failed".format(repr(cmd)))


class Clean(clean):

    """Command to remove files and directories created."""

    __glob_targets = ("*/__pycache__",
                      "*/*.py[co]",
                      "*/*/__pycache__",
                      "*/*/*.py[co]",
                      "*/*/*/__pycache__",
                      "*/*/*/*.py[co]",
                      "*/*/*/*/__pycache__",
                      "*/*/*/*/*.py[co]",
                      "build",
                      "data/nfoview.desktop",
                      "dist",
                      "doc/sphinx/api",
                      "doc/sphinx/_build",
                      "doc/sphinx/index.rst",
                      "locale",
                      "po/*~",
                      "ChangeLog",
                      "MANIFEST",
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


class Documentation(command):

    """Command to build documentation from source code."""

    description = "build documentation from source code"
    user_options = [("format=", "f",
                     "type of documentation to create (try 'html')")]

    def initialize_options(self):
        """Initialize default values for options."""
        self.format = None

    def finalize_options(self):
        """Ensure that format has some valid value."""
        if self.format is None:
            log.warn("format not specified, using 'html'")
            self.format = "html"

    def run(self):
        """Build documentation from source code."""
        os.chdir(os.path.join("doc", "sphinx"))
        if not self.dry_run:
            run_command_or_exit("make clean")
            run_command_or_exit("python{:d}.{:d} autogen.py nfoview"
                                .format(*sys.version_info[:2]))

            run_command_or_exit("make {}".format(self.format))


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
        run_command_or_warn('update-desktop-database "{}"'.format(directory))


class InstallData(install_data):

    """Command to install data files."""

    def __get_desktop_file(self):
        """Return a tuple for the translated desktop file."""
        path = os.path.join("data", "nfoview.desktop")
        run_command_or_exit("intltool-merge -d po {}.in {}"
                            .format(path, path))

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
        run_command_or_exit("msgfmt {} -o {}"
                            .format(po_file, mo_file))

        return (dest_dir, (mo_file,))

    def run(self):
        """Install data files after translating them."""
        for po_file in glob.glob("po/*.po"):
            self.data_files.append(self.__get_mo_file(po_file))
        self.data_files.append(self.__get_desktop_file())
        install_data.run(self)


class InstallLib(install_lib):

    """Command to install library files."""

    def install(self):
        """Install library files after writing changes."""
        get_command_obj = self.distribution.get_command_obj
        root = get_command_obj("install").root
        prefix = get_command_obj("install").install_data
        # Allow --root to be used like $DESTDIR.
        if root is not None:
            prefix = os.path.abspath(prefix)
            prefix = prefix.replace(os.path.abspath(root), "")
        data_dir = os.path.join(prefix, "share", "nfoview")
        locale_dir = os.path.join(prefix, "share", "locale")
        # Write changes to the nfoview.paths module.
        path = os.path.join(self.build_dir, "nfoview", "paths.py")
        text = open(path, "r", encoding="utf_8").read()
        patt = 'DATA_DIR = get_data_directory_source()'
        repl = "DATA_DIR = {}".format(repr(data_dir))
        text = text.replace(patt, repl)
        assert text.count(repr(data_dir)) > 0
        patt = 'LOCALE_DIR = get_locale_directory_source()'
        repl = "LOCALE_DIR = {}".format(repr(locale_dir))
        text = text.replace(patt, repl)
        assert text.count(repr(locale_dir)) > 0
        open(path, "w", encoding="utf_8").write(text)
        return install_lib.install(self)


class SDistGna(sdist):

    """Command to create a source distribution for gna.org."""

    description = "create source distribution for gna.org"

    def finalize_options(self):
        """Set the distribution directory to 'dist/X.Y'."""
        version = get_version()
        sdist.finalize_options(self)
        branch = ".".join(version.split(".")[:2])
        self.dist_dir = os.path.join(self.dist_dir, branch)

    def run(self):
        """Build tarballs and create additional files."""
        version = get_version()
        if os.path.isfile("ChangeLog"):
            os.remove("ChangeLog")
        run_command_or_exit("tools/generate-change-log > ChangeLog")
        assert os.path.isfile("ChangeLog")
        assert open("ChangeLog", "r").read().strip()
        sdist.run(self)
        basename = "nfoview-{}".format(version)
        tarballs = os.listdir(self.dist_dir)
        os.chdir(self.dist_dir)
        # Compare tarball contents with working copy.
        temp_dir = tempfile.gettempdir()
        test_dir = os.path.join(temp_dir, basename)
        tobj = tarfile.open(tarballs[-1], "r")
        for member in tobj.getmembers():
            tobj.extract(member, temp_dir)
        log.info("comparing tarball (tmp) with working copy (../..)")
        os.system('diff -qr -x ".*" -x "*.pyc" ../.. {}'.format(test_dir))
        response = input("Are all files in the tarball [Y/n]? ")
        if response.lower() == "n":
            raise SystemExit("Must edit MANIFEST.in.")
        shutil.rmtree(test_dir)
        # Create extra distribution files.
        os.system("xz {}.tar".format(basename))
        log.info("calculating md5sums")
        run_command_or_exit("md5sum * > {}.md5sum".format(basename))
        log.info("creating '{}.changes'".format(basename))
        source = os.path.join("..", "..", "ChangeLog")
        shutil.copyfile(source, "{}.changes".format(basename))
        log.info("creating '{}.news'".format(basename))
        source = os.path.join("..", "..", "NEWS")
        shutil.copyfile(source, "{}.news".format(basename))
        log.info("signing '{}.tar.xz'".format(basename))
        run_command_or_exit("gpg --detach {}.tar.xz".format(basename))


setup_kwargs = dict(
    name="nfoview",
    version=get_version(),
    platforms=("Platform Independent",),
    author="Osmo Salomaa",
    author_email="otsaloma@iki.fi",
    url="http://home.gna.org/nfoview/",
    description="Viewer for NFO files",
    license="GPL",
    packages=("nfoview",),
    scripts=("bin/nfoview",),
    data_files=[
        ("share/icons/hicolor/16x16/apps",
         ("data/icons/hicolor/16x16/apps/nfoview.png",)),
        ("share/icons/hicolor/22x22/apps",
         ("data/icons/hicolor/22x22/apps/nfoview.png",)),
        ("share/icons/hicolor/24x24/apps",
         ("data/icons/hicolor/24x24/apps/nfoview.png",)),
        ("share/icons/hicolor/32x32/apps",
         ("data/icons/hicolor/32x32/apps/nfoview.png",)),
        ("share/icons/hicolor/48x48/apps",
         ("data/icons/hicolor/48x48/apps/nfoview.png",)),
        ("share/icons/hicolor/256x256/apps",
         ("data/icons/hicolor/256x256/apps/nfoview.png",)),
        ("share/man/man1",
         ("doc/nfoview.1",)),
        ("share/nfoview",
         ("data/preferences-dialog.ui",
          "data/ui.xml")),
        ],

    cmdclass={"clean": Clean,
              "doc": Documentation,
              "install": Install,
              "install_data": InstallData,
              "install_lib": InstallLib,
              "sdist_gna": SDistGna,
              })

if __name__ == "__main__":
    os.chdir(os.path.dirname(__file__) or ".")
    distutils.core.setup(**setup_kwargs)
