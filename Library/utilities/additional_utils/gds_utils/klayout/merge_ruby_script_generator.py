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


from .primitives import _ruby_final_lines, _ruby_merge_design, _ruby_copy_cell_function, _ruby_main_layout


def create_ruby_gdsii_merge(
    designs,
    top_cell_name,
    grid_per_unit,
    unprefixed_cells,
    output_layer_map,
    output_gds,
):
    """Returns a Ruby script that can be run by KLayout to merge the designs
    :param designs: list of designs
    :param grid_per_unit: grid points per unit
    :param unprefixed_cells: list of unprefixed cells
    :param output layer map: output layer map
    :param output_gds name of the output gds
    :return: String of Ruby code
    """
    header = f"# Merge script for {top_cell_name} \n"
    copy_cell = _ruby_copy_cell_function(unprefixed_cells=unprefixed_cells)

    main_layout = _ruby_main_layout(top_cell_name=top_cell_name, grids_per_unit=grid_per_unit)
    designs_code = ""
    for design in designs:
        designs_code += _ruby_merge_design(
            design=design,
            grid_per_unit=grid_per_unit,
            output_layer_map=output_layer_map,
        )

    final = _ruby_final_lines(output_gds=output_gds)

    return header + copy_cell + main_layout + designs_code + final
