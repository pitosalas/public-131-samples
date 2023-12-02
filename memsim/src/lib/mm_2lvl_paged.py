from diag.diag import Diagram
from lib.mm_base import MemoryManager
from lib.pm_2lvl_paged import TwoLevelPagedPm
from lib.reporter import Reporter
from lib.pagetables import PCB


class TwoLvlPagedMm(MemoryManager):
    def __init__(self, memory_param: dict) -> None:
        super().__init__(memory_param)
        # self.default_multiplier = eval(memory_param["default_multiplier"])
        # self.page_table_size = memory_param["algo"]["page_size"]
        self.physical_memory = TwoLevelPagedPm(memory_param)
        self.pcbs: dict[str, PCB] = {}

    def launch(self, process, size):
        # allocate a new process and its sparse page table of a fixed size
        # Fixed size is part of the launching of the process.
        mapping = self.physical_memory.launch(process, size)
        if mapping is None:
            raise Exception(f"Allocation request {size} for process {process} failed")
        self.pcbs[process] = PCB(process, mapping)

    def terminate(self, process: str):
        allocation = self.pcbs[process]
        if allocation is None:
            raise Exception("process not found")
        self.physical_memory.deallocate(allocation.mapping)
        del self.pcbs[process]

    def __str__(self) -> str:
        return "SparsePagedMm"
        pass

    def report(self, rep: Reporter):
        rep.add_allocations(self.pcbs)
        self.physical_memory.report(rep)

    def allocate(self, process: str, size: int):
        pass

    def graph(self, dg: Diagram):
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
            box = dg.add_box(process, process)
            color = "grey15"
            edgecolor = "grey15"
            for id, frame in enumerate(allocation.mapping.table):
                box.add_section_to_box(
                    f"{id}", f"frame: {frame}", f"page: {id}", color, 30
                )
                dg.add_edge(f"{process}:{id}", f"physmem:{frame}", edgecolor)
            dg.render_box(box, t2)

