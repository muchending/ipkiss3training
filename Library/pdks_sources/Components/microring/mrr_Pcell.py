from setuptools.namespaces import flatten
from si_fab import all as pdk
from ipkiss3 import all as i3
import numpy as np  # useful numerical package
import json
import Components.HeatedWaveguide.hw_pcell as ht
import Components.microring.mrr_model as mm

import os


class  microring(i3.PCell):
    """A add_drop microring"""
    _name_prefix = "add_drop_microring"
    trace_template=i3.TraceTemplateProperty(doc="the template of access waveguide")
    gap=i3.PositiveNumberProperty(default=0.3,doc="the coupling gap")
    radius=i3.FloatProperty(default=10,doc="the radius of the microring")
    bus_width=i3.PositiveNumberProperty(default=0.45,doc="the width of the bus waveguide")
    bus_length=i3.PositiveNumberProperty(default=0.1,doc="the length of the bus waveguide")
    heater_width = i3.PositiveNumberProperty(default=0.6, doc="加热器宽度")
    heater_offset = i3.PositiveNumberProperty(default=1.0, doc="加热器与波导的偏移")
    def _default_trace_template(self):
        return pdk.SiWireWaveguideTemplate()

    class Layout(i3.LayoutView):


        def generate(self,layout):
            trace_template=self.trace_template
            gap=self.gap
            bus_width=self.bus_width
            radius=self.cell.radius
            bus_length=radius*2+4.0
            core_layer = trace_template.core_layer
            cladding_layer = trace_template.cladding_layer
            core_width = trace_template.core_width
            """bus waveguide"""
            layout+=[i3.Rectangle(
                layer=core_layer,
                center=(0.5*bus_length,0.0),
                box_size=(bus_length,bus_width)

            )]
            heated_ring=ht.heatedringwaveguide(heater_width=self.heater_width,
                                            heater_offset=self.heater_offset,
                                            trace_template=self.trace_template,
                                            )

            ring_radius = radius + 0.5 * bus_width
            ring_shape=i3.ShapeArc(
                    radius=ring_radius,
                    start_angle=0,
                    end_angle=360,
                    center=(0.5 * bus_length, radius + gap+bus_width+0.1),
                )

            heated_ring_layout = heated_ring.Layout(
                shape=ring_shape,
                flatten_contents=False
            )

            layout+=heated_ring_layout.elements
            layout+=[i3.CirclePath(
                layer=core_layer,
                center=(0.5 * bus_length, radius + gap+bus_width+0.1),
                angle_step=1,
                radius=ring_radius,
            )]


            layout+=[i3.Rectangle(
                layer=core_layer,
                center=(0.5 * bus_length, gap+3*bus_width+2*radius),
                box_size=(bus_length, bus_width)

            )]
            layout += [i3.Rectangle(
                layer=cladding_layer,
                center=(0.5*bus_length,gap+1.5*bus_width+radius),
                box_size=(1.2*bus_length, 2*radius+2*gap+2*bus_width+4.0),

            )]
            layout += [i3.OpticalPort(
                name="input",
                position=(0.0, 0.0),
                angle=180
            )]
            layout += [i3.OpticalPort(
                name="through",
                position=(bus_length, 0.0),
                angle=0
            )]
            layout += [i3.OpticalPort(
                name="drop",
                position=(0.0, gap + 3 * bus_width + 2 * radius),
                angle=180
            )]
            layout += [i3.OpticalPort(
                name="add",
                position=(bus_length, gap + 3 * bus_width + 2 * radius),
                angle=0
            )]
            layout += heated_ring_layout.ports["elec1"].modified_copy(name="elec1")
            layout += heated_ring_layout.ports["elec2"].modified_copy(name="elec2")

            return layout

    class Netlist(i3.NetlistFromLayout):
        pass

    class CircuitModel(i3.CircuitModelView):

        center_wavelength = i3.PositiveNumberProperty(doc="center_wavelength")
        through_response = i3.NumpyArrayProperty(doc="Polynomial coefficients for the through")
        drop_response =i3.NumpyArrayProperty(doc="Polynomial coefficients for the drop")
        reflection_in1 = i3.NumpyArrayProperty(doc="Polynomial coefficients for the reflection")
        reflection_in2 = i3.NumpyArrayProperty(doc="Polynomial coefficients for the reflection")
        reflection_out1 = i3.NumpyArrayProperty(doc="Polynomial coefficients for the reflection")
        reflection_out2 = i3.NumpyArrayProperty(doc="Polynomial coefficients for the reflection")
        data_file = i3.StringProperty(doc="多项式系数")
        def _default_data_file(self):
            return "mrr_1550.json"
        def get_data(self,data_file=None):
            if data_file is None:
                data_file = self.data_file
            script_dir = os.path.dirname(os.path.abspath(__file__))
            data_file = os.path.join(script_dir, 'mrr_1550.json')
            with open(data_file) as f:
                results_np = json.load(f)  # the json module is included in Pyton and makes it easy to load data
                center_wavelength = results_np["center_wavelength"]
                through_response = np.array(results_np["through_response"])
                drop_response = np.array(results_np["drop_response"])
                reflection_in1 = np.array(results_np["reflection_in1"])
                reflection_in2 = np.array(results_np["reflection_in2"])
                reflection_out1 = np.array(results_np["reflection_out1"])
                reflection_out2 = np.array(results_np["reflection_out2"])
            return center_wavelength, through_response,drop_response,reflection_in1, reflection_in2,reflection_out1,reflection_out2


        def _default_center_wavelength(self):
            cw=self.get_data()[0]
            return cw
        def _default_through_response(self):
            tr=self.get_data()[1]
            return tr
        def _default_drop_response(self):
            dr=self.get_data()[2]
            return dr
        def _default_reflection_in1(self):
            ri1=self.get_data()[3]
            return ri1
        def _default_reflection_in2(self):
            ri2 = self.get_data()[4]
            return ri2
        def _default_reflection_out1(self):
            ro1=self.get_data()[5]
            return ro1
        def _default_reflection_out2(self):
            ro2=self.get_data()[6]
            return ro2
        def _generate_model(self):
            return mm.mrr_model(center_wavelength=self.center_wavelength,
                                through_response=self.through_response,
                                drop_response=self.drop_response,
                                reflection_in1=self.reflection_in1,
                                reflection_in2=self.reflection_in2,
                                reflection_out1=self.reflection_out1,
                                reflection_out2=self.reflection_out2,)

