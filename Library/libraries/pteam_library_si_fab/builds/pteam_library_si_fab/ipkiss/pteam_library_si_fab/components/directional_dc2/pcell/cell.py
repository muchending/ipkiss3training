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
import ipkiss3.all as i3


class DirectionalCouplerDC2(pdk.SiDirectionalCouplerSPower):
    class CircuitModel(i3.CircuitModelView):
        # Override the DC model - we base it on the simple DC2 model
        def _generate_model(self):
            return i3.cml.DC2(
                cross_coupling=[self.power_fraction],
                insertion_loss=0,
                center_wavelength=self.target_wavelength,
            )
