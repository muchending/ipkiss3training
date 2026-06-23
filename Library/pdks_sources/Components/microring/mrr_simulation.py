import Components.microring.mrr_Pcell as pdks
import numpy as np
from ipkiss3 import all as i3

mrr=pdks.microring()
mrr_layout=mrr.Layout(radius=100)
mrr_layout.visualize(annotate=True)



wavelengths = np.linspace(1.5, 1.6, 501)
mrr_model=mrr.CircuitModel()
mrr_model_view=mrr_model._generate_model()
S=i3.circuit_sim.test_circuitmodel(mrr_model_view, wavelengths)
S.visualize(term_pairs=[("input", "through")], scale="dB", ylabel="Transmission [dB]")


