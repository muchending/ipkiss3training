from Components import all as my_pdks
from ipkiss3 import all as i3
from si_fab import all as pdk
import csv
from pathlib import Path

class mmi(i3.Circuit):
    spacing_x = i3.PositiveNumberProperty(default=50.0, doc="X direction spacing")
    spacing_y = i3.PositiveNumberProperty(default=50.0, doc="Y direction spacing")

    def _instance_specs(self):
        mmi = my_pdks.MMI1muti2()
        gc=pdk.FC_TE_1550()

        specs=[]
        specs+=[i3.Inst("mmi",mmi),
                i3.Inst("gc_in",gc),
                i3.Inst("gc_out1", gc),
                i3.Inst("gc_out2", gc),

        ]
        return specs
    def _default_specs(self):
        specs=self._instance_specs()
        specs+=[i3.Place("mmi",position=(0,0)),
                i3.Place("gc_in",position=(-self.spacing_x,0),relative_to="mmi:in1"),
                i3.Place("gc_out1",position=(self.spacing_x,+self.spacing_y),relative_to="mmi:out1",angle=180),
                i3.Place("gc_out2", position=(self.spacing_x, -self.spacing_y), relative_to="mmi:out2",angle=180),
                ]
        specs+=[i3.ConnectManhattan("gc_in:out","mmi:in1"),
                i3.ConnectManhattan("gc_out2:out", "mmi:out1",),
                i3.ConnectManhattan("gc_out1:out", "mmi:out2", ),
                ]
        return specs
    def _default_exposed_ports(self):
        exposed_ports ={
            "gc_in:vertical_in": "opt_in",
            "gc_out1:vertical_in": "opt_out1",
            "gc_out2:vertical_in": "opt_out2",

        }
        return  exposed_ports

if __name__ == "__main__":
    mmi=mmi()
    mmi_layout=mmi.Layout()
    # mmi_layout.visualize()
    for port in mmi_layout.ports:
        print(port.name, port.position)
    ROOT=Path(__file__).resolve().parents[4]
    PORT_DIR=ROOT/"tape_out"/"port"
    PORT_DIR.mkdir(parents=True, exist_ok=True)
    with open(PORT_DIR/"mmi_ports.csv", "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["Port", "X(um)", "Y(um)"])

            for port in mmi_layout.ports:
                    x, y = port.position
                    writer.writerow([port.name, x, y])
    elems=i3.stub_acute_angles(mmi_layout, stub_width=2, angle_threshold=0.01, grow_amount=0.02)
    mmi_final = i3.LayoutCell().Layout(elements=elems)
    mmi_final.visualize_violations()






