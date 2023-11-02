"""
A simple memory magement simulation and demonstration app.

class PhysicalMemory
    - total number of bytes

class ProcessMemort
    - Size

class VirtualMapping
    - range in physical memory used
    - reference to the process memory

class MemoryAssignmentRequest
    - how much memory is requested
    - for what process

class MemoryManager
    - Methods to allocate a block of memory for a process
"""


class Block:
    def __init__(self, start, size):
        self.start = start
        self.size = size

    def __str__(self):
        return f"Block: start = {self.start/2**10}K, size = {self.size/2**20} M"


class PhysicalMemory:
    def __init__(self, size: int):
        self.size = size
        self.freelist = [Block(0, size)]

    def __str__(self):
        memory_in_meg = self.size / 2**20
        free_in_meg = self.free_memory() / 2**20
        return f"PhysicalMemory = {memory_in_meg} MB, Total Free = {free_in_meg} MB"

    def free_memory(self):
        total_free = 0
        for block in self.freelist:
            total_free += block.size
        return total_free

    def find_free_block(self, size):
        for block in self.freelist:
            if block.size >= size:
                return block
        return None

    def allocate(self, size):
        """
        * Look for a free block of memory that is at least as big as the requested size.
        * If none found, then allocation fails
        * If one found of exactly the right size, then that free block is removed from
        the free list and returned as the allocated block
        * If one found that is bigger than the requested size, then the free block is split into
        two blocks, the first of which is returned as the allocated block and the second of which
        is added to the free list.

        """
        block = self.find_free_block(size)
        if block is None:
            return None
        if block.size == size:
            self.freelist.remove(block)
            return block
        else:
            self.freelist.remove(block)
            self.freelist.append(Block(block.start + size, block.size - size))
            block.size = size
            return block


class MemoryManager:
    """Keeps track of each Job that it has given memory to in the dict allocations.
    The key is the name of the job and the value is a MemoryAllocation object.

    """

    def __init__(self, physical_memory):
        self.physical_memory = physical_memory
        self.allocations: dict(str, MemoryAllocation) = {}

    def allocate_k(self, process, size):
        block = self.physical_memory.allocate(size * 2**10)
        if block is None:
            raise "memory cannot be allocated"
        self.allocations[process] = MemoryAllocation(process, block)

    def deallocate(self, process):
        pass

    def __str__(self) -> str:
        phys_memory = str(self.physical_memory)
        allocations = "\n         ".join(
            str(alloc) for alloc in self.allocations.values()
        )
        freeblocks = "\n      ".join(
            str(block) for block in self.physical_memory.freelist
        )
        return f"MemoryManager:\n   Processes:\n         {allocations}\n   Free Blocks:\n         {freeblocks}\n         {phys_memory}"


class MemoryAllocation:
    def __init__(self, process, block):
        self.block = block
        self.process = process

    def __str__(self):
        return f"Proc: {self.process} has: {self.block.size/2**10} (@ phys_addr: {self.block.start/2**10}K)"


class Simulator:
    def __init__(self):
        pass

    def add_process(self, process):
        self.processes.append(process)

    def add_virtual_mapping(self, mapping):
        self.virtual_mappings.append(mapping)

    def run(self):
        self.physical_memory = PhysicalMemory((2**30))
        self.mmanager = MemoryManager(self.physical_memory)
        self.mmanager.allocate_k("p1", 512)
        self.mmanager.allocate_k("p2", 1024)
        self.mmanager.allocate_k("p3", 368)
        print(self.mmanager)


if __name__ == "__main__":
    sim = Simulator()
    sim.run()

# what is one gig as a power of 2
