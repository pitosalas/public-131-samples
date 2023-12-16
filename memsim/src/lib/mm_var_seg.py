from diag.diag import Diagram
from lib.mm_base import MemoryManager
from lib.pagetables import PCB
from lib.pm_var_seg import VarSegPhysMem
from lib.reporter import Reporter
from lib.utils import pretty_mem_str


class VarSegMm(MemoryManager):
    def __init__(self, memory_param) -> None:
        super().__init__(memory_param)
        self.physical_memory = VarSegPhysMem(memory_param)
        self.allocations: dict[str, PCB] = {}

# the size parameter is not used for variable segment memory
    def launch(self, process: str, size: int):
        size *= eval(self.memory_param["default_multiplier"])
        block = self.physical_memory.allocate(size)
        if block is None:
            raise ValueError("not enough memory")
        self.allocations[process] = PCB(process, block)        

    def allocate(self, process: str, size: int):
        raise ValueError("allocate not valid for variable segment memory. Use Launch")
    
    def deallocate(self, process: str):
        raise ValueError("deallocate not valid for variable segment memory. Use Terminate")

    def terminate(self, process):
        allocation = self.allocations[process]
        if allocation is None:
            raise "process not found"
        self.physical_memory.deallocate(allocation.mapping)
        del self.allocations[process]

    def __str__(self) -> str:
        phys_memory = str(self.physical_memory)
        allocations = "\n         ".join(
            str(alloc) for alloc in self.allocations.values()
        )
        freeblocks = "\n         ".join(
            str(block) for block in self.physical_memory.freelist
        )
        return f"Variable Segment Memory Manager:\n   Processes:\n         {allocations}\n   {phys_memory}\n   Free Blocks:\n         {freeblocks}"

    def report(self, rep: Reporter):
        rep.add_allocations(self.allocations)
        self.physical_memory.report(rep)

    def merge_all_blocks(self):
        # sourcery skip: for-append-to-extend, list-comprehension
        blocks = []
        for block in self.physical_memory.freelist:
            blocks.append({'label': "FREE", 'start': block.physical_address, 'size': block.size})
        for allocation in self.allocations.values():
            blocks.append({'label': allocation.process, 'start': allocation.mapping.physical_address, 'size': allocation.mapping.size})
        return sorted(blocks,key=lambda x: x["start"])


    def graph(self, dg: Diagram):
        box = dg.add_box("Physical Memory", "physmem", 150)
        blocks = self.merge_all_blocks()
        for entry in blocks:
            sublabel = f"""start: {pretty_mem_str(entry["start"])}, size: {pretty_mem_str(entry["size"])}"""
            color = "bisque2" if entry["label"]=="FREE" else "gainsboro"
            box.add_section_to_box(entry["label"], entry["label"],sublabel, color, int(entry["size"]/1000))
        t1 = dg.add_tier("left", rank="sink")
        dg.render_box(box, t1)