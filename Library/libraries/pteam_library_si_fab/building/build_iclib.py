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


"""This script is used to create the .iclib file of the library for import in IPKISS Canvas.
If you create a new component in this library, you have to add it to all.py
and rerun this script to create a new .iclib file.
"""

import pteam_library_si_fab.all as pteam_lib  # noqa
from ipkiss3.all.canvas import export_ipkiss_library, SymbolImage
import os
import argparse


def build_iclib(dst_path=None):
    lib_path = os.path.dirname(os.path.abspath(pteam_lib.__file__))

    if dst_path is None:
        dst_path = lib_path
    iclib_dst = os.path.join(dst_path, "pteam_library_si_fab.iclib")

    print(f"Exporting iclib to {iclib_dst}")

    export_ipkiss_library(
        library_path=lib_path,
        library_name="pteam_library_si_fab",
        output_path=iclib_dst,
        symbols={
            "MZI": {
                "image": SymbolImage.MZI,
                "terms_positions": {
                    "elec1": [-0.4, 1],
                    "elec2": [0.4, 1],
                    "in2": [-1, 0.4],
                    "in1": [-1, -0.5],
                    "out2": [1, 0.4],
                    "out1": [1, -0.5],
                },
            },
            "Mux2Heated": {
                "width": 175,
                "height": 75,
                "terms_positions": {
                    "ht_in0": [-0.7, 1],
                    "ht_out0": [-0.5, 1],
                    "ht_in1": [-0.3, 1],
                    "ht_out1": [-0.1, 1],
                    "ht_in2": [0.1, 1],
                    "ht_out2": [0.3, 1],
                    "ht_in3": [0.5, 1],
                    "ht_out3": [0.7, 1],
                },
            },
            "TunableDelayLine": {
                "width": 150,
            },
            "SplitterTree": {
                "image": SymbolImage.DEMUX,
            },
            "MZModulator": {
                "image": SymbolImage.MZM,
                "width": 100,
                "terms_positions": {
                    "SR_pad": [-0.9, 1],
                    "G3_pad": [-0.6, 1],
                    "SL_pad": [-0.9, -1],
                    "G1_pad": [-0.6, -1],
                },
            },
            "DirectionalCouplerDC2": {"image": SymbolImage.DirectionalCoupler},
        },
    )


parser = argparse.ArgumentParser(description="build pteam_library_si_fab iclib")
parser.add_argument("-o", "--output-dir", dest="output_dir")
args = parser.parse_args()
build_iclib(args.output_dir)
