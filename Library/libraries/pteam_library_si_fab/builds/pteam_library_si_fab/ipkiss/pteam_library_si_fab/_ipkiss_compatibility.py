# Copyright (C) 2020-2025 Luceda Photonics
# This version of Luceda Academy and related packages
# (hereafter referred to as Luceda Academy) is distributed under a proprietary License by Luceda
# It does allow you to develop and distribute add-ons or plug-ins, but does
# not allow redistribution of Luceda Academy  itself (in original or modified form).
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE.
#
# For the details of the licensing contract and the conditions under which
# you may use this software, we refer to the
# EULA which was distributed along with this program.
# It is located in the root of the distribution folder.



import sys
from ipkiss3.all import VERSION
from packaging.version import Version
import os.path

if Version(VERSION.split()[-1].split("_")[-1]) < Version("2026.06.0rc1"):
    additional_path = os.path.join(
        os.path.dirname(os.path.dirname(__file__)),
        r"dependencies.zip",
    )
    sys.path.insert(0, additional_path)
    