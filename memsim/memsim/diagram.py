import random
import graphviz

class Box:
    def __init__(self, label: str, handle: str, dot: graphviz.Digraph):
        self.handle = handle
        self.label = label
        self.dot = dot
        self.sections = []

    def add_section_to_box(self, label: str, height: int = 1):
        self.sections.append({"label": label, "height": height})

class Diagram:
    def __init__(self, filename):
        self.filename = filename
        self.paged_mem_string = ""
        self.dot = graphviz.Digraph(name="memory")
        self.dot.attr('graph', rankdir="RL", ranksep="1.5")
        self.dot.attr('node', shape="none", height="0.2", width="0.4", margin="0.02 0.02", fontsize="8")
        self.dot.attr('edge', arrowsize="0.4")
        self.left_ones = graphviz.Digraph(name="left_ones")
        self.right_ones = graphviz.Digraph(name="right_ones")
        self.boxes = {}

    def generate(self):
        # self.left_ones.attr(rank="source")
        # self.right_ones.attr(rank="sink")
        # self.dot.subgraph(self.right_ones)
        # self.dot.subgraph(self.left_ones)
        self.render_box(self.boxes["physmem"])
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
    
    def render_box(self, box):
        label_start = f"""<<table border="0.1" cellborder="1" cellspacing="0"><TR><TD sides="b"><B><font color="blue">{box.label}</font></B></TD></TR>"""
        element_end = """</td></tr>"""
        label_end = """</table>>"""
        label = label_start
        for section in box.sections:
            label += f"""<tr><td align="left" height="{section["height"]}" width="60">"""
            label += section["label"]+element_end
        label += label_end
        self.dot.node(box.handle, label=label)
