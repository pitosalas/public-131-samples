from diag.diag import Colors, Diagram
from lib.mm_base import MemoryManager
from lib.pagetables import PCB
from lib.pm_paged import PagedPhysMem
from lib.reporter import Reporter


class PagedMm(MemoryManager):
    def __init__(self, memory_param: dict) -> None:
        super().__init__(memory_param)
        self.physical_memory = PagedPhysMem(memory_param)
        self.pcbs: dict[str, PCB] = {}

    def launch(self, process, size):
        size *= eval(self.memory_param["default_multiplier"])
        mapping = self.physical_memory.launch(process, size)
        if mapping is None:
            raise ValueError(f"Allocation request {size} for process {process} failed")
        self.pcbs[process] = PCB(process, mapping)

    def terminate(self, process: str):
        allocation = self.pcbs[process]
        if allocation is None:
            raise ValueError("process not found")
        self.physical_memory.deallocate(allocation.mapping)
        del self.pcbs[process]

    def __str__(self) -> str:
        return "Paged Memory Manager"


    def report(self, rep: Reporter):
        rep.add_allocations(self.pcbs)
        self.physical_memory.report(rep)

    def allocate(self, process: str, size: int):
        pass

    def graph(self, dg: Diagram):
        colors = Colors("p2")
        # Create the box which will be Physical Memory.
        phys = dg.add_box("Physical Memory", "physmem")
        for id, entry in enumerate(self.physical_memory.frame_table):
            color = "bisque2" if (id % 2) == 0 else "gainsboro"
            entrylabel = f"""frame {id}""" if entry is not None else "FREE"
            phys.add_section_to_box(f"""{id}""", entry, entrylabel, color, 30)
        t1 = dg.add_tier("left", rank="sink")
        dg.render_box(phys, t1)

        # Now create boxes for each process' page table
        t2 = dg.add_tier("right", rank="source")
        for process, allocation in self.pcbs.items():
            rotated_color = colors.rotate()
            box = dg.add_box(process, process)
            for id, frame in enumerate(allocation.mapping.table):
                box.add_section_to_box(
                    f"{id}", f"frame: {frame}", f"page: {id}", color, 30
                )
                dg.add_edge(f"{process}:{id}", f"physmem:{frame}", rotated_color)
            dg.render_box(box, t2)
