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


from si_fab import all as pdk
from ipkiss3 import all as i3
from circuit.all import CircuitCell, bezier_sbend


class SplitterTree(CircuitCell):
    _name_prefix = "SPLITTER_TREE"
    splitter = i3.ChildCellProperty(doc="Splitter used")
    levels = i3.IntProperty(default=3, doc="Number of levels")
    spacing_x = i3.PositiveNumberProperty(default=150.0, doc="Horizontal spacing between the levels")
    spacing_y = i3.PositiveNumberProperty(default=50.0, doc="Vertical spacing between the MMIs in the last level")
    bend_radius = i3.PositiveNumberProperty(default=5.0, doc="Bend radius of the connecting waveguides")

    def _default_splitter(self):
        return pdk.MMI1x2Optimized1550()

    def _default_child_cells(self):
        child_cells = dict()
        n_levels = self.levels
        for lev in range(n_levels):
            n_splitters = int(2**lev)  # Number of splitters per level
            for sp in range(n_splitters):
                child_cells[f"sp_{lev}_{sp}"] = self.splitter
        return child_cells

    def _default_connectors(self):
        conn = []
        n_levels = self.levels
        for lev in range(1, n_levels):
            n_splitters = int(2**lev)  # Number of splitters per level
            for sp in range(n_splitters):
                if sp % 2 == 0:
                    in_port = f"sp_{lev - 1}_{int(sp / 2.0)}:out1"
                else:
                    in_port = f"sp_{lev - 1}_{int(sp / 2.0)}:out2"
                out_port = f"sp_{lev}_{sp}:in1"
                conn.append((in_port, out_port, bezier_sbend, {"bend_radius": self.bend_radius}))
        return conn

    def _default_place_specs(self):
        place_specs = []
        n_levels = self.levels
        spacing_x = self.spacing_x
        spacing_y = self.spacing_y
        for lev in range(n_levels):
            n_splitters = int(2**lev)  # Number of splitters per level
            y_0 = -0.5 * spacing_y * 2 ** (n_levels - 1)
            for sp in range(n_splitters):
                x_coord = lev * spacing_x
                y_coord = y_0 + (sp + 0.5) * spacing_y * 2 ** (n_levels - lev - 1)
                place_specs.append(i3.Place(f"sp_{lev}_{sp}", (x_coord, y_coord)))
        return place_specs

    def _default_external_port_names(self):
        exposed_ports = {f"sp_{0}_{0}:in1": "in"}
        cnt = 1
        lev = self.levels - 1
        n_splitters = int(2**lev)  # Number of splitters per level
        for sp in range(n_splitters):
            exposed_ports[f"sp_{lev}_{sp}:out1"] = f"out{cnt}"
            cnt += 1
            exposed_ports[f"sp_{lev}_{sp}:out2"] = f"out{cnt}"
            cnt += 1
        return exposed_ports
