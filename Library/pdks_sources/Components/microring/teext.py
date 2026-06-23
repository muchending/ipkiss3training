
import si_fab.all as pdk

from ipkiss3 import all as i3
from Components import all as my_pdks

# # 最简单的加热波导
# ht = pdk.HeatedWaveguide(
#     heater_width=0.6,
#     heater_offset=1.0,
# )
#
# heated_ring=pdk.HeatedWaveguide(heater_width=1,
#                                             heater_offset=1,
#                                             )
# ring_shape=i3.ShapeArc(
#                     radius=20,
#                     start_angle=0,
#                     end_angle=360,
#                     center=(0.5 * 1, 20 + 0.5 + 0.5 * 0.5))
# heated_ring_layout=heated_ring.Layout(shape=ring_shape)
# # ht_lv = ht.Layout(shape=[(0.0, 0.0), (10.0, 0.0)])
# # ht_lv.visualize(annotate=True)
# heated_ring_layout.visualize()
# # # 查看横截面
# # xs = ht_lv.cross_section(cross_section_path=i3.Shape([(1.0, -8.0), (1.0, 8.0)]))
# # xs.visualize()

# 导入你刚定义的子类

lv=my_pdks.heatedringwaveguide()
lv_layout=lv.Layout(shape=i3.ShapeArc(
                    radius=1,
                    start_angle=0,
                    end_angle=360,
                    center=(0,0),
                ))

# lv_layout.visualize()
nt=lv.Netlist()
print(nt.netlist)



