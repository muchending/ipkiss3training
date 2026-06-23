

import Components.MMI.mmi_pcell as pdks
import numpy as np
from ipkiss3 import all as i3


mmi=pdks.MMI1muti2()
mmi_layout=mmi.layout()
mmi_layout.visualize(annotate=True)

wavelengths = np.linspace(1.5, 1.6, 501)
mmi_model = mmi.CircuitModel()
mmi_model_view=mmi_model.generate_model()

S=i3.circuit_sim.test_circuitmodel(mmi_model_view, wavelengths)
S.visualize(term_pairs=[("in1", "out1")], scale="dB", ylabel="Transmission [dB]")





