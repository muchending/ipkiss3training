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


from ipkiss3 import all as i3
from picazzo3.routing.place_route import ConnectComponents


def simulate_mux2(mux2, heater_voltages, wavelengths, debug=False):
    """Simulation recipe for a Mux2Heated

    Simulates the S-parameters for the specified heater voltages and wavelengths

    Parameters
    ----------
    mux2 : Mux2 cell
        Mux2 cell
    heater_voltages : [float]
        list of heater voltages
    wavelengths : [float]
        list of wavelengths at which we simulate

    Returns
    -------
    dict
        Dictionary with keys out1 and out2
    """

    # Define the function to create the sources' functions

    sources = dict()
    sources["in1"] = i3.FunctionExcitation(
        port_domain=i3.OpticalDomain,
        excitation_function=lambda t: 1.0,
    )

    for cnt, hv in enumerate(heater_voltages):
        sources[f"ht_in{cnt}"] = i3.FunctionExcitation(
            port_domain=i3.ElectricalDomain,
            excitation_function=lambda t: hv,
        )
        sources[f"ht_out{cnt}"] = i3.FunctionExcitation(
            port_domain=i3.ElectricalDomain,
            excitation_function=lambda t: 0.0,
        )

    # Define probes
    probes = dict()
    probes["out1"] = i3.Probe(port_domain=i3.OpticalDomain)
    probes["out2"] = i3.Probe(port_domain=i3.OpticalDomain)

    t0 = 0.0
    t1 = 2.0
    dt = 1.0

    children = {"DUT": mux2}

    links = []
    for key, val in sources.items():
        children[f"src_{key}"] = val
        p1 = f"src_{key}:out"
        p2 = f"DUT:{key}"
        links.append((p1, p2))

    for key, val in probes.items():
        children[f"prb_{key}"] = val
        p1 = f"prb_{key}:in"
        p2 = f"DUT:{key}"
        links.append((p1, p2))

    sim_circuit = ConnectComponents(child_cells=children, links=links)
    cm = sim_circuit.CircuitModel()

    s_out1 = []
    s_out2 = []

    for w in wavelengths:
        res = cm.get_time_response(t0=t0, t1=t1, dt=dt, center_wavelength=w, debug=debug)

        s_out1.append(res["prb_out1"][1])
        s_out2.append(res["prb_out2"][1])

    return {"out1": s_out1, "out2": s_out2}
