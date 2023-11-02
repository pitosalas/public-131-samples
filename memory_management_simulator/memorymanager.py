from physicalmemory import PhysicalMemory
from utils import MemoryAllocation


class MemoryManager:
    """Keeps track of each Job that it has given memory to in the dict allocations.
    The key is the name of the job and the value is a MemoryAllocation object.

    """

    def __init__(self, size_gig):
        self.physical_memory = PhysicalMemory(
            size_gig * 2**30
        )
        self.allocations: dict(
            str, MemoryAllocation
        ) = {}

    def allocate_k(self, process, size):
        block = self.physical_memory.allocate(
            size * 2**10
        )
        if block is None:
            raise "memory cannot be allocated"
        self.allocations[
            process
        ] = MemoryAllocation(process, block)

    def deallocate(self, process):
        allocation = self.allocations[process]
        if allocation is None:
            raise "process not found"
        self.physical_memory.deallocate(
            allocation.block
        )
        del self.allocations[process]

    def __str__(self) -> str:
        phys_memory = str(self.physical_memory)
        allocations = "\n         ".join(
            str(alloc)
            for alloc in self.allocations.values()
        )
        freeblocks = "\n      ".join(
            str(block)
            for block in self.physical_memory.freelist
        )
        return f"""MemoryManager:\n   Processes:\n         {allocations}\n   Free Blocks:\n         {freeblocks}\n         {phys_memory}"""
