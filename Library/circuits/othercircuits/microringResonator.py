from Components import all as my_pdks
from ipkiss3 import all as i3

class microringArray(i3.Circuit):
    mrr=i3.ChildCellProperty(doc="microringresonator")
    spacing_x = i3.PositiveNumberProperty(default=100.0, doc="Horizontal spacing between the microring.")
    spacing_y = i3.PositiveNumberProperty(default=50.0, doc="Vertical spacing between the microring.")


    def _default_microring(self):
        return my_pdks.microring()

    