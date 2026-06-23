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


"""Export the ipkiss components in pteam_library_si_fab to OpenAccess."""

from oatools.library import build
import os
import argparse


def build_pteam_library_si_fab(output_dir=None, exported_si_fab=None):
    curdir = os.path.dirname(os.path.abspath(__file__))
    academy_dir = os.path.abspath(os.path.join(curdir, 3 * (os.path.pardir + os.path.sep)))  # 5 directory levels up

    pteam_library_src_path = os.path.join(curdir, os.pardir, "ipkiss", "pteam_library_si_fab")
    if output_dir is None:
        output_dir = os.path.join(curdir, os.pardir, "builds", "pteam_library_si_fab")
    if exported_si_fab is None:
        exported_si_fab = os.path.join(academy_dir, "pdks", "si_fab", "openaccess")

    build.build_library(
        src_path=pteam_library_src_path,
        output_folder=output_dir,
        tech_references=["si_fab"],
        libdefs_path=os.path.join(exported_si_fab, "lib.defs"),
        force=True,
    )

    print(f"Done, exported library to {os.path.abspath(output_dir)}")


parser = argparse.ArgumentParser(description="build_pteam_library_si_fab")
parser.add_argument("-o", "--output-dir", dest="output_dir")
parser.add_argument("-r", "--reference", dest="exported_si_fab")
args = parser.parse_args()
build_pteam_library_si_fab(args.output_dir, args.exported_si_fab)
