

from Components import all as my_pdks
from ipkiss3 import all as i3
from si_fab import all as pdk
import numpy as np


spacing_x=500
spacing_y=1000

mrr1=my_pdks.microring(radius=5)
mrr2=my_pdks.microring(radius=10)
mrr3=my_pdks.microring(radius=15)
mrr4=my_pdks.microring(radius=20)
mrr5=my_pdks.microring(radius=5)
mrr6=my_pdks.microring(radius=10)
mrr7=my_pdks.microring(radius=15)
mrr8=my_pdks.microring(radius=20)
sp_tree=my_pdks.GeneralizedSplitterTree()
gc=pdk.FC_TE_1550()
pad=pdk.BONDPAD_5050()
M1_wire_tp1=pdk.M1WireTemplate().Layout(width=5)




specs=[i3.Inst("mrr1",mrr1),
       i3.Inst("mrr2",mrr2),
       i3.Inst("mrr3",mrr3),
       i3.Inst("mrr4",mrr4),
       i3.Inst("mrr5",mrr5),
       i3.Inst("mrr6",mrr6),
       i3.Inst("mrr7",mrr7),
       i3.Inst("mrr8",mrr8),
       i3.Inst("sp_tree",sp_tree),
       i3.Inst(["gc_in","gc_out1","gc_out2","gc_out3","gc_out4","gc_out5","gc_out6","gc_out7","gc_out8"],gc),
       i3.Inst([f"pad{i}"for i in range (1,9)],pad),
       i3.Inst([f"pad_{i}"for i in range (1,9)],pad)
       ]
specs+=[i3.Place("sp_tree:in",(0,0)),
        i3.Place("mrr1",(spacing_x,-spacing_y),relative_to="sp_tree:out1"),
        i3.Place("mrr2",(1.25*spacing_x,-0.8*spacing_y),relative_to="sp_tree:out2"),
        i3.Place("mrr3",(1.5*spacing_x,-0.8*spacing_y),relative_to="sp_tree:out3"),
        i3.Place("mrr4", (1.75*spacing_x,-0.4*spacing_y), relative_to="sp_tree:out4"),
        i3.Place("mrr5",(spacing_x,spacing_y),relative_to="sp_tree:out8"),
        i3.Place("mrr6",(1.25*spacing_x,0.6*spacing_y),relative_to="sp_tree:out7"),
        i3.Place("mrr7", (1.5*spacing_x,0.6*spacing_y), relative_to="sp_tree:out6"),
        i3.Place("mrr8", (1.75*spacing_x,0.4*spacing_y), relative_to="sp_tree:out5"),



        i3.ConnectManhattan("sp_tree:out1","mrr1:input",control_points=[(240,-140)]),
        i3.ConnectManhattan("sp_tree:out2","mrr2:input"),
        i3.ConnectManhattan("sp_tree:out3","mrr3:input"),
        i3.ConnectManhattan("sp_tree:out4","mrr4:input"),
        i3.ConnectManhattan("sp_tree:out5","mrr8:input"),
        i3.ConnectManhattan("sp_tree:out6","mrr7:input"),
        i3.ConnectManhattan("sp_tree:out7","mrr6:input"),
        i3.ConnectManhattan("sp_tree:out8","mrr5:input",control_points=[(240,140)]),


        ]

specs+=[i3.Place("gc_in",(-100,0),relative_to="sp_tree:in"),
        i3.Place("gc_out1",(1500,-400),relative_to="mrr1:drop",angle=180),
        i3.Place("gc_out2",(0,400),relative_to="gc_out1",angle=180),
        i3.Place("gc_out3",(0,400),relative_to="gc_out2",angle=180),
        i3.Place("gc_out4",(0,400),relative_to="gc_out3",angle=180),
        i3.Place("gc_out5", (0, 400), relative_to="gc_out4", angle=180),
        i3.Place("gc_out6", (0, 400), relative_to="gc_out5", angle=180),
        i3.Place("gc_out7", (0, 400), relative_to="gc_out6", angle=180),
        i3.Place("gc_out8", (0, 400), relative_to="gc_out7", angle=180),
        ]
specs+=[i3.ConnectManhattan("gc_in:out","sp_tree:in"),
        i3.ConnectManhattan("gc_out1:out","mrr1:through"),
        i3.ConnectManhattan("gc_out2:out","mrr2:through"),
        i3.ConnectManhattan("gc_out3:out","mrr3:through"),
        i3.ConnectManhattan("gc_out4:out","mrr4:through"),
        i3.ConnectManhattan("gc_out5:out","mrr8:through"),
        i3.ConnectManhattan("gc_out6:out","mrr7:through"),
        i3.ConnectManhattan("gc_out7:out","mrr6:through"),
        i3.ConnectManhattan("gc_out8:out","mrr5:through"),


]
specs+=[i3.Place("pad1",(600,500),relative_to="mrr5:elec1"),
        i3.Place("pad2",(800,500),relative_to="mrr5:elec1"),
        i3.Place("pad3",(1000,500),relative_to="mrr5:elec1"),
        i3.Place("pad4",(1200,500),relative_to="mrr5:elec1"),
        i3.Place("pad5", (600, -500), relative_to="mrr1:elec2"),
        i3.Place("pad6", (800, -500), relative_to="mrr1:elec2"),
        i3.Place("pad7", (1000, -500), relative_to="mrr1:elec2"),
        i3.Place("pad8", (1200, -500), relative_to="mrr1:elec2"),
        ]
specs+=[i3.Place("pad_1",(-100,500),relative_to="mrr5:elec2"),
        i3.Place("pad_2",(-300,500),relative_to="mrr5:elec2"),
        i3.Place("pad_3",(-500,500),relative_to="mrr5:elec2"),
        i3.Place("pad_4",(-700,500),relative_to="mrr5:elec2"),
        i3.Place("pad_5", (-100, -500), relative_to="mrr1:elec2"),
        i3.Place("pad_6", (-300, -500), relative_to="mrr1:elec2"),
        i3.Place("pad_7", (-500, -500), relative_to="mrr1:elec2"),
        i3.Place("pad_8", (-700, -500), relative_to="mrr1:elec2"),
        ]

specs+=[i3.ConnectElectrical("mrr5:elec1","pad1:m1",start_angle=0,end_angle=90,control_points=[i3.CP((0,-50),relative_to="pad1:m1")]),
        i3.ConnectElectrical("mrr6:elec1","pad2:m1",start_angle=0,end_angle=90,control_points=[i3.CP((0,-50),relative_to="pad2:m1")]),
        i3.ConnectElectrical("mrr7:elec1","pad3:m1",start_angle=0,end_angle=90,control_points=[i3.CP((0,-50),relative_to="pad3:m1")]),
        i3.ConnectElectrical("mrr8:elec1","pad4:m1",start_angle=0,end_angle=90,control_points=[i3.CP((0,-50),relative_to="pad4:m1")]),
        i3.ConnectElectrical("mrr1:elec1", "pad5:m1", start_angle=0, end_angle=90,control_points=[i3.CP((0,50),relative_to="pad5:m1")]),
        i3.ConnectElectrical("mrr2:elec1", "pad6:m1", start_angle=0, end_angle=90,control_points=[i3.CP((0,50),relative_to="pad6:m1")]),
        i3.ConnectElectrical("mrr3:elec1", "pad7:m1", start_angle=0, end_angle=90,control_points=[i3.CP((0,50),relative_to="pad7:m1")]),
        i3.ConnectElectrical("mrr4:elec1", "pad8:m1", start_angle=0, end_angle=90,control_points=[i3.CP((0,50),relative_to="pad8:m1")]),
        i3.ConnectElectrical("mrr5:elec2","pad_1:m1",start_angle=180,end_angle=90,control_points=[i3.CP((0,-50),relative_to="pad_1:m1")]),
        i3.ConnectElectrical("mrr6:elec2","pad_2:m1",start_angle=180,end_angle=90,control_points=[i3.CP((0,-50),relative_to="pad_2:m1")]),
        i3.ConnectElectrical("mrr7:elec2","pad_3:m1",start_angle=180,end_angle=90,control_points=[i3.CP((0,-50),relative_to="pad_3:m1")]),
        i3.ConnectElectrical("mrr8:elec2","pad_4:m1",start_angle=180,end_angle=90,control_points=[i3.CP((0,-50),relative_to="pad_4:m1")]),
        i3.ConnectElectrical("mrr1:elec2","pad_5:m1",start_angle=180,end_angle=90,control_points=[i3.CP((0,-50),relative_to="pad_5:m1")]),
        i3.ConnectElectrical("mrr2:elec2","pad_6:m1",start_angle=180,end_angle=90,control_points=[i3.CP((0,-50),relative_to="pad_6:m1")]),
        i3.ConnectElectrical("mrr3:elec2","pad_7:m1",start_angle=180,end_angle=90,control_points=[i3.CP((0,-50),relative_to="pad_7:m1")]),
        i3.ConnectElectrical("mrr4:elec2","pad_8:m1",start_angle=180,end_angle=90,control_points=[i3.CP((0,-50),relative_to="pad_8:m1")]),

        ]







circuit=i3.Circuit(specs=specs)
circuit_layout=circuit.Layout()
circuit_layout.visualize(annotate=False)
circuit_model = circuit.CircuitModel()
wavelengths = np.linspace(1.5, 1.6, 501)
S_total = circuit_model.get_smatrix(wavelengths=wavelengths)








