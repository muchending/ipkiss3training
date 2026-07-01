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


from si_fab import all as pdk  # noqa: F401
from ipkiss3 import all as i3
import os
import numpy
from gds_utils.klayout.merge import merge_with_klayout

base_dir = os.path.dirname(os.path.abspath(__file__))
designs = []

# Add the template frame
si_info_template = i3.size_info_from_numpyarray(
    numpy.loadtxt(open(os.path.join(base_dir, "template", "template_si.txt")))
)
designs.append(
    {
        "source_path": os.path.join(base_dir, "template", "template.gds"),
        "prefix": "TEMPLATE",
        "transformations": [[0.0, 0.0, 0.0, False]],
    }
)

# User 1: Chiara
designer_name = "chiara"
user_path = os.path.join(base_dir, designer_name, "gds_to_merge")
gds_files = [fl for fl in os.listdir(user_path) if fl.endswith(".gds")]
si_info_chiara = [
    i3.size_info_from_numpyarray(numpy.loadtxt(open(os.path.join(user_path, os.path.splitext(fl)[0]) + "_si.txt")))
    for fl in gds_files
]
spacing = 50  # Desired spacing between designs
margin = 50  # Margin to the block edge

# Design 1
designs.append(
    {
        "source_path": os.path.join(user_path, gds_files[0]),
        "prefix": designer_name.upper() + "_DESIGN_1",
        "transformations": [[0.0 + margin, 0.0 - si_info_chiara[0].south + margin, 0.0, False]],
    }
)

# Design 2
designs.append(
    {
        "source_path": os.path.join(user_path, gds_files[1]),
        "prefix": designer_name.upper() + "_DESIGN_2",
        "transformations": [
            [
                0.0 + margin,
                si_info_chiara[0].height - si_info_chiara[1].south + spacing + margin,
                0.0,
                False,
            ]
        ],
    }
)


# User 2: Pierre
designer_name = "pierre"
user_path = os.path.join(base_dir, designer_name, "gds_to_merge")
gds_files = [fl for fl in os.listdir(user_path) if fl.endswith(".gds")]
si_info_pierre = [
    i3.size_info_from_numpyarray(numpy.loadtxt(open(os.path.join(user_path, os.path.splitext(fl)[0]) + "_si.txt")))
    for fl in gds_files
]

# Design 1
designs.append(
    {
        "source_path": os.path.join(user_path, gds_files[0]),
        "prefix": designer_name.upper() + "_DESIGN_1",
        "transformations": [
            [
                0.0 + margin + si_info_chiara[1].width - si_info_pierre[0].west + spacing,
                0.0 + margin - si_info_pierre[0].south + 200.0,
                0.0,
                False,
            ]
        ],
    }
)

# Design 2
designs.append(
    {
        "source_path": os.path.join(user_path, gds_files[1]),
        "prefix": designer_name.upper() + "_DESIGN_2",
        "transformations": [
            [
                0.0
                + margin
                + si_info_chiara[1].width
                + si_info_pierre[0].width / 2.0
                - si_info_pierre[1].west
                + spacing,
                0.0 + margin - si_info_pierre[1].south,
                0.0,
                False,
            ]
        ],
    }
)

# User 3: Jiejun
designer_name = "jiejun"
user_path = os.path.join(base_dir, designer_name, "gds_to_merge")
gds_files = [fl for fl in os.listdir(user_path) if fl.endswith(".gds")]
si_info_jiejun = [
    i3.size_info_from_numpyarray(numpy.loadtxt(open(os.path.join(user_path, os.path.splitext(fl)[0]) + "_si.txt")))
    for fl in gds_files
]

# Design 1
designs.append(
    {
        "source_path": os.path.join(user_path, gds_files[0]),
        "prefix": designer_name.upper() + "_DESIGN_1",
        "transformations": [
            [
                1175,
                0.0 + margin + si_info_pierre[1].height - si_info_jiejun[0].south + spacing,
                0.0,
                False,
            ]
        ],
    }
)

# Design 2
designs.append(
    {
        "source_path": os.path.join(user_path, gds_files[1]),
        "prefix": designer_name.upper() + "_DESIGN_2",
        "transformations": [
            [
                1725,
                0.0 + margin + si_info_pierre[1].height - si_info_jiejun[1].south + spacing,
                0.0,
                False,
            ]
        ],
    }
)


# User 3: Ruping
designer_name = "ruping"
user_path = os.path.join(base_dir, designer_name, "gds_to_merge")
gds_files = [fl for fl in os.listdir(user_path) if fl.endswith(".gds")]
si_info_ruping = [
    i3.size_info_from_numpyarray(numpy.loadtxt(open(os.path.join(user_path, os.path.splitext(fl)[0]) + "_si.txt")))
    for fl in gds_files
]

# Design 1
designs.append(
    {
        "source_path": os.path.join(user_path, gds_files[0]),
        "prefix": designer_name.upper() + "_DESIGN_1",
        "transformations": [
            [
                si_info_template.east - margin - si_info_ruping[0].east,
                0.0 + margin - si_info_ruping[0].south,
                0.0,
                False,
            ]
        ],
    }
)

# Design 2
designs.append(
    {
        "source_path": os.path.join(user_path, gds_files[1]),
        "prefix": designer_name.upper() + "_DESIGN_2",
        "transformations": [
            [
                si_info_template.east - margin - si_info_ruping[1].east,
                0.0 + margin + si_info_ruping[0].height - si_info_ruping[1].south + spacing,
                0.0,
                0.0,
            ]
        ],
    }
)

merge_with_klayout(
    designs=designs,
    keep_temp_files=False,
    top_cell_name="TAPEOUT_202008_SI_FAB",
    grid_per_unit=int(round(i3.get_grids_per_unit())),
    unprefixed_cells=["FC_TE_1550", "TEMPLATE_2500_1250", "MMI_1X2_OPTIMIZED"],
    output_layer_map=i3.TECH.GDSII.EXPORT_LAYER_MAP,
    output_gds="tapeout_202008_si_fab_merged.gds",
)
