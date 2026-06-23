
from Components import all as my_pdks
# Copyright (C) 2020-2025 Luceda Photonics


"""GENERALIZED SPLITTER TREE
This script is an example using parameters to create a truly reusable circuit, that can be used for different
applications with very minimal changes.
Specifically this is an "n-level" splitter tree.
This means that the number of levels, and therefore number of outputs is a parameter that you can pass into the circuit.
All the instances and connections are automatically generated from the number of levels and the spacing parameters.

The exact Python code for the labeling and positioning is not too complicated, however it is more important that you
understand the method, rather than the specific code we have implemented.
"""

from si_fab import all as pdk
from ipkiss3 import all as i3


class GeneralizedSplitterTree(i3.Circuit):
    splitter = i3.ChildCellProperty(doc="Splitter used.")
    n_levels = i3.PositiveIntProperty(default=3, doc="Number of tree levels.")
    spacing_x = i3.PositiveNumberProperty(default=100.0, doc="Horizontal spacing between the splitter levels.")
    spacing_y = i3.PositiveNumberProperty(default=50.0, doc="Vertical spacing between the splitters in the last level.")

    def _default_splitter(self):
        return my_pdks.MMI1muti2()  # try changing this to the y-junction in the si_fab PDK

    def _default_specs(self):
        specs = []

        # 1.  Using nested for loops we can add all the splitters we need for the circuit, as well as name them
        # according to their position (level) in the circuit. Also note that the splitter is a parameter, so we could
        # easily replace all the MMIs with different MMIs or a y-splitter with just one change to the code.

        for level in range(self.n_levels):
            for splitter_no in range(2**level):
                specs.append(i3.Inst(f"sp_{level}_{splitter_no}", self.splitter))

        # 2. Placing the MMIs is fairly straight forward, using local variables of x and y coordinates to help improve
        # the readability of the code. The "y-coord" in particular is not obvious, however the coordinate is derived
        # from the level and number in each level due to the relationship between each MMI. Again we use nested for
        # loops to achieve this.

        for level in range(self.n_levels):
            for splitter in range(2**level):
                x_coord = level * self.spacing_x
                y_coord = self.spacing_y * (
                    -0.5 * 2 ** (self.n_levels - 1) + ((splitter + 0.5) * 2 ** (self.n_levels - level - 1))
                )
                specs.append(i3.Place(f"sp_{level}_{splitter}", (x_coord, y_coord)))

        # 3. For each MMI there are two output ports that need connecting. We decide how best to do this, using
        # "splitter % 2" which returns the remainder from dividing by 2. This will be 0 for even numbers and non-zero
        # for odd numbers. In this way we can separate the two outputs correctly.
        # In the level loop we start at 1, but then subtract 1 during the naming as the final level will not have any
        # connections.

        for level in range(1, self.n_levels):
            for splitter in range(2**level):
                if splitter % 2 == 0:
                    in_port = f"sp_{level - 1}_{int(splitter / 2)}:out1"
                else:
                    in_port = f"sp_{level - 1}_{int(splitter / 2)}:out2"
                out_port = f"sp_{level}_{splitter}:in1"
                specs.append(i3.ConnectBend(in_port, out_port))
        return specs

    def _default_exposed_ports(self):
        # 4. In the same way we can expose the ports in the circuit. By default, all unconnected ports would be exposed,
        # but we want to rename them for simplicity.

        exposed_ports = {"sp_0_0:in1": "in"}  # adding the input port
        cnt = 1  # we use a local variable to keep track of how many output we have labeled
        level = self.n_levels - 1
        n_splitters = 2**level
        for splitter in range(n_splitters):  # looping over the output ports
            exposed_ports[f"sp_{level}_{splitter}:out1"] = f"out{cnt}"
            cnt += 1
            exposed_ports[f"sp_{level}_{splitter}:out2"] = f"out{cnt}"
            cnt += 1
        return exposed_ports


if __name__ == "__main__":
    # 5. Try changing the number of levels and seeing how the circuit re-adjusts automatically. Remember the size of the
    # circuit is exponential with the number of levels, so it is recommended not to go to very high n_levels.

    splitter_tree = GeneralizedSplitterTree(n_levels=3)
    splitter_tree_layout = splitter_tree.Layout()
    splitter_tree_layout.visualize(annotate=False)
    # splitter_tree_layout.write_gdsii("generalized_splitter_tree.gds")



















