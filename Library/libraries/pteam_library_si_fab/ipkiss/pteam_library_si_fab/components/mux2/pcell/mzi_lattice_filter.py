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


class MZILatticeFilter(i3.Circuit):
    """Mach-Zender interferometer lattice filter based on directional couplers with different power
    coupling.
    The number of power couplings should be equal to the number of delay lengths plus 1.
    """

    directional_couplers = i3.ChildCellListProperty(doc="list of directional couplers")
    center_wavelength = i3.PositiveNumberProperty(default=1.55, doc="Center wavelength")
    delay_lengths = i3.ListProperty(default=[100.0], doc="List of delay lengths")
    bend_radius = i3.PositiveNumberProperty(default=5.0, doc="Bend radius")
    phase_error_width_deviation = i3.NonNegativeNumberProperty(default=0.0)
    phase_error_correlation_length = i3.NonNegativeNumberProperty(default=0.0)

    def _default_directional_couplers(self):
        power_couplings = [0.5, 0.5]
        dir_couplers = [
            pdk.SiDirectionalCouplerSPower(
                name=self.name + f"dc_{cnt}",
                power_fraction=p,
                target_wavelength=self.center_wavelength,
            )
            for cnt, p in enumerate(power_couplings)
        ]
        return dir_couplers

    def _default_specs(self):
        dcs = [dc.Layout() for dc in self.directional_couplers]
        specs = [i3.Inst(f"dc_{cnt}", dc) for cnt, dc in enumerate(dcs)]

        distance = 4 * self.bend_radius
        specs += [
            i3.Place(f"dc_{cnt}:in1", (distance, 0), relative_to=f"dc_{cnt - 1}:out1")
            for cnt in range(1, len(self.directional_couplers))
        ]

        for cnt, delay_length in enumerate(self.delay_lengths):
            if delay_length > 0:
                l_top = delay_length / 2
                l_bot = 0
            else:
                l_top = 0
                l_bot = -delay_length / 2
            p1 = f"dc_{cnt}:out1"
            p2 = f"dc_{cnt + 1}:in1"
            # modify the trace template of the port
            p1_port = dcs[cnt].ports["out1"]
            tt = p1_port.trace_template
            tt_mod = tt.cell.modified_copy()
            tt_mod.CircuitModel(
                phase_error_width_deviation=self.phase_error_width_deviation,
                phase_error_correlation_length=self.phase_error_correlation_length,
            )
            specs.append(
                i3.ConnectManhattan(
                    p1,
                    p2,
                    trace_template=tt_mod,
                    bend_radius=self.bend_radius,
                    control_points=[i3.H(p1_port.position.y - 2 * self.bend_radius - l_bot)],
                    min_straight=0,
                    start_straight=0,
                    end_straight=0,
                )
            )

            p1 = f"dc_{cnt}:out2"
            p2 = f"dc_{cnt + 1}:in2"

            p1_port = dcs[cnt].ports["out2"]
            tt = p1_port.trace_template
            tt_mod = tt.cell.modified_copy()
            tt_mod.CircuitModel(
                phase_error_width_deviation=self.phase_error_width_deviation,
                phase_error_correlation_length=self.phase_error_correlation_length,
            )
            specs.append(
                i3.ConnectManhattan(
                    p1,
                    p2,
                    trace_template=tt_mod,
                    bend_radius=self.bend_radius,
                    control_points=[i3.H(p1_port.position.y + 2 * self.bend_radius + l_top)],
                    min_straight=0,
                    start_straight=0,
                    end_straight=0,
                )
            )

        return specs

    def _default_exposed_ports(self):
        exposed_ports = {
            "dc_0:in1": "in1",
            "dc_0:in2": "in2",
            f"dc_{len(self.delay_lengths)}:out1": "out1",
            f"dc_{len(self.delay_lengths)}:out2": "out2",
        }
        return exposed_ports
