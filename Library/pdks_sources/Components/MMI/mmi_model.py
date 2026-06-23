from si_fab import all as pdk
from ipkiss3 import all as i3
import numpy as np  # useful numerical package
import json


class MMI1muti2model(i3.CompactModel):
    parameters = ["center_wavelength",
                  "reflection_in",
                  "reflection_out",
                  "transmission",
                   ]

    terms = [i3.OpticalTerm(name="in1"),
             i3.OpticalTerm(name="out1"),
             i3.OpticalTerm(name="out2")]

    def calculate_smatrix(parameters, env, S):
        reflection_in = np.polyval(parameters.reflection_in, env.wavelength - parameters.center_wavelength)
        reflection_out = np.polyval(parameters.reflection_out, env.wavelength - parameters.center_wavelength)
        transmission = np.polyval(parameters.transmission, env.wavelength - parameters.center_wavelength)
        S["in1", "out1"] = S["out1", "in1"] = S["in1", "out2"] = S["out2", "in1"] = transmission
        S["in1", "in1"] = reflection_in
        S["out1", "out1"] = S["out2", "out2"] = reflection_out




if __name__ == "__main__":
    transmission = [6689915, -372855, -23043.0, 1146.79, 12.0728, -1.74281, 0.0306654, 0.694049]
    ref_in = [15704086, 1274526, -92758.5, -4422.89, 185.873, 2.55599, -0.177514, 0.00621437]

    wavelengths = np.linspace(1.5, 1.6, 101)  # regularly spaced array of wavelengths

    S = i3.circuit_sim.test_circuitmodel(
        MMI1muti2model(
            center_wavelength=1.55,
            transmission=transmission,
            reflection_in=ref_in,
            reflection_out=np.array([0.001]),
        ),
        wavelengths=wavelengths,
    )

    S.visualize(term_pairs=[("in1", "out1")], scale="dB", ylabel="Transmission [dB]")
    S.visualize(term_pairs=[("out1", "out1"), ("in1", "in1")], scale="dB", ylabel="Reflection [dB]")


