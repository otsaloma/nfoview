#!/usr/bin/env python

import os
import subprocess
from distutils.command.install import install
from distutils.core import setup
from distutils.log import info

# Disable the installation of an egg info file.
for i, item in enumerate(install.sub_commands):
    if item[0] == "install_egg_info":
        item = ("install_egg_info", lambda self: False)
        install.sub_commands[i] = item

data_files = [("share/applications", ("nfoview.desktop",))]
data_files.append(("share/man/man1", ("nfoview.1",)))
data_files.append(("share/mime/packages", ("nfoview.xml",)))
files = {"scripts": ["nfoview"], "data_files": data_files}
dist = setup(name="nfoview", version="1.0", **files)

# Update caches if installing and root not given.
root = dist.get_command_obj("install").root
data_dir = dist.get_command_obj("install_data").install_dir
if (root is None) and (data_dir is not None):
    directory = os.path.join(data_dir, "share", "applications")
    info("updating desktop database in %s" % directory)
    subprocess.call(["update-desktop-database", directory])
    directory = os.path.join(data_dir, "share", "mime")
    info("updating mime database in %s" % directory)
    subprocess.call(["update-mime-database", directory])
