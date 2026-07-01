from gds_utils.klayout.merge import merge_with_klayout

import os
from si_fab import all as pdk  # noqa: F401
from ipkiss3 import all as i3
import numpy

base_dir = os.path.dirname(os.path.abspath(__file__))
designs = []


# Add the template frame
si_info_template = i3.size_info_from_numpyarray(
    numpy.loadtxt(open(os.path.join(base_dir, "gds_to_merge", "template_si.txt")))
)
designs.append(
    {
        "source_path": os.path.join(base_dir, "gds_to_merge", "template.gds"),
        "prefix": "TEMPLATE",
        "transformations": [[0.0, 0.0, 0.0, False]],
    }
)
designs.append(
    {
        "source_path": os.path.join(base_dir, "gds_to_merge", "mmi.gds"),
        "prefix": "mmi",
        "transformations": [[50, 1000, 0.0, False]],
    }
)
designs.append(
    {
        "source_path": os.path.join(base_dir, "gds_to_merge", "mrr.gds"),
        "prefix": "mrr",
        "transformations": [[500,1000, 0.0, False]],
    }
)
designs.append(
    {
        "source_path": os.path.join(base_dir, "gds_to_merge", "sptree.gds"),
        "prefix": "sptree",
        "transformations": [[1000,1000, 0.0, False]],
    }
)
designs.append(
    {
        "source_path": os.path.join(base_dir, "gds_to_merge", "MrrAarry.gds"),
        "prefix": "MrrAarry",
        "transformations": [[200,4000, 0.0, False]],
    }
)


merge_with_klayout(
    designs=designs,
    keep_temp_files=False,
    top_cell_name="TAPEOUT_202008_SI_FAB",
    grid_per_unit=int(round(i3.get_grids_per_unit())),
    unprefixed_cells=["FC_TE_1550", "TEMPLATE", "MMI_1X2_OPTIMIZED"],
    output_layer_map=i3.TECH.GDSII.EXPORT_LAYER_MAP,
    output_gds="tapeout_muchen_si_fab_merged.gds",
)