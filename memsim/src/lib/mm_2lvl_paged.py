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
        self.physical = dg.add_tier("physical", rank="source")
        self.inner = dg.add_tier("inner", rank="middle")
        self.outer = dg.add_tier("outer", rank="sink")
        self.dg = dg
        self.create_box_for_physical_memory()
        self.create_box_for_outer_pt()

    def create_box_for_physical_memory(self):
        # Create the box which will be Physical Memory.
        phys = self.dg.add_box("Physical Memory", "physmem")
        for id, entry in enumerate(self.physical_memory.frame_table):
            color = "bisque2" if (id % 2) == 0 else "gainsboro"
            entrylabel = f"""physical frame {id}""" if entry is not None else "FREE"
            phys.add_section_to_box(f"""{id}""", entry, entrylabel, color, 30)
        self.dg.render_box_in_tier(self.physical, phys)

    def create_box_for_outer_pt(self):
        color_palette = Colors("p5")
        c1 = color_palette.random_color()
        c2 = color_palette.alternate(c1, 50)
        for process, allocation in self.pcbs.items():
            box = self.dg.add_box(process, f"outer_{process}")
            for id, frame in enumerate(allocation.mapping.table):
                # outer pt from process
                if frame is None:
                    box.add_section_to_box(f"{id}", "empty", f"pt slot {id}", c1, 30)
                else:
                    box.add_section_to_box(
                        f"{id}", "to inner pt", f"pt slot {id}", c2, 30
                    )
                    self.create_box_for_inner_pt(process, id, frame)
            self.dg.render_box_in_tier(self.outer, box)

    def create_box_for_inner_pt(self, process, id, frame):
        color_palette = Colors("p5")
        c1 = color_palette.random_color()
        c2 = color_palette.alternate(c1, 50)
        box_inner = self.dg.add_box(f"inner_{process}_{id}", f"inner_{process}_{id}")
        for id_inner, inner_frame in enumerate(frame):
            # inner pt for outer pt slot id
            if inner_frame is None:
                box_inner.add_section_to_box(
                    f"{id_inner}",
                    "unused",
                    f"{id_inner}",
                    c1,
                    30,
                )
            else:
                box_inner.add_section_to_box(
                    f"{id_inner}", "to physical", f"pt slot: {id_inner}", c2, 30
                )
                self.dg.add_edge(
                    f"inner_{process}_{id}:{id_inner}",
                    f"physmem:{inner_frame}",
                    "orange",
                )
        self.dg.add_edge(f"outer_{process}:{id}", f"inner_{process}_{id}:0", "orange")
        self.dg.render_box_in_tier(self.inner, box_inner)
