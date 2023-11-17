from reporter import Reporter
from utils import Block, PageTable, convert_size_with_multiplier, find_and_remove, flatten_free_segments
from abc import ABC, abstractmethod
class PhysMem(ABC):
    def __init__(self, args):
        pass
        
    @abstractmethod
    def __str__(self):
        return "Default memory manager string"

    @abstractmethod
    def allocate(self, size):
        pass

    @abstractmethod
    def deallocate(self, mapping: Block | PageTable):
        pass

    @abstractmethod
    def touch(self, address: int) -> bool:
        return True

class VarSegPhysMem(PhysMem):
    def __init__(self, args):
        self.size = convert_size_with_multiplier(args["memory"]["size"])
        self.freelist = [Block(0, self.size)]
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

    def allocate(self, size: int) -> Block | None:
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

class FixedSegPhysMem(PhysMem):
    def __init__(self, args: dict):
        super().__init__(args)
        self.memsize = convert_size_with_multiplier(args["memory"]["size"])
        self.segsize = convert_size_with_multiplier(args["memory"]["seg"])
        self.seg_count = self.memsize // self.segsize
        if self.memsize % self.segsize != 0:
            raise Exception("Memory size must be a multiple of segment size")
        self.free_segments = [i for i in range(self.seg_count)]
        self.seg_table = [None] * self.seg_count

    def __str__(self):
        return str(flatten_free_segments(self.free_segments))

    def allocate(self, process: str,  size: int) -> Block | None:
        segments = self.find_contiguous_segments(size, self.free_segments)
        if segments is None:
            return None
        else:
            self.free_segments = segments[1]
            for seg in segments[0]:
                self.seg_table[seg] = process
            self.seg_table[segments[0][0]] = process
            return Block(segments[0][0]*self.segsize, size)
        
    def find_contiguous_segments(self, size, free_list) -> list[list[int]] | None:
        segs_needed = size // self.segsize
        return find_and_remove(free_list, segs_needed)
        
    def deallocate(self, block: Block) -> None:
        for i in range(block.size// self.segsize):
            self.free_segments.append(block.physical_address//self.segsize + i)
            self.seg_table[block.physical_address//self.segsize + i] = None
        self.free_segments.sort()

    def report(self, rep: Reporter):
        flattened = flatten_free_segments(self.free_segments)
        rep.add_free_segments(flattened)
        rep.add_seg_mem_stats(self.memsize, self.segsize)

    def touch(self, alloc: Block, address: int) -> bool:
        return alloc.contains(address)


class PagedPhysMem(PhysMem):
    def __init__(self, memory_param: dict, page_size: int):
        super().__init__(memory_param)
        self.memparam = memory_param
        self.memsize = convert_size_with_multiplier(memory_param["memory"]["size"])
        self.pagesize = page_size
        if self.memsize % self.pagesize != 0:
            raise Exception("Memory size must be a multiple of page size")
        self.frame_count = self.memsize // self.pagesize
        self.frame_table = [None] * self.frame_count

    def __str__(self):
        return f"PhysicalMemory = {self.memsize} MB"
    
    def allocate(self, process: str, size: int) -> PageTable | None:
        required_frames = size // self.pagesize
        if size % self.pagesize != 0:
            required_frames += 1
        return self.build_page_table(process, required_frames)
 
    def deallocate(self, mapping: PageTable) -> None:
        for frame in mapping.table:
            self.frame_table[frame] = None
        pass

    def build_page_table(self, process: str, n_frames: int) -> PageTable | None:
        page_table =  PageTable(self.pagesize)
        for index, frame in enumerate(self.frame_table):
            if frame is not None:
                continue
            page_table.add_frame(index)
            self.frame_table[index] = process
            n_frames -= 1
            if n_frames == 0:
                return page_table
        return None

    def report(self, rep: Reporter):
        rep.add_paged_memory_stats(self.memsize, self.pagesize, self.frame_count, self.frame_table)

    def touch(self, address: int) -> bool:
        return True
    

