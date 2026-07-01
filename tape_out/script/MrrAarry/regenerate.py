

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
from Components import  all as my_pdks
from circuits.testkey.MrrAarry import MRRArrayCircuit
import numpy
import os

output_folder = os.path.join(os.pardir, os.pardir,"gds_to_merge")
design_name = "MrrAarry"  # Name of your design

print(f"Regenerate {design_name}")

# Export the design to gds
lo=MRRArrayCircuit()
lo.Layout().write_gdsii(os.path.join(output_folder, design_name + ".gds"))

# Extract file info and export it
si = lo.Layout().size_info()
size_info_file = os.path.join(output_folder, design_name + "_si.txt")
numpy.savetxt(size_info_file, si.bounding_box.points)

print("Done")
