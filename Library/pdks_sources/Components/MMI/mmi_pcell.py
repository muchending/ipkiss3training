from si_fab import all as pdk
from ipkiss3 import all as i3
import numpy as np  # useful numerical package
import json


import Components.MMI.mmi_model as md

"""define a mmi used to splitter tree"""



class MMI1muti2(i3.PCell):
    """MMI with 1 input and 2 outputs."""
    name = "MMI1muti2"
    trace_template = i3.TraceTemplateProperty(doc="Trace template of the access waveguide.")
    width=i3.PositiveNumberProperty(default=4.0,doc="Width of the mmi section")
    length=i3.PositiveNumberProperty(default=20.0,doc="Length of the mmi section")
    taper_width=i3.PositiveNumberProperty(default=1.0,doc="Width of the taper")
    taper_length=i3.PositiveNumberProperty(default=5.0,doc="Length of the taper")
    waveguide_spacing=i3.PositiveNumberProperty(default=2.0,doc="spacing between waveguides")



    def _default_trace_template(self):
        return pdk.SiWireWaveguideTemplate()



    class layout(i3.LayoutView):
        def generate(self,layout):
            length = self.length
            width = self.width
            taper_length = self.taper_length
            taper_width = self.taper_width
            half_waveguide_spacing = 0.5 * self.waveguide_spacing
            trace_template = self.trace_template
            core_layer = trace_template.core_layer
            cladding_layer = trace_template.cladding_layer
            core_width = trace_template.core_width


            layout +=[i3.Rectangle(
                layer=core_layer,
                center=(0.5*length,0.0),
                box_size=(length,width)
            )]
            layout += i3.Wedge(  # we use "i3.Wedge()" to create the input and output tapers
                layer=core_layer,
                begin_coord=(-taper_length, 0.0),
                end_coord=(0.0, 0.0),
                begin_width=core_width,
                end_width=taper_width,
            )
            layout += i3.Wedge(
                layer=core_layer,
                begin_coord=(length, half_waveguide_spacing),
                end_coord=(length+taper_length, half_waveguide_spacing),
                begin_width=taper_width,
                end_width=core_width,
            )
            layout += i3.Wedge(
                layer=core_layer,
                begin_coord=(length, -half_waveguide_spacing),
                end_coord=(length+taper_length, -half_waveguide_spacing),
                begin_width=taper_width,
                end_width=core_width,
            )

            layout += i3.Rectangle(  # we can add a cladding layer as well to improve performance
                layer=cladding_layer,
                center=(0.5*length, 0.0),
                box_size=(length + 2 * taper_length, width + 2.0),
            )
            layout += i3.OpticalPort(  # you can also add electrical ports in the same way
                name="in1",  # this is the port name you will see when this PCell is used
                position=(-taper_length, 0.0),  # position is coincident with the relevant element
                angle=180.0,  # angle with respect to the x-axis, always facing outwards from the port
                trace_template=trace_template,  # the trace template for the optical port
            )
            layout += i3.OpticalPort(
                name="out1",
                position=(length + taper_length, -half_waveguide_spacing),
                angle=0.0,
                trace_template=trace_template,
            )
            layout += i3.OpticalPort(
                name="out2",
                position=(length + taper_length, half_waveguide_spacing),
                angle=0.0,
                trace_template=trace_template,
            )


            return layout

    class Netlist(i3.NetlistFromLayout):
        pass
    class CircuitModel(i3.CircuitModelView):

        center_wavelength = i3.PositiveNumberProperty(doc="center_wavelength")
        transmission = i3.NumpyArrayProperty(doc="Polynomial coefficients for the transmission")
        reflection_in = i3.NumpyArrayProperty(doc="Polynomial coefficients for the reflection_in")
        reflection_out = i3.NumpyArrayProperty(doc="Polynomial coefficients for the reflection_out")
        data_file=i3.StringProperty(doc="多项式系数")
        def _default_data_file(self):
            return "mmi_1550.json"
        def get_data(self,data_file=None):
            if data_file is None:
                data_file = self.data_file
            with open(data_file) as f:
                results_np = json.load(f)  # the json module is included in Pyton and makes it easy to load data
                center_wavelength = results_np["center_wavelength"]
                transmission = np.array(results_np["pol_trans"])
                reflection_in = np.array(results_np["pol_refl"])
            return center_wavelength, transmission, reflection_in
        def load_data(self):
            self.center_wavelength, self.transmission, self.reflection_in = self.get_data()
            return self.center_wavelength, self.transmission, self.reflection_in
        def _default_center_wavelength(self):
            return 1.55

        def _default_transmission(self):
            _,trans,_ = self.get_data()
            return trans

        def _default_reflection_in(self):
            _,_,reflection_in = self.get_data()
            return reflection_in

        def _default_reflection_out(self):
            return np.array([0.01])


        def generate_model(self):
            return md.MMI1muti2model(center_wavelength=self.center_wavelength,
                                      transmission=self.transmission,
                                      reflection_in=self.reflection_in,
                                      reflection_out=self.reflection_out)




