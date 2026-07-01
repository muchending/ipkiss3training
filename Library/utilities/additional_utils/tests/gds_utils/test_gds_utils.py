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


from si_fab import technology  # noqa: F401
from ipkiss3 import all as i3
from gds_utils.klayout.merge import merge_with_klayout

import os
import json


def test_merging():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    designs = []
    spacing = 20.0

    designer_name = "pierre"
    user_path = os.path.join(base_dir, designer_name, "gds_to_merge")
    gds_files = [fl for fl in os.listdir(user_path) if fl.endswith(".gds")]
    top = 0.0

    for cnt in range(4):
        with open(os.path.join(user_path, os.path.splitext(gds_files[cnt])[0]) + "_si.json") as fp:
            si_info = json.load(fp)
        si = i3.SizeInfo(
            east=si_info["east"],
            west=si_info["west"],
            north=si_info["north"],
            south=si_info["south"],
        )
        # Design 1
        trans = [
            (
                -si.west + cnt2 * (si.width + spacing),
                top - si.south * ((cnt2 + 1) % 2) + ((cnt2) % 2) * si.north,
                0.0,
                cnt2 % 2,
            )
            for cnt2 in range(5)
        ]

        designs.append(
            {
                "source_path": os.path.join(user_path, gds_files[cnt]),
                "prefix": designer_name.upper() + f"_DESIGN_{cnt}",
                "transformations": trans,
            }
        )

        top += si.height + spacing

    merge_with_klayout(
        designs=designs,
        output_gds="tapeout_202005_demolib_merged.gds",
        top_cell_name="TAPEOUT_SIFAB2",
        grid_per_unit=int(round(i3.get_grids_per_unit())),
        unprefixed_cells=["FC_TE_1550"],
        output_layer_map=i3.TECH.GDSII.EXPORT_LAYER_MAP,
        keep_temp_files=False,
    )
    return True
