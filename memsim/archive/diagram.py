import random
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

    def add_section_to_box(self, label: str, sub: str, height: int = 10):
        self.sections.append({"label": label, "sublabel": sub, "height": height})

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
    def __init__(self, filename):
        self.filename = filename
        self.paged_mem_string = ""
        self.dot = graphviz.Digraph(name="memory")
        self.dot.attr('graph', rankdir="RL", ranksep="1.5")
        self.dot.attr('node', shape="none", height="0.2", width="0.4", margin="0.02 0.02", fontsize="12")
        self.dot.attr('edge', arrowsize="0.4")
        self.left_ones = graphviz.Digraph(name="left_ones")
        self.right_ones = graphviz.Digraph(name="right_ones")
        self.boxes = {}
        self.tiers = {}

    def generate(self):
        # self.left_ones.attr(rank="source")
        # self.right_ones.attr(rank="sink")
        # self.dot.subgraph(self.right_ones)
        # self.dot.subgraph(self.left_ones)
        self.dot.view()

    def generate_diagram(self):
        for tier in self.tiers.values():
            tier.digraph.attr(rank=tier.rank)
            self.dot.subgraph(tier.digraph)

        # self.left_ones.attr(rank="source")
        # self.right_ones.attr(rank="sink")
        # self.dot.subgraph(self.right_ones)
        # self.dot.subgraph(self.left_ones)
        self.dot.view()


    def paged_mem_complete(self):
        last_bar = self.paged_mem_string.rfind("|")
        self.dot.node("frame", label=self.paged_mem_string[0:last_bar])

    def paged_mem_frame(self, frame_num: int, label: str):
        self.paged_mem_string += f"<{frame_num}>{label}|"

    def add_process(self, process, page_table):
        label_string = ""
        color = random.choice(["red", "blue", "green", "orange", "purple"])
        subgraph = random.choice([self.left_ones, self.right_ones])
        for frame in page_table.table:
            label_string += f"<{frame}>{frame}|"
            self.dot.edge(f"{process}:{frame}", f"frame:{frame}", color=str(color))
        last_bar = label_string.rfind("|")
        subgraph.node(process, label=label_string[0:last_bar])

    def add_box(self, label: str, handle: str):
        self.boxes[handle] = Box(label, handle, self.dot)
        return self.boxes[handle]
    
    def render_box(self, box, tier: Tier =None):
        label_start = f"""<<table border="0.1" cellborder="1" cellspacing="0"><TR><TD sides="b"><B><font color="blue">{box.label}</font></B></TD></TR>"""
        label_end = """</table>>"""
        label = label_start
        for section in box.sections:
            label += f"""<tr><td align="text" height="{section["height"]}" width="60" port="{section["label"]}">"""
            label += f"""<font point-size="{BOX_FONTSIZE}">{section["label"]}</font><br></br><font point-size="{SUB_LABEL_FONTSIZE}">{section["sublabel"]}</font></td></tr>"""
        label += label_end
        rank="sink"
        if tier is None:
            subgraph = self.dot
            print("tier is none")
        else:
            subgraph = tier.digraph
        subgraph.node(box.handle, label=label, rank=rank)

    def add_edge(self, src: str, dest: str, color: str ="black"):
        self.dot.edge(src, dest, color=color)

    def add_tier(self, name: str, rank: str = "same"):
        self.tiers[name] = Tier(name, self.dot, rank)
        return self.tiers[name]

    
