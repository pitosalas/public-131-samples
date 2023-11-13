import random
import graphviz

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


    def generate(self):
        self.left_ones.attr(rank="source")
        self.right_ones.attr(rank="sink")
        self.dot.subgraph(self.right_ones)
        self.dot.subgraph(self.left_ones)
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
        # for frame in page_table.table:
        #     label_string += f"<{frame}>{frame}|"
        #     self.dot.edge(f"{process}:{frame}", f"frame:{frame}", color=str(color))
        last_bar = label_string.rfind("|")
        subgraph.node(process, label=label_string[0:last_bar])
