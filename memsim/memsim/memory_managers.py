
from abc import ABC, abstractmethod
from physical_memory import FixedSegPhysMem, VarSegPhysMem
from reporter import Reporter
from utils import MemoryAllocation

class MemoryManager(ABC):
    """Keeps track of each Job that it has given memory to in the dict allocations.
    The key is the name of the job and the value is a MemoryAllocation object.
    """

    @abstractmethod
    def __init__(self, memory_param):
        pass

    @abstractmethod
    def allocate_k(self, process, size):
        pass

    @abstractmethod
    def deallocate(self, process):
        pass

    @abstractmethod
    def __str__(self) -> str:
        pass

    @abstractmethod
    def report(self, rep: Reporter):
        pass

class VarSegMm(MemoryManager):

    def __init__(self, memory_param) -> None:
        self.physical_memory = VarSegPhysMem(memory_param)
        self.allocations: dict[str, MemoryAllocation] = {}
        super().__init__(memory_param)

    def allocate_k(self, process, size):
        block = self.physical_memory.allocate(size)
        if block is None:
            raise Exception("Allocation failed to find space")
        self.allocations[process] = MemoryAllocation(process, block)

    def deallocate(self, process):
        allocation = self.allocations[process]
        if allocation is None:
            raise "process not found"
        self.physical_memory.deallocate(allocation.block)
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

class FixedSegMm(MemoryManager):
    """Keeps track of each Job that it has given memory to in the dict allocations.
    The key is the name of the job and the value is a MemoryAllocation object.
    """

    def __init__(self, memory_param) -> None:
        self.physical_memory = FixedSegPhysMem(memory_param)
        self.allocations: dict[str, MemoryAllocation] = {}

        
    def allocate_k(self, process: str, size: int):
        block = self.physical_memory.allocate(size)
        if block is None:
            raise Exception(f"Allocation request {size} for process {process} failed")
        self.allocations[process] = MemoryAllocation(process, block)
  
    def deallocate(self, process: str, size: int):
        assert size == self.allocations[process].block.size, "Invalid deallocate"
        allocation = self.allocations[process]
        if allocation is None:
            raise Exception("process not found")
        self.physical_memory.deallocate(allocation.block)
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

  