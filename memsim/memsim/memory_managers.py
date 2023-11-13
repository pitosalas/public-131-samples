from abc import ABC, abstractmethod
from physical_memory import FixedSegPhysMem, PagedPhysMem, VarSegPhysMem
from reporter import Reporter
from utils import PCB


class MemoryManager(ABC):
    """Keeps track of each Job that it has given memory to in the dict allocations. The key is the name of the job and the value is a MemoryAllocation object."""

    @abstractmethod
    def __init__(self, memory_param: dict):
        pass

    @abstractmethod
    def allocate(self, process: str, size: int):
        pass

    @abstractmethod
    def deallocate(self, process: int):
        pass

    @abstractmethod
    def load(self, process: str, size: int):
        pass

    @abstractmethod
    def __str__(self) -> str:
        pass

    @abstractmethod
    def report(self, rep: Reporter):
        pass

class VarSegMm(MemoryManager):
    def __init__(self, memory_param) -> None:
        super().__init__(memory_param)
        self.physical_memory = VarSegPhysMem(memory_param)
        self.allocations: dict[str, PCB] = {}

    def allocate(self, process: str, size: int):
        block = self.physical_memory.allocate(size)
        if block is None:
            raise Exception("Allocation failed to find space")
        self.allocations[process] = PCB(process, block)

    def load(self, process: str, size: int):
        self.allocate(process, size)

    # Process accesses a certain address
    def touch(self, process: str, address: int):
        allocation = self.allocations[process]
        if allocation is None:
            raise Exception("process not found")
        if not allocation.mapping.contains(address):
            raise Exception("address not found")
        self.physical_memory.touch(allocation.mapping, address)
        

    def deallocate(self, process):
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


class FixedSegMm(MemoryManager):
    """Keeps track of each Job that it has given memory to in the dict allocations. The key is the name of the job and the value is a MemoryAllocation object.
    """

    def __init__(self, memory_param) -> None:
        super().__init__(memory_param)
        self.physical_memory = FixedSegPhysMem(memory_param)
        self.allocations: dict[str, PCB] = {}

    def allocate(self, process: str, size: int):
        mapping = self.physical_memory.allocate(size)
        if mapping is None:
            raise Exception(f"Allocation request {size} for process {process} failed")
        self.allocations[process] = PCB(process, mapping)

    def touch(self, process: str, address: int) -> bool:
        allocation = self.allocations[process]
        if allocation is None:
            raise Exception("process not found")
        if not allocation.mapping.contains(address):
            raise Exception("address not found")
        return(self.physical_memory.touch(allocation.mapping, address))

    def load(self, process: str, size: int):
        self.allocate(process, size)

    def deallocate(self, process: str):
        allocation = self.allocations[process]
        if allocation is None:
            raise Exception("process not found")
        self.physical_memory.deallocate(allocation.mapping)
        del self.allocations[process]

    def report(self, rep: Reporter):
        rep.add_allocations(self.allocations)
        self.physical_memory.report(rep)

    def __str__(self) -> str:
        phys_memory = str(self.physical_memory)
        allocations = "\n         ".join(
            str(alloc) for alloc in self.allocations.values()
        )
        return f"Fixed Segment Memory Manager:\n   Processes:\n         .{allocations}\n   +{phys_memory}"


class PagedMm(MemoryManager):
    def __init__(self, memory_param: dict) -> None:
        super().__init__(memory_param)
        self.default_multiplier = eval(memory_param["default_multiplier"])
        self.physical_memory = PagedPhysMem(
            memory_param, memory_param["algo"]["page_size"]
        )
        self.allocations: dict[str, PCB] = {}

    def allocate(self, process, size):
        mapping = self.physical_memory.allocate(
            process, int(size)
        )
        if mapping is None:
            raise Exception(f"Allocation request {size} for process {process} failed")
        self.allocations[process] = PCB(process, mapping)

    def deallocate(self, process: str):
        allocation = self.allocations[process]
        if allocation is None:
            raise Exception("process not found")
        self.physical_memory.deallocate(allocation.mapping)
        del self.allocations[process]

    def __str__(self) -> str:
        pass

    def report(self, rep: Reporter):
        rep.add_allocations(self.allocations)
        self.physical_memory.report(rep)
