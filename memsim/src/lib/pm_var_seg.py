from lib.pagetables import Block
from lib.pm_base import PhysMem
from lib.reporter import Reporter
from lib.utils import convert_size_with_multiplier


class VarSegPhysMem(PhysMem):
    def __init__(self, args):
        super().__init__(args)
        self.size = convert_size_with_multiplier(args["memory"]["size"])
        self.freelist = [Block(0, self.size)]

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

    def allocate(self, size: int) -> Block | None:
        """
        Look for a free block of memory that is at least as big as the requested size. If none found, then allocation fails. If one found of exactly the right size, then that free block is removed from the free list and returned as the allocated block If one found that is bigger than the requested size, then the free block is split into two blocks, the first of which is returned as the allocated block and the second of which is added to the free list.
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
                    block.physical_address + size,
                    block.size - size,
                )
            )
            block.size = size
            return block

    def touch(self, address: int) -> bool:
        return True
    
    def deallocate(self, mapping) -> None:
        """
        * Add the block to the free list
        * Sort the free list by starting address

        """
        self.freelist.append(mapping)
        self.freelist.sort(key=lambda block: block.physical_address)
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
                if block1.physical_address + block1.size == block2.physical_address:
                    self.freelist.remove(block1)
                    self.freelist.remove(block2)
                    self.freelist.append(
                        Block(
                            block1.physical_address,
                            block1.size + block2.size,
                        )
                    )
                    self.freelist.sort(key=lambda block: block.physical_address)
                    found = True
                    break
            if not found:
                break
 
    def report(self, rep: Reporter):
        rep.add_free_segments(self.freelist)
        return super().report(rep)

