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
from ipkiss3 import all as i3
import pteam_library_si_fab.all as pt_lib
import numpy as np
import circuit_analyzer.all as ca


class Mux4(i3.Circuit):
    """Four-way wavelength demultiplexer with a passband of 25% of the FSR at the center_wavelength.
    It is implemented by staging a two-way demultiplexer on half the FSR, followed by two two-way
    de-multiplexers tuned to the frequencies coming out of the first stage.
    """

    spacing_x = i3.PositiveNumberProperty(default=100.0, doc="Port-to-port spacing between the MUXs in the x-direction")
    spacing_y = i3.PositiveNumberProperty(default=150.0, doc="Port-to-port spacing between the MUXs in the y-direction")
    bend_radius = i3.PositiveNumberProperty(default=5.0, doc="Bend radius")
    fsr = i3.PositiveNumberProperty(default=0.02, doc="Free spectral range of the MUX4")
    center_wavelength = i3.PositiveNumberProperty(default=1.55, doc="Center wavelength")
    stage_1 = i3.ChildCellProperty(doc="MUX2 for the first stage")
    stage_2_up = i3.ChildCellProperty(doc="MUX2 for the second stage (up)")
    stage_2_down = i3.ChildCellProperty(doc="MUX2 for the second stage (down)")

    def _default_stage_1(self):
        return pt_lib.Mux2(
            center_wavelength=self.center_wavelength,
            fsr=self.fsr / 2.0,
            name=self.name + "_stage1",
        )

    def _default_stage_2_up(self):
        return pt_lib.Mux2(
            center_wavelength=self.center_wavelength + self.fsr / 4,
            fsr=self.fsr,
            name=self.name + "_stage2_up",
        )

    def _default_stage_2_down(self):
        return pt_lib.Mux2(
            center_wavelength=self.center_wavelength,
            fsr=self.fsr,
            name=self.name + "_stage2_down",
        )

    def _default_specs(self):
        specs = [
            i3.Inst("mux_0_0", self.stage_1),
            i3.Inst("mux_1_0", self.stage_2_down),
            i3.Inst("mux_1_1", self.stage_2_up),
            i3.Place("mux_0_0", (0, 0)),
            i3.Place("mux_1_0:in1", (self.spacing_x, -self.spacing_y / 2), relative_to="mux_0_0:out1"),
            i3.Place("mux_1_1:in1", (self.spacing_x, +self.spacing_y / 2), relative_to="mux_0_0:out2"),
        ]

        specs += [
            i3.ConnectManhattan(
                [
                    ("mux_0_0:out1", "mux_1_0:in1"),
                    ("mux_0_0:out2", "mux_1_1:in1"),
                ],
                bend_radius=self.bend_radius,
            )
        ]
        return specs

    def _default_exposed_ports(self):
        return {
            "mux_0_0:in1": "in1",
            "mux_0_0:in2": "in2",
            "mux_1_0:in2": "in3",
            "mux_1_1:in2": "in4",
            "mux_1_0:out1": "out1",
            "mux_1_0:out2": "out2",
            "mux_1_1:out1": "out3",
            "mux_1_1:out2": "out4",
        }


if __name__ == "__main__":
    # Writing the layout
    cell = Mux4(
        name="MUX4",
        fsr=0.05,
        center_wavelength=1.55,
        spacing_x=50,
        spacing_y=80,
    )
    cell_lv = cell.Layout()
    cell_lv.write_gdsii("mux4.gds")
    # Simulating the circuit
    wavelengths = np.linspace(1.53, 1.57, 501)

    tracer = ca.Tracer(circuit=cell)
    result = tracer.run(wavelengths, progress_bar=True)
    result.visualize()
