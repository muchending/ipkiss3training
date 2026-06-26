from Components import all as my_pdks
from ipkiss3 import all as i3
from si_fab import all as pdk
import csv
from pathlib import Path

class spt(i3.Circuit):
    spacing_x = i3.PositiveNumberProperty(default=50.0, doc="X direction spacing")
    spacing_y = i3.PositiveNumberProperty(default=100.0, doc="Y direction spacing")

    def _instance_specs(self):
        spt = my_pdks.GeneralizedSplitterTree(n_levels=2)
        gc=pdk.FC_TE_1550()

        specs=[]
        specs+=[i3.Inst("spt",spt),
                i3.Inst("gc_in",gc),
                i3.Inst("gc_out1", gc),
                i3.Inst("gc_out2", gc),
                i3.Inst("gc_out3", gc),
                i3.Inst("gc_out4", gc),


        ]
        return specs
    def _default_specs(self):
        specs=self._instance_specs()
        specs+=[i3.Place("spt",position=(0,0)),
                i3.Place("gc_in",position=(-self.spacing_x,0),relative_to="spt:in"),
                i3.Place("gc_out1",position=(self.spacing_x,2*self.spacing_y),relative_to="spt:out1",angle=180),
                i3.Place("gc_out2", position=(self.spacing_x, 0), relative_to="spt:out2",angle=180),
                i3.Place("gc_out3", position=(self.spacing_x, 0), relative_to="spt:out3", angle=180),
                i3.Place("gc_out4", position=(self.spacing_x, -2*self.spacing_y), relative_to="spt:out4", angle=180),


                ]
        specs+=[i3.ConnectManhattan("gc_in:out","spt:in"),
                i3.ConnectManhattan("gc_out1:out", "spt:out4",),
                i3.ConnectManhattan("gc_out2:out", "spt:out2", ),
                i3.ConnectManhattan("gc_out3:out", "spt:out3", ),
                i3.ConnectManhattan("gc_out4:out", "spt:out1", ),

                ]
        return specs
    def _default_exposed_ports(self):
        exposed_ports ={
            "gc_in:vertical_in": "opt_in",
            "gc_out1:vertical_in": "opt_out1",
            "gc_out2:vertical_in": "opt_out2",
            "gc_out3:vertical_in": "opt_out3",
            "gc_out4:vertical_in": "opt_out4",

        }
        return  exposed_ports

if __name__ == "__main__":
    spt=spt()
    spt_layout=spt.Layout()
    # mmi_layout.visualize()
    for port in spt_layout.ports:
        print(port.name, port.position)
    ROOT=Path(__file__).resolve().parents[4]
    PORT_DIR=ROOT/"tape_out"/"port"
    PORT_DIR.mkdir(parents=True, exist_ok=True)
    with open(PORT_DIR/"spt_ports.csv", "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["Port", "X(um)", "Y(um)"])

            for port in spt_layout.ports:
                    x, y = port.position
                    writer.writerow([port.name, x, y])
    elems=i3.stub_acute_angles(spt_layout, stub_width=2, angle_threshold=0.01, grow_amount=0.02)
    mmi_final = i3.LayoutCell().Layout(elements=elems)
    mmi_final.visualize_violations()






