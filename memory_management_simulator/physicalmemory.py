from utils import Block


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

    def deallocate(self, block):
        """
        * Add the block to the free list
        * Sort the free list by starting address

        """
        self.freelist.append(block)
        self.freelist.sort(key=lambda block: block.start)
        self.coalesce()
    
    def coalesce(self):
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
                    self.freelist.append(Block(block1.start, block1.size + block2.size))
                    self.freelist.sort(key=lambda block: block.start)
                    found = True
                    break
            if not found:
                break
            