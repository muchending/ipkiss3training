import ipkiss3.all as i3
import numpy as np
from si_fab import all as pdk



class heatedringwaveguide(pdk.HeatedWaveguide):
    metal_angle_separation = i3.NumberProperty(default=180,
                                                doc="Angular separation between two metal contacts in degrees.")
    heater_width = i3.NumberProperty(default=0.8,)
    heater_offset = i3.NumberProperty(default=1.4,)
    class Layout(pdk.HeatedWaveguide.Layout):
        def _point_at_length(self, shape, target_length):
            pts = list(shape)

            if target_length <= 0:
                return pts[0]

            acc_len = 0.0

            for p0, p1 in zip(pts[:-1], pts[1:]):
                x0, y0 = p0
                x1, y1 = p1

                seg_len = np.sqrt((x1 - x0) ** 2 + (y1 - y0) ** 2)

                if acc_len + seg_len >= target_length:
                    ratio = (target_length - acc_len) / seg_len
                    return (
                        x0 + ratio * (x1 - x0),
                        y0 + ratio * (y1 - y0),
                    )

                acc_len += seg_len

            return pts[-1]


        def _generate_elements(self, elems):
            metal_angle_separation=self.metal_angle_separation
            elems=super(pdk.HeatedWaveguide.Layout,self)._generate_elements(elems)

            metal_angle_separation = self.cell.metal_angle_separation

            heater_hw=self.heater_width/2.0
            heater_offset=self.cell.heater_offset
            m1_hw=heater_hw+heater_offset+self.cell.m1_extension

            center_line=self.center_line_shape
            total_length=center_line.length()
            heater_windows = [
                i3.PathTraceWindow(
                    start_offset=i * heater_offset - heater_hw,
                    end_offset=i * heater_offset + heater_hw,
                    layer=i3.TECH.PPLAYER.HT,
                )
                for i in [-1, 1]
            ]

            for h in heater_windows:
                elems += h.get_elements_from_shape(shape=center_line)




            separation_fraction=self.metal_angle_separation/360
            start1 = 0.0
            end1 = total_length - self.cell.m1_length
            center2 = total_length * separation_fraction
            start2 = center2 - self.cell.m1_length / 2.0
            end2 = total_length - center2 - self.cell.m1_length / 2.0

            endpoints_shapes = [
                i3.ShapeShorten(
                    original_shape=center_line,
                    trim_lengths=(start1, end1),
                ),
                i3.ShapeShorten(
                    original_shape=center_line,
                    trim_lengths=(start2, end2),
                ),
            ]
            m_windows = [
                i3.PathTraceWindow(
                    start_offset=-m1_hw,
                    end_offset=m1_hw,
                    layer=i3.TECH.PPLAYER.M1,
                ),
            ]

            for w in m_windows:
                for s in endpoints_shapes:
                    elems += w.get_elements_from_shape(shape=s)

            return elems

        def _generate_ports(self, ports):
            # ports = super()._generate_ports(ports)

            center_line = self.center_line_shape
            total_length = center_line.length()

            separation_fraction = self.cell.metal_angle_separation / 360.0

            pos1 = self._point_at_length(
                center_line,
                self.cell.m1_length / 2.0
            )

            pos2 = self._point_at_length(
                center_line,
                total_length * separation_fraction
            )

            ports += i3.ElectricalPort(
                name="elec1",
                position=pos1,
                layer=i3.TECH.PPLAYER.M1,
                trace_template=pdk.M1WireTemplate(),
            )

            ports += i3.ElectricalPort(
                name="elec2",
                position=pos2,
                layer=i3.TECH.PPLAYER.M1,
                trace_template=pdk.M1WireTemplate(),
            )

            return ports


