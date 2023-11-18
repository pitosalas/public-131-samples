import random
import graphviz

class Box:
    def __init__(self, handle: str, dot: graphviz.Digraph):
        self.handle = handle
        self.dot = dot
        self.sections = []

    def add_section_to_box(self, label: str):
        self.sections.append(label)

class Dotgen:
    def __init__(self, filename):
        self.filename = filename
        self.paged_mem_string = ""
        self.dot = graphviz.Digraph(comment='Memsim')
        self.dot.attr('graph', rankdir="RL", ranksep="1.5")
        self.dot.attr('node', shape="record", height="0.2", width="0.4", margin="0.02 0.02", fontsize="8")
        self.dot.attr('edge', arrowsize="0.4")
        self.procces_string = ""
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

    def add_box(self, handle: str):
        self.boxes[handle] = Box(handle, self.dot)
        return self.boxes[handle]
    
    def render_box(self, box):
        label = ""
        for section in box.sections:
            label += f"{section}|"
        last_bar = label.rfind("|")
        label = label[0:last_bar]
        self.dot.node(box.handle, label=label)

	# graph [rankdir=RL ranksep=1.5, label="Physical Memory\nFixed Segment Memory Manager\n\n", labelloc="t", labeljust="c", fontsize=14, fontcolor="blue"]
