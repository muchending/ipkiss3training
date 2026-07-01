from Components import all as my_pdks
from ipkiss3 import all as i3
from si_fab import all as pdk
import numpy as np
import csv
from pathlib import Path

class MRRArrayCircuit(i3.Circuit):
    """MRR array circuit in the current Luceda/IPKISS Circuit style.

    In recent IPKISS versions, the ``insts`` property / ``_default_insts``
    workflow is deprecated for i3.Circuit. Instances are therefore defined
    directly in ``_default_specs`` using ``i3.Inst`` first, followed by
    placement and routing specs.
    """

    spacing_x = i3.PositiveNumberProperty(default=500.0, doc="X direction spacing")
    spacing_y = i3.PositiveNumberProperty(default=1000.0, doc="Y direction spacing")

    def _mrr_cells(self):
        """Create the eight MRR cells."""
        radii = [5, 10, 15, 20, 5, 10, 15, 20]
        return [my_pdks.microring(radius=radius) for radius in radii]

    def _instance_specs(self):
        """Instantiate all child cells first, using i3.Inst inside specs."""
        mrr_cells = self._mrr_cells()
        gc = pdk.FC_TE_1550()
        pad = pdk.BONDPAD_5050()
        sp_tree = my_pdks.GeneralizedSplitterTree()

        specs = []

        # MRRs: each ring has its own radius, so instantiate them one by one.
        for idx, mrr in enumerate(mrr_cells, start=1):
            specs.append(i3.Inst(f"mrr{idx}", mrr))

        # Splitter tree.
        specs.append(i3.Inst("sp_tree", sp_tree))

        # Grating couplers: same cell reused under different instance names.
        specs.append(
            i3.Inst(
                ["gc_in"] + [f"gc_out{idx}" for idx in range(1, 9)],
                gc,
            )
        )

        # Pads: same pad cell reused under different instance names.
        specs.append(
            i3.Inst(
                [f"pad{idx}" for idx in range(1, 9)]
                + [f"pad_{idx}" for idx in range(1, 9)],
                pad,
            )
        )

        return specs

    def _default_specs(self):
        """Define instances first, then place and connect them."""
        specs = []
        specs += self._instance_specs()
        specs += self._splitter_and_mrr_specs()
        specs += self._gc_specs()
        specs += self._pad_specs()
        specs += self._electrical_specs()
        return specs

    def _splitter_and_mrr_specs(self):
        sx = self.spacing_x
        sy = self.spacing_y

        return [
            # Splitter tree placement.
            i3.Place("sp_tree:in", (0, 0)),

            # MRR placement.
            i3.Place("mrr1", (sx, -sy), relative_to="sp_tree:out1"),
            i3.Place("mrr2", (1.25 * sx, -0.8 * sy), relative_to="sp_tree:out2"),
            i3.Place("mrr3", (1.5 * sx, -0.8 * sy), relative_to="sp_tree:out3"),
            i3.Place("mrr4", (1.75 * sx, -0.4 * sy), relative_to="sp_tree:out4"),
            i3.Place("mrr5", (sx, sy), relative_to="sp_tree:out8"),
            i3.Place("mrr6", (1.25 * sx, 0.6 * sy), relative_to="sp_tree:out7"),
            i3.Place("mrr7", (1.5 * sx, 0.6 * sy), relative_to="sp_tree:out6"),
            i3.Place("mrr8", (1.75 * sx, 0.4 * sy), relative_to="sp_tree:out5"),

            # Splitter-to-MRR optical routing.
            i3.ConnectManhattan("sp_tree:out1", "mrr1:input", control_points=[(240, -140)],bend_radius=10,cover_bends=True),
            i3.ConnectManhattan("sp_tree:out2", "mrr2:input",bend_radius=10,cover_bends=True),
            i3.ConnectManhattan("sp_tree:out3", "mrr3:input",bend_radius=10,cover_bends=True),
            i3.ConnectManhattan("sp_tree:out4", "mrr4:input",bend_radius=10,cover_bends=True),
            i3.ConnectManhattan("sp_tree:out5", "mrr8:input",bend_radius=10,cover_bends=True),
            i3.ConnectManhattan("sp_tree:out6", "mrr7:input",bend_radius=10,cover_bends=True),
            i3.ConnectManhattan("sp_tree:out7", "mrr6:input",bend_radius=10,cover_bends=True),
            i3.ConnectManhattan("sp_tree:out8", "mrr5:input", control_points=[(240, 140)],bend_radius=10,cover_bends=True),
        ]

    def _gc_specs(self):
        return [
            # GC placement. ``vertical_in`` is the fiber-side external port;
            # ``out`` is the waveguide-side internal routing port.
            i3.Place("gc_in", (-100, 0), relative_to="sp_tree:in"),
            i3.Place("gc_out1", (1500, -400), relative_to="mrr1:drop", angle=180),
            i3.Place("gc_out2", (0, 400), relative_to="gc_out1", angle=180),
            i3.Place("gc_out3", (0, 400), relative_to="gc_out2", angle=180),
            i3.Place("gc_out4", (0, 400), relative_to="gc_out3", angle=180),
            i3.Place("gc_out5", (0, 400), relative_to="gc_out4", angle=180),
            i3.Place("gc_out6", (0, 400), relative_to="gc_out5", angle=180),
            i3.Place("gc_out7", (0, 400), relative_to="gc_out6", angle=180),
            i3.Place("gc_out8", (0, 400), relative_to="gc_out7", angle=180),

            # Optical routing.
            i3.ConnectManhattan("gc_in:out", "sp_tree:in",bend_radius=10,cover_bends=True),
            i3.ConnectManhattan("gc_out1:out", "mrr1:through",bend_radius=10,cover_bends=True),
            i3.ConnectManhattan("gc_out2:out", "mrr2:through",bend_radius=10,cover_bends=True),
            i3.ConnectManhattan("gc_out3:out", "mrr3:through",bend_radius=10,cover_bends=True),
            i3.ConnectManhattan("gc_out4:out", "mrr4:through",bend_radius=10,cover_bends=True),
            i3.ConnectManhattan("gc_out5:out", "mrr8:through",bend_radius=10,cover_bends=True),
            i3.ConnectManhattan("gc_out6:out", "mrr7:through",bend_radius=10,cover_bends=True),
            i3.ConnectManhattan("gc_out7:out", "mrr6:through",bend_radius=10,cover_bends=True),
            i3.ConnectManhattan("gc_out8:out", "mrr5:through",bend_radius=10,cover_bends=True),
        ]

    def _pad_specs(self):
        return [
            # Right-side pads.
            i3.Place("pad1", (600, 500), relative_to="mrr5:elec1"),
            i3.Place("pad2", (800, 500), relative_to="mrr5:elec1"),
            i3.Place("pad3", (1000, 500), relative_to="mrr5:elec1"),
            i3.Place("pad4", (1200, 500), relative_to="mrr5:elec1"),
            i3.Place("pad5", (600, -500), relative_to="mrr1:elec2"),
            i3.Place("pad6", (800, -500), relative_to="mrr1:elec2"),
            i3.Place("pad7", (1000, -500), relative_to="mrr1:elec2"),
            i3.Place("pad8", (1200, -500), relative_to="mrr1:elec2"),

            # Left-side pads.
            i3.Place("pad_1", (-100, 500), relative_to="mrr5:elec2"),
            i3.Place("pad_2", (-300, 500), relative_to="mrr5:elec2"),
            i3.Place("pad_3", (-500, 500), relative_to="mrr5:elec2"),
            i3.Place("pad_4", (-700, 500), relative_to="mrr5:elec2"),
            i3.Place("pad_5", (-100, -500), relative_to="mrr1:elec2"),
            i3.Place("pad_6", (-300, -500), relative_to="mrr1:elec2"),
            i3.Place("pad_7", (-500, -500), relative_to="mrr1:elec2"),
            i3.Place("pad_8", (-700, -500), relative_to="mrr1:elec2"),
        ]

    def _electrical_specs(self):
        return [
            # Right-side electrical routing.
            i3.ConnectElectrical("mrr5:elec1", "pad1:m1", start_angle=0, end_angle=90, control_points=[i3.CP((0, -50), relative_to="pad1:m1")]),
            i3.ConnectElectrical("mrr6:elec1", "pad2:m1", start_angle=0, end_angle=90, control_points=[i3.CP((0, -50), relative_to="pad2:m1")]),
            i3.ConnectElectrical("mrr7:elec1", "pad3:m1", start_angle=0, end_angle=90, control_points=[i3.CP((0, -50), relative_to="pad3:m1")]),
            i3.ConnectElectrical("mrr8:elec1", "pad4:m1", start_angle=0, end_angle=90, control_points=[i3.CP((0, -50), relative_to="pad4:m1")]),
            i3.ConnectElectrical("mrr1:elec1", "pad5:m1", start_angle=0, end_angle=90, control_points=[i3.CP((0, 50), relative_to="pad5:m1")]),
            i3.ConnectElectrical("mrr2:elec1", "pad6:m1", start_angle=0, end_angle=90, control_points=[i3.CP((0, 50), relative_to="pad6:m1")]),
            i3.ConnectElectrical("mrr3:elec1", "pad7:m1", start_angle=0, end_angle=90, control_points=[i3.CP((0, 50), relative_to="pad7:m1")]),
            i3.ConnectElectrical("mrr4:elec1", "pad8:m1", start_angle=0, end_angle=90, control_points=[i3.CP((0, 50), relative_to="pad8:m1")]),

            # Left-side electrical routing.
            i3.ConnectElectrical("mrr5:elec2", "pad_1:m1", start_angle=180, end_angle=90, control_points=[i3.CP((0, -50), relative_to="pad_1:m1")]),
            i3.ConnectElectrical("mrr6:elec2", "pad_2:m1", start_angle=180, end_angle=90, control_points=[i3.CP((0, -50), relative_to="pad_2:m1")]),
            i3.ConnectElectrical("mrr7:elec2", "pad_3:m1", start_angle=180, end_angle=90, control_points=[i3.CP((0, -50), relative_to="pad_3:m1")]),
            i3.ConnectElectrical("mrr8:elec2", "pad_4:m1", start_angle=180, end_angle=90, control_points=[i3.CP((0, -50), relative_to="pad_4:m1")]),
            i3.ConnectElectrical("mrr1:elec2", "pad_5:m1", start_angle=180, end_angle=90, control_points=[i3.CP((0, -50), relative_to="pad_5:m1")]),
            i3.ConnectElectrical("mrr2:elec2", "pad_6:m1", start_angle=180, end_angle=90, control_points=[i3.CP((0, -50), relative_to="pad_6:m1")]),
            i3.ConnectElectrical("mrr3:elec2", "pad_7:m1", start_angle=180, end_angle=90, control_points=[i3.CP((0, -50), relative_to="pad_7:m1")]),
            i3.ConnectElectrical("mrr4:elec2", "pad_8:m1", start_angle=180, end_angle=90, control_points=[i3.CP((0, -50), relative_to="pad_8:m1")]),
        ]

    def _default_exposed_ports(self):
        """Expose fiber-side GC ports and electrical pad ports."""
        exposed_ports = {
            "gc_in:vertical_in": "opt_in",
        }

        for idx in range(1, 9):
            exposed_ports[f"gc_out{idx}:vertical_in"] = f"opt_out{idx}"
            exposed_ports[f"pad{idx}:m1"] = f"elec_pad{idx}"
            exposed_ports[f"pad_{idx}:m1"] = f"elec_pad_{idx}"
            exposed_ports[f"mrr{idx}:drop"] = f"mrr{idx}_drop"
            exposed_ports[f"mrr{idx}:add"] = f"mrr{idx}_add"

        return exposed_ports


if __name__ == "__main__":
    circuit = MRRArrayCircuit()
    circuit_layout = circuit.Layout()
    # circuit_layout.visualize(annotate=True)

    print("Top-level ports:")
    for port in circuit_layout.ports:
        print(port.name, port.position)
    ROOT = Path(__file__).resolve().parents[4]
    PORT_DIR = ROOT / "tape_out" / "port"
    PORT_DIR.mkdir(parents=True, exist_ok=True)
    with open(ROOT/"MrrAarry.csv", "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["Port", "X(um)", "Y(um)"])

            for port in circuit_layout.ports:
                    x, y = port.position
                    writer.writerow([port.name, x, y])
    elements = i3.stub_acute_angles(circuit_layout, stub_width=2, angle_threshold=0.01, grow_amount=0.02)
    circuit_final=i3.LayoutCell().Layout(elements=elements)
    circuit_final.visualize()




    # Optional GDS export.
    # circuit_layout.write_gdsii("mrr_array_circuit.gds")

    # Optional circuit simulation.
    circuit_model = circuit.CircuitModel()
    wavelengths = np.linspace(1.5, 1.6, 501)
    circuit_model.get_smatrix(wavelengths=wavelengths).visualize()
