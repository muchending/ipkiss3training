from Components import all as my_pdks
from ipkiss3 import all as i3
from si_fab import all as pdk
import csv
from pathlib import Path

class mrr(i3.Circuit):
    spacing_x = i3.PositiveNumberProperty(default=50.0, doc="X direction spacing")
    spacing_y = i3.PositiveNumberProperty(default=50.0, doc="Y direction spacing")

    def _instance_specs(self):
        mrr = my_pdks.microring()
        gc=pdk.FC_TE_1550()

        specs=[]
        specs+=[i3.Inst("mrr",mrr),
                i3.Inst("gc_input",gc),
                i3.Inst("gc_through", gc),
                i3.Inst("gc_drop", gc),
                i3.Inst("gc_add", gc),


        ]
        return specs
    def _default_specs(self):
        specs=self._instance_specs()
        specs+=[i3.Place("mrr",position=(0,0)),
                i3.Place("gc_input",position=(-self.spacing_x,-self.spacing_y),relative_to="mrr:input"),
                i3.Place("gc_through",position=(self.spacing_x,-self.spacing_y),relative_to="mrr:through",angle=180),
                i3.Place("gc_drop", position=(-self.spacing_x, self.spacing_y), relative_to="mrr:drop",angle=0),
                i3.Place("gc_add", position=(self.spacing_x, self.spacing_y), relative_to="mrr:add", angle=180),

                ]
        specs+=[i3.ConnectManhattan("gc_input:out","mrr:input"),
                i3.ConnectManhattan("gc_through:out", "mrr:through",),
                i3.ConnectManhattan("gc_drop:out", "mrr:drop", ),
                i3.ConnectManhattan("gc_add:out", "mrr:add", ),

                ]
        return specs
    def _default_exposed_ports(self):
        exposed_ports ={
            "gc_input:vertical_in": "opt_in",
            "gc_through:vertical_in": "opt_through",
            "gc_drop:vertical_in": "opt_drop",
            "gc_add:vertical_in": "opt_add",
            "mrr:elec1":"ele1",
            "mrr:elec2":"ele2"

        }
        return  exposed_ports

if __name__ == "__main__":
    mrr=mrr()
    mrr_layout=mrr.Layout()
    # mmi_layout.visualize()
    for port in mrr_layout.ports:
        print(port.name, port.position)
    ROOT=Path(__file__).resolve().parents[4]
    PORT_DIR=ROOT/"tape_out"/"port"
    PORT_DIR.mkdir(parents=True, exist_ok=True)
    with open(PORT_DIR/"mrr_ports.csv", "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["Port", "X(um)", "Y(um)"])

            for port in mrr_layout.ports:
                    x, y = port.position
                    writer.writerow([port.name, x, y])
    elems=i3.stub_acute_angles(mrr_layout, stub_width=2, angle_threshold=0.01, grow_amount=0.02)
    mmi_final = i3.LayoutCell().Layout(elements=elems)
    mmi_final.visualize_violations()






