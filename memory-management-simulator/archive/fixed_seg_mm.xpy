from abc import ABC, abstractmethod
from physical_memory import VarSegPhysMem
from utils import MemoryAllocation


class MemoryManager(ABC):
    """Keeps track of each Job that it has given memory to in the dict allocations.
    The key is the name of the job and the value is a MemoryAllocation object.
    """

    @abstractmethod
    def __init__(self, size_gig):
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

class VarSegMm(MemoryManager):

    def __init__(self, size_gig) -> None:
        self.physical_memory = VarSegPhysMem(size_gig * 2**30)
        self.allocations: dict[str, MemoryAllocation] = {}
        super().__init__(size_gig)

    def allocate_k(self, process, size):
        block = self.physical_memory.allocate(size * 2**10)
        if block is None:
            raise "memory cannot be allocated"
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
        return f"MemoryManager:\n   Processes:\n         {allocations}\n   {phys_memory}\n   Free Blocks:\n    {freeblocks}"
