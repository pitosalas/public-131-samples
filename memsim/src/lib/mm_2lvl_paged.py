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
            raise ValueError(f"Allocation request {size} for process {process} failed")
        self.pcbs[process] = PCB(process, mapping)

    def terminate(self, process: str):
        allocation = self.pcbs[process]
        if allocation is None:
            raise ValueError("process not found")
        self.physical_memory.deallocate(process)
        del self.pcbs[process]

    # Allocate a block of memory at a location
    def allocate(self, process: str, address: int):
        allocation = self.pcbs[process]
        if allocation is None:
            raise ValueError("process not found")
        self.physical_memory.allocate(process, address)

    def __str__(self) -> str:
        return "SparsePagedMm"

    def report(self, rep: Reporter):
        rep.add_allocations(self.pcbs)
        self.physical_memory.report(rep)

    def graph(self, dg: Diagram):
        pass
