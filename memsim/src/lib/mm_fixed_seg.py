from diag.diag import Diagram
from lib.mm_base import MemoryManager
from lib.pagetables import PCB
from lib.reporter import Reporter
from lib.utils import pretty_mem_str
from lib.pm_fixed_seg import FixedSegPhysMem


class FixedSegMm(MemoryManager):
    """Keeps track of each Job that it has given memory to in the dict allocations. The key is the name of the job and the value is a MemoryAllocation object."""

    def __init__(self, memory_param: dict) -> None:
        super().__init__(memory_param)
        self.physical_memory = FixedSegPhysMem(memory_param)
        self.allocations: dict[str, PCB] = {}

    def launch(self, process: str, size: int):
        size *= eval(self.memory_param["default_multiplier"])
        mapping = self.physical_memory.allocate(process, size)
        if mapping is None:
            raise ValueError(f"Launch request {size} for process {process} failed")
        self.allocations[process] = PCB(process, mapping)
        
    def allocate(self, process: str, size: int):
        raise ValueError("FixedSegMm does not support allocate")

    def deallocate(self, process: str):
        raise ValueError("FixedSegMm does not support deallocate")

    def terminate(self, process: str):
        allocation = self.allocations[process]
        if allocation is None:
            raise ValueError("process not found")
        self.physical_memory.deallocate(allocation.mapping)
        del self.allocations[process]

    def report(self, rep: Reporter):
        rep.add_allocations(self.allocations)
        self.physical_memory.report(rep)

    def merge_all_blocks(self):
        blocks = []
        for segnum, seg in enumerate(self.physical_memory.seg_table):
            if seg is None:
                blocks.append({'label': "FREE", 'start': self.physical_memory.segsize * segnum, 'size': self.physical_memory.segsize})
            else:
                blocks.append({'label': seg,'start': self.physical_memory.segsize * segnum, 'size': self.physical_memory.segsize})
        return sorted(blocks,key=lambda x: x["start"])


    def graph(self, dg: Diagram):
        box = dg.add_box("Physical Memory", "physmem")
        blocks = self.merge_all_blocks()
        for entry in blocks:
            sublabel = f"""start: {pretty_mem_str(entry["start"])}, size: {pretty_mem_str(entry["size"])}"""
            color = "bisque2" if entry["label"]=="FREE" else "gainsboro"
            box.add_section_to_box(entry["label"],entry["label"],sublabel, color, entry["size"]/2000)
        t1 = dg.add_tier("left", rank="sink")
        dg.render_box(box, t1)

    def __str__(self) -> str:
        phys_memory = str(self.physical_memory)
        allocations = "\n         ".join(
            str(alloc) for alloc in self.allocations.values()
        )
        return f"Fixed Segment Memory Manager:\n   Processes:\n         .{allocations}\n   +{phys_memory}"

