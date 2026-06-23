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


class SplitterTree(i3.Circuit):
    """This creates a splitter tree PCell, made of 1x2 splitter elements.

    Users can specify the number of tree levels as PCell parameter.
    """

    splitter = i3.ChildCellProperty(doc="Splitter used")
    levels = i3.IntProperty(default=3, doc="Number of levels")
    spacing_x = i3.PositiveNumberProperty(
        default=100.0, doc="Spacing between the splitters in x-direction in the last level"
    )
    spacing_y = i3.PositiveNumberProperty(default=50.0, doc="Spacing in y-direction")
    bend_radius = i3.PositiveNumberProperty()

    def _default_bend_radius(self):
        return 5.0

    def _default_splitter(self):
        return pdk.MMI1x2Optimized1550()

    def _default_specs(self):
        specs = [
            i3.Inst([f"sp_{level}_{sp}" for sp in range(int(2**level))], self.splitter) for level in range(self.levels)
        ]
        for level in range(self.levels):
            for sp in range(int(2**level)):
                sp_y = self.spacing_y * 2 ** (self.levels - level - 1)
                specs.append(
                    i3.Place(
                        f"sp_{level}_{sp}",
                        (level * self.spacing_x, -0.5 * (2**level - 1) * sp_y + sp * sp_y),
                    )
                )

        for level in range(1, self.levels):
            for sp in range(int(2**level)):
                if sp % 2 == 0:
                    in_port = f"sp_{level - 1}_{int(sp / 2.0)}:out1"
                else:
                    in_port = f"sp_{level - 1}_{int(sp / 2.0)}:out2"

                out_port = f"sp_{level}_{sp}:in1"

                specs.append(i3.ConnectManhattan(in_port, out_port, bend_radius=self.bend_radius))

        return specs

    def _default_exposed_ports(self):
        exposed_ports = dict()
        cnt = 1
        level = self.levels - 1
        for sp in range(int(2**level)):
            exposed_ports[f"sp_{level}_{sp}:out1"] = f"out{cnt}"
            cnt = cnt + 1
            exposed_ports[f"sp_{level}_{sp}:out2"] = f"out{cnt}"
            cnt = cnt + 1

        exposed_ports[f"sp_{0}_{0}:in1"] = "in"
        return exposed_ports


class RoutedSplitterTree(i3.Circuit):
    splitter_tree = i3.ChildCellProperty(doc="The splitter tree to which we add grating couplers")
    gc = i3.ChildCellProperty(doc="Fiber grating coupler PCell to be used as optical in/out")
    length_of_out_wg = i3.PositiveNumberProperty(default=300.0, doc="Length of output waveguide")
    length_of_in_wg = i3.PositiveNumberProperty(default=300.0, doc="Length of output waveguide")
    bend_radius = i3.PositiveNumberProperty(default=5.0, doc="Bend radius")

    def _default_splitter_tree(self):
        return SplitterTree()

    def _default_gc(self):
        return pdk.FC_TE_1550()

    def _default_specs(self):
        levels = self.splitter_tree.levels
        specs = [
            i3.Inst("splitter_tree", self.splitter_tree),
            i3.Inst("gc_in", self.gc),
            i3.Inst([f"gc_out{n_gc + 1}" for n_gc in range(int(2**levels))], self.gc),
            i3.Place("splitter_tree", (0.0, 0.0)),
            i3.Place("gc_in", (-self.length_of_in_wg, 0), angle=0.0, relative_to="splitter_tree:in"),
            i3.ConnectManhattan("gc_in:out", "splitter_tree:in"),
        ]

        levels = self.splitter_tree.levels
        spacing_y = 0.5 * self.splitter_tree.spacing_y
        bend_radius = self.bend_radius
        connections = []

        for n_gc in range(int(2**levels)):
            specs.append(
                i3.Place(
                    f"gc_out{n_gc + 1}",
                    (self.length_of_out_wg, -(2**levels - 1) * 0.5 * spacing_y + n_gc * spacing_y),
                    angle=180,
                    relative_to=("splitter_tree:out1", "splitter_tree:in"),
                ),
            )
            connections.append((f"gc_out{n_gc + 1}:out", f"splitter_tree:out{n_gc + 1}"))

        specs.append(
            i3.ConnectManhattanBundle(
                connections=connections,
                start_fanout=i3.SBendFanout(),
                end_fanout=i3.SBendFanout(),
                pitch=spacing_y,
                bend_radius=bend_radius,
            )
        )
        return specs

    def _default_exposed_ports(self):
        exposed_ports = dict()

        cnt = 1
        levels = self.splitter_tree.levels
        for n_gc in range(int(2**levels)):
            exposed_ports[f"gc_out{n_gc + 1}:vertical_in"] = f"out{cnt}"
            cnt = cnt + 1

        exposed_ports["gc_in:vertical_in"] = "in"
        return exposed_ports
