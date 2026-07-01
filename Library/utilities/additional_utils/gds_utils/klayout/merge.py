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


import os
from luceda.klayout import find_klayout_exe
from .merge_ruby_script_generator import create_ruby_gdsii_merge
from .checks import checks
from ipkiss3 import all as i3
import tempfile


def merge_with_klayout(
    designs,
    output_gds,
    top_cell_name="MERGED",
    grid_per_unit=None,
    unprefixed_cells=None,
    output_layer_map=i3.TECH.GDSII.EXPORT_LAYER_MAP,
    keep_temp_files=False,
):
    """Merge several gds files using klayout

    Merges a number of designs defined by GDS files together into a single GDS file.
    Uses the information inside 'designs' as instructions for GDS files to merge and
    where and how to place them.

    Parameters
    ----------
    designs : list
        List of dicts containing the following keys:
            source_path: str
                The path to the gds file to be merged.
            prefix: str
                Prefix to be prepended to the name of the PCell to avoid conflicts.
            transformations: list
                List of transformations with the following elements:
                    translation in the x-direction
                    translation in the y-direction
                    rotation angle in degrees (must be a multiple of 90, other values are rounded to the nearest
                    multiple of 90)
                    mirroring across x-axis if True
    output_gds : str
        Name of the output gds
    top_cell_name : str, optional
        Name of the top cell
    grid_per_unit : int, optional
        Grid per unit points (defaults to the value defined in the technology)
    unprefixed_cells : list, optional
        List of unprefixed cells names
    output_layer_map: map, optional
        Output layer map
    keep_temp_files: bool, optional
        Keep the temporary files for debugging
    """

    if unprefixed_cells is None:
        unprefixed_cells = []
    if grid_per_unit is None:
        grid_per_unit = int(round(i3.get_grids_per_unit()))

    for check in checks:
        check(designs=designs)
    ruby_script = create_ruby_gdsii_merge(
        designs=designs,
        top_cell_name=top_cell_name,
        grid_per_unit=grid_per_unit,
        unprefixed_cells=unprefixed_cells,
        output_layer_map=output_layer_map,
        output_gds=output_gds,
    )
    output_script_filename = "merge_script.rb"
    f = open(output_script_filename, "w+")
    f.write(ruby_script)
    f.close()
    print("done")

    generated = tempfile.mkdtemp()
    print(f"generated temporary directory: {generated}")

    from shutil import copyfile, move

    for d in designs:
        src = d["source_path"]
        dst = os.path.join(generated, os.path.basename(src))
        copyfile(src, dst)

    src = output_script_filename
    dst = os.path.join(generated, os.path.basename(output_script_filename))
    move(src, dst)
    output_script_filename = dst

    print("Running RubyScript")
    klayout_path = find_klayout_exe()
    command = [klayout_path, "-e", "-r", os.path.basename(output_script_filename)]

    import subprocess

    process = subprocess.Popen(command, cwd=os.path.abspath(generated))
    sStdout, sStdErr = process.communicate()

    print("Copying the merged GDSII back")
    src = os.path.join(generated, output_gds)
    dst = os.path.join(os.getcwd(), output_gds)
    copyfile(src, dst)

    import shutil

    if not keep_temp_files:
        print("Deleting temporary files")
        shutil.rmtree(generated)

    print("Done")
