

from Components import all as my_pdks
from ipkiss3 import all as i3
from si_fab import all as pdk

mrr2=my_pdks.microring(radius=5)
mrr1=my_pdks.microring(radius=10)
splitter_tree=my_pdks.GeneralizedSplitterTree()
pad=pdk.BONDPAD_5050()
ec=pdk.SiNInvertedTaper()

specs=[
    i3.Inst(name="mrr1",reference=mrr1),
    i3.Inst(name="mrr2",reference=mrr2),
    i3.Inst("pad" ,pad),
    i3.Inst("sp_t",reference=splitter_tree),
    i3.Inst("ec",ec),]

specs+=[i3.Place("mrr1:input",(0,0))]
specs+=[i3.Place("mrr2:input",(50,0))]
specs+=[i3.Place("pad",(100,0))]
specs+=[i3.Place("sp_t:out8",(-100,0),relative_to="mrr1:input")]
specs+=[i3.Place("ec",position=(-100,-100))]

specs+=[i3.ConnectElectrical("mrr1:elec1","pad:m1",start_angle=90,end_angle=90,)]

circuit=i3.Circuit(specs=specs)
circuit_layout=circuit.Layout()
circuit_layout.visualize(annotate=True)




