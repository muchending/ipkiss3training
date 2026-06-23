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
import numpy as np


def mzi_wav(
    name,
    separation,
    offset_high,
    bend_radius,
    heated,
    heater_width,
    heater_pad_length,
    trace_template,
    phase_error_width_deviation,
    phase_error_correlation_length,
):
    """Function that returns the waveguide needed to complete the (heated) MZI.
    The waveguide can either be heated (si_fabs' HeatedWaveguide) or not.

    Parameters
    ----------
    name : str
    separation : float
    offset_high : float
    bend_radius : float
    heated : bool
    heater_width : float
    heater_pad_length : float
    trace_template : TraceTemplate
    phase_error_width_deviation : float
    phase_error_correlation_length : float

    Returns
    -------
    cell : Waveguide or HeatedWaveguide
        U-shaped (heated) waveguide.

    """
    tt_new = trace_template.cell.modified_copy()
    tt_new.CircuitModel(
        phase_error_width_deviation=phase_error_width_deviation,
        phase_error_correlation_length=phase_error_correlation_length,
    )

    min_straight = bend_radius + heater_pad_length
    shape = [
        (0, 0),
        (min_straight, 0.0),
        (min_straight, offset_high),
        (separation - min_straight, offset_high),
        (separation - min_straight, 0.0),
        (separation, 0.0),
    ]

    r_shape = i3.ShapeRound(original_shape=shape, radius=bend_radius)
    if heated:
        cell = pdk.HeatedWaveguide(
            name=name,
            trace_template=tt_new,
            m1_length=heater_pad_length,
            heater_width=heater_width,
        )
        cell.Layout(shape=r_shape)
    else:
        cell = i3.Waveguide(name=name, trace_template=tt_new)
        cell.Layout(shape=r_shape)

    return cell


class MZILatticeFilterHeated(i3.Circuit):
    """Mach-Zehnder interferometer lattice filter based on directional couplers with different power coupling.

    The number of power couplings should be equal to the number of delay lengths plus 1.
    """

    directional_couplers = i3.ChildCellListProperty(doc="list of directional couplers")
    heater_pad_length = i3.PositiveNumberProperty(default=10.0, doc="Length of the pad length for the heaters.")
    heater_width = i3.PositiveNumberProperty(default=0.6, doc="Width of the heaters")
    center_wavelength = i3.PositiveNumberProperty(default=1.55, doc="Center wavelength")
    delay_lengths = i3.ListProperty(default=[100.0], doc="List of delay lengths")
    bend_radius = i3.PositiveNumberProperty(default=5.0, doc="Bend radius")
    phase_error_width_deviation = i3.NonNegativeNumberProperty(default=0.0, doc="Phase error width deviation")
    phase_error_correlation_length = i3.NonNegativeNumberProperty(default=0.0, doc="Phase error correlation length")

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
        specs = []

        for cnt, dc in enumerate(self.directional_couplers):
            specs.append(i3.Inst(f"dc_{cnt}", dc))

        tt = self.directional_couplers[-1].get_default_view(i3.LayoutView).ports[0].trace_template
        distance = 4 * self.bend_radius + 2 * self.heater_pad_length

        wav = mzi_wav(
            separation=distance,
            offset_high=2 * self.bend_radius,
            bend_radius=self.bend_radius,
            heated=False,
            heater_pad_length=self.heater_pad_length,
            trace_template=tt,
            phase_error_width_deviation=self.phase_error_width_deviation,
            phase_error_correlation_length=self.phase_error_correlation_length,
            heater_width=self.heater_width,
            name=self.name + "wf",
        )

        for cnt, delay_length in enumerate(self.delay_lengths):
            specs.append(
                i3.Inst(
                    f"wd_{cnt}",
                    mzi_wav(
                        separation=distance,
                        offset_high=2 * self.bend_radius + np.abs(delay_length / 2),
                        bend_radius=self.bend_radius,
                        heated=True,
                        heater_pad_length=self.heater_pad_length,
                        heater_width=self.heater_width,
                        trace_template=tt,
                        phase_error_width_deviation=self.phase_error_width_deviation,
                        phase_error_correlation_length=self.phase_error_correlation_length,
                        name=self.name + f"d_{cnt}",
                    ),
                )
            )
            specs.append(i3.Inst(f"wf_{cnt}", wav))

        for cnt, delay_length in enumerate(self.delay_lengths):
            if delay_length > 0:
                top = f"wd_{cnt}"
                bot = f"wf_{cnt}"
            else:
                bot = f"wd_{cnt}"
                top = f"wf_{cnt}"

            p1 = f"dc_{cnt}:out1"
            p2 = f"dc_{cnt + 1}:in1"
            specs.append(i3.Join(p1, f"{bot}:in"))
            specs.append(i3.Join(p2, f"{bot}:out"))
            p1 = f"dc_{cnt}:out2"
            p2 = f"dc_{cnt + 1}:in2"
            specs.append(i3.Join(p1, f"{top}:in"))
            specs.append(i3.Join(p2, f"{top}:out"))

            specs.append(i3.FlipV(f"wd_{cnt}") if delay_length < 0 else i3.FlipV(f"wf_{cnt}"))

        return specs

    def _default_exposed_ports(self):
        exposed_ports = {
            "dc_0:in1": "in1",
            "dc_0:in2": "in2",
            f"dc_{len(self.delay_lengths)}:out1": "out1",
            f"dc_{len(self.delay_lengths)}:out2": "out2",
        }

        for cnt in range(len(self.delay_lengths)):
            exposed_ports[f"wd_{cnt}:elec1"] = f"ht_in{cnt}"
            exposed_ports[f"wd_{cnt}:elec2"] = f"ht_out{cnt}"
        return exposed_ports
