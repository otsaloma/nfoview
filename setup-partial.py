#!/usr/bin/env python3

import os
import re

from pathlib import Path
from setuptools import find_packages
from setuptools import setup
from setuptools.command.install_lib import install_lib


class InstallLib(install_lib):

    def install(self):
        # Patch installation paths into nfoview/paths.py.
        prefix = os.getenv("NFOVIEW_PREFIX", "/usr/local")
        data_dir = Path(prefix) / "share" / "nfoview"
        locale_dir = Path(prefix) / "share" / "locale"
        path = Path(self.build_dir) / "nfoview" / "paths.py"
        text = path.read_text("utf-8")
        patt = r"^DATA_DIR = .*$"
        repl = f"DATA_DIR = {str(data_dir)!r}"
        text = re.sub(patt, repl, text, flags=re.MULTILINE)
        assert text.count(repl) == 1
        patt = r"^LOCALE_DIR = .*$"
        repl = f"LOCALE_DIR = {str(locale_dir)!r}"
        text = re.sub(patt, repl, text, flags=re.MULTILINE)
        assert text.count(repl) == 1
        path.write_text(text, "utf-8")
        return install_lib.install(self)


def get_version(fm="nfoview/__init__.py"):
    for line in Path(fm).read_text("utf-8").splitlines():
        if line.startswith("__version__ = "):
            return line.split()[-1].strip('"')

assert get_version()

setup(
    name="nfoview",
    version=get_version(),
    packages=find_packages(exclude=["*.test"]),
    scripts=["bin/nfoview"],
    cmdclass={"install_lib": InstallLib},
)
