from diag.diag import Colors, Diagram
from lib.mm_base import MemoryManager
from lib.pm_paged import PagedPm
from lib.reporter import Reporter
from lib.pagetables import PCB, TwoLevelPageTable


class TwoLvlPagedMm(MemoryManager):
    def __init__(self, memory_param: dict) -> None:
        super().__init__(memory_param)
        self.physical_memory = PagedPm(memory_param)
        self.pcbs: dict[str, PCB] = {}

    def launch(self, process, entires_per_page_table):
        mapping = TwoLevelPageTable(
            process, self.physical_memory, entires_per_page_table
        )
        if mapping is None:
            raise ValueError(
                f"Allocation request for page table for process {process} failed"
            )
        self.pcbs[process] = PCB(process, mapping)

    def terminate(self, process: str):
        allocation = self.pcbs[process]
        if allocation is None:
            raise ValueError("process not found")
        self.physical_memory.deallocate(process)
        del self.pcbs[process]

    # Allocate a block of memory at a location
    def allocate(self, process: str, size: int):
        allocation = self.pcbs[process]
        if allocation is None:
            raise ValueError("process not found")
        allocation.mapping.allocate(size)

    def __str__(self) -> str:
        return "SparsePagedMm"

    def report(self, rep: Reporter):
        rep.add_allocations(self.pcbs)
        self.physical_memory.report(rep)

    def graph(self, dg: Diagram):
        self.c_outer = Colors("p2")
        self.c_inner = Colors("p1")
        self.left = dg.add_tier("left", rank="source")
        self.middle = dg.add_tier("middle", rank="middle")
        self.right = dg.add_tier("left", rank="source")

        # Create the box which will be Physical Memory.
        phys = dg.add_box("Physical Memory", "physmem")
        for id, entry in enumerate(self.physical_memory.frame_table):
            color = "bisque2" if (id % 2) == 0 else "gainsboro"
            entrylabel = f"""frame {id}""" if entry is not None else "FREE"
            phys.add_section_to_box(f"""{id}""", entry, entrylabel, color, 30)
        dg.render_box_in_tier(self.left, phys)

        # Now create boxes for each process' Page Tables
        for process, allocation in self.pcbs.items():
            rotated__outer_color = self.c_outer.rotate()
            c_inner = Colors("p1")
            box = dg.add_box(process, f"outer-{process}")
            for id, frame in enumerate(allocation.mapping.table):
                inner_color = c_inner.rotate()
                # outer pt from process
                if frame is None:
                    box.add_section_to_box(f"{id}", "outer pt entry", f"{id}", color, 30)
                else:
                    box.add_section_to_box(f"{id}", "outer pt entry", f"{id}", color, 30)
                    box_inner = dg.add_box(f"inner-{process}-{id}", f"inner-{process}-{id}")
                    for id_inner, inner_frame in enumerate(frame):
                        # inner pt for outer pt slot id
                        if inner_frame is None:
                            box_inner.add_section_to_box(
                                f"{id_inner}", "inner pt entry", f"{id_inner}", color, 30
                            )
                        else:
                            box_inner.add_section_to_box(
                                f"{id_inner}", "inner pt entry", f"{id_inner}", color, 30
                            )
                            dg.add_edge(f"inner-{process}-{id}:{id_inner}", f"physmem:{inner_frame}", inner_color)
                    dg.add_edge(f"outer-{process}:{id}", f"inner-{process}-{id}:0", rotated__outer_color)
                    dg.render_box_in_tier(self.middle, box_inner)
            dg.render_box_in_tier(self.right, box)
