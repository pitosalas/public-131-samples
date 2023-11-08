
import graphviz

class Dotgen:
    def __init__(self, filename):
        self.filename = filename
        self.paged_mem_string = ""
        self.dot = graphviz.Digraph(comment='Memsim')
        self.dot.attr('graph', rankdir="RL")
        self.dot.attr('node', shape="record")
        self.procces_string = ""

    def generate(self):
        self.dot.view()

    def paged_mem_complete(self):
        self.dot.node("paged_mem", label=self.paged_mem_string)

    def paged_mem_frame(self, frame_num: int, label: str):
        self.paged_mem_string += f"<paged_mem{frame_num}>{label}|"

    def add_process(self, process, page_table):
        label_string = ""
        for frame in page_table.table:
            label_string += f"<{process}{frame}>{frame}|"
            self.dot.edge(f"{process}:{frame}", f"paged_mem:{frame}")
        self.dot.node("process", label=label_string)
