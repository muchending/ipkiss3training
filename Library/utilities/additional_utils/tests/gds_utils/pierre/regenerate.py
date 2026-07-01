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


import si_fab.all as pdk
from ipkiss3 import all as i3
from circuit.circuitcell import CircuitCell
from splitter_tree import SplitterTree
from circuit.connector_functions import sbend, manhattan
from circuit.combine_connectors import combine_connectors
import numpy as np
import os
import json


class RouteSplitterTreeNorth(CircuitCell):
    """Routed Splitter tree with grating couplers placed north."""

    dut = i3.ChildCellProperty(doc="splitter used")
    grating = i3.ChildCellProperty(doc="Splitter")
    grating_sep = i3.PositiveNumberProperty(default=50.0, doc="Separation between the gratings")
    bend_radius = i3.PositiveNumberProperty(default=20.0, doc="Bend Radius")
    wav_sep = i3.PositiveNumberProperty(default=5.0, doc="Separation between waveguides.")

    def _default_grating(self):
        return pdk.FC_TE_1550()

    def _default_bend_radius(self):
        return 20.0

    def _default_dut(self):
        return SplitterTree(name=self.name + "_DUT", levels=6)

    def _default_child_cells(self):
        children = dict()
        children["DUT"] = self.dut
        for cnt in range(2**self.dut.levels):
            children[f"gr_out_{cnt}"] = self.grating
        children["gr_in"] = self.grating
        return children

    def _default_connectors(self):
        conn = list()
        conn.append(("gr_in:out", "DUT:in", manhattan, {"bend_radius": self.bend_radius}))
        insts = self.get_child_instances()
        n_gratings = 2**self.dut.levels
        wp_x = insts["DUT"].size_info().east + self.bend_radius
        wp_y = insts["DUT"].size_info().north + 2 * self.bend_radius
        for cnt in range(n_gratings):
            grating_name = f"gr_out_{cnt}"
            dut_port_name = f"out{n_gratings - cnt}"
            grating_port = insts[grating_name].ports["out"]
            dut_port = insts["DUT"].ports[dut_port_name]
            wp_x += self.wav_sep
            if grating_port.position.x > wp_x:
                wp_y -= self.wav_sep
            else:
                wp_y += self.wav_sep
            if np.abs(grating_port.position.x - wp_x) < 2 * self.bend_radius:
                cr = combine_connectors([sbend, manhattan], [(wp_x, wp_y, -90)])
                conn.append(
                    (
                        f"{grating_name}:out",
                        f"DUT:{dut_port_name}",
                        cr,
                        {"bend_radius": self.bend_radius},
                    )
                )
            else:
                conn.append(
                    (
                        f"{grating_name}:out",
                        f"DUT:{dut_port_name}",
                        manhattan,
                        {
                            "bend_radius": self.bend_radius,
                            "control_points": [(wp_x, wp_y), (wp_x, dut_port.position.y)],
                        },
                    )
                )

        return conn

    def _default_place_specs(self):
        specs = []
        si_dut = self.dut.get_default_view(i3.LayoutView).size_info()
        nw = si_dut.north_west
        gr_y = nw[1] + (1 + np.ceil(si_dut.width / self.grating_sep)) * self.wav_sep + 5 * self.bend_radius
        for cnt in range(2**self.dut.levels):
            spec = i3.Place(f"gr_out_{cnt}:out", (nw[0] + cnt * self.grating_sep, gr_y), angle=-90)
            specs.append(spec)
        spec = i3.Place("gr_in:out", (nw[0] - 1 * self.grating_sep, gr_y), angle=-90)
        specs.append(spec)
        return specs


def serialize_size_info(si):
    return {
        "east": si.east,
        "west": si.west,
        "south": si.south,
        "north": si.north,
    }


if __name__ == "__main__":
    project_folder = "./gds_to_merge"  # Name of the project
    if not os.path.exists(project_folder):
        os.mkdir(project_folder)

    for levels in range(1, 5):
        print(f"Number levels:{levels}")
        dut = SplitterTree(name=f"SP{levels}", levels=levels)
        cell = RouteSplitterTreeNorth(name=f"Routed_tree{levels}", dut=dut)
        cell_lv = cell.Layout()
        design_name = f"splitter_tree_routed_north_{levels}"
        cell_lv.write_gdsii(os.path.join(project_folder, f"{design_name}.gds"))
        si = cell_lv.size_info()
        size_info_file = os.path.join(project_folder, design_name + "_si.json")

        with open(size_info_file, "w") as f:
            json.dump(si, f, sort_keys=True, default=serialize_size_info, indent=2)
        print("done")
