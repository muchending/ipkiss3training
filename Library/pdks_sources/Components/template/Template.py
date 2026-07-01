from si_fab import all as pdk
from ipkiss3 import all as i3
class Template(i3.PCell):
    template_width = i3.PositiveNumberProperty(default=2500.0, doc="width of the template")
    template_height = i3.PositiveNumberProperty(default=1250.0, doc="height of the template")
    edge_width = i3.PositiveNumberProperty(default=2.0)

    def _default_name(self):
        return "TEMPLATE"

    class Layout(i3.LayoutView):
        def generate(self, layout):
            shape = i3.ShapeRectangle(
                center=(self.template_width / 2.0, self.template_height / 2.0),
                box_size=(self.template_width - self.edge_width, self.template_height - self.edge_width),
            )
            layout += i3.Path(shape=shape, layer=i3.TECH.PPLAYER.DOC, line_width=self.edge_width)
            return layout
if __name__ == "__main__":
    template = Template()
    template.Layout().visualize()