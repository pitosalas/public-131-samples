import graphviz

BOX_FONTSIZE = "12"
LABEL_FONTSIZE = "11"
SUB_LABEL_FONTSIZE = "8"


class Box:
    def __init__(self, label: str, handle: str, dot: graphviz.Digraph):
        self.handle = handle
        self.label = label
        self.dot = dot
        self.sections = []

    def add_section_to_box(self, ident: str, label: str, sub: str, color: str, height: int = 10):
        self.sections.append({"ident": ident, "label": label, "sublabel": sub, "height": height, "color": color})

    def __str__(self):
        return f"Box: {self.label}  {self.handle}  {self.sections}"

class Tier:
    def __init__(self, label: str, dot: graphviz.Digraph, rank: str):
        self.label = label
        self.dot = dot
        self.boxes = []
        self.rank = rank
        self.digraph = graphviz.Digraph(name=label)

    def add_box_to_tier(self, box: Box):
        self.boxes.append(box)

class Diagram:
    def __init__(self, name: str, rankdir: str = "RL"):
        self.name = name
        self.dot = graphviz.Digraph(name=name)
        self.dot.attr('graph', rankdir="RL", ranksep="1.0", fontname="x")
        self.dot.attr('node', shape="none", height="0.2", width="0.4", margin="0.04 0.04", fontsize="10", fontname="Helvetica")
        self.dot.attr('edge', arrowsize="0.4")
        self.boxes = {}
        self.tiers = {}

    def add_edge(self, src: str, dest: str, color: str ="black"):
        self.dot.edge(src, dest, color=color)

    def add_tier(self, name: str, rank: str = "same"):
        self.tiers[name] = Tier(name, self.dot, rank)
        return self.tiers[name]    

    def generate_diagram(self):
        for tier in self.tiers.values():
            tier.digraph.attr(rank=tier.rank)
            self.dot.subgraph(tier.digraph)
        self.dot.render(outfile=f"{self.name}.pdf")

    def add_box(self, label: str, handle: str):
        self.boxes[handle] = Box(label, handle, self.dot)
        return self.boxes[handle]
    
    def render_box(self, box, tier: Tier =None):
        label_start = f"""<<table border="0.1" cellborder="1" cellspacing="0"><TR><TD sides="b"><font face="helvetica" color="grey15" point-size="12">{box.label}</font></TD></TR>"""
        label_end = """</table>>"""
        label = label_start
        for section in box.sections:
            label += f"""<tr><td align="text" color="grey" bgcolor="{section["color"]}" height="{section["height"]}" width="60" port="{section["ident"]}">"""
            label += f"""<font point-size="{BOX_FONTSIZE}">{section["label"]}</font><br></br><font point-size="{SUB_LABEL_FONTSIZE}">{section["sublabel"]}</font></td></tr>"""
        label += label_end
        subgraph = tier.digraph
        subgraph.node(box.handle, label=label)

