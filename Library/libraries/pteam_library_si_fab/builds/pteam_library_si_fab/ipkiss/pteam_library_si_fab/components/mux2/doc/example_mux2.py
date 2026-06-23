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


from si_fab import all as pdk  # noqa
from pteam_library_si_fab import all as pt_lib
from ipkiss3 import all as i3
import numpy as np
import matplotlib.pyplot as plt

# Writing the layout
cell = pt_lib.Mux2(
    name="MUX2",
    fsr=0.02,
    center_wavelength=1.55,
)
cell_lv = cell.Layout()
cell_lv.visualize(annotate=True)

# Simulating the circuit
wavelengths = np.linspace(1.5, 1.6, 501)
cell_cm = cell.CircuitModel()
S = cell_cm.get_smatrix(wavelengths=wavelengths)
# Preparing lists for plotting
S_stages = [S]
names = ["S_total"]
n_ports = [2]
channels = [cell.center_wavelength + cnt * cell.fsr / 2 for cnt in range(2)]
# Plotting
for S, name, n_port in zip(S_stages, names, n_ports):
    for p in range(n_port):
        plt.plot(
            wavelengths,
            i3.signal_power_dB(S["in1", f"out{p + 1}"]),
            "-",
            label=f"{name}_in1_out{p + 1}",
            linewidth=2.2,
        )
    for x in channels:
        plt.axvline(x=x, linewidth=2.2, color="black")
    plt.xlabel("Wavelengths [um]", fontsize=16)
    plt.ylabel("Transmission [dB]", fontsize=16)
    plt.title(f"{name} - Transmission", fontsize=18)
    plt.legend(fontsize=14, loc="center left", bbox_to_anchor=(1, 0.5))
    plt.xlim(1.5, 1.6)
    plt.ylim((-50, 2))
    plt.show()
