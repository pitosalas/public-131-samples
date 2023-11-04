from utils import Block, find_and_remove
from abc import ABC, abstractmethod

class PhysMem(ABC):
    def __init__(self, args):
        pass
        
    @abstractmethod
    def __str__(self):
        return "Default memory manager string"

    def free_memory(self) -> int:
        return 0

    @abstractmethod
    def allocate(self, size):
        pass

    @abstractmethod
    def deallocate(self, block):
        pass
class VarSegPhysMem(PhysMem):
    def __init__(self, args):
        self.freelist = [Block(0, args["size_gig"]*2**30)]
        self.size = args["size_gig"]*2**30
        super().__init__(args)

    def __str__(self):
        memory_in_meg = self.size / 2**20
        free_in_meg = self.free_memory() / 2**20
        return f"PhysicalMemory = {memory_in_meg} MB, Total Free = {free_in_meg} MB"
    
    def find_free_block(self, size) -> Block | None :
        for block in self.freelist:
            if block.size >= size:
                return block
        return None

    def free_memory(self) -> int:
        total_free = 0
        for block in self.freelist:
            total_free += block.size
        return total_free

    def allocate(self, size) -> Block | None:
        pass
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
            self.freelist.append(
                Block(
                    block.start + size,
                    block.size - size,
                )
            )
            block.size = size
            return block

    def deallocate(self, block) -> None:
        """
        * Add the block to the free list
        * Sort the free list by starting address

        """
        self.freelist.append(block)
        self.freelist.sort(key=lambda block: block.start)
        self.coalesce()

    def coalesce(self) -> None:
        """
        * Look for adjacent free blocks and combine them into one block
        * Repeat until no more adjacent free blocks are found

        """
        while True:
            found = False
            for i in range(len(self.freelist) - 1):
                block1 = self.freelist[i]
                block2 = self.freelist[i + 1]
                if block1.start + block1.size == block2.start:
                    self.freelist.remove(block1)
                    self.freelist.remove(block2)
                    self.freelist.append(
                        Block(
                            block1.start,
                            block1.size + block2.size,
                        )
                    )
                    self.freelist.sort(key=lambda block: block.start)
                    found = True
                    break
            if not found:
                break


 
class FixedSegPhysMem(PhysMem):
    def __init__(self, args: dict):
        super().__init__(args)
        self.memsize = args["size"]*2**args["size_power_of_two"]
        self.segsize = args["seg_size"]*2**args["seg_size_power_of_two"]
        if self.memsize % self.segsize != 0:
            raise Exception("Memory size must be a multiple of segment size")
        self.free_segments = [i for i in range(self.memsize//self.segsize)]

    def __str__(self):
        return "Default fixed memory manager string"


    def allocate(self, size) -> Block | None:
        segments = self.find_contiguous_segments(size, self.free_segments)
        if segments is None:
            return None
        else:
            self.free_segments = segments[1]
            return Block(segments[0][0]*self.segsize, size)
        
    def find_contiguous_segments(self, size, free_list) -> list[list[int]] | None:
        segs_needed = size // self.segsize
        return find_and_remove(free_list, segs_needed)
        
    def deallocate(self, block) -> None:
        pass

